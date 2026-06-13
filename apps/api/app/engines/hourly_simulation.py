"""Pure 8760-style hourly energy simulation primitives."""

from dataclasses import dataclass
from typing import Dict, List, Literal, Optional, Sequence, Tuple


RateKind = Literal["flat", "tou", "tiered"]


@dataclass(frozen=True)
class BatterySpec:
    usable_kwh: float
    power_kw: float
    round_trip_efficiency: float
    reserve_floor_kwh: float = 0.0


@dataclass(frozen=True)
class RateStructure:
    kind: RateKind
    flat_import_rate: float = 0.0
    export_rate: float = 0.0
    tou_import_rates: Optional[Sequence[float]] = None
    tiered_import_rates: Optional[Sequence[Tuple[float, float]]] = None


@dataclass(frozen=True)
class HourlyEnergyFlow:
    hour_index: int
    load_kwh: float
    solar_kwh: float
    battery_charge_kwh: float
    battery_discharge_kwh: float
    battery_soc_kwh: float
    grid_import_kwh: float
    grid_export_kwh: float


@dataclass(frozen=True)
class HourlySimulationResult:
    hours: Tuple[HourlyEnergyFlow, ...]
    annual_load_kwh: float
    annual_solar_kwh: float
    annual_grid_import_kwh: float
    annual_grid_export_kwh: float
    self_consumption_percent: float
    annual_bill: float
    annual_bill_without_system: float
    annual_bill_delta: float
    battery_cycles_per_year: float
    backup_coverage_hours: float
    peak_import_kw: float
    peak_export_kw: float
    confidence_tier: str
    confidence_basis: Tuple[str, ...]


def run_hourly_simulation(
    load_profile_kwh: Sequence[float],
    solar_profile_kwh: Sequence[float],
    battery: BatterySpec,
    rate: RateStructure,
    critical_load_profile_kwh: Optional[Sequence[float]] = None,
    starting_soc_kwh: Optional[float] = None,
    input_confidence_tiers: Optional[Sequence[str]] = None,
) -> HourlySimulationResult:
    """Run a deterministic hourly solar/battery/grid simulation.

    The caller provides profiles; this engine does not fetch weather, rates,
    utility tariffs, or equipment data.
    """
    if len(load_profile_kwh) != len(solar_profile_kwh):
        raise ValueError("load_profile_kwh and solar_profile_kwh must have the same length")
    if not load_profile_kwh:
        raise ValueError("profiles must contain at least one hour")
    if battery.usable_kwh < battery.reserve_floor_kwh:
        raise ValueError("battery reserve floor cannot exceed usable capacity")

    soc = starting_soc_kwh if starting_soc_kwh is not None else battery.usable_kwh
    soc = min(max(soc, battery.reserve_floor_kwh), battery.usable_kwh)
    charge_efficiency = battery.round_trip_efficiency ** 0.5
    discharge_efficiency = battery.round_trip_efficiency ** 0.5

    flows: List[HourlyEnergyFlow] = []
    total_discharge = 0.0
    for hour, (load, solar) in enumerate(zip(load_profile_kwh, solar_profile_kwh)):
        net = solar - load
        charge = 0.0
        discharge = 0.0
        grid_import = 0.0
        grid_export = 0.0
        if net >= 0:
            charge_room = battery.usable_kwh - soc
            charge = min(net, battery.power_kw, charge_room / charge_efficiency if charge_efficiency else 0)
            soc += charge * charge_efficiency
            grid_export = net - charge
        else:
            needed = -net
            available = max(soc - battery.reserve_floor_kwh, 0.0)
            discharge = min(needed / discharge_efficiency if discharge_efficiency else 0, battery.power_kw, available)
            delivered = discharge * discharge_efficiency
            soc -= discharge
            grid_import = needed - delivered
            total_discharge += discharge

        flows.append(
            HourlyEnergyFlow(
                hour_index=hour,
                load_kwh=round(load, 6),
                solar_kwh=round(solar, 6),
                battery_charge_kwh=round(charge, 6),
                battery_discharge_kwh=round(discharge, 6),
                battery_soc_kwh=round(soc, 6),
                grid_import_kwh=round(max(grid_import, 0.0), 6),
                grid_export_kwh=round(max(grid_export, 0.0), 6),
            )
        )

    annual_load = sum(load_profile_kwh)
    annual_solar = sum(solar_profile_kwh)
    annual_import = sum(flow.grid_import_kwh for flow in flows)
    annual_export = sum(flow.grid_export_kwh for flow in flows)
    solar_used_on_site = max(annual_solar - annual_export, 0.0)
    bill = _bill_for_profile(tuple(flow.grid_import_kwh for flow in flows), rate) - annual_export * rate.export_rate
    no_system_bill = _bill_for_profile(load_profile_kwh, rate)
    backup_profile = critical_load_profile_kwh or load_profile_kwh
    return HourlySimulationResult(
        hours=tuple(flows),
        annual_load_kwh=round(annual_load, 4),
        annual_solar_kwh=round(annual_solar, 4),
        annual_grid_import_kwh=round(annual_import, 4),
        annual_grid_export_kwh=round(annual_export, 4),
        self_consumption_percent=round((solar_used_on_site / annual_solar * 100) if annual_solar else 0.0, 2),
        annual_bill=round(bill, 2),
        annual_bill_without_system=round(no_system_bill, 2),
        annual_bill_delta=round(no_system_bill - bill, 2),
        battery_cycles_per_year=round(total_discharge / battery.usable_kwh if battery.usable_kwh else 0.0, 4),
        backup_coverage_hours=round(_backup_coverage_hours(backup_profile, battery), 2),
        peak_import_kw=round(max((flow.grid_import_kwh for flow in flows), default=0.0), 4),
        peak_export_kw=round(max((flow.grid_export_kwh for flow in flows), default=0.0), 4),
        confidence_tier=_weakest_confidence(input_confidence_tiers or ["missing"]),
        confidence_basis=tuple(input_confidence_tiers or ["missing"]),
    )


def _bill_for_profile(import_profile_kwh: Sequence[float], rate: RateStructure) -> float:
    if rate.kind == "flat":
        return sum(import_profile_kwh) * rate.flat_import_rate
    if rate.kind == "tou":
        if not rate.tou_import_rates or len(rate.tou_import_rates) != 24:
            raise ValueError("tou_import_rates must contain 24 hourly rates")
        return sum(kwh * rate.tou_import_rates[index % 24] for index, kwh in enumerate(import_profile_kwh))
    if rate.kind == "tiered":
        if not rate.tiered_import_rates:
            raise ValueError("tiered_import_rates are required for tiered rates")
        remaining = sum(import_profile_kwh)
        total = 0.0
        for limit_kwh, price in rate.tiered_import_rates:
            if remaining <= 0:
                break
            consumed = min(remaining, limit_kwh)
            total += consumed * price
            remaining -= consumed
        if remaining > 0:
            total += remaining * rate.tiered_import_rates[-1][1]
        return total
    raise ValueError(f"Unsupported rate kind: {rate.kind}")


def _backup_coverage_hours(profile_kwh: Sequence[float], battery: BatterySpec) -> float:
    available = max(battery.usable_kwh - battery.reserve_floor_kwh, 0.0)
    covered = 0.0
    for load in profile_kwh:
        if load <= 0:
            covered += 1
            continue
        if available >= load:
            available -= load
            covered += 1
        else:
            covered += available / load
            break
    return covered


def _weakest_confidence(tiers: Sequence[str]) -> str:
    order: Dict[str, int] = {"known": 4, "derived": 3, "assumed": 2, "missing": 1}
    return min(tiers, key=lambda tier: order.get(tier, 1))

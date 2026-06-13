"""Pure sizing primitives for battery, generator, V2H, and transformer checks."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class BatterySizingResult:
    required_usable_kwh: float
    required_nameplate_kwh: float
    recommended_capacity_band_kwh: Tuple[float, float]
    assumptions: Tuple[str, ...]
    confidence_tier: str


@dataclass(frozen=True)
class GeneratorSizingResult:
    continuous_kw: float
    surge_kw: float
    recommended_kw: float
    mode: str
    assumptions: Tuple[str, ...]
    confidence_tier: str


@dataclass(frozen=True)
class V2HCoverageResult:
    coverage_hours: float
    power_limited: bool
    architecture_implication: str
    assumptions: Tuple[str, ...]
    confidence_tier: str


@dataclass(frozen=True)
class TransformerHeadroomResult:
    transformer_capacity_kw: float
    proposed_peak_kw: float
    headroom_kw: float
    status: str
    assumptions: Tuple[str, ...]
    confidence_tier: str


def size_battery(
    critical_load_kwh_per_hour: float,
    target_autonomy_hours: float,
    round_trip_efficiency: float,
    depth_of_discharge_fraction: float,
    confidence_tier: str,
) -> BatterySizingResult:
    usable = critical_load_kwh_per_hour * target_autonomy_hours / round_trip_efficiency
    nameplate = usable / depth_of_discharge_fraction
    return BatterySizingResult(
        required_usable_kwh=round(usable, 2),
        required_nameplate_kwh=round(nameplate, 2),
        recommended_capacity_band_kwh=(round(nameplate * 0.95, 2), round(nameplate * 1.15, 2)),
        assumptions=(
            f"round_trip_efficiency={round_trip_efficiency}",
            f"depth_of_discharge_fraction={depth_of_discharge_fraction}",
            "No SGIP, 25D, 48E, pricing, quote, or eligibility assumption is included.",
        ),
        confidence_tier=confidence_tier,
    )


def size_generator(
    continuous_load_kw: float,
    surge_load_kw: float,
    derate_factor: float,
    mode: str,
    confidence_tier: str,
) -> GeneratorSizingResult:
    if derate_factor <= 0:
        raise ValueError("derate_factor must be positive")
    required = max(continuous_load_kw, surge_load_kw) / derate_factor
    if mode == "hybrid":
        required = max(continuous_load_kw / derate_factor, surge_load_kw * 0.6 / derate_factor)
    return GeneratorSizingResult(
        continuous_kw=round(continuous_load_kw, 2),
        surge_kw=round(surge_load_kw, 2),
        recommended_kw=round(required, 2),
        mode=mode,
        assumptions=(f"derate_factor={derate_factor}", "Hybrid mode assumes battery helps absorb surge."),
        confidence_tier=confidence_tier,
    )


def size_v2h_coverage(
    vehicle_usable_kwh: float,
    discharge_power_kw: float,
    critical_load_kw: float,
    confidence_tier: str,
) -> V2HCoverageResult:
    if critical_load_kw <= 0:
        raise ValueError("critical_load_kw must be positive")
    coverage = vehicle_usable_kwh / critical_load_kw
    power_limited = discharge_power_kw < critical_load_kw
    return V2HCoverageResult(
        coverage_hours=round(coverage, 2),
        power_limited=power_limited,
        architecture_implication="V2H transfer equipment review" if not power_limited else "V2H/V2L power-limit review",
        assumptions=("Vehicle pack usability and discharge limit are caller-provided.",),
        confidence_tier=confidence_tier,
    )


def check_transformer_headroom(
    transformer_kva: float,
    proposed_peak_kw: float,
    existing_peak_kw: float,
    power_factor: float,
    confidence_tier: str,
) -> TransformerHeadroomResult:
    if power_factor <= 0:
        raise ValueError("power_factor must be positive")
    capacity_kw = transformer_kva * power_factor
    total_peak = proposed_peak_kw + existing_peak_kw
    headroom = capacity_kw - total_peak
    if headroom >= capacity_kw * 0.15:
        status = "headroom_available"
    elif headroom >= 0:
        status = "tight_review_needed"
    else:
        status = "utility_review_needed"
    return TransformerHeadroomResult(
        transformer_capacity_kw=round(capacity_kw, 2),
        proposed_peak_kw=round(total_peak, 2),
        headroom_kw=round(headroom, 2),
        status=status,
        assumptions=("Transformer rating is caller-provided and not utility-verified.",),
        confidence_tier=confidence_tier,
    )

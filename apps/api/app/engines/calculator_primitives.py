"""Pure calculator primitives shared by sizing and simulation layers.

Every function in this module is deterministic and side-effect free. Inputs in,
typed values out: no database access, no app service imports, and no network
calls unless a caller injects a production-estimator function.
"""

from dataclasses import dataclass
from typing import Callable, Iterable, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class BackfeedRuleResult:
    bus_rating_amps: float
    main_breaker_amps: float
    maximum_backfeed_amps: float
    requested_backfeed_amps: Optional[float]
    passes: bool
    supply_side_tap_alternative: bool
    reason: str


@dataclass(frozen=True)
class SupplySideTapResult:
    requested_backfeed_amps: float
    service_rating_amps: float
    planning_status: str
    required_review_items: Tuple[str, ...]
    reason: str


@dataclass(frozen=True)
class CouplingDecisionResult:
    recommended_coupling: str
    reasons: Tuple[str, ...]
    review_flags: Tuple[str, ...]


@dataclass(frozen=True)
class LoadCandidate:
    id: str
    name: str
    running_watts: float
    surge_watts: Optional[float]
    backup_priority: str


@dataclass(frozen=True)
class CriticalLoadsResult:
    selected_load_ids: Tuple[str, ...]
    continuous_watts: float
    peak_watts: float
    backup_goal: str
    reason: str


@dataclass(frozen=True)
class ShadingDerateResult:
    obstruction_points: Tuple[Tuple[float, float], ...]
    derate_fraction: float
    production_factor: float
    reason: str


@dataclass(frozen=True)
class SolarProductionResult:
    annual_kwh: float
    monthly_kwh: Tuple[float, ...]
    source: str
    derate_factor: float


def calculate_120_percent_backfeed(
    bus_rating_amps: float,
    main_breaker_amps: float,
    requested_backfeed_amps: Optional[float] = None,
) -> BackfeedRuleResult:
    """Apply the residential 120% busbar planning check.

    Returns the calculated load-side backfeed allowance and, when the request
    fails or the allowance is zero/negative, marks supply-side tap review as the
    alternative path.
    """
    maximum = round(bus_rating_amps * 1.2 - main_breaker_amps, 2)
    if requested_backfeed_amps is None:
        passes = maximum > 0
    else:
        passes = maximum >= requested_backfeed_amps and maximum > 0
    return BackfeedRuleResult(
        bus_rating_amps=bus_rating_amps,
        main_breaker_amps=main_breaker_amps,
        maximum_backfeed_amps=maximum,
        requested_backfeed_amps=requested_backfeed_amps,
        passes=passes,
        supply_side_tap_alternative=not passes,
        reason=(
            "Load-side backfeed fits the 120% planning check."
            if passes
            else "Load-side backfeed does not fit; supply-side tap review is the planning alternative."
        ),
    )


def calculate_supply_side_tap(
    service_rating_amps: float,
    requested_backfeed_amps: float,
) -> SupplySideTapResult:
    """Return planning review implications for a supply-side tap path."""
    if requested_backfeed_amps <= 0:
        status = "blocked"
        reason = "Requested backfeed must be greater than zero."
    elif requested_backfeed_amps > service_rating_amps:
        status = "requires_service_upgrade_review"
        reason = "Requested backfeed exceeds the recorded service rating."
    else:
        status = "requires_professional_review"
        reason = "Supply-side tap is a review path, not an automatic approval."
    return SupplySideTapResult(
        requested_backfeed_amps=requested_backfeed_amps,
        service_rating_amps=service_rating_amps,
        planning_status=status,
        required_review_items=(
            "service_conductor_rating",
            "tap_conductor_length_and_routing",
            "overcurrent_protection",
            "utility_and_AHJ_requirements",
        ),
        reason=reason,
    )


def decide_coupling(
    array_kw_dc: float,
    battery_kwh: float,
    has_existing_pv: bool,
    retrofit: bool,
) -> CouplingDecisionResult:
    """Choose a planning coupling direction from high-level system context."""
    reasons: List[str] = []
    flags: List[str] = []
    if has_existing_pv or retrofit:
        reasons.append("Existing or retrofit PV usually favors AC-coupled review.")
        recommendation = "ac_coupled"
    elif array_kw_dc >= 1.2 * max(battery_kwh / 4.0, 1.0):
        reasons.append("New PV-heavy build can justify DC-coupled or hybrid review.")
        recommendation = "dc_coupled_or_hybrid"
    else:
        reasons.append("Balanced new-build context can use hybrid architecture review.")
        recommendation = "hybrid_review"
    if array_kw_dc <= 0 or battery_kwh <= 0:
        flags.append("array_and_battery_sizes_must_be_positive")
    return CouplingDecisionResult(
        recommended_coupling=recommendation,
        reasons=tuple(reasons),
        review_flags=tuple(flags),
    )


def identify_critical_loads(
    loads: Iterable[LoadCandidate],
    backup_goal: str,
) -> CriticalLoadsResult:
    """Select critical-load subpanel candidates and summarize draw."""
    allowed_priorities = {"essential"}
    if backup_goal in {"partial_home", "whole_home", "resilience_balanced"}:
        allowed_priorities.add("preferred")
    if backup_goal == "whole_home":
        allowed_priorities.update({"optional", "non_backup"})

    selected = [load for load in loads if load.backup_priority in allowed_priorities]
    continuous = round(sum(load.running_watts for load in selected), 2)
    peak = round(sum(load.surge_watts if load.surge_watts is not None else load.running_watts for load in selected), 2)
    return CriticalLoadsResult(
        selected_load_ids=tuple(load.id for load in selected),
        continuous_watts=continuous,
        peak_watts=peak,
        backup_goal=backup_goal,
        reason="Selected loads by backup priority for the requested planning goal.",
    )


def tier1_shading_derate(
    obstruction_points: Sequence[Tuple[float, float]],
) -> ShadingDerateResult:
    """Convert manual horizon trace points to an annual production derate.

    Elevation values are clamped from 0 to 90 degrees. Zero elevation means no
    shading derate; all points at 90 degrees means 100% derate.
    """
    normalized = tuple((float(azimuth), min(max(float(elevation), 0.0), 90.0)) for azimuth, elevation in obstruction_points)
    if not normalized:
        return ShadingDerateResult(
            obstruction_points=normalized,
            derate_fraction=0.0,
            production_factor=1.0,
            reason="No obstruction points supplied; no tier-1 shading derate applied.",
        )
    average_elevation = sum(elevation for _, elevation in normalized) / len(normalized)
    derate = round(min(max(average_elevation / 90.0, 0.0), 1.0), 4)
    return ShadingDerateResult(
        obstruction_points=normalized,
        derate_fraction=derate,
        production_factor=round(1.0 - derate, 4),
        reason="Tier-1 derate is based on average clamped obstruction elevation.",
    )


def estimate_solar_production(
    array_kw_dc: float,
    derate_factor: float,
    monthly_specific_yield: Optional[Sequence[float]] = None,
    pvwatts_estimator: Optional[Callable[[float, float], Sequence[float]]] = None,
) -> SolarProductionResult:
    """Estimate monthly and annual production.

    ``pvwatts_estimator`` is injected by the caller when desired; this function
    never imports a client or calls the network on its own.
    """
    if pvwatts_estimator is not None:
        monthly = tuple(round(value, 2) for value in pvwatts_estimator(array_kw_dc, derate_factor))
        source = "injected_pvwatts_estimator"
    else:
        yield_values = monthly_specific_yield or (95, 105, 125, 135, 145, 150, 155, 150, 135, 120, 100, 90)
        monthly = tuple(round(array_kw_dc * value * derate_factor, 2) for value in yield_values)
        source = "simplified_specific_yield_model"
    return SolarProductionResult(
        annual_kwh=round(sum(monthly), 2),
        monthly_kwh=monthly,
        source=source,
        derate_factor=derate_factor,
    )

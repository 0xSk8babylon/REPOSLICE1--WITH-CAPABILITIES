"""Pure deterministic resilience calculations.

Extracted from ``app.services.resilience_recommendation`` so the math and its
coefficient tables have a single dependency-free home. Every function here is
a pure function: typed inputs in, typed results out — no DB access, no prose
generation, no service imports, no side effects.

Allowed imports: stdlib and ``app.core.types`` (pure enums only).
"""

from dataclasses import dataclass
from typing import Dict, Optional, Sequence, Tuple

from app.core.types import (
    AutonomyReservePosture,
    FutureGrowthMarginPosture,
    ReserveMarginPosture,
    SolarSizingPosture,
)

# ---------------------------------------------------------------------------
# Coefficient tables (the deterministic planning constants)
# ---------------------------------------------------------------------------

AUTONOMY_HOUR_RANGES: Dict[AutonomyReservePosture, Tuple[float, float]] = {
    AutonomyReservePosture.minimal: (4.0, 8.0),
    AutonomyReservePosture.standard: (8.0, 14.0),
    AutonomyReservePosture.elevated: (14.0, 24.0),
    AutonomyReservePosture.extended: (24.0, 36.0),
}

RESERVE_MARGIN_FACTORS: Dict[ReserveMarginPosture, Tuple[float, float]] = {
    ReserveMarginPosture.lean: (1.05, 1.12),
    ReserveMarginPosture.standard: (1.12, 1.22),
    ReserveMarginPosture.elevated: (1.22, 1.35),
    ReserveMarginPosture.robust: (1.35, 1.5),
}

GROWTH_MARGIN_FACTORS: Dict[FutureGrowthMarginPosture, Tuple[float, float]] = {
    FutureGrowthMarginPosture.tight: (1.0, 1.08),
    FutureGrowthMarginPosture.planned: (1.08, 1.18),
    FutureGrowthMarginPosture.expansion_oriented: (1.18, 1.3),
    FutureGrowthMarginPosture.future_ready: (1.3, 1.45),
}

SOLAR_PRODUCTION_FACTORS: Dict[SolarSizingPosture, Tuple[float, float]] = {
    SolarSizingPosture.load_matched: (0.52, 0.72),
    SolarSizingPosture.resilience_balanced: (0.68, 0.9),
    SolarSizingPosture.recovery_weighted: (0.88, 1.12),
    SolarSizingPosture.future_weighted: (1.05, 1.32),
}

# Battery-recovery credit applied when deriving solar recovery need from the
# recommended battery range (previously inline magic numbers).
BATTERY_RECOVERY_MIN_CREDIT = 0.55
BATTERY_RECOVERY_MAX_CREDIT = 0.75
BACKUP_ENERGY_MAX_UPLIFT = 1.1

DEFAULT_FALLBACK_DAILY_HOURS = 4.0


def round_range(value: float) -> float:
    """Round a capacity-range bound to one decimal place."""
    return round(value, 1)


def backup_load_energy_need_kwh(
    load_demands: Sequence[Tuple[float, Optional[float]]],
    fallback_daily_hours: float = DEFAULT_FALLBACK_DAILY_HOURS,
) -> Optional[float]:
    """Daily energy need (kWh) for the selected backup loads.

    ``load_demands`` is a sequence of ``(running_watts, estimated_daily_hours)``
    pairs; ``estimated_daily_hours`` may be None, in which case the fallback
    applies. Returns None when no loads are selected.
    """
    if not load_demands:
        return None
    total_kwh = 0.0
    for running_watts, estimated_daily_hours in load_demands:
        daily_hours = estimated_daily_hours if estimated_daily_hours is not None else fallback_daily_hours
        total_kwh += (running_watts * daily_hours) / 1000
    return round(total_kwh, 2)


def backup_coverage_ratio(selected_load_count: int, total_recorded_load_count: int) -> Optional[float]:
    """Share of recorded loads covered by the selected backup scope."""
    if not total_recorded_load_count:
        return None
    return round(selected_load_count / total_recorded_load_count, 2)


@dataclass(frozen=True)
class BatterySizingRanges:
    usable_min_kwh: float
    usable_max_kwh: float
    recommended_min_kwh: float
    recommended_max_kwh: float


def battery_capacity_ranges(
    backup_energy_need_kwh: Optional[float],
    autonomy_reserve_posture: AutonomyReservePosture,
    reserve_margin_posture: ReserveMarginPosture,
    future_growth_margin_posture: FutureGrowthMarginPosture,
) -> Optional[BatterySizingRanges]:
    """Usable and recommended battery capacity ranges (kWh, rounded).

    Converts daily energy need into autonomy-window energy, then layers
    reserve and future-growth posture factors. Returns None when no backup
    energy need is known.
    """
    if backup_energy_need_kwh is None:
        return None
    autonomy_min, autonomy_max = AUTONOMY_HOUR_RANGES[autonomy_reserve_posture]
    reserve_min, reserve_max = RESERVE_MARGIN_FACTORS[reserve_margin_posture]
    growth_min, growth_max = GROWTH_MARGIN_FACTORS[future_growth_margin_posture]

    autonomy_energy_min = backup_energy_need_kwh * (autonomy_min / 24.0)
    autonomy_energy_max = backup_energy_need_kwh * (autonomy_max / 24.0)
    usable_min = autonomy_energy_min * reserve_min
    usable_max = autonomy_energy_max * reserve_max
    recommended_min = usable_min * growth_min
    recommended_max = usable_max * growth_max
    return BatterySizingRanges(
        usable_min_kwh=round_range(usable_min),
        usable_max_kwh=round_range(usable_max),
        recommended_min_kwh=round_range(recommended_min),
        recommended_max_kwh=round_range(recommended_max),
    )


@dataclass(frozen=True)
class SolarSizingRanges:
    base_recommended_min_kw: float
    base_recommended_max_kw: float
    recommended_min_kw: float
    recommended_max_kw: float


def solar_capacity_ranges(
    backup_energy_need_kwh: Optional[float],
    battery_recommended_min_kwh: Optional[float],
    battery_recommended_max_kwh: Optional[float],
    solar_sizing_posture: SolarSizingPosture,
    site_factor_range: Tuple[float, float],
    shading_factor_range: Tuple[float, float],
    seasonal_factor_range: Tuple[float, float],
    install_factor_range: Tuple[float, float],
) -> Optional[SolarSizingRanges]:
    """Base and site-adjusted solar capacity ranges (kW, rounded).

    Derives the recovery burden from backup energy need and the recommended
    battery range, applies the posture's production factors, then the four
    site-aware caution factor ranges. Returns None when the battery inputs
    are unavailable.
    """
    if (
        backup_energy_need_kwh is None
        or battery_recommended_min_kwh is None
        or battery_recommended_max_kwh is None
    ):
        return None
    solar_min_factor, solar_max_factor = SOLAR_PRODUCTION_FACTORS[solar_sizing_posture]

    base_recovery_need_min = max(backup_energy_need_kwh, battery_recommended_min_kwh * BATTERY_RECOVERY_MIN_CREDIT)
    base_recovery_need_max = max(
        backup_energy_need_kwh * BACKUP_ENERGY_MAX_UPLIFT,
        battery_recommended_max_kwh * BATTERY_RECOVERY_MAX_CREDIT,
    )
    base_recommended_min = base_recovery_need_min * solar_min_factor
    base_recommended_max = base_recovery_need_max * solar_max_factor

    site_factor_min, site_factor_max = site_factor_range
    shading_factor_min, shading_factor_max = shading_factor_range
    seasonal_factor_min, seasonal_factor_max = seasonal_factor_range
    install_factor_min, install_factor_max = install_factor_range

    recommended_min = (
        base_recommended_min * site_factor_min * shading_factor_min * seasonal_factor_min * install_factor_min
    )
    recommended_max = (
        base_recommended_max * site_factor_max * shading_factor_max * seasonal_factor_max * install_factor_max
    )
    return SolarSizingRanges(
        base_recommended_min_kw=round_range(base_recommended_min),
        base_recommended_max_kw=round_range(base_recommended_max),
        recommended_min_kw=round_range(recommended_min),
        recommended_max_kw=round_range(recommended_max),
    )

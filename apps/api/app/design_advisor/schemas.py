from typing import Dict, List, Optional

from pydantic import Field

from app.core.schemas import ORMModel
from app.core.types import (
    AutonomyReservePosture,
    BatterySizingPosture,
    ConfidenceLevel,
    DataOrigin,
    FutureGrowthMarginPosture,
    LowSolarAssumptionPosture,
    RecoveryStrengthPosture,
    ReserveMarginPosture,
    RecommendationProfile,
    SeasonalConservatismPosture,
    SolarSizingPosture,
)


class BatteryCapacityRange(ORMModel):
    min_kwh: float
    max_kwh: float


class InspectabilitySignal(ORMModel):
    key: str
    label: str
    value: str
    status: str
    note: Optional[str] = None


class EstimateInspectability(ORMModel):
    basis: str
    confidence_level: ConfidenceLevel
    trust_state: DataOrigin = DataOrigin.derived_estimate
    rule_keys: List[str] = Field(default_factory=list)
    input_signals: List[InspectabilitySignal] = Field(default_factory=list)
    estimated_inputs: List[str] = Field(default_factory=list)
    incomplete_inputs: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)
    partial_provenance_warning: Optional[str] = None


class ArchitectureConsistencyCheck(ORMModel):
    status: str
    summary: str
    reason: str
    warnings: List[str] = Field(default_factory=list)


class BackupLoadSelectionSummary(ORMModel):
    selected_scope_label: str
    selection_basis: str
    selected_priority_band: str
    selected_load_count: int
    recorded_essential_load_count: int
    recorded_preferred_load_count: int
    recorded_total_load_count: int
    coverage_ratio_of_recorded_loads: Optional[float] = None
    outage_posture: str
    outage_posture_reason: str
    confidence_level: ConfidenceLevel
    confidence_reason: str
    selection_reason: str
    planning_gap_warning: Optional[str] = None
    scope_note: str
    inspectability: Optional[EstimateInspectability] = None


class PanelServiceArchitectureEstimate(ORMModel):
    main_service_panel_posture: str
    panel_upgrade_likelihood: str
    service_upgrade_caution: str
    critical_loads_subpanel_suitability: str
    partial_home_backup_suitability: str
    whole_home_backup_suitability: str
    smart_panel_readiness_note: str
    generator_integration_readiness_note: str
    recommended_backup_architecture: str
    scope_note: str
    architecture_consistency: Optional[ArchitectureConsistencyCheck] = None
    inspectability: Optional[EstimateInspectability] = None


class BatterySizingEstimate(ORMModel):
    backup_load_energy_need_kwh: Optional[float] = None
    autonomy_duration_hours_min: float
    autonomy_duration_hours_max: float
    usable_battery_capacity_range_kwh: Optional[BatteryCapacityRange] = None
    reserve_margin_posture: ReserveMarginPosture
    future_growth_margin_posture: FutureGrowthMarginPosture
    recommended_battery_capacity_range_kwh: Optional[BatteryCapacityRange] = None
    scope_note: str
    inspectability: Optional[EstimateInspectability] = None


class SolarCapacityRange(ORMModel):
    min_kw: float
    max_kw: float


class RoofGeometryReadiness(ORMModel):
    roof_data_completeness: str
    roof_measurement_confidence: str
    placement_realism_posture: str
    estimated_roof_capacity_posture: str
    measured_geometry_status: str
    usable_roof_area_status: str
    future_geometry_sources: List[str] = Field(default_factory=list)
    missing_geometry_warning: Optional[str] = None
    scope_note: Optional[str] = None


class SolarSizingEstimate(ORMModel):
    solar_production_posture: SolarSizingPosture
    low_solar_condition_posture: LowSolarAssumptionPosture
    recovery_strength: RecoveryStrengthPosture
    seasonal_conservatism: SeasonalConservatismPosture
    base_recommended_solar_capacity_range_kw: Optional[SolarCapacityRange] = None
    recommended_solar_capacity_range_kw: Optional[SolarCapacityRange] = None
    site_capacity_posture: str
    shading_obstruction_caution: str
    seasonal_production_caution: str
    install_realism_caution: str
    battery_recovery_relationship: str
    low_solar_resilience_note: str
    roof_geometry_readiness: Optional[RoofGeometryReadiness] = None
    scope_note: str
    inspectability: Optional[EstimateInspectability] = None


class RecommendationProfileCard(ORMModel):
    profile: RecommendationProfile
    label: str
    intent: str
    behavioral_assumptions: List[str] = Field(default_factory=list)
    sizing_philosophy: str
    resilience_posture: str
    future_expansion_posture: str
    battery_sizing_posture: BatterySizingPosture
    solar_sizing_posture: SolarSizingPosture
    autonomy_reserve_posture: AutonomyReservePosture
    future_growth_margin_posture: FutureGrowthMarginPosture
    low_solar_assumption_posture: LowSolarAssumptionPosture
    battery_sizing_estimate: BatterySizingEstimate
    solar_sizing_estimate: SolarSizingEstimate
    ui_description: str
    recommended: bool = False
    fit_reason: Optional[str] = None
    inspectability: Optional[EstimateInspectability] = None


class ResilienceRecommendation(ORMModel):
    design_id: str
    recommended_profile: Optional[RecommendationProfile] = None
    confidence_level: ConfidenceLevel
    backup_load_selection: Optional[BackupLoadSelectionSummary] = None
    panel_service_architecture: Optional[PanelServiceArchitectureEstimate] = None
    profiles: List[RecommendationProfileCard] = Field(default_factory=list)
    context_signals: Dict[str, object] = Field(default_factory=dict)
    scope_note: str
    basis: str
    data_origin: DataOrigin = DataOrigin.derived_estimate
    provenance_summary: Optional[Dict[str, object]] = None

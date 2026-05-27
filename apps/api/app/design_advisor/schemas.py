from typing import Dict, List, Optional

from pydantic import Field

from app.core.schemas import ORMModel
from app.core.types import (
    AutonomyReservePosture,
    AuthorityLayer,
    BatterySizingPosture,
    ConfidenceLevel,
    DataClassification,
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
    authority_layer: AuthorityLayer = AuthorityLayer.derived
    data_classification: DataClassification = DataClassification.planning_private
    derivation_type: str = "deterministic_rule"
    confidence_level: ConfidenceLevel
    trust_state: DataOrigin = DataOrigin.derived_estimate
    rule_keys: List[str] = Field(default_factory=list)
    input_signals: List[InspectabilitySignal] = Field(default_factory=list)
    estimated_inputs: List[str] = Field(default_factory=list)
    incomplete_inputs: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)
    partial_provenance_warning: Optional[str] = None


class ArchitectureConsistencyCheck(ORMModel):
    status: str
    summary: str
    reason: str
    warnings: List[str] = Field(default_factory=list)


class ProfileArchitectureFitAssessment(ORMModel):
    status: str
    equipment_mix_summary: str
    backup_path_summary: str
    summary: str
    reason: str
    tradeoffs: List[str] = Field(default_factory=list)
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


class InverterSystemArchitectureEstimate(ORMModel):
    recorded_architecture_type: str
    inverter_pathway_posture: str
    recommended_system_architecture: str
    ac_coupled_pathway_suitability: str
    hybrid_inverter_pathway_suitability: str
    battery_integration_assumption: str
    solar_integration_assumption: str
    generator_coexistence_assumption: str
    expansion_path_posture: str
    confidence_reason: str
    scope_note: str
    architecture_consistency: Optional[ArchitectureConsistencyCheck] = None
    inspectability: Optional[EstimateInspectability] = None


class HomeEnergyArchitectureComponent(ORMModel):
    component_key: str
    label: str
    state: str
    relationship: str
    note: str


class CurrentHomeEnergyArchitectureEstimate(ORMModel):
    solar_existing_state: str
    inverter_topology: str
    topology_confidence: ConfidenceLevel
    topology_confidence_reason: str
    topology_source_inputs: List[InspectabilitySignal] = Field(default_factory=list)
    current_vs_proposed_architecture: str
    outage_solar_behavior_note: str
    battery_retrofit_implication: str
    expansion_implication: str
    generator_coexistence_note: str
    architecture_components: List[HomeEnergyArchitectureComponent] = Field(default_factory=list)
    scope_note: str
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


class ReasoningGraphNode(ORMModel):
    node_id: str
    label: str
    category: str
    summary: str
    status: str
    confidence_level: ConfidenceLevel
    trust_state: DataOrigin = DataOrigin.derived_estimate
    rule_keys: List[str] = Field(default_factory=list)


class ReasoningGraphDependency(ORMModel):
    source_node_id: str
    target_node_id: str
    relationship: str
    summary: str
    confidence_level: ConfidenceLevel
    trust_state: DataOrigin = DataOrigin.derived_estimate
    rule_keys: List[str] = Field(default_factory=list)


class StructuredSystemReasoningGraph(ORMModel):
    scope_label: str
    summary: str
    nodes: List[ReasoningGraphNode] = Field(default_factory=list)
    dependencies: List[ReasoningGraphDependency] = Field(default_factory=list)
    scope_note: str
    inspectability: Optional[EstimateInspectability] = None


class PlanningStateVariant(ORMModel):
    variant_key: str
    label: str
    state_role: str
    source_type: str
    profile: Optional[RecommendationProfile] = None
    summary: str
    confidence_level: ConfidenceLevel
    trust_state: DataOrigin = DataOrigin.derived_estimate
    note: str


class PlanningStateScenarioLink(ORMModel):
    scenario_id: str
    scenario_name: str
    description: str
    linked_design_id: str
    latest_revision_id: Optional[str] = None
    latest_revision_label: Optional[str] = None
    latest_revision_number: int = 0
    data_origin: DataOrigin
    updated_at_label: str
    state_label: str
    note: str


class PlanningStateSnapshot(ORMModel):
    snapshot_id: str
    snapshot_label: str
    snapshot_kind: str
    design_id: str
    design_name: str
    design_goal: str
    design_status: str
    version_label: str
    summary: str
    scenario_count: int = 0
    variants: List[PlanningStateVariant] = Field(default_factory=list)
    linked_scenarios: List[PlanningStateScenarioLink] = Field(default_factory=list)
    scope_note: str


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
    architecture_fit: Optional[ProfileArchitectureFitAssessment] = None
    inspectability: Optional[EstimateInspectability] = None


class ResilienceRecommendation(ORMModel):
    design_id: str
    recommended_profile: Optional[RecommendationProfile] = None
    confidence_level: ConfidenceLevel
    backup_load_selection: Optional[BackupLoadSelectionSummary] = None
    current_home_energy_architecture: Optional[CurrentHomeEnergyArchitectureEstimate] = None
    panel_service_architecture: Optional[PanelServiceArchitectureEstimate] = None
    inverter_system_architecture: Optional[InverterSystemArchitectureEstimate] = None
    reasoning_graph: Optional[StructuredSystemReasoningGraph] = None
    profiles: List[RecommendationProfileCard] = Field(default_factory=list)
    context_signals: Dict[str, object] = Field(default_factory=dict)
    scope_note: str
    basis: str
    authority_layer: AuthorityLayer = AuthorityLayer.derived
    data_classification: DataClassification = DataClassification.planning_private
    advisory_boundary: str = "planning_guidance_only"
    data_origin: DataOrigin = DataOrigin.derived_estimate
    provenance_summary: Optional[Dict[str, object]] = None

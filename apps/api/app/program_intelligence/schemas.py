from enum import Enum
from typing import Dict, List

from pydantic import Field

from app.core.schemas import ORMModel
from app.core.types import AuthorityLayer, ConfidenceLevel, DataClassification


class ProgramIntelligenceStatus(str, Enum):
    awareness_available = "awareness_available"
    needs_confirmation = "needs_confirmation"
    blocked_by_missing_inputs = "blocked_by_missing_inputs"
    source_limited = "source_limited"
    unknown = "unknown"


class ProgramAwarenessCategory(str, Enum):
    utility_context = "utility_context"
    program_categories = "program_categories"
    incentive_awareness = "incentive_awareness"
    demand_response_awareness = "demand_response_awareness"
    vpp_awareness = "vpp_awareness"
    tou_awareness = "tou_awareness"
    interconnection_awareness = "interconnection_awareness"


class GridEdgeReadinessArea(str, Enum):
    battery_participation = "battery_participation"
    load_shifting = "load_shifting"
    backup_planning = "backup_planning"
    smart_panel = "smart_panel"
    ev_coordination = "ev_coordination"
    der_aggregation = "der_aggregation"


class ProgramIntelligenceScope(ORMModel):
    scope_name: str = "phase_15_program_intelligence_grid_edge_readiness"
    read_only: bool = True
    additive_only: bool = True
    request_time_only: bool = True
    home_id_anchored: bool = True
    deterministic_for_same_inputs: bool = True
    non_authoritative: bool = True
    provenance_bearing: bool = True
    homeowner_safe: bool = True
    contractor_program_review_metadata_present: bool = True
    program_awareness_present: bool = True
    grid_edge_readiness_indicators_present: bool = True
    persistence_present: bool = False
    migrations_present: bool = False
    write_endpoints_present: bool = False
    background_jobs_present: bool = False
    external_api_calls_present: bool = False
    auth_security_changes_present: bool = False
    permission_enforcement_present: bool = False
    enrollment_workflow_present: bool = False
    rebate_calculation_present: bool = False
    incentive_calculation_present: bool = False
    tariff_optimization_present: bool = False
    eligibility_determination_present: bool = False
    interconnection_approval_present: bool = False
    utility_dispatch_present: bool = False
    device_control_present: bool = False
    demand_response_execution_present: bool = False
    grid_services_execution_present: bool = False
    billing_logic_present: bool = False
    pricing_logic_present: bool = False
    proposal_generation_present: bool = False
    crm_integration_present: bool = False
    email_automation_present: bool = False
    export_present: bool = False
    push_present: bool = False
    limitations: List[str] = Field(default_factory=list)


class ProgramIntelligenceSourceBasis(ORMModel):
    source_views: List[str] = Field(default_factory=list)
    source_fields: List[str] = Field(default_factory=list)
    source_refs: List[str] = Field(default_factory=list)
    utility_refs: List[str] = Field(default_factory=list)
    equipment_refs: List[str] = Field(default_factory=list)
    program_refs: List[str] = Field(default_factory=list)
    readiness_refs: List[str] = Field(default_factory=list)
    missing_input_refs: List[str] = Field(default_factory=list)
    blocker_refs: List[str] = Field(default_factory=list)
    confirmation_gate_refs: List[str] = Field(default_factory=list)
    assumption_refs: List[str] = Field(default_factory=list)
    dependency_refs: List[str] = Field(default_factory=list)
    deferred_boundary_refs: List[str] = Field(default_factory=list)
    basis_quality: str = "request_time_derived_from_existing_twin_planning_context"
    request_time_derived: bool = True
    external_api_call_present: bool = False
    authoritative_program_claim_present: bool = False
    authoritative_eligibility_claim_present: bool = False
    enrollment_action_present: bool = False
    dispatch_or_control_action_present: bool = False
    limitations: List[str] = Field(default_factory=list)


class ProgramIntelligenceBlocker(ORMModel):
    blocker_id: str
    blocker_type: str
    severity: str
    source_refs: List[str] = Field(default_factory=list)
    missing_inputs: List[str] = Field(default_factory=list)
    homeowner_explanation: str
    contractor_program_review_prompt: str


class ProgramAwarenessItem(ORMModel):
    category: ProgramAwarenessCategory
    status: ProgramIntelligenceStatus
    confidence_level: ConfidenceLevel
    summary: str
    homeowner_summary: str
    contractor_program_review_prompt: str
    source_basis: ProgramIntelligenceSourceBasis
    missing_inputs: List[str] = Field(default_factory=list)
    blockers: List[ProgramIntelligenceBlocker] = Field(default_factory=list)
    confirmation_gates: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    do_not_assume: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class GridEdgeReadinessIndicator(ORMModel):
    readiness_area: GridEdgeReadinessArea
    status: ProgramIntelligenceStatus
    confidence_level: ConfidenceLevel
    summary: str
    indicators: List[str] = Field(default_factory=list)
    homeowner_summary: str
    contractor_program_review_prompt: str
    source_basis: ProgramIntelligenceSourceBasis
    missing_inputs: List[str] = Field(default_factory=list)
    blockers: List[ProgramIntelligenceBlocker] = Field(default_factory=list)
    confirmation_gates: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    do_not_assume: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class ProgramIntelligenceInterpretation(ORMModel):
    homeowner_safe_summary: str
    contractor_program_review_prompts: List[str] = Field(default_factory=list)
    verification_recommendations: List[str] = Field(default_factory=list)
    do_not_assume: List[str] = Field(default_factory=list)
    source_basis: ProgramIntelligenceSourceBasis
    limitations: List[str] = Field(default_factory=list)


class ProgramIntelligenceSummary(ORMModel):
    overall_status: ProgramIntelligenceStatus
    confidence_level: ConfidenceLevel
    utility_context_known: bool = False
    program_awareness_count: int = 0
    grid_edge_readiness_count: int = 0
    missing_input_count: int = 0
    blocker_count: int = 0
    confirmation_gate_count: int = 0
    eligibility_determined: bool = False
    enrollment_available: bool = False
    dispatch_or_control_available: bool = False
    pricing_or_billing_available: bool = False
    summary_boundary_note: str


class ProgramIntelligenceView(ORMModel):
    view_name: str = "program_intelligence"
    home_id: str
    anchor_type: str = "home_id"
    generated_at: str = "request_time_derived_not_persisted"
    permission_enforcement: str = "not_enforced"
    permission_scope: str = "permission_readiness_metadata_only"
    authority_layer: AuthorityLayer = AuthorityLayer.derived
    data_classification: DataClassification = DataClassification.utility_scoped
    implementation_boundary: str
    scope: ProgramIntelligenceScope
    summary: ProgramIntelligenceSummary
    program_awareness: List[ProgramAwarenessItem] = Field(default_factory=list)
    grid_edge_readiness: List[GridEdgeReadinessIndicator] = Field(default_factory=list)
    missing_inputs: List[str] = Field(default_factory=list)
    blockers: List[ProgramIntelligenceBlocker] = Field(default_factory=list)
    confirmation_gates: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    interpretation: ProgramIntelligenceInterpretation
    source_basis: ProgramIntelligenceSourceBasis
    capability_boundary_flags: Dict[str, bool] = Field(default_factory=dict)
    deferred_boundaries: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    compatibility_note: str

from enum import Enum
from typing import Dict, List

from pydantic import Field

from app.core.schemas import ORMModel
from app.core.types import AuthorityLayer, ConfidenceLevel, DataClassification


class ContractorWorkflowReadinessStatus(str, Enum):
    review_context_available = "review_context_available"
    review_limited = "review_limited"
    blocked_or_deferred = "blocked_or_deferred"
    unavailable = "unavailable"


class ContractorWorkflowLaneId(str, Enum):
    planning_review = "planning_review"
    missing_input_review = "missing_input_review"
    confirmation_gate_review = "confirmation_gate_review"
    option_candidate_review = "option_candidate_review"
    proposal_prep_blocked_deferred = "proposal_prep_blocked_deferred"


class ContractorWorkflowBlockerCategory(str, Enum):
    source_readiness_blocker = "source_readiness_blocker"
    missing_input = "missing_input"
    confirmation_gate_review = "confirmation_gate_review"
    option_candidate_review = "option_candidate_review"
    proposal_prep_deferred = "proposal_prep_deferred"
    source_unavailable = "source_unavailable"


class ContractorWorkflowScope(ORMModel):
    scope_name: str = "phase_11a_contractor_workflow_readiness"
    read_only: bool = True
    additive_only: bool = True
    request_time_only: bool = True
    home_id_anchored: bool = True
    deterministic_for_same_inputs: bool = True
    derived_from_phase_5_contractor_context: bool = True
    derived_from_phase_6_planning_exchange: bool = True
    derived_from_phase_9_estimate_readiness: bool = True
    derived_from_phase_10_proposal_option_sets: bool = True
    phase_7_8_basis_carried_from_existing_contracts_only: bool = True
    contractor_owned_state_present: bool = False
    write_endpoints_present: bool = False
    persistence_present: bool = False
    migrations_present: bool = False
    permission_enforcement_present: bool = False
    auth_security_changes_present: bool = False
    pricing_present: bool = False
    quote_generation_present: bool = False
    proposal_generation_present: bool = False
    final_estimate_present: bool = False
    final_design_present: bool = False
    approval_tracking_present: bool = False
    crm_automation_present: bool = False
    email_automation_present: bool = False
    export_present: bool = False
    contractor_accounts_present: bool = False
    assignments_present: bool = False
    accept_complete_states_present: bool = False
    source_of_truth_mutation_present: bool = False
    twin_id_present: bool = False
    graph_behavior_present: bool = False
    operational_behavior_present: bool = False
    external_services_present: bool = False
    limitations: List[str] = Field(default_factory=list)


class ContractorWorkflowSourceBasis(ORMModel):
    source_views: List[str] = Field(default_factory=list)
    source_fields: List[str] = Field(default_factory=list)
    source_refs: List[str] = Field(default_factory=list)
    contractor_context_refs: List[str] = Field(default_factory=list)
    planning_exchange_refs: List[str] = Field(default_factory=list)
    estimate_readiness_refs: List[str] = Field(default_factory=list)
    proposal_option_set_refs: List[str] = Field(default_factory=list)
    compatibility_path_refs: List[str] = Field(default_factory=list)
    takeoff_line_refs: List[str] = Field(default_factory=list)
    blocker_refs: List[str] = Field(default_factory=list)
    missing_input_refs: List[str] = Field(default_factory=list)
    confirmation_gate_refs: List[str] = Field(default_factory=list)
    option_candidate_refs: List[str] = Field(default_factory=list)
    dependency_refs: List[str] = Field(default_factory=list)
    assumption_refs: List[str] = Field(default_factory=list)
    deferred_boundary_refs: List[str] = Field(default_factory=list)
    unavailable_source_refs: List[str] = Field(default_factory=list)
    basis_quality: str = "request_time_derived_from_existing_phase_5_6_9_10_views"
    request_time_derived: bool = True
    verified_fact_claim_present: bool = False
    limitations: List[str] = Field(default_factory=list)


class ContractorWorkflowBlocker(ORMModel):
    blocker_id: str
    lane_id: ContractorWorkflowLaneId
    category: ContractorWorkflowBlockerCategory
    severity: str
    source_refs: List[str] = Field(default_factory=list)
    gate_refs: List[str] = Field(default_factory=list)
    missing_inputs: List[str] = Field(default_factory=list)
    option_candidate_refs: List[str] = Field(default_factory=list)
    dependency_refs: List[str] = Field(default_factory=list)
    homeowner_explanation: str
    contractor_readiness_prompt: str


class ContractorWorkflowReadinessLane(ORMModel):
    lane_id: ContractorWorkflowLaneId
    lane_label: str
    status: ContractorWorkflowReadinessStatus
    confidence_level: ConfidenceLevel
    reason: str
    homeowner_summary: str
    contractor_readiness_prompt: str
    source_basis: ContractorWorkflowSourceBasis
    blockers: List[ContractorWorkflowBlocker] = Field(default_factory=list)
    missing_inputs: List[str] = Field(default_factory=list)
    confirmation_gate_ids: List[str] = Field(default_factory=list)
    option_candidate_refs: List[str] = Field(default_factory=list)
    dependency_refs: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    deferred_boundaries: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class ContractorWorkflowReadinessSummary(ORMModel):
    overall_status: ContractorWorkflowReadinessStatus
    confidence_level: ConfidenceLevel
    lane_count: int = 0
    blocked_or_deferred_lane_count: int = 0
    blocker_count: int = 0
    missing_input_count: int = 0
    confirmation_gate_count: int = 0
    option_candidate_count: int = 0
    workflow_ready_for_read_only_review: bool = True
    contractor_review_required: bool = True
    summary_boundary_note: str


class ContractorWorkflowReadinessView(ORMModel):
    view_name: str = "contractor_workflow_readiness"
    home_id: str
    anchor_type: str = "home_id"
    generated_at: str = "request_time_derived_not_persisted"
    permission_enforcement: str = "not_enforced"
    permission_scope: str = "permission_readiness_metadata_only"
    authority_layer: AuthorityLayer = AuthorityLayer.derived
    data_classification: DataClassification = DataClassification.contractor_scoped
    implementation_boundary: str
    workflow_scope: ContractorWorkflowScope
    summary: ContractorWorkflowReadinessSummary
    readiness_lanes: List[ContractorWorkflowReadinessLane] = Field(default_factory=list)
    blockers: List[ContractorWorkflowBlocker] = Field(default_factory=list)
    missing_inputs: List[str] = Field(default_factory=list)
    confirmation_gate_ids: List[str] = Field(default_factory=list)
    option_candidate_refs: List[str] = Field(default_factory=list)
    dependency_refs: List[str] = Field(default_factory=list)
    homeowner_summary: str
    contractor_summary: str
    contractor_readiness_prompts: List[str] = Field(default_factory=list)
    source_basis: ContractorWorkflowSourceBasis
    blocker_category_counts: Dict[str, int] = Field(default_factory=dict)
    assumptions: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    deferred_boundaries: List[str] = Field(default_factory=list)
    compatibility_note: str

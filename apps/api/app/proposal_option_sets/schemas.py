from enum import Enum
from typing import Dict, List, Optional

from pydantic import Field

from app.core.schemas import ORMModel
from app.core.types import AuthorityLayer, ConfidenceLevel, DataClassification


class ProposalOptionSetStatus(str, Enum):
    not_ready = "not_ready"
    review_required = "review_required"
    ready_for_contractor_review_metadata = "ready_for_contractor_review_metadata"


class ProposalOptionSetBlockerCategory(str, Enum):
    estimate_readiness_blocker = "estimate_readiness_blocker"
    missing_input = "missing_input"
    confirmation_gate_open = "confirmation_gate_open"
    proposal_prerequisite_missing = "proposal_prerequisite_missing"
    pricing_deferred = "pricing_deferred"
    authority_review_deferred = "authority_review_deferred"


class ProposalOptionSetScope(ORMModel):
    scope_name: str = "phase_10_proposal_option_sets"
    read_only: bool = True
    additive_only: bool = True
    request_time_only: bool = True
    home_id_anchored: bool = True
    derived_from_existing_twin_context: bool = True
    derived_from_proposal_readiness_foundation: bool = True
    derived_from_planning_exchange: bool = True
    derived_from_shared_compatibility: bool = True
    derived_from_topology_takeoff: bool = True
    derived_from_estimate_readiness: bool = True
    deterministic_for_same_inputs: bool = True
    persistence_present: bool = False
    migrations_present: bool = False
    write_endpoints_present: bool = False
    auth_security_changes_present: bool = False
    permission_enforcement_present: bool = False
    email_automation_present: bool = False
    exports_present: bool = False
    pdf_generation_present: bool = False
    share_links_present: bool = False
    pricing_present: bool = False
    quote_generation_present: bool = False
    bid_logic_present: bool = False
    proposal_generation_present: bool = False
    final_proposal_present: bool = False
    final_estimate_present: bool = False
    final_bill_of_materials_present: bool = False
    final_design_present: bool = False
    product_recommendations_present: bool = False
    procurement_present: bool = False
    crm_workflow_present: bool = False
    ranking_present: bool = False
    best_option_selection_present: bool = False
    savings_payback_present: bool = False
    financing_incentives_present: bool = False
    contractor_approval_claim_present: bool = False
    ahj_utility_approval_claim_present: bool = False
    permit_ready_claim_present: bool = False
    field_verification_claim_present: bool = False
    final_electrical_sizing_present: bool = False
    twin_id_present: bool = False
    operational_behavior_present: bool = False
    limitations: List[str] = Field(default_factory=list)


class ProposalOptionSetBasis(ORMModel):
    source_views: List[str] = Field(default_factory=list)
    source_fields: List[str] = Field(default_factory=list)
    source_refs: List[str] = Field(default_factory=list)
    scenario_refs: List[str] = Field(default_factory=list)
    design_refs: List[str] = Field(default_factory=list)
    proposal_readiness_refs: List[str] = Field(default_factory=list)
    planning_exchange_refs: List[str] = Field(default_factory=list)
    compatibility_path_refs: List[str] = Field(default_factory=list)
    takeoff_line_refs: List[str] = Field(default_factory=list)
    estimate_gate_refs: List[str] = Field(default_factory=list)
    estimate_blocker_refs: List[str] = Field(default_factory=list)
    missing_input_refs: List[str] = Field(default_factory=list)
    dependency_refs: List[str] = Field(default_factory=list)
    assumption_refs: List[str] = Field(default_factory=list)
    deferred_boundary_refs: List[str] = Field(default_factory=list)
    basis_quality: str = "request_time_derived_from_existing_phase_3m_and_phase_6_9_views"
    request_time_derived: bool = True
    verified_fact_claim_present: bool = False
    limitations: List[str] = Field(default_factory=list)


class ProposalOptionAudienceSummary(ORMModel):
    audience: str
    summary: str
    safe_to_show: bool = True
    hidden_or_deferred_details: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class ProposalOptionSetBlocker(ORMModel):
    blocker_id: str
    category: ProposalOptionSetBlockerCategory
    severity: str
    source_refs: List[str] = Field(default_factory=list)
    gate_refs: List[str] = Field(default_factory=list)
    missing_inputs: List[str] = Field(default_factory=list)
    homeowner_explanation: str
    contractor_review_note: str


class ProposalOptionCandidate(ORMModel):
    option_candidate_id: str
    scenario_id: str
    scenario_name: str
    linked_design_id: Optional[str] = None
    linked_design_name: Optional[str] = None
    status: ProposalOptionSetStatus
    confidence_level: ConfidenceLevel
    estimate_readiness_status: str
    proposal_readiness_posture: str
    contractor_review_required: bool = True
    proposal_allowed: bool = False
    source_basis: ProposalOptionSetBasis
    blockers: List[ProposalOptionSetBlocker] = Field(default_factory=list)
    blocker_categories: List[str] = Field(default_factory=list)
    missing_inputs: List[str] = Field(default_factory=list)
    confirmation_gate_ids: List[str] = Field(default_factory=list)
    dependency_refs: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    homeowner_summary: ProposalOptionAudienceSummary
    contractor_review_notes: List[str] = Field(default_factory=list)
    deferred_boundaries: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class ProposalOptionSetsSummary(ORMModel):
    overall_status: ProposalOptionSetStatus
    confidence_level: ConfidenceLevel
    option_candidate_count: int = 0
    candidates_requiring_review_count: int = 0
    blocker_count: int = 0
    missing_input_count: int = 0
    confirmation_gate_count: int = 0
    proposal_allowed: bool = False
    contractor_review_required: bool = True
    summary_boundary_note: str


class ProposalOptionSetsView(ORMModel):
    view_name: str = "proposal_option_sets"
    home_id: str
    anchor_type: str = "home_id"
    generated_at: str = "request_time_derived_not_persisted"
    permission_enforcement: str = "not_enforced"
    permission_scope: str = "permission_readiness_metadata_only"
    authority_layer: AuthorityLayer = AuthorityLayer.derived
    data_classification: DataClassification = DataClassification.contractor_scoped
    implementation_boundary: str
    option_set_scope: ProposalOptionSetScope
    summary: ProposalOptionSetsSummary
    option_candidates: List[ProposalOptionCandidate] = Field(default_factory=list)
    blockers: List[ProposalOptionSetBlocker] = Field(default_factory=list)
    missing_inputs: List[str] = Field(default_factory=list)
    confirmation_gate_ids: List[str] = Field(default_factory=list)
    dependency_refs: List[str] = Field(default_factory=list)
    homeowner_summary: str
    contractor_summary: str
    source_basis: ProposalOptionSetBasis
    blocker_category_counts: Dict[str, int] = Field(default_factory=dict)
    assumptions: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    deferred_boundaries: List[str] = Field(default_factory=list)
    compatibility_note: str

from enum import Enum
from typing import Dict, List

from pydantic import Field

from app.core.schemas import ORMModel
from app.core.types import AuthorityLayer, ConfidenceLevel, DataClassification


class PostInstallStatus(str, Enum):
    retention_review_available = "retention_review_available"
    review_required = "review_required"
    blocked_by_missing_inputs = "blocked_by_missing_inputs"
    source_limited = "source_limited"
    unavailable = "unavailable"


class RetentionOpportunityType(str, Enum):
    contractor_review_followup = "contractor_review_followup"
    documentation_completion = "documentation_completion"
    estimate_readiness_followup = "estimate_readiness_followup"
    homeowner_context_followup = "homeowner_context_followup"
    product_spec_followup = "product_spec_followup"
    proposal_context_followup = "proposal_context_followup"


class LifecycleEventType(str, Enum):
    confirmation_gate_open = "confirmation_gate_open"
    contractor_review_required = "contractor_review_required"
    missing_input_detected = "missing_input_detected"
    post_install_context_assembled = "post_install_context_assembled"
    product_review_needed = "product_review_needed"
    proposal_prep_deferred = "proposal_prep_deferred"


class PostInstallBlockerCategory(str, Enum):
    confirmation_gate_open = "confirmation_gate_open"
    missing_input = "missing_input"
    source_unavailable = "source_unavailable"
    deferred_boundary = "deferred_boundary"
    review_required = "review_required"


class PostInstallScope(ORMModel):
    scope_name: str = "phase_13_post_install_retention_crm_handoff"
    read_only: bool = True
    backend_api_only: bool = True
    additive_only: bool = True
    request_time_only: bool = True
    home_id_anchored: bool = True
    deterministic_for_same_inputs: bool = True
    provenance_bearing: bool = True
    post_install_state_view_present: bool = True
    retention_opportunity_identification_present: bool = True
    lifecycle_event_detection_present: bool = True
    follow_up_readiness_present: bool = True
    persistence_present: bool = False
    migrations_present: bool = False
    write_endpoints_present: bool = False
    auth_security_changes_present: bool = False
    permission_enforcement_present: bool = False
    frontend_present: bool = False
    external_crm_integration_present: bool = False
    crm_writes_present: bool = False
    email_drip_campaign_behavior_present: bool = False
    task_creation_present: bool = False
    sales_scoring_present: bool = False
    lead_scoring_present: bool = False
    ranking_present: bool = False
    best_upsell_logic_present: bool = False
    push_behavior_present: bool = False
    pricing_present: bool = False
    proposal_generation_present: bool = False
    source_of_truth_mutation_present: bool = False
    twin_id_present: bool = False
    graph_behavior_present: bool = False
    operational_behavior_present: bool = False
    limitations: List[str] = Field(default_factory=list)


class PostInstallSourceBasis(ORMModel):
    source_views: List[str] = Field(default_factory=list)
    source_fields: List[str] = Field(default_factory=list)
    source_refs: List[str] = Field(default_factory=list)
    contractor_workflow_refs: List[str] = Field(default_factory=list)
    product_preference_refs: List[str] = Field(default_factory=list)
    proposal_option_refs: List[str] = Field(default_factory=list)
    estimate_gate_refs: List[str] = Field(default_factory=list)
    missing_input_refs: List[str] = Field(default_factory=list)
    blocker_refs: List[str] = Field(default_factory=list)
    lifecycle_event_refs: List[str] = Field(default_factory=list)
    retention_opportunity_refs: List[str] = Field(default_factory=list)
    deferred_boundary_refs: List[str] = Field(default_factory=list)
    unavailable_source_refs: List[str] = Field(default_factory=list)
    basis_quality: str = "request_time_derived_from_existing_phase_9_12_views"
    request_time_derived: bool = True
    verified_fact_claim_present: bool = False
    limitations: List[str] = Field(default_factory=list)


class PostInstallBlocker(ORMModel):
    blocker_id: str
    category: PostInstallBlockerCategory
    severity: str
    source_refs: List[str] = Field(default_factory=list)
    missing_inputs: List[str] = Field(default_factory=list)
    confirmation_gate_ids: List[str] = Field(default_factory=list)
    homeowner_explanation: str
    contractor_review_note: str


class RetentionOpportunity(ORMModel):
    opportunity_id: str
    opportunity_type: RetentionOpportunityType
    status: PostInstallStatus
    confidence_level: ConfidenceLevel
    title: str
    homeowner_summary: str
    contractor_review_note: str
    follow_up_readiness: str
    source_basis: PostInstallSourceBasis
    missing_inputs: List[str] = Field(default_factory=list)
    blockers: List[PostInstallBlocker] = Field(default_factory=list)
    confirmation_gate_ids: List[str] = Field(default_factory=list)
    lifecycle_event_refs: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class LifecycleEvent(ORMModel):
    event_id: str
    event_type: LifecycleEventType
    detected: bool
    event_label: str
    source_refs: List[str] = Field(default_factory=list)
    missing_inputs: List[str] = Field(default_factory=list)
    confirmation_gate_ids: List[str] = Field(default_factory=list)
    explanation: str
    confidence_level: ConfidenceLevel


class PostInstallSummary(ORMModel):
    overall_status: PostInstallStatus
    confidence_level: ConfidenceLevel
    opportunity_count: int = 0
    lifecycle_event_count: int = 0
    blocker_count: int = 0
    missing_input_count: int = 0
    confirmation_gate_count: int = 0
    manual_follow_up_ready: bool = True
    crm_handoff_object_available: bool = True
    crm_write_allowed: bool = False
    email_campaign_allowed: bool = False
    task_creation_allowed: bool = False
    scoring_allowed: bool = False
    ranking_allowed: bool = False
    push_allowed: bool = False
    summary_boundary_note: str


class PostInstallView(ORMModel):
    view_name: str = "post_install_retention"
    home_id: str
    anchor_type: str = "home_id"
    generated_at: str = "request_time_derived_not_persisted"
    permission_enforcement: str = "not_enforced"
    permission_scope: str = "permission_readiness_metadata_only"
    authority_layer: AuthorityLayer = AuthorityLayer.derived
    data_classification: DataClassification = DataClassification.contractor_scoped
    implementation_boundary: str
    post_install_scope: PostInstallScope
    summary: PostInstallSummary
    opportunities: List[RetentionOpportunity] = Field(default_factory=list)
    lifecycle_events: List[LifecycleEvent] = Field(default_factory=list)
    blockers: List[PostInstallBlocker] = Field(default_factory=list)
    missing_inputs: List[str] = Field(default_factory=list)
    confirmation_gate_ids: List[str] = Field(default_factory=list)
    homeowner_summary: str
    contractor_summary: str
    follow_up_readiness_notes: List[str] = Field(default_factory=list)
    source_basis: PostInstallSourceBasis
    blocker_category_counts: Dict[str, int] = Field(default_factory=dict)
    assumptions: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    deferred_boundaries: List[str] = Field(default_factory=list)
    compatibility_note: str

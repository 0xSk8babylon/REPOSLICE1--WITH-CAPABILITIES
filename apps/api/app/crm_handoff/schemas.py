from enum import Enum
from typing import Dict, List

from pydantic import Field

from app.core.schemas import ORMModel
from app.core.types import AuthorityLayer, ConfidenceLevel, DataClassification


class CRMHandoffStatus(str, Enum):
    manual_handoff_object_ready = "manual_handoff_object_ready"
    review_required = "review_required"
    blocked_by_missing_inputs = "blocked_by_missing_inputs"
    source_limited = "source_limited"
    unavailable = "unavailable"


class CRMHandoffFieldCategory(str, Enum):
    boundary = "boundary"
    follow_up_readiness = "follow_up_readiness"
    home_anchor = "home_anchor"
    lifecycle_context = "lifecycle_context"
    missing_input_context = "missing_input_context"
    retention_context = "retention_context"
    review_context = "review_context"
    source_basis = "source_basis"


class CRMHandoffScope(ORMModel):
    scope_name: str = "phase_13_crm_handoff_object"
    read_only: bool = True
    backend_api_only: bool = True
    additive_only: bool = True
    request_time_only: bool = True
    home_id_anchored: bool = True
    deterministic_for_same_inputs: bool = True
    provenance_bearing: bool = True
    handoff_object_present: bool = True
    external_crm_integration_present: bool = False
    crm_write_present: bool = False
    crm_record_creation_present: bool = False
    email_drip_campaign_behavior_present: bool = False
    task_creation_present: bool = False
    sales_scoring_present: bool = False
    lead_scoring_present: bool = False
    ranking_present: bool = False
    best_upsell_logic_present: bool = False
    push_behavior_present: bool = False
    persistence_present: bool = False
    migrations_present: bool = False
    write_endpoints_present: bool = False
    auth_security_changes_present: bool = False
    permission_enforcement_present: bool = False
    frontend_present: bool = False
    external_services_present: bool = False
    secrets_present: bool = False
    source_of_truth_mutation_present: bool = False
    twin_id_present: bool = False
    graph_behavior_present: bool = False
    operational_behavior_present: bool = False
    limitations: List[str] = Field(default_factory=list)


class CRMHandoffSourceBasis(ORMModel):
    source_views: List[str] = Field(default_factory=list)
    source_fields: List[str] = Field(default_factory=list)
    source_refs: List[str] = Field(default_factory=list)
    post_install_refs: List[str] = Field(default_factory=list)
    lifecycle_event_refs: List[str] = Field(default_factory=list)
    retention_opportunity_refs: List[str] = Field(default_factory=list)
    missing_input_refs: List[str] = Field(default_factory=list)
    blocker_refs: List[str] = Field(default_factory=list)
    confirmation_gate_refs: List[str] = Field(default_factory=list)
    handoff_field_refs: List[str] = Field(default_factory=list)
    deferred_boundary_refs: List[str] = Field(default_factory=list)
    unavailable_source_refs: List[str] = Field(default_factory=list)
    basis_quality: str = "request_time_derived_from_phase_13_post_install_view"
    request_time_derived: bool = True
    verified_fact_claim_present: bool = False
    limitations: List[str] = Field(default_factory=list)


class CRMHandoffField(ORMModel):
    field_id: str
    field_key: str
    category: CRMHandoffFieldCategory
    label: str
    value: str
    source_refs: List[str] = Field(default_factory=list)
    missing_inputs: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class CRMHandoffSummary(ORMModel):
    overall_status: CRMHandoffStatus
    confidence_level: ConfidenceLevel
    handoff_field_count: int = 0
    retention_opportunity_count: int = 0
    lifecycle_event_count: int = 0
    blocker_count: int = 0
    missing_input_count: int = 0
    confirmation_gate_count: int = 0
    manual_crm_review_ready: bool = True
    crm_write_allowed: bool = False
    external_crm_sync_allowed: bool = False
    email_campaign_allowed: bool = False
    task_creation_allowed: bool = False
    scoring_allowed: bool = False
    ranking_allowed: bool = False
    push_allowed: bool = False
    summary_boundary_note: str


class CRMHandoffView(ORMModel):
    view_name: str = "crm_handoff_object"
    home_id: str
    anchor_type: str = "home_id"
    generated_at: str = "request_time_derived_not_persisted"
    permission_enforcement: str = "not_enforced"
    permission_scope: str = "permission_readiness_metadata_only"
    authority_layer: AuthorityLayer = AuthorityLayer.derived
    data_classification: DataClassification = DataClassification.contractor_scoped
    implementation_boundary: str
    handoff_object_id: str
    handoff_scope: CRMHandoffScope
    summary: CRMHandoffSummary
    handoff_fields: List[CRMHandoffField] = Field(default_factory=list)
    lifecycle_event_refs: List[str] = Field(default_factory=list)
    retention_opportunity_refs: List[str] = Field(default_factory=list)
    missing_inputs: List[str] = Field(default_factory=list)
    blockers: List[str] = Field(default_factory=list)
    confirmation_gate_ids: List[str] = Field(default_factory=list)
    manual_review_summary: str
    homeowner_safe_summary: str
    contractor_review_summary: str
    source_basis: CRMHandoffSourceBasis
    field_category_counts: Dict[str, int] = Field(default_factory=dict)
    assumptions: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    deferred_boundaries: List[str] = Field(default_factory=list)
    compatibility_note: str

from enum import Enum
from typing import Dict, List, Optional

from pydantic import Field

from app.core.schemas import ORMModel
from app.core.types import AuthorityLayer, ConfidenceLevel, DataClassification


class EstimateReadinessStatus(str, Enum):
    not_ready = "not_ready"
    partially_ready = "partially_ready"
    ready_for_contractor_review = "ready_for_contractor_review"
    ready_for_estimate = "ready_for_estimate"


class EstimateConfirmationGateStatus(str, Enum):
    pending_confirmation = "pending_confirmation"
    contractor_review_required = "contractor_review_required"
    authority_review_required = "authority_review_required"
    contractor_only_final_review_required = "contractor_only_final_review_required"
    confirmed = "confirmed"


class EstimateBlockerCategory(str, Enum):
    missing_measurement = "missing_measurement"
    missing_product_spec = "missing_product_spec"
    missing_nameplate = "missing_nameplate"
    unsafe_assumption = "unsafe_assumption"
    code_review_required = "code_review_required"
    utility_review_required = "utility_review_required"
    ahj_review_required = "ahj_review_required"
    contractor_field_verification_required = "contractor_field_verification_required"
    pricing_input_missing = "pricing_input_missing"
    material_scope_incomplete = "material_scope_incomplete"


class EstimateReadinessScope(ORMModel):
    scope_name: str = "phase_9_estimate_readiness_confirmation_gates"
    read_only: bool = True
    request_time_only: bool = True
    home_id_anchored: bool = True
    scenario_specific_runtime_engine_present: bool = False
    derived_from_existing_twin_context: bool = True
    derived_from_topology_takeoff: bool = True
    derived_from_confirmation_gate_projection: bool = True
    derived_from_shared_compatibility: bool = True
    deterministic_for_same_inputs: bool = True
    persistence_present: bool = False
    migrations_present: bool = False
    write_endpoints_present: bool = False
    auth_security_changes_present: bool = False
    permission_enforcement_present: bool = False
    pricing_present: bool = False
    proposal_generation_present: bool = False
    final_estimate_present: bool = False
    final_design_present: bool = False
    permit_ready_claim_present: bool = False
    contractor_approval_claim_present: bool = False
    ahj_utility_approval_claim_present: bool = False
    twin_id_present: bool = False
    operational_behavior_present: bool = False
    limitations: List[str] = Field(default_factory=list)


class EstimateReadinessBasis(ORMModel):
    source_views: List[str] = Field(default_factory=list)
    source_fields: List[str] = Field(default_factory=list)
    source_refs: List[str] = Field(default_factory=list)
    gate_refs: List[str] = Field(default_factory=list)
    takeoff_line_refs: List[str] = Field(default_factory=list)
    compatibility_path_refs: List[str] = Field(default_factory=list)
    scenario_refs: List[str] = Field(default_factory=list)
    missing_input_refs: List[str] = Field(default_factory=list)
    basis_quality: str = "request_time_derived_from_existing_phase_5_7_8_views"
    request_time_derived: bool = True
    verified_fact_claim_present: bool = False
    basis_notes: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class EstimateConfirmationGate(ORMModel):
    gate_id: str
    gate_name: str
    gate_version: str
    category: str
    required_for_estimate: bool
    visible_to_homeowner: bool
    contractor_only_notes: List[str] = Field(default_factory=list)
    status: EstimateConfirmationGateStatus
    basis: EstimateReadinessBasis
    missing_inputs: List[str] = Field(default_factory=list)
    blocker_categories: List[EstimateBlockerCategory] = Field(default_factory=list)
    source_gate_status: str
    source_blocker_level: str
    homeowner_explanation: str
    contractor_notes: str


class EstimateReadinessBlocker(ORMModel):
    blocker_id: str
    category: EstimateBlockerCategory
    severity: str
    gate_refs: List[str] = Field(default_factory=list)
    source_refs: List[str] = Field(default_factory=list)
    missing_inputs: List[str] = Field(default_factory=list)
    homeowner_explanation: str
    contractor_notes: str
    estimate_allowed_impact: bool = True


class ScenarioEstimateReadinessStatus(ORMModel):
    scenario_id: str
    scenario_name: str
    linked_design_id: Optional[str] = None
    status: EstimateReadinessStatus
    confidence_level: ConfidenceLevel
    estimate_allowed: bool = False
    contractor_review_required: bool = True
    complexity_flags: List[str] = Field(default_factory=list)
    required_gate_ids: List[str] = Field(default_factory=list)
    blocker_categories: List[EstimateBlockerCategory] = Field(default_factory=list)
    missing_inputs: List[str] = Field(default_factory=list)
    homeowner_explanation: str
    contractor_notes: str
    basis: EstimateReadinessBasis


class EstimateReadinessSummary(ORMModel):
    overall_status: EstimateReadinessStatus
    confidence_level: ConfidenceLevel
    estimate_allowed: bool = False
    contractor_review_required: bool = True
    required_gate_count: int = 0
    pending_gate_count: int = 0
    blocker_count: int = 0
    missing_input_count: int = 0
    scenario_count: int = 0
    summary_boundary_note: str


class EstimateReadinessView(ORMModel):
    view_name: str = "estimate_readiness"
    home_id: str
    anchor_type: str = "home_id"
    generated_at: str = "request_time_derived_not_persisted"
    permission_enforcement: str = "not_enforced"
    permission_scope: str = "permission_readiness_metadata_only"
    authority_layer: AuthorityLayer = AuthorityLayer.derived
    data_classification: DataClassification = DataClassification.contractor_scoped
    implementation_boundary: str
    readiness_scope: EstimateReadinessScope
    readiness_summary: EstimateReadinessSummary
    overall_status: EstimateReadinessStatus
    scenario_statuses: List[ScenarioEstimateReadinessStatus] = Field(default_factory=list)
    confirmation_gates: List[EstimateConfirmationGate] = Field(default_factory=list)
    blockers: List[EstimateReadinessBlocker] = Field(default_factory=list)
    missing_inputs: List[str] = Field(default_factory=list)
    homeowner_summary: str
    contractor_summary: str
    estimate_allowed: bool = False
    contractor_review_required: bool = True
    confidence_level: ConfidenceLevel
    source_basis: EstimateReadinessBasis
    blocker_category_counts: Dict[str, int] = Field(default_factory=dict)
    assumptions: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    deferred_boundaries: List[str] = Field(default_factory=list)
    compatibility_note: str

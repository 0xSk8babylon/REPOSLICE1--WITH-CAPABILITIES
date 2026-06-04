from typing import List

from pydantic import Field

from app.core.schemas import ORMModel
from app.core.types import AuthorityLayer, DataClassification


class ContractorContextScope(ORMModel):
    scope_name: str = "phase_5b_contractor_scoped_planning_visibility"
    read_only: bool = True
    request_time_only: bool = True
    home_id_anchored: bool = True
    derived_from_existing_twin_context: bool = True
    deterministic_for_same_inputs: bool = True
    permission_enforcement: str = "not_enforced"
    contractor_accounts_present: bool = False
    write_endpoints_present: bool = False
    persistence_present: bool = False
    migrations_present: bool = False
    auth_security_changes_present: bool = False
    exports_present: bool = False
    twin_id_present: bool = False
    final_electrical_design_claims_present: bool = False
    limitations: List[str] = Field(default_factory=list)


class ContractorContextProvenance(ORMModel):
    source_views: List[str] = Field(default_factory=list)
    source_fields: List[str] = Field(default_factory=list)
    source_refs: List[str] = Field(default_factory=list)
    derived_from: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class ContractorContextItem(ORMModel):
    item_id: str
    category: str
    statement: str
    source_or_basis: str
    provenance: ContractorContextProvenance
    missing_inputs: List[str] = Field(default_factory=list)
    required_verifiers: List[str] = Field(default_factory=list)
    next_actions: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class ContractorPlanningContextView(ORMModel):
    view_name: str = "contractor_scoped_planning_context"
    home_id: str
    anchor_type: str = "home_id"
    permission_enforcement: str = "not_enforced"
    authority_layer: AuthorityLayer = AuthorityLayer.derived
    data_classification: DataClassification = DataClassification.contractor_scoped
    implementation_boundary: str
    contractor_scope: ContractorContextScope
    source_basis: ContractorContextProvenance
    homeowner_goals: List[ContractorContextItem] = Field(default_factory=list)
    home_site_planning_summary: List[ContractorContextItem] = Field(default_factory=list)
    known_electrical_equipment_summary: List[ContractorContextItem] = Field(default_factory=list)
    proposed_system_context: List[ContractorContextItem] = Field(default_factory=list)
    missing_information: List[ContractorContextItem] = Field(default_factory=list)
    contractor_verification_needs: List[ContractorContextItem] = Field(default_factory=list)
    provenance_trust_notes: List[ContractorContextItem] = Field(default_factory=list)
    permission_readiness_notes: List[ContractorContextItem] = Field(default_factory=list)
    next_safe_contractor_review_prompts: List[ContractorContextItem] = Field(default_factory=list)
    deferred_boundaries: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    compatibility_note: str


class ContractorConfirmationGate(ORMModel):
    gate_id: str
    title: str
    category: str
    status: str
    required_verifier: str
    source_or_basis: str
    blocker_level: str
    reason: str
    next_action: str
    provenance: ContractorContextProvenance
    limitations: List[str] = Field(default_factory=list)


class ContractorConfirmationGateProjectionView(ORMModel):
    view_name: str = "contractor_confirmation_gate_projection"
    home_id: str
    anchor_type: str = "home_id"
    permission_enforcement: str = "not_enforced"
    authority_layer: AuthorityLayer = AuthorityLayer.derived
    data_classification: DataClassification = DataClassification.contractor_scoped
    implementation_boundary: str
    gate_titles_are_review_topics_only: bool = True
    gate_state_persisted: bool = False
    read_only: bool = True
    request_time_only: bool = True
    deterministic_for_same_inputs: bool = True
    gates: List[ContractorConfirmationGate] = Field(default_factory=list)
    source_basis: ContractorContextProvenance
    deferred_boundaries: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    compatibility_note: str


class ContractorInstallComplexitySignal(ORMModel):
    signal_id: str
    category: str
    severity: str
    reason: str
    missing_inputs: List[str] = Field(default_factory=list)
    required_verifier: str
    next_action: str
    source_or_basis: str
    provenance: ContractorContextProvenance
    limitations: List[str] = Field(default_factory=list)


class ContractorInstallComplexityView(ORMModel):
    view_name: str = "contractor_install_complexity"
    home_id: str
    anchor_type: str = "home_id"
    permission_enforcement: str = "not_enforced"
    authority_layer: AuthorityLayer = AuthorityLayer.derived
    data_classification: DataClassification = DataClassification.contractor_scoped
    implementation_boundary: str
    read_only: bool = True
    request_time_only: bool = True
    deterministic_for_same_inputs: bool = True
    final_electrical_design_claims_present: bool = False
    wire_sizing_present: bool = False
    conduit_sizing_present: bool = False
    breaker_sizing_present: bool = False
    disconnect_requirement_sizing_present: bool = False
    nec_code_compliant_design_present: bool = False
    signals: List[ContractorInstallComplexitySignal] = Field(default_factory=list)
    source_basis: ContractorContextProvenance
    deferred_boundaries: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    compatibility_note: str

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field

from app.contractor_context.schemas import (
    ContractorConfirmationGate,
    ContractorContextItem,
    ContractorInstallComplexitySignal,
)
from app.core.schemas import ORMModel
from app.core.types import AuthorityLayer, DataClassification


class PlanningExchangeTrustCategory(str, Enum):
    homeowner_provided = "homeowner_provided"
    app_derived = "app_derived"
    contractor_safe_projection = "contractor_safe_projection"
    manufacturer_required_future = "manufacturer_required_future"
    ahj_utility_dependent_future = "ahj_utility_dependent_future"
    missing_unknown = "missing_unknown"


class PlanningExchangeReadinessPosture(str, Enum):
    ready_for_planning_review = "ready_for_planning_review"
    review_limited_by_missing_information = "review_limited_by_missing_information"
    contractor_review_required = "contractor_review_required"
    not_ready_for_estimate_input = "not_ready_for_estimate_input"
    not_ready_for_proposal_option_input = "not_ready_for_proposal_option_input"


class PlanningExchangeScope(ORMModel):
    scope_name: str = "phase_6_planning_exchange_object"
    read_only: bool = True
    request_time_only: bool = True
    home_id_anchored: bool = True
    derived_package_not_source_of_truth: bool = True
    deterministic_for_same_inputs: bool = True
    additive_only: bool = True
    permission_enforcement: str = "not_enforced"
    twin_id_present: bool = False
    persistence_present: bool = False
    migrations_present: bool = False
    write_endpoints_present: bool = False
    exports_present: bool = False
    pdf_generation_present: bool = False
    share_links_present: bool = False
    auth_security_changes_present: bool = False
    contractor_accounts_present: bool = False
    source_of_truth_mutation_present: bool = False
    frontend_present: bool = False
    pricing_or_proposal_present: bool = False
    marketplace_or_bidding_present: bool = False
    final_electrical_design_claims_present: bool = False
    limitations: List[str] = Field(default_factory=list)


class PlanningExchangeSourceBasis(ORMModel):
    source_views: List[str] = Field(default_factory=list)
    source_fields: List[str] = Field(default_factory=list)
    source_refs: List[str] = Field(default_factory=list)
    derived_from: List[str] = Field(default_factory=list)
    trust_categories: List[PlanningExchangeTrustCategory] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class PlanningExchangeSectionMapping(ORMModel):
    section_key: str
    label: str
    trust_category: PlanningExchangeTrustCategory
    source_view: str
    source_fields: List[str] = Field(default_factory=list)
    source_refs: List[str] = Field(default_factory=list)
    authority_layer: AuthorityLayer = AuthorityLayer.derived
    data_classification: DataClassification = DataClassification.contractor_scoped
    source_or_basis: str
    missing_inputs: List[str] = Field(default_factory=list)
    required_verifiers: List[str] = Field(default_factory=list)
    review_prompts: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class PlanningExchangeReviewPrompt(ORMModel):
    prompt_id: str
    category: str
    prompt: str
    required_verifier: str
    source_or_basis: str
    source_mapping_refs: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class PlanningExchangeReadinessItem(ORMModel):
    readiness_area: str
    posture: PlanningExchangeReadinessPosture
    reason: str
    source_or_basis: str
    blockers: List[str] = Field(default_factory=list)
    required_verifiers: List[str] = Field(default_factory=list)
    next_review_prompts: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class PlanningExchangeReadinessSummary(ORMModel):
    participant_review: PlanningExchangeReadinessItem
    contractor_review: PlanningExchangeReadinessItem
    estimate_readiness: PlanningExchangeReadinessItem
    proposal_option_readiness: PlanningExchangeReadinessItem
    overall_posture: PlanningExchangeReadinessPosture
    non_authoritative_note: str
    limitations: List[str] = Field(default_factory=list)


class PlanningExchangeObjectView(ORMModel):
    view_name: str = "planning_exchange_object"
    home_id: str
    anchor_type: str = "home_id"
    permission_enforcement: str = "not_enforced"
    authority_layer: AuthorityLayer = AuthorityLayer.derived
    data_classification: DataClassification = DataClassification.contractor_scoped
    implementation_boundary: str
    exchange_scope: PlanningExchangeScope
    source_basis: PlanningExchangeSourceBasis
    homeowner_intent_goals: List[ContractorContextItem] = Field(default_factory=list)
    home_site_planning_context: List[ContractorContextItem] = Field(default_factory=list)
    known_electrical_equipment_summary: List[ContractorContextItem] = Field(default_factory=list)
    proposed_system_context: List[ContractorContextItem] = Field(default_factory=list)
    contractor_safe_planning_context: List[ContractorContextItem] = Field(default_factory=list)
    confirmation_gates: List[ContractorConfirmationGate] = Field(default_factory=list)
    install_complexity_uncertainty_signals: List[ContractorInstallComplexitySignal] = Field(default_factory=list)
    provenance_trust_basis: List[ContractorContextItem] = Field(default_factory=list)
    missing_information: List[ContractorContextItem] = Field(default_factory=list)
    required_verifiers: List[str] = Field(default_factory=list)
    review_prompts: List[PlanningExchangeReviewPrompt] = Field(default_factory=list)
    section_mappings: List[PlanningExchangeSectionMapping] = Field(default_factory=list)
    readiness_summary: Optional[PlanningExchangeReadinessSummary] = None
    limitations: List[str] = Field(default_factory=list)
    deferred_boundaries: List[str] = Field(default_factory=list)
    compatibility_note: str
    raw_source_payloads_embedded: bool = False
    source_payload_refs: Dict[str, Any] = Field(default_factory=dict)

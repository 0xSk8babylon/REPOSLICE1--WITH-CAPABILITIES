from enum import Enum
from typing import Dict, List, Optional

from pydantic import Field

from app.core.schemas import ORMModel
from app.core.types import AuthorityLayer, ConfidenceLevel, DataClassification


class EnergyPassportStatus(str, Enum):
    known = "known"
    planned = "planned"
    candidate = "candidate"
    needs_confirmation = "needs_confirmation"
    not_available = "not_available"
    unknown = "unknown"


class EnergyPassportSystemType(str, Enum):
    solar_pv = "solar_pv"
    battery_storage = "battery_storage"
    backup_generator = "backup_generator"
    panel_load_management = "panel_load_management"
    ev_readiness = "ev_readiness"
    utility_program_context = "utility_program_context"


class EnergyPassportFinancingStructure(str, Enum):
    cash_purchase = "cash_purchase"
    solar_loan = "solar_loan"
    home_improvement_loan = "home_improvement_loan"
    personal_loan = "personal_loan"
    secured_loan = "secured_loan"
    unsecured_loan = "unsecured_loan"
    heloc = "heloc"
    lease = "lease"
    power_purchase_agreement = "power_purchase_agreement"
    pace_assessment = "pace_assessment"
    utility_program = "utility_program"
    contractor_originated_financing = "contractor_originated_financing"
    manufacturer_financing = "manufacturer_financing"
    subscription_service = "subscription_service"
    third_party_owned = "third_party_owned"
    unknown = "unknown"
    needs_confirmation = "needs_confirmation"


class EnergyPassportTransferRelevanceFlag(str, Enum):
    no_known_transfer_issue = "no_known_transfer_issue"
    payoff_may_be_required = "payoff_may_be_required"
    contract_assignment_may_be_required = "contract_assignment_may_be_required"
    buyer_qualification_may_be_required = "buyer_qualification_may_be_required"
    tied_to_property_tax_assessment = "tied_to_property_tax_assessment"
    tied_to_property_or_title_review = "tied_to_property_or_title_review"
    tied_to_owner_credit = "tied_to_owner_credit"
    tied_to_utility_account = "tied_to_utility_account"
    tied_to_cloud_or_monitoring_account = "tied_to_cloud_or_monitoring_account"
    document_review_required = "document_review_required"
    unknown = "unknown"


class EnergyPassportTransferReadinessLevel(str, Enum):
    ready_for_manual_review = "ready_for_manual_review"
    needs_confirmation = "needs_confirmation"
    blocked_by_missing_inputs = "blocked_by_missing_inputs"
    source_limited = "source_limited"
    unknown = "unknown"


class EnergyPassportScope(ORMModel):
    scope_name: str = "phase_14_energy_passport"
    read_only: bool = True
    additive_only: bool = True
    request_time_only: bool = True
    home_id_anchored: bool = True
    deterministic_for_same_inputs: bool = True
    non_authoritative: bool = True
    homeowner_safe: bool = True
    contractor_safe_summary_present: bool = True
    provenance_bearing: bool = True
    title_claim_present: bool = False
    escrow_claim_present: bool = False
    deed_claim_present: bool = False
    lease_assignment_present: bool = False
    payoff_calculation_present: bool = False
    lien_ucc_title_search_present: bool = False
    warranty_validation_present: bool = False
    permit_validation_present: bool = False
    appraisal_present: bool = False
    underwriting_present: bool = False
    tax_advice_present: bool = False
    financial_conclusion_present: bool = False
    crm_write_present: bool = False
    persistence_present: bool = False
    migrations_present: bool = False
    auth_security_changes_present: bool = False
    permission_enforcement_present: bool = False
    deploy_present: bool = False
    push_present: bool = False
    write_endpoints_present: bool = False
    contract_validation_present: bool = False
    legal_advice_present: bool = False
    limitations: List[str] = Field(default_factory=list)


class EnergyPassportSourceBasis(ORMModel):
    source_views: List[str] = Field(default_factory=list)
    source_fields: List[str] = Field(default_factory=list)
    source_refs: List[str] = Field(default_factory=list)
    system_refs: List[str] = Field(default_factory=list)
    obligation_refs: List[str] = Field(default_factory=list)
    transfer_refs: List[str] = Field(default_factory=list)
    planning_history_refs: List[str] = Field(default_factory=list)
    post_install_refs: List[str] = Field(default_factory=list)
    future_upgrade_refs: List[str] = Field(default_factory=list)
    missing_input_refs: List[str] = Field(default_factory=list)
    blocker_refs: List[str] = Field(default_factory=list)
    assumption_refs: List[str] = Field(default_factory=list)
    deferred_boundary_refs: List[str] = Field(default_factory=list)
    unavailable_source_refs: List[str] = Field(default_factory=list)
    basis_quality: str = "request_time_derived_from_existing_phase_6_13_views"
    request_time_derived: bool = True
    verified_fact_claim_present: bool = False
    authoritative_validation_present: bool = False
    limitations: List[str] = Field(default_factory=list)


class EnergyPassportSystemSummary(ORMModel):
    system_type: EnergyPassportSystemType
    status: EnergyPassportStatus
    confidence_level: ConfidenceLevel
    summary: str
    source_basis: EnergyPassportSourceBasis
    missing_inputs: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class EnergyPassportSystemFinancialObligation(ORMModel):
    system_type: EnergyPassportSystemType
    ownership_status: EnergyPassportStatus = EnergyPassportStatus.needs_confirmation
    financing_structure: EnergyPassportFinancingStructure = EnergyPassportFinancingStructure.needs_confirmation
    transfer_relevance_flags: List[EnergyPassportTransferRelevanceFlag] = Field(default_factory=list)
    documents_needed: List[str] = Field(default_factory=list)
    non_authoritative: bool = True
    needs_confirmation: bool = True
    source_basis: EnergyPassportSourceBasis
    assumptions: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class EnergyPassportTransferReadiness(ORMModel):
    readiness_level: EnergyPassportTransferReadinessLevel
    transfer_ready: bool = False
    missing_transfer_inputs: List[str] = Field(default_factory=list)
    confirmation_needed: List[str] = Field(default_factory=list)
    buyer_disclosure_recommended: bool = True
    contractor_review_recommended: bool = True
    buyer_safe_summary: str
    contractor_safe_summary: str
    source_basis: EnergyPassportSourceBasis
    assumptions: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class EnergyPassportContextSection(ORMModel):
    section_name: str
    status: EnergyPassportStatus
    summary: str
    source_basis: EnergyPassportSourceBasis
    assumptions: List[str] = Field(default_factory=list)
    blockers: List[str] = Field(default_factory=list)
    deferred_boundaries: List[str] = Field(default_factory=list)
    missing_inputs: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class EnergyPassportSummary(ORMModel):
    overall_status: EnergyPassportStatus
    confidence_level: ConfidenceLevel
    system_count: int = 0
    relevant_obligation_count: int = 0
    unknown_obligation_count: int = 0
    missing_transfer_input_count: int = 0
    transfer_ready: bool = False
    non_authoritative_summary: str


class EnergyPassportView(ORMModel):
    view_name: str = "energy_passport"
    home_id: str
    anchor_type: str = "home_id"
    generated_at: str = "request_time_derived_not_persisted"
    permission_enforcement: str = "not_enforced"
    permission_scope: str = "permission_readiness_metadata_only"
    authority_layer: AuthorityLayer = AuthorityLayer.derived
    data_classification: DataClassification = DataClassification.planning_private
    implementation_boundary: str
    scope: EnergyPassportScope
    summary: EnergyPassportSummary
    system_summary: List[EnergyPassportSystemSummary] = Field(default_factory=list)
    system_financial_obligations: List[EnergyPassportSystemFinancialObligation] = Field(default_factory=list)
    transfer_readiness: EnergyPassportTransferReadiness
    planning_history_summary: EnergyPassportContextSection
    post_install_context: EnergyPassportContextSection
    ownership_context: EnergyPassportContextSection
    future_upgrade_context: EnergyPassportContextSection
    supported_financing_structures: List[EnergyPassportFinancingStructure] = Field(default_factory=list)
    supported_transfer_relevance_flags: List[EnergyPassportTransferRelevanceFlag] = Field(default_factory=list)
    source_basis: EnergyPassportSourceBasis
    assumptions: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    deferred_boundaries: List[str] = Field(default_factory=list)
    capability_boundary_flags: Dict[str, bool] = Field(default_factory=dict)
    compatibility_note: str

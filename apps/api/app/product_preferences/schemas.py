from enum import Enum
from typing import Dict, List

from pydantic import Field

from app.core.schemas import ORMModel
from app.core.types import AuthorityLayer, ConfidenceLevel, DataClassification


class ProductPreferenceStatus(str, Enum):
    review_guidance_available = "review_guidance_available"
    review_required = "review_required"
    blocked_by_missing_inputs = "blocked_by_missing_inputs"
    source_limited = "source_limited"
    unavailable = "unavailable"


class ProductPreferenceCategoryId(str, Enum):
    pv_modules = "pv_modules"
    inverter_topology = "inverter_topology"
    microinverter_string_hybrid_direction = "microinverter_string_hybrid_direction"
    battery_coupling = "battery_coupling"
    backup_scope = "backup_scope"
    gateway_transfer_equipment = "gateway_transfer_equipment"
    backup_loads_panel = "backup_loads_panel"
    monitoring_controls = "monitoring_controls"
    ev_charger_readiness = "ev_charger_readiness"
    main_service_panel_subpanel = "main_service_panel_subpanel"
    aesthetic_preference = "aesthetic_preference"
    contractor_preferred_product_family = "contractor_preferred_product_family"


class ProductPreferenceBlockerCategory(str, Enum):
    missing_input = "missing_input"
    confirmation_gate_open = "confirmation_gate_open"
    product_spec_review_required = "product_spec_review_required"
    source_context_unavailable = "source_context_unavailable"
    unsupported_context = "unsupported_context"
    deferred_boundary = "deferred_boundary"


class ProductPreferenceScope(ORMModel):
    scope_name: str = "phase_12_product_preference_install_logic"
    read_only: bool = True
    additive_only: bool = True
    request_time_only: bool = True
    home_id_anchored: bool = True
    deterministic_for_same_inputs: bool = True
    derived_from_phase_7_shared_compatibility: bool = True
    derived_from_phase_8_topology_takeoff: bool = True
    derived_from_phase_9_estimate_readiness: bool = True
    derived_from_phase_10_proposal_option_sets: bool = True
    derived_from_phase_11_contractor_workflow: bool = False
    homeowner_safe: bool = True
    contractor_facing_review_metadata_present: bool = True
    non_authoritative: bool = True
    persistence_present: bool = False
    migrations_present: bool = False
    write_endpoints_present: bool = False
    auth_security_changes_present: bool = False
    permission_enforcement_present: bool = False
    frontend_present: bool = False
    pricing_present: bool = False
    live_inventory_present: bool = False
    distributor_quotes_present: bool = False
    procurement_present: bool = False
    purchase_links_present: bool = False
    payments_present: bool = False
    final_bill_of_materials_present: bool = False
    final_electrical_design_present: bool = False
    final_product_recommendation_present: bool = False
    product_ranking_present: bool = False
    best_option_selection_present: bool = False
    manufacturer_certification_claim_present: bool = False
    warranty_claim_present: bool = False
    crm_handoff_present: bool = False
    email_automation_present: bool = False
    external_services_present: bool = False
    secrets_present: bool = False
    source_of_truth_mutation_present: bool = False
    twin_id_present: bool = False
    graph_behavior_present: bool = False
    operational_behavior_present: bool = False
    limitations: List[str] = Field(default_factory=list)


class ProductPreferenceSourceBasis(ORMModel):
    source_views: List[str] = Field(default_factory=list)
    source_fields: List[str] = Field(default_factory=list)
    source_refs: List[str] = Field(default_factory=list)
    product_type_refs: List[str] = Field(default_factory=list)
    compatibility_path_refs: List[str] = Field(default_factory=list)
    takeoff_line_refs: List[str] = Field(default_factory=list)
    estimate_gate_refs: List[str] = Field(default_factory=list)
    option_candidate_refs: List[str] = Field(default_factory=list)
    missing_input_refs: List[str] = Field(default_factory=list)
    blocker_refs: List[str] = Field(default_factory=list)
    assumption_refs: List[str] = Field(default_factory=list)
    deferred_boundary_refs: List[str] = Field(default_factory=list)
    unavailable_source_refs: List[str] = Field(default_factory=list)
    basis_quality: str = "request_time_derived_from_existing_phase_7_11_views"
    request_time_derived: bool = True
    verified_fact_claim_present: bool = False
    limitations: List[str] = Field(default_factory=list)


class ProductPreferenceBlocker(ORMModel):
    blocker_id: str
    category_id: ProductPreferenceCategoryId
    blocker_category: ProductPreferenceBlockerCategory
    severity: str
    source_refs: List[str] = Field(default_factory=list)
    gate_refs: List[str] = Field(default_factory=list)
    missing_inputs: List[str] = Field(default_factory=list)
    homeowner_explanation: str
    contractor_review_prompt: str


class ProductPreferenceCategory(ORMModel):
    category_id: ProductPreferenceCategoryId
    category_label: str
    status: ProductPreferenceStatus
    confidence_level: ConfidenceLevel
    planning_direction: str
    install_logic: List[str] = Field(default_factory=list)
    homeowner_explanation: str
    contractor_review_prompt: str
    source_basis: ProductPreferenceSourceBasis
    missing_inputs: List[str] = Field(default_factory=list)
    blockers: List[ProductPreferenceBlocker] = Field(default_factory=list)
    confirmation_gate_ids: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    deferred_boundaries: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class ProductPreferencesSummary(ORMModel):
    overall_status: ProductPreferenceStatus
    confidence_level: ConfidenceLevel
    category_count: int = 0
    source_limited_category_count: int = 0
    blocker_count: int = 0
    missing_input_count: int = 0
    confirmation_gate_count: int = 0
    contractor_review_required: bool = True
    product_selection_allowed: bool = False
    procurement_allowed: bool = False
    pricing_allowed: bool = False
    final_design_allowed: bool = False
    summary_boundary_note: str


class ProductPreferencesView(ORMModel):
    view_name: str = "product_preferences"
    home_id: str
    anchor_type: str = "home_id"
    generated_at: str = "request_time_derived_not_persisted"
    permission_enforcement: str = "not_enforced"
    permission_scope: str = "permission_readiness_metadata_only"
    authority_layer: AuthorityLayer = AuthorityLayer.derived
    data_classification: DataClassification = DataClassification.contractor_scoped
    implementation_boundary: str
    preference_scope: ProductPreferenceScope
    summary: ProductPreferencesSummary
    categories: List[ProductPreferenceCategory] = Field(default_factory=list)
    blockers: List[ProductPreferenceBlocker] = Field(default_factory=list)
    missing_inputs: List[str] = Field(default_factory=list)
    confirmation_gate_ids: List[str] = Field(default_factory=list)
    homeowner_summary: str
    contractor_summary: str
    contractor_review_prompts: List[str] = Field(default_factory=list)
    source_basis: ProductPreferenceSourceBasis
    blocker_category_counts: Dict[str, int] = Field(default_factory=dict)
    assumptions: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    deferred_boundaries: List[str] = Field(default_factory=list)
    compatibility_note: str

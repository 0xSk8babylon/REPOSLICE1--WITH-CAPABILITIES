from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field

from app.core.schemas import ORMModel
from app.core.types import AuthorityLayer, DataClassification, DataOrigin
from app.provenance.schemas import ProvenanceSummary


class TwinPlanningRecordClassification(str, Enum):
    recorded_fact = "recorded_fact"
    source_backed_fact = "source_backed_fact"
    derived_output = "derived_output"
    advisory_output = "advisory_output"
    placeholder = "placeholder"
    unknown = "unknown"


class TwinPlanningProvenanceGapType(str, Enum):
    missing_source = "missing_source"
    partial_source = "partial_source"
    derived_without_lineage = "derived_without_lineage"
    placeholder_without_source = "placeholder_without_source"
    unknown_origin = "unknown_origin"


class TwinPlanningDependencyAwarenessLabel(str, Enum):
    current = "current"
    snapshot_bound = "snapshot_bound"
    needs_recalculation = "needs_recalculation"
    needs_regrounding = "needs_regrounding"
    needs_review = "needs_review"
    stale_unknown = "stale_unknown"


class TwinRuntimeParticipantRole(str, Enum):
    homeowner = "homeowner"
    contractor = "contractor"
    pilot = "pilot"
    partner = "partner"
    internal_system = "internal_system"
    ai = "ai"


class TwinRuntimeVisibilityScope(str, Enum):
    owner_private = "owner_private"
    contractor_scoped = "contractor_scoped"
    pilot_scoped = "pilot_scoped"
    partner_scoped = "partner_scoped"
    internal_governance = "internal_governance"
    ai_grounding = "ai_grounding"


class TwinTopologyLifecycleDomain(str, Enum):
    recorded_current_topology = "recorded_current_topology"
    sandbox_proposed_planning_topology = "sandbox_proposed_planning_topology"
    saved_scenario_revision_topology = "saved_scenario_revision_topology"
    derived_advisory_topology = "derived_advisory_topology"


class TwinPermissionReadinessAudience(str, Enum):
    homeowner = "homeowner"
    homeowner_authorized_household = "homeowner_authorized_household"
    contractor = "contractor"
    ai = "ai"
    internal_system = "internal_system"
    future_engineer = "future_engineer"
    future_utility = "future_utility"


class TwinPermissionReadinessPurpose(str, Enum):
    owner_planning_context = "owner_planning_context"
    contractor_scoping_context = "contractor_scoping_context"
    ai_grounding = "ai_grounding"
    runtime_governance_review = "runtime_governance_review"
    missing_context_review = "missing_context_review"
    future_engineering_review_input = "future_engineering_review_input"
    future_utility_safe_context = "future_utility_safe_context"


class TwinPermissionReadinessDuration(str, Enum):
    not_active_placeholder = "not_active_placeholder"
    one_time_future = "one_time_future"
    session_bound_future = "session_bound_future"
    project_bound_future = "project_bound_future"
    time_bound_future = "time_bound_future"
    until_revoked_future = "until_revoked_future"


class TwinPermissionReadinessRevocationState(str, Enum):
    not_applicable_no_active_permission = "not_applicable_no_active_permission"
    future_revocable = "future_revocable"
    future_expirable = "future_expirable"
    future_supersedable = "future_supersedable"


class TwinPlanningDependencyHook(ORMModel):
    source_entity_type: str
    source_entity_id: Optional[str] = None
    target_entity_type: str
    target_entity_id: Optional[str] = None
    relationship: str
    rule_keys: List[str] = Field(default_factory=list)
    confidence_level: Optional[str] = None
    note: str


class TwinPlanningProvenanceGap(ORMModel):
    gap_type: TwinPlanningProvenanceGapType
    entity_type: str
    entity_id: Optional[str] = None
    field_name: Optional[str] = None
    severity: str = "warning"
    reason: str
    limitations: List[str] = Field(default_factory=list)


class TwinPlanningDependencyAwareness(ORMModel):
    label: TwinPlanningDependencyAwarenessLabel
    entity_type: str
    entity_id: Optional[str] = None
    reason: str
    rule_keys: List[str] = Field(default_factory=list)
    source_gap_types: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class TwinPlanningChangeImpactHint(ORMModel):
    source_entity_type: str
    source_entity_id: Optional[str] = None
    impacted_entity_type: str
    impacted_entity_id: Optional[str] = None
    relationship: str
    reason: str
    rule_keys: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class TwinPlanningDependencyWarning(ORMModel):
    warning_type: str
    entity_type: str
    entity_id: Optional[str] = None
    related_entity_type: Optional[str] = None
    related_entity_id: Optional[str] = None
    severity: str = "info"
    reason: str
    rule_keys: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class TwinPermissionReadinessAudienceConcept(ORMModel):
    audience: TwinPermissionReadinessAudience
    readiness_only: bool = True
    active_permission_grant_present: bool = False
    reason: str
    limitations: List[str] = Field(default_factory=list)


class TwinPermissionReadinessPurposeConcept(ORMModel):
    purpose: TwinPermissionReadinessPurpose
    readiness_only: bool = True
    active_permission_grant_present: bool = False
    reason: str
    limitations: List[str] = Field(default_factory=list)


class TwinPermissionReadinessDurationConcept(ORMModel):
    duration: TwinPermissionReadinessDuration = TwinPermissionReadinessDuration.not_active_placeholder
    readiness_only: bool = True
    active_permission_grant_present: bool = False
    starts_at: Optional[str] = None
    expires_at: Optional[str] = None
    reason: str
    limitations: List[str] = Field(default_factory=list)


class TwinPermissionReadinessRevocationConcept(ORMModel):
    revocation_state: TwinPermissionReadinessRevocationState = (
        TwinPermissionReadinessRevocationState.not_applicable_no_active_permission
    )
    readiness_only: bool = True
    active_permission_grant_present: bool = False
    revoked_at: Optional[str] = None
    reason: str
    limitations: List[str] = Field(default_factory=list)


class TwinPermissionConsentArtifactPlaceholder(ORMModel):
    consent_artifact_placeholder_only: bool = True
    active_consent_present: bool = False
    consent_artifact_id: Optional[str] = None
    consent_text_version: Optional[str] = None
    reason: str
    limitations: List[str] = Field(default_factory=list)


class TwinPermissionHomeownerAuthorityMetadata(ORMModel):
    homeowner_authority_preserved: bool = True
    permission_grant_required_for_external_sharing: bool = True
    active_permission_grant_present: bool = False
    authority_note: str
    limitations: List[str] = Field(default_factory=list)


class TwinViewPermissionAlignmentMetadata(ORMModel):
    view_name: str
    audience: TwinPermissionReadinessAudience
    purpose: TwinPermissionReadinessPurpose
    visibility_scope: Optional[TwinRuntimeVisibilityScope] = None
    alignment_status: str = "readiness_metadata_only"
    permission_enforcement: str = "not_enforced"
    active_permission_grant_present: bool = False
    active_consent_present: bool = False
    limitations: List[str] = Field(default_factory=list)


class TwinPlanningPermissionReadiness(ORMModel):
    permission_required: bool
    permission_not_enforced: bool = True
    audience: str
    purpose: str
    minimum_necessary: bool
    audience_readiness: Optional[TwinPermissionReadinessAudienceConcept] = None
    purpose_readiness: Optional[TwinPermissionReadinessPurposeConcept] = None
    duration_readiness: Optional[TwinPermissionReadinessDurationConcept] = None
    revocation_state_readiness: Optional[TwinPermissionReadinessRevocationConcept] = None
    consent_artifact_placeholder: Optional[TwinPermissionConsentArtifactPlaceholder] = None
    homeowner_authority: Optional[TwinPermissionHomeownerAuthorityMetadata] = None
    view_permission_alignment: Optional[TwinViewPermissionAlignmentMetadata] = None
    visibility_limitations: List[str] = Field(default_factory=list)
    deferred_capabilities: List[str] = Field(default_factory=list)


class TwinRuntimeParticipant(ORMModel):
    role: TwinRuntimeParticipantRole
    participant_id: Optional[str] = None
    display_name: Optional[str] = None
    relationship_to_home: Optional[str] = None


class TwinRuntimeViewContext(ORMModel):
    view_name: str
    role: TwinRuntimeParticipantRole
    visibility_scope: TwinRuntimeVisibilityScope
    purpose: str
    minimum_necessary: bool
    permission_basis: str = "permission_readiness_metadata_only"
    permission_enforcement: str = "not_enforced"
    canonical_anchor: str = "home_id"


class TwinRuntimeContributionIdentity(ORMModel):
    contributor_type: str
    contributor_ref: Optional[str] = None
    data_origin: Optional[DataOrigin] = None
    source_document_ids: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class TwinTopologyNode(ORMModel):
    node_id: str
    section_key: str
    entity_type: str
    entity_id: Optional[str] = None
    label: str
    lifecycle_domain: TwinTopologyLifecycleDomain
    classification: TwinPlanningRecordClassification
    authority_layer: AuthorityLayer
    data_classification: DataClassification = DataClassification.planning_private
    data_origin: Optional[DataOrigin] = None
    source_document_ids: List[str] = Field(default_factory=list)
    rule_keys: List[str] = Field(default_factory=list)
    provenance_gap_types: List[str] = Field(default_factory=list)
    dependency_awareness_labels: List[str] = Field(default_factory=list)
    permission_not_enforced: bool = True
    limitations: List[str] = Field(default_factory=list)


class TwinTopologyEdge(ORMModel):
    edge_id: str
    source_node_id: str
    target_node_id: str
    source_entity_type: str
    source_entity_id: Optional[str] = None
    target_entity_type: str
    target_entity_id: Optional[str] = None
    relationship: str
    lifecycle_domain: TwinTopologyLifecycleDomain
    rule_keys: List[str] = Field(default_factory=list)
    confidence_level: Optional[str] = None
    note: str
    limitations: List[str] = Field(default_factory=list)


class TwinTopologyLifecycleReadinessHint(ORMModel):
    lifecycle_domain: TwinTopologyLifecycleDomain
    readiness_status: str
    node_count: int = 0
    edge_count: int = 0
    source_document_count: int = 0
    provenance_gap_types: List[str] = Field(default_factory=list)
    dependency_awareness_labels: List[str] = Field(default_factory=list)
    planning_dependency_warning_types: List[str] = Field(default_factory=list)
    derived_from: List[str] = Field(default_factory=list)
    hints: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class TwinTopologyDeferredLifecycleDomain(ORMModel):
    lifecycle_domain: str
    current_runtime_status: str = "deferred_not_implemented"
    deferred_reason: str
    required_future_foundations: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class TwinTopologyMissingReadinessIndicator(ORMModel):
    indicator: str
    present: bool = False
    source_marker_found: bool = False
    reason: str
    derived_from: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class TwinTopologyLifecycleReadinessSummary(ORMModel):
    readiness_scope: str = "topology_snapshot_metadata_only"
    descriptive_only: bool = True
    read_only: bool = True
    topology_derived: bool = True
    provenance_aware: bool = True
    lifecycle_workflows_present: bool = False
    promotion_engine_present: bool = False
    event_log_present: bool = False
    simulation_present: bool = False
    phase_3_intelligence_present: bool = False
    node_count: int = 0
    edge_count: int = 0
    domains_present: List[str] = Field(default_factory=list)
    domains_deferred: List[str] = Field(default_factory=list)
    provenance_gap_count: int = 0
    planning_dependency_warning_count: int = 0
    dependency_awareness_labels: List[str] = Field(default_factory=list)
    missing_readiness_indicator_count: int = 0
    limitations: List[str] = Field(default_factory=list)


class TwinTopologyMissingRelationshipIndicator(ORMModel):
    indicator: str
    entity_type: str
    entity_id: Optional[str] = None
    field_name: Optional[str] = None
    attempted_value: Optional[str] = None
    relationship_family: str
    reason: str
    derived_from: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class TwinTopologyRelationshipCoverageSummary(ORMModel):
    coverage_scope: str = "topology_snapshot_relationship_metadata_only"
    descriptive_only: bool = True
    read_only: bool = True
    topology_derived: bool = True
    graph_engine_present: bool = False
    lifecycle_workflows_present: bool = False
    promotion_engine_present: bool = False
    event_log_present: bool = False
    recalculation_engine_present: bool = False
    invalidation_engine_present: bool = False
    simulation_present: bool = False
    what_if_analysis_present: bool = False
    phase_3_intelligence_present: bool = False
    relationship_edge_count: int = 0
    dependency_hook_edge_count: int = 0
    coverage_by_relationship_family: Dict[str, int] = Field(default_factory=dict)
    missing_relationship_indicator_count: int = 0
    unresolved_pathway_endpoint_count: int = 0
    limitations: List[str] = Field(default_factory=list)


class TwinPlanningContextRecord(ORMModel):
    entity_type: str
    entity_id: Optional[str] = None
    label: str
    classification: TwinPlanningRecordClassification
    authority_layer: AuthorityLayer
    data_classification: DataClassification = DataClassification.planning_private
    data_origin: Optional[DataOrigin] = None
    record: Dict[str, Any] = Field(default_factory=dict)
    provenance_summary: Optional[ProvenanceSummary] = None
    source_document_ids: List[str] = Field(default_factory=list)
    rule_keys: List[str] = Field(default_factory=list)
    dependency_hooks: List[TwinPlanningDependencyHook] = Field(default_factory=list)
    classification_reasons: List[str] = Field(default_factory=list)
    missing_fields: List[str] = Field(default_factory=list)
    provenance_gaps: List[TwinPlanningProvenanceGap] = Field(default_factory=list)
    dependency_awareness: List[TwinPlanningDependencyAwareness] = Field(default_factory=list)
    change_impact_hints: List[TwinPlanningChangeImpactHint] = Field(default_factory=list)
    planning_dependency_warnings: List[TwinPlanningDependencyWarning] = Field(default_factory=list)
    permission_readiness: Optional[TwinPlanningPermissionReadiness] = None
    limitations: List[str] = Field(default_factory=list)


class TwinRuntimeProjectionRecord(ORMModel):
    section_key: str
    entity_type: str
    entity_id: Optional[str] = None
    label: str
    visibility_scope: TwinRuntimeVisibilityScope
    classification: TwinPlanningRecordClassification
    authority_layer: AuthorityLayer
    data_classification: DataClassification = DataClassification.planning_private
    data_origin: Optional[DataOrigin] = None
    fields: Dict[str, Any] = Field(default_factory=dict)
    provenance_summary: Optional[ProvenanceSummary] = None
    source_document_ids: List[str] = Field(default_factory=list)
    contributor_identity: TwinRuntimeContributionIdentity
    rule_keys: List[str] = Field(default_factory=list)
    dependency_hooks: List[TwinPlanningDependencyHook] = Field(default_factory=list)
    missing_fields: List[str] = Field(default_factory=list)
    provenance_gaps: List[TwinPlanningProvenanceGap] = Field(default_factory=list)
    dependency_awareness: List[TwinPlanningDependencyAwareness] = Field(default_factory=list)
    change_impact_hints: List[TwinPlanningChangeImpactHint] = Field(default_factory=list)
    planning_dependency_warnings: List[TwinPlanningDependencyWarning] = Field(default_factory=list)
    permission_readiness: Optional[TwinPlanningPermissionReadiness] = None
    limitations: List[str] = Field(default_factory=list)


class TwinPlanningContextSection(ORMModel):
    section_key: str
    label: str
    records: List[TwinPlanningContextRecord] = Field(default_factory=list)
    dependency_awareness_summary: Dict[str, int] = Field(default_factory=dict)
    permission_readiness: Optional[TwinPlanningPermissionReadiness] = None
    notes: List[str] = Field(default_factory=list)


class TwinPlanningContext(ORMModel):
    context_id: str
    home_id: str
    anchor_type: str = "home_id"
    context_label: str
    authority_layer: AuthorityLayer = AuthorityLayer.canonical
    data_classification: DataClassification = DataClassification.planning_private
    permission_enforcement: str = "not_enforced"
    implementation_boundary: str
    sections: List[TwinPlanningContextSection] = Field(default_factory=list)
    classification_summary: Dict[str, int] = Field(default_factory=dict)
    provenance_gaps: List[str] = Field(default_factory=list)
    typed_provenance_gaps: List[TwinPlanningProvenanceGap] = Field(default_factory=list)
    continuity_gaps: List[str] = Field(default_factory=list)
    dependency_hooks: List[TwinPlanningDependencyHook] = Field(default_factory=list)
    dependency_awareness_summary: Dict[str, int] = Field(default_factory=dict)
    permission_readiness: Optional[TwinPlanningPermissionReadiness] = None
    limitations: List[str] = Field(default_factory=list)


class TwinRuntimeProjectionView(ORMModel):
    view_name: str = "twin_runtime_projection"
    home_id: str
    anchor_type: str = "home_id"
    participant: TwinRuntimeParticipant
    view_context: TwinRuntimeViewContext
    permission_enforcement: str = "not_enforced"
    implementation_boundary: str
    included_sections: List[str] = Field(default_factory=list)
    excluded_sections: List[str] = Field(default_factory=list)
    projection_records: List[TwinRuntimeProjectionRecord] = Field(default_factory=list)
    classification_summary: Dict[str, int] = Field(default_factory=dict)
    provenance_gaps: List[TwinPlanningProvenanceGap] = Field(default_factory=list)
    dependency_hooks: List[TwinPlanningDependencyHook] = Field(default_factory=list)
    dependency_awareness_summary: Dict[str, int] = Field(default_factory=dict)
    permission_readiness: Optional[TwinPlanningPermissionReadiness] = None
    limitations: List[str] = Field(default_factory=list)
    compatibility_note: str


class TwinTopologySnapshot(ORMModel):
    view_name: str = "topology_snapshot"
    home_id: str
    anchor_type: str = "home_id"
    permission_enforcement: str = "not_enforced"
    implementation_boundary: str
    nodes: List[TwinTopologyNode] = Field(default_factory=list)
    edges: List[TwinTopologyEdge] = Field(default_factory=list)
    scenario_branch_references: List[Dict[str, Any]] = Field(default_factory=list)
    revision_lineage_references: List[Dict[str, Any]] = Field(default_factory=list)
    lifecycle_domain_summary: Dict[str, int] = Field(default_factory=dict)
    lifecycle_readiness_summary: TwinTopologyLifecycleReadinessSummary
    lifecycle_readiness_hints: List[TwinTopologyLifecycleReadinessHint] = Field(default_factory=list)
    deferred_lifecycle_domains: List[TwinTopologyDeferredLifecycleDomain] = Field(default_factory=list)
    missing_readiness_indicators: List[TwinTopologyMissingReadinessIndicator] = Field(default_factory=list)
    relationship_coverage_summary: TwinTopologyRelationshipCoverageSummary
    missing_relationship_indicators: List[TwinTopologyMissingRelationshipIndicator] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    compatibility_note: str


class TwinDependencyImpactStatementBasis(ORMModel):
    source_view_names: List[str] = Field(default_factory=list)
    source_section_keys: List[str] = Field(default_factory=list)
    topology_node_ids: List[str] = Field(default_factory=list)
    topology_edge_ids: List[str] = Field(default_factory=list)
    lifecycle_readiness_signals_used: List[str] = Field(default_factory=list)
    dependency_warning_refs: List[str] = Field(default_factory=list)
    provenance_gap_refs: List[str] = Field(default_factory=list)
    missing_readiness_indicator_refs: List[str] = Field(default_factory=list)
    missing_relationship_indicator_refs: List[str] = Field(default_factory=list)
    derived_from: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class TwinDependencyImpactPostureItem(ORMModel):
    impact_area: str
    posture: str
    statement: str
    confidence_posture: str
    basis: TwinDependencyImpactStatementBasis
    limitations: List[str] = Field(default_factory=list)


class TwinDependencyMissingInputItem(ORMModel):
    missing_input: str
    reason: str
    basis: TwinDependencyImpactStatementBasis
    limitations: List[str] = Field(default_factory=list)


class TwinDependencyReasoningType(str, Enum):
    source_dependency = "source_dependency"
    topology_dependency = "topology_dependency"
    lifecycle_dependency = "lifecycle_dependency"
    rule_dependency = "rule_dependency"
    provenance_dependency = "provenance_dependency"
    permission_readiness_dependency = "permission_readiness_dependency"
    continuity_snapshot_dependency = "continuity_snapshot_dependency"
    missing_information_dependency = "missing_information_dependency"


class TwinDependencyReasoningScope(ORMModel):
    reasoning_scope: str = "phase_3b_dependency_reasoning"
    descriptive_only: bool = True
    read_only: bool = True
    request_time_only: bool = True
    home_id_anchored: bool = True
    derived_from_existing_twin_context: bool = True
    derived_from_topology_snapshot: bool = True
    derived_from_dependency_impact_readiness: bool = True
    deterministic_for_same_inputs: bool = True
    ai_generated_facts_present: bool = False
    new_topology_facts_created: bool = False
    graph_database_present: bool = False
    graph_engine_present: bool = False
    scenario_engine_present: bool = False
    scenario_intelligence_present: bool = False
    simulation_present: bool = False
    what_if_analysis_present: bool = False
    impact_propagation_engine_present: bool = False
    stale_state_created: bool = False
    recalculation_engine_present: bool = False
    invalidation_engine_present: bool = False
    recommendation_actions_present: bool = False
    optimization_present: bool = False
    ranking_present: bool = False
    authorization_present: bool = False
    permission_enforcement_present: bool = False
    export_present: bool = False
    operational_behavior_present: bool = False
    limitations: List[str] = Field(default_factory=list)


class TwinDependencyReasoningItem(ORMModel):
    reasoning_type: TwinDependencyReasoningType
    subject_ref: str
    statement: str
    confidence_posture: str
    basis: TwinDependencyImpactStatementBasis
    limitations: List[str] = Field(default_factory=list)


class TwinDependencyReasoningView(ORMModel):
    view_name: str = "dependency_reasoning"
    home_id: str
    anchor_type: str = "home_id"
    permission_enforcement: str = "not_enforced"
    authority_layer: AuthorityLayer = AuthorityLayer.derived
    data_classification: DataClassification = DataClassification.planning_private
    implementation_boundary: str
    source_basis: TwinDependencyImpactStatementBasis
    reasoning_scope: TwinDependencyReasoningScope
    dependency_type_summary: Dict[str, int] = Field(default_factory=dict)
    dependency_reasoning_items: List[TwinDependencyReasoningItem] = Field(default_factory=list)
    upstream_downstream_interpretations: List[TwinDependencyReasoningItem] = Field(default_factory=list)
    lifecycle_dependency_context: List[TwinDependencyReasoningItem] = Field(default_factory=list)
    provenance_dependency_context: List[TwinDependencyReasoningItem] = Field(default_factory=list)
    missing_information_context: List[TwinDependencyReasoningItem] = Field(default_factory=list)
    confidence_posture: List[TwinDependencyReasoningItem] = Field(default_factory=list)
    deferred_capabilities: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    compatibility_note: str


class TwinPlanningIntelligenceReadinessArea(str, Enum):
    topology_explanation = "topology_explanation"
    lifecycle_explanation = "lifecycle_explanation"
    relationship_coverage_explanation = "relationship_coverage_explanation"
    dependency_impact_readiness = "dependency_impact_readiness"
    dependency_reasoning = "dependency_reasoning"
    provenance_gap_reporting = "provenance_gap_reporting"
    permission_readiness_metadata = "permission_readiness_metadata"
    scenario_intelligence = "scenario_intelligence"
    impact_propagation = "impact_propagation"
    stale_state_persistence = "stale_state_persistence"
    recalculation = "recalculation"
    invalidation = "invalidation"
    simulation = "simulation"
    what_if_analysis = "what_if_analysis"
    optimization = "optimization"
    ranking = "ranking"
    economic_reasoning = "economic_reasoning"
    utility_readiness_logic = "utility_readiness_logic"
    survivability_recharge_modeling = "survivability_recharge_modeling"
    compatibility_engine = "compatibility_engine"
    recommendation_or_proposal_generation = "recommendation_or_proposal_generation"
    exports = "exports"
    auth_rbac_abac = "auth_rbac_abac"
    permission_enforcement = "permission_enforcement"
    marketplace = "marketplace"
    operational_behavior = "operational_behavior"


class TwinPlanningIntelligenceReadinessScope(ORMModel):
    readiness_scope: str = "phase_3c_planning_intelligence_readiness"
    descriptive_only: bool = True
    readiness_inventory_only: bool = True
    read_only: bool = True
    request_time_only: bool = True
    home_id_anchored: bool = True
    derived_from_existing_twin_context: bool = True
    derived_from_topology_snapshot: bool = True
    derived_from_dependency_impact_readiness: bool = True
    derived_from_dependency_reasoning: bool = True
    deterministic_for_same_inputs: bool = True
    ai_generated_facts_present: bool = False
    persistence_present: bool = False
    migrations_present: bool = False
    twin_id_present: bool = False
    canonical_twin_runtime_model_changes_present: bool = False
    new_topology_facts_created: bool = False
    graph_database_present: bool = False
    graph_engine_present: bool = False
    scenario_intelligence_present: bool = False
    impact_propagation_present: bool = False
    stale_state_persistence_present: bool = False
    recalculation_engine_present: bool = False
    invalidation_engine_present: bool = False
    simulation_present: bool = False
    what_if_analysis_present: bool = False
    optimization_present: bool = False
    ranking_present: bool = False
    recommendations_present: bool = False
    economic_reasoning_present: bool = False
    utility_readiness_logic_present: bool = False
    survivability_recharge_modeling_present: bool = False
    compatibility_engine_present: bool = False
    proposal_generation_present: bool = False
    export_present: bool = False
    auth_present: bool = False
    rbac_abac_present: bool = False
    permission_enforcement_present: bool = False
    marketplace_present: bool = False
    operational_behavior_present: bool = False
    limitations: List[str] = Field(default_factory=list)


class TwinPlanningIntelligenceReadinessItem(ORMModel):
    intelligence_area: TwinPlanningIntelligenceReadinessArea
    posture: str
    statement: str
    available_evidence: List[str] = Field(default_factory=list)
    missing_prerequisites: List[str] = Field(default_factory=list)
    unsafe_assumptions: List[str] = Field(default_factory=list)
    confidence_posture: str
    provenance_presence_is_verification: bool = False
    permission_readiness_is_enforcement: bool = False
    basis: TwinDependencyImpactStatementBasis
    limitations: List[str] = Field(default_factory=list)


class TwinPlanningIntelligenceReadinessView(ORMModel):
    view_name: str = "planning_intelligence_readiness"
    home_id: str
    anchor_type: str = "home_id"
    permission_enforcement: str = "not_enforced"
    authority_layer: AuthorityLayer = AuthorityLayer.derived
    data_classification: DataClassification = DataClassification.planning_private
    implementation_boundary: str
    source_basis: TwinDependencyImpactStatementBasis
    readiness_scope: TwinPlanningIntelligenceReadinessScope
    ready_areas: List[TwinPlanningIntelligenceReadinessItem] = Field(default_factory=list)
    blocked_deferred_areas: List[TwinPlanningIntelligenceReadinessItem] = Field(default_factory=list)
    provenance_permission_basis: List[TwinPlanningIntelligenceReadinessItem] = Field(default_factory=list)
    missing_prerequisites: List[str] = Field(default_factory=list)
    available_evidence: List[str] = Field(default_factory=list)
    unsafe_assumptions: List[str] = Field(default_factory=list)
    deferred_reasoning_boundaries: List[str] = Field(default_factory=list)
    confidence_posture: List[TwinPlanningIntelligenceReadinessItem] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    compatibility_note: str


class TwinAdvisoryContextAssemblyArea(str, Enum):
    homeowner_goals = "homeowner_goals"
    topology_facts = "topology_facts"
    equipment_site_facts = "equipment_site_facts"
    provenance_basis = "provenance_basis"
    permission_readiness_metadata = "permission_readiness_metadata"
    missing_data = "missing_data"
    unsafe_assumptions = "unsafe_assumptions"
    advisory_input_readiness = "advisory_input_readiness"
    deferred_advisory_output_boundaries = "deferred_advisory_output_boundaries"


class TwinAdvisoryContextAssemblyScope(ORMModel):
    assembly_scope: str = "phase_3d_advisory_context_assembly"
    advisory_input_context_only: bool = True
    descriptive_only: bool = True
    read_only: bool = True
    request_time_only: bool = True
    home_id_anchored: bool = True
    derived_from_existing_twin_context: bool = True
    derived_from_topology_snapshot: bool = True
    derived_from_dependency_impact_readiness: bool = True
    derived_from_dependency_reasoning: bool = True
    derived_from_planning_intelligence_readiness: bool = True
    deterministic_for_same_inputs: bool = True
    advice_generated: bool = False
    recommendations_present: bool = False
    ranking_present: bool = False
    optimization_present: bool = False
    scenario_simulation_present: bool = False
    what_if_analysis_present: bool = False
    proposal_generation_present: bool = False
    contractor_sales_logic_present: bool = False
    homeowner_guidance_outputs_present: bool = False
    permission_enforcement_present: bool = False
    auth_present: bool = False
    rbac_abac_present: bool = False
    persistence_present: bool = False
    migrations_present: bool = False
    twin_id_present: bool = False
    graph_engine_present: bool = False
    export_present: bool = False
    operational_behavior_present: bool = False
    limitations: List[str] = Field(default_factory=list)


class TwinAdvisoryContextAssemblyItem(ORMModel):
    context_area: TwinAdvisoryContextAssemblyArea
    posture: str
    statement: str
    assembled_inputs: List[str] = Field(default_factory=list)
    missing_inputs: List[str] = Field(default_factory=list)
    unsafe_assumptions: List[str] = Field(default_factory=list)
    confidence_posture: str
    basis: TwinDependencyImpactStatementBasis
    limitations: List[str] = Field(default_factory=list)


class TwinAdvisoryContextAssemblyView(ORMModel):
    view_name: str = "advisory_context_assembly"
    home_id: str
    anchor_type: str = "home_id"
    permission_enforcement: str = "not_enforced"
    authority_layer: AuthorityLayer = AuthorityLayer.derived
    data_classification: DataClassification = DataClassification.planning_private
    implementation_boundary: str
    source_basis: TwinDependencyImpactStatementBasis
    assembly_scope: TwinAdvisoryContextAssemblyScope
    homeowner_goals: List[TwinAdvisoryContextAssemblyItem] = Field(default_factory=list)
    topology_facts: List[TwinAdvisoryContextAssemblyItem] = Field(default_factory=list)
    equipment_site_facts: List[TwinAdvisoryContextAssemblyItem] = Field(default_factory=list)
    provenance_basis: List[TwinAdvisoryContextAssemblyItem] = Field(default_factory=list)
    permission_readiness_metadata: List[TwinAdvisoryContextAssemblyItem] = Field(default_factory=list)
    missing_data: List[TwinAdvisoryContextAssemblyItem] = Field(default_factory=list)
    unsafe_assumptions: List[TwinAdvisoryContextAssemblyItem] = Field(default_factory=list)
    advisory_input_readiness: List[TwinAdvisoryContextAssemblyItem] = Field(default_factory=list)
    deferred_advisory_output_boundaries: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    compatibility_note: str


class TwinConstraintRiskReasoningArea(str, Enum):
    missing_equipment_specs = "missing_equipment_specs"
    incomplete_topology = "incomplete_topology"
    low_trust_assumptions = "low_trust_assumptions"
    unsupported_load_data = "unsupported_load_data"
    permission_limited_visibility = "permission_limited_visibility"
    lifecycle_conflicts = "lifecycle_conflicts"
    provenance_gaps = "provenance_gaps"
    contractor_install_complexity_risks = "contractor_install_complexity_risks"
    field_verification_needs = "field_verification_needs"
    professional_review_boundaries = "professional_review_boundaries"


class TwinConstraintRiskReasoningScope(ORMModel):
    reasoning_scope: str = "phase_3e_constraint_risk_reasoning"
    constraint_risk_explanation_only: bool = True
    descriptive_only: bool = True
    read_only: bool = True
    request_time_only: bool = True
    home_id_anchored: bool = True
    derived_from_existing_twin_context: bool = True
    derived_from_topology_snapshot: bool = True
    derived_from_dependency_impact_readiness: bool = True
    derived_from_dependency_reasoning: bool = True
    derived_from_planning_intelligence_readiness: bool = True
    derived_from_advisory_context_assembly: bool = True
    deterministic_for_same_inputs: bool = True
    recommendations_present: bool = False
    priority_ranking_present: bool = False
    optimization_present: bool = False
    scenario_simulation_present: bool = False
    what_if_analysis_present: bool = False
    proposal_generation_present: bool = False
    final_design_guidance_present: bool = False
    contractor_directives_present: bool = False
    homeowner_directives_present: bool = False
    economic_reasoning_present: bool = False
    utility_readiness_logic_present: bool = False
    permission_enforcement_present: bool = False
    auth_present: bool = False
    rbac_abac_present: bool = False
    persistence_present: bool = False
    migrations_present: bool = False
    twin_id_present: bool = False
    graph_engine_present: bool = False
    export_present: bool = False
    operational_behavior_present: bool = False
    limitations: List[str] = Field(default_factory=list)


class TwinConstraintRiskReasoningItem(ORMModel):
    risk_area: TwinConstraintRiskReasoningArea
    non_decisional_severity_label: str
    statement: str
    observed_constraint_refs: List[str] = Field(default_factory=list)
    missing_inputs: List[str] = Field(default_factory=list)
    low_trust_inputs: List[str] = Field(default_factory=list)
    unsafe_assumptions: List[str] = Field(default_factory=list)
    professional_review_boundaries: List[str] = Field(default_factory=list)
    confidence_posture: str
    basis: TwinDependencyImpactStatementBasis
    limitations: List[str] = Field(default_factory=list)


class TwinConstraintRiskReasoningView(ORMModel):
    view_name: str = "constraint_risk_reasoning"
    home_id: str
    anchor_type: str = "home_id"
    permission_enforcement: str = "not_enforced"
    authority_layer: AuthorityLayer = AuthorityLayer.derived
    data_classification: DataClassification = DataClassification.planning_private
    implementation_boundary: str
    source_basis: TwinDependencyImpactStatementBasis
    reasoning_scope: TwinConstraintRiskReasoningScope
    constraint_risk_items: List[TwinConstraintRiskReasoningItem] = Field(default_factory=list)
    missing_equipment_specs: List[TwinConstraintRiskReasoningItem] = Field(default_factory=list)
    incomplete_topology: List[TwinConstraintRiskReasoningItem] = Field(default_factory=list)
    low_trust_assumptions: List[TwinConstraintRiskReasoningItem] = Field(default_factory=list)
    unsupported_load_data: List[TwinConstraintRiskReasoningItem] = Field(default_factory=list)
    permission_limited_visibility: List[TwinConstraintRiskReasoningItem] = Field(default_factory=list)
    lifecycle_conflicts: List[TwinConstraintRiskReasoningItem] = Field(default_factory=list)
    provenance_gaps: List[TwinConstraintRiskReasoningItem] = Field(default_factory=list)
    contractor_install_complexity_risks: List[TwinConstraintRiskReasoningItem] = Field(default_factory=list)
    field_verification_needs: List[TwinConstraintRiskReasoningItem] = Field(default_factory=list)
    professional_review_boundaries: List[TwinConstraintRiskReasoningItem] = Field(default_factory=list)
    deferred_capabilities: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    compatibility_note: str


class TwinDependencyImpactReadinessSummary(ORMModel):
    readiness_scope: str = "phase_3a_dependency_impact_readiness"
    descriptive_only: bool = True
    read_only: bool = True
    request_time_only: bool = True
    home_id_anchored: bool = True
    derived_from_existing_twin_context: bool = True
    derived_from_topology_snapshot: bool = True
    deterministic_for_same_inputs: bool = True
    ai_generated_facts_present: bool = False
    graph_database_present: bool = False
    graph_engine_present: bool = False
    scenario_engine_present: bool = False
    simulation_present: bool = False
    what_if_analysis_present: bool = False
    recalculation_engine_present: bool = False
    invalidation_engine_present: bool = False
    recommendation_actions_present: bool = False
    optimization_present: bool = False
    ranking_present: bool = False
    authorization_present: bool = False
    permission_enforcement_present: bool = False
    export_present: bool = False
    operational_behavior_present: bool = False
    limitations: List[str] = Field(default_factory=list)


class TwinDependencyImpactReadinessView(ORMModel):
    view_name: str = "dependency_impact_readiness"
    home_id: str
    anchor_type: str = "home_id"
    permission_enforcement: str = "not_enforced"
    authority_layer: AuthorityLayer = AuthorityLayer.derived
    data_classification: DataClassification = DataClassification.planning_private
    implementation_boundary: str
    source_basis: TwinDependencyImpactStatementBasis
    readiness_summary: TwinDependencyImpactReadinessSummary
    lifecycle_scope: List[TwinDependencyImpactPostureItem] = Field(default_factory=list)
    dependency_impact_posture: List[TwinDependencyImpactPostureItem] = Field(default_factory=list)
    missing_inputs: List[TwinDependencyMissingInputItem] = Field(default_factory=list)
    provenance_gap_posture: List[TwinDependencyImpactPostureItem] = Field(default_factory=list)
    confidence_posture: List[TwinDependencyImpactPostureItem] = Field(default_factory=list)
    deferred_capabilities: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    compatibility_note: str


class AIDesignGroundingRecord(ORMModel):
    section_key: str
    entity_type: str
    entity_id: Optional[str] = None
    label: str
    classification: TwinPlanningRecordClassification
    authority_layer: AuthorityLayer
    data_classification: DataClassification = DataClassification.planning_private
    data_origin: Optional[DataOrigin] = None
    fields: Dict[str, Any] = Field(default_factory=dict)
    provenance_summary: Optional[ProvenanceSummary] = None
    source_document_ids: List[str] = Field(default_factory=list)
    rule_keys: List[str] = Field(default_factory=list)
    dependency_hooks: List[TwinPlanningDependencyHook] = Field(default_factory=list)
    missing_fields: List[str] = Field(default_factory=list)
    provenance_gaps: List[TwinPlanningProvenanceGap] = Field(default_factory=list)
    dependency_awareness: List[TwinPlanningDependencyAwareness] = Field(default_factory=list)
    change_impact_hints: List[TwinPlanningChangeImpactHint] = Field(default_factory=list)
    planning_dependency_warnings: List[TwinPlanningDependencyWarning] = Field(default_factory=list)
    permission_readiness: Optional[TwinPlanningPermissionReadiness] = None
    limitations: List[str] = Field(default_factory=list)


class AIDesignGroundingView(ORMModel):
    view_name: str = "ai_design_grounding"
    home_id: str
    anchor_type: str = "home_id"
    target_design_id: Optional[str] = None
    audience: str = "ai"
    purpose: str = "grounded_design_recommendation"
    permission_enforcement: str = "not_enforced"
    authority_layer: AuthorityLayer = AuthorityLayer.advisory
    data_classification: DataClassification = DataClassification.planning_private
    implementation_boundary: str
    included_sections: List[str] = Field(default_factory=list)
    excluded_sections: List[str] = Field(default_factory=list)
    grounding_records: List[AIDesignGroundingRecord] = Field(default_factory=list)
    provenance_gaps: List[TwinPlanningProvenanceGap] = Field(default_factory=list)
    dependency_hooks: List[TwinPlanningDependencyHook] = Field(default_factory=list)
    dependency_awareness_summary: Dict[str, int] = Field(default_factory=dict)
    permission_readiness: Optional[TwinPlanningPermissionReadiness] = None
    limitations: List[str] = Field(default_factory=list)
    compatibility_note: str

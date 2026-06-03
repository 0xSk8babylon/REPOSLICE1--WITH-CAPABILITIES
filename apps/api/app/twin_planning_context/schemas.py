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

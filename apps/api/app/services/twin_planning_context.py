from collections import Counter
from typing import Dict, Iterable, List, Optional

from app.core.repository import repository
from app.core.types import AuthorityLayer, DataClassification, DataOrigin
from app.design_advisor.schemas import ResilienceRecommendation
from app.provenance.schemas import ProvenanceSummary
from app.services.design_advisor import design_advisor_service
from app.services.provenance import provenance_service
from app.twin_planning_context.schemas import (
    AIDesignGroundingRecord,
    AIDesignGroundingView,
    TwinDependencyImpactPostureItem,
    TwinDependencyImpactReadinessSummary,
    TwinDependencyImpactReadinessView,
    TwinDependencyImpactStatementBasis,
    TwinDependencyMissingInputItem,
    TwinDependencyReasoningItem,
    TwinDependencyReasoningScope,
    TwinDependencyReasoningType,
    TwinDependencyReasoningView,
    TwinPlanningIntelligenceReadinessArea,
    TwinPlanningIntelligenceReadinessItem,
    TwinPlanningIntelligenceReadinessScope,
    TwinPlanningIntelligenceReadinessView,
    TwinPlanningChangeImpactHint,
    TwinPlanningContext,
    TwinPlanningContextRecord,
    TwinPlanningContextSection,
    TwinPlanningDependencyAwareness,
    TwinPlanningDependencyAwarenessLabel,
    TwinPlanningDependencyHook,
    TwinPlanningDependencyWarning,
    TwinPlanningPermissionReadiness,
    TwinPlanningProvenanceGap,
    TwinPlanningProvenanceGapType,
    TwinPlanningRecordClassification,
    TwinPermissionConsentArtifactPlaceholder,
    TwinPermissionHomeownerAuthorityMetadata,
    TwinPermissionReadinessAudience,
    TwinPermissionReadinessAudienceConcept,
    TwinPermissionReadinessDuration,
    TwinPermissionReadinessDurationConcept,
    TwinPermissionReadinessPurpose,
    TwinPermissionReadinessPurposeConcept,
    TwinPermissionReadinessRevocationConcept,
    TwinPermissionReadinessRevocationState,
    TwinRuntimeContributionIdentity,
    TwinRuntimeParticipant,
    TwinRuntimeParticipantRole,
    TwinRuntimeProjectionRecord,
    TwinRuntimeProjectionView,
    TwinRuntimeViewContext,
    TwinRuntimeVisibilityScope,
    TwinTopologyDeferredLifecycleDomain,
    TwinTopologyEdge,
    TwinTopologyMissingRelationshipIndicator,
    TwinTopologyLifecycleReadinessHint,
    TwinTopologyLifecycleReadinessSummary,
    TwinTopologyLifecycleDomain,
    TwinTopologyMissingReadinessIndicator,
    TwinTopologyNode,
    TwinTopologyRelationshipCoverageSummary,
    TwinTopologySnapshot,
    TwinViewPermissionAlignmentMetadata,
)


PLACEHOLDER_FIELDS = {
    "upfront_cost_placeholder",
    "estimated_monthly_savings_placeholder",
    "future_expansion_score",
    "install_complexity_score",
    "backup_capability_score",
    "resilience_score",
    "unit_cost_placeholder",
    "total_cost_placeholder",
}

IMPORTANT_PROVENANCE_FIELDS = {
    "home": {
        "name",
        "address_line_1",
        "city",
        "state",
        "postal_code",
        "utility_provider",
        "service_size",
    },
    "building": {"name", "type", "approximate_distance_from_main_service"},
    "electrical_panel": {
        "panel_type",
        "amperage",
        "busbar_rating",
        "breaker_spaces_total",
        "breaker_spaces_available",
        "indoor_outdoor",
    },
    "load": {
        "name",
        "category",
        "running_watts",
        "surge_watts",
        "estimated_daily_hours",
        "backup_priority",
        "phase_type",
    },
    "equipment_location": {"name", "location_type", "approximate_coordinates"},
    "equipment_product": {"manufacturer", "model", "product_type", "ecosystem", "specs", "documentation_url"},
    "energy_system_design": {"name", "design_goal", "architecture_type", "status"},
    "design_equipment": {"product_id", "quantity", "location_id", "role_in_system"},
    "estimated_pathway": {
        "name",
        "source_location",
        "destination_location",
        "estimated_distance_ft",
        "route_type",
        "route_difficulty",
        "visibility_level",
        "confidence_level",
        "upfront_cost_placeholder",
        "estimated_monthly_savings_placeholder",
        "resilience_score",
    },
    "scenario": {
        "name",
        "description",
        "linked_design_id",
        "upfront_cost_placeholder",
        "future_expansion_score",
        "install_complexity_score",
        "backup_capability_score",
    },
    "scenario_revision": {
        "revision_status",
        "linked_design_id",
        "design_goal_snapshot",
        "design_status_snapshot",
        "recommended_profile_snapshot",
        "planning_summary",
        "planning_state_snapshot",
    },
}

PROVENANCE_GAP_LIMITATIONS = [
    "Provenance gaps describe source visibility only; they do not prove a value is incorrect.",
    "Provenance visibility does not imply field verification, safety approval, utility approval, or engineering approval.",
]

DEPENDENCY_AWARENESS_LIMITATIONS = [
    "Dependency awareness labels are descriptive runtime metadata only.",
    "Labels do not run recalculation, schedule work, persist stale state, verify facts, or create approval authority.",
]

CHANGE_IMPACT_HINT_LIMITATIONS = [
    "Change-impact hints are descriptive planning metadata only.",
    "Hints do not run recalculation, invalidate records, persist stale state, verify facts, or create approval authority.",
]

PLANNING_DEPENDENCY_WARNING_LIMITATIONS = [
    "Planning dependency warnings describe relationship uncertainty only.",
    "Warnings do not prove a dependency is wrong, complete, field-verified, approved, or operational.",
]

TOPOLOGY_SNAPSHOT_LIMITATIONS = [
    "Topology snapshot is descriptive runtime metadata derived from the current Twin Planning Context only.",
    "No topology graph is persisted, promoted, field-verified, recalculated, invalidated, simulated, exported, or approved.",
    "Lifecycle labels are planning context only and do not create installation, engineering, utility, safety, or operational authority.",
]

TOPOLOGY_READINESS_LIMITATIONS = [
    "Lifecycle readiness metadata is descriptive and read-only.",
    "Readiness hints do not create lifecycle workflows, topology promotion, event logs, simulation, or Phase 3 intelligence.",
]

TOPOLOGY_RELATIONSHIP_COVERAGE_LIMITATIONS = [
    "Topology relationship coverage is descriptive and read-only.",
    "Relationship coverage does not create a graph engine, lifecycle workflow, promotion engine, event log, recalculation, invalidation, simulation, what-if analysis, or Phase 3 intelligence.",
    "Relationship coverage uses existing planning-context records only and does not infer installed, verified, utility-reviewed, contractual, or operational topology.",
]

DEPENDENCY_IMPACT_READINESS_LIMITATIONS = [
    "Phase 3A dependency impact readiness explains existing structure, dependencies, limitations, confidence, and missing information only.",
    "Every derived statement is reproducible from the listed TwinPlanningContext and topology snapshot basis.",
    "This view does not recommend, optimize, simulate, rank, choose, authorize, recalculate, invalidate, export, enforce permissions, or operate devices.",
    "The Twin may interpret recorded and derived planning facts, but it may not invent facts.",
]

DEPENDENCY_IMPACT_DEFERRED_CAPABILITIES = [
    "scenario_intelligence",
    "impact_propagation_engine",
    "recalculation_engine",
    "invalidation_engine",
    "optimization",
    "upgrade_ranking",
    "economic_reasoning",
    "utility_readiness_reasoning",
    "survivability_modeling",
    "recharge_modeling",
    "compatibility_engines",
    "simulation",
    "what_if_analysis",
    "auth",
    "rbac_abac",
    "permission_enforcement",
    "exports",
    "utility_sharing",
    "telemetry_governance",
    "ownership_transfer",
    "registry",
    "marketplace",
    "operational_control",
]

DEPENDENCY_REASONING_LIMITATIONS = [
    "Phase 3B dependency reasoning explains existing dependency meaning only.",
    "Every reasoning statement is reproducible from the listed TwinPlanningContext, topology snapshot, and dependency impact readiness basis.",
    "This view does not propagate impacts, mark stale state, recalculate, invalidate, compare scenarios, recommend, optimize, simulate, rank, choose, authorize, export, enforce permissions, or operate devices.",
    "The Twin may classify existing dependency meaning, but it may not invent facts or create new topology relationships.",
]

DEPENDENCY_REASONING_DEFERRED_CAPABILITIES = [
    "scenario_intelligence",
    "impact_propagation_engine",
    "stale_state_persistence",
    "recalculation_engine",
    "invalidation_engine",
    "optimization",
    "upgrade_ranking",
    "economic_reasoning",
    "utility_readiness_reasoning",
    "survivability_modeling",
    "recharge_modeling",
    "compatibility_engines",
    "simulation",
    "what_if_analysis",
    "auth",
    "rbac_abac",
    "permission_enforcement",
    "exports",
    "utility_sharing",
    "telemetry_governance",
    "ownership_transfer",
    "registry",
    "marketplace",
    "operational_control",
    "twin_id",
    "graph_database",
    "graph_engine",
    "migrations",
    "canonical_twin_runtime_model",
    "recommendation_actions",
]

PLANNING_INTELLIGENCE_READINESS_LIMITATIONS = [
    "Phase 3C planning intelligence readiness is a readiness inventory only.",
    "Areas marked ready are ready for read-only explanation only.",
    "Areas marked blocked/deferred are not implemented and must not be treated as available intelligence.",
    "Provenance presence is not verification, and permission readiness is not permission enforcement.",
    "This view does not recommend, rank, optimize, simulate, compare scenarios, generate proposals, export data, enforce permissions, operate devices, or create canonical Twin runtime state.",
]

PLANNING_INTELLIGENCE_READINESS_DEFERRED_BOUNDARIES = [
    "scenario_intelligence",
    "impact_propagation",
    "stale_state_persistence",
    "recalculation",
    "invalidation",
    "simulation",
    "what_if_analysis",
    "optimization",
    "ranking",
    "recommendations",
    "economic_reasoning",
    "utility_readiness",
    "survivability_recharge_modeling",
    "compatibility_engines",
    "proposal_generation",
    "exports",
    "auth",
    "rbac_abac",
    "permission_enforcement",
    "marketplace",
    "operational_behavior",
    "twin_id",
    "graph_engine",
    "migrations",
    "canonical_twin_runtime_model",
]

TOPOLOGY_RELATIONSHIP_COVERAGE_RULE_KEY = "twin_topology.relationship_coverage_v1"

TOPOLOGY_RELATIONSHIP_FAMILY_BY_RELATIONSHIP = {
    "structure_belongs_to_premise_planning_context": "structure_premise_placement",
    "panel_assigned_to_building_planning_context": "panel_building_placement",
    "load_assigned_to_building_planning_context": "load_building_placement",
    "location_assigned_to_building_planning_context": "location_building_placement",
    "design_includes_pathway_planning_context": "design_pathway_reference",
    "pathway_source_location_planning_context": "pathway_endpoint_reference",
    "pathway_destination_location_planning_context": "pathway_endpoint_reference",
}

DEFERRED_TOPOLOGY_LIFECYCLE_DOMAINS = [
    (
        "contractor_reviewed_topology",
        "Contractor-reviewed topology remains deferred because no approved contractor review workflow or authority boundary exists.",
        ["contractor view contract", "source-linked review artifact", "future approved lifecycle transition"],
    ),
    (
        "contractual_topology",
        "Contractual topology remains deferred because no approved proposal, contract, or commitment state is modeled.",
        ["contract authority boundary", "source-linked contract artifact", "future approved lifecycle transition"],
    ),
    (
        "field_verified_topology",
        "Field-verified topology remains deferred because no inspection, photo, commissioning, or professional verification workflow exists.",
        ["field verification source", "verification authority boundary", "future approved lifecycle transition"],
    ),
    (
        "utility_reviewed_topology",
        "Utility-reviewed topology remains deferred because no utility-safe view, export, interconnection authority, or utility approval workflow exists.",
        ["permissioned utility-safe view", "utility source evidence", "future approved lifecycle transition"],
    ),
    (
        "operational_topology",
        "Operational topology remains deferred because no telemetry, device identity, command authority, dispatch, DERMS, or control boundary exists.",
        ["telemetry governance", "device identity", "operational-control isolation"],
    ),
    (
        "future_expansion_or_replacement_topology",
        "Expansion and replacement topology remains deferred beyond saved planning scenarios because no decommissioning, replacement, or upgrade lifecycle model exists.",
        ["lifecycle history model", "source-linked replacement artifact", "future approved lifecycle transition"],
    ),
]

TOPOLOGY_MISSING_READINESS_INDICATORS = [
    (
        "field_verification_readiness",
        "field-verified",
        "Topology snapshot limitations explicitly state that topology is not field-verified.",
    ),
    (
        "promotion_workflow_readiness",
        "promoted",
        "Topology snapshot limitations explicitly state that topology is not promoted.",
    ),
    (
        "lifecycle_event_log_readiness",
        "lifecycle event log",
        "Snapshot implementation boundary and limitations state that no lifecycle event log exists.",
    ),
    (
        "simulation_readiness",
        "simulated",
        "Topology snapshot limitations explicitly state that topology is not simulated.",
    ),
    (
        "operational_topology_readiness",
        "operational",
        "Topology snapshot limitations state that lifecycle labels do not create operational authority.",
    ),
]

DEFERRED_PERMISSION_CAPABILITIES = [
    "permission_grants",
    "consent_artifacts",
    "revocation_workflow",
    "rbac_abac",
    "auth",
    "tenant_isolation",
    "scoped_exports",
    "exchange",
    "ownership_transfer",
    "registry",
    "identity",
    "utility_control",
    "operational_control",
]

PERMISSION_READINESS_LIMITATIONS = [
    "Permission readiness metadata is descriptive only and does not enforce access.",
    "Endpoint access, account scaffolding, UI visibility, or AI use is not a permission grant.",
    "External sharing requires a future approved permission model before it can be treated as authorized.",
]

PERMISSION_FOUNDATION_LIMITATIONS = [
    "Permission foundation fields are readiness metadata only.",
    "No active permission grant, active consent, authorization check, export authorization, or enforcement behavior exists.",
]

REGROUNDING_GAP_TYPES = {
    TwinPlanningProvenanceGapType.missing_source.value,
    TwinPlanningProvenanceGapType.partial_source.value,
    TwinPlanningProvenanceGapType.placeholder_without_source.value,
    TwinPlanningProvenanceGapType.unknown_origin.value,
}

LOAD_PANEL_DEPENDENCY_RULE_KEY = "twin_dependency.load_panel_shared_building_v1"
EQUIPMENT_SYSTEM_DEPENDENCY_RULE_KEY = "twin_dependency.equipment_system_reference_v1"
SCENARIO_REFERENCE_DEPENDENCY_RULE_KEY = "twin_dependency.scenario_reference_v1"

REVIEW_LIMITATION_MARKERS = (
    "not NEC compliance",
    "not field-verified",
    "not final electrical design",
    "not surveyed",
    "not full advisor replay",
    "not verified",
    "planning only",
    "planning context",
)

AI_GROUNDING_FIELD_ALLOWLIST = {
    "home": {"id", "name", "state", "country", "utility_provider", "service_size", "data_origin"},
    "building": {
        "id",
        "home_id",
        "name",
        "type",
        "approximate_distance_from_main_service",
        "data_origin",
    },
    "electrical_panel": {
        "id",
        "home_id",
        "building_id",
        "panel_type",
        "amperage",
        "busbar_rating",
        "breaker_spaces_total",
        "breaker_spaces_available",
        "indoor_outdoor",
        "data_origin",
    },
    "load": {
        "id",
        "home_id",
        "building_id",
        "name",
        "category",
        "running_watts",
        "surge_watts",
        "estimated_daily_hours",
        "backup_priority",
        "phase_type",
        "data_origin",
    },
    "equipment_location": {
        "id",
        "home_id",
        "building_id",
        "name",
        "location_type",
        "approximate_coordinates",
        "data_origin",
    },
    "equipment_product": {
        "id",
        "manufacturer",
        "model",
        "product_type",
        "ecosystem",
        "specs",
        "documentation_url",
        "data_origin",
    },
    "energy_system_design": {
        "id",
        "home_id",
        "name",
        "design_goal",
        "architecture_type",
        "status",
        "data_origin",
    },
    "design_equipment": {
        "id",
        "design_id",
        "product_id",
        "quantity",
        "location_id",
        "role_in_system",
        "data_origin",
    },
    "estimated_pathway": {
        "id",
        "home_id",
        "design_id",
        "name",
        "lifecycle_stage",
        "source_location",
        "destination_location",
        "estimated_distance_ft",
        "route_type",
        "route_difficulty",
        "visibility_level",
        "confidence_level",
        "upfront_cost_placeholder",
        "estimated_monthly_savings_placeholder",
        "resilience_score",
        "data_origin",
    },
    "scenario": {
        "id",
        "home_id",
        "name",
        "linked_design_id",
        "upfront_cost_placeholder",
        "future_expansion_score",
        "install_complexity_score",
        "backup_capability_score",
        "data_origin",
    },
    "scenario_revision": {
        "id",
        "scenario_id",
        "parent_revision_id",
        "revision_number",
        "revision_label",
        "revision_status",
        "linked_design_id",
        "design_goal_snapshot",
        "design_status_snapshot",
        "recommended_profile_snapshot",
        "planning_state_snapshot",
        "data_origin",
    },
    "advisor_recommendation_summary": {
        "design_id",
        "recommended_profile",
        "confidence_level",
        "context_signals",
        "basis",
        "scope_note",
        "reasoning_graph_scope",
    },
    "advisor_note": {"design_id", "advisor_note"},
}

AI_GROUNDING_BASE_SECTION_KEYS = {
    "premise",
    "structures",
    "electrical_infrastructure",
    "loads",
}

RUNTIME_VIEW_SECTION_ALLOWLIST = {
    TwinRuntimeParticipantRole.homeowner: {
        "premise",
        "structures",
        "electrical_infrastructure",
        "loads",
        "equipment_locations",
        "equipment_products",
        "designs",
        "design_equipment",
        "pathways",
        "scenarios",
        "scenario_revisions",
        "derived_intelligence",
    },
    TwinRuntimeParticipantRole.contractor: {
        "premise",
        "structures",
        "electrical_infrastructure",
        "loads",
        "equipment_locations",
        "equipment_products",
        "designs",
        "design_equipment",
        "pathways",
        "derived_intelligence",
    },
    TwinRuntimeParticipantRole.internal_system: {
        "premise",
        "structures",
        "electrical_infrastructure",
        "loads",
        "equipment_locations",
        "equipment_products",
        "designs",
        "design_equipment",
        "pathways",
        "scenarios",
        "scenario_revisions",
        "derived_intelligence",
        "unknowns",
    },
}

RUNTIME_VIEW_SCOPE = {
    TwinRuntimeParticipantRole.homeowner: TwinRuntimeVisibilityScope.owner_private,
    TwinRuntimeParticipantRole.contractor: TwinRuntimeVisibilityScope.contractor_scoped,
    TwinRuntimeParticipantRole.internal_system: TwinRuntimeVisibilityScope.internal_governance,
}

TOPOLOGY_SNAPSHOT_SECTION_ALLOWLIST = {
    "premise",
    "structures",
    "electrical_infrastructure",
    "loads",
    "equipment_locations",
    "equipment_products",
    "designs",
    "design_equipment",
    "pathways",
    "scenarios",
    "scenario_revisions",
    "derived_intelligence",
}

RUNTIME_VIEW_PURPOSE = {
    TwinRuntimeParticipantRole.homeowner: "owner_planning_context",
    TwinRuntimeParticipantRole.contractor: "contractor_scoping_context",
    TwinRuntimeParticipantRole.internal_system: "runtime_governance_review",
}

PERMISSION_AUDIENCE_READINESS_MAP = {
    "homeowner_planning": TwinPermissionReadinessAudience.homeowner,
    "homeowner": TwinPermissionReadinessAudience.homeowner,
    "contractor": TwinPermissionReadinessAudience.contractor,
    "ai": TwinPermissionReadinessAudience.ai,
    "internal_governance": TwinPermissionReadinessAudience.internal_system,
    "internal_system": TwinPermissionReadinessAudience.internal_system,
}

PERMISSION_PURPOSE_READINESS_MAP = {
    "owner_planning_context": TwinPermissionReadinessPurpose.owner_planning_context,
    "contractor_scoping_context": TwinPermissionReadinessPurpose.contractor_scoping_context,
    "grounded_design_recommendation": TwinPermissionReadinessPurpose.ai_grounding,
    "runtime_governance_review": TwinPermissionReadinessPurpose.runtime_governance_review,
    "missing_context_review": TwinPermissionReadinessPurpose.missing_context_review,
}

RUNTIME_FIELD_ALLOWLIST = {
    TwinRuntimeParticipantRole.contractor: {
        "home": {"id", "name", "city", "state", "country", "utility_provider", "service_size", "data_origin"},
        "building": {
            "id",
            "home_id",
            "name",
            "type",
            "approximate_distance_from_main_service",
            "data_origin",
        },
        "electrical_panel": {
            "id",
            "home_id",
            "building_id",
            "panel_type",
            "amperage",
            "busbar_rating",
            "breaker_spaces_total",
            "breaker_spaces_available",
            "indoor_outdoor",
            "data_origin",
        },
        "load": {
            "id",
            "home_id",
            "building_id",
            "name",
            "category",
            "running_watts",
            "surge_watts",
            "estimated_daily_hours",
            "backup_priority",
            "phase_type",
            "data_origin",
        },
        "equipment_location": {
            "id",
            "home_id",
            "building_id",
            "name",
            "location_type",
            "approximate_coordinates",
            "data_origin",
        },
        "equipment_product": {
            "id",
            "manufacturer",
            "model",
            "product_type",
            "ecosystem",
            "specs",
            "documentation_url",
            "data_origin",
        },
        "energy_system_design": {
            "id",
            "home_id",
            "name",
            "design_goal",
            "architecture_type",
            "status",
            "data_origin",
        },
        "design_equipment": {
            "id",
            "design_id",
            "product_id",
            "quantity",
            "location_id",
            "role_in_system",
            "data_origin",
        },
        "estimated_pathway": {
            "id",
            "home_id",
            "design_id",
            "name",
            "lifecycle_stage",
            "source_location",
            "destination_location",
            "estimated_distance_ft",
            "route_type",
            "route_difficulty",
            "visibility_level",
            "confidence_level",
            "data_origin",
        },
        "advisor_recommendation_summary": {
            "design_id",
            "recommended_profile",
            "confidence_level",
            "context_signals",
            "basis",
            "scope_note",
            "reasoning_graph_scope",
        },
    },
}


class TwinPlanningContextService:
    def _record_snapshot(self, record, fields: Iterable[str]) -> Dict[str, object]:
        return {field: getattr(record, field, None) for field in fields}

    def _origin_value(self, data_origin: Optional[str]) -> Optional[str]:
        return data_origin.value if hasattr(data_origin, "value") else data_origin

    def _entity_summary(self, db, entity_type: str, entity_id: Optional[str]) -> Optional[ProvenanceSummary]:
        if not entity_id:
            return None
        return provenance_service.summarize_entity(db, entity_type, entity_id)

    def _data_provenance_records(self, db, entity_type: str, entity_id: Optional[str]) -> List[object]:
        if not entity_id:
            return []
        return repository.list_data_provenance(db, entity_type=entity_type, entity_id=entity_id)

    def _has_provenance(self, summary: Optional[ProvenanceSummary]) -> bool:
        if summary is None:
            return False
        return bool(summary.source_types or summary.source_document_ids or summary.trust_states)

    def _placeholder_fields(self, record_snapshot: Dict[str, object]) -> List[str]:
        return sorted(
            field
            for field, value in record_snapshot.items()
            if field in PLACEHOLDER_FIELDS and value is not None
        )

    def _gap(
        self,
        *,
        gap_type: TwinPlanningProvenanceGapType,
        entity_type: str,
        entity_id: Optional[str],
        reason: str,
        field_name: Optional[str] = None,
        severity: str = "warning",
    ) -> TwinPlanningProvenanceGap:
        return TwinPlanningProvenanceGap(
            gap_type=gap_type,
            entity_type=entity_type,
            entity_id=entity_id,
            field_name=field_name,
            severity=severity,
            reason=reason,
            limitations=PROVENANCE_GAP_LIMITATIONS,
        )

    def _dependency_hook(
        self,
        *,
        source_entity_type: str,
        source_entity_id: Optional[str],
        target_entity_type: str,
        target_entity_id: Optional[str],
        relationship: str,
        rule_key: str,
        note: str,
        confidence_level: str = "planning_context",
    ) -> TwinPlanningDependencyHook:
        return TwinPlanningDependencyHook(
            source_entity_type=source_entity_type,
            source_entity_id=source_entity_id,
            target_entity_type=target_entity_type,
            target_entity_id=target_entity_id,
            relationship=relationship,
            rule_keys=[rule_key],
            confidence_level=confidence_level,
            note=note,
        )

    def _change_impact_hint(
        self,
        *,
        source_entity_type: str,
        source_entity_id: Optional[str],
        impacted_entity_type: str,
        impacted_entity_id: Optional[str],
        relationship: str,
        rule_key: str,
        reason: str,
    ) -> TwinPlanningChangeImpactHint:
        return TwinPlanningChangeImpactHint(
            source_entity_type=source_entity_type,
            source_entity_id=source_entity_id,
            impacted_entity_type=impacted_entity_type,
            impacted_entity_id=impacted_entity_id,
            relationship=relationship,
            rule_keys=[rule_key],
            reason=reason,
            limitations=CHANGE_IMPACT_HINT_LIMITATIONS,
        )

    def _planning_dependency_warning(
        self,
        *,
        warning_type: str,
        entity_type: str,
        entity_id: Optional[str],
        reason: str,
        related_entity_type: Optional[str] = None,
        related_entity_id: Optional[str] = None,
        rule_key: Optional[str] = None,
        severity: str = "info",
    ) -> TwinPlanningDependencyWarning:
        return TwinPlanningDependencyWarning(
            warning_type=warning_type,
            entity_type=entity_type,
            entity_id=entity_id,
            related_entity_type=related_entity_type,
            related_entity_id=related_entity_id,
            severity=severity,
            reason=reason,
            rule_keys=[rule_key] if rule_key else [],
            limitations=PLANNING_DEPENDENCY_WARNING_LIMITATIONS,
        )

    def _sourced_fields(self, provenance_records: List[object]) -> set:
        return {
            record.field_name
            for record in provenance_records
            if getattr(record, "field_name", None)
        }

    def _important_fields(self, entity_type: str, record_snapshot: Dict[str, object]) -> List[str]:
        configured_fields = IMPORTANT_PROVENANCE_FIELDS.get(entity_type, set())
        return sorted(
            field
            for field in configured_fields
            if field in record_snapshot and record_snapshot.get(field) is not None
        )

    def _derived_output_gaps(
        self,
        *,
        entity_type: str,
        entity_id: Optional[str],
        rule_keys: Optional[List[str]],
        dependency_hooks: Optional[List[TwinPlanningDependencyHook]],
        source_document_ids: Optional[List[str]],
    ) -> List[TwinPlanningProvenanceGap]:
        if rule_keys or source_document_ids:
            return []
        return [
            self._gap(
                gap_type=TwinPlanningProvenanceGapType.derived_without_lineage,
                entity_type=entity_type,
                entity_id=entity_id,
                reason=(
                    "Derived or advisory output has no persisted rule key or source document lineage in this context."
                ),
            )
        ]

    def _provenance_gaps_for_record(
        self,
        *,
        entity_type: str,
        entity_id: Optional[str],
        record_snapshot: Dict[str, object],
        data_origin: Optional[str],
        classification: TwinPlanningRecordClassification,
        provenance_records: List[object],
        source_document_ids: List[str],
        rule_keys: Optional[List[str]] = None,
        dependency_hooks: Optional[List[TwinPlanningDependencyHook]] = None,
    ) -> List[TwinPlanningProvenanceGap]:
        gaps: List[TwinPlanningProvenanceGap] = []
        sourced_fields = self._sourced_fields(provenance_records)
        important_fields = self._important_fields(entity_type, record_snapshot)
        unsourced_important_fields = [field for field in important_fields if field not in sourced_fields]
        placeholder_fields = self._placeholder_fields(record_snapshot)
        origin_value = self._origin_value(data_origin)

        if not sourced_fields and important_fields:
            gaps.append(
                self._gap(
                    gap_type=TwinPlanningProvenanceGapType.missing_source,
                    entity_type=entity_type,
                    entity_id=entity_id,
                    reason=(
                        "No field-level source record is linked for important planning fields: "
                        f"{', '.join(important_fields)}."
                    ),
                )
            )
        elif sourced_fields and unsourced_important_fields:
            gaps.append(
                self._gap(
                    gap_type=TwinPlanningProvenanceGapType.partial_source,
                    entity_type=entity_type,
                    entity_id=entity_id,
                    reason=(
                        "Some field-level provenance exists, but important planning fields remain unsourced: "
                        f"{', '.join(unsourced_important_fields)}."
                    ),
                )
            )

        for field in placeholder_fields:
            if field not in sourced_fields:
                gaps.append(
                    self._gap(
                        gap_type=TwinPlanningProvenanceGapType.placeholder_without_source,
                        entity_type=entity_type,
                        entity_id=entity_id,
                        field_name=field,
                        reason=f"Placeholder-bearing field '{field}' has no field-level source record.",
                    )
                )

        if not sourced_fields and not source_document_ids:
            gaps.append(
                self._gap(
                    gap_type=TwinPlanningProvenanceGapType.unknown_origin,
                    entity_type=entity_type,
                    entity_id=entity_id,
                    severity="info",
                    reason=(
                        f"Persisted data_origin is '{origin_value or 'unknown'}', but no source record identifies "
                        "the document, entry, import, or rule basis for this entity."
                    ),
                )
            )

        if classification in {
            TwinPlanningRecordClassification.derived_output,
            TwinPlanningRecordClassification.advisory_output,
        }:
            gaps.extend(
                self._derived_output_gaps(
                    entity_type=entity_type,
                    entity_id=entity_id,
                    rule_keys=rule_keys,
                    dependency_hooks=dependency_hooks,
                    source_document_ids=source_document_ids,
                )
            )

        return gaps

    def _dependency_awareness(
        self,
        *,
        label: TwinPlanningDependencyAwarenessLabel,
        record: TwinPlanningContextRecord,
        reason: str,
        source_gap_types: Optional[List[str]] = None,
    ) -> TwinPlanningDependencyAwareness:
        return TwinPlanningDependencyAwareness(
            label=label,
            entity_type=record.entity_type,
            entity_id=record.entity_id,
            reason=reason,
            rule_keys=record.rule_keys,
            source_gap_types=source_gap_types or [],
            limitations=DEPENDENCY_AWARENESS_LIMITATIONS,
        )

    def _dependency_awareness_for_record(
        self, section_key: str, record: TwinPlanningContextRecord
    ) -> List[TwinPlanningDependencyAwareness]:
        items: List[TwinPlanningDependencyAwareness] = []
        source_gap_types = sorted({gap.gap_type.value for gap in record.provenance_gaps})
        regrounding_gap_types = sorted(set(source_gap_types).intersection(REGROUNDING_GAP_TYPES))
        limitation_text = " ".join(record.limitations).lower()

        if section_key == "scenario_revisions":
            items.append(
                self._dependency_awareness(
                    label=TwinPlanningDependencyAwarenessLabel.snapshot_bound,
                    record=record,
                    reason="Scenario revisions are saved historical planning snapshots, not live current-state outputs.",
                )
            )
            items.append(
                self._dependency_awareness(
                    label=TwinPlanningDependencyAwarenessLabel.needs_recalculation,
                    record=record,
                    reason=(
                        "Snapshot-bound revision data would need recalculation before reuse as current planning intelligence."
                    ),
                )
            )

        if regrounding_gap_types:
            items.append(
                self._dependency_awareness(
                    label=TwinPlanningDependencyAwarenessLabel.needs_regrounding,
                    record=record,
                    reason=(
                        "Source or provenance posture is missing, partial, placeholder-backed, or unknown."
                    ),
                    source_gap_types=regrounding_gap_types,
                )
            )

        if record.classification in {
            TwinPlanningRecordClassification.derived_output,
            TwinPlanningRecordClassification.advisory_output,
        }:
            derived_gap_types = [
                gap_type for gap_type in source_gap_types if gap_type == TwinPlanningProvenanceGapType.derived_without_lineage.value
            ]
            if derived_gap_types:
                items.append(
                    self._dependency_awareness(
                        label=TwinPlanningDependencyAwarenessLabel.stale_unknown,
                        record=record,
                        reason=(
                            "Runtime cannot determine freshness because full derived-output lineage is not available."
                        ),
                        source_gap_types=derived_gap_types,
                    )
                )
            if record.dependency_hooks or record.rule_keys:
                items.append(
                    self._dependency_awareness(
                        label=TwinPlanningDependencyAwarenessLabel.current,
                        record=record,
                        reason=(
                            "Derived or advisory output was regenerated during this request from current planner records."
                        ),
                    )
                )

        if record.classification == TwinPlanningRecordClassification.unknown:
            items.append(
                self._dependency_awareness(
                    label=TwinPlanningDependencyAwarenessLabel.stale_unknown,
                    record=record,
                    reason="Unknown marker has no independent dependency basis or freshness signal.",
                    source_gap_types=source_gap_types,
                )
            )

        if record.entity_type == "advisor_note":
            items.append(
                self._dependency_awareness(
                    label=TwinPlanningDependencyAwarenessLabel.needs_review,
                    record=record,
                    reason="Advisory text should be reviewed against structured facts before reuse.",
                )
            )

        if any(marker in limitation_text for marker in REVIEW_LIMITATION_MARKERS):
            items.append(
                self._dependency_awareness(
                    label=TwinPlanningDependencyAwarenessLabel.needs_review,
                    record=record,
                    reason=(
                        "Planning-only limitations indicate this record needs review before stronger claims are made."
                    ),
                )
            )

        if not items:
            items.append(
                self._dependency_awareness(
                    label=TwinPlanningDependencyAwarenessLabel.current,
                    record=record,
                    reason=(
                        "Record is included in the current read-only planning context; this does not imply verification."
                    ),
                )
            )

        deduped = {}
        for item in items:
            key = (item.label.value, item.reason, tuple(item.source_gap_types))
            deduped.setdefault(key, item)
        return list(deduped.values())

    def _dependency_awareness_summary(self, records: List[object]) -> Dict[str, int]:
        counts = Counter(
            item.label.value
            for record in records
            for item in getattr(record, "dependency_awareness", [])
        )
        return {
            label.value: counts.get(label.value, 0)
            for label in TwinPlanningDependencyAwarenessLabel
        }

    def _attach_dependency_awareness(self, sections: List[TwinPlanningContextSection]):
        for section in sections:
            for record in section.records:
                record.dependency_awareness = self._dependency_awareness_for_record(section.section_key, record)
            section.dependency_awareness_summary = self._dependency_awareness_summary(section.records)

    def _permission_readiness(
        self,
        *,
        permission_required: bool,
        audience: str,
        purpose: str,
        minimum_necessary: bool,
        visibility_limitations: Optional[List[str]] = None,
        view_name: str = "twin_planning_context",
        visibility_scope: Optional[TwinRuntimeVisibilityScope] = None,
    ) -> TwinPlanningPermissionReadiness:
        audience_readiness = PERMISSION_AUDIENCE_READINESS_MAP.get(
            audience,
            TwinPermissionReadinessAudience.homeowner,
        )
        fallback_purpose = TwinPermissionReadinessPurpose.owner_planning_context
        if audience_readiness == TwinPermissionReadinessAudience.contractor:
            fallback_purpose = TwinPermissionReadinessPurpose.contractor_scoping_context
        elif audience_readiness == TwinPermissionReadinessAudience.ai:
            fallback_purpose = TwinPermissionReadinessPurpose.ai_grounding
        elif audience_readiness == TwinPermissionReadinessAudience.internal_system:
            fallback_purpose = TwinPermissionReadinessPurpose.runtime_governance_review
        purpose_readiness = PERMISSION_PURPOSE_READINESS_MAP.get(purpose, fallback_purpose)
        foundation_limitations = PERMISSION_FOUNDATION_LIMITATIONS + [
            "No permission grant id, consent artifact id, revocation event, auth principal, role mapping, or export package is created.",
        ]
        return TwinPlanningPermissionReadiness(
            permission_required=permission_required,
            permission_not_enforced=True,
            audience=audience,
            purpose=purpose,
            minimum_necessary=minimum_necessary,
            audience_readiness=TwinPermissionReadinessAudienceConcept(
                audience=audience_readiness,
                reason=(
                    "Audience is labeled for future permission-scoping readiness only; it is not an authenticated "
                    "principal, account role, grant recipient, or authorization subject."
                ),
                limitations=foundation_limitations,
            ),
            purpose_readiness=TwinPermissionReadinessPurposeConcept(
                purpose=purpose_readiness,
                reason=(
                    "Purpose is labeled for future permission-scoping readiness only; it does not authorize access, "
                    "sharing, export, or operational behavior."
                ),
                limitations=foundation_limitations,
            ),
            duration_readiness=TwinPermissionReadinessDurationConcept(
                duration=TwinPermissionReadinessDuration.not_active_placeholder,
                reason=(
                    "No active permission duration exists because no permission grant or consent artifact has been created."
                ),
                limitations=foundation_limitations,
            ),
            revocation_state_readiness=TwinPermissionReadinessRevocationConcept(
                revocation_state=TwinPermissionReadinessRevocationState.not_applicable_no_active_permission,
                reason=(
                    "No revocation state exists because there is no active grant, consent artifact, or enforced access."
                ),
                limitations=foundation_limitations,
            ),
            consent_artifact_placeholder=TwinPermissionConsentArtifactPlaceholder(
                reason=(
                    "Consent artifact is a placeholder concept only; no active consent text, consent version, or consent "
                    "record is captured by this runtime foundation."
                ),
                limitations=foundation_limitations,
            ),
            homeowner_authority=TwinPermissionHomeownerAuthorityMetadata(
                authority_note=(
                    "Homeowner authority over future external sharing is preserved; this metadata does not delegate, "
                    "transfer, or enforce that authority."
                ),
                limitations=foundation_limitations,
            ),
            view_permission_alignment=TwinViewPermissionAlignmentMetadata(
                view_name=view_name,
                audience=audience_readiness,
                purpose=purpose_readiness,
                visibility_scope=visibility_scope,
                limitations=foundation_limitations,
            ),
            visibility_limitations=PERMISSION_READINESS_LIMITATIONS + (visibility_limitations or []),
            deferred_capabilities=DEFERRED_PERMISSION_CAPABILITIES,
        )

    def _context_permission_readiness(self) -> TwinPlanningPermissionReadiness:
        return self._permission_readiness(
            permission_required=False,
            audience="homeowner_planning",
            purpose="owner_planning_context",
            minimum_necessary=False,
            view_name="twin_planning_context",
            visibility_scope=TwinRuntimeVisibilityScope.owner_private,
            visibility_limitations=[
                "Broad owner planning context is not minimized for external participants.",
                "External sharing would require future explicit permission, scope, purpose, duration, and revocation handling.",
            ],
        )

    def _section_permission_readiness(self, section_key: str) -> TwinPlanningPermissionReadiness:
        if section_key == "unknowns":
            return self._permission_readiness(
                permission_required=True,
                audience="internal_governance",
                purpose="missing_context_review",
                minimum_necessary=True,
                view_name=f"section:{section_key}",
                visibility_scope=TwinRuntimeVisibilityScope.internal_governance,
                visibility_limitations=[
                    "Unknown markers are internal governance context and should not be exposed as facts.",
                ],
            )
        return self._permission_readiness(
            permission_required=True,
            audience="homeowner_planning",
            purpose=f"{section_key}_planning_context",
            minimum_necessary=False,
            view_name=f"section:{section_key}",
            visibility_scope=TwinRuntimeVisibilityScope.owner_private,
            visibility_limitations=[
                "Section data may contain homeowner planning context and requires future permission before external sharing.",
            ],
        )

    def _record_permission_readiness(
        self, section_key: str, record: TwinPlanningContextRecord
    ) -> TwinPlanningPermissionReadiness:
        audience = "internal_governance" if section_key == "unknowns" else "homeowner_planning"
        purpose = "missing_context_review" if section_key == "unknowns" else f"{record.entity_type}_planning_context"
        limitations = [
            "Record visibility metadata does not authorize access or sharing.",
            "Future permission scope may need field-level or derived-output-level limits.",
        ]
        if record.classification in {
            TwinPlanningRecordClassification.derived_output,
            TwinPlanningRecordClassification.advisory_output,
        }:
            limitations.append("Derived and advisory outputs require explicit future view-purpose limits before sharing.")
        if record.source_document_ids:
            limitations.append("Source-document visibility may be narrower than fact visibility in a future permission model.")
        return self._permission_readiness(
            permission_required=True,
            audience=audience,
            purpose=purpose,
            minimum_necessary=False,
            view_name=f"record:{record.entity_type}",
            visibility_scope=(
                TwinRuntimeVisibilityScope.internal_governance
                if section_key == "unknowns"
                else TwinRuntimeVisibilityScope.owner_private
            ),
            visibility_limitations=limitations,
        )

    def _attach_permission_readiness(self, sections: List[TwinPlanningContextSection]):
        for section in sections:
            section.permission_readiness = self._section_permission_readiness(section.section_key)
            for record in section.records:
                record.permission_readiness = self._record_permission_readiness(section.section_key, record)

    def _ai_view_permission_readiness(self) -> TwinPlanningPermissionReadiness:
        return self._permission_readiness(
            permission_required=True,
            audience="ai",
            purpose="grounded_design_recommendation",
            minimum_necessary=True,
            view_name="ai_design_grounding",
            visibility_scope=TwinRuntimeVisibilityScope.ai_grounding,
            visibility_limitations=[
                "AI grounding view is minimized for explanation and recommendation grounding only.",
                "AI access is not consent, export authorization, write authority, or permission enforcement.",
                "AI may not create canonical facts, permission grants, verification claims, or approval claims.",
            ],
        )

    def _ai_record_permission_readiness(self, record: TwinPlanningContextRecord) -> TwinPlanningPermissionReadiness:
        return self._permission_readiness(
            permission_required=True,
            audience="ai",
            purpose=f"{record.entity_type}_grounding",
            minimum_necessary=True,
            view_name=f"ai_design_grounding:{record.entity_type}",
            visibility_scope=TwinRuntimeVisibilityScope.ai_grounding,
            visibility_limitations=[
                "Record is included only because it is part of the minimized AI grounding projection.",
                "Visibility metadata does not authorize external sharing or persistence outside the approved runtime.",
            ],
        )

    def _classify_record(
        self,
        *,
        record_snapshot: Dict[str, object],
        data_origin: Optional[str],
        provenance_summary: Optional[ProvenanceSummary],
        default_classification: TwinPlanningRecordClassification = TwinPlanningRecordClassification.recorded_fact,
    ) -> TwinPlanningRecordClassification:
        placeholder_fields = self._placeholder_fields(record_snapshot)
        if data_origin == DataOrigin.placeholder.value or placeholder_fields:
            return TwinPlanningRecordClassification.placeholder
        if data_origin == DataOrigin.derived_estimate.value:
            return TwinPlanningRecordClassification.derived_output
        if self._has_provenance(provenance_summary):
            return TwinPlanningRecordClassification.source_backed_fact
        return default_classification

    def _classification_reasons(
        self,
        *,
        classification: TwinPlanningRecordClassification,
        data_origin: Optional[str],
        provenance_summary: Optional[ProvenanceSummary],
        placeholder_fields: List[str],
        extra_reasons: Optional[List[str]] = None,
    ) -> List[str]:
        reasons = list(extra_reasons or [])
        if data_origin:
            reasons.append(f"Persisted data_origin is '{data_origin}'.")
        if classification == TwinPlanningRecordClassification.source_backed_fact:
            reasons.append("A provenance summary links this record to source or lineage metadata.")
        if placeholder_fields:
            reasons.append(f"Placeholder-bearing fields are present: {', '.join(placeholder_fields)}.")
        if not self._has_provenance(provenance_summary):
            reasons.append("No field-level provenance summary is currently linked for this entity.")
        if data_origin == DataOrigin.demo_seed.value:
            reasons.append("Demo seed records are useful for continuity but are not factual authority.")
        return reasons

    def _record(
        self,
        *,
        db,
        entity_type: str,
        entity_id: Optional[str],
        label: str,
        record_snapshot: Dict[str, object],
        data_origin: Optional[str],
        authority_layer: AuthorityLayer = AuthorityLayer.canonical,
        default_classification: TwinPlanningRecordClassification = TwinPlanningRecordClassification.recorded_fact,
        provenance_entity_type: Optional[str] = None,
        rule_keys: Optional[List[str]] = None,
        dependency_hooks: Optional[List[TwinPlanningDependencyHook]] = None,
        change_impact_hints: Optional[List[TwinPlanningChangeImpactHint]] = None,
        planning_dependency_warnings: Optional[List[TwinPlanningDependencyWarning]] = None,
        extra_reasons: Optional[List[str]] = None,
        limitations: Optional[List[str]] = None,
    ) -> TwinPlanningContextRecord:
        provenance_type = provenance_entity_type or entity_type
        summary = self._entity_summary(db, provenance_type, entity_id)
        provenance_records = self._data_provenance_records(db, provenance_type, entity_id)
        placeholder_fields = self._placeholder_fields(record_snapshot)
        classification = self._classify_record(
            record_snapshot=record_snapshot,
            data_origin=data_origin,
            provenance_summary=summary,
            default_classification=default_classification,
        )
        source_document_ids = summary.source_document_ids if summary else []
        record_rule_keys = rule_keys or []
        record_dependency_hooks = dependency_hooks or []
        record_change_impact_hints = change_impact_hints or []
        record_planning_dependency_warnings = planning_dependency_warnings or []
        return TwinPlanningContextRecord(
            entity_type=entity_type,
            entity_id=entity_id,
            label=label,
            classification=classification,
            authority_layer=authority_layer,
            data_origin=data_origin,
            record=record_snapshot,
            provenance_summary=summary,
            source_document_ids=source_document_ids,
            rule_keys=record_rule_keys,
            dependency_hooks=record_dependency_hooks,
            classification_reasons=self._classification_reasons(
                classification=classification,
                data_origin=data_origin,
                provenance_summary=summary,
                placeholder_fields=placeholder_fields,
                extra_reasons=extra_reasons,
            ),
            missing_fields=placeholder_fields + (summary.unverified_fields if summary else []),
            provenance_gaps=self._provenance_gaps_for_record(
                entity_type=entity_type,
                entity_id=entity_id,
                record_snapshot=record_snapshot,
                data_origin=data_origin,
                classification=classification,
                provenance_records=provenance_records,
                source_document_ids=source_document_ids,
                rule_keys=record_rule_keys,
                dependency_hooks=record_dependency_hooks,
            ),
            change_impact_hints=record_change_impact_hints,
            planning_dependency_warnings=record_planning_dependency_warnings,
            limitations=limitations or [],
        )

    def _unknown_record(self, entity_type: str, entity_id: str, label: str, reason: str) -> TwinPlanningContextRecord:
        return TwinPlanningContextRecord(
            entity_type=entity_type,
            entity_id=entity_id,
            label=label,
            classification=TwinPlanningRecordClassification.unknown,
            authority_layer=AuthorityLayer.advisory,
            data_classification=DataClassification.internal_governance,
            record={},
            classification_reasons=[reason],
            provenance_gaps=[
                self._gap(
                    gap_type=TwinPlanningProvenanceGapType.unknown_origin,
                    entity_type=entity_type,
                    entity_id=entity_id,
                    severity="info",
                    reason="This unknown marker has no independent source; it reflects a missing planning-context gap.",
                )
            ],
            limitations=[
                "Unknown markers identify missing planning context; they are not inferred facts.",
            ],
        )

    def _advisor_record(
        self,
        *,
        design_id: str,
        recommendation: ResilienceRecommendation,
        dependency_hooks: List[TwinPlanningDependencyHook],
    ) -> TwinPlanningContextRecord:
        recommended_profile = recommendation.recommended_profile.value if recommendation.recommended_profile else None
        rule_keys = []
        if recommendation.provenance_summary:
            rule_keys = recommendation.provenance_summary.get("rule_keys", [])
        return TwinPlanningContextRecord(
            entity_type="advisor_recommendation_summary",
            entity_id=f"advisor-summary-{design_id}",
            label=f"Advisor recommendation summary for {design_id}",
            classification=TwinPlanningRecordClassification.derived_output,
            authority_layer=AuthorityLayer.derived,
            data_origin=DataOrigin.derived_estimate,
            record={
                "design_id": design_id,
                "recommended_profile": recommended_profile,
                "confidence_level": recommendation.confidence_level.value,
                "context_signals": recommendation.context_signals,
                "basis": recommendation.basis,
                "scope_note": recommendation.scope_note,
                "reasoning_graph_scope": recommendation.reasoning_graph.scope_label
                if recommendation.reasoning_graph
                else None,
            },
            rule_keys=rule_keys,
            dependency_hooks=dependency_hooks,
            classification_reasons=[
                "Advisor recommendation summary is derived from deterministic rules over recorded planning records.",
            ],
            missing_fields=[],
            provenance_gaps=self._derived_output_gaps(
                entity_type="advisor_recommendation_summary",
                entity_id=f"advisor-summary-{design_id}",
                rule_keys=rule_keys,
                dependency_hooks=dependency_hooks,
                source_document_ids=[],
            ),
            limitations=[
                "Advisor outputs are planning intelligence only and do not create canonical Twin facts.",
                "Advisor outputs are regenerated from current records; they are not a persisted full replay snapshot.",
            ],
        )

    def _advisor_note_record(self, design_id: str, advisor_note: str) -> TwinPlanningContextRecord:
        return TwinPlanningContextRecord(
            entity_type="advisor_note",
            entity_id=f"advisor-note-{design_id}",
            label=f"Advisor note for {design_id}",
            classification=TwinPlanningRecordClassification.advisory_output,
            authority_layer=AuthorityLayer.advisory,
            data_origin=DataOrigin.derived_estimate,
            record={"design_id": design_id, "advisor_note": advisor_note},
            classification_reasons=[
                "Advisor note is explanatory text over structured records and deterministic outputs.",
            ],
            provenance_gaps=self._derived_output_gaps(
                entity_type="advisor_note",
                entity_id=f"advisor-note-{design_id}",
                rule_keys=[],
                dependency_hooks=[],
                source_document_ids=[],
            ),
            limitations=[
                "Advisory text cannot create canonical facts, permission grants, engineering approval, or utility authority.",
            ],
        )

    def _dependency_hooks_from_recommendation(
        self, design_id: str, recommendation: ResilienceRecommendation
    ) -> List[TwinPlanningDependencyHook]:
        graph = recommendation.reasoning_graph
        if graph is None:
            return []
        return [
            TwinPlanningDependencyHook(
                source_entity_type=dependency.source_node_id,
                source_entity_id=None,
                target_entity_type=dependency.target_node_id,
                target_entity_id=None,
                relationship=dependency.relationship,
                rule_keys=dependency.rule_keys,
                confidence_level=dependency.confidence_level.value,
                note=f"Design {design_id}: {dependency.summary}",
            )
            for dependency in graph.dependencies
        ]

    def _load_panel_dependency_metadata(
        self, load, panels_by_building: Dict[str, List[object]]
    ):
        related_panels = panels_by_building.get(load.building_id, [])
        hooks = [
            self._dependency_hook(
                source_entity_type="load",
                source_entity_id=load.id,
                target_entity_type="electrical_panel",
                target_entity_id=panel.id,
                relationship="shared_building_id_planning_context",
                rule_key=LOAD_PANEL_DEPENDENCY_RULE_KEY,
                confidence_level="planning_context_only",
                note=(
                    f"Load {load.id} and panel {panel.id} share building_id {load.building_id}; "
                    "this is planning context only and does not identify circuit membership."
                ),
            )
            for panel in related_panels
        ]
        hints = [
            self._change_impact_hint(
                source_entity_type="electrical_panel",
                source_entity_id=panel.id,
                impacted_entity_type="load",
                impacted_entity_id=load.id,
                relationship="shared_building_id_planning_context",
                rule_key=LOAD_PANEL_DEPENDENCY_RULE_KEY,
                reason=(
                    "Panel or service-capacity changes for the same building may affect how this load is interpreted "
                    "in planning outputs."
                ),
            )
            for panel in related_panels
        ]
        warnings = []
        if related_panels:
            warnings.append(
                self._planning_dependency_warning(
                    warning_type="load_panel_relationship_is_building_level_only",
                    entity_type="load",
                    entity_id=load.id,
                    related_entity_type="electrical_panel",
                    related_entity_id=related_panels[0].id,
                    rule_key=LOAD_PANEL_DEPENDENCY_RULE_KEY,
                    reason=(
                        "The load-to-panel relationship is inferred only from shared building_id planning context; "
                        "it is not a verified circuit, breaker, or panelboard assignment."
                    ),
                )
            )
        else:
            warnings.append(
                self._planning_dependency_warning(
                    warning_type="load_has_no_same_building_panel",
                    entity_type="load",
                    entity_id=load.id,
                    rule_key=LOAD_PANEL_DEPENDENCY_RULE_KEY,
                    severity="warning",
                    reason=(
                        "No electrical panel record shares this load's building_id, so panel/service impact context "
                        "for this load is incomplete."
                    ),
                )
            )
        return hooks, hints, warnings

    def _panel_load_dependency_metadata(
        self, panel, loads_by_building: Dict[str, List[object]]
    ):
        related_loads = loads_by_building.get(panel.building_id, [])
        hints = [
            self._change_impact_hint(
                source_entity_type="load",
                source_entity_id=load.id,
                impacted_entity_type="electrical_panel",
                impacted_entity_id=panel.id,
                relationship="shared_building_id_planning_context",
                rule_key=LOAD_PANEL_DEPENDENCY_RULE_KEY,
                reason=(
                    "Recorded load changes for the same building may affect panel/service planning interpretation."
                ),
            )
            for load in related_loads
        ]
        warnings = []
        if related_loads:
            warnings.append(
                self._planning_dependency_warning(
                    warning_type="panel_load_relationship_is_building_level_only",
                    entity_type="electrical_panel",
                    entity_id=panel.id,
                    related_entity_type="load",
                    related_entity_id=related_loads[0].id,
                    rule_key=LOAD_PANEL_DEPENDENCY_RULE_KEY,
                    reason=(
                        "Panel-to-load impact is based on shared building_id only; it does not identify a verified "
                        "served-load, circuit, breaker, or subpanel relationship."
                    ),
                )
            )
        return [], hints, warnings

    def _design_equipment_dependency_metadata(
        self,
        equipment,
        designs_by_id: Dict[str, object],
        products_by_id: Dict[str, object],
        locations_by_id: Dict[str, object],
    ):
        hooks = []
        hints = []
        warnings = []

        if equipment.design_id in designs_by_id:
            hooks.append(
                self._dependency_hook(
                    source_entity_type="design_equipment",
                    source_entity_id=equipment.id,
                    target_entity_type="energy_system_design",
                    target_entity_id=equipment.design_id,
                    relationship="assigned_to_design_planning_context",
                    rule_key=EQUIPMENT_SYSTEM_DEPENDENCY_RULE_KEY,
                    note=(
                        f"Design equipment {equipment.id} is part of design {equipment.design_id} in the "
                        "current planning composition."
                    ),
                )
            )
            hints.append(
                self._change_impact_hint(
                    source_entity_type="energy_system_design",
                    source_entity_id=equipment.design_id,
                    impacted_entity_type="design_equipment",
                    impacted_entity_id=equipment.id,
                    relationship="assigned_to_design_planning_context",
                    rule_key=EQUIPMENT_SYSTEM_DEPENDENCY_RULE_KEY,
                    reason="Design goal or status changes may affect how this equipment assignment is interpreted.",
                )
            )
        else:
            warnings.append(
                self._planning_dependency_warning(
                    warning_type="design_equipment_missing_design_reference",
                    entity_type="design_equipment",
                    entity_id=equipment.id,
                    related_entity_type="energy_system_design",
                    related_entity_id=equipment.design_id,
                    rule_key=EQUIPMENT_SYSTEM_DEPENDENCY_RULE_KEY,
                    severity="warning",
                    reason="This equipment assignment references a design that is not present in the home planning context.",
                )
            )

        if equipment.product_id in products_by_id:
            hooks.append(
                self._dependency_hook(
                    source_entity_type="design_equipment",
                    source_entity_id=equipment.id,
                    target_entity_type="equipment_product",
                    target_entity_id=equipment.product_id,
                    relationship="uses_product_reference",
                    rule_key=EQUIPMENT_SYSTEM_DEPENDENCY_RULE_KEY,
                    note=(
                        f"Design equipment {equipment.id} references product {equipment.product_id}; product data "
                        "is planning reference data, not a procurement or compatibility guarantee."
                    ),
                )
            )
            hints.append(
                self._change_impact_hint(
                    source_entity_type="equipment_product",
                    source_entity_id=equipment.product_id,
                    impacted_entity_type="design_equipment",
                    impacted_entity_id=equipment.id,
                    relationship="uses_product_reference",
                    rule_key=EQUIPMENT_SYSTEM_DEPENDENCY_RULE_KEY,
                    reason="Product data changes may affect equipment composition, compatibility, and planning notes.",
                )
            )
        else:
            warnings.append(
                self._planning_dependency_warning(
                    warning_type="design_equipment_missing_product_reference",
                    entity_type="design_equipment",
                    entity_id=equipment.id,
                    related_entity_type="equipment_product",
                    related_entity_id=equipment.product_id,
                    rule_key=EQUIPMENT_SYSTEM_DEPENDENCY_RULE_KEY,
                    severity="warning",
                    reason="This equipment assignment references product data that is not present in the runtime context.",
                )
            )

        if equipment.location_id:
            if equipment.location_id in locations_by_id:
                hooks.append(
                    self._dependency_hook(
                        source_entity_type="design_equipment",
                        source_entity_id=equipment.id,
                        target_entity_type="equipment_location",
                        target_entity_id=equipment.location_id,
                        relationship="assigned_location_planning_context",
                        rule_key=EQUIPMENT_SYSTEM_DEPENDENCY_RULE_KEY,
                        note=(
                            f"Design equipment {equipment.id} references location {equipment.location_id}; "
                            "location is planning/siting context only."
                        ),
                    )
                )
                hints.append(
                    self._change_impact_hint(
                        source_entity_type="equipment_location",
                        source_entity_id=equipment.location_id,
                        impacted_entity_type="design_equipment",
                        impacted_entity_id=equipment.id,
                        relationship="assigned_location_planning_context",
                        rule_key=EQUIPMENT_SYSTEM_DEPENDENCY_RULE_KEY,
                        reason="Location changes may affect siting, pathway, and design-equipment planning interpretation.",
                    )
                )
                warnings.append(
                    self._planning_dependency_warning(
                        warning_type="equipment_location_is_planning_only",
                        entity_type="design_equipment",
                        entity_id=equipment.id,
                        related_entity_type="equipment_location",
                        related_entity_id=equipment.location_id,
                        rule_key=EQUIPMENT_SYSTEM_DEPENDENCY_RULE_KEY,
                        reason="Equipment location references are planning/siting context and are not field-verified placement.",
                    )
                )
            else:
                warnings.append(
                    self._planning_dependency_warning(
                        warning_type="design_equipment_missing_location_reference",
                        entity_type="design_equipment",
                        entity_id=equipment.id,
                        related_entity_type="equipment_location",
                        related_entity_id=equipment.location_id,
                        rule_key=EQUIPMENT_SYSTEM_DEPENDENCY_RULE_KEY,
                        severity="warning",
                        reason="This equipment assignment references a location that is not present in the home planning context.",
                    )
                )
        else:
            warnings.append(
                self._planning_dependency_warning(
                    warning_type="design_equipment_location_unassigned",
                    entity_type="design_equipment",
                    entity_id=equipment.id,
                    rule_key=EQUIPMENT_SYSTEM_DEPENDENCY_RULE_KEY,
                    reason="No equipment location is assigned, so siting and pathway dependency context is incomplete.",
                )
            )

        return hooks, hints, warnings

    def _scenario_dependency_metadata(self, scenario, designs_by_id: Dict[str, object]):
        hooks = []
        hints = []
        warnings = [
            self._planning_dependency_warning(
                warning_type="scenario_reference_is_not_live_invalidation",
                entity_type="scenario",
                entity_id=scenario.id,
                related_entity_type="energy_system_design",
                related_entity_id=scenario.linked_design_id,
                rule_key=SCENARIO_REFERENCE_DEPENDENCY_RULE_KEY,
                reason=(
                    "Scenario-to-design references are planning dependencies only; design changes do not create "
                    "automatic invalidation, recalculation, or approval state."
                ),
            )
        ]
        if scenario.linked_design_id in designs_by_id:
            hooks.append(
                self._dependency_hook(
                    source_entity_type="scenario",
                    source_entity_id=scenario.id,
                    target_entity_type="energy_system_design",
                    target_entity_id=scenario.linked_design_id,
                    relationship="linked_design_planning_context",
                    rule_key=SCENARIO_REFERENCE_DEPENDENCY_RULE_KEY,
                    note=f"Scenario {scenario.id} references design {scenario.linked_design_id}.",
                )
            )
            hints.append(
                self._change_impact_hint(
                    source_entity_type="energy_system_design",
                    source_entity_id=scenario.linked_design_id,
                    impacted_entity_type="scenario",
                    impacted_entity_id=scenario.id,
                    relationship="linked_design_planning_context",
                    rule_key=SCENARIO_REFERENCE_DEPENDENCY_RULE_KEY,
                    reason="Linked design changes may affect scenario comparison and planning interpretation.",
                )
            )
        else:
            warnings.append(
                self._planning_dependency_warning(
                    warning_type="scenario_missing_design_reference",
                    entity_type="scenario",
                    entity_id=scenario.id,
                    related_entity_type="energy_system_design",
                    related_entity_id=scenario.linked_design_id,
                    rule_key=SCENARIO_REFERENCE_DEPENDENCY_RULE_KEY,
                    severity="warning",
                    reason="This scenario references a design that is not present in the home planning context.",
                )
            )
        return hooks, hints, warnings

    def _scenario_revision_dependency_metadata(
        self,
        revision,
        scenarios_by_id: Dict[str, object],
        designs_by_id: Dict[str, object],
    ):
        hooks = []
        hints = []
        warnings = [
            self._planning_dependency_warning(
                warning_type="revision_snapshot_is_not_live_replay",
                entity_type="scenario_revision",
                entity_id=revision.id,
                related_entity_type="scenario",
                related_entity_id=revision.scenario_id,
                rule_key=SCENARIO_REFERENCE_DEPENDENCY_RULE_KEY,
                reason=(
                    "Scenario revisions are compact snapshots; current design or scenario changes do not automatically "
                    "replay, recalculate, invalidate, or approve this revision."
                ),
            )
        ]

        if revision.scenario_id in scenarios_by_id:
            hooks.append(
                self._dependency_hook(
                    source_entity_type="scenario_revision",
                    source_entity_id=revision.id,
                    target_entity_type="scenario",
                    target_entity_id=revision.scenario_id,
                    relationship="snapshot_of_scenario",
                    rule_key=SCENARIO_REFERENCE_DEPENDENCY_RULE_KEY,
                    note=f"Scenario revision {revision.id} snapshots scenario {revision.scenario_id}.",
                )
            )
            hints.append(
                self._change_impact_hint(
                    source_entity_type="scenario",
                    source_entity_id=revision.scenario_id,
                    impacted_entity_type="scenario_revision",
                    impacted_entity_id=revision.id,
                    relationship="snapshot_of_scenario",
                    rule_key=SCENARIO_REFERENCE_DEPENDENCY_RULE_KEY,
                    reason="Scenario changes may affect how this saved revision should be interpreted.",
                )
            )

        if revision.linked_design_id in designs_by_id:
            hooks.append(
                self._dependency_hook(
                    source_entity_type="scenario_revision",
                    source_entity_id=revision.id,
                    target_entity_type="energy_system_design",
                    target_entity_id=revision.linked_design_id,
                    relationship="snapshot_linked_design",
                    rule_key=SCENARIO_REFERENCE_DEPENDENCY_RULE_KEY,
                    note=f"Scenario revision {revision.id} preserves linked design {revision.linked_design_id}.",
                )
            )
            hints.append(
                self._change_impact_hint(
                    source_entity_type="energy_system_design",
                    source_entity_id=revision.linked_design_id,
                    impacted_entity_type="scenario_revision",
                    impacted_entity_id=revision.id,
                    relationship="snapshot_linked_design",
                    rule_key=SCENARIO_REFERENCE_DEPENDENCY_RULE_KEY,
                    reason="Linked design changes may affect whether this saved revision still matches current planning intent.",
                )
            )

        if revision.parent_revision_id:
            hooks.append(
                self._dependency_hook(
                    source_entity_type="scenario_revision",
                    source_entity_id=revision.id,
                    target_entity_type="scenario_revision",
                    target_entity_id=revision.parent_revision_id,
                    relationship="parent_revision_lineage",
                    rule_key=SCENARIO_REFERENCE_DEPENDENCY_RULE_KEY,
                    note=f"Scenario revision {revision.id} references parent revision {revision.parent_revision_id}.",
                )
            )
            hints.append(
                self._change_impact_hint(
                    source_entity_type="scenario_revision",
                    source_entity_id=revision.parent_revision_id,
                    impacted_entity_type="scenario_revision",
                    impacted_entity_id=revision.id,
                    relationship="parent_revision_lineage",
                    rule_key=SCENARIO_REFERENCE_DEPENDENCY_RULE_KEY,
                    reason="Parent revision lineage affects interpretation of saved revision drift.",
                )
            )

        return hooks, hints, warnings

    def _ai_grounding_fields(self, record: TwinPlanningContextRecord) -> Dict[str, object]:
        allowed_fields = AI_GROUNDING_FIELD_ALLOWLIST.get(record.entity_type, set())
        return {
            field: value
            for field, value in record.record.items()
            if field in allowed_fields
        }

    def _ai_grounding_related_ids(
        self, context: TwinPlanningContext, design_id: Optional[str]
    ) -> Dict[str, set]:
        related_ids = {
            "design_ids": set(),
            "product_ids": set(),
            "location_ids": set(),
            "scenario_ids": set(),
        }
        if not design_id:
            return related_ids

        related_ids["design_ids"].add(design_id)
        for section in context.sections:
            for record in section.records:
                if section.section_key == "design_equipment" and record.record.get("design_id") == design_id:
                    if record.record.get("product_id"):
                        related_ids["product_ids"].add(record.record["product_id"])
                    if record.record.get("location_id"):
                        related_ids["location_ids"].add(record.record["location_id"])
                if section.section_key == "scenarios" and record.record.get("linked_design_id") == design_id:
                    if record.entity_id:
                        related_ids["scenario_ids"].add(record.entity_id)
        return related_ids

    def _include_ai_grounding_record(
        self,
        *,
        section_key: str,
        record: TwinPlanningContextRecord,
        design_id: Optional[str],
        related_ids: Dict[str, set],
    ) -> bool:
        if section_key == "unknowns":
            return False
        if not design_id:
            return True
        if section_key in AI_GROUNDING_BASE_SECTION_KEYS:
            return True
        if section_key == "designs":
            return record.entity_id == design_id
        if section_key == "design_equipment":
            return record.record.get("design_id") == design_id
        if section_key == "equipment_products":
            return record.entity_id in related_ids["product_ids"]
        if section_key == "equipment_locations":
            return record.entity_id in related_ids["location_ids"]
        if section_key == "pathways":
            return record.record.get("design_id") == design_id
        if section_key == "scenarios":
            return record.record.get("linked_design_id") == design_id
        if section_key == "scenario_revisions":
            return (
                record.record.get("linked_design_id") == design_id
                or record.record.get("scenario_id") in related_ids["scenario_ids"]
            )
        if section_key == "derived_intelligence":
            return record.record.get("design_id") == design_id
        return False

    def _ai_grounding_record(
        self, section_key: str, record: TwinPlanningContextRecord
    ) -> AIDesignGroundingRecord:
        return AIDesignGroundingRecord(
            section_key=section_key,
            entity_type=record.entity_type,
            entity_id=record.entity_id,
            label=record.label,
            classification=record.classification,
            authority_layer=record.authority_layer,
            data_classification=record.data_classification,
            data_origin=record.data_origin,
            fields=self._ai_grounding_fields(record),
            provenance_summary=record.provenance_summary,
            source_document_ids=record.source_document_ids,
            rule_keys=record.rule_keys,
            dependency_hooks=record.dependency_hooks,
            missing_fields=record.missing_fields,
            provenance_gaps=record.provenance_gaps,
            dependency_awareness=record.dependency_awareness,
            change_impact_hints=record.change_impact_hints,
            planning_dependency_warnings=record.planning_dependency_warnings,
            permission_readiness=self._ai_record_permission_readiness(record),
            limitations=record.limitations,
        )

    def _topology_node_id(self, entity_type: str, entity_id: Optional[str]) -> str:
        return f"{entity_type}:{entity_id or 'unknown'}"

    def _topology_lifecycle_domain(
        self, section_key: str, record: TwinPlanningContextRecord
    ) -> TwinTopologyLifecycleDomain:
        if section_key == "scenario_revisions":
            return TwinTopologyLifecycleDomain.saved_scenario_revision_topology
        if section_key in {"designs", "design_equipment", "pathways", "scenarios"}:
            return TwinTopologyLifecycleDomain.sandbox_proposed_planning_topology
        if (
            section_key == "derived_intelligence"
            or record.classification
            in {
                TwinPlanningRecordClassification.derived_output,
                TwinPlanningRecordClassification.advisory_output,
            }
        ):
            return TwinTopologyLifecycleDomain.derived_advisory_topology
        return TwinTopologyLifecycleDomain.recorded_current_topology

    def _topology_node(
        self, section_key: str, record: TwinPlanningContextRecord
    ) -> TwinTopologyNode:
        permission_not_enforced = True
        if record.permission_readiness is not None:
            permission_not_enforced = record.permission_readiness.permission_not_enforced
        return TwinTopologyNode(
            node_id=self._topology_node_id(record.entity_type, record.entity_id),
            section_key=section_key,
            entity_type=record.entity_type,
            entity_id=record.entity_id,
            label=record.label,
            lifecycle_domain=self._topology_lifecycle_domain(section_key, record),
            classification=record.classification,
            authority_layer=record.authority_layer,
            data_classification=record.data_classification,
            data_origin=record.data_origin,
            source_document_ids=record.source_document_ids,
            rule_keys=record.rule_keys,
            provenance_gap_types=sorted({gap.gap_type.value for gap in record.provenance_gaps}),
            dependency_awareness_labels=sorted({item.label.value for item in record.dependency_awareness}),
            permission_not_enforced=permission_not_enforced,
            limitations=record.limitations + TOPOLOGY_SNAPSHOT_LIMITATIONS,
        )

    def _topology_edge_lifecycle_domain(
        self, source_node: TwinTopologyNode, target_node: TwinTopologyNode
    ) -> TwinTopologyLifecycleDomain:
        domains = {source_node.lifecycle_domain, target_node.lifecycle_domain}
        if TwinTopologyLifecycleDomain.saved_scenario_revision_topology in domains:
            return TwinTopologyLifecycleDomain.saved_scenario_revision_topology
        if TwinTopologyLifecycleDomain.sandbox_proposed_planning_topology in domains:
            return TwinTopologyLifecycleDomain.sandbox_proposed_planning_topology
        if TwinTopologyLifecycleDomain.derived_advisory_topology in domains:
            return TwinTopologyLifecycleDomain.derived_advisory_topology
        return TwinTopologyLifecycleDomain.recorded_current_topology

    def _topology_edge_from_nodes(
        self,
        *,
        source_node: TwinTopologyNode,
        target_node: TwinTopologyNode,
        relationship: str,
        note: str,
        rule_keys: Optional[List[str]] = None,
        confidence_level: Optional[str] = "medium",
        limitations: Optional[List[str]] = None,
    ) -> TwinTopologyEdge:
        return TwinTopologyEdge(
            edge_id=(
                f"topology-edge:{source_node.node_id}->{target_node.node_id}:"
                f"{relationship}"
            ),
            source_node_id=source_node.node_id,
            target_node_id=target_node.node_id,
            source_entity_type=source_node.entity_type,
            source_entity_id=source_node.entity_id,
            target_entity_type=target_node.entity_type,
            target_entity_id=target_node.entity_id,
            relationship=relationship,
            lifecycle_domain=self._topology_edge_lifecycle_domain(source_node, target_node),
            rule_keys=rule_keys or [TOPOLOGY_RELATIONSHIP_COVERAGE_RULE_KEY],
            confidence_level=confidence_level,
            note=note,
            limitations=limitations or (
                TOPOLOGY_RELATIONSHIP_COVERAGE_LIMITATIONS + TOPOLOGY_SNAPSHOT_LIMITATIONS
            ),
        )

    def _topology_edge_key(self, edge: TwinTopologyEdge) -> tuple:
        return (
            edge.source_node_id,
            edge.target_node_id,
            edge.relationship,
            tuple(edge.rule_keys),
        )

    def _sorted_topology_edges(self, edges: Dict[tuple, TwinTopologyEdge]) -> List[TwinTopologyEdge]:
        return sorted(
            edges.values(),
            key=lambda edge: (
                edge.source_node_id,
                edge.target_node_id,
                edge.relationship,
            ),
        )

    def _topology_edges(
        self,
        records: List[TwinPlanningContextRecord],
        node_map: Dict[tuple, TwinTopologyNode],
    ) -> List[TwinTopologyEdge]:
        edges = {}
        for record in records:
            for hook in record.dependency_hooks:
                source_key = (hook.source_entity_type, hook.source_entity_id)
                target_key = (hook.target_entity_type, hook.target_entity_id)
                source_node = node_map.get(source_key)
                target_node = node_map.get(target_key)
                if source_node is None or target_node is None:
                    continue
                edge_key = (
                    source_node.node_id,
                    target_node.node_id,
                    hook.relationship,
                    tuple(hook.rule_keys),
                )
                edges.setdefault(
                    edge_key,
                    self._topology_edge_from_nodes(
                        source_node=source_node,
                        target_node=target_node,
                        relationship=hook.relationship,
                        rule_keys=hook.rule_keys,
                        confidence_level=hook.confidence_level,
                        note=hook.note,
                        limitations=TOPOLOGY_SNAPSHOT_LIMITATIONS,
                    ),
                )
        return self._sorted_topology_edges(edges)

    def _topology_deduped_edges(self, edge_sets: List[List[TwinTopologyEdge]]) -> List[TwinTopologyEdge]:
        edges = {}
        for edge_set in edge_sets:
            for edge in edge_set:
                edges.setdefault(self._topology_edge_key(edge), edge)
        return self._sorted_topology_edges(edges)

    def _topology_record_map(
        self, section_records: List[tuple]
    ) -> Dict[tuple, TwinPlanningContextRecord]:
        return {
            (record.entity_type, record.entity_id): record
            for _, record in section_records
        }

    def _topology_resolution_key(self, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        normalized = str(value).strip().lower()
        return normalized or None

    def _topology_resolution_index(
        self,
        nodes: List[TwinTopologyNode],
        records_by_key: Dict[tuple, TwinPlanningContextRecord],
    ) -> Dict[str, Optional[TwinTopologyNode]]:
        candidates: Dict[str, Dict[str, TwinTopologyNode]] = {}

        def add_candidate(value: Optional[str], node: TwinTopologyNode):
            key = self._topology_resolution_key(value)
            if key is None:
                return
            candidates.setdefault(key, {})[node.node_id] = node

        for node in nodes:
            record = records_by_key.get((node.entity_type, node.entity_id))
            add_candidate(node.node_id, node)
            add_candidate(node.entity_id, node)
            add_candidate(node.label, node)
            if record is not None:
                add_candidate(record.record.get("name"), node)

        return {
            key: next(iter(value.values())) if len(value) == 1 else None
            for key, value in candidates.items()
        }

    def _resolve_topology_node(
        self,
        value: Optional[str],
        resolution_index: Dict[str, Optional[TwinTopologyNode]],
    ) -> Optional[TwinTopologyNode]:
        key = self._topology_resolution_key(value)
        if key is None:
            return None
        return resolution_index.get(key)

    def _missing_relationship_indicator(
        self,
        *,
        indicator: str,
        record: TwinPlanningContextRecord,
        field_name: Optional[str],
        attempted_value: Optional[str],
        relationship_family: str,
        reason: str,
        derived_from: Optional[List[str]] = None,
    ) -> TwinTopologyMissingRelationshipIndicator:
        return TwinTopologyMissingRelationshipIndicator(
            indicator=indicator,
            entity_type=record.entity_type,
            entity_id=record.entity_id,
            field_name=field_name,
            attempted_value=attempted_value,
            relationship_family=relationship_family,
            reason=reason,
            derived_from=derived_from or ["topology_record_fields", "topology_node_resolution_index"],
            limitations=TOPOLOGY_RELATIONSHIP_COVERAGE_LIMITATIONS + TOPOLOGY_SNAPSHOT_LIMITATIONS,
        )

    def _topology_relationship_coverage_edges(
        self,
        section_records: List[tuple],
        node_map: Dict[tuple, TwinTopologyNode],
    ) -> tuple:
        records_by_key = self._topology_record_map(section_records)
        resolution_index = self._topology_resolution_index(list(node_map.values()), records_by_key)
        relationship_edges: List[TwinTopologyEdge] = []
        missing_indicators: List[TwinTopologyMissingRelationshipIndicator] = []

        def append_edge(source_node, target_node, relationship, note):
            relationship_edges.append(
                self._topology_edge_from_nodes(
                    source_node=source_node,
                    target_node=target_node,
                    relationship=relationship,
                    note=note,
                )
            )

        for _, record in section_records:
            source_node = node_map.get((record.entity_type, record.entity_id))
            if source_node is None:
                continue

            if record.entity_type == "building":
                target_node = node_map.get(("home", record.record.get("home_id")))
                if target_node:
                    append_edge(
                        source_node,
                        target_node,
                        "structure_belongs_to_premise_planning_context",
                        "Structure-to-premise placement is derived from existing building.home_id planning data.",
                    )
                else:
                    missing_indicators.append(
                        self._missing_relationship_indicator(
                            indicator="structure_premise_relationship_unresolved",
                            record=record,
                            field_name="home_id",
                            attempted_value=record.record.get("home_id"),
                            relationship_family="structure_premise_placement",
                            reason="Building home_id did not resolve to a concrete home topology node.",
                        )
                    )

            if record.entity_type in {"electrical_panel", "load", "equipment_location"}:
                target_node = node_map.get(("building", record.record.get("building_id")))
                relationship_by_type = {
                    "electrical_panel": (
                        "panel_assigned_to_building_planning_context",
                        "panel_building_placement",
                        "Panel-to-building placement is derived from existing electrical_panel.building_id planning data.",
                    ),
                    "load": (
                        "load_assigned_to_building_planning_context",
                        "load_building_placement",
                        "Load-to-building placement is derived from existing load.building_id planning data.",
                    ),
                    "equipment_location": (
                        "location_assigned_to_building_planning_context",
                        "location_building_placement",
                        "Equipment-location-to-building placement is derived from existing equipment_location.building_id planning data.",
                    ),
                }
                relationship, family, note = relationship_by_type[record.entity_type]
                if target_node:
                    append_edge(source_node, target_node, relationship, note)
                else:
                    missing_indicators.append(
                        self._missing_relationship_indicator(
                            indicator=f"{family}_unresolved",
                            record=record,
                            field_name="building_id",
                            attempted_value=record.record.get("building_id"),
                            relationship_family=family,
                            reason=f"{record.entity_type}.building_id did not resolve to a concrete building topology node.",
                        )
                    )

            if record.entity_type == "estimated_pathway":
                pathway_node = source_node
                design_node = node_map.get(("energy_system_design", record.record.get("design_id")))
                if design_node:
                    append_edge(
                        design_node,
                        pathway_node,
                        "design_includes_pathway_planning_context",
                        "Design-to-pathway relationship is derived from existing estimated_pathway.design_id planning data.",
                    )
                else:
                    missing_indicators.append(
                        self._missing_relationship_indicator(
                            indicator="design_pathway_relationship_unresolved",
                            record=record,
                            field_name="design_id",
                            attempted_value=record.record.get("design_id"),
                            relationship_family="design_pathway_reference",
                            reason="Pathway design_id did not resolve to a concrete design topology node.",
                        )
                    )

                for field_name, relationship in [
                    ("source_location", "pathway_source_location_planning_context"),
                    ("destination_location", "pathway_destination_location_planning_context"),
                ]:
                    attempted_value = record.record.get(field_name)
                    target_node = self._resolve_topology_node(attempted_value, resolution_index)
                    if target_node:
                        append_edge(
                            pathway_node,
                            target_node,
                            relationship,
                            (
                                f"Pathway {field_name} relationship is derived from an existing "
                                "estimated_pathway field that resolves to a concrete topology node."
                            ),
                        )
                    else:
                        missing_indicators.append(
                            self._missing_relationship_indicator(
                                indicator=f"pathway_{field_name}_relationship_unresolved",
                                record=record,
                                field_name=field_name,
                                attempted_value=attempted_value,
                                relationship_family="pathway_endpoint_reference",
                                reason=(
                                    "Pathway endpoint value is absent, ambiguous, or a string label that does "
                                    "not resolve to a concrete topology node."
                                ),
                            )
                        )

        return self._topology_deduped_edges([relationship_edges]), missing_indicators

    def _topology_relationship_coverage_summary(
        self,
        dependency_edges: List[TwinTopologyEdge],
        relationship_edges: List[TwinTopologyEdge],
        missing_relationship_indicators: List[TwinTopologyMissingRelationshipIndicator],
    ) -> TwinTopologyRelationshipCoverageSummary:
        coverage_by_family = Counter()
        for edge in relationship_edges:
            family = TOPOLOGY_RELATIONSHIP_FAMILY_BY_RELATIONSHIP.get(
                edge.relationship,
                "other_relationship_coverage",
            )
            coverage_by_family[family] += 1
        unresolved_pathway_endpoint_count = sum(
            1
            for indicator in missing_relationship_indicators
            if indicator.relationship_family == "pathway_endpoint_reference"
        )
        return TwinTopologyRelationshipCoverageSummary(
            relationship_edge_count=len(relationship_edges),
            dependency_hook_edge_count=len(dependency_edges),
            coverage_by_relationship_family=dict(sorted(coverage_by_family.items())),
            missing_relationship_indicator_count=len(missing_relationship_indicators),
            unresolved_pathway_endpoint_count=unresolved_pathway_endpoint_count,
            limitations=TOPOLOGY_RELATIONSHIP_COVERAGE_LIMITATIONS + TOPOLOGY_SNAPSHOT_LIMITATIONS,
        )

    def _topology_scenario_branch_references(
        self,
        records: List[TwinPlanningContextRecord],
        node_map: Dict[tuple, TwinTopologyNode],
    ) -> List[Dict[str, object]]:
        references = []
        for record in records:
            if record.entity_type != "scenario":
                continue
            linked_design_id = record.record.get("linked_design_id")
            scenario_node = node_map.get(("scenario", record.entity_id))
            design_node = node_map.get(("energy_system_design", linked_design_id))
            references.append(
                {
                    "scenario_id": record.entity_id,
                    "linked_design_id": linked_design_id,
                    "scenario_node_id": scenario_node.node_id if scenario_node else None,
                    "linked_design_node_id": design_node.node_id if design_node else None,
                    "lifecycle_domain": TwinTopologyLifecycleDomain.sandbox_proposed_planning_topology.value,
                    "limitations": TOPOLOGY_SNAPSHOT_LIMITATIONS,
                }
            )
        return sorted(references, key=lambda item: item.get("scenario_id") or "")

    def _topology_revision_lineage_references(
        self,
        records: List[TwinPlanningContextRecord],
        node_map: Dict[tuple, TwinTopologyNode],
    ) -> List[Dict[str, object]]:
        references = []
        for record in records:
            if record.entity_type != "scenario_revision":
                continue
            scenario_id = record.record.get("scenario_id")
            linked_design_id = record.record.get("linked_design_id")
            parent_revision_id = record.record.get("parent_revision_id")
            revision_node = node_map.get(("scenario_revision", record.entity_id))
            scenario_node = node_map.get(("scenario", scenario_id))
            design_node = node_map.get(("energy_system_design", linked_design_id))
            parent_node = (
                node_map.get(("scenario_revision", parent_revision_id))
                if parent_revision_id
                else None
            )
            references.append(
                {
                    "revision_id": record.entity_id,
                    "scenario_id": scenario_id,
                    "linked_design_id": linked_design_id,
                    "parent_revision_id": parent_revision_id,
                    "revision_node_id": revision_node.node_id if revision_node else None,
                    "scenario_node_id": scenario_node.node_id if scenario_node else None,
                    "linked_design_node_id": design_node.node_id if design_node else None,
                    "parent_revision_node_id": parent_node.node_id if parent_node else None,
                    "lifecycle_domain": TwinTopologyLifecycleDomain.saved_scenario_revision_topology.value,
                    "limitations": TOPOLOGY_SNAPSHOT_LIMITATIONS,
                }
            )
        return sorted(references, key=lambda item: item.get("revision_id") or "")

    def _topology_readiness_status(
        self,
        nodes: List[TwinTopologyNode],
        provenance_gap_types: List[str],
        dependency_awareness_labels: List[str],
        planning_dependency_warning_types: List[str],
        source_document_count: int,
    ) -> str:
        if not nodes:
            return "not_represented_in_snapshot"
        dependency_limited_labels = {
            TwinPlanningDependencyAwarenessLabel.needs_recalculation.value,
            TwinPlanningDependencyAwarenessLabel.needs_regrounding.value,
            TwinPlanningDependencyAwarenessLabel.needs_review.value,
            TwinPlanningDependencyAwarenessLabel.stale_unknown.value,
        }
        has_dependency_limit = bool(planning_dependency_warning_types) or bool(
            dependency_limited_labels.intersection(dependency_awareness_labels)
        )
        if provenance_gap_types and has_dependency_limit:
            return "provenance_and_dependency_limited"
        if provenance_gap_types:
            return "provenance_limited"
        if has_dependency_limit:
            return "dependency_limited"
        if source_document_count == 0:
            return "source_limited"
        return "descriptive_planning_metadata_present"

    def _topology_lifecycle_readiness_hints(
        self,
        section_records: List[tuple],
        nodes: List[TwinTopologyNode],
        edges: List[TwinTopologyEdge],
    ) -> List[TwinTopologyLifecycleReadinessHint]:
        records_by_domain: Dict[TwinTopologyLifecycleDomain, List[TwinPlanningContextRecord]] = {
            domain: [] for domain in TwinTopologyLifecycleDomain
        }
        for section_key, record in section_records:
            records_by_domain[self._topology_lifecycle_domain(section_key, record)].append(record)

        nodes_by_domain: Dict[TwinTopologyLifecycleDomain, List[TwinTopologyNode]] = {
            domain: [] for domain in TwinTopologyLifecycleDomain
        }
        for node in nodes:
            nodes_by_domain[node.lifecycle_domain].append(node)

        edges_by_domain = Counter(edge.lifecycle_domain for edge in edges)
        readiness_hints = []
        for domain in TwinTopologyLifecycleDomain:
            domain_nodes = nodes_by_domain[domain]
            domain_records = records_by_domain[domain]
            provenance_gap_types = sorted(
                {
                    gap_type
                    for node in domain_nodes
                    for gap_type in node.provenance_gap_types
                }
            )
            dependency_awareness_labels = sorted(
                {
                    label
                    for node in domain_nodes
                    for label in node.dependency_awareness_labels
                }
            )
            warning_types = sorted(
                {
                    warning.warning_type
                    for record in domain_records
                    for warning in record.planning_dependency_warnings
                }
            )
            source_document_ids = {
                source_document_id
                for node in domain_nodes
                for source_document_id in node.source_document_ids
            }
            derived_from = ["topology_nodes", "topology_edges", "topology_snapshot_limitations"]
            if provenance_gap_types:
                derived_from.append("provenance_gap_types")
            if dependency_awareness_labels:
                derived_from.append("dependency_awareness_labels")
            if warning_types:
                derived_from.append("planning_dependency_warnings")
            if source_document_ids:
                derived_from.append("source_document_ids")

            hints = [
                (
                    f"{len(domain_nodes)} topology nodes and {edges_by_domain.get(domain, 0)} topology edges "
                    f"are represented for {domain.value}."
                ),
                "No lifecycle workflow, promotion workflow, event log, simulation, or operational authority is present.",
            ]
            if provenance_gap_types:
                hints.append(
                    "Readiness is limited by provenance gap types: "
                    + ", ".join(provenance_gap_types)
                    + "."
                )
            if warning_types:
                hints.append(
                    "Readiness is limited by planning dependency warnings: "
                    + ", ".join(warning_types)
                    + "."
                )
            if source_document_ids:
                hints.append(
                    f"{len(source_document_ids)} source document references are attached to nodes in this lifecycle domain."
                )
            elif domain_nodes:
                hints.append("No source document IDs are attached to nodes in this lifecycle domain.")

            readiness_hints.append(
                TwinTopologyLifecycleReadinessHint(
                    lifecycle_domain=domain,
                    readiness_status=self._topology_readiness_status(
                        domain_nodes,
                        provenance_gap_types,
                        dependency_awareness_labels,
                        warning_types,
                        len(source_document_ids),
                    ),
                    node_count=len(domain_nodes),
                    edge_count=edges_by_domain.get(domain, 0),
                    source_document_count=len(source_document_ids),
                    provenance_gap_types=provenance_gap_types,
                    dependency_awareness_labels=dependency_awareness_labels,
                    planning_dependency_warning_types=warning_types,
                    derived_from=derived_from,
                    hints=hints,
                    limitations=TOPOLOGY_READINESS_LIMITATIONS + TOPOLOGY_SNAPSHOT_LIMITATIONS,
                )
            )
        return readiness_hints

    def _topology_deferred_lifecycle_domains(self) -> List[TwinTopologyDeferredLifecycleDomain]:
        return [
            TwinTopologyDeferredLifecycleDomain(
                lifecycle_domain=lifecycle_domain,
                deferred_reason=deferred_reason,
                required_future_foundations=required_future_foundations,
                limitations=TOPOLOGY_READINESS_LIMITATIONS + TOPOLOGY_SNAPSHOT_LIMITATIONS,
            )
            for lifecycle_domain, deferred_reason, required_future_foundations in DEFERRED_TOPOLOGY_LIFECYCLE_DOMAINS
        ]

    def _topology_missing_readiness_indicators(
        self, snapshot_limitations: List[str]
    ) -> List[TwinTopologyMissingReadinessIndicator]:
        limitation_text = " ".join(snapshot_limitations).lower()
        indicators = []
        for indicator, marker, reason in TOPOLOGY_MISSING_READINESS_INDICATORS:
            source_marker_found = marker.lower() in limitation_text
            indicators.append(
                TwinTopologyMissingReadinessIndicator(
                    indicator=indicator,
                    present=False,
                    source_marker_found=source_marker_found,
                    reason=reason,
                    derived_from=["topology_snapshot_limitations"],
                    limitations=TOPOLOGY_READINESS_LIMITATIONS + TOPOLOGY_SNAPSHOT_LIMITATIONS,
                )
            )
        return indicators

    def _topology_lifecycle_readiness_summary(
        self,
        nodes: List[TwinTopologyNode],
        edges: List[TwinTopologyEdge],
        records: List[TwinPlanningContextRecord],
        deferred_lifecycle_domains: List[TwinTopologyDeferredLifecycleDomain],
        missing_readiness_indicators: List[TwinTopologyMissingReadinessIndicator],
    ) -> TwinTopologyLifecycleReadinessSummary:
        domains_present = sorted(
            {
                node.lifecycle_domain.value
                for node in nodes
            }
        )
        provenance_gap_count = sum(len(node.provenance_gap_types) for node in nodes)
        dependency_labels = sorted(
            {
                label
                for node in nodes
                for label in node.dependency_awareness_labels
            }
        )
        planning_dependency_warning_count = sum(
            len(record.planning_dependency_warnings)
            for record in records
        )
        return TwinTopologyLifecycleReadinessSummary(
            node_count=len(nodes),
            edge_count=len(edges),
            domains_present=domains_present,
            domains_deferred=[domain.lifecycle_domain for domain in deferred_lifecycle_domains],
            provenance_gap_count=provenance_gap_count,
            planning_dependency_warning_count=planning_dependency_warning_count,
            dependency_awareness_labels=dependency_labels,
            missing_readiness_indicator_count=len(missing_readiness_indicators),
            limitations=TOPOLOGY_READINESS_LIMITATIONS + TOPOLOGY_SNAPSHOT_LIMITATIONS,
        )

    def build_topology_snapshot_view(self, db, home_id: str) -> Optional[TwinTopologySnapshot]:
        context = self.build(db, home_id)
        if context is None:
            return None

        section_records = [
            (section.section_key, record)
            for section in context.sections
            if section.section_key in TOPOLOGY_SNAPSHOT_SECTION_ALLOWLIST
            for record in section.records
            if record.entity_id is not None
        ]
        nodes = [
            self._topology_node(section_key, record)
            for section_key, record in section_records
        ]
        node_map = {
            (node.entity_type, node.entity_id): node
            for node in nodes
        }
        records = [record for _, record in section_records]
        dependency_edges = self._topology_edges(records, node_map)
        relationship_edges, missing_relationship_indicators = self._topology_relationship_coverage_edges(
            section_records,
            node_map,
        )
        edges = self._topology_deduped_edges([dependency_edges, relationship_edges])
        relationship_coverage_summary = self._topology_relationship_coverage_summary(
            dependency_edges,
            relationship_edges,
            missing_relationship_indicators,
        )
        lifecycle_counts = Counter(node.lifecycle_domain.value for node in nodes)
        lifecycle_domain_summary = {
            domain.value: lifecycle_counts.get(domain.value, 0)
            for domain in TwinTopologyLifecycleDomain
        }
        snapshot_limitations = [
            "No twin_id is created or inferred.",
            "No topology graph, graph database, canonical topology table, migration, or persisted topology state is created.",
            "No topology promotion workflow, lifecycle event log, recalculation engine, invalidation engine, simulation, or Phase 3 intelligence is implemented.",
            "No auth, RBAC/ABAC, permission enforcement, exports, utility sharing, telemetry governance, ownership transfer, registry, marketplace, or operational control is implemented.",
        ]
        readiness_hints = self._topology_lifecycle_readiness_hints(section_records, nodes, edges)
        deferred_lifecycle_domains = self._topology_deferred_lifecycle_domains()
        missing_readiness_indicators = self._topology_missing_readiness_indicators(
            snapshot_limitations
            + TOPOLOGY_SNAPSHOT_LIMITATIONS
        )
        readiness_summary = self._topology_lifecycle_readiness_summary(
            nodes,
            edges,
            records,
            deferred_lifecycle_domains,
            missing_readiness_indicators,
        )

        return TwinTopologySnapshot(
            home_id=home_id,
            implementation_boundary=(
                "Read-only topology snapshot derived from the existing home_id-anchored Twin Planning Context; "
                "not a persisted graph, canonical topology table, lifecycle event log, export, or operational model."
            ),
            nodes=nodes,
            edges=edges,
            scenario_branch_references=self._topology_scenario_branch_references(records, node_map),
            revision_lineage_references=self._topology_revision_lineage_references(records, node_map),
            lifecycle_domain_summary=lifecycle_domain_summary,
            lifecycle_readiness_summary=readiness_summary,
            lifecycle_readiness_hints=readiness_hints,
            deferred_lifecycle_domains=deferred_lifecycle_domains,
            missing_readiness_indicators=missing_readiness_indicators,
            relationship_coverage_summary=relationship_coverage_summary,
            missing_relationship_indicators=missing_relationship_indicators,
            limitations=snapshot_limitations,
            compatibility_note=(
                "Existing TwinPlanningContext, AI grounding, runtime projection, and current /api/* contracts remain unchanged; "
                "this is an additive topology snapshot view."
            ),
        )

    def _sorted_unique(self, values: Iterable[Optional[str]]) -> List[str]:
        return sorted({value for value in values if value})

    def _dependency_warning_ref(self, warning: TwinPlanningDependencyWarning) -> str:
        return ":".join(
            [
                warning.entity_type,
                warning.entity_id or "unknown",
                warning.warning_type,
            ]
        )

    def _provenance_gap_ref(self, gap: TwinPlanningProvenanceGap) -> str:
        return ":".join(
            [
                gap.gap_type.value,
                gap.entity_type,
                gap.entity_id or "unknown",
                gap.field_name or "record",
            ]
        )

    def _missing_readiness_ref(self, indicator: TwinTopologyMissingReadinessIndicator) -> str:
        return indicator.indicator

    def _missing_relationship_ref(self, indicator: TwinTopologyMissingRelationshipIndicator) -> str:
        return ":".join(
            [
                indicator.indicator,
                indicator.entity_type,
                indicator.entity_id or "unknown",
                indicator.field_name or "relationship",
            ]
        )

    def _all_context_records_with_sections(
        self, context: TwinPlanningContext
    ) -> List[tuple]:
        return [
            (section.section_key, record)
            for section in context.sections
            for record in section.records
        ]

    def _dependency_impact_lifecycle_signals(
        self, snapshot: TwinTopologySnapshot
    ) -> List[str]:
        signals = []
        for domain in sorted(snapshot.lifecycle_readiness_summary.domains_present):
            signals.append(f"summary:domain_present:{domain}")
        for domain in sorted(snapshot.lifecycle_readiness_summary.domains_deferred):
            signals.append(f"summary:domain_deferred:{domain}")
        for hint in sorted(
            snapshot.lifecycle_readiness_hints,
            key=lambda item: item.lifecycle_domain.value,
        ):
            signals.append(
                f"hint:{hint.lifecycle_domain.value}:{hint.readiness_status}"
            )
        for indicator in sorted(
            snapshot.missing_readiness_indicators,
            key=lambda item: item.indicator,
        ):
            signals.append(
                f"missing_readiness:{indicator.indicator}:present:{str(indicator.present).lower()}"
            )
        return signals

    def _dependency_impact_basis(
        self,
        *,
        source_section_keys: Optional[List[str]] = None,
        topology_node_ids: Optional[List[str]] = None,
        topology_edge_ids: Optional[List[str]] = None,
        lifecycle_readiness_signals_used: Optional[List[str]] = None,
        dependency_warning_refs: Optional[List[str]] = None,
        provenance_gap_refs: Optional[List[str]] = None,
        missing_readiness_indicator_refs: Optional[List[str]] = None,
        missing_relationship_indicator_refs: Optional[List[str]] = None,
        derived_from: Optional[List[str]] = None,
        source_view_names: Optional[List[str]] = None,
        limitations: Optional[List[str]] = None,
    ) -> TwinDependencyImpactStatementBasis:
        return TwinDependencyImpactStatementBasis(
            source_view_names=self._sorted_unique(
                source_view_names or ["twin_planning_context", "topology_snapshot"]
            ),
            source_section_keys=self._sorted_unique(source_section_keys or []),
            topology_node_ids=self._sorted_unique(topology_node_ids or []),
            topology_edge_ids=self._sorted_unique(topology_edge_ids or []),
            lifecycle_readiness_signals_used=self._sorted_unique(
                lifecycle_readiness_signals_used or []
            ),
            dependency_warning_refs=self._sorted_unique(dependency_warning_refs or []),
            provenance_gap_refs=self._sorted_unique(provenance_gap_refs or []),
            missing_readiness_indicator_refs=self._sorted_unique(
                missing_readiness_indicator_refs or []
            ),
            missing_relationship_indicator_refs=self._sorted_unique(
                missing_relationship_indicator_refs or []
            ),
            derived_from=self._sorted_unique(derived_from or []),
            limitations=limitations or DEPENDENCY_IMPACT_READINESS_LIMITATIONS,
        )

    def _dependency_impact_record_refs(
        self, section_records: List[tuple]
    ) -> tuple:
        warning_refs = []
        provenance_gap_refs = []
        sections_by_entity = {}
        for section_key, record in section_records:
            sections_by_entity.setdefault((record.entity_type, record.entity_id), set()).add(section_key)
            for warning in record.planning_dependency_warnings:
                warning_refs.append(self._dependency_warning_ref(warning))
            for gap in record.provenance_gaps:
                provenance_gap_refs.append(self._provenance_gap_ref(gap))
        return warning_refs, provenance_gap_refs, sections_by_entity

    def _dependency_impact_confidence_posture(
        self,
        *,
        warning_refs: List[str],
        provenance_gap_refs: List[str],
        missing_readiness_refs: List[str],
        missing_relationship_refs: List[str],
    ) -> str:
        has_dependency_limits = bool(warning_refs or missing_relationship_refs)
        has_missing_readiness = bool(missing_readiness_refs)
        has_provenance_limits = bool(provenance_gap_refs)
        if has_provenance_limits and (has_dependency_limits or has_missing_readiness):
            return "provenance_dependency_and_missing_information_limited"
        if has_provenance_limits:
            return "provenance_limited"
        if has_dependency_limits:
            return "dependency_limited"
        if has_missing_readiness:
            return "missing_readiness_limited"
        return "descriptive_planning_context_present"

    def _dependency_impact_nodes_for_domain(
        self, snapshot: TwinTopologySnapshot, lifecycle_domain: TwinTopologyLifecycleDomain
    ) -> List[str]:
        return [
            node.node_id
            for node in snapshot.nodes
            if node.lifecycle_domain == lifecycle_domain
        ]

    def _dependency_impact_edges_for_domain(
        self, snapshot: TwinTopologySnapshot, lifecycle_domain: TwinTopologyLifecycleDomain
    ) -> List[str]:
        return [
            edge.edge_id
            for edge in snapshot.edges
            if edge.lifecycle_domain == lifecycle_domain
        ]

    def _dependency_impact_edges_for_nodes(
        self, snapshot: TwinTopologySnapshot, node_ids: List[str]
    ) -> List[str]:
        node_id_set = set(node_ids)
        return [
            edge.edge_id
            for edge in snapshot.edges
            if edge.source_node_id in node_id_set or edge.target_node_id in node_id_set
        ]

    def _dependency_impact_lifecycle_scope(
        self,
        *,
        snapshot: TwinTopologySnapshot,
        sections_by_entity: Dict[tuple, set],
    ) -> List[TwinDependencyImpactPostureItem]:
        items = []
        for hint in sorted(
            snapshot.lifecycle_readiness_hints,
            key=lambda item: item.lifecycle_domain.value,
        ):
            node_ids = self._dependency_impact_nodes_for_domain(snapshot, hint.lifecycle_domain)
            edge_ids = self._dependency_impact_edges_for_domain(snapshot, hint.lifecycle_domain)
            source_sections = []
            node_keys = {
                (node.entity_type, node.entity_id)
                for node in snapshot.nodes
                if node.node_id in set(node_ids)
            }
            for key in node_keys:
                source_sections.extend(sections_by_entity.get(key, []))
            signal = f"hint:{hint.lifecycle_domain.value}:{hint.readiness_status}"
            statement = (
                f"{hint.lifecycle_domain.value} is represented by {hint.node_count} topology nodes "
                f"and {hint.edge_count} topology edges with readiness status {hint.readiness_status}."
            )
            items.append(
                TwinDependencyImpactPostureItem(
                    impact_area=f"lifecycle_scope:{hint.lifecycle_domain.value}",
                    posture=hint.readiness_status,
                    statement=statement,
                    confidence_posture=hint.readiness_status,
                    basis=self._dependency_impact_basis(
                        source_section_keys=source_sections,
                        topology_node_ids=node_ids,
                        topology_edge_ids=edge_ids,
                        lifecycle_readiness_signals_used=[signal],
                        dependency_warning_refs=[
                            f"{warning_type}:{hint.lifecycle_domain.value}"
                            for warning_type in hint.planning_dependency_warning_types
                        ],
                        provenance_gap_refs=[
                            f"{gap_type}:{hint.lifecycle_domain.value}"
                            for gap_type in hint.provenance_gap_types
                        ],
                        derived_from=hint.derived_from,
                    ),
                    limitations=DEPENDENCY_IMPACT_READINESS_LIMITATIONS + hint.limitations,
                )
            )
        return items

    def _dependency_impact_posture_items(
        self,
        *,
        context: TwinPlanningContext,
        snapshot: TwinTopologySnapshot,
        warning_refs: List[str],
        provenance_gap_refs: List[str],
        missing_readiness_refs: List[str],
        missing_relationship_refs: List[str],
        lifecycle_signals: List[str],
    ) -> List[TwinDependencyImpactPostureItem]:
        section_keys = [section.section_key for section in context.sections]
        node_ids = [node.node_id for node in snapshot.nodes]
        edge_ids = [edge.edge_id for edge in snapshot.edges]
        confidence_posture = self._dependency_impact_confidence_posture(
            warning_refs=warning_refs,
            provenance_gap_refs=provenance_gap_refs,
            missing_readiness_refs=missing_readiness_refs,
            missing_relationship_refs=missing_relationship_refs,
        )

        relationship_statement = (
            "Topology relationship coverage is derived from existing topology nodes and edges; "
            f"{snapshot.relationship_coverage_summary.missing_relationship_indicator_count} unresolved relationship indicators are present."
        )
        dependency_statement = (
            "Dependency posture is derived from existing planning dependency warnings; "
            f"{len(set(warning_refs))} warning references are present."
        )
        awareness_labels = sorted(context.dependency_awareness_summary.keys())
        awareness_statement = (
            "Dependency awareness labels are copied from the existing Twin Planning Context summary: "
            + (", ".join(awareness_labels) if awareness_labels else "none")
            + "."
        )
        return [
            TwinDependencyImpactPostureItem(
                impact_area="relationship_coverage",
                posture=(
                    "relationship_limited"
                    if missing_relationship_refs
                    else "descriptive_relationship_coverage_present"
                ),
                statement=relationship_statement,
                confidence_posture=confidence_posture,
                basis=self._dependency_impact_basis(
                    source_section_keys=section_keys,
                    topology_node_ids=node_ids,
                    topology_edge_ids=edge_ids,
                    lifecycle_readiness_signals_used=lifecycle_signals,
                    dependency_warning_refs=warning_refs,
                    provenance_gap_refs=provenance_gap_refs,
                    missing_readiness_indicator_refs=missing_readiness_refs,
                    missing_relationship_indicator_refs=missing_relationship_refs,
                    derived_from=[
                        "TwinTopologySnapshot.nodes",
                        "TwinTopologySnapshot.edges",
                        "TwinTopologySnapshot.relationship_coverage_summary",
                        "TwinTopologySnapshot.missing_relationship_indicators",
                    ],
                ),
                limitations=(
                    DEPENDENCY_IMPACT_READINESS_LIMITATIONS
                    + snapshot.relationship_coverage_summary.limitations
                ),
            ),
            TwinDependencyImpactPostureItem(
                impact_area="planning_dependency_warnings",
                posture=(
                    "dependency_limited"
                    if warning_refs
                    else "no_dependency_warnings_present"
                ),
                statement=dependency_statement,
                confidence_posture=confidence_posture,
                basis=self._dependency_impact_basis(
                    source_section_keys=section_keys,
                    topology_node_ids=node_ids,
                    topology_edge_ids=edge_ids,
                    lifecycle_readiness_signals_used=lifecycle_signals,
                    dependency_warning_refs=warning_refs,
                    provenance_gap_refs=provenance_gap_refs,
                    missing_readiness_indicator_refs=missing_readiness_refs,
                    missing_relationship_indicator_refs=missing_relationship_refs,
                    derived_from=[
                        "TwinPlanningContextRecord.planning_dependency_warnings",
                        "TwinTopologySnapshot.lifecycle_readiness_summary",
                    ],
                ),
                limitations=(
                    DEPENDENCY_IMPACT_READINESS_LIMITATIONS
                    + PLANNING_DEPENDENCY_WARNING_LIMITATIONS
                ),
            ),
            TwinDependencyImpactPostureItem(
                impact_area="dependency_awareness_summary",
                posture=(
                    "dependency_awareness_labels_present"
                    if awareness_labels
                    else "no_dependency_awareness_labels_present"
                ),
                statement=awareness_statement,
                confidence_posture=confidence_posture,
                basis=self._dependency_impact_basis(
                    source_section_keys=section_keys,
                    topology_node_ids=node_ids,
                    topology_edge_ids=edge_ids,
                    lifecycle_readiness_signals_used=lifecycle_signals,
                    dependency_warning_refs=warning_refs,
                    provenance_gap_refs=provenance_gap_refs,
                    missing_readiness_indicator_refs=missing_readiness_refs,
                    missing_relationship_indicator_refs=missing_relationship_refs,
                    derived_from=[
                        "TwinPlanningContext.dependency_awareness_summary",
                        "TwinTopologySnapshot.lifecycle_readiness_summary",
                    ],
                ),
                limitations=(
                    DEPENDENCY_IMPACT_READINESS_LIMITATIONS
                    + DEPENDENCY_AWARENESS_LIMITATIONS
                ),
            ),
        ]

    def _dependency_missing_inputs(
        self,
        *,
        snapshot: TwinTopologySnapshot,
        provenance_gap_refs: List[str],
    ) -> List[TwinDependencyMissingInputItem]:
        items: List[TwinDependencyMissingInputItem] = []
        for indicator in sorted(
            snapshot.missing_readiness_indicators,
            key=lambda item: item.indicator,
        ):
            if indicator.present:
                continue
            items.append(
                TwinDependencyMissingInputItem(
                    missing_input=indicator.indicator,
                    reason=indicator.reason,
                    basis=self._dependency_impact_basis(
                        missing_readiness_indicator_refs=[self._missing_readiness_ref(indicator)],
                        derived_from=indicator.derived_from,
                    ),
                    limitations=DEPENDENCY_IMPACT_READINESS_LIMITATIONS + indicator.limitations,
                )
            )

        for indicator in sorted(
            snapshot.missing_relationship_indicators,
            key=lambda item: self._missing_relationship_ref(item),
        ):
            items.append(
                TwinDependencyMissingInputItem(
                    missing_input=self._missing_relationship_ref(indicator),
                    reason=indicator.reason,
                    basis=self._dependency_impact_basis(
                        missing_relationship_indicator_refs=[
                            self._missing_relationship_ref(indicator)
                        ],
                        derived_from=indicator.derived_from,
                    ),
                    limitations=DEPENDENCY_IMPACT_READINESS_LIMITATIONS + indicator.limitations,
                )
            )

        for gap_ref in sorted(set(provenance_gap_refs)):
            items.append(
                TwinDependencyMissingInputItem(
                    missing_input=f"provenance:{gap_ref}",
                    reason=(
                        "A source or provenance basis is missing or partial for this recorded planning context."
                    ),
                    basis=self._dependency_impact_basis(
                        provenance_gap_refs=[gap_ref],
                        derived_from=["TwinPlanningContextRecord.provenance_gaps"],
                    ),
                    limitations=DEPENDENCY_IMPACT_READINESS_LIMITATIONS + PROVENANCE_GAP_LIMITATIONS,
                )
            )
        return items

    def _dependency_provenance_gap_posture(
        self,
        *,
        context: TwinPlanningContext,
        snapshot: TwinTopologySnapshot,
    ) -> List[TwinDependencyImpactPostureItem]:
        section_records = self._all_context_records_with_sections(context)
        node_by_entity = {
            (node.entity_type, node.entity_id): node
            for node in snapshot.nodes
        }
        refs_by_gap_type: Dict[str, List[str]] = {}
        node_ids_by_gap_type: Dict[str, List[str]] = {}
        sections_by_gap_type: Dict[str, List[str]] = {}
        for section_key, record in section_records:
            node = node_by_entity.get((record.entity_type, record.entity_id))
            for gap in record.provenance_gaps:
                gap_type = gap.gap_type.value
                refs_by_gap_type.setdefault(gap_type, []).append(self._provenance_gap_ref(gap))
                sections_by_gap_type.setdefault(gap_type, []).append(section_key)
                if node is not None:
                    node_ids_by_gap_type.setdefault(gap_type, []).append(node.node_id)

        items = []
        for gap_type in sorted(refs_by_gap_type):
            node_ids = node_ids_by_gap_type.get(gap_type, [])
            refs = refs_by_gap_type[gap_type]
            edge_ids = self._dependency_impact_edges_for_nodes(snapshot, node_ids)
            items.append(
                TwinDependencyImpactPostureItem(
                    impact_area=f"provenance_gap:{gap_type}",
                    posture="provenance_limited",
                    statement=(
                        f"{len(set(refs))} {gap_type} provenance gap references are present in the existing Twin Planning Context."
                    ),
                    confidence_posture="provenance_limited",
                    basis=self._dependency_impact_basis(
                        source_section_keys=sections_by_gap_type.get(gap_type, []),
                        topology_node_ids=node_ids,
                        topology_edge_ids=edge_ids,
                        provenance_gap_refs=refs,
                        derived_from=["TwinPlanningContextRecord.provenance_gaps"],
                    ),
                    limitations=DEPENDENCY_IMPACT_READINESS_LIMITATIONS + PROVENANCE_GAP_LIMITATIONS,
                )
            )
        return items

    def build_dependency_impact_readiness_view(
        self, db, home_id: str
    ) -> Optional[TwinDependencyImpactReadinessView]:
        context = self.build(db, home_id)
        if context is None:
            return None
        snapshot = self.build_topology_snapshot_view(db, home_id)
        if snapshot is None:
            return None

        section_records = self._all_context_records_with_sections(context)
        warning_refs, provenance_gap_refs, sections_by_entity = self._dependency_impact_record_refs(
            section_records
        )
        missing_readiness_refs = [
            self._missing_readiness_ref(indicator)
            for indicator in snapshot.missing_readiness_indicators
            if not indicator.present
        ]
        missing_relationship_refs = [
            self._missing_relationship_ref(indicator)
            for indicator in snapshot.missing_relationship_indicators
        ]
        lifecycle_signals = self._dependency_impact_lifecycle_signals(snapshot)
        source_section_keys = [section.section_key for section in context.sections]
        topology_node_ids = [node.node_id for node in snapshot.nodes]
        topology_edge_ids = [edge.edge_id for edge in snapshot.edges]
        confidence_posture = self._dependency_impact_confidence_posture(
            warning_refs=warning_refs,
            provenance_gap_refs=provenance_gap_refs,
            missing_readiness_refs=missing_readiness_refs,
            missing_relationship_refs=missing_relationship_refs,
        )

        source_basis = self._dependency_impact_basis(
            source_section_keys=source_section_keys,
            topology_node_ids=topology_node_ids,
            topology_edge_ids=topology_edge_ids,
            lifecycle_readiness_signals_used=lifecycle_signals,
            dependency_warning_refs=warning_refs,
            provenance_gap_refs=provenance_gap_refs,
            missing_readiness_indicator_refs=missing_readiness_refs,
            missing_relationship_indicator_refs=missing_relationship_refs,
            derived_from=[
                "TwinPlanningContext",
                "TwinTopologySnapshot",
                "TwinTopologySnapshot.lifecycle_readiness_summary",
                "TwinTopologySnapshot.relationship_coverage_summary",
            ],
        )

        confidence_item = TwinDependencyImpactPostureItem(
            impact_area="overall_confidence_posture",
            posture=confidence_posture,
            statement=(
                "Overall dependency impact readiness confidence is derived from planning dependency warnings, "
                "provenance gaps, missing lifecycle readiness indicators, and missing relationship indicators."
            ),
            confidence_posture=confidence_posture,
            basis=source_basis,
            limitations=DEPENDENCY_IMPACT_READINESS_LIMITATIONS,
        )

        return TwinDependencyImpactReadinessView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 3A derived intelligence envelope built request-time from TwinPlanningContext "
                "and topology snapshot; not a graph engine, scenario engine, simulation, what-if analysis, "
                "export, permission enforcement layer, or operational model."
            ),
            source_basis=source_basis,
            readiness_summary=TwinDependencyImpactReadinessSummary(
                limitations=DEPENDENCY_IMPACT_READINESS_LIMITATIONS,
            ),
            lifecycle_scope=self._dependency_impact_lifecycle_scope(
                snapshot=snapshot,
                sections_by_entity=sections_by_entity,
            ),
            dependency_impact_posture=self._dependency_impact_posture_items(
                context=context,
                snapshot=snapshot,
                warning_refs=warning_refs,
                provenance_gap_refs=provenance_gap_refs,
                missing_readiness_refs=missing_readiness_refs,
                missing_relationship_refs=missing_relationship_refs,
                lifecycle_signals=lifecycle_signals,
            ),
            missing_inputs=self._dependency_missing_inputs(
                snapshot=snapshot,
                provenance_gap_refs=provenance_gap_refs,
            ),
            provenance_gap_posture=self._dependency_provenance_gap_posture(
                context=context,
                snapshot=snapshot,
            ),
            confidence_posture=[confidence_item],
            deferred_capabilities=sorted(DEPENDENCY_IMPACT_DEFERRED_CAPABILITIES),
            limitations=DEPENDENCY_IMPACT_READINESS_LIMITATIONS,
            compatibility_note=(
                "Existing TwinPlanningContext, topology snapshot, AI grounding, runtime projection, and current /api/* "
                "contracts remain unchanged; this is an additive Phase 3A derived intelligence view."
            ),
        )

    def _dependency_reasoning_basis(
        self,
        *,
        source_section_keys: Optional[List[str]] = None,
        topology_node_ids: Optional[List[str]] = None,
        topology_edge_ids: Optional[List[str]] = None,
        lifecycle_readiness_signals_used: Optional[List[str]] = None,
        dependency_warning_refs: Optional[List[str]] = None,
        provenance_gap_refs: Optional[List[str]] = None,
        missing_readiness_indicator_refs: Optional[List[str]] = None,
        missing_relationship_indicator_refs: Optional[List[str]] = None,
        derived_from: Optional[List[str]] = None,
    ) -> TwinDependencyImpactStatementBasis:
        return self._dependency_impact_basis(
            source_view_names=[
                "twin_planning_context",
                "topology_snapshot",
                "dependency_impact_readiness",
            ],
            source_section_keys=source_section_keys,
            topology_node_ids=topology_node_ids,
            topology_edge_ids=topology_edge_ids,
            lifecycle_readiness_signals_used=lifecycle_readiness_signals_used,
            dependency_warning_refs=dependency_warning_refs,
            provenance_gap_refs=provenance_gap_refs,
            missing_readiness_indicator_refs=missing_readiness_indicator_refs,
            missing_relationship_indicator_refs=missing_relationship_indicator_refs,
            derived_from=derived_from,
            limitations=DEPENDENCY_REASONING_LIMITATIONS,
        )

    def _dependency_reasoning_item_sort_key(self, item: TwinDependencyReasoningItem) -> tuple:
        return (item.reasoning_type.value, item.subject_ref, item.statement)

    def _dependency_reasoning_items_from_edges(
        self, snapshot: TwinTopologySnapshot
    ) -> List[TwinDependencyReasoningItem]:
        items = []
        for edge in sorted(snapshot.edges, key=lambda item: item.edge_id):
            basis = self._dependency_reasoning_basis(
                topology_node_ids=[edge.source_node_id, edge.target_node_id],
                topology_edge_ids=[edge.edge_id],
                lifecycle_readiness_signals_used=[
                    f"edge_lifecycle:{edge.lifecycle_domain.value}"
                ],
                derived_from=[
                    "TwinTopologySnapshot.edges",
                    "TwinTopologyEdge.source_node_id",
                    "TwinTopologyEdge.target_node_id",
                    "TwinTopologyEdge.relationship",
                ],
            )
            items.append(
                TwinDependencyReasoningItem(
                    reasoning_type=TwinDependencyReasoningType.topology_dependency,
                    subject_ref=edge.edge_id,
                    statement=(
                        f"Topology edge {edge.edge_id} explains that {edge.source_node_id} is the recorded "
                        f"source side and {edge.target_node_id} is the recorded target side for relationship {edge.relationship}."
                    ),
                    confidence_posture=edge.confidence_level or "descriptive_topology_relationship",
                    basis=basis,
                    limitations=DEPENDENCY_REASONING_LIMITATIONS + edge.limitations,
                )
            )
        return items

    def _dependency_reasoning_upstream_downstream_items(
        self, snapshot: TwinTopologySnapshot
    ) -> List[TwinDependencyReasoningItem]:
        items = []
        for edge in sorted(snapshot.edges, key=lambda item: item.edge_id):
            items.append(
                TwinDependencyReasoningItem(
                    reasoning_type=TwinDependencyReasoningType.topology_dependency,
                    subject_ref=f"direction:{edge.edge_id}",
                    statement=(
                        f"Directional dependency interpretation for {edge.edge_id} follows topology edge metadata only: "
                        f"{edge.source_node_id} is upstream/source-side context and {edge.target_node_id} is downstream/target-side context."
                    ),
                    confidence_posture=edge.confidence_level or "source_target_metadata_only",
                    basis=self._dependency_reasoning_basis(
                        topology_node_ids=[edge.source_node_id, edge.target_node_id],
                        topology_edge_ids=[edge.edge_id],
                        lifecycle_readiness_signals_used=[
                            f"edge_lifecycle:{edge.lifecycle_domain.value}"
                        ],
                        derived_from=[
                            "TwinTopologySnapshot.edges",
                            "TwinTopologyEdge.source_node_id",
                            "TwinTopologyEdge.target_node_id",
                        ],
                    ),
                    limitations=DEPENDENCY_REASONING_LIMITATIONS
                    + [
                        "Upstream/downstream means topology edge source/target direction only; it is not measured power flow, field verification, utility approval, or operational direction.",
                    ],
                )
            )
        return items

    def _dependency_reasoning_source_items(
        self,
        *,
        section_records: List[tuple],
        node_by_entity: Dict[tuple, TwinTopologyNode],
    ) -> List[TwinDependencyReasoningItem]:
        items = []
        for section_key, record in sorted(
            section_records,
            key=lambda item: (item[0], item[1].entity_type, item[1].entity_id or ""),
        ):
            if not (record.source_document_ids or record.data_origin or record.provenance_summary):
                continue
            subject_ref = f"{record.entity_type}:{record.entity_id or 'unknown'}"
            node = node_by_entity.get((record.entity_type, record.entity_id))
            source_basis_parts = []
            if record.source_document_ids:
                source_basis_parts.append(f"{len(record.source_document_ids)} source document refs")
            if record.data_origin:
                source_basis_parts.append(f"data origin {record.data_origin.value}")
            if record.provenance_summary:
                source_basis_parts.append("provenance summary")
            items.append(
                TwinDependencyReasoningItem(
                    reasoning_type=TwinDependencyReasoningType.source_dependency,
                    subject_ref=subject_ref,
                    statement=(
                        f"{subject_ref} has source dependency context from existing "
                        f"{', '.join(source_basis_parts)}."
                    ),
                    confidence_posture="source_context_present",
                    basis=self._dependency_reasoning_basis(
                        source_section_keys=[section_key],
                        topology_node_ids=[node.node_id] if node else [],
                        provenance_gap_refs=[
                            self._provenance_gap_ref(gap)
                            for gap in record.provenance_gaps
                        ],
                        derived_from=[
                            "TwinPlanningContextRecord.source_document_ids",
                            "TwinPlanningContextRecord.data_origin",
                            "TwinPlanningContextRecord.provenance_summary",
                        ],
                    ),
                    limitations=DEPENDENCY_REASONING_LIMITATIONS
                    + [
                        "Source dependency context identifies recorded source posture only; it does not verify correctness or create field authority.",
                    ],
                )
            )
        return items

    def _dependency_reasoning_lifecycle_items(
        self, impact_view: TwinDependencyImpactReadinessView
    ) -> List[TwinDependencyReasoningItem]:
        items = []
        for impact_item in sorted(impact_view.lifecycle_scope, key=lambda item: item.impact_area):
            basis = self._dependency_reasoning_basis(
                source_section_keys=impact_item.basis.source_section_keys,
                topology_node_ids=impact_item.basis.topology_node_ids,
                topology_edge_ids=impact_item.basis.topology_edge_ids,
                lifecycle_readiness_signals_used=impact_item.basis.lifecycle_readiness_signals_used,
                dependency_warning_refs=impact_item.basis.dependency_warning_refs,
                provenance_gap_refs=impact_item.basis.provenance_gap_refs,
                missing_readiness_indicator_refs=impact_item.basis.missing_readiness_indicator_refs,
                missing_relationship_indicator_refs=impact_item.basis.missing_relationship_indicator_refs,
                derived_from=impact_item.basis.derived_from
                + ["TwinDependencyImpactReadinessView.lifecycle_scope"],
            )
            items.append(
                TwinDependencyReasoningItem(
                    reasoning_type=TwinDependencyReasoningType.lifecycle_dependency,
                    subject_ref=impact_item.impact_area,
                    statement=(
                        f"Lifecycle dependency context for {impact_item.impact_area} is explained from Phase 3A posture {impact_item.posture}: {impact_item.statement}"
                    ),
                    confidence_posture=impact_item.confidence_posture,
                    basis=basis,
                    limitations=DEPENDENCY_REASONING_LIMITATIONS + impact_item.limitations,
                )
            )
        return items

    def _dependency_reasoning_rule_items(
        self,
        *,
        section_records: List[tuple],
        snapshot: TwinTopologySnapshot,
    ) -> List[TwinDependencyReasoningItem]:
        sections_by_rule: Dict[str, List[str]] = {}
        edge_ids_by_rule: Dict[str, List[str]] = {}
        warning_refs_by_rule: Dict[str, List[str]] = {}
        for section_key, record in section_records:
            rule_keys = list(record.rule_keys)
            for hook in record.dependency_hooks:
                rule_keys.extend(hook.rule_keys)
            for warning in record.planning_dependency_warnings:
                for rule_key in warning.rule_keys:
                    warning_refs_by_rule.setdefault(rule_key, []).append(
                        self._dependency_warning_ref(warning)
                    )
                    rule_keys.append(rule_key)
            for rule_key in rule_keys:
                sections_by_rule.setdefault(rule_key, []).append(section_key)
        for edge in snapshot.edges:
            for rule_key in edge.rule_keys:
                edge_ids_by_rule.setdefault(rule_key, []).append(edge.edge_id)

        items = []
        for rule_key in sorted(set(sections_by_rule) | set(edge_ids_by_rule)):
            section_count = len(set(sections_by_rule.get(rule_key, [])))
            edge_count = len(set(edge_ids_by_rule.get(rule_key, [])))
            items.append(
                TwinDependencyReasoningItem(
                    reasoning_type=TwinDependencyReasoningType.rule_dependency,
                    subject_ref=rule_key,
                    statement=(
                        f"Rule dependency {rule_key} appears in {section_count} Twin Planning Context sections "
                        f"and {edge_count} topology edges."
                    ),
                    confidence_posture="deterministic_rule_reference_present",
                    basis=self._dependency_reasoning_basis(
                        source_section_keys=sections_by_rule.get(rule_key, []),
                        topology_edge_ids=edge_ids_by_rule.get(rule_key, []),
                        dependency_warning_refs=warning_refs_by_rule.get(rule_key, []),
                        derived_from=[
                            "TwinPlanningContextRecord.rule_keys",
                            "TwinPlanningDependencyHook.rule_keys",
                            "TwinPlanningDependencyWarning.rule_keys",
                            "TwinTopologyEdge.rule_keys",
                        ],
                    ),
                    limitations=DEPENDENCY_REASONING_LIMITATIONS
                    + [
                        "Rule dependency context identifies existing rule references only; it does not run a recalculation or choose an action.",
                    ],
                )
            )
        return items

    def _dependency_reasoning_provenance_items(
        self, impact_view: TwinDependencyImpactReadinessView
    ) -> List[TwinDependencyReasoningItem]:
        items = []
        for impact_item in sorted(impact_view.provenance_gap_posture, key=lambda item: item.impact_area):
            items.append(
                TwinDependencyReasoningItem(
                    reasoning_type=TwinDependencyReasoningType.provenance_dependency,
                    subject_ref=impact_item.impact_area,
                    statement=(
                        f"Provenance dependency context for {impact_item.impact_area} is explained from Phase 3A posture {impact_item.posture}: {impact_item.statement}"
                    ),
                    confidence_posture=impact_item.confidence_posture,
                    basis=self._dependency_reasoning_basis(
                        source_section_keys=impact_item.basis.source_section_keys,
                        topology_node_ids=impact_item.basis.topology_node_ids,
                        topology_edge_ids=impact_item.basis.topology_edge_ids,
                        provenance_gap_refs=impact_item.basis.provenance_gap_refs,
                        derived_from=impact_item.basis.derived_from
                        + ["TwinDependencyImpactReadinessView.provenance_gap_posture"],
                    ),
                    limitations=DEPENDENCY_REASONING_LIMITATIONS + impact_item.limitations,
                )
            )
        return items

    def _dependency_reasoning_permission_items(
        self,
        *,
        context: TwinPlanningContext,
        section_records: List[tuple],
        node_by_entity: Dict[tuple, TwinTopologyNode],
    ) -> List[TwinDependencyReasoningItem]:
        items = []
        if context.permission_readiness is not None:
            items.append(
                TwinDependencyReasoningItem(
                    reasoning_type=TwinDependencyReasoningType.permission_readiness_dependency,
                    subject_ref="context_permission_readiness",
                    statement=(
                        f"Context permission readiness describes audience {context.permission_readiness.audience} "
                        f"and purpose {context.permission_readiness.purpose}; permission enforcement remains not enforced."
                    ),
                    confidence_posture="permission_readiness_metadata_only",
                    basis=self._dependency_reasoning_basis(
                        source_section_keys=[section.section_key for section in context.sections],
                        derived_from=["TwinPlanningContext.permission_readiness"],
                    ),
                    limitations=DEPENDENCY_REASONING_LIMITATIONS + PERMISSION_READINESS_LIMITATIONS,
                )
            )

        for section_key, record in sorted(
            section_records,
            key=lambda item: (item[0], item[1].entity_type, item[1].entity_id or ""),
        ):
            if record.permission_readiness is None:
                continue
            subject_ref = f"{record.entity_type}:{record.entity_id or 'unknown'}"
            node = node_by_entity.get((record.entity_type, record.entity_id))
            items.append(
                TwinDependencyReasoningItem(
                    reasoning_type=TwinDependencyReasoningType.permission_readiness_dependency,
                    subject_ref=subject_ref,
                    statement=(
                        f"{subject_ref} carries permission readiness metadata for audience {record.permission_readiness.audience} "
                        f"and purpose {record.permission_readiness.purpose}; it is not an authorization decision."
                    ),
                    confidence_posture="permission_readiness_metadata_only",
                    basis=self._dependency_reasoning_basis(
                        source_section_keys=[section_key],
                        topology_node_ids=[node.node_id] if node else [],
                        derived_from=["TwinPlanningContextRecord.permission_readiness"],
                    ),
                    limitations=DEPENDENCY_REASONING_LIMITATIONS + PERMISSION_READINESS_LIMITATIONS,
                )
            )
        return items

    def _dependency_reasoning_continuity_items(
        self, snapshot: TwinTopologySnapshot
    ) -> List[TwinDependencyReasoningItem]:
        items = []
        if snapshot.scenario_branch_references:
            items.append(
                TwinDependencyReasoningItem(
                    reasoning_type=TwinDependencyReasoningType.continuity_snapshot_dependency,
                    subject_ref="scenario_branch_references",
                    statement=(
                        f"Topology snapshot includes {len(snapshot.scenario_branch_references)} scenario branch references as snapshot-bound continuity context."
                    ),
                    confidence_posture="snapshot_bound_context_only",
                    basis=self._dependency_reasoning_basis(
                        derived_from=["TwinTopologySnapshot.scenario_branch_references"],
                    ),
                    limitations=DEPENDENCY_REASONING_LIMITATIONS
                    + [
                        "Scenario branch references are continuity context only; this view does not compare scenarios or implement scenario intelligence.",
                    ],
                )
            )
        if snapshot.revision_lineage_references:
            items.append(
                TwinDependencyReasoningItem(
                    reasoning_type=TwinDependencyReasoningType.continuity_snapshot_dependency,
                    subject_ref="revision_lineage_references",
                    statement=(
                        f"Topology snapshot includes {len(snapshot.revision_lineage_references)} revision lineage references as snapshot-bound continuity context."
                    ),
                    confidence_posture="snapshot_bound_context_only",
                    basis=self._dependency_reasoning_basis(
                        derived_from=["TwinTopologySnapshot.revision_lineage_references"],
                    ),
                    limitations=DEPENDENCY_REASONING_LIMITATIONS
                    + [
                        "Revision lineage references are continuity context only; this view does not replay, compare, or rank revisions.",
                    ],
                )
            )
        return items

    def _dependency_reasoning_missing_items(
        self, impact_view: TwinDependencyImpactReadinessView
    ) -> List[TwinDependencyReasoningItem]:
        items = []
        for missing_item in sorted(impact_view.missing_inputs, key=lambda item: item.missing_input):
            items.append(
                TwinDependencyReasoningItem(
                    reasoning_type=TwinDependencyReasoningType.missing_information_dependency,
                    subject_ref=missing_item.missing_input,
                    statement=(
                        f"Missing information dependency {missing_item.missing_input} is identified because {missing_item.reason}"
                    ),
                    confidence_posture="missing_information_limited",
                    basis=self._dependency_reasoning_basis(
                        source_section_keys=missing_item.basis.source_section_keys,
                        topology_node_ids=missing_item.basis.topology_node_ids,
                        topology_edge_ids=missing_item.basis.topology_edge_ids,
                        provenance_gap_refs=missing_item.basis.provenance_gap_refs,
                        missing_readiness_indicator_refs=missing_item.basis.missing_readiness_indicator_refs,
                        missing_relationship_indicator_refs=missing_item.basis.missing_relationship_indicator_refs,
                        derived_from=missing_item.basis.derived_from
                        + ["TwinDependencyImpactReadinessView.missing_inputs"],
                    ),
                    limitations=DEPENDENCY_REASONING_LIMITATIONS + missing_item.limitations,
                )
            )
        return items

    def build_dependency_reasoning_view(
        self, db, home_id: str
    ) -> Optional[TwinDependencyReasoningView]:
        context = self.build(db, home_id)
        if context is None:
            return None
        snapshot = self.build_topology_snapshot_view(db, home_id)
        if snapshot is None:
            return None
        impact_view = self.build_dependency_impact_readiness_view(db, home_id)
        if impact_view is None:
            return None

        section_records = self._all_context_records_with_sections(context)
        node_by_entity = {
            (node.entity_type, node.entity_id): node
            for node in snapshot.nodes
        }
        warning_refs, provenance_gap_refs, _sections_by_entity = self._dependency_impact_record_refs(
            section_records
        )
        missing_readiness_refs = [
            self._missing_readiness_ref(indicator)
            for indicator in snapshot.missing_readiness_indicators
            if not indicator.present
        ]
        missing_relationship_refs = [
            self._missing_relationship_ref(indicator)
            for indicator in snapshot.missing_relationship_indicators
        ]
        lifecycle_signals = self._dependency_impact_lifecycle_signals(snapshot)
        source_basis = self._dependency_reasoning_basis(
            source_section_keys=[section.section_key for section in context.sections],
            topology_node_ids=[node.node_id for node in snapshot.nodes],
            topology_edge_ids=[edge.edge_id for edge in snapshot.edges],
            lifecycle_readiness_signals_used=lifecycle_signals,
            dependency_warning_refs=warning_refs,
            provenance_gap_refs=provenance_gap_refs,
            missing_readiness_indicator_refs=missing_readiness_refs,
            missing_relationship_indicator_refs=missing_relationship_refs,
            derived_from=[
                "TwinPlanningContext",
                "TwinTopologySnapshot",
                "TwinDependencyImpactReadinessView",
                "TwinDependencyImpactReadinessView.source_basis",
            ],
        )

        topology_items = self._dependency_reasoning_items_from_edges(snapshot)
        upstream_downstream_items = self._dependency_reasoning_upstream_downstream_items(snapshot)
        source_items = self._dependency_reasoning_source_items(
            section_records=section_records,
            node_by_entity=node_by_entity,
        )
        lifecycle_items = self._dependency_reasoning_lifecycle_items(impact_view)
        rule_items = self._dependency_reasoning_rule_items(
            section_records=section_records,
            snapshot=snapshot,
        )
        provenance_items = self._dependency_reasoning_provenance_items(impact_view)
        permission_items = self._dependency_reasoning_permission_items(
            context=context,
            section_records=section_records,
            node_by_entity=node_by_entity,
        )
        continuity_items = self._dependency_reasoning_continuity_items(snapshot)
        missing_items = self._dependency_reasoning_missing_items(impact_view)

        confidence_posture = self._dependency_impact_confidence_posture(
            warning_refs=warning_refs,
            provenance_gap_refs=provenance_gap_refs,
            missing_readiness_refs=missing_readiness_refs,
            missing_relationship_refs=missing_relationship_refs,
        )
        confidence_item = TwinDependencyReasoningItem(
            reasoning_type=TwinDependencyReasoningType.provenance_dependency,
            subject_ref="overall_dependency_reasoning_confidence",
            statement=(
                "Overall dependency reasoning confidence is derived from Phase 3A confidence posture, "
                "planning dependency warnings, provenance gaps, missing lifecycle readiness indicators, and missing relationship indicators."
            ),
            confidence_posture=confidence_posture,
            basis=source_basis,
            limitations=DEPENDENCY_REASONING_LIMITATIONS,
        )

        primary_items = sorted(
            source_items
            + topology_items
            + upstream_downstream_items
            + lifecycle_items
            + rule_items
            + provenance_items
            + permission_items
            + continuity_items
            + missing_items,
            key=self._dependency_reasoning_item_sort_key,
        )
        type_counts = Counter(item.reasoning_type.value for item in primary_items)
        dependency_type_summary = {
            dependency_type.value: type_counts.get(dependency_type.value, 0)
            for dependency_type in TwinDependencyReasoningType
        }

        return TwinDependencyReasoningView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 3B dependency reasoning view built request-time from TwinPlanningContext, "
                "topology snapshot, and Phase 3A dependency impact readiness; not impact propagation, "
                "scenario intelligence, simulation, what-if analysis, export, permission enforcement, or operational behavior."
            ),
            source_basis=source_basis,
            reasoning_scope=TwinDependencyReasoningScope(
                limitations=DEPENDENCY_REASONING_LIMITATIONS,
            ),
            dependency_type_summary=dependency_type_summary,
            dependency_reasoning_items=primary_items,
            upstream_downstream_interpretations=sorted(
                upstream_downstream_items,
                key=self._dependency_reasoning_item_sort_key,
            ),
            lifecycle_dependency_context=sorted(
                lifecycle_items,
                key=self._dependency_reasoning_item_sort_key,
            ),
            provenance_dependency_context=sorted(
                provenance_items,
                key=self._dependency_reasoning_item_sort_key,
            ),
            missing_information_context=sorted(
                missing_items,
                key=self._dependency_reasoning_item_sort_key,
            ),
            confidence_posture=[confidence_item],
            deferred_capabilities=sorted(DEPENDENCY_REASONING_DEFERRED_CAPABILITIES),
            limitations=DEPENDENCY_REASONING_LIMITATIONS,
            compatibility_note=(
                "Existing TwinPlanningContext, topology snapshot, dependency impact readiness, AI grounding, runtime projection, "
                "and current /api/* contracts remain unchanged; this is an additive Phase 3B derived explanation view."
            ),
        )

    def _planning_intelligence_readiness_basis(
        self,
        *,
        source_section_keys: Optional[List[str]] = None,
        topology_node_ids: Optional[List[str]] = None,
        topology_edge_ids: Optional[List[str]] = None,
        lifecycle_readiness_signals_used: Optional[List[str]] = None,
        dependency_warning_refs: Optional[List[str]] = None,
        provenance_gap_refs: Optional[List[str]] = None,
        missing_readiness_indicator_refs: Optional[List[str]] = None,
        missing_relationship_indicator_refs: Optional[List[str]] = None,
        derived_from: Optional[List[str]] = None,
    ) -> TwinDependencyImpactStatementBasis:
        return self._dependency_impact_basis(
            source_view_names=[
                "twin_planning_context",
                "topology_snapshot",
                "dependency_impact_readiness",
                "dependency_reasoning",
            ],
            source_section_keys=source_section_keys,
            topology_node_ids=topology_node_ids,
            topology_edge_ids=topology_edge_ids,
            lifecycle_readiness_signals_used=lifecycle_readiness_signals_used,
            dependency_warning_refs=dependency_warning_refs,
            provenance_gap_refs=provenance_gap_refs,
            missing_readiness_indicator_refs=missing_readiness_indicator_refs,
            missing_relationship_indicator_refs=missing_relationship_indicator_refs,
            derived_from=derived_from,
            limitations=PLANNING_INTELLIGENCE_READINESS_LIMITATIONS,
        )

    def _planning_intelligence_readiness_item(
        self,
        *,
        intelligence_area: TwinPlanningIntelligenceReadinessArea,
        posture: str,
        statement: str,
        available_evidence: Optional[List[str]] = None,
        missing_prerequisites: Optional[List[str]] = None,
        unsafe_assumptions: Optional[List[str]] = None,
        confidence_posture: str,
        basis: TwinDependencyImpactStatementBasis,
        limitations: Optional[List[str]] = None,
    ) -> TwinPlanningIntelligenceReadinessItem:
        return TwinPlanningIntelligenceReadinessItem(
            intelligence_area=intelligence_area,
            posture=posture,
            statement=statement,
            available_evidence=self._sorted_unique(available_evidence or []),
            missing_prerequisites=self._sorted_unique(missing_prerequisites or []),
            unsafe_assumptions=self._sorted_unique(unsafe_assumptions or []),
            confidence_posture=confidence_posture,
            provenance_presence_is_verification=False,
            permission_readiness_is_enforcement=False,
            basis=basis,
            limitations=limitations or PLANNING_INTELLIGENCE_READINESS_LIMITATIONS,
        )

    def _planning_intelligence_item_sort_key(
        self, item: TwinPlanningIntelligenceReadinessItem
    ) -> str:
        return item.intelligence_area.value

    def _planning_intelligence_ready_items(
        self,
        *,
        context: TwinPlanningContext,
        snapshot: TwinTopologySnapshot,
        impact_view: TwinDependencyImpactReadinessView,
        reasoning_view: TwinDependencyReasoningView,
        source_basis: TwinDependencyImpactStatementBasis,
    ) -> List[TwinPlanningIntelligenceReadinessItem]:
        permission_record_count = sum(
            1
            for section in context.sections
            for record in section.records
            if record.permission_readiness is not None
        )
        ready_posture = "ready for read-only explanation"
        return sorted(
            [
                self._planning_intelligence_readiness_item(
                    intelligence_area=TwinPlanningIntelligenceReadinessArea.topology_explanation,
                    posture=ready_posture,
                    statement=(
                        "Topology explanation is ready for read-only explanation from existing topology snapshot nodes and edges."
                    ),
                    available_evidence=[
                        f"topology_nodes:{len(snapshot.nodes)}",
                        f"topology_edges:{len(snapshot.edges)}",
                        "TwinTopologySnapshot.nodes",
                        "TwinTopologySnapshot.edges",
                    ],
                    missing_prerequisites=[
                        "field_verified_topology",
                        "canonical_topology_graph",
                    ],
                    unsafe_assumptions=[
                        "Treating planning topology as field-verified topology would be unsafe.",
                    ],
                    confidence_posture="ready_for_read_only_explanation_with_planning_limits",
                    basis=self._planning_intelligence_readiness_basis(
                        topology_node_ids=[node.node_id for node in snapshot.nodes],
                        topology_edge_ids=[edge.edge_id for edge in snapshot.edges],
                        derived_from=[
                            "TwinTopologySnapshot.nodes",
                            "TwinTopologySnapshot.edges",
                        ],
                    ),
                    limitations=PLANNING_INTELLIGENCE_READINESS_LIMITATIONS
                    + TOPOLOGY_SNAPSHOT_LIMITATIONS,
                ),
                self._planning_intelligence_readiness_item(
                    intelligence_area=TwinPlanningIntelligenceReadinessArea.lifecycle_explanation,
                    posture=ready_posture,
                    statement=(
                        "Lifecycle explanation is ready for read-only explanation from topology lifecycle readiness metadata."
                    ),
                    available_evidence=[
                        f"lifecycle_hints:{len(snapshot.lifecycle_readiness_hints)}",
                        f"domains_present:{len(snapshot.lifecycle_readiness_summary.domains_present)}",
                        "TwinTopologySnapshot.lifecycle_readiness_summary",
                        "TwinTopologySnapshot.lifecycle_readiness_hints",
                    ],
                    missing_prerequisites=[
                        "lifecycle_workflow",
                        "lifecycle_event_log",
                        "topology_promotion_workflow",
                    ],
                    unsafe_assumptions=[
                        "Treating lifecycle readiness metadata as lifecycle workflow state would be unsafe.",
                    ],
                    confidence_posture="ready_for_read_only_explanation_with_lifecycle_limits",
                    basis=self._planning_intelligence_readiness_basis(
                        lifecycle_readiness_signals_used=self._dependency_impact_lifecycle_signals(snapshot),
                        derived_from=[
                            "TwinTopologySnapshot.lifecycle_readiness_summary",
                            "TwinTopologySnapshot.lifecycle_readiness_hints",
                        ],
                    ),
                    limitations=PLANNING_INTELLIGENCE_READINESS_LIMITATIONS
                    + TOPOLOGY_READINESS_LIMITATIONS,
                ),
                self._planning_intelligence_readiness_item(
                    intelligence_area=TwinPlanningIntelligenceReadinessArea.relationship_coverage_explanation,
                    posture=ready_posture,
                    statement=(
                        "Relationship coverage explanation is ready for read-only explanation from topology relationship coverage metadata."
                    ),
                    available_evidence=[
                        f"relationship_edges:{snapshot.relationship_coverage_summary.relationship_edge_count}",
                        f"dependency_hook_edges:{snapshot.relationship_coverage_summary.dependency_hook_edge_count}",
                        f"missing_relationship_indicators:{len(snapshot.missing_relationship_indicators)}",
                        "TwinTopologySnapshot.relationship_coverage_summary",
                    ],
                    missing_prerequisites=[
                        "resolved_relationship_inputs_for_missing_indicators",
                        "field_verified_relationships",
                    ],
                    unsafe_assumptions=[
                        "Treating relationship coverage as complete or field-verified would be unsafe.",
                    ],
                    confidence_posture="ready_for_read_only_explanation_with_relationship_limits",
                    basis=self._planning_intelligence_readiness_basis(
                        topology_edge_ids=[edge.edge_id for edge in snapshot.edges],
                        missing_relationship_indicator_refs=[
                            self._missing_relationship_ref(indicator)
                            for indicator in snapshot.missing_relationship_indicators
                        ],
                        derived_from=[
                            "TwinTopologySnapshot.relationship_coverage_summary",
                            "TwinTopologySnapshot.missing_relationship_indicators",
                        ],
                    ),
                    limitations=PLANNING_INTELLIGENCE_READINESS_LIMITATIONS
                    + TOPOLOGY_RELATIONSHIP_COVERAGE_LIMITATIONS,
                ),
                self._planning_intelligence_readiness_item(
                    intelligence_area=TwinPlanningIntelligenceReadinessArea.dependency_impact_readiness,
                    posture=ready_posture,
                    statement=(
                        "Dependency impact readiness is ready for read-only explanation from the Phase 3A dependency impact readiness view."
                    ),
                    available_evidence=[
                        f"impact_posture_items:{len(impact_view.dependency_impact_posture)}",
                        f"missing_inputs:{len(impact_view.missing_inputs)}",
                        f"provenance_gap_posture_items:{len(impact_view.provenance_gap_posture)}",
                        "TwinDependencyImpactReadinessView",
                    ],
                    missing_prerequisites=[
                        "impact_propagation_engine",
                        "recalculation_engine",
                        "invalidation_engine",
                    ],
                    unsafe_assumptions=[
                        "Treating dependency impact readiness as impact propagation would be unsafe.",
                    ],
                    confidence_posture="ready_for_read_only_explanation_with_impact_limits",
                    basis=self._planning_intelligence_readiness_basis(
                        source_section_keys=impact_view.source_basis.source_section_keys,
                        topology_node_ids=impact_view.source_basis.topology_node_ids,
                        topology_edge_ids=impact_view.source_basis.topology_edge_ids,
                        lifecycle_readiness_signals_used=impact_view.source_basis.lifecycle_readiness_signals_used,
                        dependency_warning_refs=impact_view.source_basis.dependency_warning_refs,
                        provenance_gap_refs=impact_view.source_basis.provenance_gap_refs,
                        missing_readiness_indicator_refs=impact_view.source_basis.missing_readiness_indicator_refs,
                        missing_relationship_indicator_refs=impact_view.source_basis.missing_relationship_indicator_refs,
                        derived_from=impact_view.source_basis.derived_from
                        + ["TwinDependencyImpactReadinessView.source_basis"],
                    ),
                    limitations=PLANNING_INTELLIGENCE_READINESS_LIMITATIONS
                    + impact_view.limitations,
                ),
                self._planning_intelligence_readiness_item(
                    intelligence_area=TwinPlanningIntelligenceReadinessArea.dependency_reasoning,
                    posture=ready_posture,
                    statement=(
                        "Dependency reasoning is ready for read-only explanation from the Phase 3B dependency reasoning view."
                    ),
                    available_evidence=[
                        f"reasoning_items:{len(reasoning_view.dependency_reasoning_items)}",
                        f"reasoning_types:{len(reasoning_view.dependency_type_summary)}",
                        "TwinDependencyReasoningView",
                    ],
                    missing_prerequisites=[
                        "scenario_intelligence",
                        "impact_propagation",
                        "recommendation_boundary",
                    ],
                    unsafe_assumptions=[
                        "Treating dependency reasoning as recommendations or scenario intelligence would be unsafe.",
                    ],
                    confidence_posture="ready_for_read_only_explanation_with_reasoning_limits",
                    basis=self._planning_intelligence_readiness_basis(
                        source_section_keys=reasoning_view.source_basis.source_section_keys,
                        topology_node_ids=reasoning_view.source_basis.topology_node_ids,
                        topology_edge_ids=reasoning_view.source_basis.topology_edge_ids,
                        lifecycle_readiness_signals_used=reasoning_view.source_basis.lifecycle_readiness_signals_used,
                        dependency_warning_refs=reasoning_view.source_basis.dependency_warning_refs,
                        provenance_gap_refs=reasoning_view.source_basis.provenance_gap_refs,
                        missing_readiness_indicator_refs=reasoning_view.source_basis.missing_readiness_indicator_refs,
                        missing_relationship_indicator_refs=reasoning_view.source_basis.missing_relationship_indicator_refs,
                        derived_from=reasoning_view.source_basis.derived_from
                        + ["TwinDependencyReasoningView.source_basis"],
                    ),
                    limitations=PLANNING_INTELLIGENCE_READINESS_LIMITATIONS
                    + reasoning_view.limitations,
                ),
                self._planning_intelligence_readiness_item(
                    intelligence_area=TwinPlanningIntelligenceReadinessArea.provenance_gap_reporting,
                    posture=ready_posture,
                    statement=(
                        "Provenance gap reporting is ready for read-only explanation from existing provenance gap metadata."
                    ),
                    available_evidence=[
                        f"provenance_gap_refs:{len(impact_view.source_basis.provenance_gap_refs)}",
                        "TwinPlanningContextRecord.provenance_gaps",
                        "TwinDependencyImpactReadinessView.provenance_gap_posture",
                    ],
                    missing_prerequisites=[
                        "field_level_provenance_completion",
                        "verification_workflow",
                    ],
                    unsafe_assumptions=[
                        "Treating provenance presence as verification would be unsafe.",
                    ],
                    confidence_posture="ready_for_read_only_explanation_not_verification",
                    basis=self._planning_intelligence_readiness_basis(
                        provenance_gap_refs=impact_view.source_basis.provenance_gap_refs,
                        derived_from=[
                            "TwinPlanningContextRecord.provenance_gaps",
                            "TwinDependencyImpactReadinessView.provenance_gap_posture",
                        ],
                    ),
                    limitations=PLANNING_INTELLIGENCE_READINESS_LIMITATIONS
                    + PROVENANCE_GAP_LIMITATIONS,
                ),
                self._planning_intelligence_readiness_item(
                    intelligence_area=TwinPlanningIntelligenceReadinessArea.permission_readiness_metadata,
                    posture=ready_posture,
                    statement=(
                        "Permission readiness metadata is ready for read-only explanation, but permission enforcement remains not implemented."
                    ),
                    available_evidence=[
                        f"records_with_permission_readiness:{permission_record_count}",
                        "TwinPlanningContext.permission_readiness",
                        "TwinPlanningContextRecord.permission_readiness",
                    ],
                    missing_prerequisites=[
                        "active_permission_grants",
                        "active_consent_artifacts",
                        "permission_enforcement",
                    ],
                    unsafe_assumptions=[
                        "Treating permission readiness metadata as permission enforcement would be unsafe.",
                    ],
                    confidence_posture="ready_for_read_only_explanation_metadata_only",
                    basis=self._planning_intelligence_readiness_basis(
                        source_section_keys=[section.section_key for section in context.sections],
                        derived_from=[
                            "TwinPlanningContext.permission_readiness",
                            "TwinPlanningContextRecord.permission_readiness",
                        ],
                    ),
                    limitations=PLANNING_INTELLIGENCE_READINESS_LIMITATIONS
                    + PERMISSION_READINESS_LIMITATIONS,
                ),
            ],
            key=self._planning_intelligence_item_sort_key,
        )

    def _planning_intelligence_blocked_item(
        self,
        *,
        intelligence_area: TwinPlanningIntelligenceReadinessArea,
        statement: str,
        missing_prerequisites: List[str],
        unsafe_assumptions: List[str],
        source_basis: TwinDependencyImpactStatementBasis,
    ) -> TwinPlanningIntelligenceReadinessItem:
        return self._planning_intelligence_readiness_item(
            intelligence_area=intelligence_area,
            posture="blocked/deferred",
            statement=statement,
            available_evidence=[
                "Phase 3C approved boundary",
                "current deferred capability list",
            ],
            missing_prerequisites=missing_prerequisites,
            unsafe_assumptions=unsafe_assumptions,
            confidence_posture="blocked_deferred_not_implemented",
            basis=self._planning_intelligence_readiness_basis(
                source_section_keys=source_basis.source_section_keys,
                topology_node_ids=source_basis.topology_node_ids,
                topology_edge_ids=source_basis.topology_edge_ids,
                lifecycle_readiness_signals_used=source_basis.lifecycle_readiness_signals_used,
                dependency_warning_refs=source_basis.dependency_warning_refs,
                provenance_gap_refs=source_basis.provenance_gap_refs,
                missing_readiness_indicator_refs=source_basis.missing_readiness_indicator_refs,
                missing_relationship_indicator_refs=source_basis.missing_relationship_indicator_refs,
                derived_from=source_basis.derived_from
                + ["Phase3C.planning_intelligence_readiness_deferred_boundaries"],
            ),
            limitations=PLANNING_INTELLIGENCE_READINESS_LIMITATIONS,
        )

    def _planning_intelligence_blocked_items(
        self, source_basis: TwinDependencyImpactStatementBasis
    ) -> List[TwinPlanningIntelligenceReadinessItem]:
        blocked_specs = [
            (
                TwinPlanningIntelligenceReadinessArea.scenario_intelligence,
                "Scenario intelligence is blocked/deferred; scenario references are continuity context only.",
                ["approved_scenario_intelligence_boundary", "scenario_comparison_engine"],
                ["Treating saved scenario references as scenario intelligence would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.impact_propagation,
                "Impact propagation is blocked/deferred; no propagation engine exists.",
                ["impact_propagation_engine", "affected_output_registry"],
                ["Treating dependency explanation as propagated impact state would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.stale_state_persistence,
                "Stale-state persistence is blocked/deferred; no stale-state records are created.",
                ["stale_state_model", "persistence_contract"],
                ["Treating request-time limitations as persisted stale state would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.recalculation,
                "Recalculation is blocked/deferred; no recalculation engine runs.",
                ["recalculation_engine", "approved_calculation_trigger_contract"],
                ["Treating readiness inventory as recalculation would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.invalidation,
                "Invalidation is blocked/deferred; no invalidation engine runs.",
                ["invalidation_engine", "approved_invalidation_state_contract"],
                ["Treating missing prerequisites as invalidated outputs would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.simulation,
                "Simulation is blocked/deferred; no scenario simulation or infrastructure simulation runs.",
                ["approved_simulation_engine", "source_backed_simulation_inputs"],
                ["Treating readiness evidence as simulated outcome data would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.what_if_analysis,
                "What-if analysis is blocked/deferred; no modeled change analysis runs.",
                ["approved_what_if_engine", "change_model_contract"],
                ["Treating blocked/deferred readiness as what-if analysis would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.optimization,
                "Optimization is blocked/deferred; no optimization logic runs.",
                ["approved_optimization_boundary"],
                ["Treating readiness posture as optimized choice would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.ranking,
                "Ranking is blocked/deferred; no ranking logic runs.",
                ["approved_ranking_boundary"],
                ["Treating deterministic ordering as ranking would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.economic_reasoning,
                "Economic reasoning is blocked/deferred; no pricing, savings, payback, incentive, or financial reasoning runs.",
                ["source_backed_economic_inputs", "approved_economic_reasoning_boundary"],
                ["Treating readiness posture as financial guidance would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.utility_readiness_logic,
                "Utility readiness logic is blocked/deferred; no utility approval, interconnection, program eligibility, or grid-edge readiness logic runs.",
                ["approved_utility_readiness_boundary", "source_backed_utility_inputs"],
                ["Treating planning context as utility readiness would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.survivability_recharge_modeling,
                "Survivability/recharge modeling is blocked/deferred; no endurance or recharge model runs.",
                ["approved_survivability_model", "approved_recharge_model"],
                ["Treating planning evidence as survivability or recharge results would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.compatibility_engine,
                "Compatibility engine behavior is blocked/deferred; no product or system compatibility engine runs.",
                ["approved_compatibility_engine", "verified_product_compatibility_sources"],
                ["Treating dependency relationships as compatibility approval would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.recommendation_or_proposal_generation,
                "Recommendations and proposal generation are blocked/deferred; this view does not choose or propose actions.",
                ["approved_recommendation_boundary", "approved_proposal_generation_boundary"],
                ["Treating readiness inventory as a recommendation or proposal would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.exports,
                "Exports are blocked/deferred; no scoped export package is generated.",
                ["approved_export_contract", "permissioned_view_enforcement"],
                ["Treating this API view as an export would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.auth_rbac_abac,
                "Auth/RBAC/ABAC is blocked/deferred; no authorization or access-control enforcement exists.",
                ["approved_auth_architecture", "approved_rbac_abac_model"],
                ["Treating metadata scopes as access control would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.permission_enforcement,
                "Permission enforcement is blocked/deferred; permission readiness remains metadata only.",
                ["active_permission_grants", "active_consent_artifacts", "permission_enforcement_layer"],
                ["Treating permission readiness as permission enforcement would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.marketplace,
                "Marketplace behavior is blocked/deferred; no registry or marketplace surface exists.",
                ["approved_marketplace_boundary", "ownership_transfer_boundary"],
                ["Treating planning intelligence readiness as marketplace readiness would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.operational_behavior,
                "Operational behavior is blocked/deferred; no device, dispatch, DERMS, telemetry, or control behavior exists.",
                ["operational_control_boundary", "telemetry_governance", "device_identity"],
                ["Treating planning intelligence readiness as operational readiness would be unsafe."],
            ),
        ]
        return sorted(
            [
                self._planning_intelligence_blocked_item(
                    intelligence_area=area,
                    statement=statement,
                    missing_prerequisites=missing_prerequisites,
                    unsafe_assumptions=unsafe_assumptions,
                    source_basis=source_basis,
                )
                for area, statement, missing_prerequisites, unsafe_assumptions in blocked_specs
            ],
            key=self._planning_intelligence_item_sort_key,
        )

    def build_planning_intelligence_readiness_view(
        self, db, home_id: str
    ) -> Optional[TwinPlanningIntelligenceReadinessView]:
        context = self.build(db, home_id)
        if context is None:
            return None
        snapshot = self.build_topology_snapshot_view(db, home_id)
        if snapshot is None:
            return None
        impact_view = self.build_dependency_impact_readiness_view(db, home_id)
        if impact_view is None:
            return None
        reasoning_view = self.build_dependency_reasoning_view(db, home_id)
        if reasoning_view is None:
            return None

        section_records = self._all_context_records_with_sections(context)
        warning_refs, provenance_gap_refs, _sections_by_entity = self._dependency_impact_record_refs(
            section_records
        )
        missing_readiness_refs = [
            self._missing_readiness_ref(indicator)
            for indicator in snapshot.missing_readiness_indicators
            if not indicator.present
        ]
        missing_relationship_refs = [
            self._missing_relationship_ref(indicator)
            for indicator in snapshot.missing_relationship_indicators
        ]
        lifecycle_signals = self._dependency_impact_lifecycle_signals(snapshot)
        source_basis = self._planning_intelligence_readiness_basis(
            source_section_keys=[section.section_key for section in context.sections],
            topology_node_ids=[node.node_id for node in snapshot.nodes],
            topology_edge_ids=[edge.edge_id for edge in snapshot.edges],
            lifecycle_readiness_signals_used=lifecycle_signals,
            dependency_warning_refs=warning_refs,
            provenance_gap_refs=provenance_gap_refs,
            missing_readiness_indicator_refs=missing_readiness_refs,
            missing_relationship_indicator_refs=missing_relationship_refs,
            derived_from=[
                "TwinPlanningContext",
                "TwinTopologySnapshot",
                "TwinDependencyImpactReadinessView",
                "TwinDependencyReasoningView",
            ],
        )

        ready_items = self._planning_intelligence_ready_items(
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            source_basis=source_basis,
        )
        blocked_items = self._planning_intelligence_blocked_items(source_basis)
        all_items = ready_items + blocked_items
        missing_prerequisites = self._sorted_unique(
            prerequisite
            for item in all_items
            for prerequisite in item.missing_prerequisites
        )
        available_evidence = self._sorted_unique(
            evidence
            for item in ready_items
            for evidence in item.available_evidence
        )
        unsafe_assumptions = self._sorted_unique(
            assumption
            for item in all_items
            for assumption in item.unsafe_assumptions
        )
        confidence_item = self._planning_intelligence_readiness_item(
            intelligence_area=TwinPlanningIntelligenceReadinessArea.provenance_gap_reporting,
            posture="ready for read-only explanation",
            statement=(
                "Overall planning intelligence readiness confidence is limited to read-only explanation because blocked/deferred areas are not implemented."
            ),
            available_evidence=[
                f"ready_areas:{len(ready_items)}",
                f"blocked_deferred_areas:{len(blocked_items)}",
                "TwinPlanningContext",
                "TwinTopologySnapshot",
                "TwinDependencyImpactReadinessView",
                "TwinDependencyReasoningView",
            ],
            missing_prerequisites=missing_prerequisites,
            unsafe_assumptions=[
                "Treating ready for read-only explanation as executable intelligence would be unsafe.",
            ],
            confidence_posture="read_only_explanation_ready_blocked_deferred_execution",
            basis=source_basis,
            limitations=PLANNING_INTELLIGENCE_READINESS_LIMITATIONS,
        )

        return TwinPlanningIntelligenceReadinessView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 3C planning intelligence readiness inventory built request-time from "
                "TwinPlanningContext, topology snapshot, dependency impact readiness, and dependency reasoning; "
                "not a reasoning engine, recommendation layer, scenario simulation, export, permission enforcement, "
                "graph engine, canonical Twin runtime model, or operational behavior."
            ),
            source_basis=source_basis,
            readiness_scope=TwinPlanningIntelligenceReadinessScope(
                limitations=PLANNING_INTELLIGENCE_READINESS_LIMITATIONS,
            ),
            ready_areas=ready_items,
            blocked_deferred_areas=blocked_items,
            provenance_permission_basis=[
                item
                for item in ready_items
                if item.intelligence_area
                in {
                    TwinPlanningIntelligenceReadinessArea.provenance_gap_reporting,
                    TwinPlanningIntelligenceReadinessArea.permission_readiness_metadata,
                }
            ],
            missing_prerequisites=missing_prerequisites,
            available_evidence=available_evidence,
            unsafe_assumptions=unsafe_assumptions,
            deferred_reasoning_boundaries=sorted(
                PLANNING_INTELLIGENCE_READINESS_DEFERRED_BOUNDARIES
            ),
            confidence_posture=[confidence_item],
            limitations=PLANNING_INTELLIGENCE_READINESS_LIMITATIONS,
            compatibility_note=(
                "Existing TwinPlanningContext, topology snapshot, dependency impact readiness, dependency reasoning, "
                "AI grounding, runtime projection, and current /api/* contracts remain unchanged; this is an additive Phase 3C readiness inventory."
            ),
        )

    def _runtime_role(self, role: TwinRuntimeParticipantRole) -> Optional[TwinRuntimeParticipantRole]:
        try:
            return TwinRuntimeParticipantRole(role)
        except ValueError:
            return None

    def _runtime_view_context(self, role: TwinRuntimeParticipantRole) -> TwinRuntimeViewContext:
        return TwinRuntimeViewContext(
            view_name=f"{role.value}_runtime_projection",
            role=role,
            visibility_scope=RUNTIME_VIEW_SCOPE[role],
            purpose=RUNTIME_VIEW_PURPOSE[role],
            minimum_necessary=role == TwinRuntimeParticipantRole.contractor,
        )

    def _runtime_view_permission_readiness(
        self, role: TwinRuntimeParticipantRole
    ) -> TwinPlanningPermissionReadiness:
        if role == TwinRuntimeParticipantRole.homeowner:
            return self._permission_readiness(
                permission_required=False,
                audience=role.value,
                purpose=RUNTIME_VIEW_PURPOSE[role],
                minimum_necessary=False,
                view_name=f"{role.value}_runtime_projection",
                visibility_scope=RUNTIME_VIEW_SCOPE[role],
                visibility_limitations=[
                    "Homeowner projection is owner-facing planning context, not a permission grant or export package.",
                    "It may include private planning fields that are excluded from external scoped projections.",
                ],
            )
        if role == TwinRuntimeParticipantRole.contractor:
            return self._permission_readiness(
                permission_required=True,
                audience=role.value,
                purpose=RUNTIME_VIEW_PURPOSE[role],
                minimum_necessary=True,
                view_name=f"{role.value}_runtime_projection",
                visibility_scope=RUNTIME_VIEW_SCOPE[role],
                visibility_limitations=[
                    "Contractor projection is a minimized planning/scoping view only.",
                    "It is not a contractor portal, authorization grant, bid packet, stamped design, or export package.",
                    "Homeowner account scaffolding, private notes, full address fields, and internal unknown markers are excluded.",
                ],
            )
        return self._permission_readiness(
            permission_required=True,
            audience=role.value,
            purpose=RUNTIME_VIEW_PURPOSE[role],
            minimum_necessary=False,
            view_name=f"{role.value}_runtime_projection",
            visibility_scope=RUNTIME_VIEW_SCOPE[role],
            visibility_limitations=[
                "Internal/system projection supports runtime governance inspection only.",
                "Internal visibility metadata does not create tenant isolation, audit policy, or authorization enforcement.",
            ],
        )

    def _runtime_record_permission_readiness(
        self, role: TwinRuntimeParticipantRole, record: TwinPlanningContextRecord
    ) -> TwinPlanningPermissionReadiness:
        limitations = [
            "Projection record visibility metadata does not authorize sharing or export.",
            "Future permission enforcement may further narrow fields, source documents, and derived outputs.",
        ]
        if role == TwinRuntimeParticipantRole.contractor:
            limitations.append("Contractor-scoped records remain planning-only and do not imply professional review.")
        if record.classification in {
            TwinPlanningRecordClassification.derived_output,
            TwinPlanningRecordClassification.advisory_output,
        }:
            limitations.append("Derived and advisory outputs remain downstream of recorded planning context.")
        return self._permission_readiness(
            permission_required=role != TwinRuntimeParticipantRole.homeowner,
            audience=role.value,
            purpose=f"{record.entity_type}_{RUNTIME_VIEW_PURPOSE[role]}",
            minimum_necessary=role == TwinRuntimeParticipantRole.contractor,
            view_name=f"{role.value}_runtime_projection:{record.entity_type}",
            visibility_scope=RUNTIME_VIEW_SCOPE[role],
            visibility_limitations=limitations,
        )

    def _runtime_view_fields(
        self, role: TwinRuntimeParticipantRole, record: TwinPlanningContextRecord
    ) -> Dict[str, object]:
        if role in {
            TwinRuntimeParticipantRole.homeowner,
            TwinRuntimeParticipantRole.internal_system,
        }:
            return dict(record.record)
        allowed_fields = RUNTIME_FIELD_ALLOWLIST.get(role, {}).get(record.entity_type, set())
        return {
            field: value
            for field, value in record.record.items()
            if field in allowed_fields
        }

    def _runtime_data_classification(
        self, role: TwinRuntimeParticipantRole, record: TwinPlanningContextRecord
    ) -> DataClassification:
        if role == TwinRuntimeParticipantRole.contractor:
            return DataClassification.contractor_scoped
        if role == TwinRuntimeParticipantRole.internal_system:
            return DataClassification.internal_governance
        return record.data_classification

    def _runtime_contribution_identity(
        self, role: TwinRuntimeParticipantRole, record: TwinPlanningContextRecord
    ) -> TwinRuntimeContributionIdentity:
        contributor_ref = None
        if role in {
            TwinRuntimeParticipantRole.homeowner,
            TwinRuntimeParticipantRole.internal_system,
        }:
            contributor_ref = record.record.get("account_id")

        if record.rule_keys or record.classification in {
            TwinPlanningRecordClassification.derived_output,
            TwinPlanningRecordClassification.advisory_output,
        }:
            contributor_type = "deterministic_rule_or_advisory_runtime"
        elif record.source_document_ids:
            contributor_type = "source_document"
        elif record.data_origin:
            contributor_type = record.data_origin.value if hasattr(record.data_origin, "value") else record.data_origin
        else:
            contributor_type = "unknown"

        return TwinRuntimeContributionIdentity(
            contributor_type=contributor_type,
            contributor_ref=contributor_ref,
            data_origin=record.data_origin,
            source_document_ids=record.source_document_ids,
            limitations=[
                "Contributor identity is limited to available runtime provenance and data_origin metadata.",
                "Absence of contributor_ref does not mean the value is owner-authorized, verified, or externally shareable.",
            ],
        )

    def _runtime_projection_record(
        self,
        *,
        role: TwinRuntimeParticipantRole,
        section_key: str,
        record: TwinPlanningContextRecord,
    ) -> Optional[TwinRuntimeProjectionRecord]:
        fields = self._runtime_view_fields(role, record)
        if (
            role != TwinRuntimeParticipantRole.internal_system
            and not fields
            and not record.rule_keys
            and not record.dependency_hooks
        ):
            return None

        return TwinRuntimeProjectionRecord(
            section_key=section_key,
            entity_type=record.entity_type,
            entity_id=record.entity_id,
            label=record.label,
            visibility_scope=RUNTIME_VIEW_SCOPE[role],
            classification=record.classification,
            authority_layer=record.authority_layer,
            data_classification=self._runtime_data_classification(role, record),
            data_origin=record.data_origin,
            fields=fields,
            provenance_summary=record.provenance_summary,
            source_document_ids=record.source_document_ids,
            contributor_identity=self._runtime_contribution_identity(role, record),
            rule_keys=record.rule_keys,
            dependency_hooks=record.dependency_hooks,
            missing_fields=record.missing_fields,
            provenance_gaps=record.provenance_gaps,
            dependency_awareness=record.dependency_awareness,
            change_impact_hints=record.change_impact_hints,
            planning_dependency_warnings=record.planning_dependency_warnings,
            permission_readiness=self._runtime_record_permission_readiness(role, record),
            limitations=record.limitations,
        )

    def build_runtime_projection_view(
        self, db, home_id: str, role: TwinRuntimeParticipantRole
    ) -> Optional[TwinRuntimeProjectionView]:
        role = self._runtime_role(role)
        if role not in RUNTIME_VIEW_SECTION_ALLOWLIST:
            return None

        context = self.build(db, home_id)
        if context is None:
            return None

        projection_records: List[TwinRuntimeProjectionRecord] = []
        allowed_sections = RUNTIME_VIEW_SECTION_ALLOWLIST[role]
        all_sections = {section.section_key for section in context.sections}

        for section in context.sections:
            if section.section_key not in allowed_sections:
                continue
            for record in section.records:
                projection_record = self._runtime_projection_record(
                    role=role,
                    section_key=section.section_key,
                    record=record,
                )
                if projection_record is not None:
                    projection_records.append(projection_record)

        classification_counts = Counter(record.classification for record in projection_records)
        classification_summary = {
            classification.value: classification_counts.get(classification, 0)
            for classification in TwinPlanningRecordClassification
        }

        provenance_gap_map = {}
        for record in projection_records:
            for gap in record.provenance_gaps:
                key = (
                    gap.gap_type.value,
                    gap.entity_type,
                    gap.entity_id,
                    gap.field_name,
                    gap.reason,
                )
                provenance_gap_map.setdefault(key, gap)
        provenance_gaps = sorted(
            provenance_gap_map.values(),
            key=lambda gap: (
                gap.gap_type.value,
                gap.entity_type,
                gap.entity_id or "",
                gap.field_name or "",
                gap.reason,
            ),
        )

        dependency_hooks = [
            hook
            for record in projection_records
            for hook in record.dependency_hooks
        ]

        included_sections = sorted({record.section_key for record in projection_records})
        return TwinRuntimeProjectionView(
            home_id=home_id,
            participant=TwinRuntimeParticipant(
                role=role,
                relationship_to_home=(
                    "owner_or_owner_authorized_household"
                    if role == TwinRuntimeParticipantRole.homeowner
                    else role.value
                ),
            ),
            view_context=self._runtime_view_context(role),
            implementation_boundary=(
                "Read-only role-aware projection over one existing home_id-anchored Twin Planning Context; "
                "not a separate portal, product codebase, export, permission grant, or canonical ResidentialEnergyTwin model."
            ),
            included_sections=included_sections,
            excluded_sections=sorted(all_sections - set(included_sections)),
            projection_records=projection_records,
            classification_summary=classification_summary,
            provenance_gaps=provenance_gaps,
            dependency_hooks=dependency_hooks,
            dependency_awareness_summary=self._dependency_awareness_summary(projection_records),
            permission_readiness=self._runtime_view_permission_readiness(role),
            limitations=[
                "No twin_id is created or inferred.",
                "The canonical source remains the home_id-anchored Twin Planning Context composed from existing planner records.",
                "This projection does not enforce permissions, authenticate actors, create grants, create exports, or transfer ownership.",
                "This projection does not imply engineering approval, utility approval, safety approval, procurement readiness, or operational control.",
                "Pilot, partner, registry, marketplace, utility sharing, and external partner API behavior remain deferred.",
            ],
            compatibility_note=(
                "Existing TwinPlanningContext, AI grounding, and current /api/* contracts remain unchanged; "
                "this is an additive runtime projection view."
            ),
        )

    def build_ai_design_grounding_view(
        self, db, home_id: str, design_id: Optional[str] = None
    ) -> Optional[AIDesignGroundingView]:
        context = self.build(db, home_id)
        if context is None:
            return None

        if design_id:
            design_found = any(
                record.entity_id == design_id
                for section in context.sections
                if section.section_key == "designs"
                for record in section.records
            )
            if not design_found:
                return None

        related_ids = self._ai_grounding_related_ids(context, design_id)
        grounding_records: List[AIDesignGroundingRecord] = []
        for section in context.sections:
            for record in section.records:
                if not self._include_ai_grounding_record(
                    section_key=section.section_key,
                    record=record,
                    design_id=design_id,
                    related_ids=related_ids,
                ):
                    continue
                grounding_record = self._ai_grounding_record(section.section_key, record)
                if grounding_record.fields or grounding_record.rule_keys or grounding_record.dependency_hooks:
                    grounding_records.append(grounding_record)

        included_sections = sorted({record.section_key for record in grounding_records})
        all_sections = {section.section_key for section in context.sections}
        excluded_sections = sorted(all_sections - set(included_sections))

        provenance_gap_map = {}
        for record in grounding_records:
            for gap in record.provenance_gaps:
                key = (
                    gap.gap_type.value,
                    gap.entity_type,
                    gap.entity_id,
                    gap.field_name,
                    gap.reason,
                )
                provenance_gap_map.setdefault(key, gap)
        provenance_gaps = sorted(
            provenance_gap_map.values(),
            key=lambda gap: (
                gap.gap_type.value,
                gap.entity_type,
                gap.entity_id or "",
                gap.field_name or "",
                gap.reason,
            ),
        )

        dependency_hooks = [
            hook
            for record in grounding_records
            for hook in record.dependency_hooks
        ]

        return AIDesignGroundingView(
            home_id=home_id,
            target_design_id=design_id,
            implementation_boundary=(
                "Read-only minimized AI/design grounding projection over existing Twin Planning Context records; "
                "not the full Twin Planning Context and not a canonical ResidentialEnergyTwin runtime model."
            ),
            included_sections=included_sections,
            excluded_sections=excluded_sections,
            grounding_records=grounding_records,
            provenance_gaps=provenance_gaps,
            dependency_hooks=dependency_hooks,
            dependency_awareness_summary=self._dependency_awareness_summary(grounding_records),
            permission_readiness=self._ai_view_permission_readiness(),
            limitations=[
                "No twin_id is created or inferred.",
                "This AI grounding view is a minimized planning-only projection and is not complete Twin authority.",
                "No permission enforcement, export authorization, utility authority, operational control, or field verification is implemented.",
                "AI may use this view to ground explanations and recommendations, but it must not create canonical facts.",
                "Advisor output remains derived or advisory planning intelligence and is not persisted as Twin truth.",
                "This view does not imply completeness, correctness, safety approval, utility approval, or engineering approval.",
            ],
            compatibility_note=(
                "Existing TwinPlanningContext payloads and current /api/* contracts remain unchanged; "
                "this is an additive AI grounding view."
            ),
        )

    def build(self, db, home_id: str) -> Optional[TwinPlanningContext]:
        home = repository.get_home_by_id(db, home_id)
        if home is None:
            return None

        buildings = repository.list_buildings(db, home_id=home_id)
        panels = repository.list_panels(db, home_id=home_id)
        loads = repository.list_loads(db, home_id=home_id)
        locations = repository.list_equipment_locations(db, home_id=home_id)
        designs = [design for design in repository.list_designs(db) if design.home_id == home_id]
        pathways = repository.list_estimated_pathways(db, home_id=home_id)
        scenarios = [scenario for scenario in repository.list_scenario_models(db) if scenario.home_id == home_id]

        design_equipment = [equipment for design in designs for equipment in design.equipment]
        products_by_id = {
            equipment.product.id: equipment.product
            for equipment in design_equipment
            if equipment.product is not None
        }
        designs_by_id = {design.id: design for design in designs}
        locations_by_id = {location.id: location for location in locations}
        scenarios_by_id = {scenario.id: scenario for scenario in scenarios}
        panels_by_building: Dict[str, List[object]] = {}
        loads_by_building: Dict[str, List[object]] = {}
        for panel in panels:
            panels_by_building.setdefault(panel.building_id, []).append(panel)
        for load in loads:
            loads_by_building.setdefault(load.building_id, []).append(load)
        scenario_revisions = [revision for scenario in scenarios for revision in scenario.revisions]

        sections: List[TwinPlanningContextSection] = []
        unknown_records: List[TwinPlanningContextRecord] = []
        provenance_gaps: List[str] = []

        def add_unknown_if_needed(record: TwinPlanningContextRecord):
            if self._has_provenance(record.provenance_summary):
                return
            gap = f"{record.entity_type}:{record.entity_id} has no linked field-level provenance summary."
            provenance_gaps.append(gap)
            unknown_records.append(
                self._unknown_record(
                    record.entity_type,
                    record.entity_id or "unknown",
                    f"Missing provenance for {record.label}",
                    gap,
                )
            )

        premise_records = [
            self._record(
                db=db,
                entity_type="home",
                entity_id=home.id,
                label=home.name,
                data_origin=home.data_origin,
                record_snapshot=self._record_snapshot(
                    home,
                    [
                        "id",
                        "account_id",
                        "name",
                        "address_line_1",
                        "address_line_2",
                        "city",
                        "state",
                        "postal_code",
                        "country",
                        "utility_provider",
                        "service_size",
                        "notes",
                        "data_origin",
                        "created_at",
                        "updated_at",
                    ],
                ),
                limitations=[
                    "Home records are premise planning context, not legal title, utility account authority, or verified service status.",
                ],
            )
        ]
        for record in premise_records:
            add_unknown_if_needed(record)
        sections.append(TwinPlanningContextSection(section_key="premise", label="Premise", records=premise_records))

        structure_records = [
            self._record(
                db=db,
                entity_type="building",
                entity_id=building.id,
                label=building.name,
                data_origin=building.data_origin,
                record_snapshot=self._record_snapshot(
                    building,
                    [
                        "id",
                        "home_id",
                        "name",
                        "type",
                        "approximate_distance_from_main_service",
                        "notes",
                        "data_origin",
                        "created_at",
                        "updated_at",
                    ],
                ),
                limitations=["Building distances and notes remain planning assumptions unless source-backed."],
            )
            for building in buildings
        ]
        for record in structure_records:
            add_unknown_if_needed(record)
        sections.append(
            TwinPlanningContextSection(section_key="structures", label="Structures", records=structure_records)
        )

        panel_records = []
        for panel in panels:
            panel_hooks, panel_hints, panel_warnings = self._panel_load_dependency_metadata(panel, loads_by_building)
            panel_records.append(
                self._record(
                    db=db,
                    entity_type="electrical_panel",
                    entity_id=panel.id,
                    label=f"{panel.panel_type} {panel.amperage}A",
                    data_origin=panel.data_origin,
                    record_snapshot=self._record_snapshot(
                        panel,
                        [
                            "id",
                            "home_id",
                            "building_id",
                            "panel_type",
                            "amperage",
                            "busbar_rating",
                            "breaker_spaces_total",
                            "breaker_spaces_available",
                            "indoor_outdoor",
                            "notes",
                            "data_origin",
                            "created_at",
                            "updated_at",
                        ],
                    ),
                    dependency_hooks=panel_hooks,
                    change_impact_hints=panel_hints,
                    planning_dependency_warnings=panel_warnings,
                    limitations=[
                        "Panel records are electrical planning context, not NEC compliance, AHJ approval, or engineering approval.",
                    ],
                )
            )
        for record in panel_records:
            add_unknown_if_needed(record)
        sections.append(
            TwinPlanningContextSection(
                section_key="electrical_infrastructure",
                label="Electrical Infrastructure",
                records=panel_records,
            )
        )

        load_records = []
        for load in loads:
            load_hooks, load_hints, load_warnings = self._load_panel_dependency_metadata(load, panels_by_building)
            load_records.append(
                self._record(
                    db=db,
                    entity_type="load",
                    entity_id=load.id,
                    label=load.name,
                    data_origin=load.data_origin,
                    record_snapshot=self._record_snapshot(
                        load,
                        [
                            "id",
                            "home_id",
                            "building_id",
                            "name",
                            "category",
                            "running_watts",
                            "surge_watts",
                            "estimated_daily_hours",
                            "backup_priority",
                            "phase_type",
                            "notes",
                            "data_origin",
                            "created_at",
                            "updated_at",
                        ],
                    ),
                    dependency_hooks=load_hooks,
                    change_impact_hints=load_hints,
                    planning_dependency_warnings=load_warnings,
                    limitations=[
                        "Load records are modeled planning loads, not verified circuit inventory, load study, or telemetry.",
                    ],
                )
            )
        for record in load_records:
            add_unknown_if_needed(record)
        sections.append(TwinPlanningContextSection(section_key="loads", label="Loads", records=load_records))

        location_records = [
            self._record(
                db=db,
                entity_type="equipment_location",
                entity_id=location.id,
                label=location.name,
                data_origin=location.data_origin,
                record_snapshot=self._record_snapshot(
                    location,
                    [
                        "id",
                        "home_id",
                        "building_id",
                        "name",
                        "location_type",
                        "approximate_coordinates",
                        "notes",
                        "data_origin",
                        "created_at",
                        "updated_at",
                    ],
                ),
                limitations=["Equipment locations are planning/siting context, not field-verified placement."],
            )
            for location in locations
        ]
        for record in location_records:
            add_unknown_if_needed(record)
        sections.append(
            TwinPlanningContextSection(
                section_key="equipment_locations", label="Equipment Locations", records=location_records
            )
        )

        product_records = [
            self._record(
                db=db,
                entity_type="equipment_product",
                entity_id=product.id,
                label=f"{product.manufacturer} {product.model}",
                data_origin=product.data_origin,
                record_snapshot=self._record_snapshot(
                    product,
                    [
                        "id",
                        "manufacturer",
                        "model",
                        "product_type",
                        "ecosystem",
                        "specs",
                        "documentation_url",
                        "notes",
                        "data_origin",
                        "created_at",
                        "updated_at",
                    ],
                ),
                limitations=[
                    "Product records are reference planning data and do not guarantee compatibility, procurement, warranty, or availability.",
                ],
            )
            for product in products_by_id.values()
        ]
        for record in product_records:
            add_unknown_if_needed(record)
        sections.append(
            TwinPlanningContextSection(section_key="equipment_products", label="Equipment Products", records=product_records)
        )

        design_records = [
            self._record(
                db=db,
                entity_type="energy_system_design",
                entity_id=design.id,
                label=design.name,
                data_origin=design.data_origin,
                record_snapshot=self._record_snapshot(
                    design,
                    [
                        "id",
                        "home_id",
                        "name",
                        "design_goal",
                        "architecture_type",
                        "status",
                        "notes",
                        "data_origin",
                        "created_at",
                        "updated_at",
                    ],
                ),
                limitations=["Design records are planning intent, not final electrical design or installation approval."],
            )
            for design in designs
        ]
        for record in design_records:
            add_unknown_if_needed(record)
        sections.append(TwinPlanningContextSection(section_key="designs", label="Designs", records=design_records))

        design_equipment_records = []
        for equipment in design_equipment:
            equipment_hooks, equipment_hints, equipment_warnings = self._design_equipment_dependency_metadata(
                equipment,
                designs_by_id,
                products_by_id,
                locations_by_id,
            )
            design_equipment_records.append(
                self._record(
                    db=db,
                    entity_type="design_equipment",
                    entity_id=equipment.id,
                    label=equipment.role_in_system,
                    data_origin=equipment.data_origin,
                    record_snapshot=self._record_snapshot(
                        equipment,
                        [
                            "id",
                            "design_id",
                            "product_id",
                            "quantity",
                            "location_id",
                            "role_in_system",
                            "notes",
                            "data_origin",
                            "created_at",
                            "updated_at",
                        ],
                    ),
                    dependency_hooks=equipment_hooks,
                    change_impact_hints=equipment_hints,
                    planning_dependency_warnings=equipment_warnings,
                    limitations=[
                        "Design equipment assignments are design composition, not procurement or installed equipment status."
                    ],
                )
            )
        for record in design_equipment_records:
            add_unknown_if_needed(record)
        sections.append(
            TwinPlanningContextSection(section_key="design_equipment", label="Design Equipment", records=design_equipment_records)
        )

        pathway_records = [
            self._record(
                db=db,
                entity_type="estimated_pathway",
                entity_id=pathway.id,
                label=pathway.name,
                data_origin=pathway.data_origin,
                record_snapshot=self._record_snapshot(
                    pathway,
                    [
                        "id",
                        "home_id",
                        "design_id",
                        "name",
                        "description",
                        "lifecycle_stage",
                        "source_location",
                        "destination_location",
                        "estimated_distance_ft",
                        "route_type",
                        "route_difficulty",
                        "visibility_level",
                        "confidence_level",
                        "upfront_cost_placeholder",
                        "estimated_monthly_savings_placeholder",
                        "resilience_score",
                        "notes",
                        "data_origin",
                        "created_at",
                        "updated_at",
                    ],
                ),
                limitations=["Pathways are route planning assumptions, not surveyed construction routes."],
            )
            for pathway in pathways
        ]
        for record in pathway_records:
            add_unknown_if_needed(record)
        sections.append(TwinPlanningContextSection(section_key="pathways", label="Pathways", records=pathway_records))

        scenario_records = []
        for scenario in scenarios:
            scenario_hooks, scenario_hints, scenario_warnings = self._scenario_dependency_metadata(
                scenario,
                designs_by_id,
            )
            scenario_records.append(
                self._record(
                    db=db,
                    entity_type="scenario",
                    entity_id=scenario.id,
                    label=scenario.name,
                    data_origin=scenario.data_origin,
                    record_snapshot=self._record_snapshot(
                        scenario,
                        [
                            "id",
                            "home_id",
                            "name",
                            "description",
                            "linked_design_id",
                            "upfront_cost_placeholder",
                            "future_expansion_score",
                            "install_complexity_score",
                            "backup_capability_score",
                            "notes",
                            "data_origin",
                            "created_at",
                            "updated_at",
                        ],
                    ),
                    dependency_hooks=scenario_hooks,
                    change_impact_hints=scenario_hints,
                    planning_dependency_warnings=scenario_warnings,
                    limitations=[
                        "Scenario records are planning futures; placeholder scores and costs are not bids, quotes, or financial guarantees.",
                    ],
                )
            )
        for record in scenario_records:
            add_unknown_if_needed(record)
        sections.append(TwinPlanningContextSection(section_key="scenarios", label="Scenarios", records=scenario_records))

        revision_records = []
        for revision in scenario_revisions:
            revision_hooks, revision_hints, revision_warnings = self._scenario_revision_dependency_metadata(
                revision,
                scenarios_by_id,
                designs_by_id,
            )
            revision_records.append(
                self._record(
                    db=db,
                    entity_type="scenario_revision",
                    entity_id=revision.id,
                    label=revision.revision_label,
                    data_origin=revision.data_origin,
                    authority_layer=AuthorityLayer.historical,
                    default_classification=TwinPlanningRecordClassification.derived_output,
                    record_snapshot=self._record_snapshot(
                        revision,
                        [
                            "id",
                            "scenario_id",
                            "parent_revision_id",
                            "revision_number",
                            "revision_label",
                            "revision_status",
                            "linked_design_id",
                            "design_goal_snapshot",
                            "design_status_snapshot",
                            "recommended_profile_snapshot",
                            "planning_summary",
                            "planning_state_snapshot",
                            "data_origin",
                            "created_at",
                            "updated_at",
                        ],
                    ),
                    dependency_hooks=revision_hooks,
                    change_impact_hints=revision_hints,
                    planning_dependency_warnings=revision_warnings,
                    extra_reasons=["Scenario revisions are compact historical planning snapshots."],
                    limitations=[
                        "Scenario revisions preserve compact planning-state framing, not full advisor replay.",
                    ],
                )
            )
        sections.append(
            TwinPlanningContextSection(
                section_key="scenario_revisions", label="Scenario Revisions", records=revision_records
            )
        )

        advisor_records: List[TwinPlanningContextRecord] = []
        for design in designs:
            advisor = design_advisor_service.explain(db, design.id)
            recommendation = advisor["recommendation_profiles"]
            hooks = self._dependency_hooks_from_recommendation(design.id, recommendation)
            advisor_records.append(
                self._advisor_record(design_id=design.id, recommendation=recommendation, dependency_hooks=hooks)
            )
            advisor_records.append(self._advisor_note_record(design.id, advisor["advisor_note"]))

        sections.append(
            TwinPlanningContextSection(
                section_key="derived_intelligence",
                label="Derived And Advisory Intelligence",
                records=advisor_records,
                notes=[
                    "Derived intelligence is regenerated read-only from current planner records.",
                    "No derived output is promoted into canonical facts by this planning context.",
                ],
            )
        )

        sections.append(
            TwinPlanningContextSection(
                section_key="unknowns",
                label="Unknowns And Provenance Gaps",
                records=unknown_records,
                notes=["Unknown records mark missing provenance or missing planning evidence."],
            )
        )

        self._attach_dependency_awareness(sections)
        self._attach_permission_readiness(sections)

        all_records = [record for section in sections for record in section.records]
        context_dependency_hooks = [
            hook
            for record in all_records
            for hook in record.dependency_hooks
        ]

        classification_counts = Counter(
            record.classification for record in all_records
        )
        classification_summary = {
            classification.value: classification_counts.get(classification, 0)
            for classification in TwinPlanningRecordClassification
        }
        typed_provenance_gap_map = {}
        for section in sections:
            for record in section.records:
                for gap in record.provenance_gaps:
                    key = (
                        gap.gap_type.value,
                        gap.entity_type,
                        gap.entity_id,
                        gap.field_name,
                        gap.reason,
                    )
                    typed_provenance_gap_map.setdefault(key, gap)
        typed_provenance_gaps = sorted(
            typed_provenance_gap_map.values(),
            key=lambda gap: (
                gap.gap_type.value,
                gap.entity_type,
                gap.entity_id or "",
                gap.field_name or "",
                gap.reason,
            ),
        )

        return TwinPlanningContext(
            context_id=f"home-planning-context-{home_id}",
            home_id=home_id,
            context_label=f"{home.name} Twin Planning Context",
            implementation_boundary=(
                "Read-only home_id-anchored planning context over existing planner records; "
                "not a canonical ResidentialEnergyTwin runtime model."
            ),
            sections=sections,
            classification_summary=classification_summary,
            provenance_gaps=sorted(set(provenance_gaps)),
            typed_provenance_gaps=typed_provenance_gaps,
            continuity_gaps=[
                "Scenario revisions preserve compact planning-state snapshots, not full historical advisor replay.",
                "No general lifecycle event log, stale-state marker, supersession model, or permission continuity model exists yet.",
            ],
            dependency_hooks=context_dependency_hooks,
            dependency_awareness_summary=self._dependency_awareness_summary(
                all_records
            ),
            permission_readiness=self._context_permission_readiness(),
            limitations=[
                "No twin_id is created or inferred.",
                "This endpoint is not a canonical ResidentialEnergyTwin API.",
                "No permission enforcement, scoped export, utility authority, operational control, or field verification is implemented.",
                "Existing /api/* contracts remain unchanged and are not reclassified as Twin APIs.",
            ],
        )


twin_planning_context_service = TwinPlanningContextService()

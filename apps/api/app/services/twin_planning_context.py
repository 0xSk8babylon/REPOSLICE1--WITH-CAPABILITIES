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

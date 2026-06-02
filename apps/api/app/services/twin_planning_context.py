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
    TwinPlanningContext,
    TwinPlanningContextRecord,
    TwinPlanningContextSection,
    TwinPlanningDependencyAwareness,
    TwinPlanningDependencyAwarenessLabel,
    TwinPlanningDependencyHook,
    TwinPlanningPermissionReadiness,
    TwinPlanningProvenanceGap,
    TwinPlanningProvenanceGapType,
    TwinPlanningRecordClassification,
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

REGROUNDING_GAP_TYPES = {
    TwinPlanningProvenanceGapType.missing_source.value,
    TwinPlanningProvenanceGapType.partial_source.value,
    TwinPlanningProvenanceGapType.placeholder_without_source.value,
    TwinPlanningProvenanceGapType.unknown_origin.value,
}

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
        if rule_keys or dependency_hooks or source_document_ids:
            return []
        return [
            self._gap(
                gap_type=TwinPlanningProvenanceGapType.derived_without_lineage,
                entity_type=entity_type,
                entity_id=entity_id,
                reason=(
                    "Derived or advisory output has no persisted rule key, source document, "
                    "or dependency hook lineage in this context."
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
    ) -> TwinPlanningPermissionReadiness:
        return TwinPlanningPermissionReadiness(
            permission_required=permission_required,
            permission_not_enforced=True,
            audience=audience,
            purpose=purpose,
            minimum_necessary=minimum_necessary,
            visibility_limitations=PERMISSION_READINESS_LIMITATIONS + (visibility_limitations or []),
            deferred_capabilities=DEFERRED_PERMISSION_CAPABILITIES,
        )

    def _context_permission_readiness(self) -> TwinPlanningPermissionReadiness:
        return self._permission_readiness(
            permission_required=False,
            audience="homeowner_planning",
            purpose="owner_planning_context",
            minimum_necessary=False,
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
                visibility_limitations=[
                    "Unknown markers are internal governance context and should not be exposed as facts.",
                ],
            )
        return self._permission_readiness(
            permission_required=True,
            audience="homeowner_planning",
            purpose=f"{section_key}_planning_context",
            minimum_necessary=False,
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
            permission_readiness=self._ai_record_permission_readiness(record),
            limitations=record.limitations,
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

        if design_id:
            dependency_hooks = [
                hook for hook in context.dependency_hooks if f"Design {design_id}:" in hook.note
            ]
        else:
            dependency_hooks = context.dependency_hooks

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
        scenario_revisions = [revision for scenario in scenarios for revision in scenario.revisions]

        sections: List[TwinPlanningContextSection] = []
        unknown_records: List[TwinPlanningContextRecord] = []
        provenance_gaps: List[str] = []
        dependency_hooks: List[TwinPlanningDependencyHook] = []

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

        panel_records = [
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
                limitations=[
                    "Panel records are electrical planning context, not NEC compliance, AHJ approval, or engineering approval.",
                ],
            )
            for panel in panels
        ]
        for record in panel_records:
            add_unknown_if_needed(record)
        sections.append(
            TwinPlanningContextSection(
                section_key="electrical_infrastructure",
                label="Electrical Infrastructure",
                records=panel_records,
            )
        )

        load_records = [
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
                limitations=[
                    "Load records are modeled planning loads, not verified circuit inventory, load study, or telemetry.",
                ],
            )
            for load in loads
        ]
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

        design_equipment_records = [
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
                limitations=["Design equipment assignments are design composition, not procurement or installed equipment status."],
            )
            for equipment in design_equipment
        ]
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

        scenario_records = [
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
                limitations=[
                    "Scenario records are planning futures; placeholder scores and costs are not bids, quotes, or financial guarantees.",
                ],
            )
            for scenario in scenarios
        ]
        for record in scenario_records:
            add_unknown_if_needed(record)
        sections.append(TwinPlanningContextSection(section_key="scenarios", label="Scenarios", records=scenario_records))

        revision_records = [
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
                extra_reasons=["Scenario revisions are compact historical planning snapshots."],
                limitations=[
                    "Scenario revisions preserve compact planning-state framing, not full advisor replay.",
                ],
            )
            for revision in scenario_revisions
        ]
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
            dependency_hooks.extend(hooks)
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

        classification_counts = Counter(
            record.classification for section in sections for record in section.records
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
            dependency_hooks=dependency_hooks,
            dependency_awareness_summary=self._dependency_awareness_summary(
                [record for section in sections for record in section.records]
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

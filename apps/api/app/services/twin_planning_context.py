from collections import Counter
from typing import Dict, Iterable, List, Optional

from app.core.repository import repository
from app.core.types import AuthorityLayer, DataClassification, DataOrigin
from app.design_advisor.schemas import ResilienceRecommendation
from app.provenance.schemas import ProvenanceSummary
from app.services.design_advisor import design_advisor_service
from app.services.provenance import provenance_service
from app.twin_planning_context.schemas import (
    TwinPlanningContext,
    TwinPlanningContextRecord,
    TwinPlanningContextSection,
    TwinPlanningDependencyHook,
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


class TwinPlanningContextService:
    def _record_snapshot(self, record, fields: Iterable[str]) -> Dict[str, object]:
        return {field: getattr(record, field, None) for field in fields}

    def _entity_summary(self, db, entity_type: str, entity_id: Optional[str]) -> Optional[ProvenanceSummary]:
        if not entity_id:
            return None
        return provenance_service.summarize_entity(db, entity_type, entity_id)

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
        summary = self._entity_summary(db, provenance_entity_type or entity_type, entity_id)
        placeholder_fields = self._placeholder_fields(record_snapshot)
        classification = self._classify_record(
            record_snapshot=record_snapshot,
            data_origin=data_origin,
            provenance_summary=summary,
            default_classification=default_classification,
        )
        return TwinPlanningContextRecord(
            entity_type=entity_type,
            entity_id=entity_id,
            label=label,
            classification=classification,
            authority_layer=authority_layer,
            data_origin=data_origin,
            record=record_snapshot,
            provenance_summary=summary,
            source_document_ids=summary.source_document_ids if summary else [],
            rule_keys=rule_keys or [],
            dependency_hooks=dependency_hooks or [],
            classification_reasons=self._classification_reasons(
                classification=classification,
                data_origin=data_origin,
                provenance_summary=summary,
                placeholder_fields=placeholder_fields,
                extra_reasons=extra_reasons,
            ),
            missing_fields=placeholder_fields + (summary.unverified_fields if summary else []),
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

        classification_counts = Counter(
            record.classification for section in sections for record in section.records
        )
        classification_summary = {
            classification.value: classification_counts.get(classification, 0)
            for classification in TwinPlanningRecordClassification
        }

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
            continuity_gaps=[
                "Scenario revisions preserve compact planning-state snapshots, not full historical advisor replay.",
                "No general lifecycle event log, stale-state marker, supersession model, or permission continuity model exists yet.",
            ],
            dependency_hooks=dependency_hooks,
            limitations=[
                "No twin_id is created or inferred.",
                "This endpoint is not a canonical ResidentialEnergyTwin API.",
                "No permission enforcement, scoped export, utility authority, operational control, or field verification is implemented.",
                "Existing /api/* contracts remain unchanged and are not reclassified as Twin APIs.",
            ],
        )


twin_planning_context_service = TwinPlanningContextService()

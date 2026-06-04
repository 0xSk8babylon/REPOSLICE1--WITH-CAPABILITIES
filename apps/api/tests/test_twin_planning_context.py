import os
import unittest
from pathlib import Path

os.environ.setdefault("DATA_DIR", "/tmp/residential-energy-planner-tests")
os.environ.setdefault("DATABASE_FILE", "twin_planning_context_test.sqlite3")

from sqlalchemy.orm import Session  # noqa: E402

from app.core.database import database_path, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.seed.runtime import reset_and_reseed  # noqa: E402
from app.services.twin_planning_context import twin_planning_context_service  # noqa: E402


class TwinPlanningContextServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db_path = Path(database_path())
        db_path.parent.mkdir(parents=True, exist_ok=True)
        if db_path.exists():
            db_path.unlink()
        reset_and_reseed()

    def setUp(self):
        reset_and_reseed()

    def _context(self):
        with Session(engine) as db:
            return twin_planning_context_service.build(db, "home_001")

    def _ai_view(self, design_id=None):
        with Session(engine) as db:
            return twin_planning_context_service.build_ai_design_grounding_view(
                db, "home_001", design_id=design_id
            )

    def _runtime_view(self, role):
        with Session(engine) as db:
            return twin_planning_context_service.build_runtime_projection_view(db, "home_001", role=role)

    def _topology_snapshot(self):
        with Session(engine) as db:
            return twin_planning_context_service.build_topology_snapshot_view(db, "home_001")

    def _dependency_impact_view(self):
        with Session(engine) as db:
            return twin_planning_context_service.build_dependency_impact_readiness_view(db, "home_001")

    def _dependency_reasoning_view(self):
        with Session(engine) as db:
            return twin_planning_context_service.build_dependency_reasoning_view(db, "home_001")

    def _planning_intelligence_readiness_view(self):
        with Session(engine) as db:
            return twin_planning_context_service.build_planning_intelligence_readiness_view(db, "home_001")

    def _advisory_context_assembly_view(self):
        with Session(engine) as db:
            return twin_planning_context_service.build_advisory_context_assembly_view(db, "home_001")

    def _constraint_risk_reasoning_view(self):
        with Session(engine) as db:
            return twin_planning_context_service.build_constraint_risk_reasoning_view(db, "home_001")

    def _scenario_comparison_readiness_view(self):
        with Session(engine) as db:
            return twin_planning_context_service.build_scenario_comparison_readiness_view(db, "home_001")

    def _pre_recommendation_advisory_view(self):
        with Session(engine) as db:
            return twin_planning_context_service.build_pre_recommendation_advisory_view(db, "home_001")

    def _recommendation_eligibility_readiness_view(self):
        with Session(engine) as db:
            return twin_planning_context_service.build_recommendation_eligibility_readiness_view(db, "home_001")

    def test_context_composes_existing_home_scoped_records_without_twin_identity(self):
        context = self._context()

        self.assertIsNotNone(context)
        self.assertEqual("home_001", context.home_id)
        self.assertEqual("home_id", context.anchor_type)
        self.assertFalse(hasattr(context, "twin_id"))
        self.assertIn("not a canonical ResidentialEnergyTwin", context.implementation_boundary)

        section_map = {section.section_key: section for section in context.sections}
        for section_key in [
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
        ]:
            self.assertIn(section_key, section_map)

        self.assertGreaterEqual(len(section_map["designs"].records), 2)
        self.assertGreaterEqual(len(section_map["loads"].records), 3)
        self.assertGreaterEqual(len(section_map["scenario_revisions"].records), 2)

    def test_context_classifies_records_and_surfaces_provenance_gaps(self):
        context = self._context()
        summary = context.classification_summary

        self.assertGreater(summary["recorded_fact"], 0)
        self.assertGreater(summary["source_backed_fact"], 0)
        self.assertGreater(summary["derived_output"], 0)
        self.assertGreater(summary["advisory_output"], 0)
        self.assertGreater(summary["placeholder"], 0)
        self.assertGreater(summary["unknown"], 0)
        self.assertTrue(context.provenance_gaps)

        load_records = {
            record.entity_id: record for section in context.sections for record in section.records if record.entity_type == "load"
        }
        self.assertEqual("source_backed_fact", load_records["load_001"].classification.value)
        self.assertIn("source_doc_user_load_entry", load_records["load_001"].source_document_ids)

        scenario_section = next(section for section in context.sections if section.section_key == "scenarios")
        scenario_records = {record.entity_id: record for record in scenario_section.records}
        self.assertEqual("placeholder", scenario_records["scenario_001"].classification.value)
        self.assertIn("upfront_cost_placeholder", scenario_records["scenario_001"].missing_fields)

    def test_context_reports_typed_provenance_gaps_without_replacing_compatibility_gaps(self):
        context = self._context()

        self.assertTrue(context.provenance_gaps)
        self.assertTrue(context.typed_provenance_gaps)

        gap_types = {gap.gap_type.value for gap in context.typed_provenance_gaps}
        for gap_type in [
            "missing_source",
            "partial_source",
            "derived_without_lineage",
            "placeholder_without_source",
            "unknown_origin",
        ]:
            self.assertIn(gap_type, gap_types)

    def test_record_level_typed_provenance_gaps_distinguish_partial_and_placeholder_sources(self):
        context = self._context()
        records = {
            (record.entity_type, record.entity_id): record
            for section in context.sections
            for record in section.records
        }

        load_gap_types = {gap.gap_type.value for gap in records[("load", "load_001")].provenance_gaps}
        self.assertIn("partial_source", load_gap_types)
        self.assertNotIn("missing_source", load_gap_types)

        scenario_section = next(section for section in context.sections if section.section_key == "scenarios")
        scenario_record = next(record for record in scenario_section.records if record.entity_id == "scenario_001")
        scenario_gaps = scenario_record.provenance_gaps
        placeholder_fields = {
            gap.field_name for gap in scenario_gaps if gap.gap_type.value == "placeholder_without_source"
        }
        self.assertIn("upfront_cost_placeholder", placeholder_fields)

        premise_section = next(section for section in context.sections if section.section_key == "premise")
        home_record = next(record for record in premise_section.records if record.entity_id == "home_001")
        home_gap_types = {gap.gap_type.value for gap in home_record.provenance_gaps}
        self.assertIn("missing_source", home_gap_types)
        self.assertIn("unknown_origin", home_gap_types)

    def test_derived_outputs_report_lineage_gaps_without_becoming_twin_truth(self):
        context = self._context()
        records = [
            record
            for section in context.sections
            for record in section.records
        ]

        revision_records = [record for record in records if record.entity_type == "scenario_revision"]
        self.assertTrue(
            any(
                gap.gap_type.value == "derived_without_lineage"
                for record in revision_records
                for gap in record.provenance_gaps
            )
        )

        advisor_notes = [record for record in records if record.entity_type == "advisor_note"]
        self.assertTrue(
            any(
                gap.gap_type.value == "derived_without_lineage"
                for record in advisor_notes
                for gap in record.provenance_gaps
            )
        )
        self.assertTrue(
            all("Advisory text cannot create canonical facts" in record.limitations[0] for record in advisor_notes)
        )

    def test_context_includes_advisor_dependency_hooks_as_derived_planning_intelligence(self):
        context = self._context()
        derived_records = [
            record
            for section in context.sections
            if section.section_key == "derived_intelligence"
            for record in section.records
        ]
        advisor_records = [
            record for record in derived_records if record.entity_type == "advisor_recommendation_summary"
        ]
        advisory_notes = [record for record in derived_records if record.entity_type == "advisor_note"]

        self.assertGreaterEqual(len(advisor_records), 2)
        self.assertGreaterEqual(len(advisory_notes), 2)
        self.assertTrue(context.dependency_hooks)
        self.assertTrue(
            any("recommendation.system_reasoning_graph_v1" in hook.rule_keys for hook in context.dependency_hooks)
        )
        self.assertEqual("derived_output", advisor_records[0].classification.value)
        self.assertEqual("advisory_output", advisory_notes[0].classification.value)

    def test_context_reports_descriptive_dependency_awareness_labels(self):
        context = self._context()
        summary = context.dependency_awareness_summary

        for label in [
            "current",
            "snapshot_bound",
            "needs_recalculation",
            "needs_regrounding",
            "needs_review",
            "stale_unknown",
        ]:
            self.assertIn(label, summary)
            self.assertGreater(summary[label], 0)

        revision_section = next(section for section in context.sections if section.section_key == "scenario_revisions")
        self.assertGreater(revision_section.dependency_awareness_summary["snapshot_bound"], 0)
        self.assertGreater(revision_section.dependency_awareness_summary["needs_recalculation"], 0)

        revision_record = revision_section.records[0]
        revision_labels = {item.label.value for item in revision_record.dependency_awareness}
        self.assertIn("snapshot_bound", revision_labels)
        self.assertIn("needs_recalculation", revision_labels)

    def test_dependency_awareness_interacts_with_provenance_and_advisor_outputs(self):
        context = self._context()
        records = [
            record
            for section in context.sections
            for record in section.records
        ]

        load_record = next(record for record in records if record.entity_type == "load" and record.entity_id == "load_001")
        load_labels = {item.label.value for item in load_record.dependency_awareness}
        self.assertIn("needs_regrounding", load_labels)
        self.assertTrue(
            any("partial_source" in item.source_gap_types for item in load_record.dependency_awareness)
        )

        advisor_summary = next(record for record in records if record.entity_type == "advisor_recommendation_summary")
        advisor_summary_labels = {item.label.value for item in advisor_summary.dependency_awareness}
        self.assertIn("current", advisor_summary_labels)
        self.assertEqual("derived_output", advisor_summary.classification.value)

        advisor_note = next(record for record in records if record.entity_type == "advisor_note")
        advisor_note_labels = {item.label.value for item in advisor_note.dependency_awareness}
        self.assertIn("needs_review", advisor_note_labels)
        self.assertIn("stale_unknown", advisor_note_labels)
        self.assertEqual("advisory_output", advisor_note.classification.value)

    def test_context_surfaces_phase_2b_relationship_dependency_foundations(self):
        context = self._context()
        section_map = {section.section_key: section for section in context.sections}

        def section_record(section_key, entity_type, entity_id):
            return next(
                record
                for record in section_map[section_key].records
                if record.entity_type == entity_type and record.entity_id == entity_id
            )

        load = section_record("loads", "load", "load_001")
        load_hook = next(
            hook
            for hook in load.dependency_hooks
            if hook.target_entity_type == "electrical_panel" and hook.target_entity_id == "panel_main"
        )
        self.assertEqual("shared_building_id_planning_context", load_hook.relationship)
        self.assertIn("twin_dependency.load_panel_shared_building_v1", load_hook.rule_keys)
        self.assertIn("planning context only", load_hook.note)
        self.assertTrue(load.change_impact_hints)
        self.assertIn(
            "load_panel_relationship_is_building_level_only",
            {warning.warning_type for warning in load.planning_dependency_warnings},
        )

        detached_load = section_record("loads", "load", "load_003")
        self.assertIn(
            "load_has_no_same_building_panel",
            {warning.warning_type for warning in detached_load.planning_dependency_warnings},
        )

        design_equipment = section_record("design_equipment", "design_equipment", "design_001_equipment_1")
        equipment_targets = {
            (hook.target_entity_type, hook.target_entity_id)
            for hook in design_equipment.dependency_hooks
        }
        self.assertIn(("energy_system_design", "design_001"), equipment_targets)
        self.assertIn(("equipment_product", "product_generic_panel"), equipment_targets)
        self.assertIn(("equipment_location", "location_roof_south"), equipment_targets)
        self.assertTrue(design_equipment.change_impact_hints)
        self.assertIn(
            "equipment_location_is_planning_only",
            {warning.warning_type for warning in design_equipment.planning_dependency_warnings},
        )

        scenario = section_record("scenarios", "scenario", "scenario_001")
        scenario_targets = {
            (hook.target_entity_type, hook.target_entity_id)
            for hook in scenario.dependency_hooks
        }
        self.assertIn(("energy_system_design", "design_001"), scenario_targets)
        self.assertIn(
            "scenario_reference_is_not_live_invalidation",
            {warning.warning_type for warning in scenario.planning_dependency_warnings},
        )

        revision = section_record("scenario_revisions", "scenario_revision", "scenario_001_rev_001")
        revision_targets = {
            (hook.target_entity_type, hook.target_entity_id)
            for hook in revision.dependency_hooks
        }
        self.assertIn(("scenario", "scenario_001"), revision_targets)
        self.assertIn(("energy_system_design", "design_001"), revision_targets)
        self.assertIn(
            "revision_snapshot_is_not_live_replay",
            {warning.warning_type for warning in revision.planning_dependency_warnings},
        )

        context_rule_keys = {
            rule_key
            for hook in context.dependency_hooks
            for rule_key in hook.rule_keys
        }
        self.assertIn("twin_dependency.load_panel_shared_building_v1", context_rule_keys)
        self.assertIn("twin_dependency.equipment_system_reference_v1", context_rule_keys)
        self.assertIn("twin_dependency.scenario_reference_v1", context_rule_keys)

    def test_context_reports_permission_readiness_without_enforcement(self):
        context = self._context()
        readiness = context.permission_readiness

        self.assertIsNotNone(readiness)
        self.assertFalse(readiness.permission_required)
        self.assertTrue(readiness.permission_not_enforced)
        self.assertEqual("homeowner_planning", readiness.audience)
        self.assertEqual("owner_planning_context", readiness.purpose)
        self.assertFalse(readiness.minimum_necessary)
        self.assertIn("permission_grants", readiness.deferred_capabilities)
        self.assertIn("rbac_abac", readiness.deferred_capabilities)
        self.assertIn("operational_control", readiness.deferred_capabilities)
        self.assertTrue(any("does not enforce access" in note for note in readiness.visibility_limitations))

        section = next(section for section in context.sections if section.section_key == "loads")
        self.assertTrue(section.permission_readiness.permission_required)
        self.assertTrue(section.permission_readiness.permission_not_enforced)

        load_record = next(record for record in section.records if record.entity_id == "load_001")
        self.assertTrue(load_record.permission_readiness.permission_required)
        self.assertTrue(load_record.permission_readiness.permission_not_enforced)
        self.assertEqual("homeowner_planning", load_record.permission_readiness.audience)

    def test_permission_foundations_are_placeholders_without_enforcement(self):
        context = self._context()
        section = next(section for section in context.sections if section.section_key == "loads")
        record = next(record for record in section.records if record.entity_id == "load_001")

        readiness_items = [
            context.permission_readiness,
            section.permission_readiness,
            record.permission_readiness,
        ]
        for readiness in readiness_items:
            self.assertIsNotNone(readiness)
            self.assertTrue(readiness.permission_not_enforced)
            self.assertIsNotNone(readiness.audience_readiness)
            self.assertIsNotNone(readiness.purpose_readiness)
            self.assertIsNotNone(readiness.duration_readiness)
            self.assertIsNotNone(readiness.revocation_state_readiness)
            self.assertIsNotNone(readiness.consent_artifact_placeholder)
            self.assertIsNotNone(readiness.homeowner_authority)
            self.assertIsNotNone(readiness.view_permission_alignment)
            self.assertTrue(readiness.audience_readiness.readiness_only)
            self.assertTrue(readiness.purpose_readiness.readiness_only)
            self.assertTrue(readiness.duration_readiness.readiness_only)
            self.assertTrue(readiness.revocation_state_readiness.readiness_only)
            self.assertTrue(readiness.consent_artifact_placeholder.consent_artifact_placeholder_only)
            self.assertFalse(readiness.audience_readiness.active_permission_grant_present)
            self.assertFalse(readiness.purpose_readiness.active_permission_grant_present)
            self.assertFalse(readiness.duration_readiness.active_permission_grant_present)
            self.assertFalse(readiness.revocation_state_readiness.active_permission_grant_present)
            self.assertFalse(readiness.consent_artifact_placeholder.active_consent_present)
            self.assertFalse(readiness.homeowner_authority.active_permission_grant_present)
            self.assertFalse(readiness.view_permission_alignment.active_permission_grant_present)
            self.assertFalse(readiness.view_permission_alignment.active_consent_present)
            self.assertIsNone(readiness.consent_artifact_placeholder.consent_artifact_id)
            self.assertEqual("not_enforced", readiness.view_permission_alignment.permission_enforcement)
            self.assertIn("permission_grants", readiness.deferred_capabilities)
            self.assertIn("auth", readiness.deferred_capabilities)
            self.assertIn("rbac_abac", readiness.deferred_capabilities)
            self.assertIn("scoped_exports", readiness.deferred_capabilities)
            self.assertIn("operational_control", readiness.deferred_capabilities)
            self.assertNotIn("permission_grant_id", readiness.dict())
            self.assertTrue(
                any("readiness metadata only" in note for note in readiness.audience_readiness.limitations)
            )

        self.assertEqual("homeowner", context.permission_readiness.audience_readiness.audience.value)
        self.assertEqual(
            "owner_planning_context",
            context.permission_readiness.purpose_readiness.purpose.value,
        )
        self.assertEqual(
            "not_active_placeholder",
            context.permission_readiness.duration_readiness.duration.value,
        )
        self.assertEqual(
            "not_applicable_no_active_permission",
            context.permission_readiness.revocation_state_readiness.revocation_state.value,
        )
        self.assertTrue(context.permission_readiness.homeowner_authority.homeowner_authority_preserved)
        self.assertTrue(
            context.permission_readiness.homeowner_authority.permission_grant_required_for_external_sharing
        )

    def test_api_route_is_api_prefixed_and_read_only_additive(self):
        paths = {getattr(route, "path", None) for route in app.routes}

        self.assertIn("/api/twin-planning-context/homes/{home_id}", paths)
        self.assertNotIn("/twin-planning-context/homes/{home_id}", paths)

        context = self._context()
        payload = context.dict()
        self.assertEqual("home_001", payload["home_id"])
        self.assertNotIn("twin_id", payload)
        self.assertIn("typed_provenance_gaps", payload)
        self.assertIn("No twin_id is created or inferred.", payload["limitations"])

    def test_ai_design_grounding_view_is_additive_and_minimized(self):
        paths = {getattr(route, "path", None) for route in app.routes}
        self.assertIn("/api/twin-planning-context/homes/{home_id}/views/ai-design-grounding", paths)

        full_context = self._context()
        premise_record = next(
            record
            for section in full_context.sections
            if section.section_key == "premise"
            for record in section.records
        )
        self.assertIn("account_id", premise_record.record)
        self.assertIn("address_line_1", premise_record.record)

        view = self._ai_view("design_001")
        self.assertIsNotNone(view)
        self.assertEqual("ai_design_grounding", view.view_name)
        self.assertEqual("home_001", view.home_id)
        self.assertEqual("home_id", view.anchor_type)
        self.assertEqual("design_001", view.target_design_id)
        self.assertEqual("not_enforced", view.permission_enforcement)
        self.assertNotIn("twin_id", view.dict())
        self.assertIn("unknowns", view.excluded_sections)

        exposed_field_names = {
            field_name
            for record in view.grounding_records
            for field_name in record.fields.keys()
        }
        self.assertNotIn("account_id", exposed_field_names)
        self.assertNotIn("address_line_1", exposed_field_names)
        self.assertNotIn("address_line_2", exposed_field_names)

    def test_ai_design_grounding_view_filters_to_target_design(self):
        view = self._ai_view("design_001")
        records = view.grounding_records

        design_records = [record for record in records if record.entity_type == "energy_system_design"]
        self.assertEqual(["design_001"], [record.entity_id for record in design_records])

        design_equipment_records = [record for record in records if record.entity_type == "design_equipment"]
        self.assertTrue(design_equipment_records)
        self.assertTrue(all(record.fields["design_id"] == "design_001" for record in design_equipment_records))

        scenario_records = [record for record in records if record.entity_type == "scenario"]
        self.assertTrue(scenario_records)
        self.assertTrue(all(record.fields["linked_design_id"] == "design_001" for record in scenario_records))

        derived_records = [
            record
            for record in records
            if record.entity_type in {"advisor_recommendation_summary", "advisor_note"}
        ]
        self.assertTrue(derived_records)
        self.assertTrue(all(record.fields["design_id"] == "design_001" for record in derived_records))

    def test_ai_design_grounding_view_preserves_lineage_and_limitations(self):
        view = self._ai_view("design_001")
        records = view.grounding_records

        self.assertTrue(view.provenance_gaps)
        self.assertTrue(view.dependency_hooks)
        self.assertTrue(any("recommendation.system_reasoning_graph_v1" in hook.rule_keys for hook in view.dependency_hooks))
        self.assertIn("Advisor output remains derived or advisory", " ".join(view.limitations))

        load_record = next(record for record in records if record.entity_type == "load" and record.entity_id == "load_001")
        self.assertIsNotNone(load_record.provenance_summary)
        self.assertIn("source_doc_user_load_entry", load_record.source_document_ids)
        self.assertTrue(load_record.provenance_gaps)

        scenario_record = next(record for record in records if record.entity_type == "scenario")
        self.assertIn("upfront_cost_placeholder", scenario_record.missing_fields)
        self.assertTrue(
            any(gap.gap_type.value == "placeholder_without_source" for gap in scenario_record.provenance_gaps)
        )

        advisor_summary = next(record for record in records if record.entity_type == "advisor_recommendation_summary")
        self.assertEqual("derived_output", advisor_summary.classification.value)
        self.assertTrue(advisor_summary.rule_keys)
        self.assertTrue(advisor_summary.dependency_hooks)

        advisor_note = next(record for record in records if record.entity_type == "advisor_note")
        self.assertEqual("advisory_output", advisor_note.classification.value)
        self.assertIn("Advisory text cannot create canonical facts", advisor_note.limitations[0])

    def test_ai_design_grounding_view_carries_filtered_dependency_awareness_summary(self):
        view = self._ai_view("design_001")

        self.assertTrue(view.dependency_awareness_summary)
        self.assertGreater(view.dependency_awareness_summary["current"], 0)
        self.assertGreater(view.dependency_awareness_summary["needs_regrounding"], 0)
        self.assertGreater(view.dependency_awareness_summary["snapshot_bound"], 0)

        design_ids = {
            record.fields.get("design_id")
            for record in view.grounding_records
            if "design_id" in record.fields
        }
        self.assertIn("design_001", design_ids)
        self.assertNotIn("design_002", design_ids)

        advisor_records = [
            record
            for record in view.grounding_records
            if record.entity_type in {"advisor_recommendation_summary", "advisor_note"}
        ]
        self.assertTrue(advisor_records)
        self.assertTrue(all(record.dependency_awareness for record in advisor_records))

    def test_ai_design_grounding_view_reports_permission_readiness_without_enforcement(self):
        view = self._ai_view("design_001")
        readiness = view.permission_readiness

        self.assertIsNotNone(readiness)
        self.assertTrue(readiness.permission_required)
        self.assertTrue(readiness.permission_not_enforced)
        self.assertEqual("ai", readiness.audience)
        self.assertEqual("grounded_design_recommendation", readiness.purpose)
        self.assertTrue(readiness.minimum_necessary)
        self.assertIn("consent_artifacts", readiness.deferred_capabilities)
        self.assertIn("scoped_exports", readiness.deferred_capabilities)
        self.assertIn("identity", readiness.deferred_capabilities)
        self.assertTrue(any("AI access is not consent" in note for note in readiness.visibility_limitations))

        advisor_record = next(
            record for record in view.grounding_records if record.entity_type == "advisor_recommendation_summary"
        )
        self.assertTrue(advisor_record.permission_readiness.permission_required)
        self.assertTrue(advisor_record.permission_readiness.permission_not_enforced)
        self.assertEqual("ai", advisor_record.permission_readiness.audience)
        self.assertTrue(advisor_record.permission_readiness.minimum_necessary)

    def test_ai_permission_foundations_are_readiness_only(self):
        view = self._ai_view("design_001")
        readiness = view.permission_readiness
        advisor_record = next(
            record for record in view.grounding_records if record.entity_type == "advisor_recommendation_summary"
        )

        self.assertEqual("ai", readiness.audience_readiness.audience.value)
        self.assertEqual("ai_grounding", readiness.purpose_readiness.purpose.value)
        self.assertEqual("ai_design_grounding", readiness.view_permission_alignment.view_name)
        self.assertEqual("ai_grounding", readiness.view_permission_alignment.visibility_scope.value)
        self.assertTrue(readiness.permission_not_enforced)
        self.assertFalse(readiness.consent_artifact_placeholder.active_consent_present)
        self.assertIsNone(readiness.consent_artifact_placeholder.consent_artifact_id)
        self.assertFalse(readiness.view_permission_alignment.active_permission_grant_present)

        record_readiness = advisor_record.permission_readiness
        self.assertEqual("ai", record_readiness.audience_readiness.audience.value)
        self.assertEqual("ai_grounding", record_readiness.purpose_readiness.purpose.value)
        self.assertTrue(record_readiness.permission_not_enforced)
        self.assertEqual("not_enforced", record_readiness.view_permission_alignment.permission_enforcement)

    def test_ai_design_grounding_view_returns_none_for_design_outside_home_context(self):
        self.assertIsNone(self._ai_view("missing_design"))

    def test_runtime_projection_route_is_additive_and_role_addressed(self):
        paths = {getattr(route, "path", None) for route in app.routes}

        self.assertIn(
            "/api/twin-planning-context/homes/{home_id}/views/runtime-projection/{role}",
            paths,
        )

        view = self._runtime_view("homeowner")
        payload = view.dict()
        self.assertEqual("twin_runtime_projection", view.view_name)
        self.assertEqual("home_001", view.home_id)
        self.assertEqual("home_id", view.anchor_type)
        self.assertEqual("home_id", view.view_context.canonical_anchor)
        self.assertEqual("not_enforced", view.permission_enforcement)
        self.assertNotIn("twin_id", payload)
        self.assertIn("not a separate portal", view.implementation_boundary)

    def test_runtime_projections_use_same_canonical_home_with_different_scopes(self):
        homeowner = self._runtime_view("homeowner")
        contractor = self._runtime_view("contractor")
        internal = self._runtime_view("internal_system")

        self.assertEqual("owner_private", homeowner.view_context.visibility_scope.value)
        self.assertEqual("contractor_scoped", contractor.view_context.visibility_scope.value)
        self.assertEqual("internal_governance", internal.view_context.visibility_scope.value)

        homeowner_home = next(record for record in homeowner.projection_records if record.entity_type == "home")
        contractor_home = next(record for record in contractor.projection_records if record.entity_type == "home")
        internal_home = next(record for record in internal.projection_records if record.entity_type == "home")

        self.assertEqual("home_001", homeowner_home.entity_id)
        self.assertEqual(homeowner_home.entity_id, contractor_home.entity_id)
        self.assertEqual(homeowner_home.entity_id, internal_home.entity_id)

        self.assertIn("address_line_1", homeowner_home.fields)
        self.assertIn("account_id", homeowner_home.fields)
        self.assertNotIn("address_line_1", contractor_home.fields)
        self.assertNotIn("account_id", contractor_home.fields)
        self.assertIn("address_line_1", internal_home.fields)
        self.assertEqual("contractor_scoped", contractor_home.data_classification.value)

    def test_contractor_projection_is_minimized_without_internal_unknowns_or_advisory_notes(self):
        contractor = self._runtime_view("contractor")
        section_keys = {record.section_key for record in contractor.projection_records}
        entity_types = {record.entity_type for record in contractor.projection_records}

        self.assertIn("premise", section_keys)
        self.assertIn("loads", section_keys)
        self.assertIn("derived_intelligence", section_keys)
        self.assertNotIn("scenario_revisions", section_keys)
        self.assertNotIn("unknowns", section_keys)
        self.assertIn("advisor_recommendation_summary", entity_types)
        self.assertNotIn("advisor_note", entity_types)

        self.assertTrue(contractor.permission_readiness.permission_required)
        self.assertTrue(contractor.permission_readiness.permission_not_enforced)
        self.assertTrue(contractor.permission_readiness.minimum_necessary)
        self.assertEqual("contractor", contractor.permission_readiness.audience)
        self.assertIn("permission_grants", contractor.permission_readiness.deferred_capabilities)

    def test_internal_projection_includes_governance_unknowns_without_permission_enforcement(self):
        internal = self._runtime_view("internal_system")
        section_keys = {record.section_key for record in internal.projection_records}
        unknown_records = [record for record in internal.projection_records if record.section_key == "unknowns"]

        self.assertIn("unknowns", section_keys)
        self.assertTrue(unknown_records)
        self.assertTrue(
            all(record.data_classification.value == "internal_governance" for record in internal.projection_records)
        )
        self.assertTrue(internal.permission_readiness.permission_required)
        self.assertTrue(internal.permission_readiness.permission_not_enforced)
        self.assertEqual("internal_system", internal.permission_readiness.audience)
        self.assertIn("auth", internal.permission_readiness.deferred_capabilities)

    def test_runtime_projection_permission_foundations_align_to_view_roles(self):
        homeowner = self._runtime_view("homeowner")
        contractor = self._runtime_view("contractor")
        internal = self._runtime_view("internal_system")

        expectations = [
            (homeowner, "homeowner", "owner_planning_context", "owner_private", False),
            (contractor, "contractor", "contractor_scoping_context", "contractor_scoped", True),
            (internal, "internal_system", "runtime_governance_review", "internal_governance", True),
        ]
        for view, audience, purpose, visibility_scope, permission_required in expectations:
            readiness = view.permission_readiness
            self.assertEqual(permission_required, readiness.permission_required)
            self.assertTrue(readiness.permission_not_enforced)
            self.assertEqual(audience, readiness.audience_readiness.audience.value)
            self.assertEqual(purpose, readiness.purpose_readiness.purpose.value)
            self.assertEqual(visibility_scope, readiness.view_permission_alignment.visibility_scope.value)
            self.assertEqual(f"{audience}_runtime_projection", readiness.view_permission_alignment.view_name)
            self.assertEqual("not_enforced", readiness.view_permission_alignment.permission_enforcement)
            self.assertFalse(readiness.view_permission_alignment.active_permission_grant_present)
            self.assertFalse(readiness.consent_artifact_placeholder.active_consent_present)
            self.assertTrue(readiness.homeowner_authority.homeowner_authority_preserved)
            self.assertIn("permission_grants", readiness.deferred_capabilities)
            self.assertIn("scoped_exports", readiness.deferred_capabilities)
            self.assertIn("operational_control", readiness.deferred_capabilities)

        contractor_load = next(
            record
            for record in contractor.projection_records
            if record.entity_type == "load" and record.entity_id == "load_001"
        )
        contractor_record_readiness = contractor_load.permission_readiness
        self.assertEqual("contractor", contractor_record_readiness.audience_readiness.audience.value)
        self.assertEqual(
            "contractor_scoping_context",
            contractor_record_readiness.purpose_readiness.purpose.value,
        )
        self.assertTrue(contractor_record_readiness.permission_not_enforced)
        self.assertFalse(contractor_record_readiness.consent_artifact_placeholder.active_consent_present)

    def test_runtime_projection_preserves_provenance_and_contributor_identity(self):
        contractor = self._runtime_view("contractor")
        load_record = next(
            record
            for record in contractor.projection_records
            if record.entity_type == "load" and record.entity_id == "load_001"
        )
        advisor_record = next(
            record
            for record in contractor.projection_records
            if record.entity_type == "advisor_recommendation_summary"
        )

        self.assertIsNotNone(load_record.provenance_summary)
        self.assertIn("source_doc_user_load_entry", load_record.source_document_ids)
        self.assertIn("source_doc_user_load_entry", load_record.contributor_identity.source_document_ids)
        self.assertEqual("source_document", load_record.contributor_identity.contributor_type)
        self.assertTrue(load_record.provenance_gaps)
        self.assertTrue(load_record.permission_readiness.permission_not_enforced)

        self.assertEqual("derived_output", advisor_record.classification.value)
        self.assertTrue(advisor_record.rule_keys)
        self.assertEqual(
            "deterministic_rule_or_advisory_runtime",
            advisor_record.contributor_identity.contributor_type,
        )
        self.assertTrue(advisor_record.dependency_hooks)

    def test_dependency_foundations_survive_runtime_and_ai_projections(self):
        contractor = self._runtime_view("contractor")
        internal = self._runtime_view("internal_system")
        ai_view = self._ai_view("design_001")

        contractor_load = next(
            record
            for record in contractor.projection_records
            if record.entity_type == "load" and record.entity_id == "load_001"
        )
        self.assertTrue(contractor_load.change_impact_hints)
        self.assertIn(
            "load_panel_relationship_is_building_level_only",
            {warning.warning_type for warning in contractor_load.planning_dependency_warnings},
        )
        self.assertTrue(
            any(
                hook.target_entity_type == "electrical_panel" and hook.target_entity_id == "panel_main"
                for hook in contractor_load.dependency_hooks
            )
        )

        contractor_equipment = next(
            record
            for record in contractor.projection_records
            if record.entity_type == "design_equipment" and record.entity_id == "design_001_equipment_1"
        )
        self.assertTrue(contractor_equipment.change_impact_hints)
        self.assertIn(
            "equipment_location_is_planning_only",
            {warning.warning_type for warning in contractor_equipment.planning_dependency_warnings},
        )

        internal_revision = next(
            record
            for record in internal.projection_records
            if record.entity_type == "scenario_revision" and record.entity_id == "scenario_001_rev_001"
        )
        self.assertIn(
            "revision_snapshot_is_not_live_replay",
            {warning.warning_type for warning in internal_revision.planning_dependency_warnings},
        )

        ai_equipment = next(
            record
            for record in ai_view.grounding_records
            if record.entity_type == "design_equipment" and record.entity_id == "design_001_equipment_1"
        )
        self.assertTrue(ai_equipment.change_impact_hints)
        self.assertTrue(ai_equipment.planning_dependency_warnings)

        ai_rule_keys = {
            rule_key
            for hook in ai_view.dependency_hooks
            for rule_key in hook.rule_keys
        }
        self.assertIn("twin_dependency.load_panel_shared_building_v1", ai_rule_keys)
        self.assertIn("twin_dependency.equipment_system_reference_v1", ai_rule_keys)

    def test_topology_snapshot_route_is_additive_and_read_only(self):
        paths = {getattr(route, "path", None) for route in app.routes}
        self.assertIn("/api/twin-planning-context/homes/{home_id}/views/topology-snapshot", paths)

        snapshot = self._topology_snapshot()
        payload = snapshot.dict()

        self.assertEqual("topology_snapshot", snapshot.view_name)
        self.assertEqual("home_001", snapshot.home_id)
        self.assertEqual("home_id", snapshot.anchor_type)
        self.assertEqual("not_enforced", snapshot.permission_enforcement)
        self.assertNotIn("twin_id", payload)
        self.assertIn("not a persisted graph", snapshot.implementation_boundary)
        self.assertTrue(snapshot.nodes)
        self.assertTrue(snapshot.edges)
        self.assertTrue(snapshot.scenario_branch_references)
        self.assertTrue(snapshot.revision_lineage_references)

    def test_topology_snapshot_derives_nodes_and_edges_from_existing_context(self):
        snapshot = self._topology_snapshot()
        node_map = {node.node_id: node for node in snapshot.nodes}
        edge_pairs = {
            (edge.source_node_id, edge.target_node_id, edge.relationship)
            for edge in snapshot.edges
        }

        for node_id in [
            "home:home_001",
            "building:building_main",
            "electrical_panel:panel_main",
            "load:load_001",
            "energy_system_design:design_001",
            "design_equipment:design_001_equipment_1",
            "equipment_product:product_generic_panel",
            "equipment_location:location_roof_south",
            "estimated_pathway:pathway_001",
            "scenario:scenario_001",
            "scenario_revision:scenario_001_rev_001",
        ]:
            self.assertIn(node_id, node_map)

        self.assertIn(
            (
                "load:load_001",
                "electrical_panel:panel_main",
                "shared_building_id_planning_context",
            ),
            edge_pairs,
        )
        self.assertIn(
            (
                "design_equipment:design_001_equipment_1",
                "energy_system_design:design_001",
                "assigned_to_design_planning_context",
            ),
            edge_pairs,
        )
        self.assertIn(
            (
                "design_equipment:design_001_equipment_1",
                "equipment_product:product_generic_panel",
                "uses_product_reference",
            ),
            edge_pairs,
        )
        self.assertIn(
            (
                "design_equipment:design_001_equipment_1",
                "equipment_location:location_roof_south",
                "assigned_location_planning_context",
            ),
            edge_pairs,
        )
        self.assertIn(
            (
                "scenario:scenario_001",
                "energy_system_design:design_001",
                "linked_design_planning_context",
            ),
            edge_pairs,
        )
        self.assertIn(
            (
                "scenario_revision:scenario_001_rev_001",
                "scenario:scenario_001",
                "snapshot_of_scenario",
            ),
            edge_pairs,
        )

    def test_topology_snapshot_reports_relationship_coverage_without_graph_engine(self):
        snapshot = self._topology_snapshot()
        edge_pairs = {
            (edge.source_node_id, edge.target_node_id, edge.relationship)
            for edge in snapshot.edges
        }
        coverage = snapshot.relationship_coverage_summary
        missing_by_indicator = {
            (indicator.indicator, indicator.entity_id): indicator
            for indicator in snapshot.missing_relationship_indicators
        }

        for edge_pair in [
            (
                "building:building_main",
                "home:home_001",
                "structure_belongs_to_premise_planning_context",
            ),
            (
                "electrical_panel:panel_main",
                "building:building_main",
                "panel_assigned_to_building_planning_context",
            ),
            (
                "load:load_001",
                "building:building_main",
                "load_assigned_to_building_planning_context",
            ),
            (
                "equipment_location:location_roof_south",
                "building:building_main",
                "location_assigned_to_building_planning_context",
            ),
            (
                "energy_system_design:design_001",
                "estimated_pathway:pathway_001",
                "design_includes_pathway_planning_context",
            ),
            (
                "estimated_pathway:pathway_001",
                "equipment_location:location_roof_south",
                "pathway_source_location_planning_context",
            ),
            (
                "estimated_pathway:pathway_001",
                "equipment_location:location_garage_battery",
                "pathway_destination_location_planning_context",
            ),
            (
                "estimated_pathway:pathway_002",
                "equipment_location:location_shop_pad",
                "pathway_destination_location_planning_context",
            ),
        ]:
            self.assertIn(edge_pair, edge_pairs)

        self.assertEqual("topology_snapshot_relationship_metadata_only", coverage.coverage_scope)
        self.assertTrue(coverage.descriptive_only)
        self.assertTrue(coverage.read_only)
        self.assertTrue(coverage.topology_derived)
        self.assertFalse(coverage.graph_engine_present)
        self.assertFalse(coverage.lifecycle_workflows_present)
        self.assertFalse(coverage.promotion_engine_present)
        self.assertFalse(coverage.event_log_present)
        self.assertFalse(coverage.recalculation_engine_present)
        self.assertFalse(coverage.invalidation_engine_present)
        self.assertFalse(coverage.simulation_present)
        self.assertFalse(coverage.what_if_analysis_present)
        self.assertFalse(coverage.phase_3_intelligence_present)
        self.assertGreater(coverage.relationship_edge_count, 0)
        self.assertGreater(coverage.dependency_hook_edge_count, 0)

        for family in [
            "structure_premise_placement",
            "panel_building_placement",
            "load_building_placement",
            "location_building_placement",
            "design_pathway_reference",
            "pathway_endpoint_reference",
        ]:
            self.assertIn(family, coverage.coverage_by_relationship_family)
            self.assertGreater(coverage.coverage_by_relationship_family[family], 0)

        unresolved_source = missing_by_indicator[
            ("pathway_source_location_relationship_unresolved", "pathway_002")
        ]
        self.assertEqual("source_location", unresolved_source.field_name)
        self.assertEqual("Main House MSP", unresolved_source.attempted_value)
        self.assertEqual("pathway_endpoint_reference", unresolved_source.relationship_family)
        self.assertIn("does not resolve", unresolved_source.reason)
        self.assertGreaterEqual(coverage.unresolved_pathway_endpoint_count, 1)

    def test_topology_snapshot_reports_lifecycle_and_lineage_without_engines(self):
        snapshot = self._topology_snapshot()
        node_map = {node.node_id: node for node in snapshot.nodes}

        self.assertEqual(
            "recorded_current_topology",
            node_map["load:load_001"].lifecycle_domain.value,
        )
        self.assertEqual(
            "sandbox_proposed_planning_topology",
            node_map["design_equipment:design_001_equipment_1"].lifecycle_domain.value,
        )
        self.assertEqual(
            "saved_scenario_revision_topology",
            node_map["scenario_revision:scenario_001_rev_001"].lifecycle_domain.value,
        )
        advisor_node = next(node for node in snapshot.nodes if node.entity_type == "advisor_recommendation_summary")
        self.assertEqual("derived_advisory_topology", advisor_node.lifecycle_domain.value)

        for domain in [
            "recorded_current_topology",
            "sandbox_proposed_planning_topology",
            "saved_scenario_revision_topology",
            "derived_advisory_topology",
        ]:
            self.assertIn(domain, snapshot.lifecycle_domain_summary)
            self.assertGreater(snapshot.lifecycle_domain_summary[domain], 0)

        scenario_ref = next(
            item for item in snapshot.scenario_branch_references if item["scenario_id"] == "scenario_001"
        )
        self.assertEqual("design_001", scenario_ref["linked_design_id"])
        self.assertEqual("scenario:scenario_001", scenario_ref["scenario_node_id"])
        self.assertEqual("energy_system_design:design_001", scenario_ref["linked_design_node_id"])

        revision_ref = next(
            item for item in snapshot.revision_lineage_references if item["revision_id"] == "scenario_001_rev_001"
        )
        self.assertEqual("scenario_001", revision_ref["scenario_id"])
        self.assertEqual("design_001", revision_ref["linked_design_id"])
        self.assertEqual("scenario_revision:scenario_001_rev_001", revision_ref["revision_node_id"])
        self.assertEqual("scenario:scenario_001", revision_ref["scenario_node_id"])

    def test_topology_snapshot_reports_descriptive_lifecycle_readiness(self):
        snapshot = self._topology_snapshot()
        readiness = snapshot.lifecycle_readiness_summary
        hints_by_domain = {
            hint.lifecycle_domain.value: hint
            for hint in snapshot.lifecycle_readiness_hints
        }
        missing_by_indicator = {
            item.indicator: item
            for item in snapshot.missing_readiness_indicators
        }
        deferred_domains = {
            item.lifecycle_domain
            for item in snapshot.deferred_lifecycle_domains
        }

        self.assertEqual("topology_snapshot_metadata_only", readiness.readiness_scope)
        self.assertTrue(readiness.descriptive_only)
        self.assertTrue(readiness.read_only)
        self.assertTrue(readiness.topology_derived)
        self.assertTrue(readiness.provenance_aware)
        self.assertFalse(readiness.lifecycle_workflows_present)
        self.assertFalse(readiness.promotion_engine_present)
        self.assertFalse(readiness.event_log_present)
        self.assertFalse(readiness.simulation_present)
        self.assertFalse(readiness.phase_3_intelligence_present)
        self.assertEqual(len(snapshot.nodes), readiness.node_count)
        self.assertEqual(len(snapshot.edges), readiness.edge_count)

        for domain in [
            "recorded_current_topology",
            "sandbox_proposed_planning_topology",
            "saved_scenario_revision_topology",
            "derived_advisory_topology",
        ]:
            self.assertIn(domain, hints_by_domain)
            self.assertIn(domain, readiness.domains_present)
            self.assertGreaterEqual(hints_by_domain[domain].node_count, 1)
            self.assertIn("topology_nodes", hints_by_domain[domain].derived_from)
            self.assertIn("topology_snapshot_limitations", hints_by_domain[domain].derived_from)
            self.assertIn("No lifecycle workflow", " ".join(hints_by_domain[domain].hints))

        self.assertGreater(readiness.provenance_gap_count, 0)
        self.assertGreater(readiness.planning_dependency_warning_count, 0)
        self.assertTrue(readiness.dependency_awareness_labels)

        for domain in [
            "contractor_reviewed_topology",
            "contractual_topology",
            "field_verified_topology",
            "utility_reviewed_topology",
            "operational_topology",
            "future_expansion_or_replacement_topology",
        ]:
            self.assertIn(domain, deferred_domains)
            self.assertIn(domain, readiness.domains_deferred)

        for indicator in [
            "field_verification_readiness",
            "promotion_workflow_readiness",
            "lifecycle_event_log_readiness",
            "simulation_readiness",
            "operational_topology_readiness",
        ]:
            self.assertIn(indicator, missing_by_indicator)
            self.assertFalse(missing_by_indicator[indicator].present)
            self.assertTrue(missing_by_indicator[indicator].source_marker_found)
            self.assertIn("topology_snapshot_limitations", missing_by_indicator[indicator].derived_from)

    def test_topology_snapshot_preserves_deferred_boundaries(self):
        snapshot = self._topology_snapshot()
        limitation_text = " ".join(snapshot.limitations)
        relationship_limitation_text = " ".join(snapshot.relationship_coverage_summary.limitations)
        payload = snapshot.dict()

        for boundary in [
            "No topology graph",
            "graph database",
            "canonical topology table",
            "migration",
            "persisted topology state",
            "topology promotion workflow",
            "lifecycle event log",
            "recalculation engine",
            "invalidation engine",
            "simulation",
            "Phase 3 intelligence",
            "auth",
            "RBAC/ABAC",
            "permission enforcement",
            "exports",
            "utility sharing",
            "telemetry governance",
            "ownership transfer",
            "registry",
            "marketplace",
            "operational control",
        ]:
            self.assertIn(boundary, limitation_text)

        for boundary in [
            "graph engine",
            "lifecycle workflow",
            "promotion engine",
            "event log",
            "recalculation",
            "invalidation",
            "simulation",
            "what-if analysis",
            "Phase 3 intelligence",
            "field-verified",
            "utility-reviewed",
            "contractual",
            "operational topology",
        ]:
            self.assertIn(boundary, relationship_limitation_text)

        self.assertNotIn("twin_id", payload)
        self.assertTrue(all(node.permission_not_enforced for node in snapshot.nodes))
        self.assertTrue(
            all("not create installation" in " ".join(node.limitations) for node in snapshot.nodes)
        )

    def test_dependency_impact_readiness_route_is_additive_and_explain_only(self):
        paths = {getattr(route, "path", None) for route in app.routes}
        self.assertIn(
            "/api/twin-planning-context/homes/{home_id}/views/dependency-impact-readiness",
            paths,
        )

        view = self._dependency_impact_view()
        payload = view.dict()
        summary = view.readiness_summary

        self.assertEqual("dependency_impact_readiness", view.view_name)
        self.assertEqual("home_001", view.home_id)
        self.assertEqual("home_id", view.anchor_type)
        self.assertEqual("not_enforced", view.permission_enforcement)
        self.assertEqual("derived", view.authority_layer.value)
        self.assertNotIn("twin_id", payload)
        self.assertTrue(summary.descriptive_only)
        self.assertTrue(summary.read_only)
        self.assertTrue(summary.request_time_only)
        self.assertTrue(summary.home_id_anchored)
        self.assertTrue(summary.derived_from_existing_twin_context)
        self.assertTrue(summary.derived_from_topology_snapshot)
        self.assertTrue(summary.deterministic_for_same_inputs)
        self.assertFalse(summary.ai_generated_facts_present)
        self.assertFalse(summary.graph_database_present)
        self.assertFalse(summary.graph_engine_present)
        self.assertFalse(summary.scenario_engine_present)
        self.assertFalse(summary.simulation_present)
        self.assertFalse(summary.what_if_analysis_present)
        self.assertFalse(summary.recalculation_engine_present)
        self.assertFalse(summary.invalidation_engine_present)
        self.assertFalse(summary.recommendation_actions_present)
        self.assertFalse(summary.optimization_present)
        self.assertFalse(summary.ranking_present)
        self.assertFalse(summary.authorization_present)
        self.assertFalse(summary.permission_enforcement_present)
        self.assertFalse(summary.export_present)
        self.assertFalse(summary.operational_behavior_present)
        self.assertIn("not a graph engine", view.implementation_boundary)
        self.assertIn("contracts remain unchanged", view.compatibility_note)

    def test_dependency_impact_readiness_statements_are_traceable_to_existing_basis(self):
        view = self._dependency_impact_view()

        self.assertIn("twin_planning_context", view.source_basis.source_view_names)
        self.assertIn("topology_snapshot", view.source_basis.source_view_names)
        self.assertTrue(view.source_basis.source_section_keys)
        self.assertTrue(view.source_basis.topology_node_ids)
        self.assertTrue(view.source_basis.topology_edge_ids)
        self.assertTrue(view.source_basis.lifecycle_readiness_signals_used)
        self.assertTrue(view.source_basis.dependency_warning_refs)
        self.assertTrue(view.source_basis.provenance_gap_refs)
        self.assertTrue(view.source_basis.missing_readiness_indicator_refs)
        self.assertTrue(view.source_basis.derived_from)

        for item in (
            view.lifecycle_scope
            + view.dependency_impact_posture
            + view.provenance_gap_posture
            + view.confidence_posture
        ):
            self.assertTrue(item.statement)
            self.assertTrue(item.basis.source_view_names)
            self.assertTrue(item.basis.derived_from)
            self.assertTrue(item.basis.limitations)

        for item in view.dependency_impact_posture:
            self.assertTrue(item.basis.topology_node_ids)
            self.assertTrue(item.basis.topology_edge_ids)
            self.assertTrue(item.basis.lifecycle_readiness_signals_used)
            self.assertTrue(item.basis.dependency_warning_refs)
            self.assertTrue(item.basis.provenance_gap_refs)

        self.assertTrue(view.missing_inputs)
        for item in view.missing_inputs:
            self.assertTrue(item.reason)
            self.assertTrue(item.basis.source_view_names)
            self.assertTrue(item.basis.derived_from)

    def test_dependency_impact_readiness_is_deterministic_for_same_inputs(self):
        first = self._dependency_impact_view().dict()
        second = self._dependency_impact_view().dict()

        self.assertEqual(first, second)
        self.assertEqual(
            sorted(first["deferred_capabilities"]),
            first["deferred_capabilities"],
        )

    def test_dependency_impact_readiness_preserves_deferred_boundaries(self):
        view = self._dependency_impact_view()
        deferred = set(view.deferred_capabilities)

        for capability in [
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
        ]:
            self.assertIn(capability, deferred)

        limitation_text = " ".join(view.limitations)
        self.assertIn("does not recommend", limitation_text)
        self.assertIn("simulate", limitation_text)
        self.assertIn("operate devices", limitation_text)

    def test_dependency_reasoning_route_is_additive_and_explain_only(self):
        paths = {getattr(route, "path", None) for route in app.routes}
        self.assertIn(
            "/api/twin-planning-context/homes/{home_id}/views/dependency-reasoning",
            paths,
        )

        view = self._dependency_reasoning_view()
        payload = view.dict()
        scope = view.reasoning_scope

        self.assertEqual("dependency_reasoning", view.view_name)
        self.assertEqual("home_001", view.home_id)
        self.assertEqual("home_id", view.anchor_type)
        self.assertEqual("not_enforced", view.permission_enforcement)
        self.assertEqual("derived", view.authority_layer.value)
        self.assertNotIn("twin_id", payload)
        self.assertTrue(scope.descriptive_only)
        self.assertTrue(scope.read_only)
        self.assertTrue(scope.request_time_only)
        self.assertTrue(scope.home_id_anchored)
        self.assertTrue(scope.derived_from_existing_twin_context)
        self.assertTrue(scope.derived_from_topology_snapshot)
        self.assertTrue(scope.derived_from_dependency_impact_readiness)
        self.assertTrue(scope.deterministic_for_same_inputs)
        self.assertFalse(scope.ai_generated_facts_present)
        self.assertFalse(scope.new_topology_facts_created)
        self.assertFalse(scope.graph_database_present)
        self.assertFalse(scope.graph_engine_present)
        self.assertFalse(scope.scenario_engine_present)
        self.assertFalse(scope.scenario_intelligence_present)
        self.assertFalse(scope.simulation_present)
        self.assertFalse(scope.what_if_analysis_present)
        self.assertFalse(scope.impact_propagation_engine_present)
        self.assertFalse(scope.stale_state_created)
        self.assertFalse(scope.recalculation_engine_present)
        self.assertFalse(scope.invalidation_engine_present)
        self.assertFalse(scope.recommendation_actions_present)
        self.assertFalse(scope.optimization_present)
        self.assertFalse(scope.ranking_present)
        self.assertFalse(scope.authorization_present)
        self.assertFalse(scope.permission_enforcement_present)
        self.assertFalse(scope.export_present)
        self.assertFalse(scope.operational_behavior_present)
        self.assertIn("not impact propagation", view.implementation_boundary)
        self.assertIn("contracts remain unchanged", view.compatibility_note)

    def test_dependency_reasoning_reports_bounded_dependency_types(self):
        view = self._dependency_reasoning_view()

        for dependency_type in [
            "source_dependency",
            "topology_dependency",
            "lifecycle_dependency",
            "rule_dependency",
            "provenance_dependency",
            "permission_readiness_dependency",
            "continuity_snapshot_dependency",
            "missing_information_dependency",
        ]:
            self.assertIn(dependency_type, view.dependency_type_summary)
            self.assertGreater(view.dependency_type_summary[dependency_type], 0)

        self.assertTrue(view.dependency_reasoning_items)
        self.assertTrue(view.upstream_downstream_interpretations)
        self.assertTrue(view.lifecycle_dependency_context)
        self.assertTrue(view.provenance_dependency_context)
        self.assertTrue(view.missing_information_context)
        self.assertTrue(view.confidence_posture)

    def test_dependency_reasoning_statements_are_traceable_to_existing_basis(self):
        view = self._dependency_reasoning_view()

        for source_view_name in [
            "twin_planning_context",
            "topology_snapshot",
            "dependency_impact_readiness",
        ]:
            self.assertIn(source_view_name, view.source_basis.source_view_names)
        self.assertTrue(view.source_basis.source_section_keys)
        self.assertTrue(view.source_basis.topology_node_ids)
        self.assertTrue(view.source_basis.topology_edge_ids)
        self.assertTrue(view.source_basis.lifecycle_readiness_signals_used)
        self.assertTrue(view.source_basis.dependency_warning_refs)
        self.assertTrue(view.source_basis.provenance_gap_refs)
        self.assertTrue(view.source_basis.missing_readiness_indicator_refs)
        self.assertTrue(view.source_basis.derived_from)

        for item in (
            view.dependency_reasoning_items
            + view.upstream_downstream_interpretations
            + view.lifecycle_dependency_context
            + view.provenance_dependency_context
            + view.missing_information_context
            + view.confidence_posture
        ):
            self.assertTrue(item.statement)
            self.assertTrue(item.subject_ref)
            self.assertTrue(item.basis.source_view_names)
            self.assertIn("dependency_impact_readiness", item.basis.source_view_names)
            self.assertTrue(item.basis.derived_from)
            self.assertTrue(item.basis.limitations)

        topology_items = [
            item
            for item in view.dependency_reasoning_items
            if item.reasoning_type.value == "topology_dependency"
        ]
        self.assertTrue(topology_items)
        self.assertTrue(all(item.basis.topology_edge_ids for item in topology_items))

        missing_items = [
            item
            for item in view.dependency_reasoning_items
            if item.reasoning_type.value == "missing_information_dependency"
        ]
        self.assertTrue(missing_items)
        self.assertTrue(
            all(
                item.basis.provenance_gap_refs
                or item.basis.missing_readiness_indicator_refs
                or item.basis.missing_relationship_indicator_refs
                for item in missing_items
            )
        )

    def test_dependency_reasoning_is_deterministic_for_same_inputs(self):
        first = self._dependency_reasoning_view().dict()
        second = self._dependency_reasoning_view().dict()

        self.assertEqual(first, second)
        self.assertEqual(
            sorted(first["deferred_capabilities"]),
            first["deferred_capabilities"],
        )

    def test_dependency_reasoning_preserves_deferred_boundaries(self):
        view = self._dependency_reasoning_view()
        deferred = set(view.deferred_capabilities)

        for capability in [
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
        ]:
            self.assertIn(capability, deferred)

        limitation_text = " ".join(view.limitations)
        self.assertIn("does not propagate impacts", limitation_text)
        self.assertIn("compare scenarios", limitation_text)
        self.assertIn("recommend", limitation_text)
        self.assertIn("operate devices", limitation_text)

    def test_planning_intelligence_readiness_route_is_additive_and_inventory_only(self):
        paths = {getattr(route, "path", None) for route in app.routes}
        self.assertIn(
            "/api/twin-planning-context/homes/{home_id}/views/planning-intelligence-readiness",
            paths,
        )

        view = self._planning_intelligence_readiness_view()
        payload = view.dict()
        scope = view.readiness_scope

        self.assertEqual("planning_intelligence_readiness", view.view_name)
        self.assertEqual("home_001", view.home_id)
        self.assertEqual("home_id", view.anchor_type)
        self.assertEqual("not_enforced", view.permission_enforcement)
        self.assertEqual("derived", view.authority_layer.value)
        self.assertNotIn("twin_id", payload)
        self.assertTrue(scope.descriptive_only)
        self.assertTrue(scope.readiness_inventory_only)
        self.assertTrue(scope.read_only)
        self.assertTrue(scope.request_time_only)
        self.assertTrue(scope.home_id_anchored)
        self.assertTrue(scope.derived_from_existing_twin_context)
        self.assertTrue(scope.derived_from_topology_snapshot)
        self.assertTrue(scope.derived_from_dependency_impact_readiness)
        self.assertTrue(scope.derived_from_dependency_reasoning)
        self.assertTrue(scope.deterministic_for_same_inputs)
        self.assertIn("not a reasoning engine", view.implementation_boundary)
        self.assertIn("contracts remain unchanged", view.compatibility_note)

    def test_planning_intelligence_readiness_has_no_forbidden_capability_flags(self):
        scope = self._planning_intelligence_readiness_view().readiness_scope

        self.assertFalse(scope.ai_generated_facts_present)
        self.assertFalse(scope.persistence_present)
        self.assertFalse(scope.migrations_present)
        self.assertFalse(scope.twin_id_present)
        self.assertFalse(scope.canonical_twin_runtime_model_changes_present)
        self.assertFalse(scope.new_topology_facts_created)
        self.assertFalse(scope.graph_database_present)
        self.assertFalse(scope.graph_engine_present)
        self.assertFalse(scope.scenario_intelligence_present)
        self.assertFalse(scope.impact_propagation_present)
        self.assertFalse(scope.stale_state_persistence_present)
        self.assertFalse(scope.recalculation_engine_present)
        self.assertFalse(scope.invalidation_engine_present)
        self.assertFalse(scope.simulation_present)
        self.assertFalse(scope.what_if_analysis_present)
        self.assertFalse(scope.optimization_present)
        self.assertFalse(scope.ranking_present)
        self.assertFalse(scope.recommendations_present)
        self.assertFalse(scope.economic_reasoning_present)
        self.assertFalse(scope.utility_readiness_logic_present)
        self.assertFalse(scope.survivability_recharge_modeling_present)
        self.assertFalse(scope.compatibility_engine_present)
        self.assertFalse(scope.proposal_generation_present)
        self.assertFalse(scope.export_present)
        self.assertFalse(scope.auth_present)
        self.assertFalse(scope.rbac_abac_present)
        self.assertFalse(scope.permission_enforcement_present)
        self.assertFalse(scope.marketplace_present)
        self.assertFalse(scope.operational_behavior_present)

    def test_planning_intelligence_readiness_reports_ready_and_blocked_areas(self):
        view = self._planning_intelligence_readiness_view()

        self.assertTrue(view.ready_areas)
        self.assertTrue(view.blocked_deferred_areas)
        self.assertTrue(all(item.posture == "ready for read-only explanation" for item in view.ready_areas))
        self.assertTrue(all(item.posture == "blocked/deferred" for item in view.blocked_deferred_areas))

        ready_areas = {item.intelligence_area.value for item in view.ready_areas}
        for area in [
            "topology_explanation",
            "lifecycle_explanation",
            "relationship_coverage_explanation",
            "dependency_impact_readiness",
            "dependency_reasoning",
            "provenance_gap_reporting",
            "permission_readiness_metadata",
        ]:
            self.assertIn(area, ready_areas)

        blocked_areas = {item.intelligence_area.value for item in view.blocked_deferred_areas}
        for area in [
            "scenario_intelligence",
            "impact_propagation",
            "stale_state_persistence",
            "recalculation",
            "invalidation",
            "simulation",
            "what_if_analysis",
            "optimization",
            "ranking",
            "economic_reasoning",
            "utility_readiness_logic",
            "survivability_recharge_modeling",
            "compatibility_engine",
            "recommendation_or_proposal_generation",
            "exports",
            "auth_rbac_abac",
            "permission_enforcement",
            "marketplace",
            "operational_behavior",
        ]:
            self.assertIn(area, blocked_areas)

    def test_planning_intelligence_readiness_items_are_traceable(self):
        view = self._planning_intelligence_readiness_view()

        for source_view_name in [
            "twin_planning_context",
            "topology_snapshot",
            "dependency_impact_readiness",
            "dependency_reasoning",
        ]:
            self.assertIn(source_view_name, view.source_basis.source_view_names)
        self.assertTrue(view.source_basis.source_section_keys)
        self.assertTrue(view.source_basis.topology_node_ids)
        self.assertTrue(view.source_basis.topology_edge_ids)
        self.assertTrue(view.source_basis.lifecycle_readiness_signals_used)
        self.assertTrue(view.source_basis.provenance_gap_refs)
        self.assertTrue(view.source_basis.derived_from)

        for item in (
            view.ready_areas
            + view.blocked_deferred_areas
            + view.provenance_permission_basis
            + view.confidence_posture
        ):
            self.assertTrue(item.statement)
            self.assertTrue(item.available_evidence)
            self.assertTrue(item.basis.source_view_names)
            self.assertIn("twin_planning_context", item.basis.source_view_names)
            self.assertIn("dependency_reasoning", item.basis.source_view_names)
            self.assertTrue(item.basis.derived_from)
            self.assertTrue(item.basis.limitations)

    def test_planning_intelligence_readiness_surfaces_unsafe_assumptions(self):
        view = self._planning_intelligence_readiness_view()
        assumptions = " ".join(view.unsafe_assumptions)

        self.assertTrue(view.unsafe_assumptions)
        self.assertIn("provenance presence as verification", assumptions)
        self.assertIn("permission readiness metadata as permission enforcement", assumptions)
        self.assertIn("recommendation or proposal", assumptions)
        self.assertIn("operational readiness", assumptions)

    def test_planning_intelligence_readiness_preserves_deferred_boundaries(self):
        view = self._planning_intelligence_readiness_view()
        deferred = set(view.deferred_reasoning_boundaries)

        for boundary in [
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
        ]:
            self.assertIn(boundary, deferred)

        limitation_text = " ".join(view.limitations)
        self.assertIn("readiness inventory only", limitation_text)
        self.assertIn("ready for read-only explanation", limitation_text)
        self.assertIn("blocked/deferred", limitation_text)

    def test_planning_intelligence_readiness_is_deterministic_for_same_inputs(self):
        first = self._planning_intelligence_readiness_view().dict()
        second = self._planning_intelligence_readiness_view().dict()

        self.assertEqual(first, second)
        self.assertEqual(
            sorted(first["deferred_reasoning_boundaries"]),
            first["deferred_reasoning_boundaries"],
        )

    def test_planning_intelligence_readiness_preserves_provenance_and_permission_boundaries(self):
        view = self._planning_intelligence_readiness_view()
        provenance_item = next(
            item
            for item in view.ready_areas
            if item.intelligence_area.value == "provenance_gap_reporting"
        )
        permission_item = next(
            item
            for item in view.ready_areas
            if item.intelligence_area.value == "permission_readiness_metadata"
        )

        self.assertFalse(provenance_item.provenance_presence_is_verification)
        self.assertFalse(permission_item.permission_readiness_is_enforcement)
        self.assertIn("not_verification", provenance_item.confidence_posture)
        self.assertIn("metadata_only", permission_item.confidence_posture)
        self.assertTrue(view.provenance_permission_basis)
        self.assertTrue(
            all(not item.provenance_presence_is_verification for item in view.provenance_permission_basis)
        )
        self.assertTrue(
            all(not item.permission_readiness_is_enforcement for item in view.provenance_permission_basis)
        )

    def test_advisory_context_assembly_route_is_additive_and_input_only(self):
        paths = {getattr(route, "path", None) for route in app.routes}
        self.assertIn(
            "/api/twin-planning-context/homes/{home_id}/views/advisory-context-assembly",
            paths,
        )

        view = self._advisory_context_assembly_view()
        payload = view.dict()
        scope = view.assembly_scope

        self.assertEqual("advisory_context_assembly", view.view_name)
        self.assertEqual("home_001", view.home_id)
        self.assertEqual("home_id", view.anchor_type)
        self.assertEqual("not_enforced", view.permission_enforcement)
        self.assertEqual("derived", view.authority_layer.value)
        self.assertNotIn("twin_id", payload)
        self.assertTrue(scope.advisory_input_context_only)
        self.assertTrue(scope.descriptive_only)
        self.assertTrue(scope.read_only)
        self.assertTrue(scope.request_time_only)
        self.assertTrue(scope.home_id_anchored)
        self.assertTrue(scope.derived_from_existing_twin_context)
        self.assertTrue(scope.derived_from_topology_snapshot)
        self.assertTrue(scope.derived_from_dependency_impact_readiness)
        self.assertTrue(scope.derived_from_dependency_reasoning)
        self.assertTrue(scope.derived_from_planning_intelligence_readiness)
        self.assertTrue(scope.deterministic_for_same_inputs)
        self.assertIn("not advice generation", view.implementation_boundary)
        self.assertIn("contracts remain unchanged", view.compatibility_note)

    def test_advisory_context_assembly_has_no_forbidden_capabilities(self):
        scope = self._advisory_context_assembly_view().assembly_scope

        self.assertFalse(scope.advice_generated)
        self.assertFalse(scope.recommendations_present)
        self.assertFalse(scope.ranking_present)
        self.assertFalse(scope.optimization_present)
        self.assertFalse(scope.scenario_simulation_present)
        self.assertFalse(scope.what_if_analysis_present)
        self.assertFalse(scope.proposal_generation_present)
        self.assertFalse(scope.contractor_sales_logic_present)
        self.assertFalse(scope.homeowner_guidance_outputs_present)
        self.assertFalse(scope.permission_enforcement_present)
        self.assertFalse(scope.auth_present)
        self.assertFalse(scope.rbac_abac_present)
        self.assertFalse(scope.persistence_present)
        self.assertFalse(scope.migrations_present)
        self.assertFalse(scope.twin_id_present)
        self.assertFalse(scope.graph_engine_present)
        self.assertFalse(scope.export_present)
        self.assertFalse(scope.operational_behavior_present)

    def test_advisory_context_assembly_reports_expected_context_areas(self):
        view = self._advisory_context_assembly_view()

        self.assertTrue(view.homeowner_goals)
        self.assertTrue(view.topology_facts)
        self.assertTrue(view.equipment_site_facts)
        self.assertTrue(view.provenance_basis)
        self.assertTrue(view.permission_readiness_metadata)
        self.assertTrue(view.missing_data)
        self.assertTrue(view.unsafe_assumptions)
        self.assertTrue(view.advisory_input_readiness)
        self.assertTrue(view.deferred_advisory_output_boundaries)

        goal_item = view.homeowner_goals[0]
        self.assertIn("design_goal", " ".join(goal_item.assembled_inputs))
        readiness_item = view.advisory_input_readiness[0]
        self.assertIn("no_advice_generated", readiness_item.confidence_posture)

    def test_advisory_context_assembly_items_are_traceable(self):
        view = self._advisory_context_assembly_view()
        all_items = (
            view.homeowner_goals
            + view.topology_facts
            + view.equipment_site_facts
            + view.provenance_basis
            + view.permission_readiness_metadata
            + view.missing_data
            + view.unsafe_assumptions
            + view.advisory_input_readiness
        )

        for source_view_name in [
            "twin_planning_context",
            "topology_snapshot",
            "dependency_impact_readiness",
            "dependency_reasoning",
            "planning_intelligence_readiness",
        ]:
            self.assertIn(source_view_name, view.source_basis.source_view_names)
        self.assertTrue(view.source_basis.source_section_keys)
        self.assertTrue(view.source_basis.topology_node_ids)
        self.assertTrue(view.source_basis.topology_edge_ids)
        self.assertTrue(view.source_basis.derived_from)

        for item in all_items:
            self.assertTrue(item.statement)
            self.assertTrue(item.basis.source_view_names)
            self.assertIn("planning_intelligence_readiness", item.basis.source_view_names)
            self.assertTrue(item.basis.derived_from)
            self.assertTrue(item.basis.limitations)

    def test_advisory_context_assembly_preserves_deferred_output_boundaries(self):
        view = self._advisory_context_assembly_view()
        deferred = set(view.deferred_advisory_output_boundaries)

        for boundary in [
            "advice_generation",
            "recommendations",
            "ranking",
            "optimization",
            "scenario_simulation",
            "what_if_analysis",
            "proposal_generation",
            "contractor_sales_logic",
            "homeowner_guidance_outputs",
            "permission_enforcement",
            "auth",
            "rbac_abac",
            "persistence",
            "migrations",
            "twin_id",
            "graph_engine",
            "exports",
            "operational_behavior",
        ]:
            self.assertIn(boundary, deferred)

        limitation_text = " ".join(view.limitations)
        self.assertIn("advisory input context only", limitation_text)
        self.assertIn("does not generate advice", limitation_text)

    def test_advisory_context_assembly_is_deterministic_for_same_inputs(self):
        first = self._advisory_context_assembly_view().dict()
        second = self._advisory_context_assembly_view().dict()

        self.assertEqual(first, second)
        self.assertEqual(
            sorted(first["deferred_advisory_output_boundaries"]),
            first["deferred_advisory_output_boundaries"],
        )

    def test_constraint_risk_reasoning_route_is_additive_and_read_only(self):
        paths = {getattr(route, "path", None) for route in app.routes}
        self.assertIn(
            "/api/twin-planning-context/homes/{home_id}/views/constraint-risk-reasoning",
            paths,
        )

        view = self._constraint_risk_reasoning_view()
        payload = view.dict()
        scope = view.reasoning_scope

        self.assertEqual("constraint_risk_reasoning", view.view_name)
        self.assertEqual("home_001", view.home_id)
        self.assertEqual("home_id", view.anchor_type)
        self.assertEqual("not_enforced", view.permission_enforcement)
        self.assertEqual("derived", view.authority_layer.value)
        self.assertNotIn("twin_id", payload)
        self.assertTrue(scope.constraint_risk_explanation_only)
        self.assertTrue(scope.descriptive_only)
        self.assertTrue(scope.read_only)
        self.assertTrue(scope.request_time_only)
        self.assertTrue(scope.home_id_anchored)
        self.assertTrue(scope.derived_from_existing_twin_context)
        self.assertTrue(scope.derived_from_topology_snapshot)
        self.assertTrue(scope.derived_from_dependency_impact_readiness)
        self.assertTrue(scope.derived_from_dependency_reasoning)
        self.assertTrue(scope.derived_from_planning_intelligence_readiness)
        self.assertTrue(scope.derived_from_advisory_context_assembly)
        self.assertTrue(scope.deterministic_for_same_inputs)
        self.assertIn("constraint and risk reasoning view", view.implementation_boundary)
        self.assertIn("contracts remain unchanged", view.compatibility_note)

    def test_constraint_risk_reasoning_has_no_forbidden_capabilities(self):
        scope = self._constraint_risk_reasoning_view().reasoning_scope

        self.assertFalse(scope.recommendations_present)
        self.assertFalse(scope.priority_ranking_present)
        self.assertFalse(scope.optimization_present)
        self.assertFalse(scope.scenario_simulation_present)
        self.assertFalse(scope.what_if_analysis_present)
        self.assertFalse(scope.proposal_generation_present)
        self.assertFalse(scope.final_design_guidance_present)
        self.assertFalse(scope.contractor_directives_present)
        self.assertFalse(scope.homeowner_directives_present)
        self.assertFalse(scope.economic_reasoning_present)
        self.assertFalse(scope.utility_readiness_logic_present)
        self.assertFalse(scope.permission_enforcement_present)
        self.assertFalse(scope.auth_present)
        self.assertFalse(scope.rbac_abac_present)
        self.assertFalse(scope.persistence_present)
        self.assertFalse(scope.migrations_present)
        self.assertFalse(scope.twin_id_present)
        self.assertFalse(scope.graph_engine_present)
        self.assertFalse(scope.export_present)
        self.assertFalse(scope.operational_behavior_present)

    def test_constraint_risk_reasoning_reports_expected_risk_areas(self):
        view = self._constraint_risk_reasoning_view()

        self.assertTrue(view.constraint_risk_items)
        self.assertTrue(view.missing_equipment_specs)
        self.assertTrue(view.incomplete_topology)
        self.assertTrue(view.low_trust_assumptions)
        self.assertTrue(view.unsupported_load_data)
        self.assertTrue(view.permission_limited_visibility)
        self.assertTrue(view.lifecycle_conflicts)
        self.assertTrue(view.provenance_gaps)
        self.assertTrue(view.contractor_install_complexity_risks)
        self.assertTrue(view.field_verification_needs)
        self.assertTrue(view.professional_review_boundaries)

        risk_areas = {item.risk_area.value for item in view.constraint_risk_items}
        for area in [
            "missing_equipment_specs",
            "incomplete_topology",
            "low_trust_assumptions",
            "unsupported_load_data",
            "permission_limited_visibility",
            "lifecycle_conflicts",
            "provenance_gaps",
            "contractor_install_complexity_risks",
            "field_verification_needs",
            "professional_review_boundaries",
        ]:
            self.assertIn(area, risk_areas)

    def test_constraint_risk_reasoning_items_are_traceable(self):
        view = self._constraint_risk_reasoning_view()

        for source_view_name in [
            "twin_planning_context",
            "topology_snapshot",
            "dependency_impact_readiness",
            "dependency_reasoning",
            "planning_intelligence_readiness",
            "advisory_context_assembly",
        ]:
            self.assertIn(source_view_name, view.source_basis.source_view_names)
        self.assertTrue(view.source_basis.source_section_keys)
        self.assertTrue(view.source_basis.topology_node_ids)
        self.assertTrue(view.source_basis.topology_edge_ids)
        self.assertTrue(view.source_basis.derived_from)

        for item in view.constraint_risk_items:
            self.assertTrue(item.statement)
            self.assertTrue(item.non_decisional_severity_label)
            self.assertTrue(item.observed_constraint_refs or item.missing_inputs or item.low_trust_inputs)
            self.assertTrue(item.basis.source_view_names)
            self.assertIn("advisory_context_assembly", item.basis.source_view_names)
            self.assertTrue(item.basis.derived_from)
            self.assertTrue(item.basis.limitations)
            self.assertTrue(item.confidence_posture)

    def test_constraint_risk_reasoning_surfaces_unsafe_assumptions_and_boundaries(self):
        view = self._constraint_risk_reasoning_view()
        unsafe_text = " ".join(
            assumption
            for item in view.constraint_risk_items
            for assumption in item.unsafe_assumptions
        )
        review_text = " ".join(
            boundary
            for item in view.constraint_risk_items
            for boundary in item.professional_review_boundaries
        )

        self.assertIn("field verification", unsafe_text)
        self.assertIn("permission readiness metadata as authorization", unsafe_text)
        self.assertIn("provenance presence as verification", unsafe_text)
        self.assertIn("final design guidance", unsafe_text)
        self.assertIn("Engineer review remains deferred", review_text)
        self.assertIn("Contractor review remains deferred", review_text)

    def test_constraint_risk_reasoning_preserves_deferred_boundaries(self):
        view = self._constraint_risk_reasoning_view()
        deferred = set(view.deferred_capabilities)

        for boundary in [
            "recommendations",
            "priority_ranking",
            "optimization",
            "scenario_simulation",
            "what_if_analysis",
            "proposal_generation",
            "final_design_guidance",
            "contractor_directives",
            "homeowner_directives",
            "economic_reasoning",
            "utility_readiness_logic",
            "permission_enforcement",
            "auth",
            "rbac_abac",
            "persistence",
            "migrations",
            "twin_id",
            "graph_engine",
            "exports",
            "operational_behavior",
        ]:
            self.assertIn(boundary, deferred)

        limitation_text = " ".join(view.limitations)
        self.assertIn("explains existing constraint and risk context only", limitation_text)
        self.assertIn("not rankings", limitation_text)
        self.assertIn("does not recommend actions", limitation_text)

    def test_constraint_risk_reasoning_is_deterministic_for_same_inputs(self):
        first = self._constraint_risk_reasoning_view().dict()
        second = self._constraint_risk_reasoning_view().dict()

        self.assertEqual(first, second)
        self.assertEqual(
            sorted(first["deferred_capabilities"]),
            first["deferred_capabilities"],
        )
        self.assertEqual(
            sorted(item["risk_area"] for item in first["constraint_risk_items"]),
            [item["risk_area"] for item in first["constraint_risk_items"]],
        )

    def test_constraint_risk_reasoning_keeps_provenance_and_permission_non_authoritative(self):
        view = self._constraint_risk_reasoning_view()
        provenance_item = view.provenance_gaps[0]
        permission_item = view.permission_limited_visibility[0]

        self.assertIn("provenance presence as verification", " ".join(provenance_item.unsafe_assumptions))
        self.assertIn("not_enforced", view.permission_enforcement)
        self.assertIn("permission_readiness_metadata_only", permission_item.confidence_posture)
        self.assertIn("permission_enforcement_layer", permission_item.missing_inputs)
        self.assertIn("permission-readiness metadata", permission_item.statement)
        self.assertFalse(view.reasoning_scope.permission_enforcement_present)

    def test_scenario_comparison_readiness_route_is_additive_and_readiness_only(self):
        paths = {getattr(route, "path", None) for route in app.routes}
        self.assertIn(
            "/api/twin-planning-context/homes/{home_id}/views/scenario-comparison-readiness",
            paths,
        )

        view = self._scenario_comparison_readiness_view()
        payload = view.dict()
        scope = view.readiness_scope

        self.assertEqual("scenario_comparison_readiness", view.view_name)
        self.assertEqual("home_001", view.home_id)
        self.assertEqual("home_id", view.anchor_type)
        self.assertEqual("not_enforced", view.permission_enforcement)
        self.assertEqual("derived", view.authority_layer.value)
        self.assertNotIn("twin_id", payload)
        self.assertTrue(scope.readiness_for_future_comparison_only)
        self.assertTrue(scope.descriptive_only)
        self.assertTrue(scope.read_only)
        self.assertTrue(scope.request_time_only)
        self.assertTrue(scope.home_id_anchored)
        self.assertTrue(scope.derived_from_existing_twin_context)
        self.assertTrue(scope.derived_from_topology_snapshot)
        self.assertTrue(scope.derived_from_planning_intelligence_readiness)
        self.assertTrue(scope.derived_from_advisory_context_assembly)
        self.assertTrue(scope.derived_from_constraint_risk_reasoning)
        self.assertTrue(scope.deterministic_for_same_inputs)
        self.assertIn("readiness for future comparison only", view.implementation_boundary)
        self.assertIn("contracts remain unchanged", view.compatibility_note)

    def test_scenario_comparison_readiness_has_no_forbidden_capability_flags(self):
        scope = self._scenario_comparison_readiness_view().readiness_scope

        self.assertFalse(scope.scenario_comparison_present)
        self.assertFalse(scope.scenario_intelligence_present)
        self.assertFalse(scope.scenario_simulation_present)
        self.assertFalse(scope.what_if_analysis_present)
        self.assertFalse(scope.calculated_changes_present)
        self.assertFalse(scope.option_ordering_present)
        self.assertFalse(scope.optimization_present)
        self.assertFalse(scope.recommendations_present)
        self.assertFalse(scope.propagation_present)
        self.assertFalse(scope.stale_state_persistence_present)
        self.assertFalse(scope.recalculation_present)
        self.assertFalse(scope.invalidation_present)
        self.assertFalse(scope.proposal_generation_present)
        self.assertFalse(scope.persistence_present)
        self.assertFalse(scope.migrations_present)
        self.assertFalse(scope.twin_id_present)
        self.assertFalse(scope.graph_engine_present)
        self.assertFalse(scope.export_present)
        self.assertFalse(scope.operational_behavior_present)

    def test_scenario_comparison_readiness_reports_expected_inventory(self):
        view = self._scenario_comparison_readiness_view()

        self.assertTrue(view.readiness_items)
        self.assertTrue(view.scenario_records_available)
        self.assertTrue(view.scenario_revision_lineage_available)
        self.assertTrue(view.linked_design_reference_readiness)
        self.assertTrue(view.topology_branch_reference_readiness)
        self.assertTrue(view.provenance_basis)
        self.assertTrue(view.permission_readiness_metadata)
        self.assertTrue(view.unsafe_assumptions)
        self.assertTrue(view.confidence_posture)
        self.assertTrue(view.deferred_scenario_boundaries)

        areas = {item.readiness_area.value for item in view.readiness_items}
        for area in [
            "scenario_records_available",
            "revision_lineage_available",
            "linked_design_reference_readiness",
            "topology_branch_reference_readiness",
            "provenance_basis",
            "permission_readiness_metadata",
            "missing_prerequisites",
            "unsafe_assumptions",
            "confidence_posture",
            "deferred_scenario_boundaries",
        ]:
            self.assertIn(area, areas)

    def test_scenario_comparison_readiness_items_are_traceable(self):
        view = self._scenario_comparison_readiness_view()

        for source_view in [
            "twin_planning_context",
            "topology_snapshot",
            "planning_intelligence_readiness",
            "advisory_context_assembly",
            "constraint_risk_reasoning",
        ]:
            self.assertIn(source_view, view.source_basis.source_views)
        self.assertTrue(view.source_basis.source_section_keys)
        self.assertTrue(view.source_basis.scenario_record_refs)
        self.assertTrue(view.source_basis.revision_record_refs)
        self.assertTrue(view.source_basis.topology_branch_refs)
        self.assertTrue(view.source_basis.derived_from)

        for item in view.readiness_items:
            self.assertTrue(item.statement)
            self.assertTrue(item.posture)
            self.assertTrue(item.basis.source_views)
            self.assertTrue(item.basis.derived_from)
            self.assertTrue(item.basis.limitations)
            self.assertTrue(item.available or item.missing or item.blocked_deferred)
            self.assertIn("twin_planning_context", item.basis.source_views)

    def test_scenario_comparison_readiness_preserves_readiness_only_language(self):
        view = self._scenario_comparison_readiness_view()
        response_text = str(view.dict())

        self.assertIn("readiness for future comparison", response_text)
        self.assertIn("blocked/deferred", response_text)
        self.assertIn("unsafe", response_text)
        self.assertIn("basis", response_text)
        for forbidden in [
            "better",
            "worse",
            "delta",
            "score:",
            "rank:",
            "selected",
            "recommended:",
            "outcome",
            "projection",
        ]:
            self.assertNotIn(forbidden, response_text)

    def test_scenario_comparison_readiness_preserves_deferred_boundaries(self):
        view = self._scenario_comparison_readiness_view()
        deferred = set(view.deferred_scenario_boundaries)

        for boundary in [
            "scenario_comparison",
            "scenario_intelligence",
            "scenario_simulation",
            "what_if_analysis",
            "calculated_change_analysis",
            "option_ordering",
            "optimization",
            "recommendations",
            "change_propagation",
            "stale_state_persistence",
            "recalculation",
            "invalidation",
            "proposal_generation",
            "persistence",
            "migrations",
            "twin_id",
            "graph_engine",
            "exports",
            "operational_behavior",
        ]:
            self.assertIn(boundary, deferred)

        limitation_text = " ".join(view.limitations)
        self.assertIn("readiness for future comparison only", limitation_text)
        self.assertIn("does not compare", limitation_text)

    def test_scenario_comparison_readiness_is_deterministic_for_same_inputs(self):
        first = self._scenario_comparison_readiness_view().dict()
        second = self._scenario_comparison_readiness_view().dict()

        self.assertEqual(first, second)
        self.assertEqual(
            sorted(first["deferred_scenario_boundaries"]),
            first["deferred_scenario_boundaries"],
        )
        self.assertEqual(
            sorted(item["readiness_area"] for item in first["readiness_items"]),
            [item["readiness_area"] for item in first["readiness_items"]],
        )

    def test_scenario_comparison_readiness_keeps_provenance_and_permission_non_authoritative(self):
        view = self._scenario_comparison_readiness_view()
        provenance_item = view.provenance_basis[0]
        permission_item = view.permission_readiness_metadata[0]

        self.assertIn("not verification", provenance_item.statement)
        self.assertIn("permission_enforcement_layer", permission_item.missing)
        self.assertIn("not_enforced", view.permission_enforcement)
        self.assertFalse(view.readiness_scope.permission_enforcement_present)
        self.assertFalse(view.readiness_scope.export_present)

    def test_pre_recommendation_advisory_route_is_additive_and_read_only(self):
        paths = {getattr(route, "path", None) for route in app.routes}
        self.assertIn(
            "/api/twin-planning-context/homes/{home_id}/views/pre-recommendation-advisory",
            paths,
        )

        view = self._pre_recommendation_advisory_view()
        payload = view.dict()
        scope = view.advisory_scope

        self.assertEqual("pre_recommendation_advisory", view.view_name)
        self.assertEqual("home_001", view.home_id)
        self.assertEqual("home_id", view.anchor_type)
        self.assertEqual("not_enforced", view.permission_enforcement)
        self.assertEqual("derived", view.authority_layer.value)
        self.assertNotIn("twin_id", payload)
        self.assertTrue(scope.pre_recommendation_advisory_only)
        self.assertTrue(scope.explanatory_only)
        self.assertTrue(scope.read_only)
        self.assertTrue(scope.request_time_only)
        self.assertTrue(scope.home_id_anchored)
        self.assertTrue(scope.derived_from_existing_twin_context)
        self.assertTrue(scope.derived_from_topology_snapshot)
        self.assertTrue(scope.derived_from_planning_intelligence_readiness)
        self.assertTrue(scope.derived_from_advisory_context_assembly)
        self.assertTrue(scope.derived_from_constraint_risk_reasoning)
        self.assertTrue(scope.derived_from_scenario_comparison_readiness)
        self.assertTrue(scope.deterministic_for_same_inputs)
        self.assertIn("pre-recommendation advisory view", view.implementation_boundary)
        self.assertIn("contracts remain unchanged", view.compatibility_note)

    def test_pre_recommendation_advisory_has_no_forbidden_capabilities(self):
        scope = self._pre_recommendation_advisory_view().advisory_scope

        self.assertFalse(scope.recommendations_generated)
        self.assertFalse(scope.recommendation_ranking_present)
        self.assertFalse(scope.best_option_selection_present)
        self.assertFalse(scope.optimization_present)
        self.assertFalse(scope.simulation_present)
        self.assertFalse(scope.scenario_comparison_present)
        self.assertFalse(scope.calculated_changes_present)
        self.assertFalse(scope.final_design_guidance_present)
        self.assertFalse(scope.proposal_generation_present)
        self.assertFalse(scope.economic_reasoning_present)
        self.assertFalse(scope.utility_readiness_logic_present)
        self.assertFalse(scope.contractor_directives_present)
        self.assertFalse(scope.homeowner_directives_present)
        self.assertFalse(scope.permission_enforcement_present)
        self.assertFalse(scope.auth_present)
        self.assertFalse(scope.rbac_abac_present)
        self.assertFalse(scope.persistence_present)
        self.assertFalse(scope.migrations_present)
        self.assertFalse(scope.twin_id_present)
        self.assertFalse(scope.graph_engine_present)
        self.assertFalse(scope.export_present)
        self.assertFalse(scope.operational_behavior_present)

    def test_pre_recommendation_advisory_reports_expected_sections(self):
        view = self._pre_recommendation_advisory_view()

        self.assertTrue(view.advisory_items)
        self.assertTrue(view.advice_eligible_areas)
        self.assertTrue(view.advice_blocked_areas)
        self.assertTrue(view.missing_data_before_advice)
        self.assertTrue(view.unsafe_assumptions)
        self.assertTrue(view.professional_verification_boundaries)
        self.assertTrue(view.provenance_basis)
        self.assertTrue(view.permission_readiness_basis)
        self.assertTrue(view.advisory_limitations)
        self.assertTrue(view.deferred_recommendation_boundaries)

        areas = {item.advisory_area.value for item in view.advisory_items}
        for area in [
            "advice_eligible_areas",
            "advice_blocked_areas",
            "missing_data_before_advice",
            "unsafe_assumptions",
            "professional_verification_boundaries",
            "provenance_basis",
            "permission_readiness_basis",
            "advisory_limitations",
            "deferred_recommendation_boundaries",
        ]:
            self.assertIn(area, areas)

    def test_pre_recommendation_advisory_items_are_traceable(self):
        view = self._pre_recommendation_advisory_view()

        for source_view in [
            "twin_planning_context",
            "topology_snapshot",
            "planning_intelligence_readiness",
            "advisory_context_assembly",
            "constraint_risk_reasoning",
            "scenario_comparison_readiness",
        ]:
            self.assertIn(source_view, view.source_basis.source_views)
        self.assertTrue(view.source_basis.source_section_keys)
        self.assertTrue(view.source_basis.advisory_area_refs)
        self.assertTrue(view.source_basis.constraint_refs)
        self.assertTrue(view.source_basis.scenario_readiness_refs)
        self.assertTrue(view.source_basis.derived_from)

        for item in view.advisory_items:
            self.assertTrue(item.statement)
            self.assertTrue(item.posture)
            self.assertTrue(item.basis.source_views)
            self.assertTrue(item.basis.derived_from)
            self.assertTrue(item.basis.limitations)
            self.assertTrue(item.available_basis or item.missing_data or item.blocked_deferred)
            self.assertIn("twin_planning_context", item.basis.source_views)

    def test_pre_recommendation_advisory_preserves_deferred_boundaries(self):
        view = self._pre_recommendation_advisory_view()
        deferred = set(view.deferred_recommendation_boundaries)

        for boundary in [
            "recommendation_generation",
            "recommendation_ranking",
            "best_option_selection",
            "optimization",
            "simulation",
            "scenario_comparison",
            "calculated_change_analysis",
            "final_design_guidance",
            "proposal_generation",
            "economic_reasoning",
            "utility_readiness_logic",
            "contractor_directives",
            "homeowner_directives",
            "permission_enforcement",
            "auth",
            "rbac_abac",
            "persistence",
            "migrations",
            "twin_id",
            "graph_engine",
            "exports",
            "operational_behavior",
        ]:
            self.assertIn(boundary, deferred)

        limitation_text = " ".join(view.advisory_limitations)
        self.assertIn("does not generate recommendations", limitation_text)
        self.assertIn("pre-recommendation advisory explanation only", limitation_text)

    def test_pre_recommendation_advisory_is_deterministic_for_same_inputs(self):
        first = self._pre_recommendation_advisory_view().dict()
        second = self._pre_recommendation_advisory_view().dict()

        self.assertEqual(first, second)
        self.assertEqual(
            sorted(first["deferred_recommendation_boundaries"]),
            first["deferred_recommendation_boundaries"],
        )
        self.assertEqual(
            sorted(item["advisory_area"] for item in first["advisory_items"]),
            [item["advisory_area"] for item in first["advisory_items"]],
        )

    def test_pre_recommendation_advisory_keeps_trust_boundaries_visible(self):
        view = self._pre_recommendation_advisory_view()
        provenance_item = view.provenance_basis[0]
        permission_item = view.permission_readiness_basis[0]
        professional_item = view.professional_verification_boundaries[0]

        self.assertIn("not verification", provenance_item.statement)
        self.assertIn("permission_enforcement_layer", permission_item.missing_data)
        self.assertIn("Professional verification", professional_item.statement)
        self.assertIn("Engineer review remains deferred.", professional_item.professional_boundaries)
        self.assertFalse(view.advisory_scope.recommendations_generated)
        self.assertFalse(view.advisory_scope.permission_enforcement_present)

    def test_recommendation_eligibility_readiness_route_is_additive_and_read_only(self):
        paths = {getattr(route, "path", None) for route in app.routes}
        self.assertIn(
            "/api/twin-planning-context/homes/{home_id}/views/recommendation-eligibility-readiness",
            paths,
        )

        view = self._recommendation_eligibility_readiness_view()
        payload = view.dict()
        scope = view.eligibility_scope

        self.assertEqual("recommendation_eligibility_readiness", view.view_name)
        self.assertEqual("home_001", view.home_id)
        self.assertEqual("home_id", view.anchor_type)
        self.assertEqual("not_enforced", view.permission_enforcement)
        self.assertEqual("derived", view.authority_layer.value)
        self.assertNotIn("twin_id", payload)
        self.assertTrue(scope.eligibility_readiness_gate_only)
        self.assertTrue(scope.readiness_posture_only)
        self.assertTrue(scope.read_only)
        self.assertTrue(scope.request_time_only)
        self.assertTrue(scope.home_id_anchored)
        self.assertTrue(scope.derived_from_existing_twin_context)
        self.assertTrue(scope.derived_from_topology_snapshot)
        self.assertTrue(scope.derived_from_planning_intelligence_readiness)
        self.assertTrue(scope.derived_from_advisory_context_assembly)
        self.assertTrue(scope.derived_from_constraint_risk_reasoning)
        self.assertTrue(scope.derived_from_scenario_comparison_readiness)
        self.assertTrue(scope.derived_from_pre_recommendation_advisory)
        self.assertTrue(scope.deterministic_for_same_inputs)
        self.assertIn("recommendation eligibility readiness view", view.implementation_boundary)
        self.assertIn("contracts remain unchanged", view.compatibility_note)

    def test_recommendation_eligibility_readiness_has_no_forbidden_capability_flags(self):
        scope = self._recommendation_eligibility_readiness_view().eligibility_scope

        self.assertFalse(scope.recommendations_generated)
        self.assertFalse(scope.advisor_profile_choice_present)
        self.assertFalse(scope.ranking_present)
        self.assertFalse(scope.best_option_selection_present)
        self.assertFalse(scope.optimization_present)
        self.assertFalse(scope.simulation_present)
        self.assertFalse(scope.scenario_comparison_present)
        self.assertFalse(scope.outcome_calculation_present)
        self.assertFalse(scope.proposal_generation_present)
        self.assertFalse(scope.economic_reasoning_present)
        self.assertFalse(scope.utility_readiness_reasoning_present)
        self.assertFalse(scope.contractor_directives_present)
        self.assertFalse(scope.homeowner_directives_present)
        self.assertFalse(scope.permission_enforcement_present)
        self.assertFalse(scope.auth_present)
        self.assertFalse(scope.rbac_abac_present)
        self.assertFalse(scope.persistence_present)
        self.assertFalse(scope.migrations_present)
        self.assertFalse(scope.twin_id_present)
        self.assertFalse(scope.graph_engine_present)
        self.assertFalse(scope.export_present)
        self.assertFalse(scope.operational_behavior_present)

    def test_recommendation_eligibility_readiness_reports_eligible_and_blocked_categories(self):
        view = self._recommendation_eligibility_readiness_view()

        self.assertTrue(view.eligibility_items)
        self.assertTrue(view.eligible_for_future_recommendation)
        self.assertTrue(view.blocked_deferred_categories)
        self.assertTrue(view.missing_prerequisites)
        self.assertTrue(view.provenance_sufficiency)
        self.assertTrue(view.topology_sufficiency)
        self.assertTrue(view.equipment_spec_sufficiency)
        self.assertTrue(view.permission_readiness_basis)
        self.assertTrue(view.professional_review_boundaries)
        self.assertTrue(view.unsafe_assumptions)
        self.assertTrue(view.deferred_recommendation_generation_boundaries)

        areas = {item.eligibility_area.value for item in view.eligibility_items}
        for area in [
            "topology_sufficiency",
            "equipment_spec_sufficiency",
            "load_data_sufficiency",
            "provenance_sufficiency",
            "permission_readiness_basis",
            "professional_review_boundaries",
            "scenario_readiness",
            "pre_recommendation_boundary",
            "derived_advisor_context",
            "deferred_recommendation_generation",
        ]:
            self.assertIn(area, areas)

    def test_recommendation_eligibility_readiness_items_are_traceable(self):
        view = self._recommendation_eligibility_readiness_view()

        for source_view in [
            "twin_planning_context",
            "topology_snapshot",
            "planning_intelligence_readiness",
            "advisory_context_assembly",
            "constraint_risk_reasoning",
            "scenario_comparison_readiness",
            "pre_recommendation_advisory",
        ]:
            self.assertIn(source_view, view.source_basis.source_views)
        self.assertTrue(view.source_basis.source_section_keys)
        self.assertTrue(view.source_basis.eligibility_category_refs)
        self.assertTrue(view.source_basis.eligible_basis_refs)
        self.assertTrue(view.source_basis.blocked_basis_refs)
        self.assertTrue(view.source_basis.derived_from)

        for item in view.eligibility_items:
            self.assertTrue(item.statement)
            self.assertTrue(item.eligibility_posture)
            self.assertTrue(item.basis.source_views)
            self.assertTrue(item.basis.derived_from)
            self.assertTrue(item.basis.limitations)
            self.assertTrue(
                item.eligible_basis
                or item.blocked_deferred
                or item.missing_prerequisites
                or item.unsafe_assumptions
            )
            self.assertIn("twin_planning_context", item.basis.source_views)

    def test_recommendation_eligibility_readiness_preserves_trust_boundaries(self):
        view = self._recommendation_eligibility_readiness_view()
        provenance_item = view.provenance_sufficiency[0]
        permission_item = view.permission_readiness_basis[0]
        professional_item = view.professional_review_boundaries[0]

        limitation_text = " ".join(view.limitations)
        self.assertIn("Eligibility means readiness posture only.", limitation_text)
        self.assertIn(
            "Eligibility is not permission, approval, engineering review, authority, or recommendation generation.",
            limitation_text,
        )
        self.assertIn("not verification", provenance_item.statement)
        self.assertIn("permission_enforcement_layer", permission_item.missing_prerequisites)
        self.assertIn("metadata only", permission_item.statement)
        self.assertIn("Professional review remains deferred", professional_item.statement)
        self.assertFalse(view.eligibility_scope.recommendations_generated)
        self.assertFalse(view.eligibility_scope.permission_enforcement_present)

    def test_recommendation_eligibility_readiness_preserves_deferred_boundaries(self):
        view = self._recommendation_eligibility_readiness_view()
        deferred = set(view.deferred_recommendation_generation_boundaries)

        for boundary in [
            "recommendation_generation",
            "advisor_profile_choice",
            "recommendation_ranking",
            "best_option_selection",
            "optimization",
            "simulation",
            "scenario_comparison",
            "outcome_calculation",
            "proposal_generation",
            "economic_reasoning",
            "utility_readiness_reasoning",
            "contractor_directives",
            "homeowner_directives",
            "permission_enforcement",
            "auth",
            "rbac_abac",
            "persistence",
            "migrations",
            "twin_id",
            "graph_engine",
            "exports",
            "operational_behavior",
        ]:
            self.assertIn(boundary, deferred)

        boundary_text = " ".join(view.deferred_recommendation_generation_boundaries)
        self.assertNotIn("selected", boundary_text)

    def test_recommendation_eligibility_readiness_is_deterministic_for_same_inputs(self):
        first = self._recommendation_eligibility_readiness_view().dict()
        second = self._recommendation_eligibility_readiness_view().dict()

        self.assertEqual(first, second)
        self.assertEqual(
            sorted(first["deferred_recommendation_generation_boundaries"]),
            first["deferred_recommendation_generation_boundaries"],
        )
        self.assertEqual(
            sorted(item["eligibility_area"] for item in first["eligibility_items"]),
            [item["eligibility_area"] for item in first["eligibility_items"]],
        )

    def test_recommendation_eligibility_readiness_does_not_expose_current_recommendations(self):
        view = self._recommendation_eligibility_readiness_view()
        payload_text = str(view.dict())
        advisor_item = next(
            item
            for item in view.eligibility_items
            if item.eligibility_area.value == "derived_advisor_context"
        )

        self.assertIn(
            "existing_derived_advisor_context_records",
            " ".join(advisor_item.basis.advisor_derived_context_refs),
        )
        self.assertIn("not as current recommended outputs or choices", advisor_item.statement)
        self.assertNotIn("recommended_profile", payload_text)
        self.assertNotIn("Advisor recommendation summary for", payload_text)
        self.assertFalse(view.eligibility_scope.recommendations_generated)


if __name__ == "__main__":
    unittest.main()

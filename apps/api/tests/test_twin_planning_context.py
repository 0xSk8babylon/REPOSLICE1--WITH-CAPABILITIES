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

    def test_topology_snapshot_preserves_deferred_boundaries(self):
        snapshot = self._topology_snapshot()
        limitation_text = " ".join(snapshot.limitations)
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

        self.assertNotIn("twin_id", payload)
        self.assertTrue(all(node.permission_not_enforced for node in snapshot.nodes))
        self.assertTrue(
            all("not create installation" in " ".join(node.limitations) for node in snapshot.nodes)
        )


if __name__ == "__main__":
    unittest.main()

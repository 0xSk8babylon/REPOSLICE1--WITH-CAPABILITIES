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

    def test_ai_design_grounding_view_returns_none_for_design_outside_home_context(self):
        self.assertIsNone(self._ai_view("missing_design"))


if __name__ == "__main__":
    unittest.main()

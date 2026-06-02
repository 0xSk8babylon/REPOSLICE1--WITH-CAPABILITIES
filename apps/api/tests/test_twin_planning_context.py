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
        self.assertIn("No twin_id is created or inferred.", payload["limitations"])


if __name__ == "__main__":
    unittest.main()

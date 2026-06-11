import unittest

from tests.fast_db import reset_and_reseed  # noqa: E402  must precede app imports

from app.core.database import engine  # noqa: E402
from app.core.repository import repository  # noqa: E402
from app.scenarios.schemas import ScenarioCreate, ScenarioUpdate  # noqa: E402
from app.scenarios.router import create_scenario, list_scenarios, update_scenario  # noqa: E402
from app.services.design_advisor import design_advisor_service  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402


class ScenarioRevisionFoundationTests(unittest.TestCase):
    def setUp(self):
        reset_and_reseed()

    def test_seeded_scenarios_receive_baseline_revisions(self):
        with Session(engine) as db:
            scenarios = list_scenarios(db)

        scenario_map = {scenario["id"]: scenario for scenario in scenarios}
        self.assertEqual(2, len(scenarios))
        self.assertEqual(1, scenario_map["scenario_001"]["revision_overview"]["revision_count"])
        self.assertEqual("Revision 1", scenario_map["scenario_001"]["revision_overview"]["latest_revision_label"])
        self.assertEqual(
            "seeded_baseline_revision",
            scenario_map["scenario_001"]["revision_overview"]["latest_revision_status"],
        )
        self.assertEqual(1, len(scenario_map["scenario_001"]["revisions"]))
        self.assertEqual(
            "balanced",
            scenario_map["scenario_001"]["revisions"][0]["recommended_profile_snapshot"],
        )

    def test_create_and_update_scenario_capture_immutable_revisions(self):
        payload = ScenarioCreate(
            id="scenario_003",
            home_id="home_001",
            name="Saved Future Upgrade Path",
            description="Planning state kept for later comparison.",
            linked_design_id="design_001",
            upfront_cost_placeholder=31000,
            future_expansion_score=0.76,
            install_complexity_score=0.31,
            backup_capability_score=0.62,
            notes="First saved scenario revision.",
        )

        with Session(engine) as db:
            scenario = create_scenario(payload, db)
            self.assertEqual(1, scenario["revision_overview"]["revision_count"])
            self.assertEqual("Revision 1", scenario["revision_overview"]["latest_revision_label"])

            updated = update_scenario(
                "scenario_003",
                ScenarioUpdate(notes="Second saved revision", linked_design_id="design_002"),
                db,
            )

        self.assertEqual(2, updated["revision_overview"]["revision_count"])
        self.assertEqual("Revision 2", updated["revision_overview"]["latest_revision_label"])
        self.assertEqual(2, len(updated["revisions"]))
        latest_revision = updated["revisions"][0]
        previous_revision = updated["revisions"][1]
        self.assertEqual("scenario_003_rev_002", latest_revision["id"])
        self.assertEqual("scenario_003_rev_001", latest_revision["parent_revision_id"])
        self.assertEqual("design_002", latest_revision["linked_design_id"])
        self.assertEqual("premium_future_ready", latest_revision["recommended_profile_snapshot"])
        self.assertEqual("design_001", previous_revision["linked_design_id"])

    def test_planning_state_links_latest_revision_metadata_for_saved_scenarios(self):
        with Session(engine) as db:
            scenario = repository.get_scenario_model(db, "scenario_001")
            linked_design_id = scenario.linked_design_id
            update_scenario("scenario_001", ScenarioUpdate(notes="Revised for history"), db)
            advisor = design_advisor_service.explain(db, linked_design_id)

        linked_scenarios = advisor["planning_state"].linked_scenarios
        scenario_link = next(link for link in linked_scenarios if link.scenario_id == "scenario_001")
        self.assertEqual("scenario_001_rev_002", scenario_link.latest_revision_id)
        self.assertEqual("Revision 2", scenario_link.latest_revision_label)
        self.assertEqual(2, scenario_link.latest_revision_number)


if __name__ == "__main__":
    unittest.main()

import os
import unittest
from pathlib import Path

os.environ.setdefault("DATA_DIR", "/tmp/residential-energy-planner-tests")
os.environ.setdefault("DATABASE_FILE", "resilience_recommendation_test.sqlite3")

from app.core.database import database_path, engine  # noqa: E402
from app.seed.runtime import reset_and_reseed  # noqa: E402
from app.services.design_advisor import design_advisor_service  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402


class ResilienceRecommendationRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db_path = Path(database_path())
        db_path.parent.mkdir(parents=True, exist_ok=True)
        if db_path.exists():
            db_path.unlink()
        reset_and_reseed()

    def _advisor_summary(self, design_id: str):
        with Session(engine) as db:
            return design_advisor_service.explain(db, design_id)

    def test_design_001_panel_service_stays_partial_home_planning_direction(self):
        result = self._advisor_summary("design_001")
        recommendation = result["recommendation_profiles"]
        panel_service = recommendation.panel_service_architecture

        self.assertEqual("balanced", recommendation.recommended_profile.value)
        self.assertEqual("high", recommendation.confidence_level.value)
        self.assertEqual("partial-home backup", panel_service.recommended_backup_architecture)
        self.assertEqual("conditional", panel_service.partial_home_backup_suitability)
        self.assertEqual("poor", panel_service.whole_home_backup_suitability)
        self.assertIn("Planning estimate only.", panel_service.scope_note)
        self.assertEqual("high", panel_service.inspectability.confidence_level.value)

    def test_design_002_panel_service_stays_future_ready_and_planning_only(self):
        result = self._advisor_summary("design_002")
        recommendation = result["recommendation_profiles"]
        panel_service = recommendation.panel_service_architecture

        self.assertEqual("premium_future_ready", recommendation.recommended_profile.value)
        self.assertEqual("future-ready service upgrade path", panel_service.recommended_backup_architecture)
        self.assertEqual("limited", panel_service.partial_home_backup_suitability)
        self.assertEqual("poor", panel_service.whole_home_backup_suitability)
        self.assertIn("Generator-related tie-in signals exist", panel_service.generator_integration_readiness_note)
        self.assertEqual("derived_estimate", panel_service.inspectability.trust_state.value)
        self.assertTrue(panel_service.inspectability.partial_provenance_warning)

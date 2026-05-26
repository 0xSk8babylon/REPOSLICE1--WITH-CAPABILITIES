import os
import unittest
from pathlib import Path

os.environ.setdefault("DATA_DIR", "/tmp/residential-energy-planner-tests")
os.environ.setdefault("DATABASE_FILE", "resilience_recommendation_test.sqlite3")

from app.core.database import database_path, engine  # noqa: E402
from app.core.models import EnergySystemDesign, Load  # noqa: E402
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

    def setUp(self):
        reset_and_reseed()

    def _advisor_summary(self, design_id: str):
        with Session(engine) as db:
            return design_advisor_service.explain(db, design_id)

    def test_design_001_backup_scope_stays_partial_home_and_high_confidence(self):
        result = self._advisor_summary("design_001")
        recommendation = result["recommendation_profiles"]
        selection = recommendation.backup_load_selection
        panel_service = recommendation.panel_service_architecture
        inverter_architecture = recommendation.inverter_system_architecture
        balanced_profile = next(profile for profile in recommendation.profiles if profile.profile.value == "balanced")

        self.assertEqual("balanced", recommendation.recommended_profile.value)
        self.assertEqual("high", recommendation.confidence_level.value)
        self.assertEqual("partial-home outage posture", selection.outage_posture)
        self.assertEqual("high", selection.confidence_level.value)
        self.assertEqual(0.67, selection.coverage_ratio_of_recorded_loads)
        self.assertEqual("partial-home backup", panel_service.recommended_backup_architecture)
        self.assertEqual("aligned", panel_service.architecture_consistency.status)
        self.assertEqual("aligned", balanced_profile.architecture_fit.status)
        self.assertIn("partial-home planning posture", balanced_profile.architecture_fit.summary)
        self.assertIn("Battery equipment is already recorded", balanced_profile.architecture_fit.equipment_mix_summary)
        self.assertIn("recommendation.profile_architecture_fit_v1", balanced_profile.inspectability.rule_keys)
        self.assertEqual("conditional", panel_service.partial_home_backup_suitability)
        self.assertEqual("poor", panel_service.whole_home_backup_suitability)
        self.assertIn("Planning estimate only.", panel_service.scope_note)
        self.assertEqual("high", panel_service.inspectability.confidence_level.value)
        self.assertEqual("ac coupled", inverter_architecture.recorded_architecture_type)
        self.assertEqual("battery-ready path needs inverter clarification", inverter_architecture.recommended_system_architecture)
        self.assertEqual("favorable", inverter_architecture.ac_coupled_pathway_suitability)
        self.assertEqual("conditional", inverter_architecture.hybrid_inverter_pathway_suitability)
        self.assertEqual("conditional", inverter_architecture.architecture_consistency.status)
        self.assertIn("recommendation.inverter_system_architecture_v1", inverter_architecture.inspectability.rule_keys)

    def test_design_002_panel_service_stays_future_ready_and_planning_only(self):
        result = self._advisor_summary("design_002")
        recommendation = result["recommendation_profiles"]
        panel_service = recommendation.panel_service_architecture
        inverter_architecture = recommendation.inverter_system_architecture
        premium_profile = next(
            profile for profile in recommendation.profiles if profile.profile.value == "premium_future_ready"
        )

        self.assertEqual("premium_future_ready", recommendation.recommended_profile.value)
        self.assertEqual("future-ready service upgrade path", panel_service.recommended_backup_architecture)
        self.assertEqual("limited", panel_service.partial_home_backup_suitability)
        self.assertEqual("poor", panel_service.whole_home_backup_suitability)
        self.assertEqual("aligned", panel_service.architecture_consistency.status)
        self.assertEqual("aligned", premium_profile.architecture_fit.status)
        self.assertIn("broader architecture and expansion posture", premium_profile.architecture_fit.summary)
        self.assertIn("Hybrid inverter and generator signals", premium_profile.architecture_fit.equipment_mix_summary)
        self.assertIn("Generator-related tie-in signals exist", panel_service.generator_integration_readiness_note)
        self.assertEqual("derived_estimate", panel_service.inspectability.trust_state.value)
        self.assertTrue(panel_service.inspectability.partial_provenance_warning)
        self.assertEqual("hybrid", inverter_architecture.recorded_architecture_type)
        self.assertEqual("hybrid inverter backbone", inverter_architecture.recommended_system_architecture)
        self.assertEqual("limited", inverter_architecture.ac_coupled_pathway_suitability)
        self.assertEqual("favorable", inverter_architecture.hybrid_inverter_pathway_suitability)
        self.assertEqual("aligned", inverter_architecture.architecture_consistency.status)

    def test_whole_home_goal_stays_conditional_when_grouping_is_only_partial_home(self):
        with Session(engine) as db:
            design = db.get(EnergySystemDesign, "design_001")
            design.design_goal = "whole_home_backup"
            db.commit()

        result = self._advisor_summary("design_001")
        recommendation = result["recommendation_profiles"]
        selection = recommendation.backup_load_selection
        panel_service = recommendation.panel_service_architecture
        inverter_architecture = recommendation.inverter_system_architecture

        self.assertEqual("premium_future_ready", recommendation.recommended_profile.value)
        self.assertEqual("partial-home outage posture", selection.outage_posture)
        self.assertEqual("future-ready service upgrade path", panel_service.recommended_backup_architecture)
        self.assertEqual("conditional", panel_service.architecture_consistency.status)
        self.assertIn("intentionally narrower than the design goal", panel_service.architecture_consistency.summary)
        self.assertEqual("battery-ready path needs inverter clarification", inverter_architecture.recommended_system_architecture)
        premium_profile = next(
            profile for profile in recommendation.profiles if profile.profile.value == "premium_future_ready"
        )
        self.assertTrue(
            any(
                "should not be treated as evidence of whole-home readiness" in item
                for item in premium_profile.architecture_fit.warnings
            )
        )

    def test_whole_home_candidate_can_resolve_to_whole_home_backup_direction(self):
        with Session(engine) as db:
            design = db.get(EnergySystemDesign, "design_001")
            design.design_goal = "whole_home_backup"
            workshop_load = db.get(Load, "load_003")
            workshop_load.backup_priority = "preferred"
            db.commit()

        result = self._advisor_summary("design_001")
        recommendation = result["recommendation_profiles"]
        selection = recommendation.backup_load_selection
        panel_service = recommendation.panel_service_architecture
        inverter_architecture = recommendation.inverter_system_architecture

        self.assertEqual("premium_future_ready", recommendation.recommended_profile.value)
        self.assertEqual("whole-home outage posture candidate", selection.outage_posture)
        self.assertEqual(1.0, selection.coverage_ratio_of_recorded_loads)
        self.assertEqual("future-ready service upgrade path", panel_service.recommended_backup_architecture)
        self.assertEqual("aligned", panel_service.architecture_consistency.status)
        self.assertEqual("battery-ready path needs inverter clarification", inverter_architecture.recommended_system_architecture)

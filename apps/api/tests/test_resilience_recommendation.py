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
        current_architecture = recommendation.current_home_energy_architecture
        panel_service = recommendation.panel_service_architecture
        inverter_architecture = recommendation.inverter_system_architecture
        balanced_profile = next(profile for profile in recommendation.profiles if profile.profile.value == "balanced")

        self.assertEqual("balanced", recommendation.recommended_profile.value)
        self.assertEqual("high", recommendation.confidence_level.value)
        self.assertEqual("partial-home outage posture", selection.outage_posture)
        self.assertEqual("high", selection.confidence_level.value)
        self.assertEqual(0.67, selection.coverage_ratio_of_recorded_loads)
        self.assertEqual("existing solar recorded", current_architecture.solar_existing_state)
        self.assertEqual("microinverter system", current_architecture.inverter_topology)
        self.assertEqual("high", current_architecture.topology_confidence.value)
        self.assertIn("Current home energy architecture reads as microinverter system", current_architecture.current_vs_proposed_architecture)
        self.assertIn("Do not assume the recorded solar array can operate during an outage", current_architecture.outage_solar_behavior_note)
        self.assertIn("AC-coupled battery retrofit", current_architecture.battery_retrofit_implication)
        self.assertEqual("partial-home backup", panel_service.recommended_backup_architecture)
        self.assertEqual("aligned", panel_service.architecture_consistency.status)
        self.assertEqual("aligned", balanced_profile.architecture_fit.status)
        self.assertIn("partial-home planning posture", balanced_profile.architecture_fit.summary)
        self.assertIn("Existing microinverter solar plus recorded battery signals", balanced_profile.architecture_fit.equipment_mix_summary)
        self.assertIn("recommendation.profile_architecture_fit_v1", balanced_profile.inspectability.rule_keys)
        self.assertEqual("conditional", panel_service.partial_home_backup_suitability)
        self.assertEqual("poor", panel_service.whole_home_backup_suitability)
        self.assertIn("Planning estimate only.", panel_service.scope_note)
        self.assertEqual("high", panel_service.inspectability.confidence_level.value)
        self.assertEqual("ac coupled", inverter_architecture.recorded_architecture_type)
        self.assertEqual("ac-coupled battery retrofit path", inverter_architecture.recommended_system_architecture)
        self.assertEqual("favorable", inverter_architecture.ac_coupled_pathway_suitability)
        self.assertEqual("conditional", inverter_architecture.hybrid_inverter_pathway_suitability)
        self.assertEqual("aligned", inverter_architecture.architecture_consistency.status)
        self.assertIn("recommendation.inverter_system_architecture_v1", inverter_architecture.inspectability.rule_keys)

    def test_design_002_panel_service_stays_future_ready_and_planning_only(self):
        result = self._advisor_summary("design_002")
        recommendation = result["recommendation_profiles"]
        current_architecture = recommendation.current_home_energy_architecture
        panel_service = recommendation.panel_service_architecture
        inverter_architecture = recommendation.inverter_system_architecture
        premium_profile = next(
            profile for profile in recommendation.profiles if profile.profile.value == "premium_future_ready"
        )

        self.assertEqual("premium_future_ready", recommendation.recommended_profile.value)
        self.assertEqual("proposed solar only recorded", current_architecture.solar_existing_state)
        self.assertEqual("unknown / not recorded topology", current_architecture.inverter_topology)
        self.assertEqual("low", current_architecture.topology_confidence.value)
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
        self.assertEqual("ac-coupled battery retrofit path", inverter_architecture.recommended_system_architecture)
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
        self.assertEqual("ac-coupled battery retrofit path", inverter_architecture.recommended_system_architecture)

    def test_reasoning_graph_exposes_recommended_profile_dependencies_for_design_001(self):
        result = self._advisor_summary("design_001")
        recommendation = result["recommendation_profiles"]
        reasoning_graph = recommendation.reasoning_graph

        self.assertIsNotNone(reasoning_graph)
        self.assertEqual("Recommended profile: Balanced", reasoning_graph.scope_label)
        self.assertIn("dependency graph", reasoning_graph.summary)
        self.assertEqual(7, len(reasoning_graph.nodes))
        self.assertEqual(10, len(reasoning_graph.dependencies))
        self.assertIn("recommendation.system_reasoning_graph_v1", reasoning_graph.inspectability.rule_keys)

        node_map = {node.node_id: node for node in reasoning_graph.nodes}
        self.assertEqual("partial-home outage posture", node_map["backup_scope"].status)
        self.assertEqual("microinverter system", node_map["current_topology"].status)
        self.assertEqual("partial-home backup", node_map["panel_service"].status)
        self.assertEqual("ac-coupled battery retrofit path", node_map["inverter_system"].status)
        self.assertEqual("balanced", node_map["battery_posture"].status)
        self.assertEqual("resilience_balanced", node_map["solar_posture"].status)

        dependency_map = {
            (dependency.source_node_id, dependency.target_node_id): dependency for dependency in reasoning_graph.dependencies
        }
        self.assertEqual("grounds outage posture", dependency_map[("loads", "backup_scope")].relationship)
        self.assertIn(
            "bounded by the selected outage posture",
            dependency_map[("backup_scope", "panel_service")].summary.lower(),
        )
        self.assertEqual("grounds current-state pathway", dependency_map[("current_topology", "inverter_system")].relationship)
        self.assertIn(
            "recommendation.system_reasoning_graph_v1",
            dependency_map[("battery_posture", "solar_posture")].rule_keys,
        )

    def test_reasoning_graph_tracks_hybrid_path_for_design_002(self):
        result = self._advisor_summary("design_002")
        recommendation = result["recommendation_profiles"]
        reasoning_graph = recommendation.reasoning_graph
        node_map = {node.node_id: node for node in reasoning_graph.nodes}
        dependency_map = {
            (dependency.source_node_id, dependency.target_node_id): dependency for dependency in reasoning_graph.dependencies
        }

        self.assertEqual("Recommended profile: Premium / Future-Ready", reasoning_graph.scope_label)
        self.assertEqual("unknown / not recorded topology", node_map["current_topology"].status)
        self.assertEqual("hybrid inverter backbone", node_map["inverter_system"].status)
        self.assertEqual("future-ready service upgrade path", node_map["panel_service"].status)
        self.assertEqual("robust", node_map["battery_posture"].status)
        self.assertEqual("future_weighted", node_map["solar_posture"].status)
        self.assertIn(
            "panel/service direction and consistency posture",
            dependency_map[("panel_service", "inverter_system")].summary.lower(),
        )

    def test_planning_state_snapshot_frames_design_001_as_saved_planning_state(self):
        result = self._advisor_summary("design_001")
        planning_state = result["planning_state"]

        self.assertEqual("planning-state-design_001", planning_state.snapshot_id)
        self.assertEqual("live_design_state", planning_state.snapshot_kind)
        self.assertEqual("design_001", planning_state.design_id)
        self.assertEqual("Phase 1 Partial Backup", planning_state.design_name)
        self.assertEqual("partial_backup", planning_state.design_goal)
        self.assertEqual("draft", planning_state.design_status)
        self.assertIn("planning snapshot", planning_state.snapshot_label.lower())
        self.assertIn("belong to this planning snapshot", planning_state.summary.lower())
        self.assertEqual(1, planning_state.scenario_count)

        variant_map = {variant.variant_key: variant for variant in planning_state.variants}
        self.assertEqual("current_state", variant_map["current_state"].state_role)
        self.assertEqual("proposed_pathway", variant_map["proposed_pathway"].state_role)
        self.assertEqual("balanced", variant_map["proposed_pathway"].profile.value)
        self.assertEqual("premium_future_ready", variant_map["future_ready_pathway"].profile.value)
        self.assertEqual("critical_efficient", variant_map["constrained_pathway"].profile.value)

        self.assertEqual(1, len(planning_state.linked_scenarios))
        self.assertEqual("scenario_001", planning_state.linked_scenarios[0].scenario_id)
        self.assertEqual("design_001", planning_state.linked_scenarios[0].linked_design_id)
        self.assertEqual("scenario_001_rev_001", planning_state.linked_scenarios[0].latest_revision_id)
        self.assertEqual("Revision 1", planning_state.linked_scenarios[0].latest_revision_label)
        self.assertEqual(1, planning_state.linked_scenarios[0].latest_revision_number)

    def test_planning_state_snapshot_frames_design_002_scenarios_without_new_recommendation_logic(self):
        result = self._advisor_summary("design_002")
        planning_state = result["planning_state"]

        self.assertEqual("planning-state-design_002", planning_state.snapshot_id)
        self.assertEqual("design_002", planning_state.design_id)
        self.assertEqual(1, planning_state.scenario_count)
        self.assertEqual("scenario_002", planning_state.linked_scenarios[0].scenario_id)
        self.assertEqual("linked planning scenario", planning_state.linked_scenarios[0].state_label)
        self.assertEqual("scenario_002_rev_001", planning_state.linked_scenarios[0].latest_revision_id)

        variant_map = {variant.variant_key: variant for variant in planning_state.variants}
        self.assertEqual("premium_future_ready", variant_map["proposed_pathway"].profile.value)
        self.assertEqual("premium_future_ready", variant_map["future_ready_pathway"].profile.value)
        self.assertEqual("critical_efficient", variant_map["constrained_pathway"].profile.value)

import os
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("DATA_DIR", "/tmp/residential-energy-planner-tests")
os.environ.setdefault("DATABASE_FILE", "phase11_contractor_workflow_test.sqlite3")

from sqlalchemy import text  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

from app.contractor_workflow.router import get_contractor_workflow_readiness  # noqa: E402
from app.core.database import Base, database_path, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.seed.runtime import reset_and_reseed  # noqa: E402
from app.services.contractor_workflow import contractor_workflow_service  # noqa: E402


class ContractorWorkflowReadinessServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db_path = Path(database_path())
        db_path.parent.mkdir(parents=True, exist_ok=True)
        engine.dispose()
        if db_path.exists():
            db_path.unlink()
        reset_and_reseed()
        with Session(engine) as db:
            cls.counts_before_initial_build = {
                table: db.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar_one()
                for table in sorted(Base.metadata.tables)
            }
            cls.cached_view = contractor_workflow_service.build_home_contractor_workflow_readiness(db, "home_001")
            cls.counts_after_initial_build = {
                table: db.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar_one()
                for table in sorted(Base.metadata.tables)
            }

    def _view(self):
        return self.cached_view

    def _table_counts(self):
        counts = {}
        with Session(engine) as db:
            for table in sorted(Base.metadata.tables):
                counts[table] = db.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar_one()
        return counts

    def test_route_is_additive_and_returns_home_id_anchored_view(self):
        paths = {getattr(route, "path", None) for route in app.routes}
        self.assertIn("/api/contractor-workflow/homes/{home_id}/readiness", paths)

        with patch(
            "app.contractor_workflow.router.contractor_workflow_service.build_home_contractor_workflow_readiness",
            return_value=self._view(),
        ):
            with Session(engine) as db:
                route_response = get_contractor_workflow_readiness("home_001", db)
        self.assertEqual("home_001", route_response.home_id)

        view = self._view()
        payload = view.dict()

        self.assertEqual("contractor_workflow_readiness", view.view_name)
        self.assertEqual("home_001", view.home_id)
        self.assertEqual("home_id", view.anchor_type)
        self.assertEqual("request_time_derived_not_persisted", view.generated_at)
        self.assertEqual("not_enforced", view.permission_enforcement)
        self.assertEqual("permission_readiness_metadata_only", view.permission_scope)
        self.assertEqual("derived", view.authority_layer.value)
        self.assertEqual("contractor_scoped", view.data_classification.value)
        self.assertNotIn("twin_id", payload)
        self.assertEqual(5, len(view.readiness_lanes))
        self.assertTrue(view.summary.workflow_ready_for_read_only_review)
        self.assertTrue(view.summary.contractor_review_required)

    def test_deterministic_response_order_and_no_table_mutation(self):
        response = self._view().dict()

        self.assertEqual(self.counts_before_initial_build, self.counts_after_initial_build)
        self.assertEqual(
            [
                "planning_review",
                "missing_input_review",
                "confirmation_gate_review",
                "option_candidate_review",
                "proposal_prep_blocked_deferred",
            ],
            [lane["lane_id"] for lane in response["readiness_lanes"]],
        )
        self.assertEqual(sorted(response["deferred_boundaries"]), response["deferred_boundaries"])
        self.assertEqual(sorted(response["missing_inputs"]), response["missing_inputs"])
        self.assertEqual(sorted(response["confirmation_gate_ids"]), response["confirmation_gate_ids"])
        self.assertEqual(sorted(response["option_candidate_refs"]), response["option_candidate_refs"])
        for lane in response["readiness_lanes"]:
            self.assertEqual(sorted(lane["deferred_boundaries"]), lane["deferred_boundaries"])
            self.assertEqual(sorted(lane["missing_inputs"]), lane["missing_inputs"])
            self.assertEqual(sorted(lane["confirmation_gate_ids"]), lane["confirmation_gate_ids"])
            self.assertEqual(sorted(lane["option_candidate_refs"]), lane["option_candidate_refs"])

    def test_forbidden_scope_flags_are_present_and_false(self):
        scope = self._view().workflow_scope

        self.assertFalse(scope.contractor_owned_state_present)
        self.assertFalse(scope.write_endpoints_present)
        self.assertFalse(scope.persistence_present)
        self.assertFalse(scope.migrations_present)
        self.assertFalse(scope.permission_enforcement_present)
        self.assertFalse(scope.pricing_present)
        self.assertFalse(scope.quote_generation_present)
        self.assertFalse(scope.proposal_generation_present)
        self.assertFalse(scope.final_estimate_present)
        self.assertFalse(scope.final_design_present)
        self.assertFalse(scope.approval_tracking_present)
        self.assertFalse(scope.crm_automation_present)
        self.assertFalse(scope.email_automation_present)
        self.assertFalse(scope.export_present)
        self.assertFalse(scope.contractor_accounts_present)
        self.assertFalse(scope.assignments_present)
        self.assertFalse(scope.accept_complete_states_present)
        self.assertFalse(scope.source_of_truth_mutation_present)
        self.assertFalse(scope.twin_id_present)
        self.assertFalse(scope.graph_behavior_present)
        self.assertFalse(scope.operational_behavior_present)
        self.assertFalse(scope.external_services_present)

    def test_interpretation_text_is_non_authoritative(self):
        view = self._view()
        interpretation_text = " ".join(
            [view.homeowner_summary, view.contractor_summary, view.summary.summary_boundary_note]
            + view.contractor_readiness_prompts
            + [lane.homeowner_summary for lane in view.readiness_lanes]
            + [lane.contractor_readiness_prompt for lane in view.readiness_lanes]
            + [blocker.homeowner_explanation for blocker in view.blockers]
            + [blocker.contractor_readiness_prompt for blocker in view.blockers]
        ).lower()

        self.assertIn("not a quote", interpretation_text)
        self.assertIn("not a final estimate", interpretation_text)
        self.assertIn("not a final design", interpretation_text)
        self.assertIn("not a final proposal", interpretation_text)
        self.assertNotIn("install this", interpretation_text)
        self.assertNotIn("proceed with", interpretation_text)
        self.assertNotIn("approved for installation", interpretation_text)
        self.assertNotIn("work directive", interpretation_text)
        self.assertNotIn("final design is ready", interpretation_text)
        self.assertNotIn("price is", interpretation_text)
        self.assertNotIn("quote is", interpretation_text)

    def test_proposal_option_set_basis_is_consumed(self):
        view = self._view()
        option_lane = next(lane for lane in view.readiness_lanes if lane.lane_id.value == "option_candidate_review")

        self.assertIn("ProposalOptionSetsView", option_lane.source_basis.source_views)
        self.assertTrue(option_lane.source_basis.proposal_option_set_refs)
        self.assertTrue(view.option_candidate_refs)
        self.assertEqual([], view.source_basis.unavailable_source_refs)
        self.assertTrue(
            option_lane.source_basis.compatibility_path_refs
            or option_lane.source_basis.takeoff_line_refs
            or option_lane.source_basis.blocker_refs
        )

    def test_blockers_missing_inputs_and_confirmation_gates_carry_forward(self):
        view = self._view()
        lane_map = {lane.lane_id.value: lane for lane in view.readiness_lanes}

        self.assertTrue(view.blockers)
        self.assertTrue(view.missing_inputs)
        self.assertTrue(view.confirmation_gate_ids)
        self.assertIn("manufacturer_spec_sheets", view.missing_inputs)
        self.assertIn("product_specs_verified", view.confirmation_gate_ids)
        self.assertTrue(lane_map["missing_input_review"].missing_inputs)
        self.assertTrue(lane_map["confirmation_gate_review"].confirmation_gate_ids)
        self.assertTrue(lane_map["option_candidate_review"].option_candidate_refs)

    def test_source_provenance_basis_is_preserved(self):
        view = self._view()

        self.assertIn("ContractorPlanningContextView", view.source_basis.source_views)
        self.assertIn("PlanningExchangeObjectView", view.source_basis.source_views)
        self.assertIn("EstimateReadinessView", view.source_basis.source_views)
        self.assertIn("ProposalOptionSetsView", view.source_basis.source_views)
        self.assertTrue(view.source_basis.source_refs)
        self.assertTrue(view.source_basis.missing_input_refs)
        self.assertTrue(view.source_basis.confirmation_gate_refs)
        self.assertTrue(view.source_basis.option_candidate_refs)
        self.assertTrue(view.source_basis.request_time_derived)
        self.assertFalse(view.source_basis.verified_fact_claim_present)

    def test_homeowner_and_contractor_readiness_surfaces_exist(self):
        view = self._view()

        self.assertTrue(view.homeowner_summary)
        self.assertTrue(view.contractor_summary)
        self.assertEqual(5, len(view.contractor_readiness_prompts))
        for lane in view.readiness_lanes:
            self.assertTrue(lane.homeowner_summary)
            self.assertTrue(lane.contractor_readiness_prompt)


if __name__ == "__main__":
    unittest.main()

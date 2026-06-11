import unittest

from tests.fast_db import reset_and_reseed  # noqa: E402  must precede app imports

from sqlalchemy import text  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

from app.core.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.services.proposal_option_sets import proposal_option_sets_service  # noqa: E402


class ProposalOptionSetsServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        reset_and_reseed()
        with Session(engine) as db:
            cls.cached_view = proposal_option_sets_service.build_home_proposal_option_sets(db, "home_001")

    def _view(self):
        return self.cached_view

    def _table_counts(self):
        counts = {}
        with Session(engine) as db:
            for table in sorted(Base.metadata.tables):
                counts[table] = db.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar_one()
        return counts

    def test_route_is_additive_home_id_anchored_and_schema_stable(self):
        paths = {getattr(route, "path", None) for route in app.routes}
        self.assertIn("/api/proposal-option-sets/homes/{home_id}", paths)

        view = self._view()
        payload = view.dict()

        self.assertEqual("proposal_option_sets", view.view_name)
        self.assertEqual("home_001", view.home_id)
        self.assertEqual("home_id", view.anchor_type)
        self.assertEqual("request_time_derived_not_persisted", view.generated_at)
        self.assertEqual("not_enforced", view.permission_enforcement)
        self.assertEqual("permission_readiness_metadata_only", view.permission_scope)
        self.assertEqual("derived", view.authority_layer.value)
        self.assertEqual("contractor_scoped", view.data_classification.value)
        self.assertNotIn("twin_id", payload)
        self.assertTrue(view.option_set_scope.read_only)
        self.assertTrue(view.option_set_scope.additive_only)
        self.assertTrue(view.option_set_scope.request_time_only)
        self.assertTrue(view.option_set_scope.home_id_anchored)
        self.assertFalse(view.summary.proposal_allowed)
        self.assertTrue(view.summary.contractor_review_required)
        self.assertTrue(view.option_candidates)

    def test_deterministic_response_and_no_persistence_mutation(self):
        before_counts = self._table_counts()
        with Session(engine) as db:
            first = proposal_option_sets_service.build_home_proposal_option_sets(db, "home_001").dict()
        with Session(engine) as db:
            second = proposal_option_sets_service.build_home_proposal_option_sets(db, "home_001").dict()
        after_counts = self._table_counts()

        self.assertEqual(first, second)
        self.assertEqual(before_counts, after_counts)
        self.assertEqual(sorted(first["deferred_boundaries"]), first["deferred_boundaries"])

    def test_candidates_include_source_scenario_and_design_basis(self):
        view = self._view()
        candidate = view.option_candidates[0]

        self.assertTrue(candidate.scenario_id)
        self.assertTrue(candidate.scenario_name)
        self.assertTrue(candidate.linked_design_id)
        self.assertTrue(candidate.source_basis.scenario_refs)
        self.assertTrue(candidate.source_basis.design_refs)
        self.assertIn("Scenario", candidate.source_basis.source_views)
        self.assertIn("EnergySystemDesign", candidate.source_basis.source_views)
        self.assertIn("EstimateReadinessView", candidate.source_basis.source_views)
        self.assertTrue(candidate.dependency_refs)

    def test_phase9_blockers_missing_inputs_and_confirmation_gates_carry_through(self):
        view = self._view()
        candidate = view.option_candidates[0]

        self.assertTrue(view.blockers)
        self.assertTrue(view.missing_inputs)
        self.assertTrue(view.confirmation_gate_ids)
        self.assertTrue(candidate.blockers)
        self.assertTrue(candidate.missing_inputs)
        self.assertTrue(candidate.confirmation_gate_ids)
        self.assertIn("manufacturer_spec_sheets", view.missing_inputs)
        self.assertIn("product_specs_verified", view.confirmation_gate_ids)
        self.assertIn("estimate_readiness_blocker", view.blocker_category_counts)

    def test_forbidden_boundary_flags_remain_false(self):
        scope = self._view().option_set_scope

        self.assertFalse(scope.persistence_present)
        self.assertFalse(scope.migrations_present)
        self.assertFalse(scope.write_endpoints_present)
        self.assertFalse(scope.auth_security_changes_present)
        self.assertFalse(scope.permission_enforcement_present)
        self.assertFalse(scope.email_automation_present)
        self.assertFalse(scope.pricing_present)
        self.assertFalse(scope.quote_generation_present)
        self.assertFalse(scope.bid_logic_present)
        self.assertFalse(scope.proposal_generation_present)
        self.assertFalse(scope.final_proposal_present)
        self.assertFalse(scope.final_estimate_present)
        self.assertFalse(scope.final_bill_of_materials_present)
        self.assertFalse(scope.final_design_present)
        self.assertFalse(scope.product_recommendations_present)
        self.assertFalse(scope.procurement_present)
        self.assertFalse(scope.crm_workflow_present)
        self.assertFalse(scope.ranking_present)
        self.assertFalse(scope.best_option_selection_present)
        self.assertFalse(scope.contractor_approval_claim_present)
        self.assertFalse(scope.ahj_utility_approval_claim_present)
        self.assertFalse(scope.final_electrical_sizing_present)

    def test_homeowner_text_avoids_final_design_and_contractor_only_claims(self):
        view = self._view()
        homeowner_text = " ".join(
            [view.homeowner_summary]
            + [candidate.homeowner_summary.summary for candidate in view.option_candidates]
            + [blocker.homeowner_explanation for blocker in view.blockers]
        ).lower()

        self.assertNotIn("final design", homeowner_text)
        self.assertNotIn("contractor-only", homeowner_text)
        self.assertNotIn("ahj approved", homeowner_text)
        self.assertNotIn("utility approved", homeowner_text)
        self.assertNotIn("permit-ready", homeowner_text)

    def test_contractor_notes_are_review_prompts_not_directives(self):
        view = self._view()
        contractor_text = " ".join(
            [view.contractor_summary]
            + [note for candidate in view.option_candidates for note in candidate.contractor_review_notes]
            + [blocker.contractor_review_note for blocker in view.blockers]
        ).lower()

        self.assertIn("review prompt", contractor_text)
        self.assertNotIn("install this", contractor_text)
        self.assertNotIn("proceed with", contractor_text)
        self.assertNotIn("approved for installation", contractor_text)
        self.assertNotIn("work directive", contractor_text)

    def test_deferred_boundaries_are_stable_sorted_and_include_forbidden_scope(self):
        view = self._view()

        self.assertEqual(sorted(view.deferred_boundaries), view.deferred_boundaries)
        self.assertIn("proposal_generation", view.deferred_boundaries)
        self.assertIn("pricing", view.deferred_boundaries)
        self.assertIn("final_design", view.deferred_boundaries)
        self.assertIn("permission_enforcement", view.deferred_boundaries)
        for candidate in view.option_candidates:
            self.assertEqual(sorted(candidate.deferred_boundaries), candidate.deferred_boundaries)


if __name__ == "__main__":
    unittest.main()

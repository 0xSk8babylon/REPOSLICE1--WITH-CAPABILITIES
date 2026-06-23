import unittest
from types import SimpleNamespace

from tests.fast_db import reset_and_reseed  # noqa: E402  must precede app imports

from sqlalchemy import text  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

from app.core.database import Base, engine  # noqa: E402
from app.estimate_readiness.schemas import (  # noqa: E402
    EstimateBlockerCategory,
    EstimateConfirmationGateStatus,
    EstimateReadinessBlocker,
    EstimateReadinessStatus,
)
from app.main import app  # noqa: E402
from app.services.estimate_readiness import estimate_readiness_service  # noqa: E402


class EstimateReadinessServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        reset_and_reseed()
        with Session(engine) as db:
            cls.cached_view = estimate_readiness_service.build_home_estimate_readiness(db, "home_001")

    def _view(self):
        return self.cached_view

    def _table_counts(self):
        counts = {}
        with Session(engine) as db:
            for table in sorted(Base.metadata.tables):
                counts[table] = db.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar_one()
        return counts

    def test_estimate_readiness_route_is_additive_read_only_and_schema_stable(self):
        paths = set(app.openapi()["paths"])
        self.assertIn("/api/estimate-readiness/homes/{home_id}", paths)

        view = self._view()
        payload = view.dict()
        scope = view.readiness_scope

        self.assertEqual("estimate_readiness", view.view_name)
        self.assertEqual("home_001", view.home_id)
        self.assertEqual("home_id", view.anchor_type)
        self.assertEqual("request_time_derived_not_persisted", view.generated_at)
        self.assertEqual("not_enforced", view.permission_enforcement)
        self.assertEqual("permission_readiness_metadata_only", view.permission_scope)
        self.assertEqual("derived", view.authority_layer.value)
        self.assertEqual("contractor_scoped", view.data_classification.value)
        self.assertNotIn("twin_id", payload)
        self.assertEqual("not_ready", view.overall_status.value)
        self.assertFalse(view.estimate_allowed)
        self.assertTrue(view.contractor_review_required)
        self.assertEqual(19, len(view.confirmation_gates))
        self.assertTrue(view.scenario_statuses)
        self.assertEqual(view.overall_status, view.readiness_summary.overall_status)
        self.assertIn("homeowner_summary", payload)
        self.assertIn("contractor_summary", payload)
        self.assertIn("confirmation_gates", payload)
        self.assertIn("blockers", payload)
        self.assertIn("missing_inputs", payload)
        self.assertTrue(scope.read_only)
        self.assertTrue(scope.request_time_only)
        self.assertTrue(scope.home_id_anchored)
        self.assertTrue(scope.derived_from_topology_takeoff)
        self.assertTrue(scope.derived_from_confirmation_gate_projection)
        self.assertTrue(scope.derived_from_shared_compatibility)
        self.assertFalse(scope.persistence_present)
        self.assertFalse(scope.migrations_present)
        self.assertFalse(scope.write_endpoints_present)
        self.assertFalse(scope.auth_security_changes_present)
        self.assertFalse(scope.permission_enforcement_present)
        self.assertFalse(scope.pricing_present)
        self.assertFalse(scope.proposal_generation_present)
        self.assertFalse(scope.final_estimate_present)

    def test_estimate_readiness_reports_missing_specs_nameplates_and_distance(self):
        view = self._view()
        blocker_categories = {blocker.category.value for blocker in view.blockers}

        self.assertIn("missing_product_spec", blocker_categories)
        self.assertIn("missing_nameplate", blocker_categories)
        self.assertIn("missing_measurement", blocker_categories)
        self.assertIn("pricing_input_missing", blocker_categories)
        self.assertIn("material_scope_incomplete", blocker_categories)
        self.assertIn("manufacturer_spec_sheets", view.missing_inputs)
        self.assertIn("equipment_nameplate_photos_or_recorded_ratings", view.missing_inputs)
        self.assertIn("field_measured_route_distances", view.missing_inputs)
        self.assertIn("contractor_pricing", view.missing_inputs)

    def test_estimate_readiness_marks_contractor_only_gate_visibility(self):
        view = self._view()
        gates = {gate.gate_id: gate for gate in view.confirmation_gates}

        final_review = gates["contractor_final_review_completed"]
        product_specs = gates["product_specs_verified"]

        self.assertFalse(final_review.visible_to_homeowner)
        self.assertTrue(final_review.contractor_only_notes)
        self.assertEqual(
            "contractor_only_final_review_required",
            final_review.status.value,
        )
        self.assertTrue(product_specs.visible_to_homeowner)
        self.assertEqual("phase_9_confirmation_gate_registry_v1", product_specs.gate_version)
        self.assertTrue(product_specs.required_for_estimate)
        self.assertTrue(product_specs.basis.gate_refs)

    def test_estimate_readiness_separates_homeowner_and_contractor_language(self):
        view = self._view()

        self.assertIn("A contractor needs to confirm", view.homeowner_summary)
        self.assertIn("Estimate readiness status is not_ready", view.contractor_summary)
        self.assertNotIn("derating calculation", view.homeowner_summary.lower())
        self.assertNotIn("final wire size is", str(view.dict()).lower())
        self.assertNotIn("ahj approved", str(view.dict()).lower())
        for blocker in view.blockers:
            self.assertTrue(blocker.homeowner_explanation)
            self.assertTrue(blocker.contractor_notes)

    def test_complex_topology_requires_contractor_review(self):
        view = self._view()
        scenario = view.scenario_statuses[0]

        self.assertFalse(scenario.estimate_allowed)
        self.assertTrue(scenario.contractor_review_required)
        self.assertIn("battery_backup", scenario.complexity_flags)
        self.assertIn("generator_interlock_or_transfer", scenario.complexity_flags)
        self.assertIn("long_or_uncertain_conduit_route", scenario.complexity_flags)
        self.assertIn("service_upgrade_or_load_side_work", scenario.complexity_flags)
        self.assertIn("disconnect_requirements_reviewed", scenario.required_gate_ids)
        self.assertIn("grounding_bonding_reviewed", scenario.required_gate_ids)
        self.assertIn("utility_ahj_requirements_reviewed", scenario.required_gate_ids)

    def test_ready_vs_not_ready_status_helper(self):
        confirmed_gate = SimpleNamespace(status=EstimateConfirmationGateStatus.confirmed)
        ready_status, estimate_allowed, contractor_review_required, confidence = (
            estimate_readiness_service._overall_status(
                required_gates=[confirmed_gate],
                blockers=[],
                missing_inputs=[],
            )
        )
        self.assertEqual(EstimateReadinessStatus.ready_for_estimate, ready_status)
        self.assertTrue(estimate_allowed)
        self.assertFalse(contractor_review_required)
        self.assertEqual("high", confidence.value)

        blocker = EstimateReadinessBlocker(
            blocker_id="test:missing_spec",
            category=EstimateBlockerCategory.missing_product_spec,
            severity="blocker",
            homeowner_explanation="Product specs are missing.",
            contractor_notes="Manufacturer specs are required before estimate use.",
        )
        not_ready_status, estimate_allowed, contractor_review_required, confidence = (
            estimate_readiness_service._overall_status(
                required_gates=[confirmed_gate],
                blockers=[blocker],
                missing_inputs=["manufacturer_spec_sheets"],
            )
        )
        self.assertEqual(EstimateReadinessStatus.not_ready, not_ready_status)
        self.assertFalse(estimate_allowed)
        self.assertTrue(contractor_review_required)
        self.assertEqual("low", confidence.value)

    def test_estimate_readiness_is_deterministic_and_does_not_mutate_persistence(self):
        before_counts = self._table_counts()
        with Session(engine) as db:
            first = estimate_readiness_service.build_home_estimate_readiness(db, "home_001").dict()
        with Session(engine) as db:
            second = estimate_readiness_service.build_home_estimate_readiness(db, "home_001").dict()
        after_counts = self._table_counts()

        self.assertEqual(first, second)
        self.assertEqual(before_counts, after_counts)
        self.assertEqual(sorted(first["deferred_boundaries"]), first["deferred_boundaries"])


if __name__ == "__main__":
    unittest.main()

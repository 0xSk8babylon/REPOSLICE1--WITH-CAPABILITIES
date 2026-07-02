import unittest
from unittest.mock import patch

from sqlalchemy import text  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

from app.core.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.product_preferences.router import get_product_preferences  # noqa: E402
from app.services.product_preferences import product_preferences_service  # noqa: E402
from tests.fast_db import reset_and_reseed  # noqa: E402  must precede app imports


class ProductPreferencesServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        reset_and_reseed()
        with Session(engine) as db:
            cls.counts_before_initial_build = {
                table: db.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar_one()
                for table in sorted(Base.metadata.tables)
            }
            cls.cached_view = product_preferences_service.build_home_product_preferences(db, "home_001")
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

    def test_route_is_additive_home_id_anchored_and_schema_stable(self):
        paths = set(app.openapi()["paths"])
        self.assertIn("/api/product-preferences/homes/{home_id}", paths)

        with patch(
            "app.product_preferences.router.product_preferences_service.build_home_product_preferences",
            return_value=self._view(),
        ):
            with Session(engine) as db:
                route_response = get_product_preferences("home_001", db)
        self.assertEqual("home_001", route_response.home_id)

        view = self._view()
        payload = view.dict()

        self.assertEqual("product_preferences", view.view_name)
        self.assertEqual("home_001", view.home_id)
        self.assertEqual("home_id", view.anchor_type)
        self.assertEqual("request_time_derived_not_persisted", view.generated_at)
        self.assertEqual("not_enforced", view.permission_enforcement)
        self.assertEqual("permission_readiness_metadata_only", view.permission_scope)
        self.assertEqual("derived", view.authority_layer.value)
        self.assertEqual("contractor_scoped", view.data_classification.value)
        self.assertNotIn("twin_id", payload)
        self.assertEqual(12, len(view.categories))
        self.assertFalse(view.summary.product_selection_allowed)
        self.assertTrue(view.summary.contractor_review_required)

    def test_deterministic_response_and_no_persistence_mutation(self):
        before_counts = self._table_counts()
        first = self._view().dict()
        with Session(engine) as db:
            second = product_preferences_service.build_home_product_preferences(db, "home_001").dict()
        after_counts = self._table_counts()

        self.assertEqual(first, second)
        self.assertEqual(before_counts, after_counts)
        self.assertEqual(self.counts_before_initial_build, self.counts_after_initial_build)
        self.assertEqual(sorted(first["deferred_boundaries"]), first["deferred_boundaries"])
        self.assertEqual(
            sorted(category["category_id"] for category in first["categories"]),
            [category["category_id"] for category in first["categories"]],
        )

    def test_forbidden_boundary_flags_are_present_and_false(self):
        scope = self._view().preference_scope

        self.assertFalse(scope.persistence_present)
        self.assertFalse(scope.migrations_present)
        self.assertFalse(scope.write_endpoints_present)
        self.assertFalse(scope.auth_security_changes_present)
        self.assertFalse(scope.permission_enforcement_present)
        self.assertFalse(scope.frontend_present)
        self.assertFalse(scope.pricing_present)
        self.assertFalse(scope.live_inventory_present)
        self.assertFalse(scope.distributor_quotes_present)
        self.assertFalse(scope.procurement_present)
        self.assertFalse(scope.purchase_links_present)
        self.assertFalse(scope.payments_present)
        self.assertFalse(scope.final_bill_of_materials_present)
        self.assertFalse(scope.final_electrical_design_present)
        self.assertFalse(scope.final_product_recommendation_present)
        self.assertFalse(scope.product_ranking_present)
        self.assertFalse(scope.best_option_selection_present)
        self.assertFalse(scope.manufacturer_certification_claim_present)
        self.assertFalse(scope.warranty_claim_present)
        self.assertFalse(scope.crm_handoff_present)
        self.assertFalse(scope.email_automation_present)
        self.assertFalse(scope.external_services_present)
        self.assertFalse(scope.secrets_present)

    def test_no_pricing_procurement_or_final_recommendation_claims(self):
        view = self._view()
        text = " ".join(
            [view.homeowner_summary, view.contractor_summary, view.summary.summary_boundary_note]
            + [category.planning_direction for category in view.categories]
            + [category.homeowner_explanation for category in view.categories]
            + [category.contractor_review_prompt for category in view.categories]
            + [blocker.homeowner_explanation for blocker in view.blockers]
            + [blocker.contractor_review_prompt for blocker in view.blockers]
        ).lower()

        self.assertNotIn("best option", text)
        self.assertNotIn("buy this", text)
        self.assertNotIn("purchase this", text)
        self.assertNotIn("price is", text)
        self.assertNotIn("quote is", text)
        self.assertNotIn("distributor quote", text)
        self.assertNotIn("approved for installation", text)
        self.assertNotIn("warranty-backed", text)
        self.assertFalse(view.summary.pricing_allowed)
        self.assertFalse(view.summary.procurement_allowed)
        self.assertFalse(view.summary.final_design_allowed)

    def test_missing_input_behavior_for_supported_and_unsupported_categories(self):
        view = self._view()
        categories = {category.category_id.value: category for category in view.categories}

        self.assertIn("manufacturer_spec_sheets", view.missing_inputs)
        self.assertTrue(categories["pv_modules"].missing_inputs)
        self.assertTrue(categories["inverter_topology"].missing_inputs)
        self.assertEqual("source_limited", categories["aesthetic_preference"].status.value)
        self.assertIn(
            "homeowner_aesthetic_preference_not_recorded",
            categories["aesthetic_preference"].missing_inputs,
        )
        self.assertEqual("source_limited", categories["contractor_preferred_product_family"].status.value)
        self.assertIn(
            "contractor_preferred_product_family_not_recorded",
            categories["contractor_preferred_product_family"].missing_inputs,
        )

    def test_blockers_confirmation_gates_and_install_logic_are_carried_through(self):
        view = self._view()
        categories = {category.category_id.value: category for category in view.categories}

        self.assertTrue(view.blockers)
        self.assertTrue(view.confirmation_gate_ids)
        self.assertIn("product_specs_verified", view.confirmation_gate_ids)
        self.assertTrue(categories["backup_scope"].confirmation_gate_ids)
        self.assertTrue(categories["gateway_transfer_equipment"].install_logic)
        self.assertTrue(categories["backup_loads_panel"].blockers)

    def test_homeowner_safe_and_contractor_facing_language_are_separated(self):
        view = self._view()
        homeowner_text = " ".join(
            [view.homeowner_summary]
            + [category.homeowner_explanation for category in view.categories]
            + [blocker.homeowner_explanation for blocker in view.blockers]
        ).lower()
        contractor_text = " ".join(
            [view.contractor_summary]
            + view.contractor_review_prompts
            + [category.contractor_review_prompt for category in view.categories]
            + [blocker.contractor_review_prompt for blocker in view.blockers]
        ).lower()

        self.assertNotIn("review prompt only", homeowner_text)
        self.assertIn("review prompt only", contractor_text)
        self.assertNotIn("install this", contractor_text)
        self.assertNotIn("proceed with", contractor_text)
        self.assertNotIn("work directive", contractor_text)

    def test_provenance_source_basis_is_carried_through(self):
        view = self._view()

        self.assertIn("TwinSharedCompatibilityView", view.source_basis.source_views)
        self.assertIn("TwinTopologyTakeoffView", view.source_basis.source_views)
        self.assertIn("EstimateReadinessView", view.source_basis.source_views)
        self.assertIn("ProposalOptionSetsView", view.source_basis.source_views)
        self.assertTrue(view.source_basis.source_refs)
        self.assertTrue(view.source_basis.compatibility_path_refs)
        self.assertTrue(view.source_basis.takeoff_line_refs)
        self.assertTrue(view.source_basis.estimate_gate_refs)
        self.assertTrue(view.source_basis.option_candidate_refs)
        self.assertTrue(view.source_basis.request_time_derived)
        self.assertFalse(view.source_basis.verified_fact_claim_present)
        for category in view.categories:
            self.assertTrue(category.source_basis.request_time_derived)
            self.assertFalse(category.source_basis.verified_fact_claim_present)


if __name__ == "__main__":
    unittest.main()

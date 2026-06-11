import unittest
from types import SimpleNamespace
from unittest.mock import patch

from tests.fast_db import reset_and_reseed  # noqa: E402  must precede app imports

from sqlalchemy import text  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

from app.core.database import Base, engine  # noqa: E402
from app.crm_handoff.router import get_crm_handoff  # noqa: E402
from app.main import app  # noqa: E402
from app.post_install.router import get_post_install_view  # noqa: E402
from app.services.crm_handoff import crm_handoff_service  # noqa: E402
from app.services.post_install import post_install_service  # noqa: E402


def _value(value):
    return SimpleNamespace(value=value)


def _fake_context():
    return SimpleNamespace(
        sections=[
            SimpleNamespace(section_key="home"),
            SimpleNamespace(section_key="planning"),
            SimpleNamespace(section_key="products"),
        ]
    )


def _fake_contractor_view():
    return SimpleNamespace(
        missing_inputs=["manufacturer_spec_sheets", "field_measurements"],
        confirmation_gate_ids=["product_specs_verified", "contractor_final_review_completed"],
        option_candidate_refs=["option_candidate:scenario_001"],
        summary=SimpleNamespace(contractor_review_required=True),
        readiness_lanes=[
            SimpleNamespace(lane_id=_value("planning_review")),
            SimpleNamespace(lane_id=_value("proposal_prep_blocked_deferred")),
        ],
        blockers=[
            SimpleNamespace(
                blocker_id="proposal_prep_blocked_deferred:pricing_deferred",
                severity="deferred",
                source_refs=["ContractorWorkflowReadinessView"],
                gate_refs=["contractor_final_review_completed"],
                missing_inputs=[],
                homeowner_explanation="Proposal preparation remains deferred.",
                contractor_readiness_prompt="Review prompt only: proposal preparation remains deferred.",
            )
        ],
    )


def _fake_product_view():
    return SimpleNamespace(
        missing_inputs=["manufacturer_spec_sheets", "model_specific_product_specs"],
        confirmation_gate_ids=["product_specs_verified"],
        categories=[
            SimpleNamespace(category_id=_value("pv_modules")),
            SimpleNamespace(category_id=_value("inverter_topology")),
        ],
        blockers=[
            SimpleNamespace(
                blocker_id="pv_modules:missing_specs",
                severity="blocker",
                source_refs=["ProductPreferencesView"],
                gate_refs=["product_specs_verified"],
                missing_inputs=["manufacturer_spec_sheets"],
                homeowner_explanation="Product specs are still missing.",
                contractor_review_prompt="Review prompt only: collect manufacturer product specs.",
            )
        ],
    )


class Phase13PostInstallCRMHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        reset_and_reseed()
        with Session(engine) as db:
            cls.counts_before_initial_build = {
                table: db.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar_one()
                for table in sorted(Base.metadata.tables)
            }
            with patch(
                "app.services.twin_planning_context.twin_planning_context_service.build",
                return_value=_fake_context(),
            ), patch(
                "app.services.contractor_workflow.contractor_workflow_service.build_home_contractor_workflow_readiness",
                return_value=_fake_contractor_view(),
            ), patch(
                "app.services.product_preferences.product_preferences_service.build_home_product_preferences",
                return_value=_fake_product_view(),
            ):
                cls.cached_post_install = post_install_service.build_home_post_install_view(db, "home_001")
            with patch(
                "app.services.post_install.post_install_service.build_home_post_install_view",
                return_value=cls.cached_post_install,
            ):
                cls.cached_crm_handoff = crm_handoff_service.build_home_crm_handoff(db, "home_001")
            cls.counts_after_initial_build = {
                table: db.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar_one()
                for table in sorted(Base.metadata.tables)
            }

    def _post_install(self):
        return self.cached_post_install

    def _crm_handoff(self):
        return self.cached_crm_handoff

    def test_routes_are_additive_and_home_id_anchored(self):
        paths = {getattr(route, "path", None) for route in app.routes}
        self.assertIn("/api/post-install/homes/{home_id}", paths)
        self.assertIn("/api/crm-handoff/homes/{home_id}", paths)

        with patch(
            "app.post_install.router.post_install_service.build_home_post_install_view",
            return_value=self._post_install(),
        ):
            with Session(engine) as db:
                post_install_response = get_post_install_view("home_001", db)
        with patch(
            "app.crm_handoff.router.crm_handoff_service.build_home_crm_handoff",
            return_value=self._crm_handoff(),
        ):
            with Session(engine) as db:
                crm_response = get_crm_handoff("home_001", db)

        self.assertEqual("home_001", post_install_response.home_id)
        self.assertEqual("home_001", crm_response.home_id)
        self.assertEqual("home_id", post_install_response.anchor_type)
        self.assertEqual("home_id", crm_response.anchor_type)
        self.assertNotIn("twin_id", post_install_response.dict())
        self.assertNotIn("twin_id", crm_response.dict())

    def test_request_time_views_do_not_mutate_persistence_and_are_sorted(self):
        self.assertEqual(self.counts_before_initial_build, self.counts_after_initial_build)

        post_install = self._post_install().dict()
        crm_handoff = self._crm_handoff().dict()

        self.assertEqual(sorted(post_install["deferred_boundaries"]), post_install["deferred_boundaries"])
        self.assertEqual(sorted(crm_handoff["deferred_boundaries"]), crm_handoff["deferred_boundaries"])
        self.assertEqual(
            sorted(opportunity["opportunity_type"] for opportunity in post_install["opportunities"]),
            [opportunity["opportunity_type"] for opportunity in post_install["opportunities"]],
        )
        self.assertEqual(
            sorted(field["field_key"] for field in crm_handoff["handoff_fields"]),
            [field["field_key"] for field in crm_handoff["handoff_fields"]],
        )

    def test_phase13_scope_flags_prevent_writes_crm_push_and_scoring(self):
        post_scope = self._post_install().post_install_scope
        crm_scope = self._crm_handoff().handoff_scope

        for scope in [post_scope, crm_scope]:
            self.assertFalse(scope.persistence_present)
            self.assertFalse(scope.migrations_present)
            self.assertFalse(scope.write_endpoints_present)
            self.assertFalse(scope.auth_security_changes_present)
            self.assertFalse(scope.permission_enforcement_present)
            self.assertFalse(scope.frontend_present)
            self.assertFalse(scope.email_drip_campaign_behavior_present)
            self.assertFalse(scope.task_creation_present)
            self.assertFalse(scope.sales_scoring_present)
            self.assertFalse(scope.lead_scoring_present)
            self.assertFalse(scope.ranking_present)
            self.assertFalse(scope.best_upsell_logic_present)
            self.assertFalse(scope.push_behavior_present)
            self.assertFalse(scope.source_of_truth_mutation_present)
            self.assertFalse(scope.twin_id_present)
            self.assertFalse(scope.graph_behavior_present)
            self.assertFalse(scope.operational_behavior_present)
        self.assertFalse(post_scope.external_crm_integration_present)
        self.assertFalse(post_scope.crm_writes_present)
        self.assertFalse(crm_scope.external_crm_integration_present)
        self.assertFalse(crm_scope.crm_write_present)
        self.assertFalse(crm_scope.crm_record_creation_present)

    def test_post_install_state_opportunities_lifecycle_events_and_follow_up_readiness(self):
        view = self._post_install()

        self.assertEqual("post_install_retention", view.view_name)
        self.assertEqual("request_time_derived_not_persisted", view.generated_at)
        self.assertEqual("derived", view.authority_layer.value)
        self.assertEqual("contractor_scoped", view.data_classification.value)
        self.assertEqual(6, len(view.opportunities))
        self.assertTrue(view.lifecycle_events)
        self.assertTrue(view.summary.crm_handoff_object_available)
        self.assertFalse(view.summary.crm_write_allowed)
        self.assertFalse(view.summary.email_campaign_allowed)
        self.assertFalse(view.summary.task_creation_allowed)
        self.assertFalse(view.summary.scoring_allowed)
        self.assertFalse(view.summary.ranking_allowed)
        self.assertFalse(view.summary.push_allowed)
        self.assertIn("manufacturer_spec_sheets", view.missing_inputs)
        self.assertIn("product_specs_verified", view.confirmation_gate_ids)

    def test_crm_handoff_object_is_manual_review_metadata_only(self):
        view = self._crm_handoff()

        self.assertEqual("crm_handoff_object", view.view_name)
        self.assertEqual("crm_handoff:home:home_001:phase_13_request_time", view.handoff_object_id)
        self.assertTrue(view.summary.manual_crm_review_ready)
        self.assertFalse(view.summary.crm_write_allowed)
        self.assertFalse(view.summary.external_crm_sync_allowed)
        self.assertFalse(view.summary.email_campaign_allowed)
        self.assertFalse(view.summary.task_creation_allowed)
        self.assertFalse(view.summary.scoring_allowed)
        self.assertFalse(view.summary.ranking_allowed)
        self.assertFalse(view.summary.push_allowed)
        self.assertTrue(view.handoff_fields)
        self.assertIn("manual_handoff_object_only_no_crm_write_no_task_no_email_no_score_no_rank_no_push", [
            field.value for field in view.handoff_fields
        ])

    def test_source_provenance_basis_is_preserved(self):
        post_install = self._post_install()
        crm_handoff = self._crm_handoff()

        self.assertIn("ContractorWorkflowReadinessView", post_install.source_basis.source_views)
        self.assertIn("ProductPreferencesView", post_install.source_basis.source_views)
        self.assertNotIn("ProposalOptionSetsView", post_install.source_basis.source_views)
        self.assertNotIn("EstimateReadinessView", post_install.source_basis.source_views)
        self.assertTrue(post_install.source_basis.source_refs)
        self.assertTrue(post_install.source_basis.proposal_option_refs)
        self.assertTrue(post_install.source_basis.estimate_gate_refs)
        self.assertTrue(post_install.source_basis.request_time_derived)
        self.assertFalse(post_install.source_basis.verified_fact_claim_present)

        self.assertIn("PostInstallView", crm_handoff.source_basis.source_views)
        self.assertTrue(crm_handoff.source_basis.retention_opportunity_refs)
        self.assertTrue(crm_handoff.source_basis.lifecycle_event_refs)
        self.assertTrue(crm_handoff.source_basis.handoff_field_refs)
        self.assertTrue(crm_handoff.source_basis.request_time_derived)
        self.assertFalse(crm_handoff.source_basis.verified_fact_claim_present)


if __name__ == "__main__":
    unittest.main()

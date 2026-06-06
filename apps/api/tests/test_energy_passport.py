import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch

os.environ.setdefault("DATA_DIR", "/tmp/residential-energy-planner-tests")
os.environ.setdefault("DATABASE_FILE", "phase14_energy_passport_test.sqlite3")

from app.energy_passport.router import get_energy_passport  # noqa: E402
from app.energy_passport.schemas import (  # noqa: E402
    EnergyPassportFinancingStructure,
    EnergyPassportTransferReadinessLevel,
    EnergyPassportTransferRelevanceFlag,
)
from app.main import app  # noqa: E402
from app.services.energy_passport import energy_passport_service  # noqa: E402


def _value(value):
    return SimpleNamespace(value=value)


def _record(entity_type, entity_id, record):
    return SimpleNamespace(entity_type=entity_type, entity_id=entity_id, record=record)


def _fake_context():
    return SimpleNamespace(
        sections=[
            SimpleNamespace(
                section_key="home",
                records=[
                    _record(
                        "home",
                        "home_001",
                        {
                            "name": "Test Home",
                            "utility_provider": "Example Utility",
                        },
                    )
                ],
            ),
            SimpleNamespace(
                section_key="equipment_products",
                records=[
                    _record("equipment_product", "pv_001", {"product_type": "solar_panel", "name": "PV module"}),
                    _record("equipment_product", "bat_001", {"product_type": "battery", "name": "Battery"}),
                    _record("equipment_product", "gen_001", {"product_type": "generator", "name": "Generator"}),
                    _record("equipment_product", "ev_001", {"product_type": "ev_charger", "name": "EV charger"}),
                ],
            ),
            SimpleNamespace(
                section_key="electrical_panels",
                records=[
                    _record(
                        "electrical_panel",
                        "panel_001",
                        {"panel_type": "main_service_panel", "name": "Main panel"},
                    )
                ],
            ),
            SimpleNamespace(
                section_key="scenario_revisions",
                records=[
                    _record(
                        "scenario_revision",
                        "scenario_001_rev_001",
                        {"design_goal": "whole_home_backup", "name": "Revision 1"},
                    )
                ],
            ),
        ]
    )


def _fake_product_preferences():
    return SimpleNamespace(
        missing_inputs=["manufacturer_spec_sheets", "ownership_financing_documents"],
        categories=[
            SimpleNamespace(category_id=_value("pv_modules")),
            SimpleNamespace(category_id=_value("battery_coupling")),
            SimpleNamespace(category_id=_value("backup_scope")),
            SimpleNamespace(category_id=_value("backup_loads_panel")),
            SimpleNamespace(category_id=_value("ev_charger_readiness")),
            SimpleNamespace(category_id=_value("monitoring_controls")),
        ],
        blockers=[
            SimpleNamespace(blocker_id="pv_modules:missing_specs"),
            SimpleNamespace(blocker_id="battery_coupling:missing_specs"),
        ],
    )


def _fake_contractor_workflow():
    return SimpleNamespace(
        missing_inputs=["field_measurements", "contractor_review"],
        confirmation_gate_ids=["product_specs_verified", "contractor_final_review_completed"],
    )


def _fake_post_install():
    return SimpleNamespace(
        missing_inputs=["monitoring_account_transfer_terms"],
        lifecycle_events=[
            SimpleNamespace(event_id="phase_13:post_install_context_assembled"),
            SimpleNamespace(event_id="phase_13:product_review_needed"),
        ],
        opportunities=[
            SimpleNamespace(opportunity_id="phase_13:documentation_completion"),
            SimpleNamespace(opportunity_id="phase_13:product_spec_followup"),
        ],
        blockers=[
            SimpleNamespace(blocker_id="source_unavailable:monitoring_terms"),
        ],
    )


def _fake_crm_handoff():
    return SimpleNamespace(
        handoff_fields=[SimpleNamespace(field_key="manual_review_summary")]
    )


def _fake_planning_exchange():
    return SimpleNamespace(view_name="planning_exchange_object")


class EnergyPassportTests(unittest.TestCase):
    def _build(self):
        with patch(
            "app.services.twin_planning_context.twin_planning_context_service.build",
            return_value=_fake_context(),
        ), patch(
            "app.services.planning_exchange.planning_exchange_service.build_planning_exchange_object",
            return_value=_fake_planning_exchange(),
        ), patch(
            "app.services.contractor_workflow.contractor_workflow_service.build_home_contractor_workflow_readiness",
            return_value=_fake_contractor_workflow(),
        ), patch(
            "app.services.product_preferences.product_preferences_service.build_home_product_preferences",
            return_value=_fake_product_preferences(),
        ), patch(
            "app.services.post_install.post_install_service.build_home_post_install_view",
            return_value=_fake_post_install(),
        ), patch(
            "app.services.crm_handoff.crm_handoff_service.build_home_crm_handoff",
            return_value=_fake_crm_handoff(),
        ):
            return energy_passport_service.build_home_energy_passport(None, "home_001")

    def test_route_exists_and_response_is_home_id_anchored(self):
        paths = {getattr(route, "path", None) for route in app.routes}
        self.assertIn("/api/energy-passport/homes/{home_id}", paths)

        view = self._build()
        with patch(
            "app.energy_passport.router.energy_passport_service.build_home_energy_passport",
            return_value=view,
        ):
            response = get_energy_passport("home_001", None)

        self.assertEqual("home_001", response.home_id)
        self.assertEqual("home_id", response.anchor_type)
        self.assertEqual("request_time_derived_not_persisted", response.generated_at)

    def test_scope_flags_are_explicit_read_only_additive_request_time_and_false_forbidden_boundaries(self):
        scope = self._build().scope
        self.assertTrue(scope.read_only)
        self.assertTrue(scope.additive_only)
        self.assertTrue(scope.request_time_only)
        self.assertTrue(scope.home_id_anchored)
        self.assertTrue(scope.deterministic_for_same_inputs)
        self.assertTrue(scope.non_authoritative)

        for attr in [
            "title_claim_present",
            "escrow_claim_present",
            "deed_claim_present",
            "lease_assignment_present",
            "payoff_calculation_present",
            "lien_ucc_title_search_present",
            "warranty_validation_present",
            "permit_validation_present",
            "appraisal_present",
            "underwriting_present",
            "tax_advice_present",
            "financial_conclusion_present",
            "crm_write_present",
            "persistence_present",
            "migrations_present",
            "auth_security_changes_present",
            "permission_enforcement_present",
            "deploy_present",
            "push_present",
            "write_endpoints_present",
            "contract_validation_present",
            "legal_advice_present",
        ]:
            self.assertFalse(getattr(scope, attr), attr)

    def test_response_is_deterministic_and_preserves_source_provenance_basis(self):
        first = self._build().dict()
        second = self._build().dict()

        self.assertEqual(first, second)
        self.assertTrue(first["source_basis"]["request_time_derived"])
        self.assertFalse(first["source_basis"]["verified_fact_claim_present"])
        self.assertFalse(first["source_basis"]["authoritative_validation_present"])
        self.assertIn("TwinPlanningContext", first["source_basis"]["source_views"])
        self.assertIn("ProductPreferencesView", first["source_basis"]["source_views"])
        self.assertIn("PostInstallView", first["source_basis"]["source_views"])

    def test_system_summary_uses_only_safe_statuses_and_no_authoritative_claims(self):
        view = self._build()
        safe_statuses = {"known", "planned", "candidate", "needs_confirmation", "not_available", "unknown"}
        system_types = {system.system_type.value for system in view.system_summary}
        self.assertEqual(
            {
                "solar_pv",
                "battery_storage",
                "backup_generator",
                "panel_load_management",
                "ev_readiness",
                "utility_program_context",
            },
            system_types,
        )
        for system in view.system_summary:
            self.assertIn(system.status.value, safe_statuses)
            self.assertNotIn("approved", system.summary.lower())
            self.assertNotIn("warrantied", system.summary.lower())
            self.assertNotIn("eligible", system.summary.lower())
            self.assertNotIn("installed", system.summary.lower())

    def test_system_financial_obligations_and_supported_structures_are_represented(self):
        view = self._build()
        structures = {structure.value for structure in view.supported_financing_structures}

        for expected in [
            EnergyPassportFinancingStructure.cash_purchase.value,
            EnergyPassportFinancingStructure.solar_loan.value,
            EnergyPassportFinancingStructure.home_improvement_loan.value,
            EnergyPassportFinancingStructure.personal_loan.value,
            EnergyPassportFinancingStructure.secured_loan.value,
            EnergyPassportFinancingStructure.unsecured_loan.value,
            EnergyPassportFinancingStructure.heloc.value,
            EnergyPassportFinancingStructure.lease.value,
            EnergyPassportFinancingStructure.power_purchase_agreement.value,
            EnergyPassportFinancingStructure.pace_assessment.value,
            EnergyPassportFinancingStructure.utility_program.value,
            EnergyPassportFinancingStructure.contractor_originated_financing.value,
            EnergyPassportFinancingStructure.manufacturer_financing.value,
            EnergyPassportFinancingStructure.subscription_service.value,
            EnergyPassportFinancingStructure.third_party_owned.value,
            EnergyPassportFinancingStructure.unknown.value,
            EnergyPassportFinancingStructure.needs_confirmation.value,
        ]:
            self.assertIn(expected, structures)

        self.assertTrue(view.system_financial_obligations)
        for obligation in view.system_financial_obligations:
            self.assertEqual("needs_confirmation", obligation.ownership_status.value)
            self.assertEqual("needs_confirmation", obligation.financing_structure.value)
            self.assertTrue(obligation.non_authoritative)
            self.assertTrue(obligation.needs_confirmation)
            self.assertIn("purchase agreement", obligation.documents_needed)
            self.assertIn("PPA agreement", obligation.documents_needed)
            self.assertIn("UCC/lien filing confirmation", obligation.documents_needed)

    def test_transfer_relevance_flags_and_readiness_degrade_for_unknown_inputs(self):
        view = self._build()
        flags = {flag.value for flag in view.supported_transfer_relevance_flags}

        for expected in [flag.value for flag in EnergyPassportTransferRelevanceFlag]:
            self.assertIn(expected, flags)

        self.assertEqual(
            EnergyPassportTransferReadinessLevel.blocked_by_missing_inputs,
            view.transfer_readiness.readiness_level,
        )
        self.assertFalse(view.transfer_readiness.transfer_ready)
        self.assertTrue(view.transfer_readiness.missing_transfer_inputs)
        self.assertIn("confirm financing structure", view.transfer_readiness.confirmation_needed)
        self.assertTrue(view.transfer_readiness.buyer_disclosure_recommended)
        self.assertTrue(view.transfer_readiness.contractor_review_recommended)

    def test_no_legal_financial_title_warranty_permit_payoff_lien_validation_claims(self):
        view = self._build()
        payload = view.dict()
        forbidden_true_flags = [
            key
            for key, value in payload["capability_boundary_flags"].items()
            if key
            in {
                "title_claim_present",
                "escrow_claim_present",
                "deed_claim_present",
                "lease_assignment_present",
                "payoff_calculation_present",
                "lien_ucc_title_search_present",
                "warranty_validation_present",
                "permit_validation_present",
                "appraisal_present",
                "underwriting_present",
                "tax_advice_present",
                "financial_conclusion_present",
                "crm_write_present",
                "persistence_present",
                "migrations_present",
                "auth_security_changes_present",
                "permission_enforcement_present",
                "deploy_present",
                "push_present",
            }
            and value
        ]
        self.assertEqual([], forbidden_true_flags)
        self.assertIn("not a legal", " ".join(view.limitations).lower())
        self.assertIn("does not validate transfer", view.summary.non_authoritative_summary.lower())


if __name__ == "__main__":
    unittest.main()

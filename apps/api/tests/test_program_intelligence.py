import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import tests.fast_db  # noqa: F401, E402  must precede app imports (binds in-memory DB)

from app.main import app  # noqa: E402
from app.program_intelligence.router import get_program_intelligence  # noqa: E402
from app.program_intelligence.schemas import (  # noqa: E402
    GridEdgeReadinessArea,
    ProgramAwarenessCategory,
    ProgramIntelligenceStatus,
)
from app.services.program_intelligence import program_intelligence_service  # noqa: E402


def _record(entity_type, entity_id, record):
    return SimpleNamespace(entity_type=entity_type, entity_id=entity_id, record=record)


def _section(section_key, records):
    return SimpleNamespace(section_key=section_key, records=records)


def _fake_context_with_program_inputs():
    return SimpleNamespace(
        sections=[
            _section(
                "home",
                [
                    _record(
                        "home",
                        "home_001",
                        {
                            "name": "Test Home",
                            "state": "CA",
                            "postal_code": "90001",
                            "country": "US",
                            "utility_provider": "Example Utility",
                        },
                    )
                ],
            ),
            _section(
                "equipment_products",
                [
                    _record("equipment_product", "pv_001", {"product_type": "solar_panel", "name": "PV module"}),
                    _record("equipment_product", "bat_001", {"product_type": "battery", "name": "Battery"}),
                    _record("equipment_product", "span_001", {"product_type": "smart_panel", "name": "Smart panel"}),
                    _record("equipment_product", "ev_001", {"product_type": "ev_charger", "name": "EV charger"}),
                ],
            ),
            _section(
                "electrical_panels",
                [_record("electrical_panel", "panel_001", {"panel_type": "smart_panel", "name": "Smart panel"})],
            ),
            _section(
                "loads",
                [
                    _record(
                        "load",
                        "load_001",
                        {"name": "EV charger", "backup_priority": "preferred", "controllable": True},
                    )
                ],
            ),
            _section(
                "energy_system_designs",
                [
                    _record(
                        "energy_system_design",
                        "design_001",
                        {"design_goal": "whole_home_backup", "name": "Backup planning design"},
                    )
                ],
            ),
        ]
    )


def _fake_context_unknowns():
    return SimpleNamespace(
        sections=[
            _section(
                "home",
                [
                    _record(
                        "home",
                        "home_002",
                        {
                            "name": "Unknown Utility Home",
                            "country": "US",
                        },
                    )
                ],
            )
        ]
    )


class ProgramIntelligenceTests(unittest.TestCase):
    def _build(self, context=None):
        with patch(
            "app.services.twin_planning_context.twin_planning_context_service.build",
            return_value=context or _fake_context_with_program_inputs(),
        ):
            return program_intelligence_service.build_home_program_intelligence(None, "home_001")

    def test_route_registration_and_response_is_home_id_anchored(self):
        paths = {getattr(route, "path", None) for route in app.routes}
        self.assertIn("/api/program-intelligence/homes/{home_id}", paths)

        view = self._build()
        with patch(
            "app.program_intelligence.router.program_intelligence_service.build_home_program_intelligence",
            return_value=view,
        ):
            response = get_program_intelligence("home_001", None)

        self.assertEqual("home_001", response.home_id)
        self.assertEqual("home_id", response.anchor_type)
        self.assertEqual("request_time_derived_not_persisted", response.generated_at)

    def test_scope_flags_are_read_only_additive_request_time_and_false_for_hard_stops(self):
        scope = self._build().scope
        self.assertTrue(scope.read_only)
        self.assertTrue(scope.additive_only)
        self.assertTrue(scope.request_time_only)
        self.assertTrue(scope.home_id_anchored)
        self.assertTrue(scope.deterministic_for_same_inputs)
        self.assertTrue(scope.non_authoritative)

        for attr in [
            "persistence_present",
            "migrations_present",
            "write_endpoints_present",
            "background_jobs_present",
            "external_api_calls_present",
            "auth_security_changes_present",
            "permission_enforcement_present",
            "enrollment_workflow_present",
            "rebate_calculation_present",
            "incentive_calculation_present",
            "tariff_optimization_present",
            "eligibility_determination_present",
            "utility_dispatch_present",
            "device_control_present",
            "demand_response_execution_present",
            "grid_services_execution_present",
            "billing_logic_present",
            "pricing_logic_present",
            "proposal_generation_present",
            "crm_integration_present",
            "email_automation_present",
            "export_present",
            "push_present",
        ]:
            self.assertFalse(getattr(scope, attr), attr)

    def test_output_is_deterministic_and_reports_source_provenance(self):
        first = self._build().dict()
        second = self._build().dict()

        self.assertEqual(first, second)
        self.assertTrue(first["source_basis"]["request_time_derived"])
        self.assertFalse(first["source_basis"]["external_api_call_present"])
        self.assertFalse(first["source_basis"]["authoritative_program_claim_present"])
        self.assertFalse(first["source_basis"]["authoritative_eligibility_claim_present"])
        self.assertIn("TwinPlanningContext", first["source_basis"]["source_views"])
        self.assertTrue(first["source_basis"]["source_refs"])
        self.assertTrue(first["source_basis"]["utility_refs"])

    def test_unknown_input_degradation_reports_missing_inputs_blockers_and_gates(self):
        view = self._build(_fake_context_unknowns())

        self.assertEqual(ProgramIntelligenceStatus.needs_confirmation, view.summary.overall_status)
        for expected in [
            "utility_unknown",
            "rate_plan_unknown",
            "battery_configuration_unknown",
            "export_status_unknown",
            "interconnection_status_unknown",
            "equipment_compatibility_unknown",
            "program_jurisdiction_unknown",
        ]:
            self.assertIn(expected, view.missing_inputs)
        self.assertTrue(view.blockers)
        self.assertIn("utility_provider_confirmed", view.confirmation_gates)
        self.assertIn("rate_plan_confirmed", view.confirmation_gates)
        self.assertIn("interconnection_status_confirmed", view.confirmation_gates)

    def test_required_program_and_grid_edge_sections_are_present(self):
        view = self._build()

        self.assertEqual(
            {category.value for category in ProgramAwarenessCategory},
            {item.category.value for item in view.program_awareness},
        )
        self.assertEqual(
            {area.value for area in GridEdgeReadinessArea},
            {item.readiness_area.value for item in view.grid_edge_readiness},
        )
        self.assertEqual(7, view.summary.program_awareness_count)
        self.assertEqual(6, view.summary.grid_edge_readiness_count)
        self.assertTrue(view.interpretation.homeowner_safe_summary)
        self.assertTrue(view.interpretation.contractor_program_review_prompts)
        self.assertTrue(view.interpretation.verification_recommendations)
        self.assertTrue(view.interpretation.do_not_assume)

    def test_no_authoritative_eligibility_enrollment_dispatch_control_or_pricing_claims(self):
        view = self._build()
        payload = view.dict()
        self.assertFalse(payload["summary"]["eligibility_determined"])
        self.assertFalse(payload["summary"]["enrollment_available"])
        self.assertFalse(payload["summary"]["dispatch_or_control_available"])
        self.assertFalse(payload["summary"]["pricing_or_billing_available"])
        for key in [
            "enrollment_workflow_present",
            "eligibility_determination_present",
            "utility_dispatch_present",
            "device_control_present",
            "demand_response_execution_present",
            "grid_services_execution_present",
            "billing_logic_present",
            "pricing_logic_present",
        ]:
            self.assertFalse(payload["capability_boundary_flags"][key], key)

        user_facing_text = " ".join(
            [view.summary.summary_boundary_note]
            + [item.summary for item in view.program_awareness]
            + [item.homeowner_summary for item in view.program_awareness]
            + [item.summary for item in view.grid_edge_readiness]
            + [item.homeowner_summary for item in view.grid_edge_readiness]
        ).lower()
        for forbidden in [
            "eligible",
            "enrolled",
            "dispatch enabled",
            "device control enabled",
            "rebate calculated",
            "savings calculated",
            "tariff optimized",
            "utility approved",
        ]:
            self.assertNotIn(forbidden, user_facing_text)

        serialized = json.dumps(payload, sort_keys=True).lower()
        self.assertIn("do not assume program availability", serialized)
        self.assertIn("does not determine qualification", serialized)


if __name__ == "__main__":
    unittest.main()

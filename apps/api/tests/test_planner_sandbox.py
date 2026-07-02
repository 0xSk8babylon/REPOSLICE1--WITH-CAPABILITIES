import json
import unittest

import tests.fast_db  # noqa: F401, E402  must precede app imports (binds in-memory DB)
from app.main import app  # noqa: E402
from app.planner_sandbox.router import list_guided_templates, validate_sandbox_draft  # noqa: E402
from app.planner_sandbox.schemas import (  # noqa: E402
    DraftAssumptions,
    DraftInputs,
    DraftInputValue,
    DraftValidationRequest,
    PlannerSandboxMaturityState,
    PlannerSandboxValidationStatus,
    SandboxDraft,
)
from app.services.planner_sandbox import planner_sandbox_service  # noqa: E402


def _complete_backup_draft():
    return SandboxDraft(
        draft_id="sandbox_draft_001",
        template_id="guided_backup_basics_v0",
        maturity_state=PlannerSandboxMaturityState.draft,
        draft_inputs=DraftInputs(
            template_id="guided_backup_basics_v0",
            values=[
                DraftInputValue(input_key="home_context_summary", value="Two-story home with existing panel notes."),
                DraftInputValue(input_key="backup_goal", value="partial_home"),
                DraftInputValue(input_key="essential_loads", value=["refrigerator", "network", "well_pump"]),
                DraftInputValue(input_key="known_constraints", value=["outdoor equipment space needs review"]),
            ],
            source_basis=["manual_sandbox_entry"],
        ),
        draft_assumptions=DraftAssumptions(
            accepted_assumption_keys=["site_conditions_unverified", "load_values_planning_only"]
        ),
    )


class PlannerSandboxTests(unittest.TestCase):
    def test_routes_are_registered_without_frontend_or_home_scope(self):
        paths = set(app.openapi()["paths"])
        self.assertIn("/api/planner-sandbox/templates", paths)
        self.assertIn("/api/planner-sandbox/templates/{template_id}", paths)
        self.assertIn("/api/planner-sandbox/drafts/validate", paths)

        registry = list_guided_templates()
        self.assertTrue(registry.read_only)
        self.assertFalse(registry.capability_boundary_flags["frontend_wiring_present"])
        self.assertFalse(registry.capability_boundary_flags["production_persistence_present"])

    def test_registry_exposes_guided_templates_and_maturity_states(self):
        registry = planner_sandbox_service.list_guided_templates()

        self.assertEqual("planner_sandbox_guided_templates", registry.registry_name)
        self.assertEqual(
            [
                "template_seeded",
                "draft",
                "checked",
                "validated",
                "project_candidate",
            ],
            [state.value for state in registry.maturity_states],
        )
        self.assertEqual(
            ["guided_backup_basics_v0", "guided_solar_storage_sketch_v0"],
            [template.template_id for template in registry.templates],
        )
        for template in registry.templates:
            self.assertTrue(template.read_only_registry)
            self.assertEqual(PlannerSandboxMaturityState.template_seeded, template.starting_maturity_state)
            self.assertTrue(template.draft_input_definitions)
            self.assertTrue(template.default_assumptions)
            self.assertTrue(template.steps)

    def test_validation_result_is_deterministic_and_non_persistent(self):
        request = DraftValidationRequest(
            draft=_complete_backup_draft(),
            requested_maturity_state=PlannerSandboxMaturityState.project_candidate,
        )

        first = planner_sandbox_service.validate_draft(request).dict()
        second = planner_sandbox_service.validate_draft(request).dict()

        self.assertEqual(first, second)
        self.assertEqual("project_candidate", first["resulting_maturity_state"])
        self.assertEqual("project_candidate", first["validation_status"])
        self.assertTrue(first["deterministic_for_same_inputs"])
        self.assertTrue(first["non_authoritative"])
        self.assertFalse(first["ready_for_project_creation"])
        self.assertFalse(first["persisted"])
        self.assertFalse(first["production_record_created"])
        self.assertEqual([], first["issues"])

    def test_missing_required_inputs_and_assumptions_stay_checked(self):
        draft = _complete_backup_draft()
        draft.draft_inputs.values = [
            DraftInputValue(input_key="home_context_summary", value="Context only."),
            DraftInputValue(input_key="backup_goal", value="partial_home"),
        ]
        draft.draft_assumptions.accepted_assumption_keys = ["site_conditions_unverified"]
        result = planner_sandbox_service.validate_draft(
            DraftValidationRequest(draft=draft, requested_maturity_state=PlannerSandboxMaturityState.validated)
        )

        self.assertEqual(PlannerSandboxMaturityState.checked, result.resulting_maturity_state)
        self.assertEqual(PlannerSandboxValidationStatus.needs_inputs, result.validation_status)
        self.assertEqual(["essential_loads"], result.missing_required_inputs)
        self.assertEqual(["load_values_planning_only"], result.missing_required_assumptions)
        self.assertEqual(
            ["required_input_missing", "required_assumption_missing"],
            [issue.issue_key for issue in result.issues],
        )

    def test_authority_claim_language_blocks_validation_without_echoing_claim(self):
        draft = _complete_backup_draft()
        draft.draft_inputs.values[0].value = "This is approved and guaranteed."

        result = validate_sandbox_draft(
            DraftValidationRequest(draft=draft, requested_maturity_state=PlannerSandboxMaturityState.validated)
        )

        self.assertEqual(PlannerSandboxValidationStatus.blocked_by_authority_claims, result.validation_status)
        self.assertEqual(PlannerSandboxMaturityState.checked, result.resulting_maturity_state)
        self.assertEqual(["authority_claim_present"], [issue.issue_key for issue in result.issues])
        serialized = json.dumps(result.dict(), sort_keys=True).lower()
        self.assertNotIn("this is approved and guaranteed", serialized)

    def test_returned_objects_do_not_use_forbidden_approval_or_engineering_claims(self):
        registry_payload = planner_sandbox_service.list_guided_templates().dict()
        validation_payload = planner_sandbox_service.validate_draft(
            DraftValidationRequest(
                draft=_complete_backup_draft(),
                requested_maturity_state=PlannerSandboxMaturityState.project_candidate,
            )
        ).dict()
        serialized = json.dumps(
            {"registry": registry_payload, "validation": validation_payload},
            sort_keys=True,
        ).lower()

        self.assertIn("planning-only", serialized)
        self.assertIn("non_authoritative", serialized)
        for forbidden in [
            "approved",
            "approval",
            "engineered",
            "engineering",
            "permit-ready",
            "certified",
            "guaranteed",
            "stamped",
            "utility approved",
        ]:
            self.assertNotIn(forbidden, serialized)


if __name__ == "__main__":
    unittest.main()


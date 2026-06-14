from typing import Dict, List, Optional, Set

from app.core.types import ConfidenceLevel
from app.planner_sandbox.schemas import (
    DraftAssumptionDefinition,
    DraftInputDefinition,
    DraftValidationIssue,
    DraftValidationRequest,
    DraftValidationResult,
    GuidedTemplate,
    GuidedTemplateRegistry,
    GuidedTemplateStep,
    PlannerSandboxMaturityState,
    PlannerSandboxValidationStatus,
)


PLANNER_SANDBOX_LIMITATIONS = [
    "Planner Sandbox Mode is request-time contract behavior only.",
    "No sandbox response creates production persistence, project records, contractor sharing, product ingestion, external service behavior, pricing, or frontend behavior.",
    "Sandbox maturity states describe draft completeness only and do not create final design, compliance, permitting, utility, safety, pricing, contractor, or project authority.",
]

PLANNER_SANDBOX_BOUNDARY_FLAGS = {
    "read_only_template_registry": True,
    "production_persistence_present": False,
    "migration_present": False,
    "auth_change_present": False,
    "contractor_sharing_present": False,
    "project_creation_present": False,
    "delete_endpoint_present": False,
    "drag_drop_canvas_present": False,
    "product_ingestion_present": False,
    "external_service_present": False,
    "frontend_wiring_present": False,
    "pricing_logic_present": False,
    "compliance_determination_present": False,
    "permitting_status_present": False,
    "utility_status_present": False,
    "contractor_commitment_present": False,
}

AUTHORITY_CLAIM_MARKERS = [
    "approved",
    "approval",
    "certified",
    "code compliant",
    "code-compliant",
    "engineered",
    "engineering",
    "final design",
    "guaranteed",
    "permit ready",
    "permit-ready",
    "stamped",
    "utility approved",
]


class PlannerSandboxService:
    def list_guided_templates(self) -> GuidedTemplateRegistry:
        return GuidedTemplateRegistry(
            templates=self._templates(),
            maturity_states=[
                PlannerSandboxMaturityState.template_seeded,
                PlannerSandboxMaturityState.draft,
                PlannerSandboxMaturityState.checked,
                PlannerSandboxMaturityState.validated,
                PlannerSandboxMaturityState.project_candidate,
            ],
            capability_boundary_flags=dict(PLANNER_SANDBOX_BOUNDARY_FLAGS),
            limitations=list(PLANNER_SANDBOX_LIMITATIONS),
        )

    def get_guided_template(self, template_id: str) -> Optional[GuidedTemplate]:
        return self._template_map().get(template_id)

    def validate_draft(self, request: DraftValidationRequest) -> DraftValidationResult:
        template = self.get_guided_template(request.draft.template_id)
        if template is None:
            return DraftValidationResult(
                draft_id=request.draft.draft_id,
                template_id=request.draft.template_id,
                requested_maturity_state=request.requested_maturity_state,
                resulting_maturity_state=PlannerSandboxMaturityState.checked,
                validation_status=PlannerSandboxValidationStatus.needs_inputs,
                template_found=False,
                maturity_state_reason="Template is not present in the read-only sandbox registry.",
                capability_boundary_flags=dict(PLANNER_SANDBOX_BOUNDARY_FLAGS),
                limitations=list(PLANNER_SANDBOX_LIMITATIONS),
            )

        values_by_key = {
            item.input_key: item
            for item in sorted(request.draft.draft_inputs.values, key=lambda value: value.input_key)
        }
        required_input_keys = sorted(
            definition.input_key for definition in template.draft_input_definitions if definition.required
        )
        missing_required_inputs = [
            key for key in required_input_keys if key not in values_by_key or self._value_is_missing(values_by_key[key].value)
        ]
        required_assumptions = sorted(
            assumption.assumption_key
            for assumption in template.default_assumptions
            if assumption.required_acknowledgement
        )
        accepted_assumptions = set(request.draft.draft_assumptions.accepted_assumption_keys)
        missing_required_assumptions = [
            key for key in required_assumptions if key not in accepted_assumptions
        ]
        authority_claim_keys = self._authority_claim_input_keys(request)

        issues: List[DraftValidationIssue] = []
        for key in missing_required_inputs:
            issues.append(
                DraftValidationIssue(
                    issue_key="required_input_missing",
                    severity="blocking",
                    input_key=key,
                    message="Required sandbox input is missing or blank.",
                )
            )
        for key in missing_required_assumptions:
            issues.append(
                DraftValidationIssue(
                    issue_key="required_assumption_missing",
                    severity="blocking",
                    assumption_key=key,
                    message="Required sandbox assumption has not been acknowledged.",
                )
            )
        for key in authority_claim_keys:
            issues.append(
                DraftValidationIssue(
                    issue_key="authority_claim_present",
                    severity="blocking",
                    input_key=key,
                    message="Draft text includes a claim that exceeds sandbox planning authority.",
                )
            )

        if authority_claim_keys:
            status = PlannerSandboxValidationStatus.blocked_by_authority_claims
            maturity = PlannerSandboxMaturityState.checked
            reason = "Draft was checked, but authority claims must be removed before maturity can advance."
        elif missing_required_inputs or missing_required_assumptions:
            status = PlannerSandboxValidationStatus.needs_inputs
            maturity = PlannerSandboxMaturityState.checked
            reason = "Draft was checked, but required inputs or assumptions are still missing."
        elif request.requested_maturity_state == PlannerSandboxMaturityState.project_candidate:
            status = PlannerSandboxValidationStatus.project_candidate
            maturity = PlannerSandboxMaturityState.project_candidate
            reason = "Draft has complete sandbox inputs and can be marked as a project candidate without creating a project."
        else:
            status = PlannerSandboxValidationStatus.validated
            maturity = PlannerSandboxMaturityState.validated
            reason = "Draft has complete sandbox inputs for this template."

        return DraftValidationResult(
            draft_id=request.draft.draft_id,
            template_id=request.draft.template_id,
            requested_maturity_state=request.requested_maturity_state,
            resulting_maturity_state=maturity,
            validation_status=status,
            ready_for_project_creation=False,
            persisted=False,
            production_record_created=False,
            issues=issues,
            missing_required_inputs=missing_required_inputs,
            missing_required_assumptions=missing_required_assumptions,
            checked_input_keys=sorted(values_by_key.keys()),
            maturity_state_reason=reason,
            capability_boundary_flags=dict(PLANNER_SANDBOX_BOUNDARY_FLAGS),
            limitations=list(PLANNER_SANDBOX_LIMITATIONS),
        )

    def _template_map(self) -> Dict[str, GuidedTemplate]:
        return {template.template_id: template for template in self._templates()}

    def _templates(self) -> List[GuidedTemplate]:
        return [
            GuidedTemplate(
                template_id="guided_backup_basics_v0",
                version="v0",
                name="Backup Basics",
                summary="Starter sandbox template for exploring backup scope, essential loads, and known site constraints.",
                allowed_maturity_states=[
                    PlannerSandboxMaturityState.template_seeded,
                    PlannerSandboxMaturityState.draft,
                    PlannerSandboxMaturityState.checked,
                    PlannerSandboxMaturityState.validated,
                    PlannerSandboxMaturityState.project_candidate,
                ],
                draft_input_definitions=[
                    DraftInputDefinition(
                        input_key="home_context_summary",
                        label="Home context summary",
                        category="home_context",
                        value_type="text",
                        required=True,
                    ),
                    DraftInputDefinition(
                        input_key="backup_goal",
                        label="Backup goal",
                        category="goals",
                        value_type="enum",
                        required=True,
                        allowed_values=["critical_loads", "partial_home", "whole_home", "unknown"],
                    ),
                    DraftInputDefinition(
                        input_key="essential_loads",
                        label="Essential loads",
                        category="loads",
                        value_type="list",
                        required=True,
                    ),
                    DraftInputDefinition(
                        input_key="known_constraints",
                        label="Known constraints",
                        category="site_constraints",
                        value_type="list",
                    ),
                ],
                default_assumptions=[
                    DraftAssumptionDefinition(
                        assumption_key="site_conditions_unverified",
                        label="Site conditions unverified",
                        default_text="Site conditions must be checked outside the sandbox before use.",
                    ),
                    DraftAssumptionDefinition(
                        assumption_key="load_values_planning_only",
                        label="Load values planning-only",
                        default_text="Load values may be placeholders until supported by source records.",
                    ),
                ],
                steps=[
                    GuidedTemplateStep(
                        step_id="seed_context",
                        title="Seed context",
                        input_keys=["home_context_summary", "backup_goal"],
                        maturity_state_after_step=PlannerSandboxMaturityState.draft,
                    ),
                    GuidedTemplateStep(
                        step_id="check_inputs",
                        title="Check inputs",
                        input_keys=["essential_loads", "known_constraints"],
                        maturity_state_after_step=PlannerSandboxMaturityState.checked,
                    ),
                    GuidedTemplateStep(
                        step_id="validate_draft",
                        title="Validate draft",
                        input_keys=[],
                        maturity_state_after_step=PlannerSandboxMaturityState.validated,
                    ),
                ],
                limitations=list(PLANNER_SANDBOX_LIMITATIONS),
            ),
            GuidedTemplate(
                template_id="guided_solar_storage_sketch_v0",
                version="v0",
                name="Solar Storage Sketch",
                summary="Starter sandbox template for sketching PV, storage, panel, and utility context before any project record exists.",
                allowed_maturity_states=[
                    PlannerSandboxMaturityState.template_seeded,
                    PlannerSandboxMaturityState.draft,
                    PlannerSandboxMaturityState.checked,
                    PlannerSandboxMaturityState.validated,
                    PlannerSandboxMaturityState.project_candidate,
                ],
                draft_input_definitions=[
                    DraftInputDefinition(
                        input_key="solar_interest",
                        label="Solar interest",
                        category="goals",
                        value_type="enum",
                        required=True,
                        allowed_values=["bill_offset", "backup_support", "future_ready", "unknown"],
                    ),
                    DraftInputDefinition(
                        input_key="storage_interest",
                        label="Storage interest",
                        category="goals",
                        value_type="enum",
                        required=True,
                        allowed_values=["none", "partial_backup", "whole_home", "unknown"],
                    ),
                    DraftInputDefinition(
                        input_key="panel_context",
                        label="Panel context",
                        category="electrical_context",
                        value_type="text",
                    ),
                    DraftInputDefinition(
                        input_key="utility_context",
                        label="Utility context",
                        category="utility_context",
                        value_type="text",
                    ),
                ],
                default_assumptions=[
                    DraftAssumptionDefinition(
                        assumption_key="roof_and_shading_unverified",
                        label="Roof and shading unverified",
                        default_text="Roof, shading, and structural context are not established by this template.",
                    ),
                    DraftAssumptionDefinition(
                        assumption_key="utility_terms_unverified",
                        label="Utility terms unverified",
                        default_text="Utility, interconnection, export, and program terms are not checked by this template.",
                    ),
                ],
                steps=[
                    GuidedTemplateStep(
                        step_id="seed_goals",
                        title="Seed goals",
                        input_keys=["solar_interest", "storage_interest"],
                        maturity_state_after_step=PlannerSandboxMaturityState.draft,
                    ),
                    GuidedTemplateStep(
                        step_id="check_context",
                        title="Check context",
                        input_keys=["panel_context", "utility_context"],
                        maturity_state_after_step=PlannerSandboxMaturityState.checked,
                    ),
                    GuidedTemplateStep(
                        step_id="validate_draft",
                        title="Validate draft",
                        input_keys=[],
                        maturity_state_after_step=PlannerSandboxMaturityState.validated,
                    ),
                ],
                limitations=list(PLANNER_SANDBOX_LIMITATIONS),
            ),
        ]

    def _value_is_missing(self, value) -> bool:
        if value is None:
            return True
        if isinstance(value, str) and not value.strip():
            return True
        if isinstance(value, (list, dict, set, tuple)) and not value:
            return True
        return False

    def _authority_claim_input_keys(self, request: DraftValidationRequest) -> List[str]:
        claim_keys: Set[str] = set()
        for item in request.draft.draft_inputs.values:
            if self._contains_authority_claim(item.value):
                claim_keys.add(item.input_key)
        for custom_assumption in request.draft.draft_assumptions.custom_assumptions:
            if self._contains_authority_claim(custom_assumption):
                claim_keys.add("custom_assumptions")
        return sorted(claim_keys)

    def _contains_authority_claim(self, value) -> bool:
        if value is None:
            return False
        if isinstance(value, (list, tuple, set)):
            return any(self._contains_authority_claim(item) for item in value)
        if isinstance(value, dict):
            return any(self._contains_authority_claim(item) for item in value.values())
        text = str(value).lower()
        return any(marker in text for marker in AUTHORITY_CLAIM_MARKERS)


planner_sandbox_service = PlannerSandboxService()


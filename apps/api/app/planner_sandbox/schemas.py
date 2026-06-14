from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field

from app.core.schemas import ORMModel
from app.core.types import AuthorityLayer, ConfidenceLevel, DataClassification


class PlannerSandboxMaturityState(str, Enum):
    template_seeded = "template_seeded"
    draft = "draft"
    checked = "checked"
    validated = "validated"
    project_candidate = "project_candidate"


class PlannerSandboxValidationStatus(str, Enum):
    needs_inputs = "needs_inputs"
    blocked_by_authority_claims = "blocked_by_authority_claims"
    checked = "checked"
    validated = "validated"
    project_candidate = "project_candidate"


class DraftInputDefinition(ORMModel):
    input_key: str
    label: str
    category: str
    value_type: str
    required: bool = False
    unit: Optional[str] = None
    allowed_values: List[str] = Field(default_factory=list)
    placeholder_allowed: bool = True
    non_authoritative_note: str = (
        "Planning-only sandbox input; it does not create final design, compliance, permitting, utility, safety, "
        "pricing, contractor, or project authority."
    )


class DraftInputValue(ORMModel):
    input_key: str
    value: Optional[Any] = None
    unit: Optional[str] = None
    source_label: Optional[str] = None
    confidence_level: ConfidenceLevel = ConfidenceLevel.low
    assumption_label: Optional[str] = None
    placeholder: bool = False
    non_authoritative_note: str = (
        "Planning-only sandbox value; verify against source records before using outside the sandbox."
    )


class DraftInputs(ORMModel):
    template_id: str
    values: List[DraftInputValue] = Field(default_factory=list)
    input_boundary_note: str = (
        "Draft inputs are sandbox planning data only and are not saved as production facts or project records."
    )
    source_basis: List[str] = Field(default_factory=list)


class DraftAssumptionDefinition(ORMModel):
    assumption_key: str
    label: str
    default_text: str
    required_acknowledgement: bool = True
    non_authoritative_note: str = (
        "Assumption is for sandbox planning only and must be replaced or confirmed before use outside this mode."
    )


class DraftAssumptions(ORMModel):
    accepted_assumption_keys: List[str] = Field(default_factory=list)
    custom_assumptions: List[str] = Field(default_factory=list)
    assumption_boundary_note: str = (
        "Assumptions remain explicitly labeled and do not establish compliance, permitting, utility, safety, "
        "pricing, contractor, or project authority."
    )


class GuidedTemplateStep(ORMModel):
    step_id: str
    title: str
    input_keys: List[str] = Field(default_factory=list)
    maturity_state_after_step: PlannerSandboxMaturityState


class GuidedTemplate(ORMModel):
    template_id: str
    version: str
    name: str
    summary: str
    starting_maturity_state: PlannerSandboxMaturityState = PlannerSandboxMaturityState.template_seeded
    allowed_maturity_states: List[PlannerSandboxMaturityState] = Field(default_factory=list)
    draft_input_definitions: List[DraftInputDefinition] = Field(default_factory=list)
    default_assumptions: List[DraftAssumptionDefinition] = Field(default_factory=list)
    steps: List[GuidedTemplateStep] = Field(default_factory=list)
    authority_layer: AuthorityLayer = AuthorityLayer.advisory
    data_classification: DataClassification = DataClassification.planning_private
    read_only_registry: bool = True
    non_authoritative_note: str = (
        "Guided templates seed sandbox drafts for planning review only; they do not create final design, "
        "compliance, permitting, utility, safety, pricing, contractor, or project authority."
    )
    limitations: List[str] = Field(default_factory=list)


class GuidedTemplateRegistry(ORMModel):
    registry_name: str = "planner_sandbox_guided_templates"
    version: str = "v0"
    read_only: bool = True
    generated_at: str = "request_time_static_registry"
    templates: List[GuidedTemplate] = Field(default_factory=list)
    maturity_states: List[PlannerSandboxMaturityState] = Field(default_factory=list)
    non_authoritative_note: str = (
        "Registry entries are sandbox contract templates only and do not create production persistence, project "
        "records, compliance findings, permitting status, utility status, pricing, or contractor commitments."
    )
    capability_boundary_flags: Dict[str, bool] = Field(default_factory=dict)
    limitations: List[str] = Field(default_factory=list)


class SandboxDraft(ORMModel):
    draft_id: str
    template_id: str
    maturity_state: PlannerSandboxMaturityState = PlannerSandboxMaturityState.draft
    draft_inputs: DraftInputs
    draft_assumptions: DraftAssumptions = Field(default_factory=DraftAssumptions)
    non_authoritative_note: str = (
        "Sandbox draft is not persisted as a project and does not create final design, compliance, permitting, "
        "utility, safety, pricing, contractor, or project authority."
    )


class DraftValidationIssue(ORMModel):
    issue_key: str
    severity: str
    input_key: Optional[str] = None
    assumption_key: Optional[str] = None
    message: str
    non_authoritative_note: str = "Validation issue is a sandbox planning prompt only."


class DraftValidationRequest(ORMModel):
    draft: SandboxDraft
    requested_maturity_state: PlannerSandboxMaturityState = PlannerSandboxMaturityState.checked


class DraftValidationResult(ORMModel):
    draft_id: str
    template_id: str
    requested_maturity_state: PlannerSandboxMaturityState
    resulting_maturity_state: PlannerSandboxMaturityState
    validation_status: PlannerSandboxValidationStatus
    deterministic_for_same_inputs: bool = True
    non_authoritative: bool = True
    template_found: bool = True
    ready_for_project_creation: bool = False
    persisted: bool = False
    production_record_created: bool = False
    issues: List[DraftValidationIssue] = Field(default_factory=list)
    missing_required_inputs: List[str] = Field(default_factory=list)
    missing_required_assumptions: List[str] = Field(default_factory=list)
    checked_input_keys: List[str] = Field(default_factory=list)
    maturity_state_reason: str
    capability_boundary_flags: Dict[str, bool] = Field(default_factory=dict)
    non_authoritative_note: str = (
        "Sandbox validation checks draft completeness only; it does not create final design, compliance, "
        "permitting, utility, safety, pricing, contractor, or project authority."
    )
    limitations: List[str] = Field(default_factory=list)


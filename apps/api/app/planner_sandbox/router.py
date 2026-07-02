from fastapi import APIRouter, HTTPException

from app.planner_sandbox.schemas import (
    DraftValidationRequest,
    DraftValidationResult,
    GuidedTemplate,
    GuidedTemplateRegistry,
)
from app.services.planner_sandbox import planner_sandbox_service

router = APIRouter(prefix="/planner-sandbox", tags=["planner_sandbox"])


@router.get("/templates", response_model=GuidedTemplateRegistry)
def list_guided_templates():
    return planner_sandbox_service.list_guided_templates()


@router.get("/templates/{template_id}", response_model=GuidedTemplate)
def get_guided_template(template_id: str):
    template = planner_sandbox_service.get_guided_template(template_id)
    if template is None:
        raise HTTPException(status_code=404, detail="Guided template not found")
    return template


@router.post("/drafts/validate", response_model=DraftValidationResult)
def validate_sandbox_draft(payload: DraftValidationRequest):
    result = planner_sandbox_service.validate_draft(payload)
    if not result.template_found:
        raise HTTPException(status_code=404, detail="Guided template not found")
    return result


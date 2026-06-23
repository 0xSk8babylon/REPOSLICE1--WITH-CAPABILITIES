from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.repository import repository
from app.planning.schemas import (
    DesignGoalPreset,
    DesignGoalPresetCreate,
    DesignGoalPresetUpdate,
    EstimatedPathway,
    EstimatedPathwayCreate,
    EstimatedPathwayUpdate,
    LoadTemplate,
    LoadTemplateCreate,
    LoadTemplateUpdate,
)
from app.services.provenance import provenance_service

estimated_pathways_router = APIRouter(prefix="/estimated-pathways", tags=["estimated_pathways"])
load_templates_router = APIRouter(prefix="/load-templates", tags=["load_templates"])
design_goal_presets_router = APIRouter(prefix="/design-goal-presets", tags=["design_goal_presets"])


def _serialize_estimated_pathway(pathway, provenance_summaries=None) -> EstimatedPathway:
    provenance_summaries = provenance_summaries or {}
    return EstimatedPathway.model_validate(pathway).model_copy(update={"provenance_summary": provenance_summaries.get(pathway.id)})


@estimated_pathways_router.get("", response_model=List[EstimatedPathway])
def list_estimated_pathways(home_id: Optional[str] = Query(None), db: Session = Depends(get_db)):
    pathways = repository.list_estimated_pathways(db, home_id=home_id)
    summaries = provenance_service.summarize_entities(db, "estimated_pathway", [pathway.id for pathway in pathways])
    return [_serialize_estimated_pathway(pathway, summaries) for pathway in pathways]


@estimated_pathways_router.post("", response_model=EstimatedPathway)
def create_estimated_pathway(payload: EstimatedPathwayCreate, db: Session = Depends(get_db)):
    pathway = repository.create_estimated_pathway(db, payload)
    summaries = provenance_service.summarize_entities(db, "estimated_pathway", [pathway.id])
    return _serialize_estimated_pathway(pathway, summaries)


@estimated_pathways_router.patch("/{pathway_id}", response_model=EstimatedPathway)
def update_estimated_pathway(pathway_id: str, payload: EstimatedPathwayUpdate, db: Session = Depends(get_db)):
    if repository.get_estimated_pathway(db, pathway_id) is None:
        raise HTTPException(status_code=404, detail="Estimated pathway not found")
    pathway = repository.update_estimated_pathway(db, pathway_id, payload)
    summaries = provenance_service.summarize_entities(db, "estimated_pathway", [pathway.id])
    return _serialize_estimated_pathway(pathway, summaries)


@load_templates_router.get("", response_model=List[LoadTemplate])
def list_load_templates(db: Session = Depends(get_db)):
    return repository.list_load_templates(db)


@load_templates_router.post("", response_model=LoadTemplate)
def create_load_template(payload: LoadTemplateCreate, db: Session = Depends(get_db)):
    return repository.create_load_template(db, payload)


@load_templates_router.patch("/{template_id}", response_model=LoadTemplate)
def update_load_template(template_id: str, payload: LoadTemplateUpdate, db: Session = Depends(get_db)):
    if repository.get_load_template(db, template_id) is None:
        raise HTTPException(status_code=404, detail="Load template not found")
    return repository.update_load_template(db, template_id, payload)


@design_goal_presets_router.get("", response_model=List[DesignGoalPreset])
def list_design_goal_presets(db: Session = Depends(get_db)):
    return repository.list_design_goal_presets(db)


@design_goal_presets_router.post("", response_model=DesignGoalPreset)
def create_design_goal_preset(payload: DesignGoalPresetCreate, db: Session = Depends(get_db)):
    return repository.create_design_goal_preset(db, payload)


@design_goal_presets_router.patch("/{preset_id}", response_model=DesignGoalPreset)
def update_design_goal_preset(preset_id: str, payload: DesignGoalPresetUpdate, db: Session = Depends(get_db)):
    if repository.get_design_goal_preset(db, preset_id) is None:
        raise HTTPException(status_code=404, detail="Design goal preset not found")
    return repository.update_design_goal_preset(db, preset_id, payload)

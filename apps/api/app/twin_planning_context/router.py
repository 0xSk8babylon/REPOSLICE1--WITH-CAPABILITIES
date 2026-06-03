from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.twin_planning_context import twin_planning_context_service
from app.twin_planning_context.schemas import (
    AIDesignGroundingView,
    TwinPlanningContext,
    TwinRuntimeParticipantRole,
    TwinRuntimeProjectionView,
)

router = APIRouter(prefix="/twin-planning-context", tags=["twin_planning_context"])


@router.get("/homes/{home_id}", response_model=TwinPlanningContext)
def get_twin_planning_context(home_id: str, db: Session = Depends(get_db)):
    context = twin_planning_context_service.build(db, home_id)
    if context is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return context


@router.get("/homes/{home_id}/views/ai-design-grounding", response_model=AIDesignGroundingView)
def get_ai_design_grounding_view(
    home_id: str,
    design_id: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    view = twin_planning_context_service.build_ai_design_grounding_view(db, home_id, design_id=design_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home or design not found")
    return view


@router.get("/homes/{home_id}/views/runtime-projection/{role}", response_model=TwinRuntimeProjectionView)
def get_runtime_projection_view(
    home_id: str,
    role: TwinRuntimeParticipantRole,
    db: Session = Depends(get_db),
):
    view = twin_planning_context_service.build_runtime_projection_view(db, home_id, role=role)
    if view is None:
        raise HTTPException(status_code=404, detail="Home or runtime projection role not found")
    return view

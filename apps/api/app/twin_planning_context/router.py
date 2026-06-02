from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.twin_planning_context import twin_planning_context_service
from app.twin_planning_context.schemas import TwinPlanningContext

router = APIRouter(prefix="/twin-planning-context", tags=["twin_planning_context"])


@router.get("/homes/{home_id}", response_model=TwinPlanningContext)
def get_twin_planning_context(home_id: str, db: Session = Depends(get_db)):
    context = twin_planning_context_service.build(db, home_id)
    if context is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return context

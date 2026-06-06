from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.program_intelligence.schemas import ProgramIntelligenceView
from app.services.program_intelligence import program_intelligence_service

router = APIRouter(prefix="/program-intelligence", tags=["program_intelligence"])


@router.get("/homes/{home_id}", response_model=ProgramIntelligenceView)
def get_program_intelligence(home_id: str, db: Session = Depends(get_db)):
    view = program_intelligence_service.build_home_program_intelligence(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view

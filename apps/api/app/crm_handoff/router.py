from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crm_handoff.schemas import CRMHandoffView
from app.services.crm_handoff import crm_handoff_service

router = APIRouter(prefix="/crm-handoff", tags=["crm_handoff"])


@router.get("/homes/{home_id}", response_model=CRMHandoffView)
def get_crm_handoff(home_id: str, db: Session = Depends(get_db)):
    view = crm_handoff_service.build_home_crm_handoff(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view

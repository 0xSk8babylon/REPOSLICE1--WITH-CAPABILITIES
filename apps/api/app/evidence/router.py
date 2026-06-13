from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.repository import repository
from app.evidence.schemas import EvidenceIntakeResult, PhotoEvidenceFactCreate
from app.services.evidence import evidence_intake_service

router = APIRouter(prefix="/evidence/homes/{home_id}", tags=["evidence"])


@router.post("/photo-facts", response_model=EvidenceIntakeResult)
def create_photo_evidence_fact(home_id: str, payload: PhotoEvidenceFactCreate, db: Session = Depends(get_db)):
    if repository.get_home_by_id(db, home_id) is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return evidence_intake_service.photo_evidence_to_fact(db, home_id, payload)

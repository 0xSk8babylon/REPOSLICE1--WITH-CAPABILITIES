from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.repository import repository
from app.privacy.schemas import ConsentRecord, ConsentRecordCreate, PrivacyDeletionResult, PrivacyExport
from app.services.privacy import privacy_service

router = APIRouter(prefix="/privacy/homes/{home_id}", tags=["privacy"])


@router.get("/export", response_model=PrivacyExport)
def export_homeowner_record(home_id: str, db: Session = Depends(get_db)):
    if repository.get_home_by_id(db, home_id) is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return privacy_service.export_homeowner_record(db, home_id)


@router.post("/consent", response_model=ConsentRecord)
def record_consent(home_id: str, payload: ConsentRecordCreate, db: Session = Depends(get_db)):
    if payload.home_id != home_id:
        raise HTTPException(status_code=400, detail="Payload home_id must match path home_id")
    if repository.get_home_by_id(db, home_id) is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return privacy_service.record_consent(db, payload)


@router.delete("", response_model=PrivacyDeletionResult)
def delete_homeowner_record(home_id: str, db: Session = Depends(get_db)):
    if repository.get_home_by_id(db, home_id) is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return privacy_service.delete_homeowner_record(db, home_id)

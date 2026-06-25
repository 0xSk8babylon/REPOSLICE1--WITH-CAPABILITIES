from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.router import current_principal
from app.core.database import get_db
from app.core.repository import repository
from app.privacy.schemas import ConsentRecord, ConsentRecordCreate, PrivacyDeletionResult, PrivacyExport
from app.security.audit import audit_service
from app.security import permissions
from app.services.privacy import privacy_service

router = APIRouter(prefix="/privacy/homes/{home_id}", tags=["privacy"])


@router.get("/export", response_model=PrivacyExport)
def export_homeowner_record(home_id: str, db: Session = Depends(get_db), principal=Depends(current_principal)):
    if repository.get_home_by_id(db, home_id) is None:
        raise HTTPException(status_code=404, detail="Home not found")
    permissions.require_allowed(permissions.can_privacy_admin_home(db, principal, home_id))
    exported = privacy_service.export_homeowner_record(db, home_id)
    audit_service.record(
        db,
        action="privacy.export",
        method="GET",
        path=f"/api/privacy/homes/{home_id}/export",
        status_code=200,
        authorized=True,
        reason="privacy export authorized",
        principal=principal,
        home_id=home_id,
        object_type="home",
        object_id=home_id,
        route_template="/api/privacy/homes/{home_id}/export",
        source_surface="privacy",
        decision="allowed",
        event_context={"privacy_action": "export", "payload_recorded": False},
    )
    return exported


@router.post("/consent", response_model=ConsentRecord)
def record_consent(home_id: str, payload: ConsentRecordCreate, db: Session = Depends(get_db)):
    if payload.home_id != home_id:
        raise HTTPException(status_code=400, detail="Payload home_id must match path home_id")
    if repository.get_home_by_id(db, home_id) is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return privacy_service.record_consent(db, payload)


@router.delete("", response_model=PrivacyDeletionResult)
def delete_homeowner_record(home_id: str, db: Session = Depends(get_db), principal=Depends(current_principal)):
    if repository.get_home_by_id(db, home_id) is None:
        raise HTTPException(status_code=404, detail="Home not found")
    permissions.require_allowed(permissions.can_privacy_admin_home(db, principal, home_id))
    audit_service.record(
        db,
        action="privacy.delete",
        method="DELETE",
        path=f"/api/privacy/homes/{home_id}",
        status_code=200,
        authorized=True,
        reason="privacy delete authorized",
        principal=principal,
        home_id=home_id,
        object_type="home",
        object_id=home_id,
        route_template="/api/privacy/homes/{home_id}",
        source_surface="privacy",
        decision="allowed",
        event_context={"privacy_action": "delete", "payload_recorded": False},
    )
    return privacy_service.delete_homeowner_record(db, home_id)

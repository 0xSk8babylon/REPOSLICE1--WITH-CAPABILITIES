from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.router import current_principal
from app.core.database import get_db
from app.core.repository import repository
from app.security import permissions
from app.services.takeoff_generation import takeoff_generation_service
from app.takeoffs.schemas import TakeoffResponse

router = APIRouter(prefix="/takeoffs", tags=["takeoffs"])


@router.get("/current", response_model=TakeoffResponse)
def get_takeoff(db: Session = Depends(get_db), principal=Depends(current_principal)):
    result = repository.get_takeoff(db, design_ids=permissions.scoped_design_ids(db, principal))
    if result["request"] is None:
        raise HTTPException(status_code=404, detail="Takeoff not found")
    return result


@router.get("/generate/{design_id}", response_model=TakeoffResponse)
def generate_takeoff(design_id: str, db: Session = Depends(get_db), principal=Depends(current_principal)):
    design = repository.get_design(db, design_id)
    if design is None:
        raise HTTPException(status_code=404, detail="Design not found")
    permissions.require_allowed(permissions.can_access_design(db, principal, design_id))
    return takeoff_generation_service.generate(db, design_id)

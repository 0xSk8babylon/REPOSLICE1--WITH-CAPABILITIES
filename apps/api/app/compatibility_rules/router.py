from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.router import current_principal
from app.compatibility_rules.schemas import CompatibilityExplanation, CompatibilityIssue
from app.core.database import get_db
from app.core.repository import repository
from app.security import permissions
from app.services.compatibility import compatibility_service

router = APIRouter(prefix="/compatibility-rules", tags=["compatibility_rules"])


@router.get("/issues", response_model=List[CompatibilityIssue])
def list_issues(db: Session = Depends(get_db), principal=Depends(current_principal)):
    return repository.list_compatibility_issues_for_designs(db, permissions.scoped_design_ids(db, principal))


@router.get("/evaluate/{design_id}", response_model=List[CompatibilityExplanation])
def evaluate_design(design_id: str, db: Session = Depends(get_db), principal=Depends(current_principal)):
    design = repository.get_design(db, design_id)
    if design is None:
        raise HTTPException(status_code=404, detail="Design not found")
    permissions.require_allowed(permissions.can_access_design(db, principal, design_id))
    return compatibility_service.evaluate_design(db, design_id)

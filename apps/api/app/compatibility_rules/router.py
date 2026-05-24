from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.compatibility_rules.schemas import CompatibilityExplanation, CompatibilityIssue
from app.core.database import get_db
from app.core.repository import repository
from app.services.compatibility import compatibility_service

router = APIRouter(prefix="/compatibility-rules", tags=["compatibility_rules"])


@router.get("/issues", response_model=List[CompatibilityIssue])
def list_issues(db: Session = Depends(get_db)):
    return repository.list_compatibility_issues(db)


@router.get("/evaluate/{design_id}", response_model=List[CompatibilityExplanation])
def evaluate_design(design_id: str, db: Session = Depends(get_db)):
    return compatibility_service.evaluate_design(db, design_id)


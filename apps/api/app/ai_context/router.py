from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.router import current_principal
from app.core.database import get_db
from app.core.repository import repository
from app.security import permissions
from app.services.ai_context import ai_context_service

router = APIRouter(prefix="/ai-context", tags=["ai_context"])


@router.get("/design/{design_id}")
def design_context(design_id: str, db: Session = Depends(get_db), principal=Depends(current_principal)):
    design = repository.get_design(db, design_id)
    if design is None:
        raise HTTPException(status_code=404, detail="Design not found")
    permissions.require_allowed(permissions.can_access_design(db, principal, design_id))
    return ai_context_service.build_design_context(db, design_id)

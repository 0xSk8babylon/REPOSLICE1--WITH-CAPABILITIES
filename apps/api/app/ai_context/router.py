from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.ai_context import ai_context_service

router = APIRouter(prefix="/ai-context", tags=["ai_context"])


@router.get("/design/{design_id}")
def design_context(design_id: str, db: Session = Depends(get_db)):
    return ai_context_service.build_design_context(db, design_id)


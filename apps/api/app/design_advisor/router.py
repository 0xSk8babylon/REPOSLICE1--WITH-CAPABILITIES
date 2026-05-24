from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.design_advisor import design_advisor_service

router = APIRouter(prefix="/design-advisor", tags=["design_advisor"])


@router.get("/summary/{design_id}")
def advisor_summary(design_id: str, db: Session = Depends(get_db)):
    return design_advisor_service.explain(db, design_id)


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.estimate_readiness.schemas import EstimateReadinessView
from app.services.estimate_readiness import estimate_readiness_service

router = APIRouter(prefix="/estimate-readiness", tags=["estimate_readiness"])


@router.get("/homes/{home_id}", response_model=EstimateReadinessView)
def get_estimate_readiness(home_id: str, db: Session = Depends(get_db)):
    view = estimate_readiness_service.build_home_estimate_readiness(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.repository import repository
from app.nec_load_calculation.schemas import NecLoadCalculationResponse
from app.services.nec_load_calculation import nec_load_calculation_service

router = APIRouter(prefix="/homes/{home_id}/load-calculations", tags=["load_calculations"])


@router.get("/nec-220", response_model=NecLoadCalculationResponse)
def get_nec_220_load_calculation(home_id: str, db: Session = Depends(get_db)):
    if repository.get_home_by_id(db, home_id) is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return nec_load_calculation_service.calculate(db, home_id)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.energy_passport.schemas import EnergyPassportView
from app.services.energy_passport import energy_passport_service

router = APIRouter(prefix="/energy-passport", tags=["energy_passport"])


@router.get("/homes/{home_id}", response_model=EnergyPassportView)
def get_energy_passport(home_id: str, db: Session = Depends(get_db)):
    view = energy_passport_service.build_home_energy_passport(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view

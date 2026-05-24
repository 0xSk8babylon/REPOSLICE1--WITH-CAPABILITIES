from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.repository import repository
from app.equipment.schemas import EquipmentLocation, EquipmentLocationCreate, EquipmentLocationUpdate

router = APIRouter(prefix="/equipment", tags=["equipment"])


@router.get("/locations", response_model=List[EquipmentLocation])
def list_equipment_locations(db: Session = Depends(get_db)):
    return repository.list_equipment_locations(db)


@router.post("/locations", response_model=EquipmentLocation)
def create_equipment_location(payload: EquipmentLocationCreate, db: Session = Depends(get_db)):
    return repository.create_equipment_location(db, payload)


@router.patch("/locations/{location_id}", response_model=EquipmentLocation)
def update_equipment_location(location_id: str, payload: EquipmentLocationUpdate, db: Session = Depends(get_db)):
    if repository.get_equipment_location(db, location_id) is None:
        raise HTTPException(status_code=404, detail="Equipment location not found")
    return repository.update_equipment_location(db, location_id, payload)


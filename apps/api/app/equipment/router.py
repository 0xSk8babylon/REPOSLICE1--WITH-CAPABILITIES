from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.router import current_principal
from app.core.database import get_db
from app.core.repository import repository
from app.equipment.schemas import EquipmentLocation, EquipmentLocationCreate, EquipmentLocationUpdate
from app.security import permissions

router = APIRouter(prefix="/equipment", tags=["equipment"])


@router.get("/locations", response_model=List[EquipmentLocation])
def list_equipment_locations(db: Session = Depends(get_db), principal=Depends(current_principal)):
    return repository.list_equipment_locations_for_homes(db, permissions.scoped_home_ids(db, principal))


@router.post("/locations", response_model=EquipmentLocation)
def create_equipment_location(
    payload: EquipmentLocationCreate,
    db: Session = Depends(get_db),
    principal=Depends(current_principal),
):
    permissions.require_allowed(permissions.can_write_home(db, principal, payload.home_id))
    permissions.require_building_matches_home(db, payload.building_id, payload.home_id)
    return repository.create_equipment_location(db, payload)


@router.patch("/locations/{location_id}", response_model=EquipmentLocation)
def update_equipment_location(
    location_id: str,
    payload: EquipmentLocationUpdate,
    db: Session = Depends(get_db),
    principal=Depends(current_principal),
):
    location = repository.get_equipment_location(db, location_id)
    permissions.require_found_and_allowed(
        location is not None,
        location is not None and permissions.can_write_home(db, principal, location.home_id),
        "Equipment location not found",
    )
    if payload.building_id:
        permissions.require_building_matches_home(db, payload.building_id, location.home_id)
    return repository.update_equipment_location(db, location_id, payload)

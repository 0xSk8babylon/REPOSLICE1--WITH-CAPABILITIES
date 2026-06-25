from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.router import current_principal
from app.core.database import get_db
from app.core.repository import repository
from app.homes.schemas import BuildingStructure, BuildingStructureCreate, BuildingStructureUpdate
from app.security import permissions

router = APIRouter(prefix="/buildings", tags=["buildings"])


@router.get("", response_model=List[BuildingStructure])
def list_buildings(
    home_id: Optional[str] = None,
    db: Session = Depends(get_db),
    principal=Depends(current_principal),
):
    if home_id:
        permissions.require_allowed(permissions.can_access_home(db, principal, home_id))
        return repository.list_buildings(db, home_id=home_id)
    return repository.list_buildings_for_homes(db, permissions.scoped_home_ids(db, principal))


@router.post("", response_model=BuildingStructure)
def create_building(payload: BuildingStructureCreate, db: Session = Depends(get_db), principal=Depends(current_principal)):
    permissions.require_allowed(permissions.can_write_home(db, principal, payload.home_id))
    return repository.create_building(db, payload)


@router.patch("/{building_id}", response_model=BuildingStructure)
def update_building(
    building_id: str,
    payload: BuildingStructureUpdate,
    db: Session = Depends(get_db),
    principal=Depends(current_principal),
):
    building = repository.get_building(db, building_id)
    permissions.require_found_and_allowed(
        building is not None,
        building is not None and permissions.can_write_home(db, principal, building.home_id),
        "Building not found",
    )
    return repository.update_building(db, building_id, payload)

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.repository import repository
from app.homes.schemas import BuildingStructure, BuildingStructureCreate, BuildingStructureUpdate

router = APIRouter(prefix="/buildings", tags=["buildings"])


@router.get("", response_model=List[BuildingStructure])
def list_buildings(home_id: Optional[str] = Query(None), db: Session = Depends(get_db)):
    return repository.list_buildings(db, home_id=home_id)


@router.post("", response_model=BuildingStructure)
def create_building(payload: BuildingStructureCreate, db: Session = Depends(get_db)):
    return repository.create_building(db, payload)


@router.patch("/{building_id}", response_model=BuildingStructure)
def update_building(building_id: str, payload: BuildingStructureUpdate, db: Session = Depends(get_db)):
    if repository.get_building(db, building_id) is None:
        raise HTTPException(status_code=404, detail="Building not found")
    return repository.update_building(db, building_id, payload)


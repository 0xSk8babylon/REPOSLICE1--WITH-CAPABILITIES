from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.router import current_principal
from app.core.database import get_db
from app.core.repository import repository
from app.designs.schemas import (
    DesignEquipment,
    DesignEquipmentCreate,
    DesignEquipmentUpdate,
    EnergySystemDesign,
    EnergySystemDesignCreate,
    EnergySystemDesignUpdate,
)
from app.security import permissions

router = APIRouter(prefix="/designs", tags=["designs"])


@router.get("", response_model=List[EnergySystemDesign])
def list_designs(db: Session = Depends(get_db), principal=Depends(current_principal)):
    return repository.list_designs(db, home_ids=permissions.scoped_home_ids(db, principal))


@router.post("", response_model=EnergySystemDesign)
def create_design(payload: EnergySystemDesignCreate, db: Session = Depends(get_db), principal=Depends(current_principal)):
    permissions.require_allowed(permissions.can_write_home(db, principal, payload.home_id))
    return repository.create_design(db, payload)


@router.patch("/{design_id}", response_model=EnergySystemDesign)
def update_design(
    design_id: str,
    payload: EnergySystemDesignUpdate,
    db: Session = Depends(get_db),
    principal=Depends(current_principal),
):
    design = repository.get_design(db, design_id)
    permissions.require_found_and_allowed(
        design is not None,
        permissions.can_write_design(db, principal, design_id),
        "Design not found",
    )
    return repository.update_design(db, design_id, payload)


@router.get("/{design_id}/equipment", response_model=List[DesignEquipment])
def list_design_equipment(design_id: str, db: Session = Depends(get_db), principal=Depends(current_principal)):
    design = repository.get_design(db, design_id)
    permissions.require_found_and_allowed(
        design is not None,
        permissions.can_access_design(db, principal, design_id),
        "Design not found",
    )
    return repository.list_design_equipment(db, design_id)


@router.post("/{design_id}/equipment", response_model=DesignEquipment)
def create_design_equipment(
    design_id: str,
    payload: DesignEquipmentCreate,
    db: Session = Depends(get_db),
    principal=Depends(current_principal),
):
    design = repository.get_design(db, design_id)
    permissions.require_found_and_allowed(
        design is not None,
        permissions.can_write_design(db, principal, design_id),
        "Design not found",
    )
    if payload.design_id != design_id:
        raise HTTPException(status_code=400, detail="Payload design_id must match route design_id")
    if repository.get_product(db, payload.product_id) is None:
        raise HTTPException(status_code=404, detail="Equipment product not found")
    if payload.location_id:
        location = repository.get_equipment_location(db, payload.location_id)
        if location is None:
            raise HTTPException(status_code=404, detail="Equipment location not found")
        if location.home_id != design.home_id:
            raise HTTPException(status_code=400, detail="Equipment location must belong to the design home")
    return repository.create_design_equipment(db, payload)


@router.patch("/{design_id}/equipment/{equipment_id}", response_model=DesignEquipment)
def update_design_equipment(
    design_id: str,
    equipment_id: str,
    payload: DesignEquipmentUpdate,
    db: Session = Depends(get_db),
    principal=Depends(current_principal),
):
    design = repository.get_design(db, design_id)
    permissions.require_found_and_allowed(
        design is not None,
        permissions.can_write_design(db, principal, design_id),
        "Design not found",
    )
    equipment = repository.get_design_equipment(db, equipment_id)
    if equipment is None or equipment.design_id != design_id:
        raise HTTPException(status_code=404, detail="Design equipment not found")
    if payload.product_id and repository.get_product(db, payload.product_id) is None:
        raise HTTPException(status_code=404, detail="Equipment product not found")
    if payload.location_id:
        location = repository.get_equipment_location(db, payload.location_id)
        if location is None:
            raise HTTPException(status_code=404, detail="Equipment location not found")
        if location.home_id != design.home_id:
            raise HTTPException(status_code=400, detail="Equipment location must belong to the design home")
    return repository.update_design_equipment(db, equipment_id, payload)


@router.delete("/{design_id}/equipment/{equipment_id}", status_code=204)
def delete_design_equipment(
    design_id: str,
    equipment_id: str,
    db: Session = Depends(get_db),
    principal=Depends(current_principal),
):
    design = repository.get_design(db, design_id)
    permissions.require_found_and_allowed(
        design is not None,
        permissions.can_write_design(db, principal, design_id),
        "Design not found",
    )
    equipment = repository.get_design_equipment(db, equipment_id)
    if equipment is None or equipment.design_id != design_id:
        raise HTTPException(status_code=404, detail="Design equipment not found")
    repository.delete_design_equipment(db, equipment_id)

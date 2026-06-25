from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.router import current_principal
from app.core.database import get_db
from app.core.repository import repository
from app.loads.schemas import Load, LoadCreate, LoadUpdate
from app.security import permissions
from app.services.load_calculation import load_calculation_service
from app.services.provenance import provenance_service

router = APIRouter(prefix="/loads", tags=["loads"])


def _serialize_load(load, provenance_summaries=None) -> Load:
    provenance_summaries = provenance_summaries or {}
    return Load.model_validate(load).model_copy(update={"provenance_summary": provenance_summaries.get(load.id)})


@router.get("", response_model=List[Load])
def list_loads(db: Session = Depends(get_db), principal=Depends(current_principal)):
    loads = repository.list_loads_for_homes(db, permissions.scoped_home_ids(db, principal))
    summaries = provenance_service.summarize_entities(db, "load", [load.id for load in loads])
    return [_serialize_load(load, summaries) for load in loads]


@router.get("/summary")
def load_summary(db: Session = Depends(get_db), principal=Depends(current_principal)):
    return load_calculation_service.summarize(
        repository.list_loads_for_homes(db, permissions.scoped_home_ids(db, principal))
    )


@router.post("", response_model=Load)
def create_load(payload: LoadCreate, db: Session = Depends(get_db), principal=Depends(current_principal)):
    permissions.require_allowed(permissions.can_write_home(db, principal, payload.home_id))
    permissions.require_building_matches_home(db, payload.building_id, payload.home_id)
    load = repository.create_load(db, payload)
    summaries = provenance_service.summarize_entities(db, "load", [load.id])
    return _serialize_load(load, summaries)


@router.patch("/{load_id}", response_model=Load)
def update_load(load_id: str, payload: LoadUpdate, db: Session = Depends(get_db), principal=Depends(current_principal)):
    existing = repository.get_load(db, load_id)
    permissions.require_found_and_allowed(
        existing is not None,
        existing is not None and permissions.can_write_home(db, principal, existing.home_id),
        "Load not found",
    )
    if payload.building_id:
        permissions.require_building_matches_home(db, payload.building_id, existing.home_id)
    load = repository.update_load(db, load_id, payload)
    summaries = provenance_service.summarize_entities(db, "load", [load.id])
    return _serialize_load(load, summaries)

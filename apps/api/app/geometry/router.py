from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.repository import repository
from app.geometry.schemas import (
    GeometryObstruction,
    GeometryObstructionCreate,
    HomeGeometryExport,
    RoofPlane,
    RoofPlaneCreate,
)
from app.services.geometry import geometry_service

router = APIRouter(prefix="/homes/{home_id}/geometry", tags=["geometry"])


@router.get("/roof-planes", response_model=List[RoofPlane])
def list_roof_planes(home_id: str, db: Session = Depends(get_db)):
    if repository.get_home_by_id(db, home_id) is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return repository.list_roof_planes(db, home_id)


@router.post("/roof-planes", response_model=RoofPlane)
def create_roof_plane(home_id: str, payload: RoofPlaneCreate, db: Session = Depends(get_db)):
    if payload.home_id != home_id:
        raise HTTPException(status_code=400, detail="Payload home_id must match path home_id")
    if repository.get_home_by_id(db, home_id) is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return repository.create_roof_plane(db, payload)


@router.get("/obstructions", response_model=List[GeometryObstruction])
def list_obstructions(home_id: str, db: Session = Depends(get_db)):
    if repository.get_home_by_id(db, home_id) is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return repository.list_geometry_obstructions(db, home_id)


@router.post("/obstructions", response_model=GeometryObstruction)
def create_obstruction(home_id: str, payload: GeometryObstructionCreate, db: Session = Depends(get_db)):
    if payload.home_id != home_id:
        raise HTTPException(status_code=400, detail="Payload home_id must match path home_id")
    if repository.get_home_by_id(db, home_id) is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return repository.create_geometry_obstruction(db, payload)


@router.get("/export", response_model=HomeGeometryExport)
def export_geometry(home_id: str, db: Session = Depends(get_db)):
    if repository.get_home_by_id(db, home_id) is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return geometry_service.export_home_geometry(db, home_id)

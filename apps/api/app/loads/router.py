from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.repository import repository
from app.loads.schemas import Load, LoadCreate, LoadUpdate
from app.services.load_calculation import load_calculation_service

router = APIRouter(prefix="/loads", tags=["loads"])


@router.get("", response_model=List[Load])
def list_loads(db: Session = Depends(get_db)):
    return repository.list_loads(db)


@router.get("/summary")
def load_summary(db: Session = Depends(get_db)):
    return load_calculation_service.summarize(repository.list_loads(db))


@router.post("", response_model=Load)
def create_load(payload: LoadCreate, db: Session = Depends(get_db)):
    return repository.create_load(db, payload)


@router.patch("/{load_id}", response_model=Load)
def update_load(load_id: str, payload: LoadUpdate, db: Session = Depends(get_db)):
    if repository.get_load(db, load_id) is None:
        raise HTTPException(status_code=404, detail="Load not found")
    return repository.update_load(db, load_id, payload)


from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.repository import repository
from app.homes.schemas import Home, HomeCreate, HomeUpdate

router = APIRouter(prefix="/homes", tags=["homes"])


@router.get("", response_model=Home)
def get_home(db: Session = Depends(get_db)):
    home = repository.get_home(db)
    if home is None:
        raise HTTPException(status_code=404, detail="No home profile found")
    return home


@router.get("/all", response_model=List[Home])
def list_homes(db: Session = Depends(get_db)):
    return repository.list_homes(db)


@router.post("", response_model=Home)
def create_home(payload: HomeCreate, db: Session = Depends(get_db)):
    return repository.create_home(db, payload)


@router.patch("/{home_id}", response_model=Home)
def update_home(home_id: str, payload: HomeUpdate, db: Session = Depends(get_db)):
    if repository.get_home_by_id(db, home_id) is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return repository.update_home(db, home_id, payload)


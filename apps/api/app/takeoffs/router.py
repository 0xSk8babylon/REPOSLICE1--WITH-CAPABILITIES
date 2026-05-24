from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.repository import repository
from app.takeoffs.schemas import TakeoffResponse
from app.services.takeoff_generation import takeoff_generation_service

router = APIRouter(prefix="/takeoffs", tags=["takeoffs"])


@router.get("/current", response_model=TakeoffResponse)
def get_takeoff(db: Session = Depends(get_db)):
    return repository.get_takeoff(db)


@router.get("/generate/{design_id}", response_model=TakeoffResponse)
def generate_takeoff(design_id: str, db: Session = Depends(get_db)):
    return takeoff_generation_service.generate(db, design_id)


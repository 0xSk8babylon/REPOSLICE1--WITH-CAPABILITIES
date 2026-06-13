from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.repository import repository
from app.facts.schemas import EffectiveFact, Fact, FactCreate, FactGapsResponse, FactUpdate
from app.services.facts import fact_lifecycle_service

router = APIRouter(prefix="/homes/{home_id}/facts", tags=["facts"])


@router.get("", response_model=List[EffectiveFact])
def list_facts(home_id: str, db: Session = Depends(get_db)):
    if repository.get_home_by_id(db, home_id) is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return fact_lifecycle_service.effective_facts_for_home(db, home_id)


@router.post("", response_model=Fact)
def create_fact(home_id: str, payload: FactCreate, db: Session = Depends(get_db)):
    if repository.get_home_by_id(db, home_id) is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return fact_lifecycle_service.create_fact(db, home_id, payload)


@router.patch("/{fact_id}", response_model=Fact)
def update_fact(home_id: str, fact_id: str, payload: FactUpdate, db: Session = Depends(get_db)):
    fact = repository.get_fact(db, fact_id)
    if fact is None or fact.home_id != home_id:
        raise HTTPException(status_code=404, detail="Fact not found")
    return fact_lifecycle_service.update_fact(db, fact_id, payload)


@router.get("/gaps/{calculation_name}", response_model=FactGapsResponse)
def get_fact_gaps(home_id: str, calculation_name: str, db: Session = Depends(get_db)):
    if repository.get_home_by_id(db, home_id) is None:
        raise HTTPException(status_code=404, detail="Home not found")
    response = fact_lifecycle_service.fact_gaps(db, home_id, calculation_name)
    if response is None:
        raise HTTPException(status_code=404, detail="Calculation requirement set not found")
    return response

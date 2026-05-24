from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.repository import repository
from app.scenarios.schemas import Scenario, ScenarioCreate, ScenarioUpdate
from app.services.scenario_comparison import scenario_comparison_service

router = APIRouter(prefix="/scenarios", tags=["scenarios"])


@router.get("", response_model=List[Scenario])
def list_scenarios(db: Session = Depends(get_db)):
    return repository.list_scenarios(db)


@router.get("/compare", response_model=Dict[str, object])
def compare_scenarios(db: Session = Depends(get_db)):
    return scenario_comparison_service.compare(db, repository.list_scenarios(db))


@router.post("", response_model=Scenario)
def create_scenario(payload: ScenarioCreate, db: Session = Depends(get_db)):
    return repository.create_scenario(db, payload)


@router.patch("/{scenario_id}", response_model=Scenario)
def update_scenario(scenario_id: str, payload: ScenarioUpdate, db: Session = Depends(get_db)):
    if repository.get_scenario(db, scenario_id) is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return repository.update_scenario(db, scenario_id, payload)

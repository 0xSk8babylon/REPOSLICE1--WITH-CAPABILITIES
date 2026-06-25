from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.router import current_principal
from app.core.database import get_db
from app.core.repository import repository
from app.scenarios.schemas import Scenario, ScenarioCreate, ScenarioRevisionSummary, ScenarioUpdate
from app.security import permissions
from app.services.scenario_comparison import scenario_comparison_service
from app.services.scenario_revision import scenario_revision_service

router = APIRouter(prefix="/scenarios", tags=["scenarios"])


def _serialize_scenario(db: Session, scenario):
    if scenario is None:
        return None
    serialized = Scenario.model_validate(scenario).model_dump()
    serialized["revision_overview"] = scenario_revision_service.build_revision_overview(
        db, scenario.id
    ).model_dump()
    serialized["revisions"] = [
        revision.model_dump()
        for revision in scenario_revision_service.list_revision_summaries(db, scenario.id)
    ]
    return serialized


@router.get("", response_model=List[Scenario])
def list_scenarios(db: Session = Depends(get_db), principal=Depends(current_principal)):
    scenarios = repository.list_scenario_models(db, home_ids=permissions.scoped_home_ids(db, principal))
    return [_serialize_scenario(db, scenario) for scenario in scenarios]


@router.get("/compare", response_model=Dict[str, object])
def compare_scenarios(db: Session = Depends(get_db), principal=Depends(current_principal)):
    scenarios = repository.list_scenario_models(db, home_ids=permissions.scoped_home_ids(db, principal))
    return scenario_comparison_service.compare(db, scenarios)


@router.get("/{scenario_id}/revisions", response_model=List[ScenarioRevisionSummary])
def list_scenario_revisions(scenario_id: str, db: Session = Depends(get_db), principal=Depends(current_principal)):
    scenario = repository.get_scenario_model(db, scenario_id)
    permissions.require_found_and_allowed(
        scenario is not None,
        permissions.can_access_scenario(db, principal, scenario_id),
        "Scenario not found",
    )
    return scenario_revision_service.list_revision_summaries(db, scenario_id)


@router.post("", response_model=Scenario)
def create_scenario(payload: ScenarioCreate, db: Session = Depends(get_db), principal=Depends(current_principal)):
    permissions.require_allowed(permissions.can_write_home(db, principal, payload.home_id))
    design = repository.get_design(db, payload.linked_design_id)
    if design is None:
        raise HTTPException(status_code=404, detail="Linked design not found")
    if design.home_id != payload.home_id:
        raise HTTPException(status_code=400, detail="Linked design must belong to the scenario home")
    scenario = repository.create_scenario(db, payload)
    scenario_revision_service.capture_revision(db, scenario, reason="saved_revision")
    return _serialize_scenario(db, repository.get_scenario_model(db, scenario.id))


@router.patch("/{scenario_id}", response_model=Scenario)
def update_scenario(
    scenario_id: str,
    payload: ScenarioUpdate,
    db: Session = Depends(get_db),
    principal=Depends(current_principal),
):
    existing = repository.get_scenario_model(db, scenario_id)
    permissions.require_found_and_allowed(
        existing is not None,
        permissions.can_write_scenario(db, principal, scenario_id),
        "Scenario not found",
    )
    if payload.linked_design_id:
        design = repository.get_design(db, payload.linked_design_id)
        if design is None:
            raise HTTPException(status_code=404, detail="Linked design not found")
        if design.home_id != existing.home_id:
            raise HTTPException(status_code=400, detail="Linked design must belong to the scenario home")
    scenario = repository.update_scenario(db, scenario_id, payload)
    scenario_revision_service.capture_revision(db, scenario, reason="saved_revision")
    return _serialize_scenario(db, repository.get_scenario_model(db, scenario_id))

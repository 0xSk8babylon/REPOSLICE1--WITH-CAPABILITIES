from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.contractor_context.schemas import (
    ContractorConfirmationGateProjectionView,
    ContractorInstallComplexityView,
    ContractorPlanningContextView,
)
from app.core.database import get_db
from app.services.contractor_context import contractor_context_service

router = APIRouter(prefix="/contractor-context", tags=["contractor_context"])


@router.get("/homes/{home_id}", response_model=ContractorPlanningContextView)
def get_contractor_planning_context(home_id: str, db: Session = Depends(get_db)):
    view = contractor_context_service.build_contractor_planning_context(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view


@router.get("/homes/{home_id}/confirmation-gates", response_model=ContractorConfirmationGateProjectionView)
def get_contractor_confirmation_gates(home_id: str, db: Session = Depends(get_db)):
    view = contractor_context_service.build_confirmation_gate_projection(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view


@router.get("/homes/{home_id}/install-complexity", response_model=ContractorInstallComplexityView)
def get_contractor_install_complexity(home_id: str, db: Session = Depends(get_db)):
    view = contractor_context_service.build_install_complexity_view(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view

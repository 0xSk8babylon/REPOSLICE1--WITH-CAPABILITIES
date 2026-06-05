from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.contractor_workflow.schemas import ContractorWorkflowReadinessView
from app.core.database import get_db
from app.services.contractor_workflow import contractor_workflow_service

router = APIRouter(prefix="/contractor-workflow", tags=["contractor_workflow"])


@router.get("/homes/{home_id}/readiness", response_model=ContractorWorkflowReadinessView)
def get_contractor_workflow_readiness(home_id: str, db: Session = Depends(get_db)):
    view = contractor_workflow_service.build_home_contractor_workflow_readiness(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view

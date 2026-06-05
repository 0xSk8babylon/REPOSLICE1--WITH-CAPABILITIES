from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.proposal_option_sets.schemas import ProposalOptionSetsView
from app.services.proposal_option_sets import proposal_option_sets_service

router = APIRouter(prefix="/proposal-option-sets", tags=["proposal_option_sets"])


@router.get("/homes/{home_id}", response_model=ProposalOptionSetsView)
def get_proposal_option_sets(home_id: str, db: Session = Depends(get_db)):
    view = proposal_option_sets_service.build_home_proposal_option_sets(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view

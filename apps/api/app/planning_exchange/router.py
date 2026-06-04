from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.planning_exchange.schemas import PlanningExchangeObjectView
from app.services.planning_exchange import planning_exchange_service

router = APIRouter(prefix="/planning-exchange", tags=["planning_exchange"])


@router.get("/homes/{home_id}", response_model=PlanningExchangeObjectView)
def get_planning_exchange_object(home_id: str, db: Session = Depends(get_db)):
    view = planning_exchange_service.build_planning_exchange_object(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view

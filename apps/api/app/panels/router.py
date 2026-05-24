from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.repository import repository
from app.homes.schemas import ElectricalPanel, ElectricalPanelCreate, ElectricalPanelUpdate

router = APIRouter(prefix="/panels", tags=["panels"])


@router.get("", response_model=List[ElectricalPanel])
def list_panels(home_id: Optional[str] = Query(None), db: Session = Depends(get_db)):
    return repository.list_panels(db, home_id=home_id)


@router.post("", response_model=ElectricalPanel)
def create_panel(payload: ElectricalPanelCreate, db: Session = Depends(get_db)):
    return repository.create_panel(db, payload)


@router.patch("/{panel_id}", response_model=ElectricalPanel)
def update_panel(panel_id: str, payload: ElectricalPanelUpdate, db: Session = Depends(get_db)):
    if repository.get_panel(db, panel_id) is None:
        raise HTTPException(status_code=404, detail="Panel not found")
    return repository.update_panel(db, panel_id, payload)


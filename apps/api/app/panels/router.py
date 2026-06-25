from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.router import current_principal
from app.core.database import get_db
from app.core.repository import repository
from app.homes.schemas import ElectricalPanel, ElectricalPanelCreate, ElectricalPanelUpdate
from app.security import permissions

router = APIRouter(prefix="/panels", tags=["panels"])


@router.get("", response_model=List[ElectricalPanel])
def list_panels(
    home_id: Optional[str] = None,
    db: Session = Depends(get_db),
    principal=Depends(current_principal),
):
    if home_id:
        permissions.require_allowed(permissions.can_access_home(db, principal, home_id))
        return repository.list_panels(db, home_id=home_id)
    return repository.list_panels_for_homes(db, permissions.scoped_home_ids(db, principal))


@router.post("", response_model=ElectricalPanel)
def create_panel(payload: ElectricalPanelCreate, db: Session = Depends(get_db), principal=Depends(current_principal)):
    permissions.require_allowed(permissions.can_write_home(db, principal, payload.home_id))
    permissions.require_building_matches_home(db, payload.building_id, payload.home_id)
    return repository.create_panel(db, payload)


@router.patch("/{panel_id}", response_model=ElectricalPanel)
def update_panel(
    panel_id: str,
    payload: ElectricalPanelUpdate,
    db: Session = Depends(get_db),
    principal=Depends(current_principal),
):
    panel = repository.get_panel(db, panel_id)
    permissions.require_found_and_allowed(
        panel is not None,
        panel is not None and permissions.can_write_home(db, principal, panel.home_id),
        "Panel not found",
    )
    if payload.building_id:
        permissions.require_building_matches_home(db, payload.building_id, panel.home_id)
    return repository.update_panel(db, panel_id, payload)

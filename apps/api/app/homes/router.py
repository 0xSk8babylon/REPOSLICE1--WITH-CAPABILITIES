from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.router import current_principal
from app.core.database import get_db
from app.core.repository import repository
from app.homes.schemas import Home, HomeCreate, HomeUpdate
from app.security import permissions

router = APIRouter(prefix="/homes", tags=["homes"])


@router.get("", response_model=Home)
def get_home(db: Session = Depends(get_db), principal=Depends(current_principal)):
    if principal.auth_source == permissions.LOCAL_TEST_HEADER_SOURCE:
        homes = permissions.filter_home_records(principal, repository.list_homes(db))
        home = homes[0] if homes else None
    else:
        home = repository.get_home(db, account_ids=permissions.allowed_account_ids(principal))
    if home is None:
        raise HTTPException(status_code=404, detail="No home profile found")
    return home


@router.get("/all", response_model=List[Home])
def list_homes(db: Session = Depends(get_db), principal=Depends(current_principal)):
    if principal.auth_source == permissions.LOCAL_TEST_HEADER_SOURCE:
        return permissions.filter_home_records(principal, repository.list_homes(db))
    return repository.list_homes(db, account_ids=permissions.allowed_account_ids(principal))


@router.post("", response_model=Home)
def create_home(payload: HomeCreate, db: Session = Depends(get_db), principal=Depends(current_principal)):
    permissions.require_allowed(permissions.can_write_account(principal, payload.account_id))
    return repository.create_home(db, payload)


@router.patch("/{home_id}", response_model=Home)
def update_home(home_id: str, payload: HomeUpdate, db: Session = Depends(get_db), principal=Depends(current_principal)):
    home = repository.get_home_by_id(db, home_id)
    permissions.require_found_and_allowed(
        home is not None,
        permissions.can_write_home_record(principal, home),
        "Home not found",
    )
    if payload.account_id and payload.account_id != home.account_id:
        permissions.require_allowed(permissions.can_write_account(principal, payload.account_id))
    return repository.update_home(db, home_id, payload)

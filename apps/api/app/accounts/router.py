from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.accounts.schemas import Account, AccountCreate, AccountUpdate
from app.core.database import get_db
from app.core.repository import repository

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("", response_model=List[Account])
def list_accounts(db: Session = Depends(get_db)):
    return repository.list_accounts(db)


@router.post("", response_model=Account)
def create_account(payload: AccountCreate, db: Session = Depends(get_db)):
    return repository.create_account(db, payload)


@router.patch("/{account_id}", response_model=Account)
def update_account(account_id: str, payload: AccountUpdate, db: Session = Depends(get_db)):
    if repository.get_account(db, account_id) is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return repository.update_account(db, account_id, payload)


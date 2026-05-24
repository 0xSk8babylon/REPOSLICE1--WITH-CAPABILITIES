from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.repository import repository
from app.provenance.schemas import RuleProvenance

router = APIRouter(prefix="/rule-provenance", tags=["rule_provenance"])


@router.get("", response_model=List[RuleProvenance])
def list_rule_provenance(rule_key: Optional[str] = None, db: Session = Depends(get_db)):
    return repository.list_rule_provenance(db, rule_key=rule_key)

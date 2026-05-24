from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.repository import repository
from app.provenance.schemas import DataProvenance

router = APIRouter(prefix="/provenance", tags=["provenance"])


@router.get("", response_model=List[DataProvenance])
def list_provenance(
    entity_type: Optional[str] = None,
    entity_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return repository.list_data_provenance(db, entity_type=entity_type, entity_id=entity_id)

from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.repository import repository
from app.provenance.schemas import SourceDocument

router = APIRouter(prefix="/source-documents", tags=["source_documents"])


@router.get("", response_model=List[SourceDocument])
def list_source_documents(
    manufacturer: Optional[str] = None,
    product_model: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return repository.list_source_documents(db, manufacturer=manufacturer, product_model=product_model)

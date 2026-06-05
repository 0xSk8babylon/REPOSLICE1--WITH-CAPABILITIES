from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.product_preferences.schemas import ProductPreferencesView
from app.services.product_preferences import product_preferences_service

router = APIRouter(prefix="/product-preferences", tags=["product_preferences"])


@router.get("/homes/{home_id}", response_model=ProductPreferencesView)
def get_product_preferences(home_id: str, db: Session = Depends(get_db)):
    view = product_preferences_service.build_home_product_preferences(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view

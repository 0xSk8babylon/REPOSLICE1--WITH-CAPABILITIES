from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.post_install.schemas import PostInstallView
from app.services.post_install import post_install_service

router = APIRouter(prefix="/post-install", tags=["post_install"])


@router.get("/homes/{home_id}", response_model=PostInstallView)
def get_post_install_view(home_id: str, db: Session = Depends(get_db)):
    view = post_install_service.build_home_post_install_view(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view

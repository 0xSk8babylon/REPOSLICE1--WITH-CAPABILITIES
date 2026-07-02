from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.repository import repository
from app.equipment.schemas import EquipmentProduct, EquipmentProductCreate, EquipmentProductUpdate
from app.services.provenance import provenance_service

router = APIRouter(prefix="/product-library", tags=["product_library"])


@router.get("", response_model=List[EquipmentProduct])
def list_products(db: Session = Depends(get_db)):
    return [
        EquipmentProduct(
            **EquipmentProduct.model_validate(product).model_dump(
                exclude={"provenance_summary", "source_documents"}
            ),
            provenance_summary=provenance_service.summarize_entity(db, "equipment_product", product.id),
            source_documents=provenance_service.get_source_documents_for_entity(db, "equipment_product", product.id),
        )
        for product in repository.list_products(db)
    ]


@router.post("", response_model=EquipmentProduct)
def create_product(payload: EquipmentProductCreate, db: Session = Depends(get_db)):
    return repository.create_product(db, payload)


@router.patch("/{product_id}", response_model=EquipmentProduct)
def update_product(product_id: str, payload: EquipmentProductUpdate, db: Session = Depends(get_db)):
    if repository.get_product(db, product_id) is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return repository.update_product(db, product_id, payload)

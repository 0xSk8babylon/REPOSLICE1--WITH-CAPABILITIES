from typing import Any, Dict, List, Optional

from pydantic import Field

from app.core.schemas import ORMModel
from app.core.types import DataOrigin, Ecosystem, LocationType, ProductType
from app.provenance.schemas import ProvenanceSummary, SourceDocument


class EquipmentProductBase(ORMModel):
    manufacturer: str
    model: str
    product_type: ProductType
    ecosystem: Ecosystem
    specs: Dict[str, Any]
    documentation_url: Optional[str] = None
    notes: Optional[str] = None
    data_origin: DataOrigin = DataOrigin.user_created


class EquipmentProduct(EquipmentProductBase):
    id: str
    provenance_summary: Optional[ProvenanceSummary] = None
    source_documents: List[SourceDocument] = Field(default_factory=list)


class EquipmentProductCreate(EquipmentProduct):
    pass


class EquipmentProductUpdate(ORMModel):
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    product_type: Optional[ProductType] = None
    ecosystem: Optional[Ecosystem] = None
    specs: Optional[Dict[str, Any]] = None
    documentation_url: Optional[str] = None
    notes: Optional[str] = None


class EquipmentLocationBase(ORMModel):
    home_id: str
    building_id: str
    name: str
    location_type: LocationType
    approximate_coordinates: Optional[str] = None
    notes: Optional[str] = None
    data_origin: DataOrigin = DataOrigin.user_created


class EquipmentLocation(EquipmentLocationBase):
    id: str


class EquipmentLocationCreate(EquipmentLocation):
    pass


class EquipmentLocationUpdate(ORMModel):
    building_id: Optional[str] = None
    name: Optional[str] = None
    location_type: Optional[LocationType] = None
    approximate_coordinates: Optional[str] = None
    notes: Optional[str] = None

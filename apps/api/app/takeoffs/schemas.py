from typing import List, Optional

from pydantic import Field

from app.core.schemas import ORMModel
from app.core.types import DataOrigin


class TakeoffRequest(ORMModel):
    id: str
    design_id: str
    status: str
    requested_by: str
    notes: Optional[str] = None
    data_origin: DataOrigin = DataOrigin.user_created
    trust_notes: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    provenance_summary: Optional[dict] = None


class TakeoffLineItem(ORMModel):
    id: str
    takeoff_request_id: str
    category: str
    item_name: str
    quantity: float
    unit: str
    unit_cost_placeholder: Optional[float] = None
    total_cost_placeholder: Optional[float] = None
    assumptions: Optional[str] = None
    notes: Optional[str] = None
    data_origin: DataOrigin = DataOrigin.user_created
    derivation_basis: Optional[str] = None
    trust_notes: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    provenance_summary: Optional[dict] = None


class TakeoffResponse(ORMModel):
    request: TakeoffRequest
    line_items: List[TakeoffLineItem]

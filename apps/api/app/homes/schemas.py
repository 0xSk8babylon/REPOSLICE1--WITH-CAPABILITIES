from typing import List, Optional

from pydantic import Field

from app.core.schemas import ORMModel
from app.core.types import DataOrigin, IndoorOutdoor, PanelType, StructureType


class BuildingStructureBase(ORMModel):
    home_id: str
    name: str
    type: StructureType
    approximate_distance_from_main_service: Optional[float] = None
    notes: Optional[str] = None
    data_origin: DataOrigin = DataOrigin.user_created


class BuildingStructure(BuildingStructureBase):
    id: str


class BuildingStructureCreate(BuildingStructure):
    pass


class BuildingStructureUpdate(ORMModel):
    name: Optional[str] = None
    type: Optional[StructureType] = None
    approximate_distance_from_main_service: Optional[float] = None
    notes: Optional[str] = None


class ElectricalPanelBase(ORMModel):
    home_id: str
    building_id: str
    panel_type: PanelType
    amperage: int
    busbar_rating: Optional[int] = None
    breaker_spaces_total: int
    breaker_spaces_available: int
    indoor_outdoor: IndoorOutdoor
    notes: Optional[str] = None
    data_origin: DataOrigin = DataOrigin.user_created


class ElectricalPanel(ElectricalPanelBase):
    id: str


class ElectricalPanelCreate(ElectricalPanel):
    pass


class ElectricalPanelUpdate(ORMModel):
    building_id: Optional[str] = None
    panel_type: Optional[PanelType] = None
    amperage: Optional[int] = None
    busbar_rating: Optional[int] = None
    breaker_spaces_total: Optional[int] = None
    breaker_spaces_available: Optional[int] = None
    indoor_outdoor: Optional[IndoorOutdoor] = None
    notes: Optional[str] = None


class HomeBase(ORMModel):
    account_id: Optional[str] = None
    name: str
    address_line_1: str
    address_line_2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country: str = "US"
    utility_provider: Optional[str] = None
    service_size: Optional[int] = None
    notes: Optional[str] = None
    data_origin: DataOrigin = DataOrigin.user_created


class Home(HomeBase):
    id: str
    buildings: List[BuildingStructure] = Field(default_factory=list)
    panels: List[ElectricalPanel] = Field(default_factory=list)


class HomeCreate(HomeBase):
    id: str


class HomeUpdate(ORMModel):
    account_id: Optional[str] = None
    name: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    utility_provider: Optional[str] = None
    service_size: Optional[int] = None
    notes: Optional[str] = None

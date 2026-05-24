from typing import List, Optional

from pydantic import Field

from app.core.schemas import ORMModel
from app.core.types import ArchitectureType, DataOrigin, DesignGoal


class DesignEquipmentBase(ORMModel):
    product_id: str
    quantity: float
    location_id: Optional[str] = None
    role_in_system: str
    notes: Optional[str] = None
    data_origin: DataOrigin = DataOrigin.user_created


class DesignEquipment(DesignEquipmentBase):
    id: str
    design_id: str


class DesignEquipmentCreate(DesignEquipment):
    pass


class DesignEquipmentUpdate(ORMModel):
    product_id: Optional[str] = None
    quantity: Optional[float] = None
    location_id: Optional[str] = None
    role_in_system: Optional[str] = None
    notes: Optional[str] = None


class EnergySystemDesignBase(ORMModel):
    home_id: str
    name: str
    design_goal: DesignGoal
    architecture_type: ArchitectureType
    status: str
    notes: Optional[str] = None
    data_origin: DataOrigin = DataOrigin.user_created


class EnergySystemDesign(EnergySystemDesignBase):
    id: str
    equipment: List[DesignEquipment] = Field(default_factory=list)


class EnergySystemDesignCreate(EnergySystemDesign):
    pass


class EnergySystemDesignUpdate(ORMModel):
    name: Optional[str] = None
    design_goal: Optional[DesignGoal] = None
    architecture_type: Optional[ArchitectureType] = None
    status: Optional[str] = None
    notes: Optional[str] = None

from typing import Optional

from app.core.schemas import ORMModel
from app.core.types import DataOrigin


class ScenarioBase(ORMModel):
    home_id: str
    name: str
    description: str
    linked_design_id: str
    upfront_cost_placeholder: Optional[float] = None
    future_expansion_score: Optional[float] = None
    install_complexity_score: Optional[float] = None
    backup_capability_score: Optional[float] = None
    notes: Optional[str] = None
    data_origin: DataOrigin = DataOrigin.user_created


class Scenario(ScenarioBase):
    id: str


class ScenarioCreate(Scenario):
    pass


class ScenarioUpdate(ORMModel):
    name: Optional[str] = None
    description: Optional[str] = None
    linked_design_id: Optional[str] = None
    upfront_cost_placeholder: Optional[float] = None
    future_expansion_score: Optional[float] = None
    install_complexity_score: Optional[float] = None
    backup_capability_score: Optional[float] = None
    notes: Optional[str] = None

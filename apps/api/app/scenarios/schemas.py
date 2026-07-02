from datetime import datetime
from typing import List, Optional

from pydantic import Field

from app.core.schemas import ORMModel
from app.core.types import DataOrigin


class ScenarioRevisionSummary(ORMModel):
    id: str
    scenario_id: str
    parent_revision_id: Optional[str] = None
    revision_number: int
    revision_label: str
    revision_status: str
    linked_design_id: str
    design_goal_snapshot: Optional[str] = None
    design_status_snapshot: Optional[str] = None
    recommended_profile_snapshot: Optional[str] = None
    planning_summary: str
    planning_state_snapshot: dict
    created_at: datetime
    updated_at: datetime
    data_origin: DataOrigin = DataOrigin.derived_estimate


class ScenarioRevisionOverview(ORMModel):
    latest_revision_id: Optional[str] = None
    latest_revision_label: Optional[str] = None
    latest_revision_status: Optional[str] = None
    latest_revision_number: int = 0
    revision_count: int = 0
    note: str


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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    revision_overview: Optional[ScenarioRevisionOverview] = None
    revisions: List[ScenarioRevisionSummary] = Field(default_factory=list)


class ScenarioCreate(ScenarioBase):
    id: str


class ScenarioUpdate(ORMModel):
    name: Optional[str] = None
    description: Optional[str] = None
    linked_design_id: Optional[str] = None
    upfront_cost_placeholder: Optional[float] = None
    future_expansion_score: Optional[float] = None
    install_complexity_score: Optional[float] = None
    backup_capability_score: Optional[float] = None
    notes: Optional[str] = None

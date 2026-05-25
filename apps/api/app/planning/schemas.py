from datetime import datetime
from typing import Optional

from app.core.schemas import ORMModel
from app.core.types import ArchitectureType, BackupPriority, DataOrigin, DesignGoal, PhaseType
from app.provenance.schemas import ProvenanceSummary


class EstimatedPathwayBase(ORMModel):
    home_id: str
    design_id: Optional[str] = None
    name: str
    description: str
    lifecycle_stage: str
    source_location: Optional[str] = None
    destination_location: Optional[str] = None
    estimated_distance_ft: Optional[float] = None
    route_type: Optional[str] = None
    route_difficulty: Optional[str] = None
    visibility_level: Optional[str] = None
    confidence_level: Optional[str] = None
    upfront_cost_placeholder: Optional[float] = None
    estimated_monthly_savings_placeholder: Optional[float] = None
    resilience_score: Optional[float] = None
    notes: Optional[str] = None
    data_origin: DataOrigin = DataOrigin.user_created


class EstimatedPathway(EstimatedPathwayBase):
    id: str
    created_at: datetime
    updated_at: datetime
    provenance_summary: Optional[ProvenanceSummary] = None


class EstimatedPathwayCreate(EstimatedPathwayBase):
    id: str


class EstimatedPathwayUpdate(ORMModel):
    design_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    lifecycle_stage: Optional[str] = None
    source_location: Optional[str] = None
    destination_location: Optional[str] = None
    estimated_distance_ft: Optional[float] = None
    route_type: Optional[str] = None
    route_difficulty: Optional[str] = None
    visibility_level: Optional[str] = None
    confidence_level: Optional[str] = None
    upfront_cost_placeholder: Optional[float] = None
    estimated_monthly_savings_placeholder: Optional[float] = None
    resilience_score: Optional[float] = None
    notes: Optional[str] = None


class LoadTemplateBase(ORMModel):
    account_id: Optional[str] = None
    name: str
    category: str
    running_watts: float
    surge_watts: Optional[float] = None
    estimated_daily_hours: Optional[float] = None
    backup_priority: BackupPriority
    phase_type: PhaseType
    notes: Optional[str] = None
    data_origin: DataOrigin = DataOrigin.user_created


class LoadTemplate(LoadTemplateBase):
    id: str
    created_at: datetime
    updated_at: datetime


class LoadTemplateCreate(LoadTemplateBase):
    id: str


class LoadTemplateUpdate(ORMModel):
    account_id: Optional[str] = None
    name: Optional[str] = None
    category: Optional[str] = None
    running_watts: Optional[float] = None
    surge_watts: Optional[float] = None
    estimated_daily_hours: Optional[float] = None
    backup_priority: Optional[BackupPriority] = None
    phase_type: Optional[PhaseType] = None
    notes: Optional[str] = None


class DesignGoalPresetBase(ORMModel):
    name: str
    design_goal: DesignGoal
    architecture_type: ArchitectureType
    summary: str
    notes: Optional[str] = None
    data_origin: DataOrigin = DataOrigin.user_created


class DesignGoalPreset(DesignGoalPresetBase):
    id: str
    created_at: datetime
    updated_at: datetime


class DesignGoalPresetCreate(DesignGoalPresetBase):
    id: str


class DesignGoalPresetUpdate(ORMModel):
    name: Optional[str] = None
    design_goal: Optional[DesignGoal] = None
    architecture_type: Optional[ArchitectureType] = None
    summary: Optional[str] = None
    notes: Optional[str] = None

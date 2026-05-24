from typing import Optional

from app.core.schemas import ORMModel
from app.core.types import BackupPriority, DataOrigin, PhaseType


class LoadBase(ORMModel):
    home_id: str
    building_id: str
    name: str
    category: str
    running_watts: float
    surge_watts: Optional[float] = None
    estimated_daily_hours: Optional[float] = None
    backup_priority: BackupPriority
    phase_type: PhaseType
    notes: Optional[str] = None
    data_origin: DataOrigin = DataOrigin.user_created


class Load(LoadBase):
    id: str


class LoadCreate(Load):
    pass


class LoadUpdate(ORMModel):
    building_id: Optional[str] = None
    name: Optional[str] = None
    category: Optional[str] = None
    running_watts: Optional[float] = None
    surge_watts: Optional[float] = None
    estimated_daily_hours: Optional[float] = None
    backup_priority: Optional[BackupPriority] = None
    phase_type: Optional[PhaseType] = None
    notes: Optional[str] = None

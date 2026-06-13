from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import Field

from app.core.schemas import ORMModel


class ConsentRecordCreate(ORMModel):
    id: str
    home_id: str
    user_id: str
    consent_type: str
    status: str
    notes: Optional[str] = None


class ConsentRecord(ConsentRecordCreate):
    created_at: datetime
    updated_at: datetime


class PrivacyExport(ORMModel):
    home_id: str
    exported_sections: Dict[str, Any]
    portable_format: str = "residential_energy_planner_privacy_export_v1"
    limitations: List[str] = Field(default_factory=list)


class PrivacyDeletionResult(ORMModel):
    home_id: str
    deleted: bool
    deleted_sections: List[str]
    retained_sections: List[str]
    limitations: List[str] = Field(default_factory=list)

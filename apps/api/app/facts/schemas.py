from datetime import datetime
from typing import Any, List, Optional

from pydantic import Field

from app.core.schemas import ORMModel
from app.core.types import FactConfidenceTier, FactDecayPolicy, FactSource


class FactBase(ORMModel):
    key: str
    value: Any
    unit: Optional[str] = None
    source: FactSource
    confidence_tier: FactConfidenceTier
    expires_at: Optional[datetime] = None
    decay_policy: Optional[FactDecayPolicy] = None
    derived_from: List[str] = Field(default_factory=list)
    notes: Optional[str] = None


class FactCreate(FactBase):
    id: str


class FactUpdate(ORMModel):
    value: Optional[Any] = None
    unit: Optional[str] = None
    source: Optional[FactSource] = None
    confidence_tier: Optional[FactConfidenceTier] = None
    expires_at: Optional[datetime] = None
    decay_policy: Optional[FactDecayPolicy] = None
    derived_from: Optional[List[str]] = None
    notes: Optional[str] = None


class Fact(FactBase):
    id: str
    home_id: str
    verified_at: datetime
    created_at: datetime
    updated_at: datetime


class EffectiveFact(Fact):
    effective_confidence_score: float
    effective_confidence_tier: FactConfidenceTier
    effective_confidence_reason: str
    decay_policy_applied: FactDecayPolicy


class FactGap(ORMModel):
    key: str
    required: bool
    defaultable: bool
    status: str
    reason: str


class FactGapsResponse(ORMModel):
    home_id: str
    calculation_name: str
    required_keys: List[str]
    defaultable_keys: List[str]
    present_keys: List[str]
    gaps: List[FactGap]
    ready: bool
    limitations: List[str] = Field(default_factory=list)

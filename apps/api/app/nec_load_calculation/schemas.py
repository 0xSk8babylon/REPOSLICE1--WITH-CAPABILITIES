from typing import Any, List, Optional

from pydantic import Field

from app.core.schemas import ORMModel
from app.core.types import FactConfidenceTier
from app.facts.schemas import FactGap


class ConsumedFact(ORMModel):
    key: str
    value: Any
    unit: Optional[str] = None
    source: str
    confidence_tier: FactConfidenceTier
    effective_confidence_score: float
    effective_confidence_tier: FactConfidenceTier
    derived_from: List[str] = Field(default_factory=list)


class CalculationAssumption(ORMModel):
    key: str
    value: Any
    unit: Optional[str] = None
    reason: str
    confidence_tier: FactConfidenceTier = FactConfidenceTier.assumed


class NecLoadStage(ORMModel):
    stage: str
    va: float
    formula: str
    basis_keys: List[str] = Field(default_factory=list)


class NecLoadMethodResult(ORMModel):
    method: str
    calculation_ready: bool
    calculated_service_load_va: Optional[float] = None
    calculated_service_load_amps: Optional[float] = None
    existing_service_amps: Optional[float] = None
    headroom_amps: Optional[float] = None
    stages: List[NecLoadStage] = Field(default_factory=list)
    consumed_facts: List[ConsumedFact] = Field(default_factory=list)
    assumptions: List[CalculationAssumption] = Field(default_factory=list)
    gaps: List[FactGap] = Field(default_factory=list)
    output_confidence_tier: FactConfidenceTier = FactConfidenceTier.missing
    limitations: List[str] = Field(default_factory=list)


class NecLoadCalculationResponse(ORMModel):
    home_id: str
    voltage: float
    results: List[NecLoadMethodResult]
    source_basis: List[str] = Field(default_factory=list)
    compliance_boundary: str
    missing_data: List[str] = Field(default_factory=list)

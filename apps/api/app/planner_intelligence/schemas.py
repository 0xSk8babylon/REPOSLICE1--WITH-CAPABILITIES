from typing import Any, Dict, List, Optional

from pydantic import Field

from app.compatibility_rules.schemas import CompatibilityExplanation
from app.core.schemas import ORMModel, ViewBoundaryMetadata
from app.core.types import AuthorityLayer, ConfidenceLevel, DataClassification
from app.design_advisor.schemas import PlanningStateSnapshot, ResilienceRecommendation
from app.provenance.schemas import ProvenanceSummary


class ProvenanceRef(ORMModel):
    """Compact reference to a source object touched while composing a block."""

    entity_type: str
    entity_id: str
    role: Optional[str] = None


class TrustEnvelope(ORMModel):
    """Uniform, non-authoritative trust labeling carried by every block."""

    authority_layer: AuthorityLayer = AuthorityLayer.advisory
    trust_zone: str = "advisory_explanation"
    data_classification: DataClassification = DataClassification.planning_private
    confidence_level: Optional[ConfidenceLevel] = None
    provisional: bool = False
    missing_inputs: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    scope_limitations: List[str] = Field(default_factory=list)
    provenance_refs: List[ProvenanceRef] = Field(default_factory=list)


class RecommendationsBlock(ORMModel):
    recommendation: Optional[ResilienceRecommendation] = None
    trust_envelope: TrustEnvelope


class ConstraintsBlock(ORMModel):
    items: List[CompatibilityExplanation] = Field(default_factory=list)
    trust_envelope: TrustEnvelope


class ReadinessExplanationBlock(ORMModel):
    completeness: Dict[str, Any] = Field(default_factory=dict)
    trust_envelope: TrustEnvelope


class UpgradePathReadinessContext(ORMModel):
    """Home-scoped readiness/constraint context that enriches the upgrade path.

    These views feed confidence and missing-inputs only; they do not originate
    the upgrade ladder, which comes from the planning_state snapshot.
    """

    home_id: str
    planning_intelligence_readiness_available: bool = False
    constraint_risk_available: bool = False
    dependency_impact_available: bool = False
    dependency_reasoning_available: bool = False
    expansion_score: Optional[float] = None
    expansion_basis: Optional[str] = None
    readiness_missing_inputs: List[str] = Field(default_factory=list)


class UpgradePathExplanationBlock(ORMModel):
    planning_state: Optional[PlanningStateSnapshot] = None
    readiness_context: UpgradePathReadinessContext
    trust_envelope: TrustEnvelope


class ScenarioComparisonBlock(ORMModel):
    comparison: Dict[str, Any] = Field(default_factory=dict)
    trust_envelope: TrustEnvelope


class ProvenanceSummaryBlock(ORMModel):
    contributing: List[ProvenanceSummary] = Field(default_factory=list)
    source_object_refs: List[ProvenanceRef] = Field(default_factory=list)
    rule_keys: List[str] = Field(default_factory=list)
    source_document_ids: List[str] = Field(default_factory=list)
    missing_inputs: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    confidence_level: Optional[ConfidenceLevel] = None
    trust_envelope: TrustEnvelope


class PlannerIntelligenceBlocks(ORMModel):
    recommendations: RecommendationsBlock
    constraints: ConstraintsBlock
    readiness_explanation: ReadinessExplanationBlock
    upgrade_path_explanation: UpgradePathExplanationBlock
    scenario_comparison_explanation: Optional[ScenarioComparisonBlock] = None
    provenance_summary: ProvenanceSummaryBlock


class PlannerIntelligenceDesignSummary(ORMModel):
    view_boundary: ViewBoundaryMetadata
    design_id: str
    home_id: Optional[str] = None
    blocks: PlannerIntelligenceBlocks
    limitations: List[str] = Field(default_factory=list)

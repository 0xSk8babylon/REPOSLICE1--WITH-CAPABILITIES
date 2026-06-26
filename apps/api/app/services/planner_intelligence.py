"""Planner-intelligence read facade.

Composes existing, verified public reasoning outputs into one authorized,
provenance-backed read payload. It introduces no new reasoning math, no LLM, and
no external calls. It does not call private builders; the upgrade ladder is
consumed directly from ``design_advisor_service.explain()["planning_state"]``.
"""

from typing import Any, Dict, List, Optional

from app.core.repository import repository
from app.core.schemas import ViewBoundaryMetadata
from app.core.types import (
    ApiViewAudience,
    AuthorityLayer,
    ConfidenceLevel,
    DataClassification,
)
from app.planner_intelligence.schemas import (
    ConstraintsBlock,
    PlannerIntelligenceBlocks,
    PlannerIntelligenceDesignSummary,
    ProvenanceRef,
    ProvenanceSummaryBlock,
    ReadinessExplanationBlock,
    RecommendationsBlock,
    ScenarioComparisonBlock,
    TrustEnvelope,
    UpgradePathExplanationBlock,
    UpgradePathReadinessContext,
)
from app.services.design_advisor import design_advisor_service
from app.services.provenance import provenance_service
from app.services.scenario_comparison import scenario_comparison_service
from app.services.twin_planning_context import twin_planning_context_service


PLANNER_INTELLIGENCE_LIMITATIONS = [
    "Advisory planning intelligence. Not engineering, permitting, utility, or pricing authority.",
    "Composed from existing deterministic rule and derived outputs; no new reasoning, no LLM, no external lookup.",
    "Recommendations and explanations are non-authoritative and source-linked; verify on site before action.",
]


def _dedupe(values: List[str]) -> List[str]:
    seen: Dict[str, None] = {}
    for value in values:
        if value and value not in seen:
            seen[value] = None
    return list(seen.keys())


class PlannerIntelligenceService:
    def build_design_summary(self, db, design, home_id: Optional[str]) -> PlannerIntelligenceDesignSummary:
        design_id = design.id

        # Single approved composition method; consume its public return only.
        advisor = design_advisor_service.explain(db, design_id)
        recommendation = advisor.get("recommendation_profiles")
        compatibility_items = list(advisor.get("compatibility") or [])
        completeness: Dict[str, Any] = advisor.get("completeness") or {}
        planning_state = advisor.get("planning_state")
        expansion: Dict[str, Any] = advisor.get("expansion") or {}

        source_object_refs: List[ProvenanceRef] = [
            ProvenanceRef(entity_type="design", entity_id=design_id, role="subject"),
        ]
        if home_id:
            source_object_refs.append(
                ProvenanceRef(entity_type="home", entity_id=home_id, role="parent_home")
            )

        contributing = [provenance_service.summarize_entity(db, "design", design_id)]
        if home_id:
            contributing.append(provenance_service.summarize_entity(db, "home", home_id))

        recommendations_block = self._build_recommendations_block(recommendation, design_id)
        constraints_block = self._build_constraints_block(db, compatibility_items, source_object_refs)
        readiness_block = self._build_readiness_block(completeness, design_id)
        upgrade_block = self._build_upgrade_path_block(
            db, recommendation, planning_state, expansion, home_id, source_object_refs
        )
        scenario_block = self._build_scenario_comparison_block(db, home_id, source_object_refs)

        provenance_block = self._build_provenance_summary_block(
            contributing=contributing,
            source_object_refs=source_object_refs,
            recommendation=recommendation,
            completeness=completeness,
        )

        blocks = PlannerIntelligenceBlocks(
            recommendations=recommendations_block,
            constraints=constraints_block,
            readiness_explanation=readiness_block,
            upgrade_path_explanation=upgrade_block,
            scenario_comparison_explanation=scenario_block,
            provenance_summary=provenance_block,
        )

        return PlannerIntelligenceDesignSummary(
            view_boundary=ViewBoundaryMetadata(
                view_name="planner_intelligence_design_summary",
                audience=ApiViewAudience.consumer,
                authority_layer=AuthorityLayer.advisory,
                trust_zone="advisory_explanation",
                data_classification=DataClassification.planning_private,
                exposed_authority_layers=[
                    AuthorityLayer.canonical,
                    AuthorityLayer.derived,
                    AuthorityLayer.advisory,
                ],
            ),
            design_id=design_id,
            home_id=home_id,
            blocks=blocks,
            limitations=list(PLANNER_INTELLIGENCE_LIMITATIONS),
        )

    def _build_recommendations_block(self, recommendation, design_id: str) -> RecommendationsBlock:
        confidence = getattr(recommendation, "confidence_level", None)
        envelope = TrustEnvelope(
            authority_layer=AuthorityLayer.derived,
            trust_zone="derived_planning_intelligence",
            confidence_level=confidence,
            provisional=recommendation is None or confidence == ConfidenceLevel.low,
            assumptions=["Deterministic recommendation profiles derived from recorded design state."],
            scope_limitations=["Planning guidance only; not engineering approval or permit guidance."],
            provenance_refs=[ProvenanceRef(entity_type="design", entity_id=design_id, role="recommendation_basis")],
        )
        return RecommendationsBlock(recommendation=recommendation, trust_envelope=envelope)

    def _build_constraints_block(
        self, db, compatibility_items, source_object_refs: List[ProvenanceRef]
    ) -> ConstraintsBlock:
        equipment_refs: List[ProvenanceRef] = []
        for item in compatibility_items:
            for equipment_id in getattr(item, "related_equipment_ids", []) or []:
                ref = ProvenanceRef(
                    entity_type="equipment_product", entity_id=equipment_id, role="constraint_subject"
                )
                equipment_refs.append(ref)
                source_object_refs.append(ref)
        envelope = TrustEnvelope(
            authority_layer=AuthorityLayer.derived,
            trust_zone="derived_planning_intelligence",
            assumptions=["Rule-based compatibility evaluation over recorded equipment and topology."],
            scope_limitations=["Identifies planning constraints; does not certify compliance or safety."],
            provenance_refs=equipment_refs,
        )
        return ConstraintsBlock(items=list(compatibility_items), trust_envelope=envelope)

    def _build_readiness_block(self, completeness: Dict[str, Any], design_id: str) -> ReadinessExplanationBlock:
        missing = list(completeness.get("missing_categories") or [])
        envelope = TrustEnvelope(
            authority_layer=AuthorityLayer.derived,
            trust_zone="derived_planning_intelligence",
            provisional=bool(missing),
            missing_inputs=missing,
            assumptions=["Planning completeness only; not engineering completeness."],
            scope_limitations=[completeness.get("scope_note")] if completeness.get("scope_note") else [],
            provenance_refs=[ProvenanceRef(entity_type="design", entity_id=design_id, role="readiness_subject")],
        )
        return ReadinessExplanationBlock(completeness=completeness, trust_envelope=envelope)

    def _build_upgrade_path_block(
        self,
        db,
        recommendation,
        planning_state,
        expansion: Dict[str, Any],
        home_id: Optional[str],
        source_object_refs: List[ProvenanceRef],
    ) -> UpgradePathExplanationBlock:
        # Enrichment only: home-scoped readiness/dependency views feed confidence
        # and missing-inputs; they do not originate the ladder.
        readiness_view = None
        constraint_view = None
        dependency_impact_view = None
        dependency_reasoning_view = None
        if home_id:
            readiness_view = twin_planning_context_service.build_planning_intelligence_readiness_view(db, home_id)
            constraint_view = twin_planning_context_service.build_constraint_risk_reasoning_view(db, home_id)
            dependency_impact_view = twin_planning_context_service.build_dependency_impact_readiness_view(db, home_id)
            dependency_reasoning_view = twin_planning_context_service.build_dependency_reasoning_view(db, home_id)

        readiness_missing: List[str] = []
        if readiness_view is not None:
            readiness_missing.extend(list(getattr(readiness_view, "missing_prerequisites", []) or []))

        readiness_context = UpgradePathReadinessContext(
            home_id=home_id or "",
            planning_intelligence_readiness_available=readiness_view is not None,
            constraint_risk_available=constraint_view is not None,
            dependency_impact_available=dependency_impact_view is not None,
            dependency_reasoning_available=dependency_reasoning_view is not None,
            expansion_score=expansion.get("future_expansion_score"),
            expansion_basis=expansion.get("basis"),
            readiness_missing_inputs=_dedupe(readiness_missing),
        )

        # Ladder source: the planning_state snapshot's variants (canonical object).
        variant_refs: List[ProvenanceRef] = []
        variant_confidences: List[Any] = []
        if planning_state is not None:
            for variant in getattr(planning_state, "variants", []) or []:
                variant_refs.append(
                    ProvenanceRef(
                        entity_type="planning_state_variant",
                        entity_id=getattr(variant, "variant_key", "unknown"),
                        role=getattr(variant, "state_role", None),
                    )
                )
                variant_confidences.append(getattr(variant, "confidence_level", None))
        source_object_refs.extend(variant_refs)

        current_arch_missing = (
            recommendation is None or getattr(recommendation, "current_home_energy_architecture", None) is None
        )
        low_confidence = ConfidenceLevel.low in variant_confidences or (
            recommendation is not None and getattr(recommendation, "confidence_level", None) == ConfidenceLevel.low
        )
        provisional = current_arch_missing or low_confidence or planning_state is None

        assumptions = [
            "Upgrade ladder consumed directly from the design advisor planning_state snapshot variants.",
        ]
        scope_limitations = [
            "Home-scoped readiness/dependency views enrich the path; they do not originate it.",
        ]
        if current_arch_missing:
            scope_limitations.append(
                "Current-home energy architecture is not modeled; upgrade path is provisional."
            )

        envelope = TrustEnvelope(
            authority_layer=AuthorityLayer.advisory,
            trust_zone="advisory_explanation",
            confidence_level=getattr(recommendation, "confidence_level", None),
            provisional=provisional,
            missing_inputs=readiness_context.readiness_missing_inputs,
            assumptions=assumptions,
            scope_limitations=scope_limitations,
            provenance_refs=variant_refs,
        )
        return UpgradePathExplanationBlock(
            planning_state=planning_state,
            readiness_context=readiness_context,
            trust_envelope=envelope,
        )

    def _build_scenario_comparison_block(
        self, db, home_id: Optional[str], source_object_refs: List[ProvenanceRef]
    ) -> Optional[ScenarioComparisonBlock]:
        if not home_id:
            return None
        scenarios = repository.list_scenario_models(db, home_ids={home_id})
        if not scenarios:
            return None

        comparison = scenario_comparison_service.compare(db, scenarios)
        scenario_refs = [
            ProvenanceRef(entity_type="scenario", entity_id=scenario.id, role="comparison_member")
            for scenario in scenarios
        ]
        source_object_refs.extend(scenario_refs)
        envelope = TrustEnvelope(
            authority_layer=AuthorityLayer.derived,
            trust_zone="derived_planning_intelligence",
            assumptions=["Deterministic ranking across home-scoped planning scenarios."],
            scope_limitations=["Comparison reflects recorded scenario placeholders and derived scores only."],
            provenance_refs=scenario_refs,
        )
        return ScenarioComparisonBlock(comparison=comparison, trust_envelope=envelope)

    def _build_provenance_summary_block(
        self,
        *,
        contributing,
        source_object_refs: List[ProvenanceRef],
        recommendation,
        completeness: Dict[str, Any],
    ) -> ProvenanceSummaryBlock:
        source_document_ids: List[str] = []
        missing_inputs: List[str] = list(completeness.get("missing_categories") or [])
        for summary in contributing:
            source_document_ids.extend(getattr(summary, "source_document_ids", []) or [])
            missing_inputs.extend(getattr(summary, "unverified_fields", []) or [])

        rule_keys: List[str] = []
        recommendation_provenance = getattr(recommendation, "provenance_summary", None)
        if isinstance(recommendation_provenance, dict):
            rule_keys.extend(recommendation_provenance.get("rule_keys", []) or [])

        confidence = getattr(recommendation, "confidence_level", None)
        envelope = TrustEnvelope(
            authority_layer=AuthorityLayer.derived,
            trust_zone="derived_planning_intelligence",
            confidence_level=confidence,
            missing_inputs=_dedupe(missing_inputs),
            assumptions=["Aggregated lineage across the objects composed for this summary."],
            scope_limitations=["Field-level provenance is not exhaustive; absence of lineage is not verification."],
            provenance_refs=list(source_object_refs),
        )
        return ProvenanceSummaryBlock(
            contributing=list(contributing),
            source_object_refs=list(source_object_refs),
            rule_keys=_dedupe(rule_keys),
            source_document_ids=_dedupe(source_document_ids),
            missing_inputs=_dedupe(missing_inputs),
            confidence_level=confidence,
            trust_envelope=envelope,
        )


planner_intelligence_service = PlannerIntelligenceService()

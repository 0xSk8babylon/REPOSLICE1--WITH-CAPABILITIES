"""Pure planning graph comparator and smart-panel scoring primitives."""

from dataclasses import dataclass
from typing import Dict, Sequence, Tuple


@dataclass(frozen=True)
class GraphNode:
    id: str
    node_type: str
    confidence: str


@dataclass(frozen=True)
class GraphEdge:
    source_id: str
    target_id: str
    edge_type: str
    confidence: str


@dataclass(frozen=True)
class CandidateConfiguration:
    id: str
    name: str
    nodes: Tuple[GraphNode, ...]
    edges: Tuple[GraphEdge, ...]
    annual_bill_delta: float
    backup_coverage_hours: float
    headroom_kw: float
    complexity_score: float
    compliance_blockers: int
    confidence: str


@dataclass(frozen=True)
class CandidateScore:
    candidate_id: str
    economics_score: float
    backup_score: float
    headroom_score: float
    complexity_score: float
    compliance_score: float
    total_score: float
    tradeoffs: Tuple[str, ...]
    confidence: str


@dataclass(frozen=True)
class SmartPanelScore:
    panel_name: str
    load_management_value_score: float
    backfeed_constraint_value_score: float
    total_score: float
    reasons: Tuple[str, ...]
    confidence: str


def compare_configurations(candidates: Sequence[CandidateConfiguration]) -> Tuple[CandidateScore, ...]:
    """Score supplied candidate configurations without ranking a winner."""
    if not candidates:
        return tuple()
    max_bill_delta = max(candidate.annual_bill_delta for candidate in candidates) or 1
    max_backup = max(candidate.backup_coverage_hours for candidate in candidates) or 1
    scores = []
    for candidate in candidates:
        economics = _clamp(candidate.annual_bill_delta / max_bill_delta * 100)
        backup = _clamp(candidate.backup_coverage_hours / max_backup * 100)
        headroom = _clamp(50 + candidate.headroom_kw * 5)
        complexity = _clamp(100 - candidate.complexity_score * 10)
        compliance = _clamp(100 - candidate.compliance_blockers * 30)
        total = round((economics * 0.25) + (backup * 0.3) + (headroom * 0.2) + (complexity * 0.15) + (compliance * 0.1), 2)
        scores.append(
            CandidateScore(
                candidate_id=candidate.id,
                economics_score=round(economics, 2),
                backup_score=round(backup, 2),
                headroom_score=round(headroom, 2),
                complexity_score=round(complexity, 2),
                compliance_score=round(compliance, 2),
                total_score=total,
                tradeoffs=_tradeoffs(candidate),
                confidence=candidate.confidence,
            )
        )
    return tuple(scores)


def score_smart_panel(
    panel_name: str,
    controllable_load_kw: float,
    critical_load_kw: float,
    backfeed_headroom_amps: float,
    confidence: str,
) -> SmartPanelScore:
    """Evaluate planning value of smart load management for a home."""
    load_value = _clamp((controllable_load_kw / critical_load_kw * 100) if critical_load_kw else 0)
    backfeed_value = _clamp(100 - max(backfeed_headroom_amps, 0) * 2)
    total = round(load_value * 0.65 + backfeed_value * 0.35, 2)
    reasons = [
        "Smart-panel load management can reduce critical-load sizing pressure.",
        "Limited backfeed headroom increases the planning value of load management.",
    ]
    if backfeed_headroom_amps >= 40:
        reasons.append("Backfeed headroom appears less constrained from supplied inputs.")
    return SmartPanelScore(
        panel_name=panel_name,
        load_management_value_score=round(load_value, 2),
        backfeed_constraint_value_score=round(backfeed_value, 2),
        total_score=total,
        reasons=tuple(reasons),
        confidence=confidence,
    )


def graph_confidence(nodes: Sequence[GraphNode], edges: Sequence[GraphEdge]) -> Dict[str, int]:
    counts: Dict[str, int] = {"known": 0, "derived": 0, "assumed": 0, "missing": 0}
    for item in list(nodes) + list(edges):
        counts[item.confidence if item.confidence in counts else "missing"] += 1
    return counts


def _tradeoffs(candidate: CandidateConfiguration) -> Tuple[str, ...]:
    tradeoffs = []
    if candidate.compliance_blockers:
        tradeoffs.append("Compliance blockers require professional review before design selection.")
    if candidate.complexity_score >= 7:
        tradeoffs.append("Install complexity is high relative to the supplied candidate set.")
    if candidate.headroom_kw < 0:
        tradeoffs.append("Headroom is negative and requires utility or service-capacity review.")
    if not tradeoffs:
        tradeoffs.append("No dominant blocker surfaced from supplied planning inputs.")
    return tuple(tradeoffs)


def _clamp(value: float) -> float:
    return min(max(value, 0.0), 100.0)

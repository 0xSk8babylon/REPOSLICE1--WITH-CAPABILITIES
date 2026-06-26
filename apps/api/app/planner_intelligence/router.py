import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.router import current_principal
from app.core.database import get_db
from app.core.repository import repository
from app.planner_intelligence.schemas import PlannerIntelligenceDesignSummary
from app.security import permissions
from app.security.audit import audit_service
from app.services.planner_intelligence import planner_intelligence_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/planner-intelligence", tags=["planner_intelligence"])

_ROUTE_TEMPLATE = "/api/planner-intelligence/designs/{design_id}/summary"


def _safe_record_audit(
    *,
    principal,
    design_id: str,
    home_id: Optional[str],
    decision: str,
    status_code: int,
    authorized: bool,
    reason: str,
    provenance_refs=None,
    event_context=None,
) -> None:
    """Audit a planner-intelligence read on its own session.

    Degrading by design: a failed audit write is logged but must never break an
    otherwise valid read. Uses a separate session so an audit failure cannot
    poison the request session.
    """

    try:
        audit_service.record_with_new_session(
            action="planner_intelligence.read",
            method="GET",
            path=f"/api/planner-intelligence/designs/{design_id}/summary",
            status_code=status_code,
            authorized=authorized,
            reason=reason,
            principal=principal,
            home_id=home_id,
            object_type="design",
            object_id=design_id,
            route_template=_ROUTE_TEMPLATE,
            source_surface="planner_intelligence",
            decision=decision,
            provenance_refs=provenance_refs,
            event_context=event_context,
        )
    except Exception:  # pragma: no cover - defensive degradation path
        logger.warning(
            "planner_intelligence audit write failed for design_id=%s", design_id, exc_info=True
        )


@router.get("/designs/{design_id}/summary", response_model=PlannerIntelligenceDesignSummary)
def get_design_planner_intelligence_summary(
    design_id: str,
    db: Session = Depends(get_db),
    principal=Depends(current_principal),
):
    # Unauthenticated 401 is raised by current_principal before this handler and
    # is audited by the existing auth middleware, not here.
    design = repository.get_design(db, design_id)
    if design is None:
        _safe_record_audit(
            principal=principal,
            design_id=design_id,
            home_id=None,
            decision="denied",
            status_code=404,
            authorized=False,
            reason="design_not_found",
            event_context={"design_id": design_id, "outcome": "not_found"},
        )
        raise HTTPException(status_code=404, detail="Design not found")

    home_id = design.home_id

    # Explicit design-scoped authorization at the facade boundary; do not rely
    # only on HomeAccessMiddleware.
    if not permissions.can_access_design(db, principal, design_id):
        _safe_record_audit(
            principal=principal,
            design_id=design_id,
            home_id=home_id,
            decision="denied",
            status_code=403,
            authorized=False,
            reason="design_access_denied",
            event_context={"design_id": design_id, "home_id": home_id, "outcome": "denied"},
        )
        raise HTTPException(status_code=403, detail="Permission denied")

    summary = planner_intelligence_service.build_design_summary(db, design, home_id)

    provenance_refs = [
        {"entity_type": "design", "entity_id": design_id},
        {"entity_type": "home", "entity_id": home_id},
    ]
    provenance_refs.extend(
        ref.model_dump() for ref in summary.blocks.provenance_summary.source_object_refs
    )
    event_context = {
        "design_id": design_id,
        "home_id": home_id,
        "constraint_count": len(summary.blocks.constraints.items),
        "recommendation_present": summary.blocks.recommendations.recommendation is not None,
        "scenario_comparison_present": summary.blocks.scenario_comparison_explanation is not None,
        "provenance_source_count": len(provenance_refs),
        "outcome": "allowed",
    }
    _safe_record_audit(
        principal=principal,
        design_id=design_id,
        home_id=home_id,
        decision="allowed",
        status_code=200,
        authorized=True,
        reason="planner_intelligence_read",
        provenance_refs=provenance_refs,
        event_context=event_context,
    )
    return summary

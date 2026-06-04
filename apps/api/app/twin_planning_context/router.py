from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.twin_planning_context import twin_planning_context_service
from app.twin_planning_context.schemas import (
    AIDesignGroundingView,
    TwinAdvisoryContextAssemblyView,
    TwinBasicAdvisoryRecommendationsView,
    TwinContractorFacingAdvisoryView,
    TwinConstraintRiskReasoningView,
    TwinDependencyImpactReadinessView,
    TwinDependencyReasoningView,
    TwinEnergyGoalReasoningView,
    TwinHomeownerFacingAdvisoryView,
    TwinPlanningIntelligenceReadinessView,
    TwinPlanningContext,
    TwinPreRecommendationAdvisoryView,
    TwinProposalReadinessFoundationView,
    TwinProductSpecReadinessView,
    TwinRecommendationEligibilityReadinessView,
    TwinRuntimeParticipantRole,
    TwinRuntimeProjectionView,
    TwinScenarioComparisonReadinessView,
    TwinTopologySnapshot,
    TwinTrustProvenanceReadinessIndexView,
)

router = APIRouter(prefix="/twin-planning-context", tags=["twin_planning_context"])


@router.get("/homes/{home_id}", response_model=TwinPlanningContext)
def get_twin_planning_context(home_id: str, db: Session = Depends(get_db)):
    context = twin_planning_context_service.build(db, home_id)
    if context is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return context


@router.get("/homes/{home_id}/views/ai-design-grounding", response_model=AIDesignGroundingView)
def get_ai_design_grounding_view(
    home_id: str,
    design_id: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    view = twin_planning_context_service.build_ai_design_grounding_view(db, home_id, design_id=design_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home or design not found")
    return view


@router.get("/homes/{home_id}/views/topology-snapshot", response_model=TwinTopologySnapshot)
def get_topology_snapshot_view(home_id: str, db: Session = Depends(get_db)):
    view = twin_planning_context_service.build_topology_snapshot_view(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view


@router.get(
    "/homes/{home_id}/views/dependency-impact-readiness",
    response_model=TwinDependencyImpactReadinessView,
)
def get_dependency_impact_readiness_view(home_id: str, db: Session = Depends(get_db)):
    view = twin_planning_context_service.build_dependency_impact_readiness_view(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view


@router.get(
    "/homes/{home_id}/views/dependency-reasoning",
    response_model=TwinDependencyReasoningView,
)
def get_dependency_reasoning_view(home_id: str, db: Session = Depends(get_db)):
    view = twin_planning_context_service.build_dependency_reasoning_view(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view


@router.get(
    "/homes/{home_id}/views/planning-intelligence-readiness",
    response_model=TwinPlanningIntelligenceReadinessView,
)
def get_planning_intelligence_readiness_view(home_id: str, db: Session = Depends(get_db)):
    view = twin_planning_context_service.build_planning_intelligence_readiness_view(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view


@router.get(
    "/homes/{home_id}/views/advisory-context-assembly",
    response_model=TwinAdvisoryContextAssemblyView,
)
def get_advisory_context_assembly_view(home_id: str, db: Session = Depends(get_db)):
    view = twin_planning_context_service.build_advisory_context_assembly_view(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view


@router.get(
    "/homes/{home_id}/views/constraint-risk-reasoning",
    response_model=TwinConstraintRiskReasoningView,
)
def get_constraint_risk_reasoning_view(home_id: str, db: Session = Depends(get_db)):
    view = twin_planning_context_service.build_constraint_risk_reasoning_view(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view


@router.get(
    "/homes/{home_id}/views/scenario-comparison-readiness",
    response_model=TwinScenarioComparisonReadinessView,
)
def get_scenario_comparison_readiness_view(home_id: str, db: Session = Depends(get_db)):
    view = twin_planning_context_service.build_scenario_comparison_readiness_view(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view


@router.get(
    "/homes/{home_id}/views/pre-recommendation-advisory",
    response_model=TwinPreRecommendationAdvisoryView,
)
def get_pre_recommendation_advisory_view(home_id: str, db: Session = Depends(get_db)):
    view = twin_planning_context_service.build_pre_recommendation_advisory_view(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view


@router.get(
    "/homes/{home_id}/views/recommendation-eligibility-readiness",
    response_model=TwinRecommendationEligibilityReadinessView,
)
def get_recommendation_eligibility_readiness_view(home_id: str, db: Session = Depends(get_db)):
    view = twin_planning_context_service.build_recommendation_eligibility_readiness_view(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view


@router.get(
    "/homes/{home_id}/views/basic-advisory-recommendations",
    response_model=TwinBasicAdvisoryRecommendationsView,
)
def get_basic_advisory_recommendations_view(home_id: str, db: Session = Depends(get_db)):
    view = twin_planning_context_service.build_basic_advisory_recommendations_view(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view


@router.get(
    "/homes/{home_id}/views/contractor-facing-advisory",
    response_model=TwinContractorFacingAdvisoryView,
)
def get_contractor_facing_advisory_view(home_id: str, db: Session = Depends(get_db)):
    view = twin_planning_context_service.build_contractor_facing_advisory_view(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view


@router.get(
    "/homes/{home_id}/views/homeowner-facing-advisory",
    response_model=TwinHomeownerFacingAdvisoryView,
)
def get_homeowner_facing_advisory_view(home_id: str, db: Session = Depends(get_db)):
    view = twin_planning_context_service.build_homeowner_facing_advisory_view(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view


@router.get(
    "/homes/{home_id}/views/energy-goal-reasoning",
    response_model=TwinEnergyGoalReasoningView,
)
def get_energy_goal_reasoning_view(home_id: str, db: Session = Depends(get_db)):
    view = twin_planning_context_service.build_energy_goal_reasoning_view(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view


@router.get(
    "/homes/{home_id}/views/proposal-readiness-foundation",
    response_model=TwinProposalReadinessFoundationView,
)
def get_proposal_readiness_foundation_view(home_id: str, db: Session = Depends(get_db)):
    view = twin_planning_context_service.build_proposal_readiness_foundation_view(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view


@router.get(
    "/homes/{home_id}/views/product-spec-readiness",
    response_model=TwinProductSpecReadinessView,
)
def get_product_spec_readiness_view(home_id: str, db: Session = Depends(get_db)):
    view = twin_planning_context_service.build_product_spec_readiness_view(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view


@router.get(
    "/homes/{home_id}/views/trust-provenance-readiness-index",
    response_model=TwinTrustProvenanceReadinessIndexView,
)
def get_trust_provenance_readiness_index_view(home_id: str, db: Session = Depends(get_db)):
    view = twin_planning_context_service.build_trust_provenance_readiness_index_view(db, home_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return view


@router.get("/homes/{home_id}/views/runtime-projection/{role}", response_model=TwinRuntimeProjectionView)
def get_runtime_projection_view(
    home_id: str,
    role: TwinRuntimeParticipantRole,
    db: Session = Depends(get_db),
):
    view = twin_planning_context_service.build_runtime_projection_view(db, home_id, role=role)
    if view is None:
        raise HTTPException(status_code=404, detail="Home or runtime projection role not found")
    return view

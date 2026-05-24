from app.core.types import DataOrigin
from app.services.design_analysis import design_analysis_service


class ExpansionReadinessService:
    def score(self, db, design_id: str):
        analysis = design_analysis_service.build(db, design_id)
        if analysis is None:
            return {
                "design_id": design_id,
                "future_expansion_score": 0,
                "status": "missing_design",
                "basis": "No design found for expansion planning evaluation.",
                "data_origin": DataOrigin.derived_estimate,
            }

        score = 0.2
        if analysis["main_panel"] and (analysis["main_panel"].breaker_spaces_available or 0) > 1:
            score += 0.25
        if analysis["linked_pathways"]:
            score += 0.2
        if analysis["product_types"].intersection({"smart_panel", "load_center", "hybrid_inverter"}):
            score += 0.15
        if analysis["design"].design_goal in {"expansion_ready", "workshop_ready"}:
            score += 0.1
        if analysis["workshop_buildings"]:
            score += 0.05 if analysis["linked_pathways"] else -0.1

        score = max(0.0, min(0.95, round(score, 2)))
        return {
            "design_id": design_id,
            "future_expansion_score": score,
            "status": "derived_estimate",
            "basis": "Planning heuristic based on spare panel capacity, pathways, and modular equipment signals. It does not confirm future code, service, or site suitability.",
            "data_origin": DataOrigin.derived_estimate,
        }


expansion_readiness_service = ExpansionReadinessService()

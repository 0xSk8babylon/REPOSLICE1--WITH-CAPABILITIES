from app.core.types import DataOrigin
from app.services.design_analysis import design_analysis_service


class InstallComplexityService:
    def score(self, db, design_id: str):
        analysis = design_analysis_service.build(db, design_id)
        if analysis is None:
            return {
                "design_id": design_id,
                "install_complexity_score": 0,
                "status": "missing_design",
                "basis": "No design found for installation-planning evaluation.",
                "data_origin": DataOrigin.derived_estimate,
            }

        score = 0.15
        if analysis["detached_buildings"]:
            score += 0.2
        if any((pathway.route_type == "trench_route") for pathway in analysis["linked_pathways"]):
            score += 0.2
        if any((pathway.visibility_level == "high") for pathway in analysis["linked_pathways"]):
            score += 0.1
        if len(analysis["ecosystems"]) > 1:
            score += 0.1
        if analysis["missing_location_assignments"]:
            score += 0.05

        score = max(0.0, min(0.95, round(score, 2)))
        return {
            "design_id": design_id,
            "install_complexity_score": score,
            "status": DataOrigin.derived_estimate.value,
            "basis": "Planning heuristic based on detached structures, trenching assumptions, ecosystem mixing, and routing visibility. It is not a field-validated install assessment.",
            "data_origin": DataOrigin.derived_estimate,
        }


install_complexity_service = InstallComplexityService()

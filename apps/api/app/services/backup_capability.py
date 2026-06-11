from app.core.types import DataOrigin
from app.services.design_analysis import design_analysis_service


class BackupCapabilityService:
    def estimate(self, db, design_id: str):
        analysis = design_analysis_service.build(db, design_id)
        if analysis is None:
            return {
                "design_id": design_id,
                "backup_capability_score": 0,
                "status": "missing_design",
                "basis": "No design found for backup planning evaluation.",
                "data_origin": DataOrigin.derived_estimate,
            }

        score = 0.15
        if analysis["essential_loads"] or analysis["backup_loads"]:
            score += 0.25
        if analysis["product_types"].intersection({"battery", "generator", "hybrid_inverter"}):
            score += 0.25
        if analysis["product_types"].intersection({"gateway", "transfer_switch", "critical_load_panel", "smart_panel"}):
            score += 0.2
        if analysis["linked_pathways"]:
            score += 0.05
        if analysis["design"].design_goal == "whole_home_backup" and not analysis["product_types"].intersection({"battery", "generator"}):
            score -= 0.15

        score = max(0.0, min(0.95, round(score, 2)))
        return {
            "design_id": design_id,
            "backup_capability_score": score,
            "status": DataOrigin.derived_estimate.value,
            "basis": "Planning heuristic based on backup load tagging, assigned backup architecture, and transfer/control strategy. It does not model runtime, surge sequencing, or engineering constraints.",
            "data_origin": DataOrigin.derived_estimate,
        }


backup_capability_service = BackupCapabilityService()

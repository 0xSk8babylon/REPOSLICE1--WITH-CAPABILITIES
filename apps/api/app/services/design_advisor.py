from app.services.backup_capability import backup_capability_service
from app.services.compatibility import compatibility_service
from app.services.design_analysis import design_analysis_service
from app.services.design_completeness import design_completeness_service
from app.services.expansion_readiness import expansion_readiness_service
from app.services.install_complexity import install_complexity_service
from app.services.resilience_recommendation import resilience_recommendation_service


class DesignAdvisorService:
    def explain(self, db, design_id: str):
        analysis = design_analysis_service.build(db, design_id)
        completeness = design_completeness_service.evaluate(db, design_id)
        return {
            "design_id": design_id,
            "compatibility": compatibility_service.evaluate_design(db, design_id),
            "backup": backup_capability_service.estimate(db, design_id),
            "expansion": expansion_readiness_service.score(db, design_id),
            "install_complexity": install_complexity_service.score(db, design_id),
            "recommendation_profiles": resilience_recommendation_service.recommend(db, design_id),
            "completeness": completeness,
            "design_status": {
                "stored_status": analysis["design"].status if analysis else None,
                "effective_status": analysis["effective_status"] if analysis else None,
                "explanation": analysis["status_explanation"] if analysis else "No design selected.",
            },
            "trust_posture": {
                "transient_takeoffs_only": True,
                "placeholder_and_derived_outputs_must_stay_visible": True,
                "site_verification_required": True,
            },
            "advisor_note": "This advisor composes structured facts, deterministic planning heuristics, and explicit uncertainty markers. It is not engineering approval or permit guidance.",
        }


design_advisor_service = DesignAdvisorService()

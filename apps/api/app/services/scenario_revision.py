from typing import Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core import models
from app.core.types import DataOrigin
from app.design_advisor.schemas import PlanningStateSnapshot, ResilienceRecommendation
from app.scenarios.schemas import ScenarioRevisionOverview, ScenarioRevisionSummary
from app.services.design_advisor import design_advisor_service


def _compact_planning_state_snapshot(planning_state: PlanningStateSnapshot) -> Dict[str, object]:
    return {
        "snapshot_id": planning_state.snapshot_id,
        "snapshot_label": planning_state.snapshot_label,
        "snapshot_kind": planning_state.snapshot_kind,
        "design_id": planning_state.design_id,
        "design_name": planning_state.design_name,
        "design_goal": planning_state.design_goal,
        "design_status": planning_state.design_status,
        "version_label": planning_state.version_label,
        "summary": planning_state.summary,
        "variants": [
            {
                "variant_key": variant.variant_key,
                "label": variant.label,
                "state_role": variant.state_role,
                "profile": variant.profile.value if variant.profile else None,
                "summary": variant.summary,
                "confidence_level": variant.confidence_level.value,
            }
            for variant in planning_state.variants
        ],
        "linked_scenarios": [
            {
                "scenario_id": scenario.scenario_id,
                "scenario_name": scenario.scenario_name,
                "revision_id": getattr(scenario, "latest_revision_id", None),
                "revision_label": getattr(scenario, "latest_revision_label", None),
                "revision_number": getattr(scenario, "latest_revision_number", 0),
            }
            for scenario in planning_state.linked_scenarios
        ],
    }


class ScenarioRevisionService:
    def _list_revision_models(
        self, db, scenario_id: str
    ) -> List[models.ScenarioRevision]:
        statement = (
            select(models.ScenarioRevision)
            .where(models.ScenarioRevision.scenario_id == scenario_id)
            .order_by(models.ScenarioRevision.revision_number.desc())
        )
        return db.scalars(statement).all()

    def list_revision_summaries(self, db, scenario_id: str) -> List[ScenarioRevisionSummary]:
        return [
            ScenarioRevisionSummary.from_orm(revision)
            for revision in self._list_revision_models(db, scenario_id)
        ]

    def build_revision_overview(self, db, scenario_id: str) -> ScenarioRevisionOverview:
        revisions = self._list_revision_models(db, scenario_id)
        latest = revisions[0] if revisions else None
        return ScenarioRevisionOverview(
            latest_revision_id=latest.id if latest else None,
            latest_revision_label=latest.revision_label if latest else None,
            latest_revision_status=latest.revision_status if latest else None,
            latest_revision_number=latest.revision_number if latest else 0,
            revision_count=len(revisions),
            note=(
                "Immutable revisions preserve saved planning-state framing for this scenario."
                if latest
                else "No immutable revisions have been captured for this scenario yet."
            ),
        )

    def _build_revision_payload(
        self,
        scenario: models.Scenario,
        recommendation: ResilienceRecommendation,
        planning_state: PlanningStateSnapshot,
    ) -> Dict[str, object]:
        return {
            "linked_design_id": scenario.linked_design_id,
            "design_goal_snapshot": planning_state.design_goal,
            "design_status_snapshot": planning_state.design_status,
            "recommended_profile_snapshot": recommendation.recommended_profile.value
            if recommendation.recommended_profile
            else None,
            "planning_summary": planning_state.summary,
            "planning_state_snapshot": _compact_planning_state_snapshot(planning_state),
        }

    def capture_revision(
        self,
        db,
        scenario: models.Scenario,
        reason: str = "saved_revision",
    ) -> models.ScenarioRevision:
        revisions = self._list_revision_models(db, scenario.id)
        latest = revisions[0] if revisions else None
        next_number = (latest.revision_number + 1) if latest else 1

        advisor = design_advisor_service.explain(db, scenario.linked_design_id)
        recommendation = advisor["recommendation_profiles"]
        planning_state = advisor["planning_state"]
        payload = self._build_revision_payload(scenario, recommendation, planning_state)

        revision = models.ScenarioRevision(
            id=f"{scenario.id}_rev_{next_number:03d}",
            scenario_id=scenario.id,
            parent_revision_id=latest.id if latest else None,
            revision_number=next_number,
            revision_label=f"Revision {next_number}",
            revision_status=reason,
            data_origin=DataOrigin.derived_estimate.value,
            **payload,
        )
        db.add(revision)
        db.commit()
        db.refresh(revision)
        return revision

    def ensure_revisions_for_existing_scenarios(self, db):
        statement = select(models.Scenario).options(selectinload(models.Scenario.revisions))
        scenarios = db.scalars(statement).all()
        for scenario in scenarios:
            if scenario.revisions:
                continue
            self.capture_revision(db, scenario, reason="seeded_baseline_revision")


scenario_revision_service = ScenarioRevisionService()

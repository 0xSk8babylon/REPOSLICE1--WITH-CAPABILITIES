from app.design_advisor.schemas import (
    PlanningStateScenarioLink,
    PlanningStateSnapshot,
    PlanningStateVariant,
)
from app.services.backup_capability import backup_capability_service
from app.services.compatibility import compatibility_service
from app.services.design_analysis import design_analysis_service
from app.services.design_completeness import design_completeness_service
from app.services.expansion_readiness import expansion_readiness_service
from app.services.install_complexity import install_complexity_service
from app.services.resilience_recommendation import resilience_recommendation_service


class DesignAdvisorService:
    def _format_version_label(self, timestamp):
        if not timestamp:
            return "Version not recorded"
        return timestamp.strftime("%Y-%m-%d %H:%M UTC")

    def _build_planning_state(self, analysis, recommendation):
        design = analysis["design"] if analysis else None
        current_architecture = recommendation.current_home_energy_architecture
        recommended_profile = next(
            (profile for profile in recommendation.profiles if profile.recommended),
            None,
        )
        future_ready_profile = next(
            (
                profile
                for profile in recommendation.profiles
                if profile.profile.value == "premium_future_ready"
            ),
            recommended_profile,
        )
        constrained_profile = next(
            (
                profile
                for profile in recommendation.profiles
                if profile.profile.value == "critical_efficient"
            ),
            recommended_profile,
        )

        variants = [
            PlanningStateVariant(
                variant_key="current_state",
                label="Current state",
                state_role="current_state",
                source_type="current_home_energy_architecture",
                summary=current_architecture.current_vs_proposed_architecture
                if current_architecture
                else "Current-home architecture has not been modeled for this design yet.",
                confidence_level=current_architecture.topology_confidence
                if current_architecture
                else recommendation.confidence_level,
                trust_state=current_architecture.inspectability.trust_state
                if current_architecture and current_architecture.inspectability
                else recommendation.data_origin,
                note="Structured current-state context stays separate from future planning pathways.",
            ),
        ]

        if recommended_profile:
            variants.append(
                PlanningStateVariant(
                    variant_key="proposed_pathway",
                    label="Proposed pathway",
                    state_role="proposed_pathway",
                    source_type="recommendation_profile",
                    profile=recommended_profile.profile,
                    summary=recommended_profile.fit_reason or recommended_profile.ui_description,
                    confidence_level=recommended_profile.inspectability.confidence_level
                    if recommended_profile.inspectability
                    else recommendation.confidence_level,
                    trust_state=recommended_profile.inspectability.trust_state
                    if recommended_profile.inspectability
                    else recommendation.data_origin,
                    note="The primary recommendation belongs to this snapshot only; later saved states may diverge.",
                )
            )

        if future_ready_profile:
            variants.append(
                PlanningStateVariant(
                    variant_key="future_ready_pathway",
                    label="Future-ready pathway",
                    state_role="future_ready_pathway",
                    source_type="recommendation_profile",
                    profile=future_ready_profile.profile,
                    summary=future_ready_profile.fit_reason
                    or future_ready_profile.ui_description,
                    confidence_level=future_ready_profile.inspectability.confidence_level
                    if future_ready_profile.inspectability
                    else recommendation.confidence_level,
                    trust_state=future_ready_profile.inspectability.trust_state
                    if future_ready_profile.inspectability
                    else recommendation.data_origin,
                    note="Use this variant to inspect broader upgrade posture without treating it as an automatic winner.",
                )
            )

        if constrained_profile:
            variants.append(
                PlanningStateVariant(
                    variant_key="constrained_pathway",
                    label="Constrained / minimal-upgrade pathway",
                    state_role="constrained_pathway",
                    source_type="recommendation_profile",
                    profile=constrained_profile.profile,
                    summary=constrained_profile.fit_reason
                    or constrained_profile.ui_description,
                    confidence_level=constrained_profile.inspectability.confidence_level
                    if constrained_profile.inspectability
                    else recommendation.confidence_level,
                    trust_state=constrained_profile.inspectability.trust_state
                    if constrained_profile.inspectability
                    else recommendation.data_origin,
                    note="This variant keeps lower-upgrade posture visible for tradeoff review, not as final design guidance.",
                )
            )

        linked_scenarios = [
            PlanningStateScenarioLink(
                scenario_id=scenario.id,
                scenario_name=scenario.name,
                description=scenario.description,
                linked_design_id=scenario.linked_design_id,
                latest_revision_id=latest_revision.id if latest_revision else None,
                latest_revision_label=latest_revision.revision_label if latest_revision else None,
                latest_revision_number=latest_revision.revision_number if latest_revision else 0,
                data_origin=scenario.data_origin,
                updated_at_label=self._format_version_label(scenario.updated_at),
                state_label="linked planning scenario",
                note=(
                    "Latest immutable revision metadata is attached when available, but the current advisor output still reflects the live linked design state."
                    if latest_revision
                    else "Saved scenario metadata exists for this design, but no immutable revision has been captured yet."
                ),
            )
            for scenario in sorted(
                [scenario for scenario in getattr(design, "scenarios", []) if scenario.linked_design_id == design.id],
                key=lambda scenario: (scenario.updated_at or scenario.created_at),
                reverse=True,
            )
            for latest_revision in [max(getattr(scenario, "revisions", []), key=lambda revision: revision.revision_number, default=None)]
        ]

        return PlanningStateSnapshot(
            snapshot_id=f"planning-state-{design.id}" if design else "planning-state-unavailable",
            snapshot_label=f"{design.name} planning snapshot" if design else "Planning snapshot unavailable",
            snapshot_kind="live_design_state",
            design_id=design.id if design else recommendation.design_id,
            design_name=design.name if design else recommendation.design_id,
            design_goal=design.design_goal if design else "unknown",
            design_status=analysis["effective_status"] if analysis else "unknown",
            version_label=self._format_version_label(design.updated_at if design else None),
            summary=(
                f"This advisor workspace reflects the current saved state of {design.name}. "
                f"Recommendation, architecture, and reasoning outputs belong to this planning snapshot."
            )
            if design
            else "This advisor workspace reflects the currently selected design state.",
            scenario_count=len(linked_scenarios),
            variants=variants,
            linked_scenarios=linked_scenarios,
            scope_note=(
                "Planning-state snapshots are additive identity framing for deterministic advisor outputs. "
                "They are not final design revisions, permit sets, or compliance-approved versions."
            ),
        )

    def explain(self, db, design_id: str):
        analysis = design_analysis_service.build(db, design_id)
        completeness = design_completeness_service.evaluate(db, design_id)
        recommendation = resilience_recommendation_service.recommend(db, design_id)
        return {
            "design_id": design_id,
            "compatibility": compatibility_service.evaluate_design(db, design_id),
            "backup": backup_capability_service.estimate(db, design_id),
            "expansion": expansion_readiness_service.score(db, design_id),
            "install_complexity": install_complexity_service.score(db, design_id),
            "recommendation_profiles": recommendation,
            "planning_state": self._build_planning_state(analysis, recommendation),
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

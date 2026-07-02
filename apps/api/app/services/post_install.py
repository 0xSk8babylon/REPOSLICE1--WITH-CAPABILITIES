from collections import Counter
from typing import List, Optional

from app.core.types import ConfidenceLevel
from app.post_install.schemas import (
    LifecycleEvent,
    LifecycleEventType,
    PostInstallBlocker,
    PostInstallBlockerCategory,
    PostInstallScope,
    PostInstallSourceBasis,
    PostInstallStatus,
    PostInstallSummary,
    PostInstallView,
    RetentionOpportunity,
    RetentionOpportunityType,
)

POST_INSTALL_LIMITATIONS = [
    "Post-install retention readiness is read-only planning metadata only.",
    "It does not create CRM records, write CRM data, create tasks, send email, create drip campaigns, push notifications, score leads, score sales opportunities, rank follow-ups, or choose a best upsell.",
    "It does not generate proposals, pricing, quotes, bids, final estimates, final designs, product recommendations, procurement actions, or operational behavior.",
    "Lifecycle events are request-time detections from existing planning views, not persisted events or authoritative installation records.",
    "Homeowner and contractor text are wording metadata only and are not permission-enforced views.",
]

POST_INSTALL_DEFERRED_BOUNDARIES = [
    "auth",
    "best_upsell_logic",
    "billing",
    "crm_integration",
    "crm_writes",
    "email_drip_campaigns",
    "external_services",
    "frontend",
    "lead_scoring",
    "migrations",
    "permission_enforcement",
    "persistence",
    "pricing",
    "proposal_generation",
    "push_behavior",
    "ranking",
    "sales_scoring",
    "secrets",
    "task_creation",
    "twin_id",
    "write_endpoints",
]


class PostInstallService:
    def _sorted_unique(self, values: List[str]) -> List[str]:
        return sorted({value for value in values if value})

    def _basis(
        self,
        *,
        source_refs: Optional[List[str]] = None,
        contractor_workflow_refs: Optional[List[str]] = None,
        product_preference_refs: Optional[List[str]] = None,
        proposal_option_refs: Optional[List[str]] = None,
        estimate_gate_refs: Optional[List[str]] = None,
        missing_input_refs: Optional[List[str]] = None,
        blocker_refs: Optional[List[str]] = None,
        lifecycle_event_refs: Optional[List[str]] = None,
        retention_opportunity_refs: Optional[List[str]] = None,
        deferred_boundary_refs: Optional[List[str]] = None,
        unavailable_source_refs: Optional[List[str]] = None,
        basis_quality: str = "request_time_derived_from_existing_phase_9_12_views",
    ) -> PostInstallSourceBasis:
        return PostInstallSourceBasis(
            source_views=[
                "ContractorWorkflowReadinessView",
                "ProductPreferencesView",
            ],
            source_fields=[
                "ContractorWorkflowReadinessView.readiness_lanes",
                "ContractorWorkflowReadinessView.blockers",
                "ContractorWorkflowReadinessView.option_candidate_refs",
                "ContractorWorkflowReadinessView.confirmation_gate_ids",
                "ProductPreferencesView.categories",
                "ProductPreferencesView.blockers",
                "ProductPreferencesView.confirmation_gate_ids",
            ],
            source_refs=self._sorted_unique(source_refs or []),
            contractor_workflow_refs=self._sorted_unique(contractor_workflow_refs or []),
            product_preference_refs=self._sorted_unique(product_preference_refs or []),
            proposal_option_refs=self._sorted_unique(proposal_option_refs or []),
            estimate_gate_refs=self._sorted_unique(estimate_gate_refs or []),
            missing_input_refs=self._sorted_unique(missing_input_refs or []),
            blocker_refs=self._sorted_unique(blocker_refs or []),
            lifecycle_event_refs=self._sorted_unique(lifecycle_event_refs or []),
            retention_opportunity_refs=self._sorted_unique(retention_opportunity_refs or []),
            deferred_boundary_refs=self._sorted_unique(deferred_boundary_refs or []),
            unavailable_source_refs=self._sorted_unique(unavailable_source_refs or []),
            basis_quality=basis_quality,
            request_time_derived=True,
            verified_fact_claim_present=False,
            limitations=POST_INSTALL_LIMITATIONS,
        )

    def _blocker(
        self,
        *,
        blocker_id: str,
        category: PostInstallBlockerCategory,
        severity: str,
        source_refs: Optional[List[str]] = None,
        missing_inputs: Optional[List[str]] = None,
        confirmation_gate_ids: Optional[List[str]] = None,
        homeowner_explanation: str,
        contractor_review_note: str,
    ) -> PostInstallBlocker:
        return PostInstallBlocker(
            blocker_id=blocker_id,
            category=category,
            severity=severity,
            source_refs=self._sorted_unique(source_refs or []),
            missing_inputs=self._sorted_unique(missing_inputs or []),
            confirmation_gate_ids=self._sorted_unique(confirmation_gate_ids or []),
            homeowner_explanation=homeowner_explanation,
            contractor_review_note=contractor_review_note,
        )

    def _event(
        self,
        *,
        event_type: LifecycleEventType,
        detected: bool,
        source_refs: Optional[List[str]] = None,
        missing_inputs: Optional[List[str]] = None,
        confirmation_gate_ids: Optional[List[str]] = None,
        explanation: str,
    ) -> LifecycleEvent:
        return LifecycleEvent(
            event_id=f"phase_13:{event_type.value}",
            event_type=event_type,
            detected=detected,
            event_label=event_type.value.replace("_", " "),
            source_refs=self._sorted_unique(source_refs or []),
            missing_inputs=self._sorted_unique(missing_inputs or []),
            confirmation_gate_ids=self._sorted_unique(confirmation_gate_ids or []),
            explanation=explanation,
            confidence_level=ConfidenceLevel.medium if detected else ConfidenceLevel.low,
        )

    def _opportunity(
        self,
        *,
        opportunity_type: RetentionOpportunityType,
        title: str,
        missing_inputs: Optional[List[str]] = None,
        blockers: Optional[List[PostInstallBlocker]] = None,
        confirmation_gate_ids: Optional[List[str]] = None,
        lifecycle_event_refs: Optional[List[str]] = None,
        source_basis: PostInstallSourceBasis,
        homeowner_summary: str,
        contractor_review_note: str,
    ) -> RetentionOpportunity:
        missing = self._sorted_unique(missing_inputs or [])
        blocker_records = sorted(blockers or [], key=lambda blocker: blocker.blocker_id)
        gates = self._sorted_unique(confirmation_gate_ids or [])
        if missing:
            status = PostInstallStatus.blocked_by_missing_inputs
            confidence = ConfidenceLevel.low
            follow_up_readiness = "manual_review_blocked_by_missing_inputs"
        elif blocker_records or gates:
            status = PostInstallStatus.review_required
            confidence = ConfidenceLevel.medium
            follow_up_readiness = "manual_review_ready_with_open_review_items"
        else:
            status = PostInstallStatus.retention_review_available
            confidence = ConfidenceLevel.medium
            follow_up_readiness = "manual_review_ready"
        opportunity_id = f"phase_13:{opportunity_type.value}"
        return RetentionOpportunity(
            opportunity_id=opportunity_id,
            opportunity_type=opportunity_type,
            status=status,
            confidence_level=confidence,
            title=title,
            homeowner_summary=homeowner_summary,
            contractor_review_note=contractor_review_note,
            follow_up_readiness=follow_up_readiness,
            source_basis=source_basis,
            missing_inputs=missing,
            blockers=blocker_records,
            confirmation_gate_ids=gates,
            lifecycle_event_refs=self._sorted_unique(lifecycle_event_refs or []),
            assumptions=["Opportunity categories use fixed Phase 13 ordering and are not ranked."],
            limitations=POST_INSTALL_LIMITATIONS,
        )

    def build_home_post_install_view(self, db, home_id: str) -> Optional[PostInstallView]:
        from app.services.contractor_workflow import contractor_workflow_service
        from app.services.product_preferences import product_preferences_service
        from app.services.twin_planning_context import twin_planning_context_service

        context = twin_planning_context_service.build(db, home_id)
        if context is None:
            return None

        contractor_view = contractor_workflow_service.build_home_contractor_workflow_readiness(db, home_id)
        product_view = product_preferences_service.build_home_product_preferences(db, home_id)
        unavailable_sources = [
            source_name
            for source_name, source_value in [
                ("ContractorWorkflowReadinessView", contractor_view),
                ("ProductPreferencesView", product_view),
            ]
            if source_value is None
        ]
        if unavailable_sources:
            blocker = self._blocker(
                blocker_id="source_unavailable:phase_13_post_install",
                category=PostInstallBlockerCategory.source_unavailable,
                severity="unavailable",
                source_refs=unavailable_sources,
                homeowner_explanation="Post-install retention readiness could not be assembled because source views were unavailable.",
                contractor_review_note="Review prompt only: rebuild source readiness context before using Phase 13 post-install metadata.",
            )
            source_basis = self._basis(
                source_refs=[section.section_key for section in context.sections],
                blocker_refs=[blocker.blocker_id],
                unavailable_source_refs=unavailable_sources,
                deferred_boundary_refs=POST_INSTALL_DEFERRED_BOUNDARIES,
                basis_quality="source_unavailable_for_phase_13_post_install",
            )
            summary = PostInstallSummary(
                overall_status=PostInstallStatus.unavailable,
                confidence_level=ConfidenceLevel.low,
                blocker_count=1,
                manual_follow_up_ready=False,
                crm_handoff_object_available=False,
                summary_boundary_note="Post-install readiness is source-limited and does not create CRM behavior.",
            )
            return PostInstallView(
                home_id=home_id,
                implementation_boundary="Read-only Phase 13 post-install view. Source readiness metadata was unavailable.",
                post_install_scope=PostInstallScope(limitations=POST_INSTALL_LIMITATIONS),
                summary=summary,
                blockers=[blocker],
                homeowner_summary="Post-install readiness is unavailable because source planning views are incomplete.",
                contractor_summary="Source readiness metadata is unavailable for this home.",
                source_basis=source_basis,
                blocker_category_counts={blocker.category.value: 1},
                assumptions=["A home record exists, but one or more source views were unavailable."],
                limitations=POST_INSTALL_LIMITATIONS,
                deferred_boundaries=sorted(POST_INSTALL_DEFERRED_BOUNDARIES),
                compatibility_note="Existing Phase 9 through Phase 12 routes remain unchanged.",
            )

        missing_inputs = self._sorted_unique(
            contractor_view.missing_inputs
            + product_view.missing_inputs
        )
        confirmation_gate_ids = self._sorted_unique(
            contractor_view.confirmation_gate_ids
            + product_view.confirmation_gate_ids
        )
        blockers = sorted(
            [
                self._blocker(
                    blocker_id=f"contractor_workflow:{blocker.blocker_id}",
                    category=PostInstallBlockerCategory.review_required,
                    severity=blocker.severity,
                    source_refs=blocker.source_refs,
                    missing_inputs=blocker.missing_inputs,
                    confirmation_gate_ids=blocker.gate_refs,
                    homeowner_explanation=blocker.homeowner_explanation,
                    contractor_review_note=blocker.contractor_readiness_prompt,
                )
                for blocker in contractor_view.blockers
            ]
            + [
                self._blocker(
                    blocker_id=f"product_preferences:{blocker.blocker_id}",
                    category=(
                        PostInstallBlockerCategory.missing_input
                        if blocker.missing_inputs
                        else PostInstallBlockerCategory.review_required
                    ),
                    severity=blocker.severity,
                    source_refs=blocker.source_refs,
                    missing_inputs=blocker.missing_inputs,
                    confirmation_gate_ids=blocker.gate_refs,
                    homeowner_explanation=blocker.homeowner_explanation,
                    contractor_review_note=blocker.contractor_review_prompt,
                )
                for blocker in product_view.blockers
            ],
            key=lambda blocker: blocker.blocker_id,
        )
        lifecycle_events = sorted(
            [
                self._event(
                    event_type=LifecycleEventType.post_install_context_assembled,
                    detected=True,
                    source_refs=["ContractorWorkflowReadinessView", "ProductPreferencesView"],
                    explanation="Existing planning views were available for request-time post-install retention assembly.",
                ),
                self._event(
                    event_type=LifecycleEventType.contractor_review_required,
                    detected=contractor_view.summary.contractor_review_required,
                    source_refs=["ContractorWorkflowReadinessView.summary.contractor_review_required"],
                    explanation="Contractor review is indicated by the existing contractor workflow readiness source view.",
                ),
                self._event(
                    event_type=LifecycleEventType.missing_input_detected,
                    detected=bool(missing_inputs),
                    missing_inputs=missing_inputs,
                    explanation="One or more source views carry missing inputs into post-install readiness.",
                ),
                self._event(
                    event_type=LifecycleEventType.confirmation_gate_open,
                    detected=bool(confirmation_gate_ids),
                    confirmation_gate_ids=confirmation_gate_ids,
                    explanation="Confirmation gate topics are present in existing readiness views.",
                ),
                self._event(
                    event_type=LifecycleEventType.product_review_needed,
                    detected=bool(product_view.categories),
                    source_refs=[category.category_id.value for category in product_view.categories],
                    explanation="Product/install preference categories are present for manual review preparation.",
                ),
                self._event(
                    event_type=LifecycleEventType.proposal_prep_deferred,
                    detected="proposal_prep_blocked_deferred" in [lane.lane_id.value for lane in contractor_view.readiness_lanes],
                    source_refs=["ContractorWorkflowReadinessView.readiness_lanes.proposal_prep_blocked_deferred"],
                    explanation="Proposal preparation remains deferred where the contractor workflow source view carries that lane.",
                ),
            ],
            key=lambda event: event.event_id,
        )
        detected_event_refs = [event.event_id for event in lifecycle_events if event.detected]
        source_refs = [section.section_key for section in context.sections]
        base_basis = self._basis(
            source_refs=source_refs,
            contractor_workflow_refs=[lane.lane_id.value for lane in contractor_view.readiness_lanes],
            product_preference_refs=[category.category_id.value for category in product_view.categories],
            proposal_option_refs=contractor_view.option_candidate_refs,
            estimate_gate_refs=confirmation_gate_ids,
            missing_input_refs=missing_inputs,
            blocker_refs=[blocker.blocker_id for blocker in blockers],
            lifecycle_event_refs=detected_event_refs,
            deferred_boundary_refs=POST_INSTALL_DEFERRED_BOUNDARIES,
            basis_quality="home_level_phase_13_post_install_rollup",
        )
        opportunities = sorted(
            [
                self._opportunity(
                    opportunity_type=RetentionOpportunityType.contractor_review_followup,
                    title="Contractor review follow-up",
                    blockers=blockers,
                    confirmation_gate_ids=contractor_view.confirmation_gate_ids,
                    lifecycle_event_refs=detected_event_refs,
                    source_basis=base_basis,
                    homeowner_summary="Contractor review follow-up summarizes review items from the current planning context.",
                    contractor_review_note="Review prompt only: use existing contractor readiness lanes as manual follow-up context.",
                ),
                self._opportunity(
                    opportunity_type=RetentionOpportunityType.documentation_completion,
                    title="Documentation completion",
                    missing_inputs=missing_inputs,
                    lifecycle_event_refs=detected_event_refs,
                    source_basis=base_basis,
                    homeowner_summary="Documentation completion identifies missing planning inputs that may need follow-up.",
                    contractor_review_note="Review prompt only: missing-input follow-up is manual metadata, not a generated task.",
                ),
                self._opportunity(
                    opportunity_type=RetentionOpportunityType.estimate_readiness_followup,
                    title="Estimate readiness follow-up",
                    confirmation_gate_ids=contractor_view.confirmation_gate_ids,
                    lifecycle_event_refs=detected_event_refs,
                    source_basis=base_basis,
                    homeowner_summary="Estimate readiness follow-up summarizes open confirmation topics before estimating.",
                    contractor_review_note="Review prompt only: this is not an estimate, quote, bid, or pricing instruction.",
                ),
                self._opportunity(
                    opportunity_type=RetentionOpportunityType.homeowner_context_followup,
                    title="Homeowner context follow-up",
                    missing_inputs=product_view.missing_inputs,
                    lifecycle_event_refs=detected_event_refs,
                    source_basis=base_basis,
                    homeowner_summary="Homeowner context follow-up summarizes planning context gaps in homeowner-safe wording.",
                    contractor_review_note="Review prompt only: homeowner-facing wording metadata is not permission enforcement.",
                ),
                self._opportunity(
                    opportunity_type=RetentionOpportunityType.product_spec_followup,
                    title="Product/spec follow-up",
                    missing_inputs=[
                        missing for missing in product_view.missing_inputs if "spec" in missing or "manufacturer" in missing
                    ],
                    confirmation_gate_ids=[
                        gate for gate in product_view.confirmation_gate_ids if "spec" in gate or "manufacturer" in gate
                    ],
                    lifecycle_event_refs=detected_event_refs,
                    source_basis=base_basis,
                    homeowner_summary="Product/spec follow-up identifies product information that remains review-limited.",
                    contractor_review_note="Review prompt only: this does not recommend products, rank products, or procure equipment.",
                ),
                self._opportunity(
                    opportunity_type=RetentionOpportunityType.proposal_context_followup,
                    title="Proposal context follow-up",
                    blockers=[
                        blocker
                        for blocker in blockers
                        if "proposal_prep" in blocker.blocker_id or "option_candidate" in blocker.blocker_id
                    ],
                    confirmation_gate_ids=contractor_view.confirmation_gate_ids,
                    lifecycle_event_refs=detected_event_refs,
                    source_basis=base_basis,
                    homeowner_summary="Proposal context follow-up keeps proposal preparation deferred until source blockers are resolved.",
                    contractor_review_note="Review prompt only: this does not generate proposals, prices, quotes, bids, or packages.",
                ),
            ],
            key=lambda opportunity: opportunity.opportunity_type.value,
        )
        all_opportunity_blockers = sorted(
            [blocker for opportunity in opportunities for blocker in opportunity.blockers],
            key=lambda blocker: blocker.blocker_id,
        )
        blocker_records = sorted(blockers + all_opportunity_blockers, key=lambda blocker: blocker.blocker_id)
        if unavailable_sources:
            overall_status = PostInstallStatus.unavailable
            confidence = ConfidenceLevel.low
        elif missing_inputs:
            overall_status = PostInstallStatus.blocked_by_missing_inputs
            confidence = ConfidenceLevel.low
        elif blocker_records or confirmation_gate_ids:
            overall_status = PostInstallStatus.review_required
            confidence = ConfidenceLevel.medium
        else:
            overall_status = PostInstallStatus.retention_review_available
            confidence = ConfidenceLevel.medium
        source_basis = self._basis(
            source_refs=source_refs,
            contractor_workflow_refs=[lane.lane_id.value for lane in contractor_view.readiness_lanes],
            product_preference_refs=[category.category_id.value for category in product_view.categories],
            proposal_option_refs=contractor_view.option_candidate_refs,
            estimate_gate_refs=confirmation_gate_ids,
            missing_input_refs=missing_inputs,
            blocker_refs=[blocker.blocker_id for blocker in blocker_records],
            lifecycle_event_refs=detected_event_refs,
            retention_opportunity_refs=[opportunity.opportunity_id for opportunity in opportunities],
            deferred_boundary_refs=POST_INSTALL_DEFERRED_BOUNDARIES,
            basis_quality="home_level_phase_13_post_install_rollup",
        )
        summary = PostInstallSummary(
            overall_status=overall_status,
            confidence_level=confidence,
            opportunity_count=len(opportunities),
            lifecycle_event_count=sum(1 for event in lifecycle_events if event.detected),
            blocker_count=len(blocker_records),
            missing_input_count=len(missing_inputs),
            confirmation_gate_count=len(confirmation_gate_ids),
            manual_follow_up_ready=True,
            crm_handoff_object_available=True,
            crm_write_allowed=False,
            email_campaign_allowed=False,
            task_creation_allowed=False,
            scoring_allowed=False,
            ranking_allowed=False,
            push_allowed=False,
            summary_boundary_note=(
                "Post-install retention readiness is manual review metadata only. It does not write CRM data, "
                "create tasks, send email, score, rank, choose upsells, push notifications, or create external behavior."
            ),
        )
        return PostInstallView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 13 post-install retention view built request-time from existing Phase 11 contractor workflow "
                "readiness and Phase 12 product preference metadata, carrying Phase 9/10 references only where those source "
                "contracts already surface them. "
                "It detects lifecycle events and retention follow-up opportunities only; it does not write data, persist state, "
                "run migrations, enforce permissions, integrate with CRM, write CRM records, create tasks, send email, create drip "
                "campaigns, score leads or sales opportunities, rank follow-ups, choose a best upsell, push notifications, create "
                "external service behavior, create twin_id, create graph behavior, or create operational behavior."
            ),
            post_install_scope=PostInstallScope(limitations=POST_INSTALL_LIMITATIONS),
            summary=summary,
            opportunities=opportunities,
            lifecycle_events=lifecycle_events,
            blockers=blocker_records,
            missing_inputs=missing_inputs,
            confirmation_gate_ids=confirmation_gate_ids,
            homeowner_summary="Post-install readiness summarizes manual follow-up context from existing planning views.",
            contractor_summary=(
                f"Phase 13 post-install readiness status is {overall_status.value}. "
                f"{len(opportunities)} fixed follow-up categories, {summary.lifecycle_event_count} detected lifecycle events, "
                f"{len(missing_inputs)} missing inputs, and {len(confirmation_gate_ids)} confirmation gate topics are present."
            ),
            follow_up_readiness_notes=[opportunity.follow_up_readiness for opportunity in opportunities],
            source_basis=source_basis,
            blocker_category_counts=dict(sorted(Counter(blocker.category.value for blocker in blocker_records).items())),
            assumptions=[
                "Retention opportunities use fixed deterministic categories and are not ranked.",
                "Lifecycle events are detected request-time from existing source views and are not persisted.",
                "Existing source views are authoritative over this derived Phase 13 layer.",
            ],
            limitations=POST_INSTALL_LIMITATIONS,
            deferred_boundaries=sorted(POST_INSTALL_DEFERRED_BOUNDARIES),
            compatibility_note=(
                "Existing estimate-readiness, proposal-option-set, contractor-workflow, product-preference, "
                "scenario, takeoff, and design routes remain unchanged."
            ),
        )


post_install_service = PostInstallService()

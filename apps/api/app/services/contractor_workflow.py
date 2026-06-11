from collections import Counter
from typing import List, Optional, Tuple

from app.contractor_workflow.schemas import (
    ContractorWorkflowBlocker,
    ContractorWorkflowBlockerCategory,
    ContractorWorkflowLaneId,
    ContractorWorkflowReadinessLane,
    ContractorWorkflowReadinessStatus,
    ContractorWorkflowReadinessSummary,
    ContractorWorkflowReadinessView,
    ContractorWorkflowScope,
    ContractorWorkflowSourceBasis,
)
from app.core.types import ConfidenceLevel


CONTRACTOR_WORKFLOW_LIMITATIONS = [
    "Contractor workflow readiness is read-only planning metadata for review preparation only.",
    "It is not a quote, an approval, a final estimate, a final design, or a final proposal.",
    "It does not create contractor-held workflow state, account access, permission enforcement, exports, CRM behavior, email behavior, or source record changes.",
    "Readiness lanes organize existing Phase 5, Phase 6, Phase 9, and Phase 10 context without creating new authority.",
]

CONTRACTOR_WORKFLOW_DEFERRED_BOUNDARIES = [
    "accept_complete_states",
    "assignments",
    "auth",
    "contractor_accounts",
    "contractor_state_persistence",
    "crm_automation",
    "email_automation",
    "exports",
    "external_services",
    "final_design",
    "final_estimate",
    "final_proposal",
    "graph_behavior",
    "lifecycle_control",
    "migrations",
    "operational_behavior",
    "permission_enforcement",
    "persistence",
    "pricing",
    "quote_generation",
    "source_record_changes",
    "twin_id",
    "write_endpoints",
]


class ContractorWorkflowService:
    def _sorted_unique(self, values: List[str]) -> List[str]:
        return sorted({value for value in values if value})

    def _basis(
        self,
        *,
        source_refs: Optional[List[str]] = None,
        contractor_context_refs: Optional[List[str]] = None,
        planning_exchange_refs: Optional[List[str]] = None,
        estimate_readiness_refs: Optional[List[str]] = None,
        proposal_option_set_refs: Optional[List[str]] = None,
        compatibility_path_refs: Optional[List[str]] = None,
        takeoff_line_refs: Optional[List[str]] = None,
        blocker_refs: Optional[List[str]] = None,
        missing_input_refs: Optional[List[str]] = None,
        confirmation_gate_refs: Optional[List[str]] = None,
        option_candidate_refs: Optional[List[str]] = None,
        dependency_refs: Optional[List[str]] = None,
        assumption_refs: Optional[List[str]] = None,
        deferred_boundary_refs: Optional[List[str]] = None,
        unavailable_source_refs: Optional[List[str]] = None,
        basis_quality: str = "request_time_derived_from_existing_phase_5_6_9_10_views",
    ) -> ContractorWorkflowSourceBasis:
        return ContractorWorkflowSourceBasis(
            source_views=[
                "ContractorPlanningContextView",
                "ContractorConfirmationGateProjectionView",
                "ContractorInstallComplexityView",
                "PlanningExchangeObjectView",
                "EstimateReadinessView",
                "ProposalOptionSetsView",
            ],
            source_fields=[
                "ContractorPlanningContextView.next_safe_contractor_review_prompts",
                "ContractorPlanningContextView.missing_information",
                "ContractorConfirmationGateProjectionView.gates",
                "ContractorInstallComplexityView.signals",
                "PlanningExchangeObjectView.section_mappings",
                "PlanningExchangeObjectView.readiness_summary",
                "EstimateReadinessView.confirmation_gates",
                "EstimateReadinessView.blockers",
                "EstimateReadinessView.missing_inputs",
                "ProposalOptionSetsView.option_candidates",
                "ProposalOptionSetsView.blockers",
                "ProposalOptionSetsView.source_basis",
            ],
            source_refs=self._sorted_unique(source_refs or []),
            contractor_context_refs=self._sorted_unique(contractor_context_refs or []),
            planning_exchange_refs=self._sorted_unique(planning_exchange_refs or []),
            estimate_readiness_refs=self._sorted_unique(estimate_readiness_refs or []),
            proposal_option_set_refs=self._sorted_unique(proposal_option_set_refs or []),
            compatibility_path_refs=self._sorted_unique(compatibility_path_refs or []),
            takeoff_line_refs=self._sorted_unique(takeoff_line_refs or []),
            blocker_refs=self._sorted_unique(blocker_refs or []),
            missing_input_refs=self._sorted_unique(missing_input_refs or []),
            confirmation_gate_refs=self._sorted_unique(confirmation_gate_refs or []),
            option_candidate_refs=self._sorted_unique(option_candidate_refs or []),
            dependency_refs=self._sorted_unique(dependency_refs or []),
            assumption_refs=self._sorted_unique(assumption_refs or []),
            deferred_boundary_refs=self._sorted_unique(deferred_boundary_refs or []),
            unavailable_source_refs=self._sorted_unique(unavailable_source_refs or []),
            basis_quality=basis_quality,
            request_time_derived=True,
            verified_fact_claim_present=False,
            limitations=CONTRACTOR_WORKFLOW_LIMITATIONS,
        )

    def _status(
        self,
        *,
        blocker_count: int,
        missing_input_count: int = 0,
        unavailable_count: int = 0,
    ) -> Tuple[ContractorWorkflowReadinessStatus, ConfidenceLevel]:
        if unavailable_count:
            return ContractorWorkflowReadinessStatus.unavailable, ConfidenceLevel.low
        if blocker_count or missing_input_count:
            return ContractorWorkflowReadinessStatus.blocked_or_deferred, ConfidenceLevel.low
        return ContractorWorkflowReadinessStatus.review_context_available, ConfidenceLevel.medium

    def _blocker(
        self,
        *,
        blocker_id: str,
        lane_id: ContractorWorkflowLaneId,
        category: ContractorWorkflowBlockerCategory,
        severity: str,
        source_refs: Optional[List[str]] = None,
        gate_refs: Optional[List[str]] = None,
        missing_inputs: Optional[List[str]] = None,
        option_candidate_refs: Optional[List[str]] = None,
        dependency_refs: Optional[List[str]] = None,
        homeowner_explanation: str,
        contractor_readiness_prompt: str,
    ) -> ContractorWorkflowBlocker:
        return ContractorWorkflowBlocker(
            blocker_id=blocker_id,
            lane_id=lane_id,
            category=category,
            severity=severity,
            source_refs=self._sorted_unique(source_refs or []),
            gate_refs=self._sorted_unique(gate_refs or []),
            missing_inputs=self._sorted_unique(missing_inputs or []),
            option_candidate_refs=self._sorted_unique(option_candidate_refs or []),
            dependency_refs=self._sorted_unique(dependency_refs or []),
            homeowner_explanation=homeowner_explanation,
            contractor_readiness_prompt=contractor_readiness_prompt,
        )

    def _lane(
        self,
        *,
        lane_id: ContractorWorkflowLaneId,
        lane_label: str,
        blocker_records: List[ContractorWorkflowBlocker],
        missing_inputs: Optional[List[str]] = None,
        confirmation_gate_ids: Optional[List[str]] = None,
        option_candidate_refs: Optional[List[str]] = None,
        dependency_refs: Optional[List[str]] = None,
        assumptions: Optional[List[str]] = None,
        source_basis: ContractorWorkflowSourceBasis,
        reason_available: str,
        reason_blocked: str,
        homeowner_summary: str,
        contractor_readiness_prompt: str,
        unavailable_count: int = 0,
    ) -> ContractorWorkflowReadinessLane:
        clean_missing = self._sorted_unique(missing_inputs or [])
        status, confidence = self._status(
            blocker_count=len(blocker_records),
            missing_input_count=len(clean_missing),
            unavailable_count=unavailable_count,
        )
        return ContractorWorkflowReadinessLane(
            lane_id=lane_id,
            lane_label=lane_label,
            status=status,
            confidence_level=confidence,
            reason=reason_available if status == ContractorWorkflowReadinessStatus.review_context_available else reason_blocked,
            homeowner_summary=homeowner_summary,
            contractor_readiness_prompt=contractor_readiness_prompt,
            source_basis=source_basis,
            blockers=sorted(blocker_records, key=lambda blocker: blocker.blocker_id),
            missing_inputs=clean_missing,
            confirmation_gate_ids=self._sorted_unique(confirmation_gate_ids or []),
            option_candidate_refs=self._sorted_unique(option_candidate_refs or []),
            dependency_refs=self._sorted_unique(dependency_refs or []),
            assumptions=self._sorted_unique(assumptions or []),
            deferred_boundaries=sorted(CONTRACTOR_WORKFLOW_DEFERRED_BOUNDARIES),
            limitations=CONTRACTOR_WORKFLOW_LIMITATIONS,
        )

    def _planning_lane(self, contractor_context, planning_exchange, install_complexity) -> ContractorWorkflowReadinessLane:
        missing_inputs = self._sorted_unique(
            [
                missing
                for item in contractor_context.missing_information
                for missing in item.missing_inputs
            ]
            + [
                missing
                for mapping in planning_exchange.section_mappings
                for missing in mapping.missing_inputs
            ]
        )
        contractor_refs = [item.item_id for item in contractor_context.next_safe_contractor_review_prompts]
        exchange_refs = [mapping.section_key for mapping in planning_exchange.section_mappings]
        signal_refs = [signal.signal_id for signal in install_complexity.signals]
        blockers = []
        if missing_inputs:
            blockers.append(
                self._blocker(
                    blocker_id="planning_review:missing_inputs",
                    lane_id=ContractorWorkflowLaneId.planning_review,
                    category=ContractorWorkflowBlockerCategory.missing_input,
                    severity="review_limited",
                    source_refs=["contractor_context", "planning_exchange"],
                    missing_inputs=missing_inputs,
                    homeowner_explanation="Some planning information is still missing before contractor review preparation is complete.",
                    contractor_readiness_prompt="Review missing planning inputs before relying on this lane for preparation.",
                )
            )
        return self._lane(
            lane_id=ContractorWorkflowLaneId.planning_review,
            lane_label="Planning review",
            blocker_records=blockers,
            missing_inputs=missing_inputs,
            dependency_refs=signal_refs,
            assumptions=["Planning review lane is assembled from existing contractor-safe context and exchange mappings."],
            source_basis=self._basis(
                contractor_context_refs=contractor_refs,
                planning_exchange_refs=exchange_refs,
                missing_input_refs=missing_inputs,
                dependency_refs=signal_refs,
                basis_quality="planning_review_lane_from_phase_5_and_phase_6_context",
            ),
            reason_available="Contractor-safe planning context is available as review metadata.",
            reason_blocked="Planning review is limited by missing information or uncertainty already surfaced by source views.",
            homeowner_summary="Planning context is organized for contractor review preparation only.",
            contractor_readiness_prompt="Use the planning review lane as a checklist of existing context and uncertainty.",
        )

    def _missing_input_lane(self, contractor_context, estimate_view, proposal_view) -> ContractorWorkflowReadinessLane:
        missing_inputs = self._sorted_unique(
            [
                missing
                for item in contractor_context.missing_information
                for missing in item.missing_inputs
            ]
            + estimate_view.missing_inputs
            + proposal_view.missing_inputs
        )
        blockers = []
        if missing_inputs:
            blockers.append(
                self._blocker(
                    blocker_id="missing_input_review:missing_inputs",
                    lane_id=ContractorWorkflowLaneId.missing_input_review,
                    category=ContractorWorkflowBlockerCategory.missing_input,
                    severity="blocker",
                    source_refs=["contractor_context", "estimate_readiness", "proposal_option_sets"],
                    missing_inputs=missing_inputs,
                    homeowner_explanation="Missing inputs limit readiness for contractor review preparation.",
                    contractor_readiness_prompt="Treat missing inputs as review prompts for information gathering.",
                )
            )
        return self._lane(
            lane_id=ContractorWorkflowLaneId.missing_input_review,
            lane_label="Missing-input review",
            blocker_records=blockers,
            missing_inputs=missing_inputs,
            assumptions=["Missing inputs are carried from existing contractor, estimate-readiness, and proposal-option views."],
            source_basis=self._basis(
                contractor_context_refs=[item.item_id for item in contractor_context.missing_information],
                estimate_readiness_refs=["EstimateReadinessView.missing_inputs"],
                proposal_option_set_refs=["ProposalOptionSetsView.missing_inputs"],
                missing_input_refs=missing_inputs,
                basis_quality="missing_input_lane_from_existing_source_missing_input_lists",
            ),
            reason_available="No missing inputs were surfaced by the composed readiness views.",
            reason_blocked="Missing inputs remain in the source readiness views.",
            homeowner_summary="Missing items are shown so the homeowner can see what may need review.",
            contractor_readiness_prompt="Review missing inputs before proposal preparation or estimate preparation.",
        )

    def _confirmation_gate_lane(self, gate_view, estimate_view) -> ContractorWorkflowReadinessLane:
        gate_ids = self._sorted_unique(
            [gate.gate_id for gate in gate_view.gates]
            + [gate.gate_id for gate in estimate_view.confirmation_gates]
        )
        open_gate_ids = self._sorted_unique(
            [
                gate.gate_id
                for gate in estimate_view.confirmation_gates
                if gate.status.value != "confirmed"
            ]
        )
        blockers = [
            self._blocker(
                blocker_id=f"confirmation_gate_review:{gate_id}",
                lane_id=ContractorWorkflowLaneId.confirmation_gate_review,
                category=ContractorWorkflowBlockerCategory.confirmation_gate_review,
                severity="review_required",
                source_refs=["contractor_confirmation_gates", "estimate_readiness"],
                gate_refs=[gate_id],
                homeowner_explanation="A contractor review topic remains unresolved in the readiness metadata.",
                contractor_readiness_prompt="Review this gate topic against field and source information outside this response.",
            )
            for gate_id in open_gate_ids
        ]
        return self._lane(
            lane_id=ContractorWorkflowLaneId.confirmation_gate_review,
            lane_label="Confirmation-gate review",
            blocker_records=blockers,
            confirmation_gate_ids=gate_ids,
            assumptions=["Gate status is read-only derived metadata and is not persisted by this view."],
            source_basis=self._basis(
                contractor_context_refs=[gate.gate_id for gate in gate_view.gates],
                estimate_readiness_refs=[gate.gate_id for gate in estimate_view.confirmation_gates],
                confirmation_gate_refs=gate_ids,
                blocker_refs=[blocker.blocker_id for blocker in estimate_view.blockers],
                basis_quality="confirmation_gate_lane_from_phase_5_and_phase_9_gate_metadata",
            ),
            reason_available="Confirmation-gate metadata is available for review preparation.",
            reason_blocked="One or more gate topics still need review outside this response.",
            homeowner_summary="Review topics are listed as planning prompts only.",
            contractor_readiness_prompt="Use gate topics to guide review preparation, not as status authority.",
        )

    def _option_candidate_lane(self, proposal_view) -> ContractorWorkflowReadinessLane:
        option_refs = self._sorted_unique(
            [candidate.option_candidate_id for candidate in proposal_view.option_candidates]
        )
        blocker_refs = self._sorted_unique([blocker.blocker_id for blocker in proposal_view.blockers])
        missing_inputs = self._sorted_unique(proposal_view.missing_inputs)
        dependency_refs = self._sorted_unique(proposal_view.dependency_refs)
        blockers = [
            self._blocker(
                blocker_id=f"option_candidate_review:{blocker.blocker_id}",
                lane_id=ContractorWorkflowLaneId.option_candidate_review,
                category=ContractorWorkflowBlockerCategory.option_candidate_review,
                severity=blocker.severity,
                source_refs=blocker.source_refs,
                gate_refs=blocker.gate_refs,
                missing_inputs=blocker.missing_inputs,
                option_candidate_refs=option_refs,
                dependency_refs=dependency_refs,
                homeowner_explanation=blocker.homeowner_explanation,
                contractor_readiness_prompt="Review the proposal-option readiness source before using this option candidate for preparation.",
            )
            for blocker in proposal_view.blockers
        ]
        return self._lane(
            lane_id=ContractorWorkflowLaneId.option_candidate_review,
            lane_label="Option-candidate review",
            blocker_records=blockers,
            missing_inputs=missing_inputs,
            confirmation_gate_ids=proposal_view.confirmation_gate_ids,
            option_candidate_refs=option_refs,
            dependency_refs=dependency_refs,
            assumptions=proposal_view.assumptions,
            source_basis=self._basis(
                proposal_option_set_refs=option_refs,
                compatibility_path_refs=proposal_view.source_basis.compatibility_path_refs,
                takeoff_line_refs=proposal_view.source_basis.takeoff_line_refs,
                blocker_refs=blocker_refs,
                missing_input_refs=missing_inputs,
                confirmation_gate_refs=proposal_view.confirmation_gate_ids,
                option_candidate_refs=option_refs,
                dependency_refs=dependency_refs,
                deferred_boundary_refs=proposal_view.deferred_boundaries,
                basis_quality="option_candidate_lane_from_phase_10_proposal_option_sets",
            ),
            reason_available="Proposal option-set metadata is available for contractor review preparation.",
            reason_blocked="Proposal option-set metadata is limited by blockers, gates, or missing inputs.",
            homeowner_summary="Option candidates are planning metadata only and do not select a path.",
            contractor_readiness_prompt="Use option candidates as review prompts only.",
        )

    def _proposal_prep_lane(self, proposal_view, estimate_view) -> ContractorWorkflowReadinessLane:
        missing_inputs = self._sorted_unique(proposal_view.missing_inputs + estimate_view.missing_inputs)
        gate_ids = self._sorted_unique(proposal_view.confirmation_gate_ids)
        option_refs = self._sorted_unique(
            [candidate.option_candidate_id for candidate in proposal_view.option_candidates]
        )
        blockers = [
            self._blocker(
                blocker_id="proposal_prep:deferred",
                lane_id=ContractorWorkflowLaneId.proposal_prep_blocked_deferred,
                category=ContractorWorkflowBlockerCategory.proposal_prep_deferred,
                severity="deferred",
                source_refs=["proposal_option_sets", "estimate_readiness"],
                gate_refs=gate_ids,
                missing_inputs=missing_inputs,
                option_candidate_refs=option_refs,
                dependency_refs=proposal_view.dependency_refs,
                homeowner_explanation="Proposal preparation remains blocked or deferred in the current planning metadata.",
                contractor_readiness_prompt="Use this lane only to see why proposal preparation is not available from the app.",
            )
        ]
        return self._lane(
            lane_id=ContractorWorkflowLaneId.proposal_prep_blocked_deferred,
            lane_label="Proposal-prep blocked/deferred",
            blocker_records=blockers,
            missing_inputs=missing_inputs,
            confirmation_gate_ids=gate_ids,
            option_candidate_refs=option_refs,
            dependency_refs=proposal_view.dependency_refs,
            assumptions=[
                "Proposal preparation lane preserves Phase 10 deferred boundaries.",
                "This view does not create commercial, engineering, authority, or workflow state.",
            ],
            source_basis=self._basis(
                estimate_readiness_refs=["EstimateReadinessView.readiness_summary"],
                proposal_option_set_refs=option_refs,
                blocker_refs=[blocker.blocker_id for blocker in proposal_view.blockers],
                missing_input_refs=missing_inputs,
                confirmation_gate_refs=gate_ids,
                option_candidate_refs=option_refs,
                dependency_refs=proposal_view.dependency_refs,
                deferred_boundary_refs=proposal_view.deferred_boundaries + CONTRACTOR_WORKFLOW_DEFERRED_BOUNDARIES,
                basis_quality="proposal_prep_lane_from_phase_9_and_phase_10_deferred_boundaries",
            ),
            reason_available="Proposal preparation remains outside this read-only readiness view.",
            reason_blocked="Proposal preparation is blocked or deferred by existing readiness metadata and explicit boundaries.",
            homeowner_summary="This is not a quote, approval, final estimate, final design, or final proposal.",
            contractor_readiness_prompt="Do not treat this lane as proposal generation or authorization.",
        )

    def build_home_contractor_workflow_readiness(self, db, home_id: str) -> Optional[ContractorWorkflowReadinessView]:
        from app.services.contractor_context import contractor_context_service
        from app.services.estimate_readiness import estimate_readiness_service
        from app.services.planning_exchange import planning_exchange_service
        from app.services.proposal_option_sets import proposal_option_sets_service
        from app.services.twin_planning_context import twin_planning_context_service

        context = twin_planning_context_service.build(db, home_id)
        if context is None:
            return None

        contractor_context = contractor_context_service.build_contractor_planning_context(db, home_id)
        gate_view = contractor_context_service.build_confirmation_gate_projection(
            db, home_id, contractor_context=contractor_context
        )
        install_complexity = contractor_context_service.build_install_complexity_view(
            db, home_id, contractor_context=contractor_context, gate_projection=gate_view
        )
        planning_exchange = planning_exchange_service.build_planning_exchange_object(
            db,
            home_id,
            contractor_context=contractor_context,
            confirmation_gates=gate_view,
            install_complexity=install_complexity,
        )
        estimate_view = estimate_readiness_service.build_home_estimate_readiness(db, home_id)
        proposal_view = proposal_option_sets_service.build_home_proposal_option_sets(db, home_id)
        unavailable_sources = [
            source_name
            for source_name, source_value in [
                ("ContractorPlanningContextView", contractor_context),
                ("ContractorConfirmationGateProjectionView", gate_view),
                ("ContractorInstallComplexityView", install_complexity),
                ("PlanningExchangeObjectView", planning_exchange),
                ("EstimateReadinessView", estimate_view),
                ("ProposalOptionSetsView", proposal_view),
            ]
            if source_value is None
        ]
        if unavailable_sources:
            blockers = [
                self._blocker(
                    blocker_id=f"source_unavailable:{source}",
                    lane_id=ContractorWorkflowLaneId.planning_review,
                    category=ContractorWorkflowBlockerCategory.source_unavailable,
                    severity="unavailable",
                    source_refs=[source],
                    homeowner_explanation="A source readiness view was not available for this home.",
                    contractor_readiness_prompt="Rebuild source readiness context before using this workflow readiness view.",
                )
                for source in unavailable_sources
            ]
            source_basis = self._basis(
                source_refs=[section.section_key for section in context.sections],
                unavailable_source_refs=unavailable_sources,
                basis_quality="source_unavailable_for_contractor_workflow_readiness",
            )
            lane = self._lane(
                lane_id=ContractorWorkflowLaneId.planning_review,
                lane_label="Planning review",
                blocker_records=blockers,
                source_basis=source_basis,
                reason_available="Source context is available.",
                reason_blocked="One or more source readiness views were unavailable.",
                homeowner_summary="Contractor workflow readiness could not be assembled from all source views.",
                contractor_readiness_prompt="Review source availability before using this view.",
                unavailable_count=len(unavailable_sources),
            )
            summary = ContractorWorkflowReadinessSummary(
                overall_status=ContractorWorkflowReadinessStatus.unavailable,
                confidence_level=ConfidenceLevel.low,
                lane_count=1,
                blocked_or_deferred_lane_count=1,
                blocker_count=len(blockers),
                summary_boundary_note="Contractor workflow readiness is source-limited and not authority-bearing.",
            )
            return ContractorWorkflowReadinessView(
                home_id=home_id,
                implementation_boundary="Read-only Phase 11A contractor workflow readiness view. It assembles source readiness metadata only.",
                workflow_scope=ContractorWorkflowScope(limitations=CONTRACTOR_WORKFLOW_LIMITATIONS),
                summary=summary,
                readiness_lanes=[lane],
                blockers=blockers,
                homeowner_summary="Contractor workflow readiness is unavailable because source readiness metadata is incomplete.",
                contractor_summary="Source readiness metadata is unavailable for this home.",
                contractor_readiness_prompts=[lane.contractor_readiness_prompt],
                source_basis=source_basis,
                blocker_category_counts=dict(Counter(blocker.category.value for blocker in blockers)),
                assumptions=["A home record exists, but one or more source views were unavailable."],
                limitations=CONTRACTOR_WORKFLOW_LIMITATIONS,
                deferred_boundaries=sorted(CONTRACTOR_WORKFLOW_DEFERRED_BOUNDARIES),
                compatibility_note="Existing Phase 5, Phase 6, Phase 9, and Phase 10 routes remain unchanged.",
            )

        lanes = [
            self._planning_lane(contractor_context, planning_exchange, install_complexity),
            self._missing_input_lane(contractor_context, estimate_view, proposal_view),
            self._confirmation_gate_lane(gate_view, estimate_view),
            self._option_candidate_lane(proposal_view),
            self._proposal_prep_lane(proposal_view, estimate_view),
        ]
        blockers = sorted(
            [blocker for lane in lanes for blocker in lane.blockers],
            key=lambda blocker: blocker.blocker_id,
        )
        missing_inputs = self._sorted_unique(
            [missing for lane in lanes for missing in lane.missing_inputs]
        )
        confirmation_gate_ids = self._sorted_unique(
            [gate for lane in lanes for gate in lane.confirmation_gate_ids]
        )
        option_candidate_refs = self._sorted_unique(
            [candidate for lane in lanes for candidate in lane.option_candidate_refs]
        )
        dependency_refs = self._sorted_unique(
            [dependency for lane in lanes for dependency in lane.dependency_refs]
        )
        if any(lane.status == ContractorWorkflowReadinessStatus.unavailable for lane in lanes):
            overall_status = ContractorWorkflowReadinessStatus.unavailable
            confidence_level = ConfidenceLevel.low
        elif any(lane.status == ContractorWorkflowReadinessStatus.blocked_or_deferred for lane in lanes):
            overall_status = ContractorWorkflowReadinessStatus.blocked_or_deferred
            confidence_level = ConfidenceLevel.low
        elif any(lane.status == ContractorWorkflowReadinessStatus.review_limited for lane in lanes):
            overall_status = ContractorWorkflowReadinessStatus.review_limited
            confidence_level = ConfidenceLevel.medium
        else:
            overall_status = ContractorWorkflowReadinessStatus.review_context_available
            confidence_level = ConfidenceLevel.medium

        source_basis = self._basis(
            source_refs=[section.section_key for section in context.sections],
            contractor_context_refs=[item.item_id for item in contractor_context.next_safe_contractor_review_prompts],
            planning_exchange_refs=[mapping.section_key for mapping in planning_exchange.section_mappings],
            estimate_readiness_refs=["EstimateReadinessView"],
            proposal_option_set_refs=option_candidate_refs,
            compatibility_path_refs=proposal_view.source_basis.compatibility_path_refs,
            takeoff_line_refs=proposal_view.source_basis.takeoff_line_refs,
            blocker_refs=[blocker.blocker_id for blocker in blockers],
            missing_input_refs=missing_inputs,
            confirmation_gate_refs=confirmation_gate_ids,
            option_candidate_refs=option_candidate_refs,
            dependency_refs=dependency_refs,
            assumption_refs=["phase_11a_readiness_lanes_are_derived_from_existing_views"],
            deferred_boundary_refs=CONTRACTOR_WORKFLOW_DEFERRED_BOUNDARIES,
            basis_quality="home_level_phase_11a_contractor_workflow_readiness_rollup",
        )
        summary = ContractorWorkflowReadinessSummary(
            overall_status=overall_status,
            confidence_level=confidence_level,
            lane_count=len(lanes),
            blocked_or_deferred_lane_count=sum(
                1
                for lane in lanes
                if lane.status in {
                    ContractorWorkflowReadinessStatus.blocked_or_deferred,
                    ContractorWorkflowReadinessStatus.unavailable,
                }
            ),
            blocker_count=len(blockers),
            missing_input_count=len(missing_inputs),
            confirmation_gate_count=len(confirmation_gate_ids),
            option_candidate_count=len(option_candidate_refs),
            workflow_ready_for_read_only_review=True,
            contractor_review_required=True,
            summary_boundary_note=(
                "Contractor workflow readiness is a read-only organization layer. It is not a quote, not an approval, "
                "not a final estimate, not a final design, not a final proposal, not an assignment, not an account, "
                "not an export, and not a source record change."
            ),
        )
        return ContractorWorkflowReadinessView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 11A contractor workflow readiness view built request-time from existing Phase 5 contractor "
                "context, Phase 6 planning exchange, Phase 9 estimate readiness, and Phase 10 proposal option-set metadata. "
                "Phase 7 and Phase 8 basis is carried only where existing source contracts already surface it. This endpoint "
                "does not write data, persist workflow state, run migrations, enforce permissions, create contractor accounts, "
                "create assignments, create accept/complete states, create exports, automate CRM or email, calculate prices, "
                "create quotes, generate proposals, produce final estimates, produce final designs, change source records, "
                "create twin_id, create graph behavior, or create operational behavior."
            ),
            workflow_scope=ContractorWorkflowScope(limitations=CONTRACTOR_WORKFLOW_LIMITATIONS),
            summary=summary,
            readiness_lanes=lanes,
            blockers=blockers,
            missing_inputs=missing_inputs,
            confirmation_gate_ids=confirmation_gate_ids,
            option_candidate_refs=option_candidate_refs,
            dependency_refs=dependency_refs,
            homeowner_summary=(
                "Contractor workflow readiness organizes what may need review before contractor preparation can rely on the planning context."
            ),
            contractor_summary=(
                f"Contractor workflow readiness status is {overall_status.value}. "
                f"{len(lanes)} readiness lanes, {len(blockers)} blockers, {len(missing_inputs)} missing inputs, "
                f"{len(confirmation_gate_ids)} gate topics, and {len(option_candidate_refs)} option candidates are present."
            ),
            contractor_readiness_prompts=[lane.contractor_readiness_prompt for lane in lanes],
            source_basis=source_basis,
            blocker_category_counts=dict(sorted(Counter(blocker.category.value for blocker in blockers).items())),
            assumptions=[
                "Readiness lanes are fixed and sorted in a deterministic order.",
                "Existing source views are authoritative over this organizing layer.",
                "This endpoint creates no contractor-held state and no source record changes.",
            ],
            limitations=CONTRACTOR_WORKFLOW_LIMITATIONS,
            deferred_boundaries=sorted(CONTRACTOR_WORKFLOW_DEFERRED_BOUNDARIES),
            compatibility_note=(
                "Existing contractor-context, planning-exchange, estimate-readiness, proposal-option-set, twin-planning-context, "
                "scenario, takeoff, and estimate-placeholder routes remain unchanged."
            ),
        )


contractor_workflow_service = ContractorWorkflowService()

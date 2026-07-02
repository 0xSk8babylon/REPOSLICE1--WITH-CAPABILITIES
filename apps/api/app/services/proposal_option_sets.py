from collections import Counter
from typing import Dict, List, Optional, Tuple

from app.core.repository import repository
from app.core.types import ConfidenceLevel
from app.estimate_readiness.schemas import EstimateReadinessStatus
from app.proposal_option_sets.schemas import (
    ProposalOptionAudienceSummary,
    ProposalOptionCandidate,
    ProposalOptionSetBasis,
    ProposalOptionSetBlocker,
    ProposalOptionSetBlockerCategory,
    ProposalOptionSetScope,
    ProposalOptionSetsSummary,
    ProposalOptionSetStatus,
    ProposalOptionSetsView,
)

PROPOSAL_OPTION_SET_LIMITATIONS = [
    "Proposal option sets are read-only planning readiness metadata only.",
    "They do not generate proposals, prices, quotes, bids, sales copy, savings, payback, financing, incentives, or final estimates.",
    "They do not recommend products, rank options, choose a selected design, procure equipment, create CRM workflow, export packets, create PDFs, share links, or send email.",
    "They do not perform or approve final electrical design, wire sizing, conduit sizing, breaker sizing, disconnect requirements, bill of materials, permit design, AHJ approval, utility approval, contractor approval, or field verification.",
    "Audience summaries are wording metadata only and are not permission-enforced views.",
]

PROPOSAL_OPTION_SET_DEFERRED_BOUNDARIES = [
    "ahj_approval",
    "auth",
    "best_option_selection",
    "bid_logic",
    "contractor_approval",
    "crm_workflow",
    "email_automation",
    "exports",
    "field_verification",
    "final_bill_of_materials",
    "final_design",
    "final_disconnect_requirements",
    "final_estimate",
    "final_proposal",
    "final_wire_conduit_breaker_sizing",
    "financing",
    "incentives",
    "migrations",
    "pdf_generation",
    "permission_enforcement",
    "persistence",
    "pricing",
    "procurement",
    "product_recommendations",
    "proposal_generation",
    "quote_generation",
    "ranking",
    "savings_payback",
    "share_links",
    "twin_id",
    "utility_approval",
    "write_endpoints",
]


class ProposalOptionSetsService:
    def _sorted_unique(self, values: List[str]) -> List[str]:
        return sorted({value for value in values if value})

    def _basis(
        self,
        *,
        source_refs: Optional[List[str]] = None,
        scenario_refs: Optional[List[str]] = None,
        design_refs: Optional[List[str]] = None,
        proposal_readiness_refs: Optional[List[str]] = None,
        planning_exchange_refs: Optional[List[str]] = None,
        compatibility_path_refs: Optional[List[str]] = None,
        takeoff_line_refs: Optional[List[str]] = None,
        estimate_gate_refs: Optional[List[str]] = None,
        estimate_blocker_refs: Optional[List[str]] = None,
        missing_input_refs: Optional[List[str]] = None,
        dependency_refs: Optional[List[str]] = None,
        assumption_refs: Optional[List[str]] = None,
        deferred_boundary_refs: Optional[List[str]] = None,
        basis_quality: str = "request_time_derived_from_existing_phase_3m_and_phase_6_9_views",
    ) -> ProposalOptionSetBasis:
        return ProposalOptionSetBasis(
            source_views=[
                "TwinProposalReadinessFoundationView",
                "PlanningExchangeObjectView",
                "TwinSharedCompatibilityView",
                "TwinTopologyTakeoffView",
                "EstimateReadinessView",
                "Scenario",
                "EnergySystemDesign",
            ],
            source_fields=[
                "TwinProposalReadinessFoundationView.readiness_items",
                "PlanningExchangeObjectView.section_mappings",
                "PlanningExchangeObjectView.readiness_summary",
                "TwinSharedCompatibilityView.compatibility_paths",
                "TwinTopologyTakeoffView.line_items",
                "TwinTopologyTakeoffView.missing_information",
                "EstimateReadinessView.scenario_statuses",
                "EstimateReadinessView.confirmation_gates",
                "EstimateReadinessView.blockers",
                "Scenario.id",
                "Scenario.linked_design_id",
                "EnergySystemDesign.id",
            ],
            source_refs=self._sorted_unique(source_refs or []),
            scenario_refs=self._sorted_unique(scenario_refs or []),
            design_refs=self._sorted_unique(design_refs or []),
            proposal_readiness_refs=self._sorted_unique(proposal_readiness_refs or []),
            planning_exchange_refs=self._sorted_unique(planning_exchange_refs or []),
            compatibility_path_refs=self._sorted_unique(compatibility_path_refs or []),
            takeoff_line_refs=self._sorted_unique(takeoff_line_refs or []),
            estimate_gate_refs=self._sorted_unique(estimate_gate_refs or []),
            estimate_blocker_refs=self._sorted_unique(estimate_blocker_refs or []),
            missing_input_refs=self._sorted_unique(missing_input_refs or []),
            dependency_refs=self._sorted_unique(dependency_refs or []),
            assumption_refs=self._sorted_unique(assumption_refs or []),
            deferred_boundary_refs=self._sorted_unique(deferred_boundary_refs or []),
            basis_quality=basis_quality,
            request_time_derived=True,
            verified_fact_claim_present=False,
            limitations=PROPOSAL_OPTION_SET_LIMITATIONS,
        )

    def _status_from_estimate_readiness(
        self, estimate_status: str, blocker_count: int, missing_input_count: int
    ) -> Tuple[ProposalOptionSetStatus, ConfidenceLevel]:
        if blocker_count or missing_input_count:
            return ProposalOptionSetStatus.not_ready, ConfidenceLevel.low
        if estimate_status == EstimateReadinessStatus.ready_for_estimate.value:
            return ProposalOptionSetStatus.ready_for_contractor_review_metadata, ConfidenceLevel.medium
        return ProposalOptionSetStatus.review_required, ConfidenceLevel.medium

    def _blockers_for_candidate(self, scenario_status, estimate_view) -> List[ProposalOptionSetBlocker]:
        blockers: List[ProposalOptionSetBlocker] = []
        for category in scenario_status.blocker_categories:
            blockers.append(
                ProposalOptionSetBlocker(
                    blocker_id=f"scenario:{scenario_status.scenario_id}:estimate_blocker:{category}",
                    category=ProposalOptionSetBlockerCategory.estimate_readiness_blocker,
                    severity="blocker",
                    source_refs=[f"scenario:{scenario_status.scenario_id}"],
                    gate_refs=scenario_status.required_gate_ids,
                    missing_inputs=scenario_status.missing_inputs,
                    homeowner_explanation=(
                        "This option candidate needs more review information before it can support proposal preparation."
                    ),
                    contractor_review_note=(
                        "Review prompt only: estimate-readiness blocker category "
                        f"'{category}' is still present for this scenario context."
                    ),
                )
            )
        if scenario_status.missing_inputs:
            blockers.append(
                ProposalOptionSetBlocker(
                    blocker_id=f"scenario:{scenario_status.scenario_id}:missing_inputs",
                    category=ProposalOptionSetBlockerCategory.missing_input,
                    severity="blocker",
                    source_refs=[f"scenario:{scenario_status.scenario_id}"],
                    missing_inputs=scenario_status.missing_inputs,
                    homeowner_explanation=(
                        "This option candidate is missing planning information needed before proposal preparation."
                    ),
                    contractor_review_note=(
                        "Review prompt only: missing inputs remain unresolved in the current readiness context."
                    ),
                )
            )
        open_gate_ids = [
            gate.gate_id
            for gate in estimate_view.confirmation_gates
            if gate.gate_id in scenario_status.required_gate_ids and gate.status.value != "confirmed"
        ]
        for gate_id in open_gate_ids:
            blockers.append(
                ProposalOptionSetBlocker(
                    blocker_id=f"scenario:{scenario_status.scenario_id}:open_gate:{gate_id}",
                    category=ProposalOptionSetBlockerCategory.confirmation_gate_open,
                    severity="review_required",
                    source_refs=[f"scenario:{scenario_status.scenario_id}"],
                    gate_refs=[gate_id],
                    homeowner_explanation=(
                        "This option candidate still has review gates that need to be resolved before proposal preparation."
                    ),
                    contractor_review_note=(
                        f"Review prompt only: confirmation gate '{gate_id}' is open in the Phase 9 readiness context."
                    ),
                )
            )
        if estimate_view.estimate_allowed is False:
            blockers.append(
                ProposalOptionSetBlocker(
                    blocker_id=f"scenario:{scenario_status.scenario_id}:pricing_deferred",
                    category=ProposalOptionSetBlockerCategory.pricing_deferred,
                    severity="deferred",
                    source_refs=[f"scenario:{scenario_status.scenario_id}", "estimate_readiness"],
                    homeowner_explanation=(
                        "Pricing is not available from this planning view."
                    ),
                    contractor_review_note=(
                        "Review prompt only: contractor pricing remains outside this API response."
                    ),
                )
            )
        return blockers

    def _homeowner_summary(
        self,
        *,
        scenario_name: str,
        status: ProposalOptionSetStatus,
        blocker_count: int,
        missing_input_count: int,
    ) -> ProposalOptionAudienceSummary:
        if status == ProposalOptionSetStatus.ready_for_contractor_review_metadata:
            summary = f"{scenario_name} has enough readiness metadata for contractor review preparation."
        elif status == ProposalOptionSetStatus.review_required:
            summary = f"{scenario_name} needs review before it can support proposal preparation."
        else:
            summary = (
                f"{scenario_name} is missing planning details before it can support proposal preparation. "
                f"Current blockers: {blocker_count}; missing inputs: {missing_input_count}."
            )
        return ProposalOptionAudienceSummary(
            audience="homeowner",
            summary=summary,
            hidden_or_deferred_details=[
                "pricing",
                "proposal_generation",
                "authority_review",
            ],
            limitations=PROPOSAL_OPTION_SET_LIMITATIONS,
        )

    def _candidate(
        self,
        scenario,
        *,
        design_by_id: Dict[str, object],
        scenario_status,
        estimate_view,
        proposal_readiness_view,
        planning_exchange,
    ) -> ProposalOptionCandidate:
        design = design_by_id.get(scenario.linked_design_id)
        candidate_blockers = self._blockers_for_candidate(scenario_status, estimate_view)
        status, confidence_level = self._status_from_estimate_readiness(
            scenario_status.status.value,
            len(candidate_blockers),
            len(scenario_status.missing_inputs),
        )
        scenario_ref = f"scenario:{scenario.id}"
        design_ref = f"design:{scenario.linked_design_id}" if scenario.linked_design_id else ""
        compatibility_path_refs = self._sorted_unique(
            scenario_status.basis.compatibility_path_refs
            + estimate_view.source_basis.compatibility_path_refs
        )
        takeoff_line_refs = self._sorted_unique(
            scenario_status.basis.takeoff_line_refs
            + estimate_view.source_basis.takeoff_line_refs
        )
        estimate_blocker_refs = [blocker.blocker_id for blocker in estimate_view.blockers]
        proposal_readiness_refs = [
            item.readiness_area.value for item in proposal_readiness_view.readiness_items
        ]
        planning_exchange_refs = [mapping.section_key for mapping in planning_exchange.section_mappings]
        dependency_refs = self._sorted_unique(
            scenario_status.complexity_flags
            + compatibility_path_refs
            + takeoff_line_refs
            + scenario_status.required_gate_ids
        )
        basis = self._basis(
            source_refs=[scenario_ref, design_ref],
            scenario_refs=[scenario_ref],
            design_refs=[design_ref],
            proposal_readiness_refs=proposal_readiness_refs,
            planning_exchange_refs=planning_exchange_refs,
            compatibility_path_refs=compatibility_path_refs,
            takeoff_line_refs=takeoff_line_refs,
            estimate_gate_refs=scenario_status.required_gate_ids,
            estimate_blocker_refs=estimate_blocker_refs,
            missing_input_refs=scenario_status.missing_inputs,
            dependency_refs=dependency_refs,
            assumption_refs=["scenario_status_derived_from_home_level_readiness"],
            deferred_boundary_refs=PROPOSAL_OPTION_SET_DEFERRED_BOUNDARIES,
            basis_quality="candidate_assembled_from_scenario_design_and_phase_3m_6_9_readiness",
        )
        return ProposalOptionCandidate(
            option_candidate_id=f"proposal_option_candidate:{scenario.id}",
            scenario_id=scenario.id,
            scenario_name=scenario.name,
            linked_design_id=scenario.linked_design_id,
            linked_design_name=getattr(design, "name", None),
            status=status,
            confidence_level=confidence_level,
            estimate_readiness_status=scenario_status.status.value,
            proposal_readiness_posture=(
                proposal_readiness_view.proposal_readiness_posture[0].posture
                if proposal_readiness_view.proposal_readiness_posture
                else "proposal_readiness_context_unavailable"
            ),
            contractor_review_required=True,
            proposal_allowed=False,
            source_basis=basis,
            blockers=candidate_blockers,
            blocker_categories=self._sorted_unique([blocker.category.value for blocker in candidate_blockers]),
            missing_inputs=scenario_status.missing_inputs,
            confirmation_gate_ids=scenario_status.required_gate_ids,
            dependency_refs=dependency_refs,
            assumptions=[
                "Candidate is assembled from an existing scenario and linked design context.",
                "Scenario readiness is inherited from Phase 9 home-level estimate readiness metadata.",
                "Structured planning records and existing derived views are authoritative over generated text.",
            ],
            homeowner_summary=self._homeowner_summary(
                scenario_name=scenario.name,
                status=status,
                blocker_count=len(candidate_blockers),
                missing_input_count=len(scenario_status.missing_inputs),
            ),
            contractor_review_notes=[
                "Review prompt only: compare scenario context with current confirmation gates before proposal preparation.",
                "Review prompt only: verify product/spec, topology, route, and authority-dependent inputs outside this response.",
                "Review prompt only: use this candidate as planning metadata, not as authorization or instructions.",
            ],
            deferred_boundaries=sorted(PROPOSAL_OPTION_SET_DEFERRED_BOUNDARIES),
            limitations=PROPOSAL_OPTION_SET_LIMITATIONS,
        )

    def _fallback_candidate_for_scenario(
        self,
        scenario,
        *,
        design_by_id: Dict[str, object],
        proposal_readiness_view,
        planning_exchange,
        estimate_view,
    ) -> ProposalOptionCandidate:
        design = design_by_id.get(scenario.linked_design_id)
        scenario_ref = f"scenario:{scenario.id}"
        design_ref = f"design:{scenario.linked_design_id}" if scenario.linked_design_id else ""
        missing_inputs = estimate_view.missing_inputs
        blockers = [
            ProposalOptionSetBlocker(
                blocker_id=f"scenario:{scenario.id}:estimate_status_missing",
                category=ProposalOptionSetBlockerCategory.proposal_prerequisite_missing,
                severity="review_required",
                source_refs=[scenario_ref],
                missing_inputs=missing_inputs,
                homeowner_explanation=(
                    "This option candidate does not have scenario-specific estimate readiness metadata."
                ),
                contractor_review_note=(
                    "Review prompt only: scenario-specific readiness was not available; use home-level readiness context only."
                ),
            )
        ]
        return ProposalOptionCandidate(
            option_candidate_id=f"proposal_option_candidate:{scenario.id}",
            scenario_id=scenario.id,
            scenario_name=scenario.name,
            linked_design_id=scenario.linked_design_id,
            linked_design_name=getattr(design, "name", None),
            status=ProposalOptionSetStatus.review_required,
            confidence_level=ConfidenceLevel.low,
            estimate_readiness_status="scenario_estimate_readiness_unavailable",
            proposal_readiness_posture=(
                proposal_readiness_view.proposal_readiness_posture[0].posture
                if proposal_readiness_view.proposal_readiness_posture
                else "proposal_readiness_context_unavailable"
            ),
            contractor_review_required=True,
            proposal_allowed=False,
            source_basis=self._basis(
                source_refs=[scenario_ref, design_ref],
                scenario_refs=[scenario_ref],
                design_refs=[design_ref],
                planning_exchange_refs=[mapping.section_key for mapping in planning_exchange.section_mappings],
                compatibility_path_refs=estimate_view.source_basis.compatibility_path_refs,
                takeoff_line_refs=estimate_view.source_basis.takeoff_line_refs,
                missing_input_refs=missing_inputs,
                deferred_boundary_refs=PROPOSAL_OPTION_SET_DEFERRED_BOUNDARIES,
                basis_quality="candidate_missing_scenario_specific_estimate_status",
            ),
            blockers=blockers,
            blocker_categories=[ProposalOptionSetBlockerCategory.proposal_prerequisite_missing.value],
            missing_inputs=missing_inputs,
            confirmation_gate_ids=[gate.gate_id for gate in estimate_view.confirmation_gates],
            dependency_refs=[],
            assumptions=[
                "Candidate has scenario/design identity but lacks scenario-specific Phase 9 readiness mapping.",
            ],
            homeowner_summary=self._homeowner_summary(
                scenario_name=scenario.name,
                status=ProposalOptionSetStatus.review_required,
                blocker_count=len(blockers),
                missing_input_count=len(missing_inputs),
            ),
            contractor_review_notes=[
                "Review prompt only: scenario-specific estimate readiness was unavailable for this candidate.",
            ],
            deferred_boundaries=sorted(PROPOSAL_OPTION_SET_DEFERRED_BOUNDARIES),
            limitations=PROPOSAL_OPTION_SET_LIMITATIONS,
        )

    def _overall_status(
        self,
        candidates: List[ProposalOptionCandidate],
    ) -> Tuple[ProposalOptionSetStatus, ConfidenceLevel]:
        if not candidates:
            return ProposalOptionSetStatus.not_ready, ConfidenceLevel.low
        if any(candidate.status == ProposalOptionSetStatus.not_ready for candidate in candidates):
            return ProposalOptionSetStatus.not_ready, ConfidenceLevel.low
        if all(
            candidate.status == ProposalOptionSetStatus.ready_for_contractor_review_metadata
            for candidate in candidates
        ):
            return ProposalOptionSetStatus.ready_for_contractor_review_metadata, ConfidenceLevel.medium
        return ProposalOptionSetStatus.review_required, ConfidenceLevel.medium

    def build_home_proposal_option_sets(self, db, home_id: str) -> Optional[ProposalOptionSetsView]:
        from app.services.estimate_readiness import estimate_readiness_service
        from app.services.planning_exchange import planning_exchange_service
        from app.services.twin_planning_context import twin_planning_context_service

        context = twin_planning_context_service.build(db, home_id)
        if context is None:
            return None
        proposal_readiness_view = twin_planning_context_service.build_proposal_readiness_foundation_view(db, home_id)
        planning_exchange = planning_exchange_service.build_planning_exchange_object(db, home_id)
        estimate_view = estimate_readiness_service.build_home_estimate_readiness(db, home_id)
        if (
            proposal_readiness_view is None
            or planning_exchange is None
            or estimate_view is None
        ):
            return None

        scenario_models = [
            scenario for scenario in repository.list_scenario_models(db) if scenario.home_id == home_id
        ]
        design_by_id = {
            design.id: design
            for design in repository.list_designs(db)
            if design.home_id == home_id
        }
        scenario_status_by_id = {
            scenario_status.scenario_id: scenario_status
            for scenario_status in estimate_view.scenario_statuses
        }
        candidates = []
        for scenario in scenario_models:
            scenario_status = scenario_status_by_id.get(scenario.id)
            if scenario_status is None:
                candidates.append(
                    self._fallback_candidate_for_scenario(
                        scenario,
                        design_by_id=design_by_id,
                        proposal_readiness_view=proposal_readiness_view,
                        planning_exchange=planning_exchange,
                        estimate_view=estimate_view,
                    )
                )
                continue
            candidates.append(
                self._candidate(
                    scenario,
                    design_by_id=design_by_id,
                    scenario_status=scenario_status,
                    estimate_view=estimate_view,
                    proposal_readiness_view=proposal_readiness_view,
                    planning_exchange=planning_exchange,
                )
            )
        candidates = sorted(candidates, key=lambda candidate: candidate.scenario_id)
        blockers = [
            blocker
            for candidate in candidates
            for blocker in candidate.blockers
        ]
        missing_inputs = self._sorted_unique(
            estimate_view.missing_inputs
            + [missing for candidate in candidates for missing in candidate.missing_inputs]
        )
        confirmation_gate_ids = self._sorted_unique(
            [gate.gate_id for gate in estimate_view.confirmation_gates]
            + [gate for candidate in candidates for gate in candidate.confirmation_gate_ids]
        )
        dependency_refs = self._sorted_unique(
            [dependency for candidate in candidates for dependency in candidate.dependency_refs]
        )
        overall_status, confidence_level = self._overall_status(candidates)
        blocker_category_counts = Counter(blocker.category.value for blocker in blockers)
        source_basis = self._basis(
            source_refs=[section.section_key for section in context.sections],
            scenario_refs=[f"scenario:{scenario.id}" for scenario in scenario_models],
            design_refs=[f"design:{design_id}" for design_id in design_by_id],
            proposal_readiness_refs=[item.readiness_area.value for item in proposal_readiness_view.readiness_items],
            planning_exchange_refs=[mapping.section_key for mapping in planning_exchange.section_mappings],
            compatibility_path_refs=estimate_view.source_basis.compatibility_path_refs,
            takeoff_line_refs=estimate_view.source_basis.takeoff_line_refs,
            estimate_gate_refs=confirmation_gate_ids,
            estimate_blocker_refs=[blocker.blocker_id for blocker in estimate_view.blockers],
            missing_input_refs=missing_inputs,
            dependency_refs=dependency_refs,
            assumption_refs=[
                "phase_10_option_candidates_derive_from_existing_scenarios",
                "proposal_generation_deferred",
            ],
            deferred_boundary_refs=PROPOSAL_OPTION_SET_DEFERRED_BOUNDARIES,
            basis_quality="home_level_phase_10_proposal_option_set_rollup",
        )
        summary = ProposalOptionSetsSummary(
            overall_status=overall_status,
            confidence_level=confidence_level,
            option_candidate_count=len(candidates),
            candidates_requiring_review_count=sum(
                1 for candidate in candidates if candidate.contractor_review_required
            ),
            blocker_count=len(blockers),
            missing_input_count=len(missing_inputs),
            confirmation_gate_count=len(confirmation_gate_ids),
            proposal_allowed=False,
            contractor_review_required=True,
            summary_boundary_note=(
                "Proposal option sets are planning readiness candidates only. They are not proposals, prices, quotes, bids, "
                "selected options, final estimates, final bills of materials, authority approvals, or permission-enforced views."
            ),
        )
        return ProposalOptionSetsView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 10 proposal option sets view built request-time from existing Phase 3M proposal readiness, "
                "Phase 6 planning exchange, Phase 7 shared compatibility, Phase 8 topology takeoff, Phase 9 estimate readiness, "
                "and scenario/design records. It assembles proposal option-set readiness candidates only; it does not write data, "
                "persist state, run migrations, enforce permissions, create auth/security behavior, send email, export packets, "
                "generate proposals, calculate prices, create quotes or bids, rank options, choose a selected option, recommend products, "
                "produce final estimates, produce final bills of materials, approve contractor review, approve NEC/code compliance, "
                "or imply AHJ/utility approval."
            ),
            option_set_scope=ProposalOptionSetScope(limitations=PROPOSAL_OPTION_SET_LIMITATIONS),
            summary=summary,
            option_candidates=candidates,
            blockers=blockers,
            missing_inputs=missing_inputs,
            confirmation_gate_ids=confirmation_gate_ids,
            dependency_refs=dependency_refs,
            homeowner_summary=(
                "Proposal option-set candidates show which existing scenarios still need review before proposal preparation."
            ),
            contractor_summary=(
                f"Proposal option-set readiness status is {overall_status.value}. "
                f"{len(candidates)} candidates, {len(blockers)} blockers, and {len(missing_inputs)} missing inputs are present. "
                "Treat these as review prompts only."
            ),
            source_basis=source_basis,
            blocker_category_counts=dict(sorted(blocker_category_counts.items())),
            assumptions=[
                "Option candidates are assembled from existing scenario records and linked design context.",
                "Phase 9 readiness is used as precondition metadata only, not as an estimate or proposal approval.",
                "No scenario-specific pricing, package generation, product recommendation, or design selection engine exists.",
                "Structured planning records and existing derived views are authoritative over generated text.",
            ],
            limitations=PROPOSAL_OPTION_SET_LIMITATIONS,
            deferred_boundaries=sorted(PROPOSAL_OPTION_SET_DEFERRED_BOUNDARIES),
            compatibility_note=(
                "Existing TwinPlanningContext, planning-exchange, shared-compatibility, topology-takeoff, estimate-readiness, "
                "scenario, takeoff, and estimate-placeholder routes remain unchanged; this is an additive Phase 10 GET surface."
            ),
        )


proposal_option_sets_service = ProposalOptionSetsService()

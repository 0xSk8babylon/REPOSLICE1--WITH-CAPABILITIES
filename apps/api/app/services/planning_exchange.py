from typing import List, Optional

from app.contractor_context.schemas import ContractorContextItem
from app.services.contractor_context import contractor_context_service
from app.services.twin_planning_context import twin_planning_context_service
from app.planning_exchange.schemas import (
    PlanningExchangeObjectView,
    PlanningExchangeReadinessItem,
    PlanningExchangeReadinessPosture,
    PlanningExchangeReadinessSummary,
    PlanningExchangeReviewPrompt,
    PlanningExchangeSectionMapping,
    PlanningExchangeScope,
    PlanningExchangeSourceBasis,
    PlanningExchangeTrustCategory,
)


PLANNING_EXCHANGE_LIMITATIONS = [
    "Planning exchange object is a read-only derived planning package for participant review only.",
    "It is not a source of truth, export, PDF, share link, permission grant, authorization layer, bid, proposal, quote, CRM workflow, or work directive.",
    "It does not calculate or approve final wire size, conduit size, breaker size, disconnect requirements, NEC/code-compliant installation design, AHJ approval, utility approval, safety approval, or field verification.",
    "Permission-readiness metadata may be visible, but permission enforcement is not implemented.",
]

PLANNING_EXCHANGE_DEFERRED_BOUNDARIES = [
    "auth",
    "contractor_accounts",
    "contractor_ranking",
    "crm_integration",
    "exports",
    "final_breaker_sizing",
    "final_conduit_sizing",
    "final_disconnect_requirements",
    "final_wire_sizing",
    "marketplace_behavior",
    "migrations",
    "payments",
    "pdf_generation",
    "permission_enforcement",
    "persistence",
    "pricing",
    "proposals",
    "share_links",
    "source_of_truth_mutation",
    "twin_id",
    "write_endpoints",
]


class PlanningExchangeService:
    def _sorted_unique(self, values: List[str]) -> List[str]:
        return sorted({value for value in values if value})

    def _source_basis(
        self,
        *,
        source_views: List[str],
        source_fields: List[str],
        source_refs: List[str],
        derived_from: List[str],
        trust_categories: List[PlanningExchangeTrustCategory],
    ) -> PlanningExchangeSourceBasis:
        return PlanningExchangeSourceBasis(
            source_views=self._sorted_unique(source_views),
            source_fields=self._sorted_unique(source_fields),
            source_refs=self._sorted_unique(source_refs),
            derived_from=self._sorted_unique(derived_from),
            trust_categories=sorted(set(trust_categories), key=lambda category: category.value),
            limitations=PLANNING_EXCHANGE_LIMITATIONS,
        )

    def _required_verifiers(self, items: List[ContractorContextItem]) -> List[str]:
        return self._sorted_unique(
            [
                verifier
                for item in items
                for verifier in item.required_verifiers
            ]
        )

    def _review_prompt(
        self,
        *,
        prompt_id: str,
        category: str,
        prompt: str,
        required_verifier: str,
        source_or_basis: str,
        source_mapping_refs: Optional[List[str]] = None,
    ) -> PlanningExchangeReviewPrompt:
        return PlanningExchangeReviewPrompt(
            prompt_id=prompt_id,
            category=category,
            prompt=prompt,
            required_verifier=required_verifier,
            source_or_basis=source_or_basis,
            source_mapping_refs=self._sorted_unique(source_mapping_refs or []),
            limitations=PLANNING_EXCHANGE_LIMITATIONS,
        )

    def _section_mapping(
        self,
        *,
        section_key: str,
        label: str,
        trust_category: PlanningExchangeTrustCategory,
        source_view: str,
        source_fields: List[str],
        source_refs: List[str],
        source_or_basis: str,
        missing_inputs: Optional[List[str]] = None,
        required_verifiers: Optional[List[str]] = None,
        review_prompts: Optional[List[str]] = None,
    ) -> PlanningExchangeSectionMapping:
        return PlanningExchangeSectionMapping(
            section_key=section_key,
            label=label,
            trust_category=trust_category,
            source_view=source_view,
            source_fields=self._sorted_unique(source_fields),
            source_refs=self._sorted_unique(source_refs),
            source_or_basis=source_or_basis,
            missing_inputs=self._sorted_unique(missing_inputs or []),
            required_verifiers=self._sorted_unique(required_verifiers or []),
            review_prompts=self._sorted_unique(review_prompts or []),
            limitations=PLANNING_EXCHANGE_LIMITATIONS,
        )

    def _readiness_item(
        self,
        *,
        readiness_area: str,
        posture: PlanningExchangeReadinessPosture,
        reason: str,
        source_or_basis: str,
        blockers: Optional[List[str]] = None,
        required_verifiers: Optional[List[str]] = None,
        next_review_prompts: Optional[List[str]] = None,
    ) -> PlanningExchangeReadinessItem:
        return PlanningExchangeReadinessItem(
            readiness_area=readiness_area,
            posture=posture,
            reason=reason,
            source_or_basis=source_or_basis,
            blockers=self._sorted_unique(blockers or []),
            required_verifiers=self._sorted_unique(required_verifiers or []),
            next_review_prompts=self._sorted_unique(next_review_prompts or []),
            limitations=PLANNING_EXCHANGE_LIMITATIONS,
        )

    def build_planning_exchange_object(self, db, home_id: str) -> Optional[PlanningExchangeObjectView]:
        context = twin_planning_context_service.build(db, home_id)
        contractor_context = contractor_context_service.build_contractor_planning_context(db, home_id)
        confirmation_gates = contractor_context_service.build_confirmation_gate_projection(db, home_id)
        install_complexity = contractor_context_service.build_install_complexity_view(db, home_id)

        if context is None or contractor_context is None or confirmation_gates is None or install_complexity is None:
            return None

        contractor_items = (
            contractor_context.homeowner_goals
            + contractor_context.home_site_planning_summary
            + contractor_context.known_electrical_equipment_summary
            + contractor_context.proposed_system_context
            + contractor_context.missing_information
            + contractor_context.contractor_verification_needs
            + contractor_context.provenance_trust_notes
            + contractor_context.permission_readiness_notes
            + contractor_context.next_safe_contractor_review_prompts
        )
        required_verifiers = self._sorted_unique(
            self._required_verifiers(contractor_items)
            + [gate.required_verifier for gate in confirmation_gates.gates]
            + [signal.required_verifier for signal in install_complexity.signals]
        )
        review_prompts = [
            self._review_prompt(
                prompt_id=f"exchange_gate_{gate.gate_id}",
                category="confirmation_gate",
                prompt=gate.next_action,
                required_verifier=gate.required_verifier,
                source_or_basis=gate.source_or_basis,
                source_mapping_refs=[gate.gate_id],
            )
            for gate in confirmation_gates.gates
        ] + [
            self._review_prompt(
                prompt_id=f"exchange_signal_{signal.signal_id}",
                category="install_complexity_signal",
                prompt=signal.next_action,
                required_verifier=signal.required_verifier,
                source_or_basis=signal.source_or_basis,
                source_mapping_refs=[signal.signal_id],
            )
            for signal in install_complexity.signals
        ]

        source_refs = (
            [item.item_id for item in contractor_items]
            + [gate.gate_id for gate in confirmation_gates.gates]
            + [signal.signal_id for signal in install_complexity.signals]
            + context.provenance_gaps
            + context.continuity_gaps
        )
        source_basis = self._source_basis(
            source_views=[
                "TwinPlanningContext",
                "ContractorPlanningContextView",
                "ContractorConfirmationGateProjectionView",
                "ContractorInstallComplexityView",
            ],
            source_fields=[
                "TwinPlanningContext.sections",
                "TwinPlanningContext.provenance_gaps",
                "TwinPlanningContext.typed_provenance_gaps",
                "ContractorPlanningContextView.homeowner_goals",
                "ContractorPlanningContextView.home_site_planning_summary",
                "ContractorPlanningContextView.known_electrical_equipment_summary",
                "ContractorPlanningContextView.proposed_system_context",
                "ContractorPlanningContextView.missing_information",
                "ContractorPlanningContextView.contractor_verification_needs",
                "ContractorPlanningContextView.provenance_trust_notes",
                "ContractorPlanningContextView.next_safe_contractor_review_prompts",
                "ContractorConfirmationGateProjectionView.gates",
                "ContractorInstallComplexityView.signals",
            ],
            source_refs=source_refs,
            derived_from=[
                "existing_home_id_anchored_twin_planning_context",
                "phase_5b_contractor_scoped_planning_context",
                "phase_5c_confirmation_gate_projection",
                "phase_5d_install_complexity_signals",
            ],
            trust_categories=[
                PlanningExchangeTrustCategory.app_derived,
                PlanningExchangeTrustCategory.contractor_safe_projection,
                PlanningExchangeTrustCategory.homeowner_provided,
                PlanningExchangeTrustCategory.manufacturer_required_future,
                PlanningExchangeTrustCategory.ahj_utility_dependent_future,
                PlanningExchangeTrustCategory.missing_unknown,
            ],
        )
        manufacturer_gate_refs = [
            gate.gate_id
            for gate in confirmation_gates.gates
            if gate.category == "product_specification"
        ]
        ahj_utility_gate_refs = [
            gate.gate_id
            for gate in confirmation_gates.gates
            if gate.category == "authority_review"
        ]
        missing_inputs = self._sorted_unique(
            [
                missing
                for item in contractor_context.missing_information
                + contractor_context.known_electrical_equipment_summary
                + contractor_context.proposed_system_context
                for missing in item.missing_inputs
            ]
        )
        section_mappings = [
            self._section_mapping(
                section_key="homeowner_intent_goals",
                label="Homeowner intent and goals",
                trust_category=PlanningExchangeTrustCategory.homeowner_provided,
                source_view="ContractorPlanningContextView",
                source_fields=["homeowner_goals"],
                source_refs=[item.item_id for item in contractor_context.homeowner_goals],
                source_or_basis="Recorded homeowner goals carried through contractor-safe planning context.",
                review_prompts=["Review goals as planning context, not a contractor scope of work."],
            ),
            self._section_mapping(
                section_key="home_site_planning_context",
                label="Home and site planning context",
                trust_category=PlanningExchangeTrustCategory.contractor_safe_projection,
                source_view="ContractorPlanningContextView",
                source_fields=["home_site_planning_summary"],
                source_refs=[item.item_id for item in contractor_context.home_site_planning_summary],
                source_or_basis="Minimized contractor-safe projection of existing home/site planning records.",
                review_prompts=["Use site context as a site-walk preparation prompt only."],
            ),
            self._section_mapping(
                section_key="known_electrical_equipment_summary",
                label="Known electrical equipment summary",
                trust_category=PlanningExchangeTrustCategory.contractor_safe_projection,
                source_view="ContractorPlanningContextView",
                source_fields=["known_electrical_equipment_summary"],
                source_refs=[item.item_id for item in contractor_context.known_electrical_equipment_summary],
                source_or_basis="Contractor-safe equipment context requiring field and source-backed verification.",
                required_verifiers=["contractor_or_qualified_professional"],
                review_prompts=["Verify equipment identity, nameplate data, and source-backed specifications."],
            ),
            self._section_mapping(
                section_key="proposed_system_context",
                label="Proposed system context",
                trust_category=PlanningExchangeTrustCategory.app_derived,
                source_view="ContractorPlanningContextView",
                source_fields=["proposed_system_context"],
                source_refs=[item.item_id for item in contractor_context.proposed_system_context],
                source_or_basis="Existing planning context only; not a final design, bid, proposal, or directive.",
                required_verifiers=["contractor_or_qualified_professional"],
                review_prompts=["Review proposed context only after missing information and field conditions are checked."],
            ),
            self._section_mapping(
                section_key="contractor_safe_planning_context",
                label="Contractor-safe planning context",
                trust_category=PlanningExchangeTrustCategory.contractor_safe_projection,
                source_view="ContractorPlanningContextView",
                source_fields=[
                    "homeowner_goals",
                    "home_site_planning_summary",
                    "known_electrical_equipment_summary",
                    "proposed_system_context",
                    "missing_information",
                    "contractor_verification_needs",
                    "provenance_trust_notes",
                    "permission_readiness_notes",
                    "next_safe_contractor_review_prompts",
                ],
                source_refs=[item.item_id for item in contractor_items],
                source_or_basis="Phase 5B contractor-scoped planning context packaged without raw source payload embedding.",
                missing_inputs=missing_inputs,
                required_verifiers=required_verifiers,
                review_prompts=["Treat contractor-safe context as review preparation, not authorization or completed verification."],
            ),
            self._section_mapping(
                section_key="confirmation_gates",
                label="Confirmation gates",
                trust_category=PlanningExchangeTrustCategory.app_derived,
                source_view="ContractorConfirmationGateProjectionView",
                source_fields=["gates"],
                source_refs=[gate.gate_id for gate in confirmation_gates.gates],
                source_or_basis="Phase 5C gates are read-only derived review topics, not persisted gate state.",
                required_verifiers=required_verifiers,
                review_prompts=["Use gates as review prompts; do not treat them as completed verification."],
            ),
            self._section_mapping(
                section_key="install_complexity_uncertainty_signals",
                label="Install complexity and uncertainty signals",
                trust_category=PlanningExchangeTrustCategory.app_derived,
                source_view="ContractorInstallComplexityView",
                source_fields=["signals"],
                source_refs=[signal.signal_id for signal in install_complexity.signals],
                source_or_basis="Phase 5D uncertainty signals are review-burden indicators only.",
                missing_inputs=[
                    missing
                    for signal in install_complexity.signals
                    for missing in signal.missing_inputs
                ],
                required_verifiers=required_verifiers,
                review_prompts=["Use uncertainty signals to plan review effort, not to infer design approval."],
            ),
            self._section_mapping(
                section_key="provenance_trust_basis",
                label="Provenance and trust basis",
                trust_category=PlanningExchangeTrustCategory.app_derived,
                source_view="ContractorPlanningContextView",
                source_fields=["provenance_trust_notes", "source_basis"],
                source_refs=[item.item_id for item in contractor_context.provenance_trust_notes],
                source_or_basis="Provenance and trust notes indicate basis and uncertainty only.",
                review_prompts=["Review source basis and missing provenance before relying on a planning item."],
            ),
            self._section_mapping(
                section_key="missing_information",
                label="Missing information",
                trust_category=PlanningExchangeTrustCategory.missing_unknown,
                source_view="ContractorPlanningContextView",
                source_fields=["missing_information"],
                source_refs=[item.item_id for item in contractor_context.missing_information],
                source_or_basis="Missing information is surfaced for review preparation and does not authorize assumptions.",
                missing_inputs=missing_inputs,
                review_prompts=["Collect or verify missing inputs before treating planning context as review-ready."],
            ),
            self._section_mapping(
                section_key="manufacturer_required_future",
                label="Manufacturer-required future source review",
                trust_category=PlanningExchangeTrustCategory.manufacturer_required_future,
                source_view="ContractorConfirmationGateProjectionView",
                source_fields=["gates.product_specification"],
                source_refs=manufacturer_gate_refs,
                source_or_basis="Manufacturer specs, nameplates, and manuals are required future source checks, not verified facts from this exchange object.",
                required_verifiers=["contractor_or_qualified_professional"],
                review_prompts=["Review manufacturer source documents before product-specific design work."],
            ),
            self._section_mapping(
                section_key="ahj_utility_dependent_future",
                label="AHJ and utility dependent future review",
                trust_category=PlanningExchangeTrustCategory.ahj_utility_dependent_future,
                source_view="ContractorConfirmationGateProjectionView",
                source_fields=["gates.authority_review"],
                source_refs=ahj_utility_gate_refs,
                source_or_basis="AHJ and utility requirements are future external-authority dependencies only.",
                required_verifiers=["contractor_ahj_or_utility"],
                review_prompts=["Treat AHJ and utility requirements as external review dependencies."],
            ),
        ]
        unresolved_gate_refs = [
            gate.gate_id
            for gate in confirmation_gates.gates
            if gate.status in {
                "contractor_review_required",
                "needs_site_visit",
                "ahj_or_utility_dependent",
                "unknown",
            }
        ]
        complexity_blockers = [
            signal.signal_id
            for signal in install_complexity.signals
            if signal.severity in {"high", "blocked", "unknown"}
        ]
        readiness_blockers = self._sorted_unique(
            missing_inputs
            + unresolved_gate_refs
            + complexity_blockers
        )
        readiness_summary = PlanningExchangeReadinessSummary(
            participant_review=self._readiness_item(
                readiness_area="participant_review",
                posture=(
                    PlanningExchangeReadinessPosture.review_limited_by_missing_information
                    if missing_inputs
                    else PlanningExchangeReadinessPosture.ready_for_planning_review
                ),
                reason=(
                    "The exchange package can support bounded participant planning review, but missing information must remain visible."
                    if missing_inputs
                    else "The exchange package has bounded planning context for participant review only."
                ),
                source_or_basis="Phase 6 package sections and Phase 5 contractor-safe planning context.",
                blockers=missing_inputs,
                required_verifiers=required_verifiers,
                next_review_prompts=[
                    "Review package limitations before relying on any planning item.",
                    "Confirm whether missing information affects the intended review purpose.",
                ],
            ),
            contractor_review=self._readiness_item(
                readiness_area="contractor_review",
                posture=PlanningExchangeReadinessPosture.contractor_review_required,
                reason=(
                    "Contractor review remains required because confirmation gates and install-complexity signals are review prompts only."
                ),
                source_or_basis="ContractorConfirmationGateProjectionView.gates and ContractorInstallComplexityView.signals.",
                blockers=unresolved_gate_refs + complexity_blockers,
                required_verifiers=required_verifiers,
                next_review_prompts=[
                    "Use confirmation gates as contractor review prompts.",
                    "Use install complexity signals to identify review burden.",
                ],
            ),
            estimate_readiness=self._readiness_item(
                readiness_area="estimate_readiness_input_review",
                posture=PlanningExchangeReadinessPosture.not_ready_for_estimate_input,
                reason=(
                    "The exchange package is not sufficient for estimating because route, product, field, AHJ/utility, and verifier inputs remain unresolved."
                ),
                source_or_basis="Missing information, confirmation gates, and install-complexity uncertainty signals.",
                blockers=readiness_blockers,
                required_verifiers=required_verifiers,
                next_review_prompts=[
                    "Resolve missing information before estimating.",
                    "Treat estimate use as future scoped work requiring separate approval.",
                ],
            ),
            proposal_option_readiness=self._readiness_item(
                readiness_area="proposal_option_input_review",
                posture=PlanningExchangeReadinessPosture.not_ready_for_proposal_option_input,
                reason=(
                    "The exchange package does not generate or support proposal options because product, pricing, design, and authority dependencies remain deferred."
                ),
                source_or_basis="Phase 6 deferred boundaries and Phase 5 contractor context limitations.",
                blockers=readiness_blockers
                + [
                    "pricing",
                    "proposals",
                    "product_recommendations",
                    "final_electrical_design",
                    "permission_enforcement",
                ],
                required_verifiers=required_verifiers,
                next_review_prompts=[
                    "Do not treat this package as a proposal input without a separate approved scope.",
                    "Keep proposal-option work deferred until product, pricing, design, and authority boundaries are approved.",
                ],
            ),
            overall_posture=(
                PlanningExchangeReadinessPosture.review_limited_by_missing_information
                if readiness_blockers
                else PlanningExchangeReadinessPosture.ready_for_planning_review
            ),
            non_authoritative_note=(
                "Readiness summary describes planning-review posture only; it is not authorization, approval, verification, "
                "estimate readiness certification, proposal readiness certification, or final design readiness."
            ),
            limitations=PLANNING_EXCHANGE_LIMITATIONS,
        )

        return PlanningExchangeObjectView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 6 planning exchange object built request-time from existing TwinPlanningContext "
                "and Phase 5 contractor-context outputs; does not persist an exchange object, write data, enforce "
                "permissions, export data, create PDFs/share links, create accounts, create twin_id, mutate source "
                "truth, generate proposals, price work, rank contractors, integrate CRM, or calculate final electrical design."
            ),
            exchange_scope=PlanningExchangeScope(limitations=PLANNING_EXCHANGE_LIMITATIONS),
            source_basis=source_basis,
            homeowner_intent_goals=contractor_context.homeowner_goals,
            home_site_planning_context=contractor_context.home_site_planning_summary,
            known_electrical_equipment_summary=contractor_context.known_electrical_equipment_summary,
            proposed_system_context=contractor_context.proposed_system_context,
            contractor_safe_planning_context=contractor_items,
            confirmation_gates=confirmation_gates.gates,
            install_complexity_uncertainty_signals=install_complexity.signals,
            provenance_trust_basis=contractor_context.provenance_trust_notes,
            missing_information=contractor_context.missing_information,
            required_verifiers=required_verifiers,
            review_prompts=review_prompts,
            section_mappings=section_mappings,
            readiness_summary=readiness_summary,
            limitations=PLANNING_EXCHANGE_LIMITATIONS,
            deferred_boundaries=sorted(PLANNING_EXCHANGE_DEFERRED_BOUNDARIES),
            compatibility_note=(
                "Existing TwinPlanningContext, Phase 3/4 derived views, and Phase 5 contractor-context responses "
                "remain unchanged; this is an additive planning-exchange GET surface."
            ),
            raw_source_payloads_embedded=False,
            source_payload_refs={
                "twin_planning_context_sections": sorted(section.section_key for section in context.sections),
                "contractor_context_item_ids": self._sorted_unique([item.item_id for item in contractor_items]),
                "confirmation_gate_ids": [gate.gate_id for gate in confirmation_gates.gates],
                "install_complexity_signal_ids": [signal.signal_id for signal in install_complexity.signals],
                "readiness_posture_vocab": [posture.value for posture in PlanningExchangeReadinessPosture],
            },
        )


planning_exchange_service = PlanningExchangeService()

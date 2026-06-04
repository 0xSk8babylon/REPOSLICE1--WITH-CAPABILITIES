from typing import List, Optional

from app.contractor_context.schemas import (
    ContractorConfirmationGate,
    ContractorConfirmationGateProjectionView,
    ContractorContextItem,
    ContractorContextProvenance,
    ContractorContextScope,
    ContractorInstallComplexitySignal,
    ContractorInstallComplexityView,
    ContractorPlanningContextView,
)
from app.services.twin_planning_context import twin_planning_context_service
from app.twin_planning_context.schemas import (
    TwinContractorFacingAdvisoryArea,
    TwinContractorFacingAdvisoryItem,
    TwinRuntimeParticipantRole,
)


CONTRACTOR_CONTEXT_LIMITATIONS = [
    "Contractor context is read-only planning context for scoping and review preparation only.",
    "It is not a contractor portal, permission grant, export, bid, proposal, quote, CRM workflow, or work directive.",
    "It does not calculate or approve final wire size, conduit size, breaker size, disconnect requirements, or code-compliant installation design.",
    "Permission-readiness metadata is visible, but permission enforcement is not implemented.",
]

CONTRACTOR_CONTEXT_DEFERRED_BOUNDARIES = [
    "auth",
    "bid_logic",
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
    "permission_enforcement",
    "persistence",
    "pricing",
    "proposals",
    "source_of_truth_mutation",
    "twin_id",
    "write_endpoints",
]

CONTRACTOR_CONFIRMATION_GATE_LIMITATIONS = [
    "Confirmation gates are read-only derived review topics, not persisted gate state.",
    "Gate titles do not mean the app has performed or approved the underlying engineering review.",
    "Gate status does not imply final approval, compliance, field verification, AHJ approval, utility approval, or contractor completion.",
    "This projection does not calculate final wire size, conduit size, breaker size, disconnect requirements, or code-compliant installation design.",
]

CONTRACTOR_CONFIRMATION_GATES = [
    ("product_specs_verified", "Product specs verified", "product_specification", "contractor_review_required", "contractor_or_qualified_professional", "high"),
    ("nameplate_ratings_verified", "Nameplate ratings verified", "product_specification", "contractor_review_required", "contractor_or_qualified_professional", "high"),
    ("manufacturer_install_manual_reviewed", "Manufacturer install manual reviewed", "product_specification", "contractor_review_required", "contractor_or_qualified_professional", "high"),
    ("circuit_purpose_confirmed", "Circuit purpose confirmed", "load_context", "contractor_review_required", "contractor_or_qualified_professional", "medium"),
    ("load_current_assumptions_confirmed", "Load/current assumptions confirmed", "load_context", "contractor_review_required", "contractor_or_qualified_professional", "high"),
    ("distance_measurements_confirmed", "Distance measurements confirmed", "field_measurement", "needs_site_visit", "contractor_or_qualified_professional", "high"),
    ("conduit_routing_path_confirmed", "Conduit/routing path confirmed", "field_measurement", "needs_site_visit", "contractor_or_qualified_professional", "high"),
    ("indoor_outdoor_wet_location_confirmed", "Indoor/outdoor/wet location confirmed", "site_condition", "needs_site_visit", "contractor_or_qualified_professional", "medium"),
    ("conductor_material_confirmed", "Conductor material confirmed", "material_review", "contractor_review_required", "contractor_or_qualified_professional", "medium"),
    ("raceway_type_confirmed", "Raceway type confirmed", "material_review", "contractor_review_required", "contractor_or_qualified_professional", "medium"),
    ("current_carrying_conductors_confirmed", "Number of current-carrying conductors confirmed", "engineering_review_topic", "contractor_review_required", "contractor_or_qualified_professional", "high"),
    ("derating_factors_applied", "Derating factors applied", "engineering_review_topic", "contractor_review_required", "contractor_or_qualified_professional", "high"),
    ("voltage_drop_reviewed", "Voltage drop reviewed", "engineering_review_topic", "contractor_review_required", "contractor_or_qualified_professional", "medium"),
    ("disconnect_requirements_reviewed", "Disconnect requirements reviewed", "engineering_review_topic", "contractor_review_required", "contractor_or_qualified_professional", "high"),
    ("overcurrent_protection_reviewed", "Overcurrent protection reviewed", "engineering_review_topic", "contractor_review_required", "contractor_or_qualified_professional", "high"),
    ("grounding_bonding_reviewed", "Grounding/bonding reviewed", "engineering_review_topic", "contractor_review_required", "contractor_or_qualified_professional", "high"),
    ("labeling_signage_requirements_reviewed", "Labeling/signage requirements reviewed", "engineering_review_topic", "contractor_review_required", "contractor_or_qualified_professional", "medium"),
    ("utility_ahj_requirements_reviewed", "Utility/AHJ requirements reviewed", "authority_review", "ahj_or_utility_dependent", "contractor_ahj_or_utility", "blocked"),
    ("contractor_final_review_completed", "Contractor final review completed", "final_review", "contractor_review_required", "contractor_or_qualified_professional", "blocked"),
]

CONTRACTOR_INSTALL_COMPLEXITY_LIMITATIONS = [
    "Install complexity signals are read-only derived uncertainty and review-burden signals only.",
    "Signals do not calculate final wire size, conduit size, breaker size, disconnect requirements, or NEC/code-compliant installation design.",
    "Signals do not create contractor directives, bids, proposals, pricing, AHJ approval, utility approval, field verification, or operational readiness.",
]

CONTRACTOR_INSTALL_COMPLEXITY_CATEGORIES = [
    "product_uncertainty",
    "nameplate_uncertainty",
    "panel_service_uncertainty",
    "routing_path_uncertainty",
    "backup_scope_uncertainty",
    "ahj_utility_uncertainty",
    "material_takeoff_uncertainty",
    "field_verification_burden",
    "homeowner_decision_dependency",
    "contractor_review_burden",
]


class ContractorContextService:
    def _sorted_unique(self, values: List[str]) -> List[str]:
        return sorted({value for value in values if value})

    def _provenance(
        self,
        *,
        source_views: Optional[List[str]] = None,
        source_fields: Optional[List[str]] = None,
        source_refs: Optional[List[str]] = None,
        derived_from: Optional[List[str]] = None,
        limitations: Optional[List[str]] = None,
    ) -> ContractorContextProvenance:
        return ContractorContextProvenance(
            source_views=self._sorted_unique(source_views or []),
            source_fields=self._sorted_unique(source_fields or []),
            source_refs=self._sorted_unique(source_refs or []),
            derived_from=self._sorted_unique(derived_from or []),
            limitations=self._sorted_unique(limitations or CONTRACTOR_CONTEXT_LIMITATIONS),
        )

    def _item(
        self,
        *,
        item_id: str,
        category: str,
        statement: str,
        source_or_basis: str,
        provenance: ContractorContextProvenance,
        missing_inputs: Optional[List[str]] = None,
        required_verifiers: Optional[List[str]] = None,
        next_actions: Optional[List[str]] = None,
        limitations: Optional[List[str]] = None,
    ) -> ContractorContextItem:
        return ContractorContextItem(
            item_id=item_id,
            category=category,
            statement=statement,
            source_or_basis=source_or_basis,
            provenance=provenance,
            missing_inputs=self._sorted_unique(missing_inputs or []),
            required_verifiers=self._sorted_unique(required_verifiers or []),
            next_actions=self._sorted_unique(next_actions or []),
            limitations=self._sorted_unique(limitations or CONTRACTOR_CONTEXT_LIMITATIONS),
        )

    def _advisory_item_refs(self, items: List[TwinContractorFacingAdvisoryItem], field_name: str) -> List[str]:
        refs: List[str] = []
        for item in items:
            refs.extend(getattr(item, field_name, []) or [])
        return self._sorted_unique(refs)

    def build_contractor_planning_context(self, db, home_id: str) -> Optional[ContractorPlanningContextView]:
        context = twin_planning_context_service.build(db, home_id)
        if context is None:
            return None

        runtime_view = twin_planning_context_service.build_runtime_projection_view(
            db,
            home_id,
            role=TwinRuntimeParticipantRole.contractor,
        )
        contractor_advisory = twin_planning_context_service.build_contractor_facing_advisory_view(db, home_id)
        energy_goal_reasoning = twin_planning_context_service.build_energy_goal_reasoning_view(db, home_id)
        proposal_readiness = twin_planning_context_service.build_proposal_readiness_foundation_view(db, home_id)

        if runtime_view is None or contractor_advisory is None:
            return None

        source_basis = self._provenance(
            source_views=[
                "TwinPlanningContext",
                "TwinRuntimeProjectionView.contractor",
                "TwinContractorFacingAdvisoryView",
                "TwinEnergyGoalReasoningView",
                "TwinProposalReadinessFoundationView",
            ],
            source_fields=[
                "TwinPlanningContext.sections",
                "TwinRuntimeProjectionView.projection_records",
                "TwinContractorFacingAdvisoryView.advisory_items",
                "TwinContractorFacingAdvisoryView.source_basis",
                "TwinEnergyGoalReasoningView.recorded_homeowner_goals",
                "TwinProposalReadinessFoundationView.contractor_advisory_context_readiness",
            ],
            source_refs=contractor_advisory.source_basis.known_refs
            + contractor_advisory.source_basis.unknown_refs
            + contractor_advisory.source_basis.provenance_refs
            + contractor_advisory.source_basis.permission_refs,
            derived_from=[
                "existing_home_id_anchored_twin_planning_context",
                "existing_contractor_runtime_projection",
                "existing_phase_3j_contractor_facing_advisory",
            ],
        )

        homeowner_goal_refs = []
        if energy_goal_reasoning is not None:
            homeowner_goal_refs = [
                item.statement for item in energy_goal_reasoning.recorded_homeowner_goals
            ]

        home_site_refs = [
            f"{record.section_key}:{record.entity_type}:{record.entity_id or record.label}"
            for record in runtime_view.projection_records
            if record.section_key in {"home", "buildings", "locations"}
        ]
        equipment_refs = [
            f"{record.section_key}:{record.entity_type}:{record.entity_id or record.label}"
            for record in runtime_view.projection_records
            if record.section_key in {"panels", "equipment", "loads"}
        ]
        proposed_system_refs = [
            f"{record.section_key}:{record.entity_type}:{record.entity_id or record.label}"
            for record in runtime_view.projection_records
            if record.section_key in {"designs", "scenarios", "estimated_pathways"}
        ]
        missing_refs = self._advisory_item_refs(
            contractor_advisory.contractor_visible_known_unknown_summary,
            "contractor_visible_unknowns",
        )
        verification_refs = self._advisory_item_refs(
            contractor_advisory.field_verification_needs
            + contractor_advisory.topology_verification_needs
            + contractor_advisory.professional_review_boundaries,
            "field_verification_needs",
        )
        next_prompt_refs = self._advisory_item_refs(
            contractor_advisory.prerequisite_advisory_recommendations,
            "prerequisite_recommendation_refs",
        )

        homeowner_goals = [
            self._item(
                item_id="homeowner_goals",
                category="homeowner_goals",
                statement="Recorded homeowner goals are included as planning context only and do not define a contractor scope of work.",
                source_or_basis="TwinEnergyGoalReasoningView.recorded_homeowner_goals",
                provenance=self._provenance(
                    source_views=["TwinEnergyGoalReasoningView"],
                    source_fields=["recorded_homeowner_goals"],
                    source_refs=homeowner_goal_refs,
                    derived_from=["recorded_homeowner_goals"],
                ),
                next_actions=["Review goals as planning context before contractor scoping."],
            )
        ]
        home_site_summary = [
            self._item(
                item_id="home_site_planning_summary",
                category="home_site_planning_summary",
                statement="Home and site planning summary is minimized for contractor scoping and excludes private account context.",
                source_or_basis="TwinRuntimeProjectionView.contractor.projection_records",
                provenance=self._provenance(
                    source_views=["TwinRuntimeProjectionView.contractor"],
                    source_fields=["projection_records"],
                    source_refs=home_site_refs,
                    derived_from=["contractor_runtime_projection"],
                ),
                next_actions=["Use site summary as a planning prompt for site-walk preparation."],
            )
        ]
        equipment_summary = [
            self._item(
                item_id="known_electrical_equipment_summary",
                category="known_electrical_equipment_summary",
                statement="Known electrical equipment context is planning-only and remains subject to field and source verification.",
                source_or_basis="TwinRuntimeProjectionView.contractor.projection_records",
                provenance=self._provenance(
                    source_views=["TwinRuntimeProjectionView.contractor"],
                    source_fields=["projection_records"],
                    source_refs=equipment_refs,
                    derived_from=["contractor_runtime_projection"],
                ),
                required_verifiers=["contractor_or_qualified_professional"],
                next_actions=["Verify equipment identity, nameplate data, and source-backed specifications before design work."],
            )
        ]
        proposed_system_context = [
            self._item(
                item_id="proposed_system_context",
                category="proposed_system_context",
                statement="Proposed system context is existing planning context only and is not a final design, bid, proposal, or directive.",
                source_or_basis="TwinRuntimeProjectionView.contractor.projection_records",
                provenance=self._provenance(
                    source_views=["TwinRuntimeProjectionView.contractor", "TwinProposalReadinessFoundationView"],
                    source_fields=["projection_records", "contractor_advisory_context_readiness"],
                    source_refs=proposed_system_refs,
                    derived_from=["contractor_runtime_projection", "proposal_readiness_foundation"],
                ),
                required_verifiers=["contractor_or_qualified_professional"],
                next_actions=["Review proposed context only after missing information and field conditions are checked."],
            )
        ]
        missing_information = [
            self._item(
                item_id="missing_information",
                category="missing_information",
                statement="Missing information is surfaced for contractor review preparation and does not authorize assumptions.",
                source_or_basis="TwinContractorFacingAdvisoryView.contractor_visible_known_unknown_summary",
                provenance=self._provenance(
                    source_views=["TwinContractorFacingAdvisoryView"],
                    source_fields=["contractor_visible_known_unknown_summary"],
                    source_refs=missing_refs,
                    derived_from=["contractor_facing_advisory"],
                ),
                missing_inputs=missing_refs,
                next_actions=["Collect or verify missing inputs before treating planning context as review-ready."],
            )
        ]
        verification_needs = [
            self._item(
                item_id="contractor_verification_needs",
                category="contractor_verification_needs",
                statement="Contractor verification needs identify review burden only; this endpoint does not verify field conditions.",
                source_or_basis="TwinContractorFacingAdvisoryView.field_verification_needs",
                provenance=self._provenance(
                    source_views=["TwinContractorFacingAdvisoryView"],
                    source_fields=["field_verification_needs", "topology_verification_needs", "professional_review_boundaries"],
                    source_refs=verification_refs,
                    derived_from=["contractor_facing_advisory"],
                ),
                required_verifiers=["contractor_or_qualified_professional", "engineer_or_ahj_when_required"],
                next_actions=["Use verification needs as review prompts, not as completed verification."],
            )
        ]
        provenance_notes = [
            self._item(
                item_id="provenance_trust_notes",
                category="provenance_trust_notes",
                statement="Provenance and trust notes indicate source basis and uncertainty only; they do not prove correctness or field verification.",
                source_or_basis="TwinContractorFacingAdvisoryView.provenance_basis",
                provenance=self._provenance(
                    source_views=["TwinContractorFacingAdvisoryView"],
                    source_fields=["provenance_basis", "source_basis"],
                    source_refs=contractor_advisory.source_basis.provenance_refs,
                    derived_from=["contractor_facing_advisory"],
                ),
                next_actions=["Review source basis and missing provenance before relying on a planning item."],
            )
        ]
        permission_notes = [
            self._item(
                item_id="permission_readiness_notes",
                category="permission_readiness_notes",
                statement="Permission-readiness notes preserve homeowner authority but are not authorization, consent, or enforcement.",
                source_or_basis="TwinContractorFacingAdvisoryView.permission_readiness_metadata",
                provenance=self._provenance(
                    source_views=["TwinContractorFacingAdvisoryView", "TwinRuntimeProjectionView.contractor"],
                    source_fields=["permission_readiness_metadata", "permission_readiness"],
                    source_refs=contractor_advisory.source_basis.permission_refs,
                    derived_from=["contractor_facing_advisory", "contractor_runtime_projection"],
                ),
                next_actions=["Treat sharing and review as future permission-scoped behavior until enforcement exists."],
            )
        ]
        review_prompts = [
            self._item(
                item_id="next_safe_contractor_review_prompts",
                category="next_safe_contractor_review_prompts",
                statement="Next contractor review prompts are planning prompts only and are not contractor directives.",
                source_or_basis="TwinContractorFacingAdvisoryView.prerequisite_advisory_recommendations",
                provenance=self._provenance(
                    source_views=["TwinContractorFacingAdvisoryView"],
                    source_fields=["prerequisite_advisory_recommendations"],
                    source_refs=next_prompt_refs,
                    derived_from=["contractor_facing_advisory"],
                ),
                required_verifiers=["homeowner", "contractor_or_qualified_professional"],
                next_actions=[
                    "Verify equipment and source documents.",
                    "Review field-verification needs.",
                    "Confirm missing information before proposal, pricing, or design work.",
                ],
            )
        ]

        return ContractorPlanningContextView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 5B contractor-scoped planning context built request-time from existing "
                "TwinPlanningContext, contractor runtime projection, and contractor-facing advisory outputs; "
                "does not write data, enforce permissions, create contractor accounts, export data, persist state, "
                "create twin_id, generate proposals, price work, rank contractors, integrate CRM, or calculate final electrical design."
            ),
            contractor_scope=ContractorContextScope(limitations=CONTRACTOR_CONTEXT_LIMITATIONS),
            source_basis=source_basis,
            homeowner_goals=homeowner_goals,
            home_site_planning_summary=home_site_summary,
            known_electrical_equipment_summary=equipment_summary,
            proposed_system_context=proposed_system_context,
            missing_information=missing_information,
            contractor_verification_needs=verification_needs,
            provenance_trust_notes=provenance_notes,
            permission_readiness_notes=permission_notes,
            next_safe_contractor_review_prompts=review_prompts,
            deferred_boundaries=sorted(CONTRACTOR_CONTEXT_DEFERRED_BOUNDARIES),
            limitations=CONTRACTOR_CONTEXT_LIMITATIONS,
            compatibility_note=(
                "Existing TwinPlanningContext and Phase 3/4 routes remain unchanged; this is an additive "
                "contractor-context GET surface under /api/contractor-context."
            ),
        )

    def _confirmation_gate(
        self,
        *,
        gate_id: str,
        title: str,
        category: str,
        status: str,
        required_verifier: str,
        blocker_level: str,
        source_basis: ContractorContextProvenance,
    ) -> ContractorConfirmationGate:
        return ContractorConfirmationGate(
            gate_id=gate_id,
            title=title,
            category=category,
            status=status,
            required_verifier=required_verifier,
            source_or_basis=(
                "Derived from existing contractor planning context and contractor-facing advisory readiness; "
                "status is a review prompt only, not persisted confirmation."
            ),
            blocker_level=blocker_level,
            reason=(
                f"{title} is a contractor/AHJ/utility review topic. The app has not performed or approved this review."
            ),
            next_action=(
                f"Use '{title}' as a planning review prompt for {required_verifier}; do not treat it as completed verification."
            ),
            provenance=source_basis,
            limitations=CONTRACTOR_CONFIRMATION_GATE_LIMITATIONS,
        )

    def build_confirmation_gate_projection(self, db, home_id: str) -> Optional[ContractorConfirmationGateProjectionView]:
        contractor_context = self.build_contractor_planning_context(db, home_id)
        if contractor_context is None:
            return None

        source_basis = self._provenance(
            source_views=[
                "ContractorPlanningContextView",
                "TwinContractorFacingAdvisoryView",
                "TwinRuntimeProjectionView.contractor",
            ],
            source_fields=[
                "contractor_verification_needs",
                "missing_information",
                "provenance_trust_notes",
                "permission_readiness_notes",
                "next_safe_contractor_review_prompts",
            ],
            source_refs=[
                item.item_id
                for item in (
                    contractor_context.contractor_verification_needs
                    + contractor_context.missing_information
                    + contractor_context.next_safe_contractor_review_prompts
                )
            ],
            derived_from=["phase_5b_contractor_scoped_planning_context"],
            limitations=CONTRACTOR_CONFIRMATION_GATE_LIMITATIONS,
        )
        gates = [
            self._confirmation_gate(
                gate_id=gate_id,
                title=title,
                category=category,
                status=status,
                required_verifier=required_verifier,
                blocker_level=blocker_level,
                source_basis=source_basis,
            )
            for gate_id, title, category, status, required_verifier, blocker_level in CONTRACTOR_CONFIRMATION_GATES
        ]

        return ContractorConfirmationGateProjectionView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 5C confirmation gate projection built request-time from existing contractor planning context; "
                "does not persist gate state, confirm completion, approve design, enforce permissions, create accounts, or write data."
            ),
            gates=gates,
            source_basis=source_basis,
            deferred_boundaries=sorted(CONTRACTOR_CONTEXT_DEFERRED_BOUNDARIES),
            limitations=CONTRACTOR_CONFIRMATION_GATE_LIMITATIONS,
            compatibility_note=(
                "Existing contractor planning context response remains unchanged; this is an additive confirmation-gates GET surface."
            ),
        )

    def _install_signal(
        self,
        *,
        signal_id: str,
        category: str,
        severity: str,
        reason: str,
        missing_inputs: List[str],
        required_verifier: str,
        next_action: str,
        source_or_basis: str,
        provenance: ContractorContextProvenance,
    ) -> ContractorInstallComplexitySignal:
        return ContractorInstallComplexitySignal(
            signal_id=signal_id,
            category=category,
            severity=severity,
            reason=reason,
            missing_inputs=self._sorted_unique(missing_inputs),
            required_verifier=required_verifier,
            next_action=next_action,
            source_or_basis=source_or_basis,
            provenance=provenance,
            limitations=CONTRACTOR_INSTALL_COMPLEXITY_LIMITATIONS,
        )

    def build_install_complexity_view(self, db, home_id: str) -> Optional[ContractorInstallComplexityView]:
        contractor_context = self.build_contractor_planning_context(db, home_id)
        gate_projection = self.build_confirmation_gate_projection(db, home_id)
        if contractor_context is None or gate_projection is None:
            return None

        source_basis = self._provenance(
            source_views=[
                "ContractorPlanningContextView",
                "ContractorConfirmationGateProjectionView",
                "TwinContractorFacingAdvisoryView",
            ],
            source_fields=[
                "missing_information",
                "contractor_verification_needs",
                "known_electrical_equipment_summary",
                "proposed_system_context",
                "next_safe_contractor_review_prompts",
                "gates",
            ],
            source_refs=[
                item.item_id
                for item in (
                    contractor_context.missing_information
                    + contractor_context.contractor_verification_needs
                    + contractor_context.known_electrical_equipment_summary
                    + contractor_context.proposed_system_context
                    + contractor_context.next_safe_contractor_review_prompts
                )
            ]
            + [gate.gate_id for gate in gate_projection.gates],
            derived_from=[
                "phase_5b_contractor_scoped_planning_context",
                "phase_5c_confirmation_gate_projection",
            ],
            limitations=CONTRACTOR_INSTALL_COMPLEXITY_LIMITATIONS,
        )
        missing_inputs = self._sorted_unique(
            [
                missing
                for item in contractor_context.missing_information
                + contractor_context.known_electrical_equipment_summary
                + contractor_context.proposed_system_context
                for missing in item.missing_inputs
            ]
        )
        gate_missing_inputs = [
            gate.gate_id
            for gate in gate_projection.gates
            if gate.status in {"contractor_review_required", "needs_site_visit", "ahj_or_utility_dependent"}
        ]
        verification_inputs = self._sorted_unique(
            [
                need
                for item in contractor_context.contractor_verification_needs
                for need in item.provenance.source_refs + item.required_verifiers
            ]
        )

        signal_specs = [
            (
                "product_uncertainty",
                "product_uncertainty",
                "high",
                "Product/spec context remains uncertain until source-backed specs, nameplates, and manuals are reviewed.",
                ["product_specs_verified", "manufacturer_install_manual_reviewed"],
                "contractor_or_qualified_professional",
                "Review product specs and manuals as planning prerequisites only.",
            ),
            (
                "nameplate_uncertainty",
                "nameplate_uncertainty",
                "high",
                "Nameplate ratings remain a required review topic and are not verified by this app.",
                ["nameplate_ratings_verified"],
                "contractor_or_qualified_professional",
                "Verify nameplate ratings in the field or from source-backed documentation.",
            ),
            (
                "panel_service_uncertainty",
                "panel_service_uncertainty",
                "medium",
                "Panel/service context is planning-only and may require contractor or professional review before design use.",
                ["panel_service_review", "overcurrent_protection_reviewed"],
                "contractor_or_qualified_professional",
                "Review recorded panel/service context before interpreting design feasibility.",
            ),
            (
                "routing_path_uncertainty",
                "routing_path_uncertainty",
                "high",
                "Routing/path conditions require site review; this signal does not determine route design or conduit requirements.",
                ["distance_measurements_confirmed", "conduit_routing_path_confirmed", "indoor_outdoor_wet_location_confirmed"],
                "contractor_or_qualified_professional",
                "Use route items as site-walk prompts only.",
            ),
            (
                "backup_scope_uncertainty",
                "backup_scope_uncertainty",
                "medium",
                "Backup scope depends on homeowner decisions, recorded loads, and contractor review; it is not finalized here.",
                ["circuit_purpose_confirmed", "load_current_assumptions_confirmed"],
                "homeowner_and_contractor",
                "Confirm load intent and backup scope before proposal or design work.",
            ),
            (
                "ahj_utility_uncertainty",
                "ahj_utility_uncertainty",
                "blocked",
                "AHJ/utility requirements are external authority topics and are not determined by this app.",
                ["utility_ahj_requirements_reviewed"],
                "contractor_ahj_or_utility",
                "Treat AHJ/utility requirements as external review dependencies.",
            ),
            (
                "material_takeoff_uncertainty",
                "material_takeoff_uncertainty",
                "high",
                "Material/takeoff uncertainty remains until route, raceway, conductor, and site conditions are reviewed.",
                ["conductor_material_confirmed", "raceway_type_confirmed", "current_carrying_conductors_confirmed"],
                "contractor_or_qualified_professional",
                "Do not derive material quantities or final conductor/raceway choices from this signal.",
            ),
            (
                "field_verification_burden",
                "field_verification_burden",
                "high",
                "Field verification burden is visible because multiple gates remain contractor-review or site-visit dependent.",
                gate_missing_inputs,
                "contractor_or_qualified_professional",
                "Plan field verification around unresolved gate topics.",
            ),
            (
                "homeowner_decision_dependency",
                "homeowner_decision_dependency",
                "medium",
                "Homeowner goals and backup-scope decisions remain planning dependencies and do not define contractor scope by themselves.",
                missing_inputs or ["homeowner_goal_and_scope_confirmation"],
                "homeowner",
                "Confirm homeowner intent before treating planning context as contractor-scoped work.",
            ),
            (
                "contractor_review_burden",
                "contractor_review_burden",
                "high",
                "Contractor review burden remains because planning context is not a directive, bid, proposal, or final design.",
                verification_inputs or gate_missing_inputs,
                "contractor_or_qualified_professional",
                "Use contractor review burden as a review checklist, not as completed review.",
            ),
        ]
        signals = [
            self._install_signal(
                signal_id=signal_id,
                category=category,
                severity=severity,
                reason=reason,
                missing_inputs=signal_missing_inputs,
                required_verifier=required_verifier,
                next_action=next_action,
                source_or_basis="Derived from Phase 5B contractor context and Phase 5C confirmation gate projection.",
                provenance=source_basis,
            )
            for (
                signal_id,
                category,
                severity,
                reason,
                signal_missing_inputs,
                required_verifier,
                next_action,
            ) in signal_specs
        ]

        return ContractorInstallComplexityView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 5D install complexity and uncertainty signal view built request-time from existing "
                "contractor context and confirmation gate projection; does not calculate final wire, conduit, breaker, "
                "disconnect, NEC/code-compliant design, proposals, pricing, bids, contractor directives, or field verification."
            ),
            signals=signals,
            source_basis=source_basis,
            deferred_boundaries=sorted(CONTRACTOR_CONTEXT_DEFERRED_BOUNDARIES),
            limitations=CONTRACTOR_INSTALL_COMPLEXITY_LIMITATIONS,
            compatibility_note=(
                "Existing contractor context and confirmation gate responses remain unchanged; this is an additive install-complexity GET surface."
            ),
        )


contractor_context_service = ContractorContextService()

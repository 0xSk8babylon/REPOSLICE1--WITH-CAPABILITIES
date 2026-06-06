from typing import Dict, List, Optional

from app.core.types import ConfidenceLevel
from app.energy_passport.schemas import (
    EnergyPassportContextSection,
    EnergyPassportFinancingStructure,
    EnergyPassportScope,
    EnergyPassportSourceBasis,
    EnergyPassportStatus,
    EnergyPassportSummary,
    EnergyPassportSystemFinancialObligation,
    EnergyPassportSystemSummary,
    EnergyPassportSystemType,
    EnergyPassportTransferReadiness,
    EnergyPassportTransferReadinessLevel,
    EnergyPassportTransferRelevanceFlag,
    EnergyPassportView,
)


ENERGY_PASSPORT_LIMITATIONS = [
    "Energy Passport is a read-only homeowner-safe summary derived at request time from existing planning views.",
    "It is not a legal, title, escrow, deed, tax, appraisal, underwriting, warranty, permit, payoff, lien, UCC, or financial validation product.",
    "System ownership, financing, transfer relevance, and document needs are non-authoritative review metadata unless source-backed records are added later.",
    "Buyer-safe and contractor-safe summaries are wording metadata only and are not permission-enforced views or external disclosures.",
]

ENERGY_PASSPORT_DEFERRED_BOUNDARIES = [
    "appraisal",
    "auth_security",
    "crm_write",
    "deed_review",
    "deploy",
    "escrow",
    "financial_conclusions",
    "lien_search",
    "lease_assignment",
    "migrations",
    "payoff_calculation",
    "permit_validation",
    "permission_enforcement",
    "persistence",
    "push",
    "tax_advice",
    "title_search",
    "ucc_search",
    "underwriting",
    "warranty_validation",
    "write_endpoints",
]

ENERGY_PASSPORT_DOCUMENTS_NEEDED = [
    "purchase agreement",
    "loan agreement",
    "lease agreement",
    "PPA agreement",
    "payoff statement",
    "assignment or transfer terms",
    "UCC/lien filing confirmation",
    "utility program agreement",
    "manufacturer financing agreement",
    "contractor financing agreement",
    "monitoring/account transfer terms",
]

SYSTEM_LABELS = {
    EnergyPassportSystemType.solar_pv: "solar PV",
    EnergyPassportSystemType.battery_storage: "battery storage",
    EnergyPassportSystemType.backup_generator: "backup/generator",
    EnergyPassportSystemType.panel_load_management: "panel/load management",
    EnergyPassportSystemType.ev_readiness: "EV readiness",
    EnergyPassportSystemType.utility_program_context: "utility/program context",
}


class EnergyPassportService:
    def _sorted_unique(self, values: List[str]) -> List[str]:
        return sorted({value for value in values if value})

    def _basis(
        self,
        *,
        source_views: Optional[List[str]] = None,
        source_fields: Optional[List[str]] = None,
        source_refs: Optional[List[str]] = None,
        system_refs: Optional[List[str]] = None,
        obligation_refs: Optional[List[str]] = None,
        transfer_refs: Optional[List[str]] = None,
        planning_history_refs: Optional[List[str]] = None,
        post_install_refs: Optional[List[str]] = None,
        future_upgrade_refs: Optional[List[str]] = None,
        missing_input_refs: Optional[List[str]] = None,
        blocker_refs: Optional[List[str]] = None,
        assumption_refs: Optional[List[str]] = None,
        deferred_boundary_refs: Optional[List[str]] = None,
        unavailable_source_refs: Optional[List[str]] = None,
        basis_quality: str = "request_time_derived_from_existing_phase_6_13_views",
    ) -> EnergyPassportSourceBasis:
        return EnergyPassportSourceBasis(
            source_views=self._sorted_unique(
                source_views
                or [
                    "TwinPlanningContext",
                    "PlanningExchangeObject",
                    "ContractorWorkflowReadinessView",
                    "ProductPreferencesView",
                    "PostInstallView",
                    "CRMHandoffView",
                ]
            ),
            source_fields=self._sorted_unique(
                source_fields
                or [
                    "TwinPlanningContext.sections",
                    "PlanningExchangeObject.source_basis",
                    "ContractorWorkflowReadinessView.missing_inputs",
                    "ProductPreferencesView.categories",
                    "PostInstallView.lifecycle_events",
                    "PostInstallView.opportunities",
                    "CRMHandoffView.handoff_fields",
                ]
            ),
            source_refs=self._sorted_unique(source_refs or []),
            system_refs=self._sorted_unique(system_refs or []),
            obligation_refs=self._sorted_unique(obligation_refs or []),
            transfer_refs=self._sorted_unique(transfer_refs or []),
            planning_history_refs=self._sorted_unique(planning_history_refs or []),
            post_install_refs=self._sorted_unique(post_install_refs or []),
            future_upgrade_refs=self._sorted_unique(future_upgrade_refs or []),
            missing_input_refs=self._sorted_unique(missing_input_refs or []),
            blocker_refs=self._sorted_unique(blocker_refs or []),
            assumption_refs=self._sorted_unique(assumption_refs or []),
            deferred_boundary_refs=self._sorted_unique(deferred_boundary_refs or ENERGY_PASSPORT_DEFERRED_BOUNDARIES),
            unavailable_source_refs=self._sorted_unique(unavailable_source_refs or []),
            basis_quality=basis_quality,
            request_time_derived=True,
            verified_fact_claim_present=False,
            authoritative_validation_present=False,
            limitations=ENERGY_PASSPORT_LIMITATIONS,
        )

    def _context_refs(self, context) -> Dict[str, List[str]]:
        refs: Dict[str, List[str]] = {
            "battery_storage": [],
            "backup_generator": [],
            "ev_readiness": [],
            "panel_load_management": [],
            "planning_history": [],
            "solar_pv": [],
            "utility_program_context": [],
        }
        for section in getattr(context, "sections", []):
            section_key = getattr(section, "section_key", "")
            records = getattr(section, "records", [])
            if section_key in {"scenario", "scenarios", "scenario_revisions", "energy_system_designs", "designs"}:
                refs["planning_history"].append(section_key)
            for record in records:
                entity_type = getattr(record, "entity_type", "")
                entity_id = getattr(record, "entity_id", "")
                record_ref = f"{section_key}:{entity_type}:{entity_id}"
                payload = getattr(record, "record", {}) or {}
                product_type = str(payload.get("product_type") or "").lower()
                category = str(payload.get("category") or "").lower()
                role = str(payload.get("role_in_system") or "").lower()
                design_goal = str(payload.get("design_goal") or "").lower()
                field_values = " ".join(
                    str(value).lower() for value in [product_type, category, role, design_goal, payload.get("name", "")]
                )

                if product_type in {"solar_panel", "pv_module"} or "solar" in field_values or "pv" in field_values:
                    refs["solar_pv"].append(record_ref)
                if product_type == "battery" or "battery" in field_values:
                    refs["battery_storage"].append(record_ref)
                if product_type == "generator" or "generator" in field_values:
                    refs["backup_generator"].append(record_ref)
                if entity_type in {"electrical_panel", "load"}:
                    refs["panel_load_management"].append(record_ref)
                if "ev" in field_values or "charger" in field_values:
                    refs["ev_readiness"].append(record_ref)
                if entity_type == "home" and payload.get("utility_provider"):
                    refs["utility_program_context"].append(record_ref)
                if entity_type in {"scenario", "scenario_revision", "energy_system_design"}:
                    refs["planning_history"].append(record_ref)
        return {key: self._sorted_unique(value) for key, value in refs.items()}

    def _category_refs(self, product_view) -> Dict[str, List[str]]:
        refs: Dict[str, List[str]] = {
            "battery_storage": [],
            "backup_generator": [],
            "ev_readiness": [],
            "panel_load_management": [],
            "solar_pv": [],
            "future_upgrade": [],
        }
        for category in getattr(product_view, "categories", []) if product_view else []:
            raw_category_id = getattr(category, "category_id", "")
            category_id = getattr(raw_category_id, "value", raw_category_id)
            category_ref = f"ProductPreferencesView.category:{category_id}"
            if category_id in {"pv_modules", "inverter_topology", "microinverter_string_hybrid_direction"}:
                refs["solar_pv"].append(category_ref)
            if category_id in {"battery_coupling", "backup_scope", "gateway_transfer_equipment"}:
                refs["battery_storage"].append(category_ref)
            if category_id == "backup_scope":
                refs["backup_generator"].append(category_ref)
            if category_id in {"backup_loads_panel", "main_service_panel_subpanel", "monitoring_controls"}:
                refs["panel_load_management"].append(category_ref)
            if category_id == "ev_charger_readiness":
                refs["ev_readiness"].append(category_ref)
            refs["future_upgrade"].append(category_ref)
        return {key: self._sorted_unique(value) for key, value in refs.items()}

    def _safe_status(self, *, context_refs: List[str], category_refs: List[str], missing_inputs: List[str]) -> EnergyPassportStatus:
        if context_refs:
            return EnergyPassportStatus.planned
        if category_refs:
            return EnergyPassportStatus.candidate if not missing_inputs else EnergyPassportStatus.needs_confirmation
        return EnergyPassportStatus.unknown

    def _system_summary(
        self,
        *,
        system_type: EnergyPassportSystemType,
        context_refs: List[str],
        category_refs: List[str],
        missing_inputs: List[str],
    ) -> EnergyPassportSystemSummary:
        label = SYSTEM_LABELS[system_type]
        status = self._safe_status(
            context_refs=context_refs,
            category_refs=category_refs,
            missing_inputs=missing_inputs,
        )
        all_refs = self._sorted_unique(context_refs + category_refs)
        if status == EnergyPassportStatus.planned:
            summary = f"{label} has planning records in the current home context; this is not an installation, approval, or warranty claim."
            confidence = ConfidenceLevel.medium
        elif status == EnergyPassportStatus.candidate:
            summary = f"{label} appears as review metadata from existing planning views and needs source confirmation before transfer use."
            confidence = ConfidenceLevel.low
        elif status == EnergyPassportStatus.needs_confirmation:
            summary = f"{label} has review metadata but missing inputs prevent a stronger planning summary."
            confidence = ConfidenceLevel.low
        else:
            summary = f"{label} is unknown from the current source basis."
            confidence = ConfidenceLevel.low
        return EnergyPassportSystemSummary(
            system_type=system_type,
            status=status,
            confidence_level=confidence,
            summary=summary,
            source_basis=self._basis(
                source_refs=all_refs,
                system_refs=[f"{system_type.value}:{ref}" for ref in all_refs],
                missing_input_refs=missing_inputs,
            ),
            missing_inputs=missing_inputs,
            assumptions=["System status is limited to known/planned/candidate/needs_confirmation/not_available/unknown safe statuses."],
            limitations=ENERGY_PASSPORT_LIMITATIONS,
        )

    def _obligation(
        self,
        system: EnergyPassportSystemSummary,
    ) -> EnergyPassportSystemFinancialObligation:
        system_label = SYSTEM_LABELS[system.system_type]
        return EnergyPassportSystemFinancialObligation(
            system_type=system.system_type,
            ownership_status=EnergyPassportStatus.needs_confirmation,
            financing_structure=EnergyPassportFinancingStructure.needs_confirmation,
            transfer_relevance_flags=[
                EnergyPassportTransferRelevanceFlag.document_review_required,
                EnergyPassportTransferRelevanceFlag.unknown,
            ],
            documents_needed=ENERGY_PASSPORT_DOCUMENTS_NEEDED,
            non_authoritative=True,
            needs_confirmation=True,
            source_basis=self._basis(
                source_refs=system.source_basis.source_refs,
                system_refs=system.source_basis.system_refs,
                obligation_refs=[f"{system.system_type.value}:ownership_financing_needs_confirmation"],
                transfer_refs=[
                    f"{system.system_type.value}:{EnergyPassportTransferRelevanceFlag.document_review_required.value}",
                    f"{system.system_type.value}:{EnergyPassportTransferRelevanceFlag.unknown.value}",
                ],
                missing_input_refs=[
                    f"{system.system_type.value}:ownership_status",
                    f"{system.system_type.value}:financing_structure",
                    f"{system.system_type.value}:transfer_documents",
                ],
                basis_quality="ownership_financing_transfer_inputs_not_source_backed",
            ),
            assumptions=[
                f"{system_label} ownership and financing are marked needs_confirmation because no existing source contract provides authoritative obligation data."
            ],
            limitations=ENERGY_PASSPORT_LIMITATIONS,
        )

    def _context_section(
        self,
        *,
        section_name: str,
        refs: List[str],
        summary_when_present: str,
        summary_when_missing: str,
        source_fields: List[str],
        missing_inputs: Optional[List[str]] = None,
        blockers: Optional[List[str]] = None,
        future_upgrade_refs: Optional[List[str]] = None,
        post_install_refs: Optional[List[str]] = None,
    ) -> EnergyPassportContextSection:
        missing = self._sorted_unique(missing_inputs or [])
        section_refs = self._sorted_unique(refs)
        if section_refs and not missing:
            status = EnergyPassportStatus.known
        elif section_refs:
            status = EnergyPassportStatus.needs_confirmation
        else:
            status = EnergyPassportStatus.unknown
        return EnergyPassportContextSection(
            section_name=section_name,
            status=status,
            summary=summary_when_present if section_refs else summary_when_missing,
            source_basis=self._basis(
                source_fields=source_fields,
                source_refs=section_refs,
                planning_history_refs=section_refs if section_name == "planning_history_summary" else [],
                post_install_refs=post_install_refs or [],
                future_upgrade_refs=future_upgrade_refs or [],
                missing_input_refs=missing,
                blocker_refs=blockers or [],
            ),
            assumptions=["Context section is derived at request time and does not create a new history or ownership store."],
            blockers=self._sorted_unique(blockers or []),
            deferred_boundaries=ENERGY_PASSPORT_DEFERRED_BOUNDARIES,
            missing_inputs=missing,
            limitations=ENERGY_PASSPORT_LIMITATIONS,
        )

    def _transfer_readiness(
        self,
        *,
        obligations: List[EnergyPassportSystemFinancialObligation],
        missing_inputs: List[str],
        source_refs: List[str],
    ) -> EnergyPassportTransferReadiness:
        obligation_missing = [
            missing
            for obligation in obligations
            for missing in obligation.source_basis.missing_input_refs
        ]
        all_missing = self._sorted_unique(missing_inputs + obligation_missing)
        confirmation_needed = self._sorted_unique(
            [
                "confirm system ownership status",
                "confirm financing structure",
                "review transfer documents",
                "confirm monitoring or cloud account transfer needs",
                "confirm utility-program or property-tax assessment relevance",
            ]
        )
        readiness_level = (
            EnergyPassportTransferReadinessLevel.blocked_by_missing_inputs
            if all_missing
            else EnergyPassportTransferReadinessLevel.ready_for_manual_review
        )
        return EnergyPassportTransferReadiness(
            readiness_level=readiness_level,
            transfer_ready=False,
            missing_transfer_inputs=all_missing,
            confirmation_needed=confirmation_needed,
            buyer_disclosure_recommended=True,
            contractor_review_recommended=True,
            buyer_safe_summary=(
                "Energy-system transfer context needs document review and confirmation before a buyer-facing disclosure should rely on it."
            ),
            contractor_safe_summary=(
                "Contractor review should treat ownership, financing, transfer terms, monitoring accounts, and utility-program links as open confirmation items."
            ),
            source_basis=self._basis(
                source_refs=source_refs,
                transfer_refs=[flag.value for flag in EnergyPassportTransferRelevanceFlag],
                missing_input_refs=all_missing,
                basis_quality="transfer_readiness_degraded_by_unknown_ownership_financing_inputs",
            ),
            assumptions=["Unknown or needs-confirmation obligation inputs always degrade transfer readiness."],
            limitations=ENERGY_PASSPORT_LIMITATIONS,
        )

    def build_home_energy_passport(self, db, home_id: str) -> Optional[EnergyPassportView]:
        from app.services.contractor_workflow import contractor_workflow_service
        from app.services.crm_handoff import crm_handoff_service
        from app.services.planning_exchange import planning_exchange_service
        from app.services.post_install import post_install_service
        from app.services.product_preferences import product_preferences_service
        from app.services.twin_planning_context import twin_planning_context_service

        context = twin_planning_context_service.build(db, home_id)
        if context is None:
            return None

        planning_exchange = planning_exchange_service.build_planning_exchange_object(db, home_id)
        contractor_workflow = contractor_workflow_service.build_home_contractor_workflow_readiness(db, home_id)
        product_preferences = product_preferences_service.build_home_product_preferences(db, home_id)
        post_install = post_install_service.build_home_post_install_view(db, home_id)
        crm_handoff = crm_handoff_service.build_home_crm_handoff(db, home_id)

        unavailable_sources = [
            name
            for name, value in [
                ("PlanningExchangeObject", planning_exchange),
                ("ContractorWorkflowReadinessView", contractor_workflow),
                ("ProductPreferencesView", product_preferences),
                ("PostInstallView", post_install),
                ("CRMHandoffView", crm_handoff),
            ]
            if value is None
        ]

        context_refs = self._context_refs(context)
        category_refs = self._category_refs(product_preferences)
        view_missing_inputs = self._sorted_unique(
            getattr(contractor_workflow, "missing_inputs", [])
            + getattr(product_preferences, "missing_inputs", [])
            + getattr(post_install, "missing_inputs", [])
        )

        systems = [
            self._system_summary(
                system_type=system_type,
                context_refs=context_refs.get(system_type.value, []),
                category_refs=category_refs.get(system_type.value, []),
                missing_inputs=view_missing_inputs,
            )
            for system_type in [
                EnergyPassportSystemType.solar_pv,
                EnergyPassportSystemType.battery_storage,
                EnergyPassportSystemType.backup_generator,
                EnergyPassportSystemType.panel_load_management,
                EnergyPassportSystemType.ev_readiness,
                EnergyPassportSystemType.utility_program_context,
            ]
        ]

        relevant_systems = [
            system
            for system in systems
            if system.status
            in {
                EnergyPassportStatus.known,
                EnergyPassportStatus.planned,
                EnergyPassportStatus.candidate,
                EnergyPassportStatus.needs_confirmation,
            }
            and system.status != EnergyPassportStatus.unknown
        ]
        obligations = [self._obligation(system) for system in relevant_systems]

        all_source_refs = self._sorted_unique(
            [ref for refs in context_refs.values() for ref in refs]
            + [ref for refs in category_refs.values() for ref in refs]
        )
        transfer_readiness = self._transfer_readiness(
            obligations=obligations,
            missing_inputs=view_missing_inputs,
            source_refs=all_source_refs,
        )

        planning_history_refs = context_refs.get("planning_history", [])
        post_install_refs = self._sorted_unique(
            [event.event_id for event in getattr(post_install, "lifecycle_events", [])]
            + [opportunity.opportunity_id for opportunity in getattr(post_install, "opportunities", [])]
        )
        future_upgrade_refs = category_refs.get("future_upgrade", [])

        planning_history_summary = self._context_section(
            section_name="planning_history_summary",
            refs=planning_history_refs,
            summary_when_present="Planning history context is available from existing design, scenario, or revision planning records.",
            summary_when_missing="Planning history context is not available from the current source basis.",
            source_fields=["TwinPlanningContext.sections.scenarios", "TwinPlanningContext.sections.scenario_revisions"],
        )
        post_install_context = self._context_section(
            section_name="post_install_context",
            refs=post_install_refs,
            summary_when_present="Post-install context is available as request-time retention and lifecycle metadata only.",
            summary_when_missing="Post-install context is unavailable from the current source basis.",
            source_fields=["PostInstallView.lifecycle_events", "PostInstallView.opportunities"],
            missing_inputs=getattr(post_install, "missing_inputs", []),
            blockers=[blocker.blocker_id for blocker in getattr(post_install, "blockers", [])],
            post_install_refs=post_install_refs,
        )
        ownership_context = self._context_section(
            section_name="ownership_context",
            refs=[obligation.system_type.value for obligation in obligations],
            summary_when_present="Ownership and financing context is represented only as needs-confirmation transfer metadata.",
            summary_when_missing="Ownership and financing source context is unavailable.",
            source_fields=["EnergyPassportView.system_financial_obligations"],
            missing_inputs=transfer_readiness.missing_transfer_inputs,
            blockers=["ownership_financing_source_basis_missing"] if obligations else [],
        )
        future_upgrade_context = self._context_section(
            section_name="future_upgrade_context",
            refs=future_upgrade_refs,
            summary_when_present="Future upgrade context is available from existing product/install review metadata only.",
            summary_when_missing="Future upgrade context is unavailable from the current source basis.",
            source_fields=["ProductPreferencesView.categories", "ContractorWorkflowReadinessView.option_candidate_refs"],
            missing_inputs=getattr(product_preferences, "missing_inputs", []),
            blockers=[blocker.blocker_id for blocker in getattr(product_preferences, "blockers", [])],
            future_upgrade_refs=future_upgrade_refs,
        )

        overall_status = (
            EnergyPassportStatus.needs_confirmation
            if transfer_readiness.missing_transfer_inputs or unavailable_sources
            else EnergyPassportStatus.known
        )
        summary = EnergyPassportSummary(
            overall_status=overall_status,
            confidence_level=ConfidenceLevel.low if transfer_readiness.missing_transfer_inputs else ConfidenceLevel.medium,
            system_count=len(systems),
            relevant_obligation_count=len(obligations),
            unknown_obligation_count=len([obligation for obligation in obligations if obligation.needs_confirmation]),
            missing_transfer_input_count=len(transfer_readiness.missing_transfer_inputs),
            transfer_ready=transfer_readiness.transfer_ready,
            non_authoritative_summary=(
                "Energy Passport summary is deterministic request-time metadata and does not validate transfer, title, financial, permit, warranty, or legal status."
            ),
        )
        scope = EnergyPassportScope(limitations=ENERGY_PASSPORT_LIMITATIONS)
        return EnergyPassportView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 14 Energy Passport summary. It composes existing Phase 6 through Phase 13 source surfaces where available."
            ),
            scope=scope,
            summary=summary,
            system_summary=systems,
            system_financial_obligations=obligations,
            transfer_readiness=transfer_readiness,
            planning_history_summary=planning_history_summary,
            post_install_context=post_install_context,
            ownership_context=ownership_context,
            future_upgrade_context=future_upgrade_context,
            supported_financing_structures=[structure for structure in EnergyPassportFinancingStructure],
            supported_transfer_relevance_flags=[flag for flag in EnergyPassportTransferRelevanceFlag],
            source_basis=self._basis(
                source_refs=all_source_refs,
                system_refs=[system.system_type.value for system in systems],
                obligation_refs=[obligation.system_type.value for obligation in obligations],
                transfer_refs=[flag.value for flag in EnergyPassportTransferRelevanceFlag],
                planning_history_refs=planning_history_refs,
                post_install_refs=post_install_refs,
                future_upgrade_refs=future_upgrade_refs,
                missing_input_refs=transfer_readiness.missing_transfer_inputs,
                blocker_refs=ownership_context.blockers + post_install_context.blockers + future_upgrade_context.blockers,
                unavailable_source_refs=unavailable_sources,
            ),
            assumptions=[
                "Ownership, financing, transfer, warranty, permit, payoff, lien, UCC, title, tax, appraisal, and underwriting values are not validated.",
                "Financing structures and transfer relevance flags are supported vocabulary, not detected obligations unless future source-backed records are added.",
            ],
            limitations=ENERGY_PASSPORT_LIMITATIONS,
            deferred_boundaries=ENERGY_PASSPORT_DEFERRED_BOUNDARIES,
            capability_boundary_flags={
                "read_only": scope.read_only,
                "additive_only": scope.additive_only,
                "request_time_only": scope.request_time_only,
                "home_id_anchored": scope.home_id_anchored,
                "deterministic_for_same_inputs": scope.deterministic_for_same_inputs,
                "non_authoritative": scope.non_authoritative,
                "title_claim_present": scope.title_claim_present,
                "escrow_claim_present": scope.escrow_claim_present,
                "deed_claim_present": scope.deed_claim_present,
                "lease_assignment_present": scope.lease_assignment_present,
                "payoff_calculation_present": scope.payoff_calculation_present,
                "lien_ucc_title_search_present": scope.lien_ucc_title_search_present,
                "warranty_validation_present": scope.warranty_validation_present,
                "permit_validation_present": scope.permit_validation_present,
                "appraisal_present": scope.appraisal_present,
                "underwriting_present": scope.underwriting_present,
                "tax_advice_present": scope.tax_advice_present,
                "financial_conclusion_present": scope.financial_conclusion_present,
                "crm_write_present": scope.crm_write_present,
                "persistence_present": scope.persistence_present,
                "migrations_present": scope.migrations_present,
                "auth_security_changes_present": scope.auth_security_changes_present,
                "permission_enforcement_present": scope.permission_enforcement_present,
                "deploy_present": scope.deploy_present,
                "push_present": scope.push_present,
            },
            compatibility_note="Existing Phase 6 through Phase 13 routes remain unchanged.",
        )


energy_passport_service = EnergyPassportService()

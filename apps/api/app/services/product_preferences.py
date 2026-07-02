from collections import Counter
from typing import Dict, List, Optional

from app.core.types import ConfidenceLevel
from app.product_preferences.schemas import (
    ProductPreferenceBlocker,
    ProductPreferenceBlockerCategory,
    ProductPreferenceCategory,
    ProductPreferenceCategoryId,
    ProductPreferenceScope,
    ProductPreferenceSourceBasis,
    ProductPreferencesSummary,
    ProductPreferenceStatus,
    ProductPreferencesView,
)

PRODUCT_PREFERENCE_LIMITATIONS = [
    "Product preference guidance is read-only planning metadata for review preparation only.",
    "It does not select products, rank products, choose a best option, create purchase links, procure equipment, or check live inventory.",
    "It does not create prices, quotes, bids, proposals, final estimates, final bills of materials, final electrical designs, certifications, or warranty claims.",
    "Every category remains subject to contractor, manufacturer, AHJ, utility, and field-verification review where applicable.",
    "Homeowner and contractor text are wording metadata only and are not permission-enforced views.",
]

PRODUCT_PREFERENCE_DEFERRED_BOUNDARIES = [
    "ahj_approval",
    "auth",
    "best_option_selection",
    "billing",
    "crm_handoff",
    "distributor_quotes",
    "email_automation",
    "external_services",
    "final_bill_of_materials",
    "final_design",
    "final_electrical_sizing",
    "final_product_recommendation",
    "frontend",
    "inventory",
    "manufacturer_certification_claims",
    "migrations",
    "payments",
    "permission_enforcement",
    "persistence",
    "pricing",
    "procurement",
    "product_ranking",
    "purchase_links",
    "secrets",
    "utility_approval",
    "warranty_claims",
    "write_endpoints",
]


class ProductPreferencesService:
    def _sorted_unique(self, values: List[str]) -> List[str]:
        return sorted({value for value in values if value})

    def _basis(
        self,
        *,
        source_refs: Optional[List[str]] = None,
        product_type_refs: Optional[List[str]] = None,
        compatibility_path_refs: Optional[List[str]] = None,
        takeoff_line_refs: Optional[List[str]] = None,
        estimate_gate_refs: Optional[List[str]] = None,
        option_candidate_refs: Optional[List[str]] = None,
        missing_input_refs: Optional[List[str]] = None,
        blocker_refs: Optional[List[str]] = None,
        assumption_refs: Optional[List[str]] = None,
        deferred_boundary_refs: Optional[List[str]] = None,
        unavailable_source_refs: Optional[List[str]] = None,
        basis_quality: str = "request_time_derived_from_existing_phase_7_11_views",
    ) -> ProductPreferenceSourceBasis:
        return ProductPreferenceSourceBasis(
            source_views=[
                "TwinPlanningContext",
                "TwinSharedCompatibilityView",
                "TwinTopologyTakeoffView",
                "EstimateReadinessView",
                "ProposalOptionSetsView",
            ],
            source_fields=[
                "TwinPlanningContext.sections",
                "TwinSharedCompatibilityView.compatibility_paths",
                "TwinTopologyTakeoffView.line_items",
                "EstimateReadinessView.confirmation_gates",
                "EstimateReadinessView.missing_inputs",
                "ProposalOptionSetsView.option_candidates",
            ],
            source_refs=self._sorted_unique(source_refs or []),
            product_type_refs=self._sorted_unique(product_type_refs or []),
            compatibility_path_refs=self._sorted_unique(compatibility_path_refs or []),
            takeoff_line_refs=self._sorted_unique(takeoff_line_refs or []),
            estimate_gate_refs=self._sorted_unique(estimate_gate_refs or []),
            option_candidate_refs=self._sorted_unique(option_candidate_refs or []),
            missing_input_refs=self._sorted_unique(missing_input_refs or []),
            blocker_refs=self._sorted_unique(blocker_refs or []),
            assumption_refs=self._sorted_unique(assumption_refs or []),
            deferred_boundary_refs=self._sorted_unique(deferred_boundary_refs or []),
            unavailable_source_refs=self._sorted_unique(unavailable_source_refs or []),
            basis_quality=basis_quality,
            request_time_derived=True,
            verified_fact_claim_present=False,
            limitations=PRODUCT_PREFERENCE_LIMITATIONS,
        )

    def _product_type_refs(self, context) -> Dict[str, List[str]]:
        product_type_by_id: Dict[str, str] = {}
        product_ref_by_id: Dict[str, str] = {}
        refs_by_type: Dict[str, List[str]] = {}
        for section in context.sections:
            for record in section.records:
                record_ref = f"{section.section_key}:{record.entity_type}:{record.entity_id}"
                payload = record.record or {}
                if record.entity_type == "equipment_product":
                    product_type = str(payload.get("product_type") or "").lower()
                    if not product_type:
                        continue
                    if record.entity_id:
                        product_type_by_id[record.entity_id] = product_type
                        product_ref_by_id[record.entity_id] = record_ref
                    refs_by_type.setdefault(product_type, []).append(record_ref)
        for section in context.sections:
            for record in section.records:
                if record.entity_type != "design_equipment":
                    continue
                payload = record.record or {}
                product_id = str(payload.get("product_id") or "")
                product_type = product_type_by_id.get(product_id)
                if not product_type:
                    continue
                record_ref = f"{section.section_key}:{record.entity_type}:{record.entity_id}"
                refs_by_type.setdefault(product_type, []).extend([record_ref, product_ref_by_id.get(product_id, "")])
        return {
            product_type: self._sorted_unique(refs)
            for product_type, refs in refs_by_type.items()
        }

    def _line_by_category(self, topology_takeoff) -> Dict[str, object]:
        return {
            line.category.value: line
            for line in topology_takeoff.line_items
        }

    def _paths_by_key(self, shared_compatibility) -> Dict[str, object]:
        return {
            path.path_key: path
            for path in shared_compatibility.compatibility_paths
        }

    def _blocker(
        self,
        *,
        blocker_id: str,
        category_id: ProductPreferenceCategoryId,
        blocker_category: ProductPreferenceBlockerCategory,
        severity: str,
        source_refs: Optional[List[str]] = None,
        gate_refs: Optional[List[str]] = None,
        missing_inputs: Optional[List[str]] = None,
        homeowner_explanation: str,
        contractor_review_prompt: str,
    ) -> ProductPreferenceBlocker:
        return ProductPreferenceBlocker(
            blocker_id=blocker_id,
            category_id=category_id,
            blocker_category=blocker_category,
            severity=severity,
            source_refs=self._sorted_unique(source_refs or []),
            gate_refs=self._sorted_unique(gate_refs or []),
            missing_inputs=self._sorted_unique(missing_inputs or []),
            homeowner_explanation=homeowner_explanation,
            contractor_review_prompt=contractor_review_prompt,
        )

    def _status(self, *, has_source: bool, missing_inputs: List[str], blockers: List[ProductPreferenceBlocker]) -> ProductPreferenceStatus:
        if not has_source:
            return ProductPreferenceStatus.source_limited
        if any(blocker.blocker_category == ProductPreferenceBlockerCategory.source_context_unavailable for blocker in blockers):
            return ProductPreferenceStatus.unavailable
        if missing_inputs:
            return ProductPreferenceStatus.blocked_by_missing_inputs
        if blockers:
            return ProductPreferenceStatus.review_required
        return ProductPreferenceStatus.review_guidance_available

    def _category_from_line(
        self,
        *,
        category_id: ProductPreferenceCategoryId,
        category_label: str,
        line,
        compatibility_paths: Optional[List[object]] = None,
        product_refs: Optional[List[str]] = None,
        planning_direction: str,
        install_logic: List[str],
        homeowner_explanation: str,
        contractor_review_prompt: str,
        assumption_refs: Optional[List[str]] = None,
    ) -> ProductPreferenceCategory:
        paths = compatibility_paths or []
        missing_inputs = self._sorted_unique(
            line.missing_information
            + [missing for path in paths for missing in path.missing_information]
        )
        gate_ids = self._sorted_unique(
            line.required_confirmations
            + line.contractor_confirmation_gates
            + [gate for path in paths for gate in path.required_confirmations]
            + [gate for path in paths for gate in path.contractor_confirmation_gates]
        )
        source_refs = self._sorted_unique(
            line.basis.source_refs
            + [ref for path in paths for ref in path.basis.source_refs]
            + (product_refs or [])
        )
        blocker_ids = self._sorted_unique(
            line.blockers
            + [blocker for path in paths for blocker in path.blockers]
        )
        blockers = [
            self._blocker(
                blocker_id=f"{category_id.value}:missing_inputs",
                category_id=category_id,
                blocker_category=ProductPreferenceBlockerCategory.missing_input,
                severity="review_required",
                source_refs=source_refs,
                gate_refs=gate_ids,
                missing_inputs=missing_inputs,
                homeowner_explanation="More product or site information is needed before this category can support selection review.",
                contractor_review_prompt="Review prompt only: resolve missing product, topology, site, and manufacturer inputs before using this category.",
            )
        ] if missing_inputs else []
        blockers.extend(
            self._blocker(
                blocker_id=f"{category_id.value}:source_blocker:{blocker_id}",
                category_id=category_id,
                blocker_category=ProductPreferenceBlockerCategory.confirmation_gate_open,
                severity="review_required",
                source_refs=source_refs,
                gate_refs=gate_ids,
                homeowner_explanation="This category has review gates that remain open in the current planning context.",
                contractor_review_prompt=f"Review prompt only: verify open gate or blocker '{blocker_id}' before product selection work.",
            )
            for blocker_id in blocker_ids
        )
        basis = self._basis(
            source_refs=source_refs,
            product_type_refs=product_refs or [],
            compatibility_path_refs=[path.path_key for path in paths],
            takeoff_line_refs=[line.line_id],
            estimate_gate_refs=gate_ids,
            missing_input_refs=missing_inputs,
            blocker_refs=[blocker.blocker_id for blocker in blockers],
            assumption_refs=assumption_refs or [],
            deferred_boundary_refs=PRODUCT_PREFERENCE_DEFERRED_BOUNDARIES,
            basis_quality=f"{category_id.value}_from_topology_takeoff_and_compatibility_context",
        )
        return ProductPreferenceCategory(
            category_id=category_id,
            category_label=category_label,
            status=self._status(has_source=True, missing_inputs=missing_inputs, blockers=blockers),
            confidence_level=ConfidenceLevel.low if missing_inputs or blockers else ConfidenceLevel.medium,
            planning_direction=planning_direction,
            install_logic=install_logic,
            homeowner_explanation=homeowner_explanation,
            contractor_review_prompt=contractor_review_prompt,
            source_basis=basis,
            missing_inputs=missing_inputs,
            blockers=sorted(blockers, key=lambda blocker: blocker.blocker_id),
            confirmation_gate_ids=gate_ids,
            assumptions=self._sorted_unique(
                [
                    "Category guidance is derived from existing planning context only.",
                    "No unsupported product facts, product rankings, or final selections are inferred.",
                ]
                + (assumption_refs or [])
            ),
            deferred_boundaries=sorted(PRODUCT_PREFERENCE_DEFERRED_BOUNDARIES),
            limitations=PRODUCT_PREFERENCE_LIMITATIONS,
        )

    def _source_limited_category(
        self,
        *,
        category_id: ProductPreferenceCategoryId,
        category_label: str,
        missing_inputs: List[str],
        planning_direction: str,
        homeowner_explanation: str,
        contractor_review_prompt: str,
    ) -> ProductPreferenceCategory:
        blockers = [
            self._blocker(
                blocker_id=f"{category_id.value}:source_limited",
                category_id=category_id,
                blocker_category=ProductPreferenceBlockerCategory.unsupported_context,
                severity="source_limited",
                missing_inputs=missing_inputs,
                homeowner_explanation="The current planning record does not include enough supported context for this category.",
                contractor_review_prompt="Review prompt only: capture supported source context before using this category.",
            )
        ]
        basis = self._basis(
            missing_input_refs=missing_inputs,
            blocker_refs=[blocker.blocker_id for blocker in blockers],
            assumption_refs=[f"{category_id.value}_not_represented_in_current_supported_context"],
            deferred_boundary_refs=PRODUCT_PREFERENCE_DEFERRED_BOUNDARIES,
            basis_quality=f"{category_id.value}_source_limited_no_supported_input",
        )
        return ProductPreferenceCategory(
            category_id=category_id,
            category_label=category_label,
            status=ProductPreferenceStatus.source_limited,
            confidence_level=ConfidenceLevel.low,
            planning_direction=planning_direction,
            install_logic=["Do not infer this category from unsupported context."],
            homeowner_explanation=homeowner_explanation,
            contractor_review_prompt=contractor_review_prompt,
            source_basis=basis,
            missing_inputs=self._sorted_unique(missing_inputs),
            blockers=blockers,
            assumptions=[
                "No supported structured input is present for this category.",
                "Unsupported preferences are surfaced as missing rather than inferred.",
            ],
            deferred_boundaries=sorted(PRODUCT_PREFERENCE_DEFERRED_BOUNDARIES),
            limitations=PRODUCT_PREFERENCE_LIMITATIONS,
        )

    def _battery_coupling_direction(self, product_refs_by_type: Dict[str, List[str]]) -> str:
        has_battery = bool(product_refs_by_type.get("battery"))
        has_hybrid = bool(product_refs_by_type.get("hybrid_inverter"))
        has_ac_solar_conversion = bool(
            product_refs_by_type.get("microinverter") or product_refs_by_type.get("string_inverter")
        )
        if has_battery and has_hybrid and has_ac_solar_conversion:
            return "Recorded context supports mixed AC-coupled and hybrid/DC-coupled review; selection remains contractor/manufacturer-confirmed."
        if has_battery and has_hybrid:
            return "Recorded hybrid inverter and battery context supports hybrid/DC-coupled review only as planning guidance."
        if has_battery and has_ac_solar_conversion:
            return "Recorded AC solar conversion and battery context supports AC-coupled battery retrofit review only as planning guidance."
        if has_battery:
            return "Recorded battery context exists, but coupling posture needs inverter and manufacturer review."
        return "Battery coupling cannot be derived because battery context is not represented."

    def _inverter_direction(self, product_refs_by_type: Dict[str, List[str]]) -> str:
        inverter_types = [
            label
            for label in ["microinverter", "string_inverter", "hybrid_inverter"]
            if product_refs_by_type.get(label)
        ]
        if inverter_types:
            return (
                "Recorded inverter topology context includes "
                + ", ".join(inverter_types)
                + "; treat this as review guidance, not a product selection."
            )
        return "Inverter topology cannot be derived because inverter context is not represented."

    def _categories(self, *, context, shared_compatibility, topology_takeoff) -> List[ProductPreferenceCategory]:
        product_refs_by_type = self._product_type_refs(context)
        lines = self._line_by_category(topology_takeoff)
        paths = self._paths_by_key(shared_compatibility)

        def line_or_limited(category_key, category_id, label, missing, direction, homeowner, contractor):
            line = lines.get(category_key)
            if line is None:
                return self._source_limited_category(
                    category_id=category_id,
                    category_label=label,
                    missing_inputs=missing,
                    planning_direction=direction,
                    homeowner_explanation=homeowner,
                    contractor_review_prompt=contractor,
                )
            return self._category_from_line(
                category_id=category_id,
                category_label=label,
                line=line,
                product_refs=[],
                planning_direction=direction,
                install_logic=[
                    "Use existing topology/takeoff context as a review checklist only.",
                    "Confirm product specs, manufacturer requirements, site conditions, and authority-dependent constraints before selection work.",
                ],
                homeowner_explanation=homeowner,
                contractor_review_prompt=contractor,
            )

        categories = [
            line_or_limited(
                "pv_source_circuit_array_side",
                ProductPreferenceCategoryId.pv_modules,
                "PV modules",
                ["solar_panel_product_context", "roof_or_array_layout_context", "manufacturer_module_specs"],
                "PV module preference is limited to planning review of existing PV scope and missing module/layout inputs.",
                "PV module details are not selected here; this view shows what context is available for later review.",
                "Review prompt only: verify module specs, layout constraints, mounting context, and product compatibility outside this response.",
            ),
            line_or_limited(
                "inverter_power_electronics",
                ProductPreferenceCategoryId.inverter_topology,
                "Inverter topology",
                ["inverter_product_context", "power_electronics_location", "manufacturer_inverter_specs"],
                self._inverter_direction(product_refs_by_type),
                "Inverter topology is planning guidance based on recorded context, not a selected inverter design.",
                "Review prompt only: compare recorded inverter topology with manufacturer specs, backup architecture, and field conditions.",
            ),
            line_or_limited(
                "inverter_power_electronics",
                ProductPreferenceCategoryId.microinverter_string_hybrid_direction,
                "Microinverter / string / hybrid direction",
                ["microinverter_string_or_hybrid_context", "manufacturer_inverter_specs"],
                self._inverter_direction(product_refs_by_type),
                "Microinverter, string, or hybrid direction remains review metadata until product specs and topology are confirmed.",
                "Review prompt only: confirm whether current records support microinverter, string, hybrid, or unresolved topology before selection work.",
            ),
            line_or_limited(
                "battery_ess",
                ProductPreferenceCategoryId.battery_coupling,
                "AC-coupled vs DC-coupled battery direction",
                ["battery_product_context", "inverter_coupling_context", "manufacturer_battery_specs"],
                self._battery_coupling_direction(product_refs_by_type),
                "Battery coupling guidance is planning-only and depends on recorded inverter and battery context.",
                "Review prompt only: confirm AC-coupled, hybrid/DC-coupled, or unresolved coupling with manufacturer documents and site topology.",
            ),
            self._category_from_line(
                category_id=ProductPreferenceCategoryId.backup_scope,
                category_label="Partial-home vs whole-home backup direction",
                line=lines.get("panel_subpanel_load_center") or lines.get("backup_interface_gateway_transfer"),
                compatibility_paths=[
                    path
                    for path in [
                        paths.get("pv_battery_partial_backup"),
                        paths.get("pv_battery_whole_home_backup"),
                        paths.get("critical_loads_subpanel"),
                    ]
                    if path is not None
                ],
                planning_direction="Backup scope remains a planning posture comparing partial-home and whole-home path evidence without choosing a final design.",
                install_logic=[
                    "Treat partial-home and whole-home paths as review contexts.",
                    "Confirm backed-up loads, panel topology, utility/AHJ requirements, and contractor field conditions before design use.",
                ],
                homeowner_explanation="Backup scope is shown as planning context only; it is not a final backup design.",
                contractor_review_prompt="Review prompt only: verify backed-up loads, critical-loads panel implications, and whole-home service constraints.",
                assumption_refs=["backup_scope_derived_from_phase_7_paths_and_phase_8_panel_or_gateway_scope"],
            )
            if (lines.get("panel_subpanel_load_center") or lines.get("backup_interface_gateway_transfer"))
            else self._source_limited_category(
                category_id=ProductPreferenceCategoryId.backup_scope,
                category_label="Partial-home vs whole-home backup direction",
                missing_inputs=["backup_load_context", "panel_or_gateway_scope", "partial_or_whole_home_path_context"],
                planning_direction="Backup scope cannot be derived without supported backup load and panel/gateway context.",
                homeowner_explanation="Backup scope is not available from the current planning record.",
                contractor_review_prompt="Review prompt only: capture backup loads, panel topology, and transfer/gateway context before backup-scope review.",
            ),
            line_or_limited(
                "backup_interface_gateway_transfer",
                ProductPreferenceCategoryId.gateway_transfer_equipment,
                "Gateway / transfer equipment implications",
                ["battery_or_generator_context", "backup_load_context", "manufacturer_gateway_or_transfer_requirements"],
                "Gateway or transfer equipment implications are review metadata tied to backup-interface scope evidence.",
                "Gateway or transfer equipment is not selected here; only planning implications are surfaced.",
                "Review prompt only: verify gateway, transfer, disconnect, and interlock requirements outside this response.",
            ),
            line_or_limited(
                "panel_subpanel_load_center",
                ProductPreferenceCategoryId.backup_loads_panel,
                "Backup loads panel implications",
                ["panel_context", "backup_load_context", "circuit_purpose_confirmation"],
                "Backup-loads panel guidance remains a review posture based on panel/subpanel and load context.",
                "Panel implications are planning-only and not final electrical design.",
                "Review prompt only: verify panel space, critical-loads circuits, subpanel needs, and overcurrent protection outside this response.",
            ),
            line_or_limited(
                "monitoring_communications",
                ProductPreferenceCategoryId.monitoring_controls,
                "Monitoring / controls",
                ["monitoring_or_controls_context", "manufacturer_communications_requirements"],
                "Monitoring and controls guidance is limited to existing communications scope evidence and missing manufacturer requirements.",
                "Monitoring and controls are not selected here; this view shows review context only.",
                "Review prompt only: verify communications, gateway/control integrations, and manufacturer requirements before selection work.",
            ),
            self._source_limited_category(
                category_id=ProductPreferenceCategoryId.ev_charger_readiness,
                category_label="EV charger readiness",
                missing_inputs=["ev_charger_context_not_recorded"],
                planning_direction="EV charger readiness is not represented in current supported context.",
                homeowner_explanation="EV charger readiness is not inferred because no supported EV charger context is recorded.",
                contractor_review_prompt="Review prompt only: capture EV charger load, circuit, panel, and product context before EV charger review.",
            )
            if not product_refs_by_type.get("ev_charger")
            else self._source_limited_category(
                category_id=ProductPreferenceCategoryId.ev_charger_readiness,
                category_label="EV charger readiness",
                missing_inputs=["ev_charger_install_requirements", "panel_capacity_review"],
                planning_direction="EV charger context is recorded, but install readiness still needs panel and product review.",
                homeowner_explanation="EV charger readiness is represented only as planning context.",
                contractor_review_prompt="Review prompt only: verify EV charger circuit, load management, and panel capacity outside this response.",
            ),
            self._category_from_line(
                category_id=ProductPreferenceCategoryId.main_service_panel_subpanel,
                category_label="Main service panel / subpanel implications",
                line=lines.get("panel_subpanel_load_center"),
                compatibility_paths=[
                    path
                    for path in [paths.get("service_upgrade_likely"), paths.get("existing_panel_reuse")]
                    if path is not None
                ],
                planning_direction="Main service panel and subpanel implications are planning guidance based on current panel/path evidence.",
                install_logic=[
                    "Use panel and service path evidence as review prompts only.",
                    "Confirm service capacity, available spaces, subpanel needs, and authority requirements before design use.",
                ],
                homeowner_explanation="Panel and subpanel implications are not final electrical design.",
                contractor_review_prompt="Review prompt only: verify panel/service constraints, subpanel needs, and utility/AHJ requirements.",
                assumption_refs=["panel_implications_derived_from_phase_7_paths_and_phase_8_panel_scope"],
            )
            if lines.get("panel_subpanel_load_center")
            else self._source_limited_category(
                category_id=ProductPreferenceCategoryId.main_service_panel_subpanel,
                category_label="Main service panel / subpanel implications",
                missing_inputs=["panel_context", "service_capacity_context"],
                planning_direction="Panel/subpanel implications cannot be derived without supported panel context.",
                homeowner_explanation="Panel and subpanel implications are not available from current context.",
                contractor_review_prompt="Review prompt only: capture panel/service context before panel/subpanel review.",
            ),
            self._source_limited_category(
                category_id=ProductPreferenceCategoryId.aesthetic_preference,
                category_label="Aesthetic preference",
                missing_inputs=["homeowner_aesthetic_preference_not_recorded"],
                planning_direction="Aesthetic preference is not represented in current supported context.",
                homeowner_explanation="Aesthetic preferences are not inferred because no supported preference field is recorded.",
                contractor_review_prompt="Review prompt only: capture homeowner-visible placement or finish preferences before using aesthetic criteria.",
            ),
            self._source_limited_category(
                category_id=ProductPreferenceCategoryId.contractor_preferred_product_family,
                category_label="Contractor-preferred product family",
                missing_inputs=["contractor_preferred_product_family_not_recorded"],
                planning_direction="Contractor-preferred product family is not represented in current supported context.",
                homeowner_explanation="Contractor product-family preferences are not inferred from product catalog or seed data.",
                contractor_review_prompt="Review prompt only: capture contractor-stated product-family preference with provenance before using it.",
            ),
        ]
        return categories

    def build_home_product_preferences(self, db, home_id: str) -> Optional[ProductPreferencesView]:
        from app.services.estimate_readiness import estimate_readiness_service
        from app.services.proposal_option_sets import proposal_option_sets_service
        from app.services.twin_planning_context import twin_planning_context_service

        context = twin_planning_context_service.build(db, home_id)
        if context is None:
            return None

        shared_compatibility = twin_planning_context_service.build_shared_compatibility_view(db, home_id)
        topology_takeoff = twin_planning_context_service.build_topology_takeoff_view(db, home_id)
        estimate_view = estimate_readiness_service.build_home_estimate_readiness(db, home_id)
        proposal_view = proposal_option_sets_service.build_home_proposal_option_sets(db, home_id)
        unavailable_sources = [
            source_name
            for source_name, source_value in [
                ("TwinSharedCompatibilityView", shared_compatibility),
                ("TwinTopologyTakeoffView", topology_takeoff),
                ("EstimateReadinessView", estimate_view),
                ("ProposalOptionSetsView", proposal_view),
            ]
            if source_value is None
        ]
        if unavailable_sources:
            source_basis = self._basis(
                source_refs=[section.section_key for section in context.sections],
                unavailable_source_refs=unavailable_sources,
                basis_quality="source_unavailable_for_phase_12_product_preferences",
            )
            blocker = self._blocker(
                blocker_id="source_unavailable:phase_12_product_preferences",
                category_id=ProductPreferenceCategoryId.pv_modules,
                blocker_category=ProductPreferenceBlockerCategory.source_context_unavailable,
                severity="unavailable",
                source_refs=unavailable_sources,
                homeowner_explanation="Product preference guidance could not be assembled because source planning views were unavailable.",
                contractor_review_prompt="Review prompt only: rebuild source planning views before product preference review.",
            )
            summary = ProductPreferencesSummary(
                overall_status=ProductPreferenceStatus.unavailable,
                confidence_level=ConfidenceLevel.low,
                category_count=0,
                blocker_count=1,
                summary_boundary_note="Product preference guidance is source-limited and non-authoritative.",
            )
            return ProductPreferencesView(
                home_id=home_id,
                implementation_boundary="Read-only Phase 12 product preference view. Source readiness metadata was unavailable.",
                preference_scope=ProductPreferenceScope(limitations=PRODUCT_PREFERENCE_LIMITATIONS),
                summary=summary,
                blockers=[blocker],
                homeowner_summary="Product preference guidance is unavailable because source planning views are incomplete.",
                contractor_summary="Source planning views are unavailable for product preference review.",
                contractor_review_prompts=[blocker.contractor_review_prompt],
                source_basis=source_basis,
                blocker_category_counts={blocker.blocker_category.value: 1},
                assumptions=["A home record exists, but one or more source views were unavailable."],
                limitations=PRODUCT_PREFERENCE_LIMITATIONS,
                deferred_boundaries=sorted(PRODUCT_PREFERENCE_DEFERRED_BOUNDARIES),
                compatibility_note="Existing Phase 7 through Phase 11 routes remain unchanged.",
            )

        categories = self._categories(
            context=context,
            shared_compatibility=shared_compatibility,
            topology_takeoff=topology_takeoff,
        )
        categories = sorted(categories, key=lambda category: category.category_id.value)
        blockers = sorted(
            [blocker for category in categories for blocker in category.blockers],
            key=lambda blocker: blocker.blocker_id,
        )
        missing_inputs = self._sorted_unique(
            [missing for category in categories for missing in category.missing_inputs]
            + estimate_view.missing_inputs
            + proposal_view.missing_inputs
        )
        confirmation_gate_ids = self._sorted_unique(
            [gate for category in categories for gate in category.confirmation_gate_ids]
            + [gate.gate_id for gate in estimate_view.confirmation_gates]
            + proposal_view.confirmation_gate_ids
        )
        source_limited_count = sum(
            1 for category in categories if category.status == ProductPreferenceStatus.source_limited
        )
        if source_limited_count == len(categories):
            overall_status = ProductPreferenceStatus.source_limited
        elif blockers or missing_inputs:
            overall_status = ProductPreferenceStatus.blocked_by_missing_inputs
        else:
            overall_status = ProductPreferenceStatus.review_guidance_available
        source_basis = self._basis(
            source_refs=[section.section_key for section in context.sections],
            product_type_refs=[
                ref
                for refs in self._product_type_refs(context).values()
                for ref in refs
            ],
            compatibility_path_refs=[path.path_key for path in shared_compatibility.compatibility_paths],
            takeoff_line_refs=[line.line_id for line in topology_takeoff.line_items],
            estimate_gate_refs=confirmation_gate_ids,
            option_candidate_refs=[candidate.option_candidate_id for candidate in proposal_view.option_candidates],
            missing_input_refs=missing_inputs,
            blocker_refs=[blocker.blocker_id for blocker in blockers],
            assumption_refs=["phase_12_categories_are_fixed_and_request_time_derived"],
            deferred_boundary_refs=PRODUCT_PREFERENCE_DEFERRED_BOUNDARIES,
            basis_quality="home_level_phase_12_product_preference_rollup",
        )
        summary = ProductPreferencesSummary(
            overall_status=overall_status,
            confidence_level=ConfidenceLevel.low if blockers or missing_inputs else ConfidenceLevel.medium,
            category_count=len(categories),
            source_limited_category_count=source_limited_count,
            blocker_count=len(blockers),
            missing_input_count=len(missing_inputs),
            confirmation_gate_count=len(confirmation_gate_ids),
            contractor_review_required=True,
            product_selection_allowed=False,
            procurement_allowed=False,
            pricing_allowed=False,
            final_design_allowed=False,
            summary_boundary_note=(
                "Product preference guidance is a read-only planning layer. It is not product selection, product ranking, "
                "procurement, pricing, live inventory, a final bill of materials, a final electrical design, or authorization."
            ),
        )
        return ProductPreferencesView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 12 product preference and install-logic view built request-time from existing Phase 7 shared "
                "compatibility, Phase 8 topology takeoff, Phase 9 estimate readiness, and Phase 10 proposal option-set metadata. "
                "It does not write data, persist state, run migrations, enforce permissions, "
                "create frontend behavior, price work, check live inventory, request distributor quotes, procure products, create "
                "purchase links, create payments, produce final bills of materials, produce final electrical designs, select final "
                "products, rank products, choose a best option, claim manufacturer certification or warranty coverage, create CRM "
                "handoff, automate email, use external services, add secrets, create twin_id, create graph behavior, or create "
                "operational behavior."
            ),
            preference_scope=ProductPreferenceScope(limitations=PRODUCT_PREFERENCE_LIMITATIONS),
            summary=summary,
            categories=categories,
            blockers=blockers,
            missing_inputs=missing_inputs,
            confirmation_gate_ids=confirmation_gate_ids,
            homeowner_summary=(
                "Product preference guidance summarizes planning context and missing inputs for later review; it does not select products."
            ),
            contractor_summary=(
                f"Product preference guidance includes {len(categories)} categories, {len(blockers)} blockers, "
                f"{len(missing_inputs)} missing inputs, and {len(confirmation_gate_ids)} confirmation gates for review preparation."
            ),
            contractor_review_prompts=[category.contractor_review_prompt for category in categories],
            source_basis=source_basis,
            blocker_category_counts=dict(sorted(Counter(blocker.blocker_category.value for blocker in blockers).items())),
            assumptions=[
                "Product preference categories are fixed and sorted deterministically.",
                "Existing Phase 7 through Phase 11 source views are authoritative over this derived layer.",
                "Unsupported categories are shown as source-limited rather than inferred.",
            ],
            limitations=PRODUCT_PREFERENCE_LIMITATIONS,
            deferred_boundaries=sorted(PRODUCT_PREFERENCE_DEFERRED_BOUNDARIES),
            compatibility_note=(
                "Existing shared-compatibility, topology-takeoff, estimate-readiness, proposal-option-set, contractor-workflow, "
                "product-library, scenario, takeoff, and design routes remain unchanged."
            ),
        )


product_preferences_service = ProductPreferencesService()

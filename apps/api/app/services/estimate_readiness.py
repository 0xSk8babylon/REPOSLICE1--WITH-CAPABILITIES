from collections import Counter
from typing import Dict, List, Optional, Tuple

from app.core.repository import repository
from app.core.types import ConfidenceLevel
from app.estimate_readiness.schemas import (
    EstimateBlockerCategory,
    EstimateConfirmationGate,
    EstimateConfirmationGateStatus,
    EstimateReadinessBasis,
    EstimateReadinessBlocker,
    EstimateReadinessScope,
    EstimateReadinessStatus,
    EstimateReadinessSummary,
    EstimateReadinessView,
    ScenarioEstimateReadinessStatus,
)


ESTIMATE_READINESS_GATE_REGISTRY_VERSION = "phase_9_confirmation_gate_registry_v1"

ESTIMATE_READINESS_LIMITATIONS = [
    "Estimate readiness is read-only planning readiness metadata only.",
    "It does not generate proposals, prices, quotes, bids, final estimates, final bills of materials, or contractor-approved scope.",
    "It does not perform or approve electrical design, NEC compliance, permit design, AHJ approval, utility approval, field verification, or contractor final review.",
    "Homeowner-facing text is simplified and hides contractor-only calculation details; it is not a permission-enforced view.",
    "Contractor-facing notes are review prompts only and are not instructions, stamped design, or authority approval.",
]

ESTIMATE_READINESS_DEFERRED_BOUNDARIES = [
    "ahj_approval",
    "auth",
    "billing",
    "contractor_approved_scope",
    "contractor_final_review_completion",
    "exports",
    "field_verification_completion",
    "final_bill_of_materials",
    "final_design",
    "final_estimate",
    "migrations",
    "permission_enforcement",
    "permit_ready_design",
    "persistence",
    "pricing",
    "proposal_generation",
    "twin_id",
    "utility_approval",
    "write_endpoints",
]

GATE_MISSING_INPUTS: Dict[str, List[str]] = {
    "product_specs_verified": ["manufacturer_spec_sheets", "model_specific_product_specs"],
    "nameplate_ratings_verified": ["equipment_nameplate_photos_or_recorded_ratings"],
    "manufacturer_install_manual_reviewed": ["manufacturer_install_manuals"],
    "circuit_purpose_confirmed": ["field_confirmed_circuit_purpose"],
    "load_current_assumptions_confirmed": ["field_confirmed_load_current_assumptions"],
    "distance_measurements_confirmed": ["field_measured_route_distances"],
    "conduit_routing_path_confirmed": ["field_confirmed_routing_path"],
    "indoor_outdoor_wet_location_confirmed": ["field_confirmed_location_conditions"],
    "conductor_material_confirmed": ["selected_conductor_material"],
    "raceway_type_confirmed": ["selected_raceway_type"],
    "current_carrying_conductors_confirmed": ["current_carrying_conductor_count"],
    "derating_factors_applied": ["raceway_conditions", "conductor_count", "ambient_conditions", "derating_review"],
    "voltage_drop_reviewed": ["field_measured_distance", "load_current_basis", "voltage_drop_review"],
    "disconnect_requirements_reviewed": ["disconnect_requirement_review"],
    "overcurrent_protection_reviewed": ["overcurrent_protection_review"],
    "grounding_bonding_reviewed": ["grounding_bonding_review"],
    "labeling_signage_requirements_reviewed": ["labeling_signage_review"],
    "utility_ahj_requirements_reviewed": ["utility_requirements", "ahj_requirements"],
    "contractor_final_review_completed": ["contractor_final_review_record"],
}

GATE_BLOCKER_CATEGORIES: Dict[str, List[EstimateBlockerCategory]] = {
    "product_specs_verified": [EstimateBlockerCategory.missing_product_spec],
    "nameplate_ratings_verified": [EstimateBlockerCategory.missing_nameplate],
    "manufacturer_install_manual_reviewed": [EstimateBlockerCategory.missing_product_spec],
    "circuit_purpose_confirmed": [EstimateBlockerCategory.contractor_field_verification_required],
    "load_current_assumptions_confirmed": [
        EstimateBlockerCategory.unsafe_assumption,
        EstimateBlockerCategory.contractor_field_verification_required,
    ],
    "distance_measurements_confirmed": [EstimateBlockerCategory.missing_measurement],
    "conduit_routing_path_confirmed": [EstimateBlockerCategory.missing_measurement],
    "indoor_outdoor_wet_location_confirmed": [EstimateBlockerCategory.contractor_field_verification_required],
    "conductor_material_confirmed": [EstimateBlockerCategory.material_scope_incomplete],
    "raceway_type_confirmed": [EstimateBlockerCategory.material_scope_incomplete],
    "current_carrying_conductors_confirmed": [EstimateBlockerCategory.code_review_required],
    "derating_factors_applied": [EstimateBlockerCategory.code_review_required],
    "voltage_drop_reviewed": [EstimateBlockerCategory.code_review_required],
    "disconnect_requirements_reviewed": [EstimateBlockerCategory.code_review_required],
    "overcurrent_protection_reviewed": [EstimateBlockerCategory.code_review_required],
    "grounding_bonding_reviewed": [EstimateBlockerCategory.code_review_required],
    "labeling_signage_requirements_reviewed": [EstimateBlockerCategory.code_review_required],
    "utility_ahj_requirements_reviewed": [
        EstimateBlockerCategory.utility_review_required,
        EstimateBlockerCategory.ahj_review_required,
    ],
    "contractor_final_review_completed": [EstimateBlockerCategory.contractor_field_verification_required],
}

CONTRACTOR_ONLY_GATE_IDS = {"contractor_final_review_completed"}

COMPLEXITY_GATE_REQUIREMENTS: Dict[str, List[str]] = {
    "pv_only_or_basic_solar": [
        "product_specs_verified",
        "nameplate_ratings_verified",
        "manufacturer_install_manual_reviewed",
        "distance_measurements_confirmed",
        "conduit_routing_path_confirmed",
        "utility_ahj_requirements_reviewed",
        "contractor_final_review_completed",
    ],
    "battery_backup": [
        "product_specs_verified",
        "nameplate_ratings_verified",
        "manufacturer_install_manual_reviewed",
        "load_current_assumptions_confirmed",
        "distance_measurements_confirmed",
        "conduit_routing_path_confirmed",
        "disconnect_requirements_reviewed",
        "overcurrent_protection_reviewed",
        "grounding_bonding_reviewed",
        "utility_ahj_requirements_reviewed",
        "contractor_final_review_completed",
    ],
    "whole_home_backup": [
        "circuit_purpose_confirmed",
        "load_current_assumptions_confirmed",
        "current_carrying_conductors_confirmed",
        "derating_factors_applied",
        "voltage_drop_reviewed",
        "disconnect_requirements_reviewed",
        "overcurrent_protection_reviewed",
        "grounding_bonding_reviewed",
        "utility_ahj_requirements_reviewed",
        "contractor_final_review_completed",
    ],
    "generator_interlock_or_transfer": [
        "product_specs_verified",
        "nameplate_ratings_verified",
        "manufacturer_install_manual_reviewed",
        "disconnect_requirements_reviewed",
        "overcurrent_protection_reviewed",
        "grounding_bonding_reviewed",
        "labeling_signage_requirements_reviewed",
        "utility_ahj_requirements_reviewed",
        "contractor_final_review_completed",
    ],
    "long_or_uncertain_conduit_route": [
        "distance_measurements_confirmed",
        "conduit_routing_path_confirmed",
        "indoor_outdoor_wet_location_confirmed",
        "conductor_material_confirmed",
        "raceway_type_confirmed",
        "current_carrying_conductors_confirmed",
        "derating_factors_applied",
        "voltage_drop_reviewed",
        "contractor_final_review_completed",
    ],
    "wet_location_exterior_equipment": [
        "indoor_outdoor_wet_location_confirmed",
        "raceway_type_confirmed",
        "grounding_bonding_reviewed",
        "labeling_signage_requirements_reviewed",
        "contractor_final_review_completed",
    ],
    "service_upgrade_or_load_side_work": [
        "load_current_assumptions_confirmed",
        "disconnect_requirements_reviewed",
        "overcurrent_protection_reviewed",
        "utility_ahj_requirements_reviewed",
        "contractor_final_review_completed",
    ],
}


class EstimateReadinessService:
    def _sorted_unique(self, values: List[str]) -> List[str]:
        return sorted({value for value in values if value})

    def _basis(
        self,
        *,
        source_refs: Optional[List[str]] = None,
        gate_refs: Optional[List[str]] = None,
        takeoff_line_refs: Optional[List[str]] = None,
        compatibility_path_refs: Optional[List[str]] = None,
        scenario_refs: Optional[List[str]] = None,
        missing_input_refs: Optional[List[str]] = None,
        basis_quality: str = "request_time_derived_from_existing_phase_5_7_8_views",
        basis_notes: Optional[List[str]] = None,
    ) -> EstimateReadinessBasis:
        return EstimateReadinessBasis(
            source_views=[
                "TwinPlanningContext",
                "ContractorConfirmationGateProjectionView",
                "TwinSharedCompatibilityView",
                "TwinTopologyTakeoffView",
                "Scenario",
            ],
            source_fields=[
                "ContractorConfirmationGateProjectionView.gates",
                "TwinSharedCompatibilityView.compatibility_paths",
                "TwinTopologyTakeoffView.line_items",
                "TwinTopologyTakeoffView.missing_information",
                "TwinTopologyTakeoffView.blockers",
                "Scenario.home_id",
                "Scenario.linked_design_id",
            ],
            source_refs=self._sorted_unique(source_refs or []),
            gate_refs=self._sorted_unique(gate_refs or []),
            takeoff_line_refs=self._sorted_unique(takeoff_line_refs or []),
            compatibility_path_refs=self._sorted_unique(compatibility_path_refs or []),
            scenario_refs=self._sorted_unique(scenario_refs or []),
            missing_input_refs=self._sorted_unique(missing_input_refs or []),
            basis_quality=basis_quality,
            request_time_derived=True,
            verified_fact_claim_present=False,
            basis_notes=self._sorted_unique(
                basis_notes
                or [
                    "Readiness basis is assembled from existing read-only planning, gate, compatibility, and takeoff views.",
                    "Basis references are not field verification, contractor completion, AHJ approval, utility approval, or final estimate approval.",
                ]
            ),
            limitations=ESTIMATE_READINESS_LIMITATIONS,
        )

    def _gate_status(self, gate_id: str, source_status: str, blocker_level: str) -> EstimateConfirmationGateStatus:
        if source_status == "confirmed":
            return EstimateConfirmationGateStatus.confirmed
        if gate_id in CONTRACTOR_ONLY_GATE_IDS:
            return EstimateConfirmationGateStatus.contractor_only_final_review_required
        if source_status == "ahj_or_utility_dependent" or blocker_level == "blocked":
            return EstimateConfirmationGateStatus.authority_review_required
        if source_status == "contractor_review_required":
            return EstimateConfirmationGateStatus.contractor_review_required
        return EstimateConfirmationGateStatus.pending_confirmation

    def _confirmation_gate(self, source_gate) -> EstimateConfirmationGate:
        status = self._gate_status(source_gate.gate_id, source_gate.status, source_gate.blocker_level)
        missing_inputs = GATE_MISSING_INPUTS.get(source_gate.gate_id, [])
        blocker_categories = GATE_BLOCKER_CATEGORIES.get(source_gate.gate_id, [])
        homeowner_visible = source_gate.gate_id not in CONTRACTOR_ONLY_GATE_IDS
        return EstimateConfirmationGate(
            gate_id=source_gate.gate_id,
            gate_name=source_gate.title,
            gate_version=ESTIMATE_READINESS_GATE_REGISTRY_VERSION,
            category=source_gate.category,
            required_for_estimate=True,
            visible_to_homeowner=homeowner_visible,
            contractor_only_notes=(
                [
                    "Final contractor review is contractor-facing only and is not presented as homeowner-completed readiness.",
                    "The app cannot mark contractor review complete.",
                ]
                if not homeowner_visible
                else []
            ),
            status=status,
            basis=self._basis(
                source_refs=source_gate.provenance.source_refs,
                gate_refs=[source_gate.gate_id],
                missing_input_refs=missing_inputs,
                basis_quality="versioned_gate_registry_wrapped_from_phase_5_confirmation_projection",
            ),
            missing_inputs=missing_inputs,
            blocker_categories=blocker_categories,
            source_gate_status=source_gate.status,
            source_blocker_level=source_gate.blocker_level,
            homeowner_explanation=(
                "A contractor needs to confirm this item before the plan can be priced accurately."
                if homeowner_visible
                else "A contractor must complete final review before estimate use."
            ),
            contractor_notes=(
                f"{source_gate.title} remains a review gate. Source status is '{source_gate.status}' "
                f"with blocker level '{source_gate.blocker_level}'. This is not persisted completion or authority approval."
            ),
        )

    def _complexity_flags(self, takeoff_view, shared_compatibility) -> List[str]:
        line_categories = {item.category.value for item in takeoff_view.line_items}
        path_statuses = {path.path_key: path.status.value for path in shared_compatibility.compatibility_paths}
        flags = ["pv_only_or_basic_solar"]
        if "battery_ess" in line_categories:
            flags.append("battery_backup")
        if path_statuses.get("pv_battery_whole_home_backup") in {"blocked", "requires_contractor_confirmation"}:
            flags.append("whole_home_backup")
        if "generator_integration" in line_categories or any(
            "generator" in key and status != "unknown"
            for key, status in path_statuses.items()
        ):
            flags.append("generator_interlock_or_transfer")
        if "conduit_raceway_pathway" in line_categories or "routing_trenching_structural_mounting" in line_categories:
            flags.append("long_or_uncertain_conduit_route")
        if any("wet_location" in missing for missing in takeoff_view.missing_information):
            flags.append("wet_location_exterior_equipment")
        if path_statuses.get("service_upgrade_likely") in {"unknown", "blocked", "requires_contractor_confirmation"}:
            flags.append("service_upgrade_or_load_side_work")
        return self._sorted_unique(flags)

    def _required_gates_for_complexity(self, complexity_flags: List[str]) -> List[str]:
        required: List[str] = []
        for flag in complexity_flags:
            required.extend(COMPLEXITY_GATE_REQUIREMENTS.get(flag, []))
        return self._sorted_unique(required)

    def _blockers_from_gates(
        self,
        gates: List[EstimateConfirmationGate],
        required_gate_ids: List[str],
    ) -> List[EstimateReadinessBlocker]:
        blockers: List[EstimateReadinessBlocker] = []
        required = set(required_gate_ids)
        for gate in gates:
            if gate.gate_id not in required:
                continue
            if gate.status == EstimateConfirmationGateStatus.confirmed:
                continue
            for category in gate.blocker_categories:
                blockers.append(
                    EstimateReadinessBlocker(
                        blocker_id=f"gate:{gate.gate_id}:{category.value}",
                        category=category,
                        severity="blocker" if gate.source_blocker_level == "blocked" else "review_required",
                        gate_refs=[gate.gate_id],
                        source_refs=gate.basis.source_refs,
                        missing_inputs=gate.missing_inputs,
                        homeowner_explanation=(
                            "A contractor needs to confirm the related installation information before this can be estimated accurately."
                        ),
                        contractor_notes=(
                            f"{gate.gate_name} must be resolved before estimate use. "
                            "This blocker is readiness metadata, not a completed engineering review."
                        ),
                    )
                )
        return blockers

    def _blockers_from_takeoff(self, takeoff_view) -> List[EstimateReadinessBlocker]:
        blockers: List[EstimateReadinessBlocker] = []
        category_by_missing_input = {
            "contractor_pricing": EstimateBlockerCategory.pricing_input_missing,
            "verified_material_quantities": EstimateBlockerCategory.material_scope_incomplete,
            "field_verified_topology": EstimateBlockerCategory.contractor_field_verification_required,
            "field_measured_route": EstimateBlockerCategory.missing_measurement,
            "site_measurements": EstimateBlockerCategory.missing_measurement,
            "manufacturer_install_requirements": EstimateBlockerCategory.missing_product_spec,
            "manufacturer_requirements": EstimateBlockerCategory.missing_product_spec,
            "AHJ_or_utility_requirements": EstimateBlockerCategory.utility_review_required,
        }
        for missing, category in sorted(category_by_missing_input.items()):
            if missing not in takeoff_view.missing_information:
                continue
            blockers.append(
                EstimateReadinessBlocker(
                    blocker_id=f"takeoff_missing:{missing}",
                    category=category,
                    severity="blocker",
                    source_refs=takeoff_view.provenance_basis.source_refs,
                    missing_inputs=[missing],
                    homeowner_explanation=(
                        "A contractor needs to confirm the project scope, site conditions, and pricing inputs before estimate use."
                    ),
                    contractor_notes=(
                        f"Topology takeoff is missing '{missing}'. Do not use the takeoff as an estimate basis until resolved."
                    ),
                )
            )
        return blockers

    def _overall_status(
        self,
        *,
        required_gates: List[EstimateConfirmationGate],
        blockers: List[EstimateReadinessBlocker],
        missing_inputs: List[str],
    ) -> Tuple[EstimateReadinessStatus, bool, bool, ConfidenceLevel]:
        if not required_gates:
            return EstimateReadinessStatus.not_ready, False, True, ConfidenceLevel.low
        open_gates = [gate for gate in required_gates if gate.status != EstimateConfirmationGateStatus.confirmed]
        if not open_gates and not blockers and not missing_inputs:
            return EstimateReadinessStatus.ready_for_estimate, True, False, ConfidenceLevel.high
        hard_categories = {
            EstimateBlockerCategory.missing_measurement,
            EstimateBlockerCategory.missing_product_spec,
            EstimateBlockerCategory.missing_nameplate,
            EstimateBlockerCategory.unsafe_assumption,
            EstimateBlockerCategory.code_review_required,
            EstimateBlockerCategory.utility_review_required,
            EstimateBlockerCategory.ahj_review_required,
            EstimateBlockerCategory.pricing_input_missing,
            EstimateBlockerCategory.material_scope_incomplete,
        }
        blocker_categories = {blocker.category for blocker in blockers}
        if blocker_categories & hard_categories:
            return EstimateReadinessStatus.not_ready, False, True, ConfidenceLevel.low
        if open_gates:
            return EstimateReadinessStatus.ready_for_contractor_review, False, True, ConfidenceLevel.medium
        return EstimateReadinessStatus.partially_ready, False, True, ConfidenceLevel.medium

    def _scenario_status(
        self,
        scenario,
        *,
        overall_status: EstimateReadinessStatus,
        estimate_allowed: bool,
        contractor_review_required: bool,
        confidence_level: ConfidenceLevel,
        complexity_flags: List[str],
        required_gate_ids: List[str],
        blockers: List[EstimateReadinessBlocker],
        missing_inputs: List[str],
        takeoff_line_refs: List[str],
        compatibility_path_refs: List[str],
    ) -> ScenarioEstimateReadinessStatus:
        scenario_ref = f"scenario:{scenario.id}"
        blocker_categories = self._sorted_unique([blocker.category.value for blocker in blockers])
        return ScenarioEstimateReadinessStatus(
            scenario_id=scenario.id,
            scenario_name=scenario.name,
            linked_design_id=scenario.linked_design_id,
            status=overall_status,
            confidence_level=confidence_level,
            estimate_allowed=estimate_allowed,
            contractor_review_required=contractor_review_required,
            complexity_flags=complexity_flags,
            required_gate_ids=required_gate_ids,
            blocker_categories=blocker_categories,
            missing_inputs=missing_inputs,
            homeowner_explanation=(
                "This scenario is not ready for an estimate until contractor review confirms the missing project details."
                if not estimate_allowed
                else "This scenario has the required confirmation metadata for estimate preparation."
            ),
            contractor_notes=(
                "Scenario readiness is derived from home-level topology/takeoff and confirmation gates. "
                "No scenario-specific final design, field verification, or pricing approval is implied."
            ),
            basis=self._basis(
                source_refs=[scenario_ref],
                gate_refs=required_gate_ids,
                takeoff_line_refs=takeoff_line_refs,
                compatibility_path_refs=compatibility_path_refs,
                scenario_refs=[scenario_ref],
                missing_input_refs=missing_inputs,
                basis_quality="scenario_status_derived_from_home_level_phase_9_readiness",
            ),
        )

    def _homeowner_summary(
        self,
        status: EstimateReadinessStatus,
        blocker_count: int,
        missing_count: int,
    ) -> str:
        if status == EstimateReadinessStatus.ready_for_estimate:
            return "The plan has the confirmation metadata needed to prepare an estimate."
        if status == EstimateReadinessStatus.ready_for_contractor_review:
            return "A contractor needs to review the plan before it can become an estimate."
        return (
            "A contractor needs to confirm product details, installation conditions, and pricing inputs "
            f"before this can be estimated accurately. Current blockers: {blocker_count}; missing inputs: {missing_count}."
        )

    def _contractor_summary(
        self,
        status: EstimateReadinessStatus,
        blocker_count: int,
        required_gate_count: int,
    ) -> str:
        return (
            f"Estimate readiness status is {status.value}. "
            f"{required_gate_count} confirmation gates are required by current topology complexity, and "
            f"{blocker_count} blocker records remain. Treat this as pre-estimate review metadata only."
        )

    def build_home_estimate_readiness(self, db, home_id: str) -> Optional[EstimateReadinessView]:
        from app.services.contractor_context import contractor_context_service
        from app.services.twin_planning_context import twin_planning_context_service

        context = twin_planning_context_service.build(db, home_id)
        if context is None:
            return None

        gate_projection = contractor_context_service.build_confirmation_gate_projection(db, home_id)
        shared_compatibility = twin_planning_context_service.build_shared_compatibility_view(db, home_id)
        takeoff_view = twin_planning_context_service.build_topology_takeoff_view(db, home_id)
        if gate_projection is None or shared_compatibility is None or takeoff_view is None:
            return None

        gates = [self._confirmation_gate(gate) for gate in gate_projection.gates]
        complexity_flags = self._complexity_flags(takeoff_view, shared_compatibility)
        required_gate_ids = self._required_gates_for_complexity(complexity_flags)
        required_gates = [gate for gate in gates if gate.gate_id in required_gate_ids]
        blockers = self._blockers_from_gates(gates, required_gate_ids) + self._blockers_from_takeoff(takeoff_view)
        missing_inputs = self._sorted_unique(
            [
                missing
                for gate in required_gates
                for missing in gate.missing_inputs
            ]
            + takeoff_view.missing_information
        )
        overall_status, estimate_allowed, contractor_review_required, confidence_level = self._overall_status(
            required_gates=required_gates,
            blockers=blockers,
            missing_inputs=missing_inputs,
        )
        scenario_models = [
            scenario
            for scenario in repository.list_scenario_models(db)
            if scenario.home_id == home_id
        ]
        takeoff_line_refs = [item.line_id for item in takeoff_view.line_items]
        compatibility_path_refs = [path.path_key for path in shared_compatibility.compatibility_paths]
        scenario_statuses = [
            self._scenario_status(
                scenario,
                overall_status=overall_status,
                estimate_allowed=estimate_allowed,
                contractor_review_required=contractor_review_required,
                confidence_level=confidence_level,
                complexity_flags=complexity_flags,
                required_gate_ids=required_gate_ids,
                blockers=blockers,
                missing_inputs=missing_inputs,
                takeoff_line_refs=takeoff_line_refs,
                compatibility_path_refs=compatibility_path_refs,
            )
            for scenario in scenario_models
        ]
        blocker_category_counts = Counter(blocker.category.value for blocker in blockers)
        pending_gate_count = sum(1 for gate in required_gates if gate.status != EstimateConfirmationGateStatus.confirmed)
        source_basis = self._basis(
            source_refs=takeoff_view.provenance_basis.source_refs,
            gate_refs=[gate.gate_id for gate in gates],
            takeoff_line_refs=takeoff_line_refs,
            compatibility_path_refs=compatibility_path_refs,
            scenario_refs=[f"scenario:{scenario.id}" for scenario in scenario_models],
            missing_input_refs=missing_inputs,
            basis_quality="home_level_phase_9_estimate_readiness_rollup",
        )
        readiness_summary = EstimateReadinessSummary(
            overall_status=overall_status,
            confidence_level=confidence_level,
            estimate_allowed=estimate_allowed,
            contractor_review_required=contractor_review_required,
            required_gate_count=len(required_gates),
            pending_gate_count=pending_gate_count,
            blocker_count=len(blockers),
            missing_input_count=len(missing_inputs),
            scenario_count=len(scenario_statuses),
            summary_boundary_note=(
                "Estimate readiness is a pre-estimate confirmation gate rollup only. It is not a final estimate, "
                "proposal, quote, bid, final bill of materials, field verification, AHJ/utility approval, or engineering approval."
            ),
        )
        return EstimateReadinessView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 9 estimate readiness view built request-time from existing TwinPlanningContext, "
                "Phase 5 confirmation gates, Phase 7 shared compatibility, and Phase 8 topology takeoff metadata. "
                "It classifies estimate readiness and missing confirmations only; it does not write data, persist gate state, "
                "run migrations, enforce permissions, create auth/security behavior, generate proposals, calculate prices, "
                "produce final estimates, approve contractor review, approve NEC/code compliance, or imply AHJ/utility approval."
            ),
            readiness_scope=EstimateReadinessScope(limitations=ESTIMATE_READINESS_LIMITATIONS),
            readiness_summary=readiness_summary,
            overall_status=overall_status,
            scenario_statuses=scenario_statuses,
            confirmation_gates=gates,
            blockers=blockers,
            missing_inputs=missing_inputs,
            homeowner_summary=self._homeowner_summary(overall_status, len(blockers), len(missing_inputs)),
            contractor_summary=self._contractor_summary(overall_status, len(blockers), len(required_gates)),
            estimate_allowed=estimate_allowed,
            contractor_review_required=contractor_review_required,
            confidence_level=confidence_level,
            source_basis=source_basis,
            blocker_category_counts=dict(sorted(blocker_category_counts.items())),
            assumptions=[
                "Scenario readiness is derived from current home-level topology/takeoff context because no separate scenario-specific estimate-readiness engine exists.",
                "Unconfirmed gates are treated as not complete because no persisted contractor confirmation state exists.",
                "Structured planning records and existing derived views are authoritative over generated text.",
            ],
            limitations=ESTIMATE_READINESS_LIMITATIONS,
            deferred_boundaries=sorted(ESTIMATE_READINESS_DEFERRED_BOUNDARIES),
            compatibility_note=(
                "Existing TwinPlanningContext, contractor-context, planning-exchange, shared-compatibility, topology-takeoff, "
                "takeoff, estimate-placeholder, and scenario routes remain unchanged; this is an additive Phase 9 GET surface."
            ),
        )


estimate_readiness_service = EstimateReadinessService()

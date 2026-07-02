from typing import Dict, List, Optional

from app.core.types import ConfidenceLevel
from app.program_intelligence.schemas import (
    GridEdgeReadinessArea,
    GridEdgeReadinessIndicator,
    ProgramAwarenessCategory,
    ProgramAwarenessItem,
    ProgramIntelligenceBlocker,
    ProgramIntelligenceInterpretation,
    ProgramIntelligenceScope,
    ProgramIntelligenceSourceBasis,
    ProgramIntelligenceStatus,
    ProgramIntelligenceSummary,
    ProgramIntelligenceView,
)

PROGRAM_INTELLIGENCE_LIMITATIONS = [
    "Program Intelligence is read-only, request-time context derived from existing home planning records.",
    "It is non-authoritative awareness metadata, not a program determination, application, approval, program registration, tariff analysis, rebate calculation, or interconnection decision.",
    "Grid-edge readiness indicators are informational review prompts only and do not operate devices, dispatch load, register assets for programs, execute demand response, or provide grid services.",
    "Utility, rate, incentive, interconnection, export, equipment-compatibility, and jurisdiction details must be verified against current utility or program sources before use.",
]

PROGRAM_INTELLIGENCE_DEFERRED_BOUNDARIES = [
    "auth_security",
    "background_jobs",
    "billing_logic",
    "crm_integration",
    "demand_response_execution",
    "device_control",
    "email_automation",
    "enrollment_workflows",
    "exports",
    "external_api_calls",
    "grid_services_execution",
    "incentive_calculations",
    "interconnection_approval",
    "migrations",
    "permission_enforcement",
    "persistence",
    "pricing_logic",
    "program_eligibility_determinations",
    "proposal_generation",
    "pushes",
    "rebate_calculations",
    "tariff_optimization",
    "utility_dispatch",
    "writes",
]

PROGRAM_CONFIRMATION_GATES = [
    "utility_provider_confirmed",
    "program_jurisdiction_confirmed",
    "rate_plan_confirmed",
    "tou_schedule_confirmed",
    "incentive_program_terms_confirmed",
    "demand_response_program_terms_confirmed",
    "vpp_program_terms_confirmed",
    "interconnection_status_confirmed",
    "export_status_confirmed",
    "equipment_compatibility_confirmed",
    "battery_configuration_confirmed",
    "controllable_loads_confirmed",
    "ev_charger_program_requirements_confirmed",
]


class ProgramIntelligenceService:
    def _sorted_unique(self, values: List[str]) -> List[str]:
        return sorted({value for value in values if value})

    def _basis(
        self,
        *,
        source_refs: Optional[List[str]] = None,
        utility_refs: Optional[List[str]] = None,
        equipment_refs: Optional[List[str]] = None,
        program_refs: Optional[List[str]] = None,
        readiness_refs: Optional[List[str]] = None,
        missing_input_refs: Optional[List[str]] = None,
        blocker_refs: Optional[List[str]] = None,
        confirmation_gate_refs: Optional[List[str]] = None,
        assumption_refs: Optional[List[str]] = None,
        dependency_refs: Optional[List[str]] = None,
        deferred_boundary_refs: Optional[List[str]] = None,
        basis_quality: str = "request_time_derived_from_existing_twin_planning_context",
    ) -> ProgramIntelligenceSourceBasis:
        return ProgramIntelligenceSourceBasis(
            source_views=["TwinPlanningContext"],
            source_fields=[
                "TwinPlanningContext.sections.home",
                "TwinPlanningContext.sections.equipment_products",
                "TwinPlanningContext.sections.energy_system_designs",
                "TwinPlanningContext.sections.electrical_panels",
                "TwinPlanningContext.sections.loads",
                "TwinPlanningContext.sections.scenarios",
            ],
            source_refs=self._sorted_unique(source_refs or []),
            utility_refs=self._sorted_unique(utility_refs or []),
            equipment_refs=self._sorted_unique(equipment_refs or []),
            program_refs=self._sorted_unique(program_refs or []),
            readiness_refs=self._sorted_unique(readiness_refs or []),
            missing_input_refs=self._sorted_unique(missing_input_refs or []),
            blocker_refs=self._sorted_unique(blocker_refs or []),
            confirmation_gate_refs=self._sorted_unique(confirmation_gate_refs or []),
            assumption_refs=self._sorted_unique(assumption_refs or []),
            dependency_refs=self._sorted_unique(dependency_refs or []),
            deferred_boundary_refs=self._sorted_unique(
                deferred_boundary_refs or PROGRAM_INTELLIGENCE_DEFERRED_BOUNDARIES
            ),
            basis_quality=basis_quality,
            request_time_derived=True,
            external_api_call_present=False,
            authoritative_program_claim_present=False,
            authoritative_eligibility_claim_present=False,
            enrollment_action_present=False,
            dispatch_or_control_action_present=False,
            limitations=PROGRAM_INTELLIGENCE_LIMITATIONS,
        )

    def _record_ref(self, section_key: str, record) -> str:
        return f"{section_key}:{getattr(record, 'entity_type', '')}:{getattr(record, 'entity_id', '')}"

    def _context_evidence(self, context) -> Dict[str, List[str]]:
        evidence: Dict[str, List[str]] = {
            "battery": [],
            "controllable_loads": [],
            "der": [],
            "ev": [],
            "export_status": [],
            "home": [],
            "interconnection_status": [],
            "jurisdiction": [],
            "load": [],
            "rate_plan": [],
            "smart_panel": [],
            "solar": [],
            "utility": [],
        }
        for section in getattr(context, "sections", []):
            section_key = getattr(section, "section_key", "")
            for record in getattr(section, "records", []):
                ref = self._record_ref(section_key, record)
                payload = getattr(record, "record", {}) or {}
                entity_type = str(getattr(record, "entity_type", "") or "").lower()
                product_type = str(payload.get("product_type") or "").lower()
                panel_type = str(payload.get("panel_type") or "").lower()
                category = str(payload.get("category") or "").lower()
                design_goal = str(payload.get("design_goal") or "").lower()
                notes = str(payload.get("notes") or "").lower()
                name = str(payload.get("name") or "").lower()
                values = " ".join([entity_type, product_type, panel_type, category, design_goal, notes, name])

                if entity_type == "home":
                    evidence["home"].append(ref)
                    if payload.get("utility_provider"):
                        evidence["utility"].append(ref)
                    if payload.get("state") or payload.get("postal_code") or payload.get("country"):
                        evidence["jurisdiction"].append(ref)
                    if payload.get("rate_plan") or payload.get("tariff") or payload.get("tou_schedule"):
                        evidence["rate_plan"].append(ref)

                if payload.get("interconnection_status") or payload.get("interconnection_application_status"):
                    evidence["interconnection_status"].append(ref)
                if payload.get("export_status") or payload.get("export_permission") or payload.get("net_metering_status"):
                    evidence["export_status"].append(ref)

                if product_type in {"solar_panel", "pv_module", "microinverter", "string_inverter", "hybrid_inverter"} or "solar" in values or "pv" in values:
                    evidence["solar"].append(ref)
                    evidence["der"].append(ref)
                if product_type == "battery" or "battery" in values:
                    evidence["battery"].append(ref)
                    evidence["der"].append(ref)
                if product_type in {"gateway", "transfer_switch", "disconnect"} or "gateway" in values:
                    evidence["der"].append(ref)
                if product_type == "ev_charger" or "ev charger" in values or "ev_" in values:
                    evidence["ev"].append(ref)
                    evidence["controllable_loads"].append(ref)
                if product_type == "smart_panel" or panel_type == "smart_panel" or "smart panel" in values:
                    evidence["smart_panel"].append(ref)
                    evidence["controllable_loads"].append(ref)
                if entity_type == "load":
                    evidence["load"].append(ref)
                    if payload.get("backup_priority") or payload.get("controllable") or "shift" in values:
                        evidence["controllable_loads"].append(ref)
                if design_goal in {"partial_backup", "whole_home_backup", "expansion_ready", "off_grid_capable"}:
                    evidence["der"].append(ref)

        return {key: self._sorted_unique(values) for key, values in evidence.items()}

    def _missing_inputs(self, evidence: Dict[str, List[str]]) -> List[str]:
        missing = []
        if not evidence["utility"]:
            missing.append("utility_unknown")
        if not evidence["rate_plan"]:
            missing.append("rate_plan_unknown")
        if not evidence["battery"]:
            missing.append("battery_configuration_unknown")
        if not evidence["export_status"]:
            missing.append("export_status_unknown")
        if not evidence["interconnection_status"]:
            missing.append("interconnection_status_unknown")
        if not evidence["der"] and not evidence["ev"] and not evidence["smart_panel"]:
            missing.append("equipment_compatibility_unknown")
        else:
            missing.append("equipment_program_compatibility_unknown")
        if not evidence["jurisdiction"] or not evidence["utility"]:
            missing.append("program_jurisdiction_unknown")
        return self._sorted_unique(missing)

    def _blocker(
        self,
        *,
        blocker_id: str,
        blocker_type: str,
        missing_inputs: List[str],
        source_refs: Optional[List[str]] = None,
        severity: str = "review_required",
    ) -> ProgramIntelligenceBlocker:
        readable = ", ".join(missing_inputs) if missing_inputs else "source confirmation"
        return ProgramIntelligenceBlocker(
            blocker_id=blocker_id,
            blocker_type=blocker_type,
            severity=severity,
            source_refs=self._sorted_unique(source_refs or []),
            missing_inputs=self._sorted_unique(missing_inputs),
            homeowner_explanation=f"Program context is limited until {readable} is confirmed.",
            contractor_program_review_prompt=(
                f"Review prompt only: confirm {readable} against current utility, program, equipment, and site records."
            ),
        )

    def _blockers(self, missing_inputs: List[str]) -> List[ProgramIntelligenceBlocker]:
        blocker_groups = {
            "utility_context_missing": ["utility_unknown", "program_jurisdiction_unknown"],
            "rate_context_missing": ["rate_plan_unknown"],
            "interconnection_export_missing": ["interconnection_status_unknown", "export_status_unknown"],
            "equipment_program_context_missing": [
                "battery_configuration_unknown",
                "equipment_compatibility_unknown",
                "equipment_program_compatibility_unknown",
            ],
        }
        blockers = []
        for blocker_id, group_inputs in blocker_groups.items():
            group_missing = [missing for missing in group_inputs if missing in missing_inputs]
            if group_missing:
                blockers.append(
                    self._blocker(
                        blocker_id=blocker_id,
                        blocker_type="missing_confirmation_input",
                        missing_inputs=group_missing,
                    )
                )
        return blockers

    def _status_for(self, *, has_source: bool, missing_inputs: List[str]) -> ProgramIntelligenceStatus:
        if not has_source and missing_inputs:
            return ProgramIntelligenceStatus.source_limited
        if not has_source:
            return ProgramIntelligenceStatus.unknown
        if missing_inputs:
            return ProgramIntelligenceStatus.needs_confirmation
        return ProgramIntelligenceStatus.awareness_available

    def _awareness_item(
        self,
        *,
        category: ProgramAwarenessCategory,
        source_refs: List[str],
        utility_refs: List[str],
        equipment_refs: List[str],
        missing_inputs: List[str],
        dependencies: List[str],
        summary: str,
        homeowner_summary: str,
        contractor_prompt: str,
    ) -> ProgramAwarenessItem:
        blockers = self._blockers(missing_inputs)
        status = self._status_for(has_source=bool(source_refs or utility_refs or equipment_refs), missing_inputs=missing_inputs)
        confidence = ConfidenceLevel.medium if status == ProgramIntelligenceStatus.awareness_available else ConfidenceLevel.low
        gates = self._confirmation_gates(missing_inputs)
        return ProgramAwarenessItem(
            category=category,
            status=status,
            confidence_level=confidence,
            summary=summary,
            homeowner_summary=homeowner_summary,
            contractor_program_review_prompt=contractor_prompt,
            source_basis=self._basis(
                source_refs=source_refs + utility_refs + equipment_refs,
                utility_refs=utility_refs,
                equipment_refs=equipment_refs,
                program_refs=[category.value],
                missing_input_refs=missing_inputs,
                blocker_refs=[blocker.blocker_id for blocker in blockers],
                confirmation_gate_refs=gates,
                dependency_refs=dependencies,
            ),
            missing_inputs=self._sorted_unique(missing_inputs),
            blockers=blockers,
            confirmation_gates=gates,
            assumptions=["Program awareness is derived only from existing planning records and fixed review categories."],
            dependencies=self._sorted_unique(dependencies),
            do_not_assume=[
                "Do not assume program availability, participation approval, bill impact, export permission, or interconnection approval.",
                "Do not assume this view has checked current utility tariffs, rebate rules, or program terms.",
            ],
            limitations=PROGRAM_INTELLIGENCE_LIMITATIONS,
        )

    def _confirmation_gates(self, missing_inputs: List[str]) -> List[str]:
        gate_by_missing = {
            "utility_unknown": "utility_provider_confirmed",
            "program_jurisdiction_unknown": "program_jurisdiction_confirmed",
            "rate_plan_unknown": "rate_plan_confirmed",
            "battery_configuration_unknown": "battery_configuration_confirmed",
            "export_status_unknown": "export_status_confirmed",
            "interconnection_status_unknown": "interconnection_status_confirmed",
            "equipment_compatibility_unknown": "equipment_compatibility_confirmed",
            "equipment_program_compatibility_unknown": "equipment_compatibility_confirmed",
        }
        return self._sorted_unique([gate_by_missing[missing] for missing in missing_inputs if missing in gate_by_missing])

    def _program_awareness(self, evidence: Dict[str, List[str]], missing_inputs: List[str]) -> List[ProgramAwarenessItem]:
        utility_missing = [item for item in missing_inputs if item in {"utility_unknown", "program_jurisdiction_unknown"}]
        rate_missing = [item for item in missing_inputs if item == "rate_plan_unknown"]
        interconnection_missing = [
            item for item in missing_inputs if item in {"interconnection_status_unknown", "export_status_unknown"}
        ]
        equipment_missing = [
            item
            for item in missing_inputs
            if item in {"battery_configuration_unknown", "equipment_compatibility_unknown", "equipment_program_compatibility_unknown"}
        ]
        der_refs = self._sorted_unique(evidence["der"] + evidence["battery"] + evidence["solar"] + evidence["smart_panel"] + evidence["ev"])
        return [
            self._awareness_item(
                category=ProgramAwarenessCategory.utility_context,
                source_refs=evidence["home"],
                utility_refs=evidence["utility"],
                equipment_refs=[],
                missing_inputs=utility_missing,
                dependencies=["home.utility_provider", "home.state", "home.postal_code"],
                summary="Utility context awareness is limited to recorded home planning fields and does not verify account, territory, or service status.",
                homeowner_summary="Utility context can be prepared for review, but utility and jurisdiction details still need confirmation.",
                contractor_prompt="Review prompt only: confirm serving utility, service territory, jurisdiction, account-specific program context, and current source dates.",
            ),
            self._awareness_item(
                category=ProgramAwarenessCategory.program_categories,
                source_refs=evidence["home"] + der_refs,
                utility_refs=evidence["utility"],
                equipment_refs=der_refs,
                missing_inputs=utility_missing + equipment_missing,
                dependencies=["utility context", "equipment type context", "program jurisdiction"],
                summary="Program categories are surfaced as awareness topics only, including incentives, rate programs, demand response, VPP, TOU, and interconnection review.",
                homeowner_summary="The home may have program topics worth checking, but no program is confirmed by this view.",
                contractor_prompt="Review prompt only: match recorded DER, EV, panel, and load context against current utility or program materials.",
            ),
            self._awareness_item(
                category=ProgramAwarenessCategory.incentive_awareness,
                source_refs=evidence["home"] + der_refs,
                utility_refs=evidence["utility"],
                equipment_refs=der_refs,
                missing_inputs=utility_missing + equipment_missing,
                dependencies=["program jurisdiction", "equipment compatibility", "current incentive terms"],
                summary="Incentive and rebate awareness is a review topic only; no value, qualification, availability, or award amount is calculated.",
                homeowner_summary="Incentives or rebates should be checked with current program sources before planning around them.",
                contractor_prompt="Review prompt only: verify current incentive/rebate source documents, effective dates, equipment requirements, and application steps outside this endpoint.",
            ),
            self._awareness_item(
                category=ProgramAwarenessCategory.demand_response_awareness,
                source_refs=evidence["home"] + evidence["battery"] + evidence["smart_panel"] + evidence["ev"] + evidence["controllable_loads"],
                utility_refs=evidence["utility"],
                equipment_refs=evidence["battery"] + evidence["smart_panel"] + evidence["ev"] + evidence["controllable_loads"],
                missing_inputs=utility_missing + rate_missing + equipment_missing,
                dependencies=["utility program terms", "controllable loads", "equipment compatibility"],
                summary="Demand response awareness is limited to whether current planning records contain potentially relevant controllable-load or DER context.",
                homeowner_summary="Demand response may require separate utility and equipment review; nothing is registered for a program or controlled here.",
                contractor_prompt="Review prompt only: confirm program rules, device compatibility, customer consent requirements, and controls architecture outside this endpoint.",
            ),
            self._awareness_item(
                category=ProgramAwarenessCategory.vpp_awareness,
                source_refs=evidence["home"] + evidence["battery"] + evidence["solar"],
                utility_refs=evidence["utility"],
                equipment_refs=evidence["battery"] + evidence["solar"],
                missing_inputs=utility_missing + interconnection_missing + equipment_missing,
                dependencies=["battery/DER records", "export/interconnection status", "program compatibility"],
                summary="VPP awareness is an informational review topic for DER aggregation context; it does not imply participation, aggregator compatibility, or dispatch.",
                homeowner_summary="VPP participation would need separate utility/program, equipment, export, and consent review.",
                contractor_prompt="Review prompt only: verify aggregator/program terms, device eligibility requirements, export/interconnection posture, and homeowner authorization outside this endpoint.",
            ),
            self._awareness_item(
                category=ProgramAwarenessCategory.tou_awareness,
                source_refs=evidence["home"] + evidence["battery"] + evidence["ev"] + evidence["controllable_loads"],
                utility_refs=evidence["utility"],
                equipment_refs=evidence["battery"] + evidence["ev"] + evidence["controllable_loads"],
                missing_inputs=utility_missing + rate_missing,
                dependencies=["rate plan", "TOU schedule", "load shifting inputs"],
                summary="TOU awareness identifies that rate-plan review may matter; it does not optimize tariffs, schedules, bills, or savings.",
                homeowner_summary="Time-of-use context should be confirmed from current rate-plan documents before using it in planning.",
                contractor_prompt="Review prompt only: confirm rate plan, TOU period definitions, export/import treatment, and customer-specific tariff status.",
            ),
            self._awareness_item(
                category=ProgramAwarenessCategory.interconnection_awareness,
                source_refs=evidence["home"] + der_refs + evidence["interconnection_status"] + evidence["export_status"],
                utility_refs=evidence["utility"],
                equipment_refs=der_refs,
                missing_inputs=utility_missing + interconnection_missing,
                dependencies=["DER context", "interconnection status", "export status", "utility review"],
                summary="Interconnection awareness is limited to open review needs for DER/export context; it does not approve interconnection or export.",
                homeowner_summary="Interconnection and export status should be confirmed with utility/AHJ records before relying on this context.",
                contractor_prompt="Review prompt only: verify interconnection application status, export permission, net-metering/export rules, and AHJ/utility requirements.",
            ),
        ]

    def _readiness_indicator(
        self,
        *,
        readiness_area: GridEdgeReadinessArea,
        source_refs: List[str],
        utility_refs: List[str],
        equipment_refs: List[str],
        missing_inputs: List[str],
        indicators: List[str],
        dependencies: List[str],
        summary: str,
        homeowner_summary: str,
        contractor_prompt: str,
    ) -> GridEdgeReadinessIndicator:
        blockers = self._blockers(missing_inputs)
        status = self._status_for(has_source=bool(source_refs or utility_refs or equipment_refs), missing_inputs=missing_inputs)
        confidence = ConfidenceLevel.medium if status == ProgramIntelligenceStatus.awareness_available else ConfidenceLevel.low
        gates = self._confirmation_gates(missing_inputs)
        return GridEdgeReadinessIndicator(
            readiness_area=readiness_area,
            status=status,
            confidence_level=confidence,
            summary=summary,
            indicators=self._sorted_unique(indicators),
            homeowner_summary=homeowner_summary,
            contractor_program_review_prompt=contractor_prompt,
            source_basis=self._basis(
                source_refs=source_refs + utility_refs + equipment_refs,
                utility_refs=utility_refs,
                equipment_refs=equipment_refs,
                readiness_refs=[readiness_area.value],
                missing_input_refs=missing_inputs,
                blocker_refs=[blocker.blocker_id for blocker in blockers],
                confirmation_gate_refs=gates,
                dependency_refs=dependencies,
            ),
            missing_inputs=self._sorted_unique(missing_inputs),
            blockers=blockers,
            confirmation_gates=gates,
            assumptions=["Grid-edge readiness indicators are informational and depend on future source-backed program review."],
            dependencies=self._sorted_unique(dependencies),
            do_not_assume=[
                "Do not assume the home can participate in a program, shift load automatically, export power, or be dispatched.",
                "Do not assume equipment compatibility, telemetry availability, cybersecurity readiness, or homeowner consent from this view.",
            ],
            limitations=PROGRAM_INTELLIGENCE_LIMITATIONS,
        )

    def _grid_edge_readiness(self, evidence: Dict[str, List[str]], missing_inputs: List[str]) -> List[GridEdgeReadinessIndicator]:
        utility_missing = [item for item in missing_inputs if item in {"utility_unknown", "program_jurisdiction_unknown"}]
        rate_missing = [item for item in missing_inputs if item == "rate_plan_unknown"]
        interconnection_missing = [
            item for item in missing_inputs if item in {"interconnection_status_unknown", "export_status_unknown"}
        ]
        battery_missing = [item for item in missing_inputs if item == "battery_configuration_unknown"]
        equipment_missing = [
            item for item in missing_inputs if item in {"equipment_compatibility_unknown", "equipment_program_compatibility_unknown"}
        ]
        return [
            self._readiness_indicator(
                readiness_area=GridEdgeReadinessArea.battery_participation,
                source_refs=evidence["battery"],
                utility_refs=evidence["utility"],
                equipment_refs=evidence["battery"],
                missing_inputs=utility_missing + interconnection_missing + battery_missing + equipment_missing,
                indicators=["battery record context", "export/interconnection review dependency", "program compatibility review dependency"],
                dependencies=["battery configuration", "interconnection/export status", "program terms"],
                summary="Battery participation readiness is informational and depends on battery configuration, equipment compatibility, export posture, and program rules.",
                homeowner_summary="Battery program participation cannot be assumed from planning records alone.",
                contractor_prompt="Review prompt only: confirm battery model/configuration, gateway/control capability, export/interconnection status, telemetry needs, and program terms.",
            ),
            self._readiness_indicator(
                readiness_area=GridEdgeReadinessArea.load_shifting,
                source_refs=evidence["controllable_loads"] + evidence["load"],
                utility_refs=evidence["utility"],
                equipment_refs=evidence["smart_panel"] + evidence["ev"] + evidence["battery"],
                missing_inputs=utility_missing + rate_missing + equipment_missing,
                indicators=["controllable-load context", "rate-plan dependency", "controls compatibility dependency"],
                dependencies=["rate plan", "TOU schedule", "controllable load inventory", "customer/program consent"],
                summary="Load shifting readiness is limited to review context for loads, batteries, smart panels, EV charging, and rate plans.",
                homeowner_summary="Load shifting may be worth review, but this view does not schedule, optimize, or control loads.",
                contractor_prompt="Review prompt only: confirm controllable loads, panel/control equipment, rate plan, and homeowner authorization requirements.",
            ),
            self._readiness_indicator(
                readiness_area=GridEdgeReadinessArea.backup_planning,
                source_refs=evidence["battery"] + evidence["smart_panel"] + evidence["load"],
                utility_refs=evidence["utility"],
                equipment_refs=evidence["battery"] + evidence["smart_panel"],
                missing_inputs=battery_missing + equipment_missing,
                indicators=["backup-related equipment context", "load context", "equipment confirmation dependency"],
                dependencies=["backup load selection", "battery/gateway configuration", "contractor field review"],
                summary="Backup planning readiness is context for review only and is not a backup performance, runtime, or safety guarantee.",
                homeowner_summary="Backup planning still needs contractor and equipment review before relying on it.",
                contractor_prompt="Review prompt only: confirm backup loads, transfer/gateway equipment, battery configuration, and site conditions.",
            ),
            self._readiness_indicator(
                readiness_area=GridEdgeReadinessArea.smart_panel,
                source_refs=evidence["smart_panel"],
                utility_refs=evidence["utility"],
                equipment_refs=evidence["smart_panel"],
                missing_inputs=utility_missing + equipment_missing,
                indicators=["smart-panel context", "load-control review dependency", "program compatibility review dependency"],
                dependencies=["smart panel equipment", "manufacturer/program compatibility", "homeowner consent"],
                summary="Smart panel readiness indicates whether smart-panel context exists for review; it does not enable control or program registration.",
                homeowner_summary="Smart panel features and program use need separate product and program confirmation.",
                contractor_prompt="Review prompt only: confirm panel model, control capabilities, data/telemetry requirements, and program compatibility.",
            ),
            self._readiness_indicator(
                readiness_area=GridEdgeReadinessArea.ev_coordination,
                source_refs=evidence["ev"],
                utility_refs=evidence["utility"],
                equipment_refs=evidence["ev"],
                missing_inputs=utility_missing + rate_missing + equipment_missing,
                indicators=["EV charging context", "rate/program review dependency", "equipment compatibility review dependency"],
                dependencies=["EV charger model", "rate plan", "managed charging program terms"],
                summary="EV coordination readiness is informational only and does not register managed charging or control charging behavior.",
                homeowner_summary="EV coordination should be checked against charger, vehicle, utility program, and rate-plan requirements.",
                contractor_prompt="Review prompt only: confirm EVSE model, vehicle/program compatibility, rate plan, load management, and consent requirements.",
            ),
            self._readiness_indicator(
                readiness_area=GridEdgeReadinessArea.der_aggregation,
                source_refs=evidence["der"],
                utility_refs=evidence["utility"],
                equipment_refs=evidence["der"],
                missing_inputs=utility_missing + interconnection_missing + equipment_missing,
                indicators=["DER context", "interconnection/export dependency", "aggregation program review dependency"],
                dependencies=["DER equipment", "export/interconnection status", "program/aggregator terms", "homeowner authorization"],
                summary="DER aggregation readiness is a review indicator only and does not create aggregation, dispatch, telemetry, or grid-services behavior.",
                homeowner_summary="DER aggregation would need separate equipment, utility/program, export, telemetry, and consent review.",
                contractor_prompt="Review prompt only: confirm DER equipment, export/interconnection posture, aggregator terms, telemetry/security needs, and homeowner authorization.",
            ),
        ]

    def build_home_program_intelligence(self, db, home_id: str) -> Optional[ProgramIntelligenceView]:
        from app.services.twin_planning_context import twin_planning_context_service

        context = twin_planning_context_service.build(db, home_id)
        if context is None:
            return None

        evidence = self._context_evidence(context)
        missing_inputs = self._missing_inputs(evidence)
        program_awareness = self._program_awareness(evidence, missing_inputs)
        grid_edge_readiness = self._grid_edge_readiness(evidence, missing_inputs)
        blockers = self._sorted_blockers(
            [blocker for item in program_awareness for blocker in item.blockers]
            + [blocker for item in grid_edge_readiness for blocker in item.blockers]
        )
        confirmation_gates = self._sorted_unique(
            [gate for item in program_awareness for gate in item.confirmation_gates]
            + [gate for item in grid_edge_readiness for gate in item.confirmation_gates]
            + PROGRAM_CONFIRMATION_GATES
        )
        source_refs = self._sorted_unique([ref for refs in evidence.values() for ref in refs])
        utility_known = bool(evidence["utility"])
        overall_status = (
            ProgramIntelligenceStatus.needs_confirmation
            if source_refs and missing_inputs
            else ProgramIntelligenceStatus.awareness_available
            if source_refs
            else ProgramIntelligenceStatus.source_limited
        )
        scope = ProgramIntelligenceScope(limitations=PROGRAM_INTELLIGENCE_LIMITATIONS)
        source_basis = self._basis(
            source_refs=source_refs,
            utility_refs=evidence["utility"],
            equipment_refs=self._sorted_unique(evidence["der"] + evidence["smart_panel"] + evidence["ev"]),
            program_refs=[category.value for category in ProgramAwarenessCategory],
            readiness_refs=[area.value for area in GridEdgeReadinessArea],
            missing_input_refs=missing_inputs,
            blocker_refs=[blocker.blocker_id for blocker in blockers],
            confirmation_gate_refs=confirmation_gates,
            assumption_refs=[
                "program_context_is_awareness_only",
                "readiness_indicators_are_informational_only",
                "current_program_terms_not_fetched",
            ],
        )
        interpretation = ProgramIntelligenceInterpretation(
            homeowner_safe_summary=(
                "Program and grid-edge context can be prepared for review, but this endpoint does not confirm program availability, participation, savings, export permission, or utility approval."
            ),
            contractor_program_review_prompts=self._sorted_unique(
                [item.contractor_program_review_prompt for item in program_awareness]
                + [item.contractor_program_review_prompt for item in grid_edge_readiness]
            ),
            verification_recommendations=[
                "Confirm serving utility, jurisdiction, rate plan, TOU schedule, and current program documents from source records.",
                "Confirm equipment model, configuration, controls/telemetry capability, and manufacturer or program compatibility.",
                "Confirm export and interconnection status before relying on DER, VPP, or aggregation context.",
                "Confirm homeowner authorization, consent, and program registration requirements outside this endpoint.",
            ],
            do_not_assume=[
                "Do not assume program availability, qualification, program registration, incentive value, bill savings, tariff optimization, utility approval, export permission, dispatch, or device control.",
                "Do not assume the endpoint has called a utility, rebate, tariff, aggregator, manufacturer, CRM, email, or external service.",
            ],
            source_basis=source_basis,
            limitations=PROGRAM_INTELLIGENCE_LIMITATIONS,
        )
        return ProgramIntelligenceView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 15 Program Intelligence and Grid Edge Readiness context derived from existing TwinPlanningContext records at request time."
            ),
            scope=scope,
            summary=ProgramIntelligenceSummary(
                overall_status=overall_status,
                confidence_level=ConfidenceLevel.low if missing_inputs else ConfidenceLevel.medium,
                utility_context_known=utility_known,
                program_awareness_count=len(program_awareness),
                grid_edge_readiness_count=len(grid_edge_readiness),
                missing_input_count=len(missing_inputs),
                blocker_count=len(blockers),
                confirmation_gate_count=len(confirmation_gates),
                eligibility_determined=False,
                enrollment_available=False,
                dispatch_or_control_available=False,
                pricing_or_billing_available=False,
                summary_boundary_note=(
                    "Program Intelligence reports awareness and readiness context only; it does not determine qualification, register assets for programs, calculate incentives, optimize tariffs, bill customers, or operate devices."
                ),
            ),
            program_awareness=program_awareness,
            grid_edge_readiness=grid_edge_readiness,
            missing_inputs=missing_inputs,
            blockers=blockers,
            confirmation_gates=confirmation_gates,
            assumptions=[
                "Known context is limited to existing structured planning records.",
                "Unknown program, tariff, incentive, interconnection, export, compatibility, and jurisdiction inputs degrade the response instead of being inferred.",
                "Program and grid-edge terms must be verified from current source documents outside this endpoint.",
            ],
            dependencies=[
                "TwinPlanningContext",
                "serving utility confirmation",
                "rate-plan confirmation",
                "program source documents",
                "equipment compatibility review",
                "interconnection/export confirmation",
                "homeowner authorization outside this endpoint",
            ],
            interpretation=interpretation,
            source_basis=source_basis,
            capability_boundary_flags={
                "read_only": scope.read_only,
                "additive_only": scope.additive_only,
                "request_time_only": scope.request_time_only,
                "home_id_anchored": scope.home_id_anchored,
                "deterministic_for_same_inputs": scope.deterministic_for_same_inputs,
                "non_authoritative": scope.non_authoritative,
                "persistence_present": scope.persistence_present,
                "migrations_present": scope.migrations_present,
                "write_endpoints_present": scope.write_endpoints_present,
                "background_jobs_present": scope.background_jobs_present,
                "external_api_calls_present": scope.external_api_calls_present,
                "auth_security_changes_present": scope.auth_security_changes_present,
                "permission_enforcement_present": scope.permission_enforcement_present,
                "enrollment_workflow_present": scope.enrollment_workflow_present,
                "rebate_calculation_present": scope.rebate_calculation_present,
                "incentive_calculation_present": scope.incentive_calculation_present,
                "tariff_optimization_present": scope.tariff_optimization_present,
                "eligibility_determination_present": scope.eligibility_determination_present,
                "utility_dispatch_present": scope.utility_dispatch_present,
                "device_control_present": scope.device_control_present,
                "demand_response_execution_present": scope.demand_response_execution_present,
                "grid_services_execution_present": scope.grid_services_execution_present,
                "billing_logic_present": scope.billing_logic_present,
                "pricing_logic_present": scope.pricing_logic_present,
                "proposal_generation_present": scope.proposal_generation_present,
                "crm_integration_present": scope.crm_integration_present,
                "email_automation_present": scope.email_automation_present,
                "export_present": scope.export_present,
                "push_present": scope.push_present,
            },
            deferred_boundaries=PROGRAM_INTELLIGENCE_DEFERRED_BOUNDARIES,
            limitations=PROGRAM_INTELLIGENCE_LIMITATIONS,
            compatibility_note="Existing Phase 1 through Phase 14 routes remain unchanged.",
        )

    def _sorted_blockers(self, blockers: List[ProgramIntelligenceBlocker]) -> List[ProgramIntelligenceBlocker]:
        by_id: Dict[str, ProgramIntelligenceBlocker] = {}
        for blocker in blockers:
            existing = by_id.get(blocker.blocker_id)
            if existing is None:
                by_id[blocker.blocker_id] = blocker
                continue
            existing.missing_inputs = self._sorted_unique(existing.missing_inputs + blocker.missing_inputs)
            existing.source_refs = self._sorted_unique(existing.source_refs + blocker.source_refs)
        return [by_id[key] for key in sorted(by_id)]


program_intelligence_service = ProgramIntelligenceService()

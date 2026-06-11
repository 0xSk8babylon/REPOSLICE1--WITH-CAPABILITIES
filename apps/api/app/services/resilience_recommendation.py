from typing import Dict, List, Optional, Tuple

from app.core.types import (
    AutonomyReservePosture,
    BatterySizingPosture,
    ConfidenceLevel,
    FactLifecycleState,
    FutureGrowthMarginPosture,
    LowSolarAssumptionPosture,
    RecoveryStrengthPosture,
    ReserveMarginPosture,
    RecommendationProfile,
    SeasonalConservatismPosture,
    SolarSizingPosture,
)
from app.engines.resilience import calc
from app.design_advisor.schemas import (
    ArchitectureConsistencyCheck,
    BackupLoadSelectionSummary,
    BatteryCapacityRange,
    BatterySizingEstimate,
    CurrentHomeEnergyArchitectureEstimate,
    EstimateInspectability,
    HomeEnergyArchitectureComponent,
    InverterSystemArchitectureEstimate,
    PanelServiceArchitectureEstimate,
    ReasoningGraphDependency,
    ReasoningGraphNode,
    ProfileArchitectureFitAssessment,
    RecommendationProfileCard,
    ResilienceRecommendation,
    RoofGeometryReadiness,
    SolarCapacityRange,
    SolarSizingEstimate,
    StructuredSystemReasoningGraph,
)
from app.services.design_analysis import design_analysis_service
from app.services.design_completeness import design_completeness_service
from app.services.provenance import provenance_service


PROFILE_LIBRARY = {
    RecommendationProfile.critical_efficient: {
        "label": "Critical / Efficient",
        "intent": "Protect the highest-priority loads with disciplined scope and lower upfront commitment.",
        "behavioral_assumptions": [
            "Owner is comfortable prioritizing essentials over whole-home continuity.",
            "Outages matter, but cost discipline and simpler phase-one deployment still matter more.",
            "Future upgrades can happen later if the architecture leaves room.",
        ],
        "sizing_philosophy": "Size around essential resilience outcomes first, then avoid carrying unused margin too early.",
        "resilience_posture": "Focused on essential continuity during shorter or moderate disruptions.",
        "future_expansion_posture": "Preserve optional growth paths without pre-buying the full end state.",
        "battery_sizing_posture": BatterySizingPosture.lean,
        "solar_sizing_posture": SolarSizingPosture.load_matched,
        "autonomy_reserve_posture": AutonomyReservePosture.minimal,
        "future_growth_margin_posture": FutureGrowthMarginPosture.tight,
        "low_solar_assumption_posture": LowSolarAssumptionPosture.favorable,
        "reserve_margin_posture": ReserveMarginPosture.lean,
        "ui_description": "Best for disciplined first-phase resilience centered on critical loads and a cleaner entry cost.",
    },
    RecommendationProfile.balanced: {
        "label": "Balanced",
        "intent": "Balance present-day resilience, solar recovery, and cost without assuming premium redundancy.",
        "behavioral_assumptions": [
            "Owner wants stronger day-to-day outage coverage than a bare essentials design.",
            "The system should support a meaningful resilience step-up without chasing every future case immediately.",
            "Some future growth is likely and should be acknowledged in the recommendation.",
        ],
        "sizing_philosophy": "Balance backup scope, solar recovery, and moderate future headroom for mainstream planning use.",
        "resilience_posture": "Covers essential and select preferred loads with a practical outage stance.",
        "future_expansion_posture": "Leaves moderate room for later load or storage growth.",
        "battery_sizing_posture": BatterySizingPosture.balanced,
        "solar_sizing_posture": SolarSizingPosture.resilience_balanced,
        "autonomy_reserve_posture": AutonomyReservePosture.standard,
        "future_growth_margin_posture": FutureGrowthMarginPosture.planned,
        "low_solar_assumption_posture": LowSolarAssumptionPosture.typical,
        "reserve_margin_posture": ReserveMarginPosture.standard,
        "ui_description": "Best default recommendation when resilience, recovery, and budget all matter.",
    },
    RecommendationProfile.conservative: {
        "label": "Conservative",
        "intent": "Bias toward stronger outage protection and more protective resilience assumptions before making premium future-growth moves.",
        "behavioral_assumptions": [
            "Owner is more outage-sensitive and less comfortable with tight reserve assumptions.",
            "Lower-solar periods and imperfect site conditions should be treated more cautiously.",
            "Recommendation should absorb more uncertainty before calling the system sufficient.",
        ],
        "sizing_philosophy": "Carry more reserve and stronger solar recovery posture to reduce planning fragility.",
        "resilience_posture": "More defensive against longer outages, uncertainty, and weaker solar periods.",
        "future_expansion_posture": "Preserve growth headroom, but resilience certainty comes first.",
        "battery_sizing_posture": BatterySizingPosture.elevated,
        "solar_sizing_posture": SolarSizingPosture.recovery_weighted,
        "autonomy_reserve_posture": AutonomyReservePosture.elevated,
        "future_growth_margin_posture": FutureGrowthMarginPosture.expansion_oriented,
        "low_solar_assumption_posture": LowSolarAssumptionPosture.protective,
        "reserve_margin_posture": ReserveMarginPosture.elevated,
        "ui_description": "Best when resilience confidence matters more than minimizing first-cost or aggressive future build-out.",
    },
    RecommendationProfile.premium_future_ready: {
        "label": "Premium / Future-Ready",
        "intent": "Bias toward long-term resilience continuity, expansion flexibility, and fewer near-term architectural dead ends.",
        "behavioral_assumptions": [
            "Owner expects meaningful future electrification, detached-load growth, or broader resilience expectations.",
            "Recommendation should reduce retrofit regret rather than optimize only for the present phase.",
            "Higher upfront scope is acceptable when it preserves long-term flexibility and confidence.",
        ],
        "sizing_philosophy": "Bias both storage and solar toward resilient recovery plus future infrastructure headroom.",
        "resilience_posture": "Broadest planning posture short of claiming engineering-grade certainty.",
        "future_expansion_posture": "Strong bias toward future load growth and modular infrastructure continuity.",
        "battery_sizing_posture": BatterySizingPosture.robust,
        "solar_sizing_posture": SolarSizingPosture.future_weighted,
        "autonomy_reserve_posture": AutonomyReservePosture.extended,
        "future_growth_margin_posture": FutureGrowthMarginPosture.future_ready,
        "low_solar_assumption_posture": LowSolarAssumptionPosture.defensive,
        "reserve_margin_posture": ReserveMarginPosture.robust,
        "ui_description": "Best when future electrification, broader backup expectations, and retrofit avoidance outweigh near-term cost discipline.",
    },
}


class ResilienceRecommendationService:
    EXISTING_ROLE_PREFIXES = ("existing_", "current_")
    PROPOSED_ROLE_PREFIXES = ("proposed_", "planned_", "future_")
    SOLAR_CONVERSION_TYPES = {"microinverter", "string_inverter", "hybrid_inverter"}
    SOLAR_RELATED_TYPES = {"solar_panel", "microinverter", "string_inverter", "hybrid_inverter"}

    # Coefficient tables now live in the dependency-free calculation engine;
    # these aliases keep existing references working without duplicating values.
    AUTONOMY_HOUR_RANGES = calc.AUTONOMY_HOUR_RANGES
    RESERVE_MARGIN_FACTORS = calc.RESERVE_MARGIN_FACTORS
    GROWTH_MARGIN_FACTORS = calc.GROWTH_MARGIN_FACTORS
    SOLAR_PRODUCTION_FACTORS = calc.SOLAR_PRODUCTION_FACTORS

    SEASONAL_CONSERVATISM = {
        LowSolarAssumptionPosture.favorable: SeasonalConservatismPosture.mild,
        LowSolarAssumptionPosture.typical: SeasonalConservatismPosture.standard,
        LowSolarAssumptionPosture.protective: SeasonalConservatismPosture.protective,
        LowSolarAssumptionPosture.defensive: SeasonalConservatismPosture.defensive,
    }

    RECOVERY_STRENGTH = {
        SolarSizingPosture.load_matched: RecoveryStrengthPosture.modest,
        SolarSizingPosture.resilience_balanced: RecoveryStrengthPosture.balanced,
        SolarSizingPosture.recovery_weighted: RecoveryStrengthPosture.strong,
        SolarSizingPosture.future_weighted: RecoveryStrengthPosture.aggressive,
    }

    HIGH_SOLAR_STATES = {"AZ", "CA", "CO", "NV", "NM", "UT"}
    LOWER_SOLAR_STATES = {
        "AK",
        "CT",
        "ID",
        "IL",
        "IN",
        "MA",
        "ME",
        "MI",
        "MN",
        "MT",
        "NH",
        "NJ",
        "NY",
        "OH",
        "OR",
        "PA",
        "RI",
        "VT",
        "WA",
        "WI",
        "WY",
    }
    STATE_NAME_TO_ABBREVIATION = {
        "ALASKA": "AK",
        "ARIZONA": "AZ",
        "CALIFORNIA": "CA",
        "COLORADO": "CO",
        "CONNECTICUT": "CT",
        "IDAHO": "ID",
        "ILLINOIS": "IL",
        "INDIANA": "IN",
        "MASSACHUSETTS": "MA",
        "MAINE": "ME",
        "MICHIGAN": "MI",
        "MINNESOTA": "MN",
        "MONTANA": "MT",
        "NEVADA": "NV",
        "NEW HAMPSHIRE": "NH",
        "NEW JERSEY": "NJ",
        "NEW MEXICO": "NM",
        "NEW YORK": "NY",
        "OHIO": "OH",
        "OREGON": "OR",
        "PENNSYLVANIA": "PA",
        "RHODE ISLAND": "RI",
        "TEXAS": "TX",
        "UTAH": "UT",
        "VERMONT": "VT",
        "WASHINGTON": "WA",
        "WISCONSIN": "WI",
        "WYOMING": "WY",
    }

    def _assignment_stage(self, assignment) -> str:
        role = ((assignment["equipment"].role_in_system or "") if assignment.get("equipment") else "").strip().lower()
        if role.startswith(self.EXISTING_ROLE_PREFIXES):
            return "existing"
        if role.startswith(self.PROPOSED_ROLE_PREFIXES):
            return "proposed"
        return "unclear"

    def _product_note_blob(self, assignment) -> str:
        product = assignment.get("product")
        equipment = assignment.get("equipment")
        parts = []
        if product is not None:
            parts.extend(
                [
                    product.manufacturer or "",
                    product.model or "",
                    str(product.specs or ""),
                    product.notes or "",
                ]
            )
        if equipment is not None:
            parts.extend([equipment.role_in_system or "", equipment.notes or ""])
        return " ".join(parts).lower()

    def _has_optimizer_signal(self, assignment) -> bool:
        blob = self._product_note_blob(assignment)
        return "optimizer" in blob or "solaredge" in blob

    def _component_state(self, assignments, product_types: set) -> str:
        existing = [
            assignment
            for assignment in assignments
            if self._assignment_stage(assignment) == "existing"
            and assignment["product"]
            and assignment["product"].product_type in product_types
        ]
        proposed = [
            assignment
            for assignment in assignments
            if self._assignment_stage(assignment) == "proposed"
            and assignment["product"]
            and assignment["product"].product_type in product_types
        ]
        unclear = [
            assignment
            for assignment in assignments
            if self._assignment_stage(assignment) == "unclear"
            and assignment["product"]
            and assignment["product"].product_type in product_types
        ]
        if existing:
            return "existing"
        if proposed:
            return "proposed"
        if unclear:
            return "unclear"
        return "missing"

    def _round_range(self, value: float) -> float:
        return calc.round_range(value)

    def _solar_assignments(self, analysis):
        return [
            assignment
            for assignment in analysis["assigned_products"]
            if assignment["product"] and assignment["product"].product_type == "solar_panel"
        ]

    def _site_capacity_adjustment(self, analysis) -> Dict[str, object]:
        roof_locations = [location for location in analysis["locations"] if location.location_type == "roof"]
        solar_assignments = self._solar_assignments(analysis)
        assigned_solar_roof_locations = [
            assignment
            for assignment in solar_assignments
            if assignment["location"] and assignment["location"].location_type == "roof"
        ]

        if assigned_solar_roof_locations:
            return {
                "posture": "solar roof placement recorded",
                "factor_range": (0.98, 1.03),
                "status": "recorded",
                "note": "A roof placement is already recorded for assigned solar equipment, so the solar range stays close to the base recovery estimate.",
            }
        if roof_locations:
            posture = "multiple roof options recorded" if len(roof_locations) > 1 else "single roof option recorded"
            factor_range = (1.0, 1.05) if len(roof_locations) > 1 else (1.03, 1.1)
            return {
                "posture": posture,
                "factor_range": factor_range,
                "status": "recorded",
                "note": "Roof location records exist, but the current design does not yet fully prove usable solar placement capacity.",
            }
        if solar_assignments:
            return {
                "posture": "solar equipment assigned without roof placement",
                "factor_range": (1.06, 1.14),
                "status": "estimated",
                "note": "Solar equipment is assigned, but no roof placement is recorded yet, so the range carries extra placement caution.",
            }
        return {
            "posture": "roof placement not yet recorded",
            "factor_range": (1.08, 1.18),
            "status": "missing",
            "note": "No recorded roof placement exists yet, so the range carries a conservative placement uplift.",
        }

    def _roof_geometry_readiness(self, analysis) -> RoofGeometryReadiness:
        roof_locations = [location for location in analysis["locations"] if location.location_type == "roof"]
        assigned_solar_roof_locations = [
            assignment
            for assignment in self._solar_assignments(analysis)
            if assignment["location"] and assignment["location"].location_type == "roof"
        ]
        home = analysis.get("home")
        has_coordinates = any(location.approximate_coordinates for location in roof_locations)

        if assigned_solar_roof_locations and has_coordinates:
            return RoofGeometryReadiness(
                roof_data_completeness="placement tagged",
                roof_measurement_confidence="low",
                placement_realism_posture="inferred placement is grounded",
                estimated_roof_capacity_posture="estimated from recorded solar placement only",
                measured_geometry_status="not measured",
                usable_roof_area_status="not estimated",
                future_geometry_sources=[
                    "GIS/map-based scaling",
                    "traced roof polygons",
                    "roof plane modeling",
                    "usable roof area estimation",
                ],
                missing_geometry_warning="Recorded roof placement exists, but no measured roof geometry is available yet. Capacity posture remains estimated.",
                scope_note="This readiness layer distinguishes recorded placement from future measured roof geometry. It does not calculate roof area yet.",
            )
        if roof_locations:
            return RoofGeometryReadiness(
                roof_data_completeness="roof options recorded",
                roof_measurement_confidence="low",
                placement_realism_posture="inferred placement is partial",
                estimated_roof_capacity_posture="estimated from coarse roof options",
                measured_geometry_status="not measured",
                usable_roof_area_status="not estimated",
                future_geometry_sources=[
                    "GIS/map-based scaling",
                    "traced roof polygons",
                    "roof plane modeling",
                    "usable roof area estimation",
                ],
                missing_geometry_warning="Roof candidate locations are recorded, but no measured geometry or usable-area estimate exists yet.",
                scope_note="This readiness layer distinguishes coarse roof options from future measured roof geometry. It does not calculate roof area yet.",
            )
        state_context = home.state if home and home.state else "unknown region"
        return RoofGeometryReadiness(
            roof_data_completeness="geometry missing",
            roof_measurement_confidence="very low",
            placement_realism_posture="inferred placement is weak",
            estimated_roof_capacity_posture="estimated from fallback posture only",
            measured_geometry_status="not measured",
            usable_roof_area_status="not estimated",
            future_geometry_sources=[
                "GIS/map-based scaling",
                "traced roof polygons",
                "roof plane modeling",
                "usable roof area estimation",
            ],
            missing_geometry_warning=f"No measured roof geometry exists yet for this home in {state_context}. Solar capacity remains a planning estimate, not a measured roof-fit result.",
            scope_note="This readiness layer distinguishes missing geometry from coarse placement realism. It does not calculate roof area yet.",
        )

    def _shading_adjustment(self, analysis) -> Dict[str, object]:
        roof_locations = [location for location in analysis["locations"] if location.location_type == "roof"]
        if not roof_locations:
            return {
                "posture": "shading not modeled",
                "factor_range": (1.03, 1.08),
                "status": "missing",
                "note": "No explicit shading or obstruction field exists yet, so the solar range carries a modest default caution.",
            }
        return {
            "posture": "shading not modeled",
            "factor_range": (1.01, 1.05),
            "status": "estimated",
            "note": "Roof placement exists, but shading and obstruction are still unmodeled, so the range keeps a small caution uplift.",
        }

    def _seasonal_region_adjustment(self, analysis) -> Dict[str, object]:
        raw_state = analysis["home"].state if analysis.get("home") else ""
        state = (raw_state or "").strip().upper()
        normalized_state = self.STATE_NAME_TO_ABBREVIATION.get(state, state)
        if normalized_state in self.HIGH_SOLAR_STATES:
            return {
                "posture": "higher-production region",
                "factor_range": (0.97, 1.02),
                "status": "recorded",
                "note": f"State '{raw_state or normalized_state}' is treated as a higher-production region in this coarse planning model.",
            }
        if normalized_state in self.LOWER_SOLAR_STATES:
            return {
                "posture": "lower-production region",
                "factor_range": (1.08, 1.16),
                "status": "recorded",
                "note": f"State '{raw_state or normalized_state}' is treated as a lower-production region in this coarse planning model.",
            }
        if normalized_state:
            return {
                "posture": "mixed-production region",
                "factor_range": (1.02, 1.08),
                "status": "recorded",
                "note": f"State '{raw_state or normalized_state}' is treated as a mixed-production region in this coarse planning model.",
            }
        return {
            "posture": "seasonal region not recorded",
            "factor_range": (1.05, 1.12),
            "status": "missing",
            "note": "No recorded state exists for coarse seasonal posture, so the range keeps a generic seasonal caution uplift.",
        }

    def _install_realism_adjustment(self, analysis) -> Dict[str, object]:
        linked_pathways = analysis["linked_pathways"]
        if not linked_pathways:
            return {
                "posture": "install path incomplete",
                "factor_range": (1.05, 1.12),
                "status": "missing",
                "note": "No linked pathways are recorded, so install realism is incomplete and confidence should stay conservative.",
            }
        if any(pathway.route_difficulty == "high" for pathway in linked_pathways) or any(
            pathway.visibility_level == "high" for pathway in linked_pathways
        ):
            return {
                "posture": "install path constrained",
                "factor_range": (1.04, 1.1),
                "status": "estimated",
                "note": "Current pathway records suggest more difficult or more visible install conditions, so solar guidance should be treated more cautiously.",
            }
        if analysis["missing_location_assignments"]:
            return {
                "posture": "install path partially grounded",
                "factor_range": (1.02, 1.06),
                "status": "estimated",
                "note": "Some assigned equipment is still missing siting locations, so install realism remains partial.",
            }
        return {
            "posture": "install path broadly grounded",
            "factor_range": (0.99, 1.02),
            "status": "recorded",
            "note": "Linked pathways and siting assignments give the solar guidance a more grounded install context.",
        }

    def _has_backup_scope(self, analysis) -> bool:
        return bool(analysis["essential_loads"] or analysis["backup_loads"])

    def _preferred_loads(self, analysis):
        return [load for load in analysis["loads"] if load.backup_priority == "preferred"]

    def _backup_scope_selection(self, analysis, profile: Optional[RecommendationProfile] = None) -> Dict[str, object]:
        essential_loads = analysis["essential_loads"]
        preferred_loads = self._preferred_loads(analysis)
        total_recorded_load_count = len(analysis["loads"])
        selected_loads = []
        selection_basis = "missing"
        selected_priority_band = "none"
        selected_scope_label = "no backup load scope recorded"
        selection_reason = "No essential or preferred backup loads are recorded yet, so backup scope remains ungrounded."
        planning_gap_warning = "Record essential or preferred backup loads before relying on backup architecture or sizing guidance."

        if profile == RecommendationProfile.critical_efficient and essential_loads:
            selected_loads = essential_loads
            selection_basis = "essential_only"
            selected_priority_band = "essential"
            selected_scope_label = "essential loads only"
            selection_reason = (
                "Critical / Efficient intentionally constrains planning to recorded essential loads before broader backup scope is carried."
            )
            planning_gap_warning = None
        elif essential_loads and preferred_loads:
            selected_loads = analysis["backup_loads"]
            selection_basis = "essential_and_preferred"
            selected_priority_band = "preferred_plus_essential"
            selected_scope_label = "essential and preferred loads"
            selection_reason = (
                "Recorded preferred loads justify a broader backup scope, so planning uses the combined essential and preferred load group."
            )
            planning_gap_warning = None
        elif preferred_loads:
            selected_loads = preferred_loads
            selection_basis = "preferred_only"
            selected_priority_band = "preferred"
            selected_scope_label = "preferred loads only"
            selection_reason = (
                "Preferred backup loads are recorded without explicit essential loads, so planning uses the recorded preferred group rather than inventing a broader scope."
            )
            planning_gap_warning = "Essential-load tagging is missing, so outage-priority discipline is only partially grounded."
        elif essential_loads:
            selected_loads = essential_loads
            selected_priority_band = "essential"
            selected_scope_label = "essential loads only"
            if profile == RecommendationProfile.critical_efficient:
                selection_basis = "essential_only"
                selection_reason = (
                    "Critical / Efficient intentionally constrains planning to recorded essential loads before broader backup scope is carried."
                )
                planning_gap_warning = None
            else:
                selection_basis = "essential_fallback"
                selection_reason = (
                    "No preferred backup loads are recorded, so planning stays grounded in essential loads only instead of inferring broader backup scope."
                )
                planning_gap_warning = (
                    "Broader backup ambition is not yet reflected in load grouping, so current planning remains limited to essential loads."
                )

        selected_load_count = len(selected_loads)
        coverage_ratio = calc.backup_coverage_ratio(selected_load_count, total_recorded_load_count)

        if not selected_load_count:
            outage_posture = "ungrounded outage posture"
            outage_posture_reason = (
                "No selected backup scope exists yet, so the planner cannot describe even a critical-load outage posture from recorded loads."
            )
            confidence_level = ConfidenceLevel.low
            confidence_reason = (
                "Backup-scope confidence is low because no essential or preferred load grouping currently grounds the outage posture."
            )
        elif selection_basis == "preferred_only":
            outage_posture = "partial-home outage posture"
            outage_posture_reason = (
                "Preferred loads extend backup scope beyond essentials, but the missing essential anchor weakens outage-priority discipline."
            )
            confidence_level = ConfidenceLevel.low
            confidence_reason = (
                "Backup-scope confidence stays low because preferred loads are recorded without a matching essential-load anchor."
            )
        elif selection_basis in {"essential_only", "essential_fallback"}:
            outage_posture = "critical-load outage posture"
            outage_posture_reason = (
                f"Selected scope covers {selected_load_count} of {total_recorded_load_count} recorded loads and stays anchored to essentials only."
            )
            confidence_level = ConfidenceLevel.medium
            confidence_reason = (
                "Backup-scope confidence is medium because essential loads are grounded, but broader partial-home or whole-home grouping is not yet recorded."
            )
        elif coverage_ratio is not None and coverage_ratio >= 0.85:
            outage_posture = "whole-home outage posture candidate"
            outage_posture_reason = (
                f"Selected scope covers {selected_load_count} of {total_recorded_load_count} recorded loads, so the recorded grouping resembles a whole-home planning candidate."
            )
            confidence_level = ConfidenceLevel.high
            confidence_reason = (
                "Backup-scope confidence is high because both essential and preferred grouping are recorded and they cover nearly all recorded loads."
            )
        else:
            outage_posture = "partial-home outage posture"
            outage_posture_reason = (
                f"Selected scope covers {selected_load_count} of {total_recorded_load_count} recorded loads and extends beyond essentials without claiming every recorded load."
            )
            confidence_level = ConfidenceLevel.high
            confidence_reason = (
                "Backup-scope confidence is high because both essential and preferred grouping are recorded and the broader outage posture is explicit."
            )

        return {
            "selected_loads": selected_loads,
            "selection_basis": selection_basis,
            "selected_priority_band": selected_priority_band,
            "selected_scope_label": selected_scope_label,
            "selection_reason": selection_reason,
            "planning_gap_warning": planning_gap_warning,
            "outage_posture": outage_posture,
            "outage_posture_reason": outage_posture_reason,
            "confidence_level": confidence_level,
            "confidence_reason": confidence_reason,
            "recorded_essential_load_count": len(essential_loads),
            "recorded_preferred_load_count": len(preferred_loads),
            "recorded_total_load_count": total_recorded_load_count,
            "selected_load_count": selected_load_count,
            "coverage_ratio_of_recorded_loads": coverage_ratio,
            "supports_broader_backup": selection_basis in {"essential_and_preferred", "preferred_only"},
            "supports_partial_home_backup": outage_posture in {
                "partial-home outage posture",
                "whole-home outage posture candidate",
            },
            "supports_whole_home_backup": outage_posture == "whole-home outage posture candidate",
        }

    def _selected_backup_loads(self, analysis, profile: Optional[RecommendationProfile] = None):
        return self._backup_scope_selection(analysis, profile)["selected_loads"]

    def _backup_load_energy_need_kwh(
        self, analysis, profile: Optional[RecommendationProfile] = None
    ) -> Optional[float]:
        selected_loads = self._selected_backup_loads(analysis, profile)
        return calc.backup_load_energy_need_kwh(
            [(load.running_watts, load.estimated_daily_hours) for load in selected_loads]
        )

    def _backup_load_model_summary(
        self, analysis, profile: Optional[RecommendationProfile] = None
    ) -> Dict[str, object]:
        selection = self._backup_scope_selection(analysis, profile)
        selected_loads = selection["selected_loads"]
        missing_daily_hours = [load.name for load in selected_loads if not load.estimated_daily_hours]
        fallback_applied = bool(selected_loads) and bool(missing_daily_hours)
        return {
            "selected_load_count": len(selected_loads),
            "selected_source": selection["selection_basis"],
            "selected_scope_label": selection["selected_scope_label"],
            "selected_priority_band": selection["selected_priority_band"],
            "selection_reason": selection["selection_reason"],
            "planning_gap_warning": selection["planning_gap_warning"],
            "outage_posture": selection["outage_posture"],
            "outage_posture_reason": selection["outage_posture_reason"],
            "confidence_level": selection["confidence_level"],
            "confidence_reason": selection["confidence_reason"],
            "recorded_essential_load_count": selection["recorded_essential_load_count"],
            "recorded_preferred_load_count": selection["recorded_preferred_load_count"],
            "recorded_total_load_count": selection["recorded_total_load_count"],
            "coverage_ratio_of_recorded_loads": selection["coverage_ratio_of_recorded_loads"],
            "supports_broader_backup": selection["supports_broader_backup"],
            "supports_partial_home_backup": selection["supports_partial_home_backup"],
            "supports_whole_home_backup": selection["supports_whole_home_backup"],
            "missing_daily_hour_loads": missing_daily_hours,
            "fallback_applied": fallback_applied,
        }

    def _architecture_consistency_check(
        self,
        analysis,
        load_summary,
        recommended_backup_architecture: str,
    ) -> ArchitectureConsistencyCheck:
        design_goal = analysis["design"].design_goal
        warnings: List[str] = []

        if design_goal == "lowest_cost":
            goal_target = "critical-load planning"
        elif design_goal == "partial_backup":
            goal_target = "partial-home planning"
        elif design_goal in {"whole_home_backup", "off_grid_capable"}:
            goal_target = "whole-home planning"
        elif design_goal in {"workshop_ready", "expansion_ready"}:
            goal_target = "future-ready planning"
        else:
            goal_target = "phased backup planning"

        if recommended_backup_architecture == "whole-home backup" and not load_summary["supports_whole_home_backup"]:
            warnings.append(
                "Whole-home architecture should not be treated as grounded until the selected scope covers nearly all recorded loads."
            )
            status = "misaligned"
            summary = "Architecture direction is broader than the recorded backup scope."
            reason = (
                "The current recommendation reaches whole-home architecture without a whole-home outage-posture candidate in recorded load grouping."
            )
        elif design_goal in {"whole_home_backup", "off_grid_capable"} and not load_summary["supports_whole_home_backup"]:
            warnings.append(
                "The current design goal is broader than the recorded load grouping, so architecture remains intentionally narrower than the stated ambition."
            )
            status = "conditional"
            summary = "Architecture direction is intentionally narrower than the design goal."
            reason = (
                "Recorded load grouping does not yet justify whole-home outage posture, so the architecture recommendation remains bounded to planning evidence."
            )
        elif recommended_backup_architecture == "partial-home backup" and not load_summary["supports_partial_home_backup"]:
            warnings.append(
                "Partial-home architecture remains weakly grounded because recorded loads currently resolve only to an essential-only outage posture."
            )
            status = "conditional"
            summary = "Architecture direction is slightly broader than the current load grouping."
            reason = (
                "Panel/service posture leaves room for partial-home planning, but the selected backup scope still behaves like critical-load planning."
            )
        elif goal_target == "critical-load planning" and recommended_backup_architecture != "critical-loads subpanel":
            warnings.append(
                "The design goal is cost-disciplined critical-load planning, so broader architecture should be treated cautiously."
            )
            status = "conditional"
            summary = "Architecture direction is broader than the cost-disciplined goal."
            reason = (
                "Current architecture signals allow a broader path, but the design goal still points toward critical-load discipline."
            )
        else:
            status = "aligned"
            summary = "Architecture direction is consistent with the recorded backup scope."
            reason = (
                f"The current recommendation stays aligned with {load_summary['outage_posture']} and the '{goal_target}' design-goal posture."
            )

        return ArchitectureConsistencyCheck(
            status=status,
            summary=summary,
            reason=reason,
            warnings=warnings,
        )

    def _backup_load_selection_summary(
        self,
        db,
        analysis,
        profile: RecommendationProfile,
        confidence: ConfidenceLevel,
        rule_documents_map=None,
    ) -> BackupLoadSelectionSummary:
        load_summary = self._backup_load_model_summary(analysis, profile)
        input_signals = [
            {
                "key": "recorded_essential_loads",
                "label": "Recorded essential loads",
                "value": str(load_summary["recorded_essential_load_count"]),
                "status": "recorded" if load_summary["recorded_essential_load_count"] else "missing",
                "note": "Essential-load tagging is the narrowest deterministic backup scope available to the planner.",
            },
            {
                "key": "recorded_preferred_loads",
                "label": "Recorded preferred loads",
                "value": str(load_summary["recorded_preferred_load_count"]),
                "status": "recorded" if load_summary["recorded_preferred_load_count"] else "missing",
                "note": "Preferred-load tagging is the current structured signal that the backup scope extends beyond essentials.",
            },
            {
                "key": "recorded_load_coverage",
                "label": "Selected coverage of recorded loads",
                "value": (
                    f"{int(load_summary['coverage_ratio_of_recorded_loads'] * 100)}% of recorded loads"
                    if load_summary["coverage_ratio_of_recorded_loads"] is not None
                    else "No recorded loads"
                ),
                "status": "rule_based" if load_summary["selected_load_count"] else "missing",
                "note": "Coverage is measured only against currently recorded loads, so it remains a planning signal rather than a validated whole-home inventory.",
            },
            {
                "key": "selected_backup_scope",
                "label": "Selected backup scope",
                "value": f"{load_summary['selected_load_count']} loads from {load_summary['selected_scope_label']}",
                "status": "rule_based" if load_summary["selected_load_count"] else "missing",
                "note": "Battery, solar, and backup-architecture planning consume this selected scope instead of inferring broader outage intent.",
            },
            {
                "key": "outage_posture",
                "label": "Derived outage posture",
                "value": load_summary["outage_posture"],
                "status": "rule_based" if load_summary["selected_load_count"] else "missing",
                "note": "The outage posture distinguishes critical-load, partial-home, and whole-home candidates from recorded grouping only.",
            },
            {
                "key": "recommendation_profile",
                "label": "Recommendation profile context",
                "value": profile.value.replace("_", " "),
                "status": "rule_based",
                "note": "Profile posture can narrow the selected scope, but it does not invent missing broader load grouping.",
            },
        ]
        estimated_inputs = []
        incomplete_inputs = []
        if load_summary["planning_gap_warning"]:
            incomplete_inputs.append(load_summary["planning_gap_warning"])
        return BackupLoadSelectionSummary(
            selected_scope_label=load_summary["selected_scope_label"],
            selection_basis=load_summary["selected_source"],
            selected_priority_band=load_summary["selected_priority_band"],
            selected_load_count=load_summary["selected_load_count"],
            recorded_essential_load_count=load_summary["recorded_essential_load_count"],
            recorded_preferred_load_count=load_summary["recorded_preferred_load_count"],
            recorded_total_load_count=load_summary["recorded_total_load_count"],
            coverage_ratio_of_recorded_loads=load_summary["coverage_ratio_of_recorded_loads"],
            outage_posture=load_summary["outage_posture"],
            outage_posture_reason=load_summary["outage_posture_reason"],
            confidence_level=load_summary["confidence_level"],
            confidence_reason=load_summary["confidence_reason"],
            selection_reason=load_summary["selection_reason"],
            planning_gap_warning=load_summary["planning_gap_warning"],
            scope_note="Planning-only selection summary. It explains which recorded loads currently ground backup architecture and sizing, not final transfer, inverter, or generator design.",
            inspectability=provenance_service.build_estimate_inspectability(
                db,
                basis="Backup scope selection is derived from recorded essential/preferred load grouping plus explicit profile-aware selection rules.",
                confidence_level=load_summary["confidence_level"],
                rule_keys=[
                    "recommendation.resilience_profile_matrix_v1",
                    "recommendation.backup_load_selection_v1",
                ],
                input_signals=input_signals,
                estimated_inputs=estimated_inputs,
                incomplete_inputs=incomplete_inputs,
                notes=[
                    "The planner distinguishes recorded load grouping from the selected planning scope so broader outage intent is not silently inferred.",
                ],
                rule_documents_map=rule_documents_map,
            ),
        )

    def _current_home_energy_architecture_estimate(
        self,
        db,
        analysis,
        backup_load_selection: BackupLoadSelectionSummary,
        confidence: ConfidenceLevel,
        rule_documents_map=None,
    ) -> CurrentHomeEnergyArchitectureEstimate:
        assignments = analysis["assigned_products"]
        design = analysis["design"]

        existing_assignments = [
            assignment
            for assignment in assignments
            if self._assignment_stage(assignment) == "existing" and assignment["product"] is not None
        ]
        proposed_assignments = [
            assignment
            for assignment in assignments
            if self._assignment_stage(assignment) == "proposed" and assignment["product"] is not None
        ]
        unclear_assignments = [
            assignment
            for assignment in assignments
            if self._assignment_stage(assignment) == "unclear" and assignment["product"] is not None
        ]

        existing_types = {assignment["product"].product_type for assignment in existing_assignments}
        proposed_types = {assignment["product"].product_type for assignment in proposed_assignments}
        unclear_types = {assignment["product"].product_type for assignment in unclear_assignments}

        existing_has_solar = bool(existing_types.intersection(self.SOLAR_RELATED_TYPES))
        proposed_has_solar = bool(proposed_types.intersection(self.SOLAR_RELATED_TYPES))
        unclear_has_solar = bool(unclear_types.intersection(self.SOLAR_RELATED_TYPES))

        has_existing_micro = "microinverter" in existing_types
        has_existing_string = "string_inverter" in existing_types
        has_existing_hybrid = "hybrid_inverter" in existing_types
        has_existing_battery = "battery" in existing_types
        has_existing_generator = "generator" in existing_types
        has_existing_transfer = bool(existing_types.intersection({"gateway", "transfer_switch", "disconnect"}))
        has_existing_smart_panel = bool(existing_types.intersection({"smart_panel", "load_center"}))
        has_existing_optimizer_signal = any(self._has_optimizer_signal(assignment) for assignment in existing_assignments)
        has_unclear_optimizer_signal = any(self._has_optimizer_signal(assignment) for assignment in unclear_assignments)
        topology_family_count = sum(
            [
                1 if has_existing_micro else 0,
                1 if has_existing_string else 0,
                1 if has_existing_hybrid else 0,
                1 if has_existing_optimizer_signal else 0,
            ]
        )

        if existing_has_solar:
            solar_existing_state = "existing solar recorded"
        elif proposed_has_solar:
            solar_existing_state = "proposed solar only recorded"
        elif unclear_has_solar:
            solar_existing_state = "solar stage unclear"
        else:
            solar_existing_state = "solar not recorded"

        if existing_has_solar and topology_family_count > 1:
            inverter_topology = "mixed or unclear topology"
            topology_confidence = ConfidenceLevel.medium
            topology_confidence_reason = (
                "Existing solar equipment is recorded, but multiple inverter-family signals appear together, so the current topology should be treated as mixed or unclear."
            )
        elif has_existing_hybrid and has_existing_battery and design.architecture_type in {"hybrid", "dc_coupled"}:
            inverter_topology = "DC-coupled battery system"
            topology_confidence = ConfidenceLevel.high
            topology_confidence_reason = (
                "Existing hybrid inverter and battery signals align with the recorded architecture type, so the current storage path reads as DC-coupled at planning level."
            )
        elif (has_existing_micro or has_existing_string or has_existing_optimizer_signal) and has_existing_battery:
            inverter_topology = "AC-coupled battery retrofit"
            topology_confidence = ConfidenceLevel.high
            topology_confidence_reason = (
                "Existing solar conversion equipment and existing battery signals together suggest an AC-coupled solar-plus-storage posture."
            )
        elif has_existing_micro:
            inverter_topology = "microinverter system"
            topology_confidence = ConfidenceLevel.high
            topology_confidence_reason = (
                "Existing microinverter equipment is explicitly recorded, so the current solar topology is grounded as a microinverter system."
            )
        elif has_existing_optimizer_signal:
            inverter_topology = "optimizer-based system"
            topology_confidence = ConfidenceLevel.medium
            topology_confidence_reason = (
                "Optimizer-oriented product or note signals are present, but the optimizer path is inferred from recorded product context rather than a dedicated optimizer equipment type."
            )
        elif has_existing_string:
            inverter_topology = "string inverter system"
            topology_confidence = ConfidenceLevel.high
            topology_confidence_reason = (
                "Existing string-inverter equipment is explicitly recorded, so the current solar topology is grounded as a string-inverter system."
            )
        elif has_existing_hybrid:
            inverter_topology = "hybrid inverter system"
            topology_confidence = ConfidenceLevel.high
            topology_confidence_reason = (
                "Existing hybrid-inverter equipment is explicitly recorded, so the current topology already includes a hybrid conversion backbone."
            )
        elif existing_has_solar:
            inverter_topology = "unknown / not recorded topology"
            topology_confidence = ConfidenceLevel.low
            topology_confidence_reason = (
                "Existing solar-related equipment is recorded without a matching inverter-family signal, so the current topology remains unknown."
            )
        elif proposed_has_solar or unclear_has_solar:
            inverter_topology = "unknown / not recorded topology"
            topology_confidence = ConfidenceLevel.low
            topology_confidence_reason = (
                "Solar-related equipment appears only as proposed or stage-unclear records, so the current home topology should remain unresolved instead of guessed."
            )
        else:
            inverter_topology = "unknown / not recorded topology"
            topology_confidence = ConfidenceLevel.low
            topology_confidence_reason = (
                "The current design does not record enough existing solar or inverter evidence to classify the home's current topology."
            )

        current_labels = []
        if existing_has_solar:
            current_labels.append(inverter_topology)
        if has_existing_battery:
            current_labels.append("existing battery")
        if has_existing_generator:
            current_labels.append("existing generator")
        if has_existing_smart_panel:
            current_labels.append("existing smart/load-control panel")
        proposed_labels = sorted(
            {
                assignment["product"].product_type.replace("_", " ")
                for assignment in proposed_assignments
                if assignment["product"] is not None
            }
        )
        current_description = ", ".join(current_labels) if current_labels else "no current topology clearly recorded"
        proposed_description = ", ".join(proposed_labels) if proposed_labels else "no proposed add-ons clearly recorded"
        current_vs_proposed_architecture = (
            f"Current home energy architecture reads as {current_description}; proposed design additions read as {proposed_description}."
        )

        if inverter_topology in {"microinverter system", "string inverter system", "optimizer-based system"} and (
            "battery" in proposed_types or "battery" in unclear_types or not has_existing_battery and "battery" in analysis["product_types"]
        ):
            battery_retrofit_implication = (
                "Current solar topology commonly points toward an AC-coupled battery retrofit planning posture, but product-level gateway, controls, and battery compatibility still need validation."
            )
        elif inverter_topology in {"hybrid inverter system", "DC-coupled battery system"}:
            battery_retrofit_implication = (
                "Current topology already leans toward a shared hybrid/DC-coupled storage path, but final battery compatibility and operating behavior still require product-level validation."
            )
        elif inverter_topology == "unknown / not recorded topology":
            battery_retrofit_implication = (
                "Battery retrofit posture remains open because the current inverter topology is not yet recorded well enough to favor AC-coupled or hybrid planning."
            )
        else:
            battery_retrofit_implication = (
                "Battery retrofit posture remains planning-only because the current topology is either mixed or only partially grounded."
            )

        if inverter_topology == "microinverter system":
            expansion_implication = (
                "Microinverter-based solar is often expansion-friendly at planning level because conversion happens at the module level, but branch, gateway, and backup-control details still matter."
            )
        elif inverter_topology == "optimizer-based system":
            expansion_implication = (
                "Optimizer-based systems can preserve array-level flexibility, but future storage and backup behavior still depend on the recorded inverter/control path."
            )
        elif inverter_topology in {"hybrid inverter system", "DC-coupled battery system"}:
            expansion_implication = (
                "Hybrid-centered topology often preserves a broader storage path, but future expansion still depends on final equipment limits and service/panel constraints."
            )
        elif inverter_topology == "unknown / not recorded topology":
            expansion_implication = (
                "Expansion readiness remains only partially grounded because the current solar conversion path is not yet recorded."
            )
        else:
            expansion_implication = (
                "Current topology leaves room for expansion planning, but the exact future path remains dependent on panel, control, and product compatibility details."
            )

        if existing_has_solar and not (has_existing_transfer and (has_existing_battery or has_existing_hybrid)):
            outage_solar_behavior_note = (
                "Do not assume the recorded solar array can operate during an outage. Existing solar production may stay unavailable without compatible backup gateway, grid-forming equipment, and storage architecture."
            )
        elif existing_has_solar:
            outage_solar_behavior_note = (
                "Recorded solar and backup-control signals suggest outage solar operation may be possible, but product-level behavior still requires validation before assuming solar-backed outage support."
            )
        else:
            outage_solar_behavior_note = (
                "Outage solar behavior cannot be described yet because the current solar topology is not clearly recorded."
            )

        if "generator" in analysis["product_types"] and not bool(analysis["product_types"].intersection({"gateway", "transfer_switch", "disconnect"})):
            generator_coexistence_note = (
                "Generator coexistence should remain uncertain because no transfer switch, gateway, or disconnect path is recorded yet."
            )
        elif "generator" in analysis["product_types"]:
            generator_coexistence_note = (
                "Generator coexistence is partially grounded by recorded transfer/control hardware, but product-level operating coordination remains unverified."
            )
        else:
            generator_coexistence_note = (
                "No generator signal is recorded, so generator coexistence remains outside the current topology summary."
            )

        architecture_components = [
            HomeEnergyArchitectureComponent(
                component_key="solar_array",
                label="Solar array",
                state="existing" if existing_has_solar else "proposed" if proposed_has_solar else "unclear" if unclear_has_solar else "missing",
                relationship="Solar array is the current generation anchor when recorded; otherwise it remains proposed or unresolved.",
                note="Uses existing/proposed role markers when available and stays unresolved when stage markers are missing.",
            ),
            HomeEnergyArchitectureComponent(
                component_key="inverter_topology",
                label="Solar / inverter topology",
                state="existing" if existing_has_solar else "unclear" if unclear_has_solar else "missing",
                relationship=f"Current topology is classified as {inverter_topology}.",
                note=topology_confidence_reason,
            ),
            HomeEnergyArchitectureComponent(
                component_key="main_service_panel",
                label="Main service panel",
                state="existing" if analysis["main_panel"] is not None else "missing",
                relationship="Current solar and backup pathways ultimately tie back to the main service context used by the planner.",
                note="Panel/service posture remains a separate planning layer and is not inferred from topology alone.",
            ),
            HomeEnergyArchitectureComponent(
                component_key="backup_loads",
                label="Backup loads",
                state="planning_assumption" if backup_load_selection.selected_load_count else "missing",
                relationship="Backup loads represent the selected outage-scope assumption that downstream battery and architecture guidance consume.",
                note="Load grouping is planning-only and does not prove existing transfer configuration.",
            ),
            HomeEnergyArchitectureComponent(
                component_key="battery",
                label="Battery",
                state=self._component_state(assignments, {"battery"}),
                relationship="Battery state is shown separately so current storage can be distinguished from a proposed retrofit path.",
                note=battery_retrofit_implication,
            ),
            HomeEnergyArchitectureComponent(
                component_key="generator",
                label="Generator",
                state=self._component_state(assignments, {"generator"}),
                relationship="Generator is shown as a coexistence signal rather than automatic backup compatibility.",
                note=generator_coexistence_note,
            ),
            HomeEnergyArchitectureComponent(
                component_key="smart_panel",
                label="Smart panel / load control",
                state=self._component_state(assignments, {"smart_panel", "load_center"}),
                relationship="Selective-load control can change future backup behavior, but it is separate from current solar topology.",
                note="No smart-panel behavior is assumed unless equipment is explicitly recorded.",
            ),
            HomeEnergyArchitectureComponent(
                component_key="service_upgrade_path",
                label="Service upgrade path",
                state="planning_assumption",
                relationship="Service-upgrade direction remains a future planning path rather than a current-state topology component.",
                note="Use the panel/service architecture layer for upgrade caution and backup-architecture consistency.",
            ),
        ]

        topology_source_inputs = [
            {
                "key": "existing_stage_markers",
                "label": "Existing-vs-proposed stage markers",
                "value": (
                    f"{len(existing_assignments)} existing, {len(proposed_assignments)} proposed, {len(unclear_assignments)} unclear"
                ),
                "status": "recorded" if assignments else "missing",
                "note": "Current-state topology only treats equipment as existing when role markers explicitly say so; otherwise it preserves ambiguity.",
            },
            {
                "key": "existing_solar_signals",
                "label": "Existing solar signals",
                "value": solar_existing_state,
                "status": "recorded" if existing_has_solar else "missing" if not (proposed_has_solar or unclear_has_solar) else "estimated",
                "note": "Existing solar is distinguished from proposed-only solar so the advisor does not silently turn future equipment into current-state evidence.",
            },
            {
                "key": "inverter_family_signals",
                "label": "Inverter family signals",
                "value": ", ".join(
                    sorted(
                        {
                            assignment["product"].product_type.replace("_", " ")
                            for assignment in existing_assignments
                            if assignment["product"].product_type in self.SOLAR_CONVERSION_TYPES
                        }
                    )
                )
                or ("optimizer-oriented context" if has_existing_optimizer_signal or has_unclear_optimizer_signal else "No explicit existing inverter family recorded"),
                "status": "recorded" if existing_types.intersection(self.SOLAR_CONVERSION_TYPES) else "estimated" if has_existing_optimizer_signal or has_unclear_optimizer_signal else "missing",
                "note": "Microinverter, string, hybrid, and inferred optimizer cues are used to classify current topology without claiming product compatibility.",
            },
            {
                "key": "architecture_type",
                "label": "Recorded design architecture type",
                "value": (design.architecture_type or "not recorded").replace("_", " "),
                "status": "recorded" if design.architecture_type else "missing",
                "note": "Architecture type acts only as a supporting signal; it does not override missing current-state equipment records.",
            },
            {
                "key": "transfer_gateway_signals",
                "label": "Transfer or gateway signals",
                "value": "present" if analysis["product_types"].intersection({"gateway", "transfer_switch", "disconnect"}) else "not recorded",
                "status": "recorded" if analysis["product_types"].intersection({"gateway", "transfer_switch", "disconnect"}) else "missing",
                "note": "Outage solar and generator coexistence remain cautious until control or transfer hardware is explicitly recorded.",
            },
        ]

        incomplete_inputs: List[str] = []
        if not existing_has_solar:
            incomplete_inputs.append("Current-state solar inventory is incomplete or not explicitly marked as existing.")
        if inverter_topology == "unknown / not recorded topology":
            incomplete_inputs.append("Current inverter topology is not explicitly recorded, so AC-coupled vs hybrid planning remains less grounded.")
        if unclear_assignments:
            incomplete_inputs.append("Some equipment roles do not distinguish existing from proposed state, so topology confidence stays lower.")
        if not analysis["main_panel"]:
            incomplete_inputs.append("Main service panel details are missing, so topology relationships to the service equipment stay partial.")

        inspectability = provenance_service.build_estimate_inspectability(
            db,
            basis="Current home energy architecture is derived from explicit existing-vs-proposed role markers, current solar and inverter product signals, transfer/gateway records, panel context, and the current backup-load scope.",
            confidence_level=topology_confidence,
            rule_keys=[
                "recommendation.backup_load_selection_v1",
                "recommendation.current_home_energy_architecture_v1",
            ],
            input_signals=topology_source_inputs,
            estimated_inputs=[
                "Topology classification is planning-only and preserves unknowns when the current-state equipment record is incomplete."
            ],
            incomplete_inputs=incomplete_inputs,
            notes=[
                "Current topology does not imply outage capability, NEC compliance, rapid-shutdown compliance, or final compatibility between solar, storage, and generator hardware."
            ],
            rule_documents_map=rule_documents_map,
        )

        return CurrentHomeEnergyArchitectureEstimate(
            solar_existing_state=solar_existing_state,
            inverter_topology=inverter_topology,
            topology_confidence=topology_confidence,
            topology_confidence_reason=topology_confidence_reason,
            topology_source_inputs=topology_source_inputs,
            current_vs_proposed_architecture=current_vs_proposed_architecture,
            outage_solar_behavior_note=outage_solar_behavior_note,
            battery_retrofit_implication=battery_retrofit_implication,
            expansion_implication=expansion_implication,
            generator_coexistence_note=generator_coexistence_note,
            architecture_components=architecture_components,
            scope_note="Planning-only current-state architecture summary. It helps explain what the home appears to have today versus what remains proposed, without claiming final electrical design, outage behavior approval, or compatibility validation.",
            inspectability=inspectability,
        )

    def _panel_service_architecture_estimate(
        self,
        db,
        analysis,
        completeness,
        profile: RecommendationProfile,
        confidence: ConfidenceLevel,
        rule_documents_map=None,
    ) -> PanelServiceArchitectureEstimate:
        main_panel = analysis["main_panel"]
        home = analysis["home"]
        load_summary = self._backup_load_model_summary(analysis, profile)
        linked_pathways = analysis["linked_pathways"]
        product_types = analysis["product_types"]
        design_goal = analysis["design"].design_goal
        supports_partial_home_backup = load_summary["supports_partial_home_backup"]
        supports_whole_home_backup = load_summary["supports_whole_home_backup"]

        if main_panel is None:
            main_service_panel_posture = "main service panel not recorded"
            panel_upgrade_likelihood = "unknown, needs verification"
            service_upgrade_caution = "Service equipment is not documented well enough to trust a backup architecture path."
            critical_loads_subpanel_suitability = "unknown"
            partial_home_backup_suitability = "unknown"
            whole_home_backup_suitability = "poor"
        else:
            breaker_spaces = main_panel.breaker_spaces_available or 0
            amperage = main_panel.amperage or 0
            if amperage >= 200 and breaker_spaces >= 4:
                main_service_panel_posture = "serviceable panel with some backup headroom"
                panel_upgrade_likelihood = "low to moderate"
                critical_loads_subpanel_suitability = "favorable"
                partial_home_backup_suitability = "conditional"
                whole_home_backup_suitability = "conditional" if design_goal in {"whole_home_backup", "off_grid_capable"} else "limited"
            elif amperage >= 200 and breaker_spaces >= 2:
                main_service_panel_posture = "serviceable panel with tight expansion headroom"
                panel_upgrade_likelihood = "moderate"
                critical_loads_subpanel_suitability = "favorable"
                partial_home_backup_suitability = "conditional"
                whole_home_backup_suitability = "limited"
            elif amperage >= 125:
                main_service_panel_posture = "smaller or tighter panel likely to constrain backup architecture"
                panel_upgrade_likelihood = "moderate to high"
                critical_loads_subpanel_suitability = "conditional"
                partial_home_backup_suitability = "limited"
                whole_home_backup_suitability = "poor"
            else:
                main_service_panel_posture = "service equipment appears undersized for broad backup architecture"
                panel_upgrade_likelihood = "high"
                critical_loads_subpanel_suitability = "limited"
                partial_home_backup_suitability = "poor"
                whole_home_backup_suitability = "poor"

            if home is not None and (home.service_size or 0) >= 200:
                service_upgrade_caution = "Recorded service size suggests no immediate service-upgrade assumption, but site verification is still required."
            elif home is not None and home.service_size:
                service_upgrade_caution = "Recorded service size suggests broader backup goals may push toward service or distribution upgrades."
            else:
                service_upgrade_caution = "Service size is not recorded, so service-upgrade risk remains a planning caution."

        if not supports_partial_home_backup:
            if partial_home_backup_suitability == "conditional":
                partial_home_backup_suitability = "limited"
            elif partial_home_backup_suitability == "favorable":
                partial_home_backup_suitability = "conditional"
            whole_home_backup_suitability = "poor"
        elif not supports_whole_home_backup:
            if whole_home_backup_suitability == "conditional":
                whole_home_backup_suitability = "limited"
            elif whole_home_backup_suitability == "favorable":
                whole_home_backup_suitability = "conditional"

        if linked_pathways and any(pathway.route_difficulty == "high" or pathway.visibility_level == "high" for pathway in linked_pathways):
            if partial_home_backup_suitability == "conditional":
                partial_home_backup_suitability = "limited"
            if whole_home_backup_suitability == "conditional":
                whole_home_backup_suitability = "limited"
            elif whole_home_backup_suitability == "limited":
                whole_home_backup_suitability = "poor"

        if analysis["workshop_buildings"] or len(linked_pathways) > 1:
            if whole_home_backup_suitability == "conditional":
                whole_home_backup_suitability = "limited"
            elif whole_home_backup_suitability == "limited":
                whole_home_backup_suitability = "poor"

        if "smart_panel" in product_types or "load_center" in product_types:
            smart_panel_readiness_note = "Smart-panel or load-control equipment is already present in the architecture signals, so selective backup control is more realistic."
        elif main_panel is not None and (main_panel.breaker_spaces_available or 0) >= 2:
            smart_panel_readiness_note = "Existing panel context suggests smart-panel or load-control assistance may be feasible, but no explicit smart-panel strategy is recorded yet."
        else:
            smart_panel_readiness_note = "Smart-panel readiness is uncertain because the current panel/service record is tight or incomplete."

        if "generator" in product_types or "transfer_switch" in product_types or "gateway" in product_types or "disconnect" in product_types:
            generator_integration_readiness_note = "Generator-related tie-in signals exist in the current architecture, but generator sizing and runtime logic remain deferred."
        elif main_panel is None:
            generator_integration_readiness_note = "Generator integration readiness is unknown because the current panel/service tie-in path is not documented."
        else:
            generator_integration_readiness_note = "Generator sizing is deferred, but panel/service architecture should still verify inlet, interlock, transfer, or gateway provisions before assuming generator-backed backup paths."

        if main_panel is None:
            recommended_backup_architecture = "future-ready service upgrade path"
        elif supports_partial_home_backup and "smart_panel" in product_types and profile in {
            RecommendationProfile.balanced,
            RecommendationProfile.conservative,
            RecommendationProfile.premium_future_ready,
        }:
            recommended_backup_architecture = "smart-panel/load-control assisted"
        elif profile == RecommendationProfile.critical_efficient:
            recommended_backup_architecture = "critical-loads subpanel"
        elif profile == RecommendationProfile.balanced:
            recommended_backup_architecture = (
                "partial-home backup"
                if supports_partial_home_backup and partial_home_backup_suitability in {"favorable", "conditional"}
                else "critical-loads subpanel"
            )
        elif profile == RecommendationProfile.conservative:
            if (
                supports_whole_home_backup
                and whole_home_backup_suitability in {"favorable", "conditional"}
                and design_goal in {"whole_home_backup", "off_grid_capable"}
            ):
                recommended_backup_architecture = "whole-home backup"
            elif supports_partial_home_backup:
                recommended_backup_architecture = "partial-home backup"
            else:
                recommended_backup_architecture = "critical-loads subpanel"
        else:
            if (
                supports_whole_home_backup
                and whole_home_backup_suitability in {"favorable", "conditional"}
                and home is not None
                and (home.service_size or 0) >= 200
            ):
                recommended_backup_architecture = "whole-home backup"
            elif supports_partial_home_backup and "smart_panel" in product_types:
                recommended_backup_architecture = "smart-panel/load-control assisted"
            else:
                recommended_backup_architecture = "future-ready service upgrade path"

        consistency = self._architecture_consistency_check(
            analysis,
            load_summary,
            recommended_backup_architecture,
        )

        input_signals = [
            {
                "key": "main_panel_posture",
                "label": "Existing main service panel posture",
                "value": main_service_panel_posture,
                "status": "recorded" if main_panel is not None else "missing",
                "note": "Uses current panel amperage and available breaker-space records as a preliminary architecture signal.",
            },
            {
                "key": "service_size",
                "label": "Recorded service size",
                "value": str(home.service_size) if home is not None and home.service_size else "Not recorded",
                "status": "recorded" if home is not None and home.service_size else "missing",
                "note": "Service-size context influences service-upgrade caution but is not a final utility or code determination.",
            },
            {
                "key": "backup_load_scope",
                "label": "Backup load scope",
                "value": (
                    f"{load_summary['selected_load_count']} selected from {load_summary['selected_scope_label']}"
                    if load_summary["selected_load_count"]
                    else "No selected backup scope"
                ),
                "status": "recorded" if load_summary["selected_load_count"] else "missing",
                "note": "Current architecture posture uses the selected backup scope rather than silently assuming broader outage intent.",
            },
            {
                "key": "outage_posture",
                "label": "Outage posture from recorded grouping",
                "value": load_summary["outage_posture"],
                "status": "rule_based" if load_summary["selected_load_count"] else "missing",
                "note": "Panel/service posture now distinguishes critical-load, partial-home, and whole-home candidates from the selected scope.",
            },
            {
                "key": "pathway_realism",
                "label": "Install and pathway realism",
                "value": f"{len(linked_pathways)} linked pathways",
                "status": "recorded" if linked_pathways else "missing",
                "note": "Pathway difficulty and visibility affect how realistic broader backup architectures appear at planning time.",
            },
            {
                "key": "recommendation_profile",
                "label": "Recommended resilience profile",
                "value": profile.value.replace("_", " "),
                "status": "rule_based",
                "note": "Panel/service architecture posture is interpreted in the context of the selected planning philosophy.",
            },
            {
                "key": "architecture_consistency",
                "label": "Architecture consistency check",
                "value": consistency.status,
                "status": "rule_based",
                "note": "Checks whether the architecture direction stays bounded by the recorded backup scope and the stated design-goal posture.",
            },
        ]
        estimated_inputs: List[str] = [
            "Panel/service architecture is a deterministic planning posture, not a final code, busbar, feeder, or interlock design."
        ]
        incomplete_inputs: List[str] = []
        if completeness["completeness_score"] < 75:
            estimated_inputs.append("Planning completeness is still partial, so backup architecture posture remains directional.")
        if main_panel is None:
            incomplete_inputs.append("Main service panel details are missing, so backup architecture posture cannot be strongly grounded.")
        if home is None or not home.service_size:
            incomplete_inputs.append("Service size is not recorded, so service-upgrade caution remains conservative.")
        if not load_summary["selected_load_count"]:
            incomplete_inputs.append("Backup load grouping is incomplete, so architecture fit is not yet tied to a trustworthy backup scope.")
        elif load_summary["planning_gap_warning"]:
            incomplete_inputs.append(load_summary["planning_gap_warning"])
        if not linked_pathways:
            incomplete_inputs.append("No linked pathways are recorded, so install realism behind backup architecture remains incomplete.")

        inspectability = provenance_service.build_estimate_inspectability(
            db,
            basis="Panel/service architecture posture is based on current service-panel records, service-size context, backup-load scope, pathway realism, assigned architecture signals, and the selected recommendation profile.",
            confidence_level=confidence,
            rule_keys=[
                "recommendation.resilience_profile_matrix_v1",
                "recommendation.backup_load_selection_v1",
                "recommendation.panel_service_preliminary_architecture_v1",
                "recommendation.backup_architecture_consistency_v1",
            ],
            input_signals=input_signals,
            estimated_inputs=estimated_inputs,
            incomplete_inputs=incomplete_inputs,
            notes=[
                "This layer constrains backup architecture choices before inverter sizing, smart-panel behavior modeling, or generator sizing are introduced.",
            ],
            rule_documents_map=rule_documents_map,
        )

        return PanelServiceArchitectureEstimate(
            main_service_panel_posture=main_service_panel_posture,
            panel_upgrade_likelihood=panel_upgrade_likelihood,
            service_upgrade_caution=service_upgrade_caution,
            critical_loads_subpanel_suitability=critical_loads_subpanel_suitability,
            partial_home_backup_suitability=partial_home_backup_suitability,
            whole_home_backup_suitability=whole_home_backup_suitability,
            smart_panel_readiness_note=smart_panel_readiness_note,
            generator_integration_readiness_note=generator_integration_readiness_note,
            recommended_backup_architecture=recommended_backup_architecture,
            scope_note="Planning estimate only. This preliminary panel/service architecture layer constrains backup design direction before final load, inverter, smart-panel, or generator sizing.",
            architecture_consistency=consistency,
            inspectability=inspectability,
        )

    def _build_profile_input_signals(
        self,
        analysis,
        completeness,
        profile: RecommendationProfile,
        current_home_energy_architecture: Optional[CurrentHomeEnergyArchitectureEstimate] = None,
    ) -> Tuple[List[Dict[str, object]], List[str], List[str]]:
        load_summary = self._backup_load_model_summary(analysis, profile)
        architecture_type = (analysis["design"].architecture_type or "not_recorded").replace("_", " ")
        signals = [
            {
                "key": "design_goal",
                "label": "Design goal",
                "value": analysis["design"].design_goal.replace("_", " "),
                "status": "recorded",
                "note": "Primary deterministic signal used to map the design into a recommendation philosophy.",
            },
            {
                "key": "load_grouping",
                "label": "Backup load grouping",
                "value": (
                    f"{load_summary['selected_load_count']} selected from {load_summary['selected_scope_label']}"
                    if load_summary["selected_load_count"]
                    else "no selected backup scope"
                ),
                "status": "recorded" if load_summary["selected_load_count"] else "missing",
                "note": "Current essential/preferred load grouping influences resilience scope through an explicit selected planning scope.",
            },
            {
                "key": "assigned_architecture",
                "label": "Assigned equipment architecture",
                "value": f"{len(analysis['assigned_products'])} assigned products",
                "status": "recorded" if analysis["assigned_products"] else "missing",
                "note": "Assigned products indicate whether battery and backup architecture planning exists.",
            },
            {
                "key": "architecture_type",
                "label": "Recorded architecture type",
                "value": architecture_type,
                "status": "recorded" if analysis["design"].architecture_type else "missing",
                "note": "The current design architecture helps explain whether the profile fit stays phase-one, hybrid, or future-ready.",
            },
            {
                "key": "current_topology",
                "label": "Current home energy topology",
                "value": (
                    current_home_energy_architecture.inverter_topology
                    if current_home_energy_architecture is not None
                    else "not evaluated"
                ),
                "status": "rule_based" if current_home_energy_architecture is not None else "missing",
                "note": "Current-state solar topology is kept separate from future architecture direction so existing conditions do not get silently merged with proposals.",
            },
            {
                "key": "outage_posture",
                "label": "Recorded outage posture",
                "value": load_summary["outage_posture"],
                "status": "rule_based" if load_summary["selected_load_count"] else "missing",
                "note": "Profile fit now inherits the explicit outage posture rather than inferring broader backup intent from the design goal alone.",
            },
            {
                "key": "panel_context",
                "label": "Main panel context",
                "value": "Known" if analysis["main_panel"] is not None else "Not recorded",
                "status": "recorded" if analysis["main_panel"] is not None else "missing",
                "note": "Panel context affects confidence in practical resilience fit.",
            },
            {
                "key": "pathway_context",
                "label": "Pathway planning",
                "value": f"{len(analysis['linked_pathways'])} linked pathways",
                "status": "recorded" if analysis["linked_pathways"] else "missing",
                "note": "Pathway planning improves confidence that the recommendation maps to a real install path.",
            },
            {
                "key": "planning_completeness",
                "label": "Planning completeness",
                "value": f"{completeness['completeness_score']}/100",
                "status": "estimated" if completeness["completeness_score"] < 75 else "recorded",
                "note": "Lower completeness reduces confidence even when the profile rule still resolves deterministically.",
            },
        ]
        estimated_inputs: List[str] = []
        incomplete_inputs: List[str] = []
        if completeness["completeness_score"] < 75:
            estimated_inputs.append("Recommendation fit still depends on partial planning completeness.")
        if not analysis["linked_pathways"]:
            incomplete_inputs.append("Pathway planning is incomplete, so install realism behind the recommendation is still partial.")
        if analysis["main_panel"] is None:
            incomplete_inputs.append("Main panel context is missing, so architecture fit remains lower-confidence.")
        if not analysis["assigned_products"]:
            incomplete_inputs.append("Assigned equipment architecture is incomplete, so recommendation fit remains directional.")
        if not self._has_backup_scope(analysis):
            incomplete_inputs.append("No essential or backup load grouping is recorded, so resilience scope remains incomplete.")
        elif load_summary["planning_gap_warning"]:
            incomplete_inputs.append(load_summary["planning_gap_warning"])
        return signals, estimated_inputs, incomplete_inputs

    def _profile_architecture_fit(
        self,
        analysis,
        profile: RecommendationProfile,
        current_home_energy_architecture: CurrentHomeEnergyArchitectureEstimate,
        panel_service_architecture: PanelServiceArchitectureEstimate,
        inverter_system_architecture: InverterSystemArchitectureEstimate,
    ) -> ProfileArchitectureFitAssessment:
        load_summary = self._backup_scope_selection(analysis, profile)
        product_types = analysis["product_types"]
        architecture_type = analysis["design"].architecture_type or "not_recorded"
        consistency_status = (
            panel_service_architecture.architecture_consistency.status
            if panel_service_architecture.architecture_consistency is not None
            else "unknown"
        )
        recommended_backup_architecture = panel_service_architecture.recommended_backup_architecture
        recommended_system_architecture = inverter_system_architecture.recommended_system_architecture

        has_battery = "battery" in product_types
        has_hybrid = "hybrid_inverter" in product_types
        has_generator = "generator" in product_types
        has_gateway = "gateway" in product_types
        has_smart_panel = "smart_panel" in product_types
        current_topology = current_home_energy_architecture.inverter_topology

        if current_topology == "microinverter system" and has_battery:
            equipment_mix_summary = "Existing microinverter solar plus recorded battery signals point toward an AC-coupled retrofit planning path."
        elif current_topology == "microinverter system":
            equipment_mix_summary = "Existing microinverter solar is already recorded, so future storage fit should be read through an AC-coupled planning posture unless later hardware proves otherwise."
        elif current_topology == "optimizer-based system":
            equipment_mix_summary = "Current solar appears optimizer-based, so storage fit still depends on the inverter/control path rather than assuming simple backup behavior."
        elif has_hybrid and has_generator:
            equipment_mix_summary = "Hybrid inverter and generator signals already push the design toward a broader, staged backup path."
        elif has_hybrid:
            equipment_mix_summary = "Hybrid inverter signals point toward a more integrated backup path than a simple starter architecture."
        elif has_smart_panel or has_gateway:
            equipment_mix_summary = "Control-path equipment signals leave room for selective-load backup without forcing a whole-home claim."
        elif has_battery:
            equipment_mix_summary = "Battery equipment is already recorded, but control-path hardware remains intentionally open."
        else:
            equipment_mix_summary = "No explicit storage or control-path hardware is recorded yet, so profile fit stays more directional."

        backup_path_summary = (
            f"Recorded outage posture is '{load_summary['outage_posture']}', panel/service direction resolves to '{recommended_backup_architecture}', and inverter/system posture resolves to '{recommended_system_architecture}'."
        )

        tradeoffs: List[str] = []
        warnings: List[str] = []

        if profile == RecommendationProfile.critical_efficient:
            if load_summary["supports_whole_home_backup"] or recommended_backup_architecture == "whole-home backup":
                status = "stretched"
                summary = "Critical / Efficient is narrower than the recorded backup path."
                reason = "Whole-home-oriented outage posture or architecture direction exceeds a disciplined critical-load philosophy."
            elif load_summary["supports_partial_home_backup"] or has_generator or has_hybrid:
                status = "conditional"
                summary = "Critical / Efficient can still fit, but broader backup signals are already present."
                reason = "The design still supports a lean phase-one posture, yet the recorded backup path leaves room for a broader architecture than this profile prefers."
            else:
                status = "aligned"
                summary = "Critical / Efficient matches the current narrow backup path."
                reason = "Recorded loads and architecture signals still behave like a phase-one critical-load plan."
            tradeoffs.append("Lower phase-one scope reduces upfront commitment but can slow expansion into broader backup coverage later.")
            if load_summary["supports_partial_home_backup"]:
                warnings.append("Preferred-load grouping already extends beyond essentials, so this profile would intentionally understate the broader recorded outage posture.")
        elif profile == RecommendationProfile.balanced:
            if recommended_backup_architecture in {"partial-home backup", "smart-panel/load-control assisted"} and consistency_status == "aligned":
                status = "aligned"
                summary = "Balanced matches the current partial-home planning posture."
                reason = "Recorded outage posture and panel/service direction both support a practical middle path without forcing premium future-ready scope."
            elif load_summary["supports_whole_home_backup"] or has_generator or has_hybrid:
                status = "conditional"
                summary = "Balanced remains viable, but the architecture already contains broader continuity signals."
                reason = "The design can still be planned as a middle path, though generator, hybrid, or near-whole-home signals pull the fit upward."
            else:
                status = "conditional"
                summary = "Balanced remains viable, but the current scope is still narrow."
                reason = "The design is still close to critical-load planning, so this profile assumes some broader backup growth that is not fully recorded yet."
            tradeoffs.append("Balanced preserves meaningful outage coverage without committing as early to premium future-ready infrastructure.")
            if consistency_status != "aligned":
                warnings.append("Architecture consistency is not fully aligned, so balanced fit should be read as planning guidance rather than settled architecture direction.")
        elif profile == RecommendationProfile.conservative:
            if (
                load_summary["supports_partial_home_backup"]
                and recommended_backup_architecture in {"partial-home backup", "whole-home backup", "future-ready service upgrade path"}
            ):
                status = "aligned"
                summary = "Conservative matches the stronger outage-protection posture."
                reason = "Recorded backup scope already reaches beyond essentials, and the current architecture direction keeps more resilience headroom available."
            elif load_summary["selected_load_count"]:
                status = "conditional"
                summary = "Conservative can fit, but the current backup path is not fully broadened."
                reason = "The design shows some resilience ambition, yet the selected outage posture or architecture direction still stops short of a clearly broader backup path."
            else:
                status = "stretched"
                summary = "Conservative is weakly grounded until backup scope is recorded."
                reason = "Without explicit load grouping, the stronger outage-protection stance becomes harder to justify from structured evidence."
            tradeoffs.append("Conservative adds resilience headroom, but that caution can overshoot a lean first-phase design.")
            if not has_battery:
                warnings.append("No battery equipment is recorded yet, so the conservative posture leans on planning intent more than equipment evidence.")
        else:
            if (
                analysis["design"].design_goal in {"expansion_ready", "workshop_ready", "whole_home_backup", "off_grid_capable"}
                or has_hybrid
                or has_generator
                or len(analysis["linked_pathways"]) > 1
                or recommended_backup_architecture == "future-ready service upgrade path"
            ):
                status = "aligned"
                summary = "Premium / Future-Ready matches the broader architecture and expansion posture."
                reason = "Current equipment mix or design intent already preserves future flexibility beyond a simple starter backup path."
            elif load_summary["supports_partial_home_backup"]:
                status = "conditional"
                summary = "Premium / Future-Ready remains plausible, but the recorded path is still only partial-home."
                reason = "The design carries some broader backup ambition, yet the current outage posture and architecture direction are not fully future-ready on their own."
            else:
                status = "stretched"
                summary = "Premium / Future-Ready is broader than the current design evidence."
                reason = "The recorded outage posture and equipment mix are still closer to an early-phase resilience plan than a future-ready architecture."
            tradeoffs.append("Future-ready posture preserves headroom and retrofit flexibility but can raise phase-one complexity before the broader scope is fully grounded.")
            if consistency_status == "conditional":
                warnings.append("The design goal is broader than the recorded backup scope, so future-ready fit should not be treated as evidence of whole-home readiness.")

        if current_topology == "microinverter system" and profile in {
            RecommendationProfile.conservative,
            RecommendationProfile.premium_future_ready,
        }:
            tradeoffs.append("Existing microinverter solar can still support broader resilience planning, but future-ready storage often depends on a clearer AC-coupled retrofit path than a hybrid-first posture.")
        if architecture_type == "hybrid" and profile in {
            RecommendationProfile.critical_efficient,
            RecommendationProfile.balanced,
        }:
            tradeoffs.append("The recorded hybrid architecture keeps broader integration options open, which can be more infrastructure than a narrower profile strictly needs.")
        elif architecture_type == "ac_coupled" and profile in {
            RecommendationProfile.conservative,
            RecommendationProfile.premium_future_ready,
        }:
            tradeoffs.append("The recorded AC-coupled architecture keeps phase one simpler, but it may preserve less long-term flexibility than this profile prefers.")

        return ProfileArchitectureFitAssessment(
            status=status,
            equipment_mix_summary=equipment_mix_summary,
            backup_path_summary=backup_path_summary,
            summary=summary,
            reason=reason,
            tradeoffs=tradeoffs,
            warnings=warnings,
        )

    def _system_architecture_consistency_check(
        self,
        analysis,
        recommended_system_architecture: str,
        panel_service_architecture: PanelServiceArchitectureEstimate,
    ) -> ArchitectureConsistencyCheck:
        product_types = analysis["product_types"]
        architecture_type = analysis["design"].architecture_type or "not_recorded"
        backup_direction = panel_service_architecture.recommended_backup_architecture
        warnings: List[str] = []

        has_hybrid = "hybrid_inverter" in product_types
        has_ac_inverter = bool(product_types.intersection({"microinverter", "string_inverter"}))
        has_generator = "generator" in product_types
        has_transfer_path = bool(product_types.intersection({"gateway", "transfer_switch", "disconnect"}))
        has_battery = "battery" in product_types

        if "hybrid inverter backbone" in recommended_system_architecture and architecture_type == "ac_coupled" and not has_hybrid:
            warnings.append(
                "Hybrid-centered system direction is still partially inferred because the recorded architecture type remains AC-coupled and no hybrid inverter is assigned."
            )
            status = "conditional"
            summary = "System architecture direction is broader than the recorded architecture type."
            reason = "Current backup and expansion signals pull toward a hybrid path, but the structured architecture record does not fully support that shift yet."
        elif "ac-coupled" in recommended_system_architecture and has_hybrid:
            warnings.append(
                "AC-coupled system direction is narrow compared with the assigned hybrid inverter signal."
            )
            status = "conditional"
            summary = "System architecture direction is narrower than the recorded equipment path."
            reason = "The assigned equipment already supports a more integrated hybrid path than the current system-direction label suggests."
        elif has_generator and "generator" in recommended_system_architecture and not has_transfer_path:
            warnings.append(
                "Generator coexistence remains weakly grounded because no gateway, transfer switch, or disconnect path is recorded."
            )
            status = "conditional"
            summary = "System architecture direction is only partially grounded."
            reason = "Generator signals exist, but the control or transfer path needed to describe coexistence is still incomplete."
        elif has_battery and not (has_hybrid or has_ac_inverter) and "needs inverter clarification" in recommended_system_architecture:
            status = "conditional"
            summary = "System architecture direction correctly reflects an unresolved inverter path."
            reason = "Battery signals exist without explicit inverter hardware, so the planning direction stays intentionally provisional."
        elif architecture_type == "hybrid" and backup_direction == "critical-loads subpanel" and not has_hybrid:
            warnings.append(
                "The recorded hybrid architecture type is stronger than the currently assigned hardware and backup direction."
            )
            status = "conditional"
            summary = "System architecture direction is only partially aligned with the recorded architecture type."
            reason = "The design record points toward a hybrid path, but hardware and backup-path signals still behave like an early-phase architecture."
        else:
            status = "aligned"
            summary = "System architecture direction is consistent with the recorded architecture and equipment signals."
            reason = "Recorded architecture type, inverter/control equipment, and current backup direction point to the same planning posture."

        return ArchitectureConsistencyCheck(
            status=status,
            summary=summary,
            reason=reason,
            warnings=warnings,
        )

    def _inverter_system_architecture_estimate(
        self,
        db,
        analysis,
        profile: RecommendationProfile,
        confidence: ConfidenceLevel,
        current_home_energy_architecture: CurrentHomeEnergyArchitectureEstimate,
        panel_service_architecture: PanelServiceArchitectureEstimate,
        rule_documents_map=None,
    ) -> InverterSystemArchitectureEstimate:
        product_types = analysis["product_types"]
        design = analysis["design"]
        load_summary = self._backup_load_model_summary(analysis, profile)
        architecture_type = (design.architecture_type or "not recorded").replace("_", " ")
        current_topology = current_home_energy_architecture.inverter_topology

        has_battery = "battery" in product_types
        has_generator = "generator" in product_types
        has_hybrid = "hybrid_inverter" in product_types
        has_ac_inverter = bool(product_types.intersection({"microinverter", "string_inverter"}))
        has_gateway = "gateway" in product_types
        has_transfer_path = bool(product_types.intersection({"gateway", "transfer_switch", "disconnect"}))
        has_solar_generation = bool(product_types.intersection({"solar_panel", "microinverter", "string_inverter", "hybrid_inverter"}))
        multi_building = bool(analysis["workshop_buildings"] or len(analysis["linked_pathways"]) > 1)
        backup_direction = panel_service_architecture.recommended_backup_architecture

        if current_topology == "DC-coupled battery system":
            inverter_pathway_posture = "existing hybrid-centered solar-plus-storage path is explicitly signaled"
            recommended_system_architecture = "hybrid inverter backbone"
        elif current_topology == "AC-coupled battery retrofit":
            inverter_pathway_posture = "existing solar-plus-storage topology already reads as an ac-coupled retrofit path"
            recommended_system_architecture = "ac-coupled battery retrofit path"
        elif current_topology == "microinverter system" and has_battery:
            inverter_pathway_posture = "existing microinverter solar suggests an ac-coupled battery retrofit path"
            recommended_system_architecture = "ac-coupled battery retrofit path"
        elif current_topology == "microinverter system":
            inverter_pathway_posture = "existing microinverter solar path is explicitly signaled"
            recommended_system_architecture = "existing microinverter solar-first path"
        elif current_topology == "string inverter system" and has_battery:
            inverter_pathway_posture = "existing string-inverter solar suggests an ac-coupled battery retrofit path"
            recommended_system_architecture = "ac-coupled battery retrofit path"
        elif current_topology == "string inverter system":
            inverter_pathway_posture = "existing string-inverter solar path is explicitly signaled"
            recommended_system_architecture = "existing string-inverter solar-first path"
        elif current_topology == "optimizer-based system" and has_battery:
            inverter_pathway_posture = "existing optimizer-based solar suggests an ac-coupled battery retrofit path until a hybrid path is explicitly recorded"
            recommended_system_architecture = "ac-coupled battery retrofit path"
        elif has_hybrid and has_generator and has_transfer_path:
            inverter_pathway_posture = "hybrid-plus-generator path is explicitly signaled"
            recommended_system_architecture = "hybrid inverter backbone with generator coexistence"
        elif has_hybrid:
            inverter_pathway_posture = "hybrid inverter path is explicitly signaled"
            recommended_system_architecture = "hybrid inverter backbone"
        elif has_ac_inverter and has_battery:
            inverter_pathway_posture = "ac-coupled solar-plus-storage path is partially signaled"
            recommended_system_architecture = "ac-coupled solar plus storage path"
        elif has_ac_inverter:
            inverter_pathway_posture = "ac-coupled solar path is explicitly signaled"
            recommended_system_architecture = "ac-coupled solar-first path"
        elif has_battery and has_transfer_path:
            inverter_pathway_posture = "battery-first backup path is signaled, but inverter posture remains partially inferred"
            recommended_system_architecture = "battery-ready path with control hardware"
        elif has_battery:
            inverter_pathway_posture = "battery-first backup path is signaled, but inverter posture is still open"
            recommended_system_architecture = "battery-ready path needs inverter clarification"
        elif has_generator:
            inverter_pathway_posture = "generator coexistence is signaled, but inverter/control posture is incomplete"
            recommended_system_architecture = "generator-augmented path needs inverter clarification"
        else:
            inverter_pathway_posture = "no explicit inverter or backup-conversion path is recorded yet"
            recommended_system_architecture = "system architecture path remains open"

        if current_topology in {"microinverter system", "string inverter system", "optimizer-based system", "AC-coupled battery retrofit"}:
            hybrid_inverter_pathway_suitability = "conditional" if has_battery or has_generator or multi_building else "limited"
        elif has_hybrid or design.architecture_type == "hybrid":
            hybrid_inverter_pathway_suitability = (
                "favorable"
                if load_summary["supports_partial_home_backup"] or multi_building or has_generator
                else "conditional"
            )
        elif has_battery or has_generator or multi_building:
            hybrid_inverter_pathway_suitability = "conditional"
        else:
            hybrid_inverter_pathway_suitability = "limited"

        if current_topology in {"microinverter system", "string inverter system", "optimizer-based system", "AC-coupled battery retrofit"}:
            ac_coupled_pathway_suitability = (
                "favorable"
                if backup_direction in {"critical-loads subpanel", "partial-home backup"} and not has_hybrid
                else "conditional"
            )
        elif design.architecture_type == "ac_coupled" or has_ac_inverter:
            ac_coupled_pathway_suitability = (
                "favorable"
                if backup_direction in {"critical-loads subpanel", "partial-home backup"} and not has_hybrid
                else "conditional"
            )
        elif has_solar_generation and not has_hybrid:
            ac_coupled_pathway_suitability = "conditional"
        else:
            ac_coupled_pathway_suitability = "limited"

        if current_topology in {"microinverter system", "string inverter system", "optimizer-based system"} and has_battery:
            battery_integration_assumption = current_home_energy_architecture.battery_retrofit_implication
        elif has_battery and has_hybrid:
            battery_integration_assumption = (
                "Battery coexistence is most coherent through a hybrid-centered planning path, though final coupling details remain deferred."
            )
        elif has_battery and has_ac_inverter:
            battery_integration_assumption = (
                "Battery coexistence likely depends on an AC-coupled control strategy, but the exact inverter/control relationship is still planning-only."
            )
        elif has_battery:
            battery_integration_assumption = (
                "Battery signals exist, but the conversion/control path is still incomplete, so storage topology remains provisional."
            )
        else:
            battery_integration_assumption = "No battery signal is recorded, so storage coexistence remains outside the current architecture posture."

        if current_topology == "microinverter system":
            solar_integration_assumption = (
                "Existing solar appears microinverter-based. It should not be assumed to run through outages unless compatible backup gateway, grid-forming, and storage architecture is also present."
            )
        elif current_topology == "string inverter system":
            solar_integration_assumption = (
                "Existing solar appears string-inverter-based, but outage behavior and storage integration still depend on the recorded control and backup path."
            )
        elif current_topology == "optimizer-based system":
            solar_integration_assumption = (
                "Existing solar appears optimizer-based, but outage behavior still depends on the paired inverter and backup-control architecture rather than optimizer presence alone."
            )
        elif has_solar_generation and has_hybrid:
            solar_integration_assumption = (
                "Solar and storage can be planned on a shared hybrid-centered architecture path, but product-specific topology remains deferred."
            )
        elif has_solar_generation and has_ac_inverter:
            solar_integration_assumption = (
                "Solar appears to fit an AC-coupled path, and storage additions would likely layer on top of that planning posture."
            )
        elif has_solar_generation:
            solar_integration_assumption = (
                "Solar generation is implied by product signals, but the conversion path is still incomplete."
            )
        else:
            solar_integration_assumption = "No explicit solar-conversion signal is recorded, so solar coexistence remains only directional."

        if current_home_energy_architecture.generator_coexistence_note:
            generator_coexistence_assumption = current_home_energy_architecture.generator_coexistence_note
        elif has_generator and has_transfer_path and has_hybrid:
            generator_coexistence_assumption = (
                "Generator coexistence is planning-compatible with a hybrid-centered path because both generation and transfer/control signals are recorded."
            )
        elif has_generator and has_transfer_path:
            generator_coexistence_assumption = (
                "Generator coexistence is partially grounded through transfer/control signals, though inverter behavior remains planning-only."
            )
        elif has_generator:
            generator_coexistence_assumption = (
                "Generator coexistence is weakly grounded because generation is recorded without a matching transfer or gateway path."
            )
        else:
            generator_coexistence_assumption = "No generator signal is recorded, so generator coexistence remains outside the current architecture posture."

        if current_topology == "microinverter system":
            expansion_path_posture = "existing microinverter solar keeps a modular expansion path open"
        elif design.design_goal in {"expansion_ready", "workshop_ready"} or multi_building or backup_direction == "future-ready service upgrade path":
            expansion_path_posture = "future-ready expansion path is favored"
        elif load_summary["supports_partial_home_backup"] or has_battery or has_transfer_path:
            expansion_path_posture = "moderate expansion path is preserved"
        else:
            expansion_path_posture = "first-phase architecture remains narrower than future-ready expansion"

        if current_topology in {"microinverter system", "string inverter system", "AC-coupled battery retrofit"}:
            confidence_level = current_home_energy_architecture.topology_confidence
            confidence_reason = (
                f"System-architecture confidence inherits the current topology classification because the home appears to have a {current_topology} and the future pathway remains planning-only."
            )
        elif has_hybrid and design.architecture_type == "hybrid" and panel_service_architecture.architecture_consistency and panel_service_architecture.architecture_consistency.status == "aligned":
            confidence_level = ConfidenceLevel.high
            confidence_reason = "System-architecture confidence is high because architecture type, hybrid equipment, and backup direction all point to the same planning path."
        elif (has_ac_inverter or has_hybrid or has_transfer_path) and design.architecture_type:
            confidence_level = ConfidenceLevel.medium
            confidence_reason = "System-architecture confidence is medium because some inverter or control-path signals are recorded, but coexistence assumptions are still planning-only."
        else:
            confidence_level = ConfidenceLevel.low
            confidence_reason = "System-architecture confidence is low because the current design lacks explicit inverter or transfer-path records."

        consistency = self._system_architecture_consistency_check(
            analysis,
            recommended_system_architecture,
            panel_service_architecture,
        )
        if consistency.status != "aligned" and confidence_level == ConfidenceLevel.high:
            confidence_level = ConfidenceLevel.medium
            confidence_reason = "System-architecture confidence drops to medium because the planning direction still has unresolved consistency gaps."

        input_signals = [
            {
                "key": "current_topology",
                "label": "Current home energy topology",
                "value": current_topology,
                "status": "rule_based",
                "note": "Current-state topology is kept separate from the future system recommendation so existing solar is not mistaken for a final backup-capable architecture.",
            },
            {
                "key": "recorded_architecture_type",
                "label": "Recorded architecture type",
                "value": architecture_type,
                "status": "recorded" if design.architecture_type else "missing",
                "note": "The stored architecture type is a planning posture, not a final engineered topology.",
            },
            {
                "key": "inverter_equipment_signals",
                "label": "Inverter equipment signals",
                "value": ", ".join(
                    sorted(
                        product_type.replace("_", " ")
                        for product_type in product_types.intersection({"microinverter", "string_inverter", "hybrid_inverter"})
                    )
                )
                or "No explicit inverter products recorded",
                "status": "recorded" if has_hybrid or has_ac_inverter else "missing",
                "note": "Explicit inverter products make the system-architecture path more grounded than architecture type alone.",
            },
            {
                "key": "backup_direction",
                "label": "Backup architecture direction",
                "value": backup_direction,
                "status": "rule_based",
                "note": "Inverter/system reasoning inherits the current planning-only backup direction rather than inventing a broader backup path.",
            },
            {
                "key": "battery_generator_signals",
                "label": "Battery and generator coexistence signals",
                "value": (
                    f"battery={has_battery}, generator={has_generator}, control_path={has_transfer_path}"
                ),
                "status": "recorded" if has_battery or has_generator or has_transfer_path else "missing",
                "note": "Coexistence assumptions stay grounded in recorded equipment and transfer/control-path signals only.",
            },
            {
                "key": "pathway_context",
                "label": "Pathway and expansion context",
                "value": f"{len(analysis['linked_pathways'])} linked pathways, {len(analysis['workshop_buildings'])} workshop buildings",
                "status": "recorded" if analysis["linked_pathways"] or analysis["workshop_buildings"] else "missing",
                "note": "Multi-building or longer-path context can make hybrid or future-ready paths more realistic at planning time.",
            },
            {
                "key": "system_architecture_consistency",
                "label": "System architecture consistency",
                "value": consistency.status,
                "status": "rule_based",
                "note": "Checks whether architecture type, equipment signals, and backup direction describe the same planning posture.",
            },
        ]
        estimated_inputs: List[str] = [
            "System architecture reasoning is planning-only and does not confirm inverter sizing, interconnection method, or final transfer topology."
        ]
        incomplete_inputs: List[str] = []
        if current_topology == "microinverter system" and not has_transfer_path:
            incomplete_inputs.append("Existing microinverter solar does not imply outage operation, because no gateway, transfer, or grid-forming path is recorded.")
        if has_battery and not (has_hybrid or has_ac_inverter):
            incomplete_inputs.append("Battery equipment is recorded without explicit inverter hardware, so storage topology remains provisional.")
        if has_generator and not has_transfer_path:
            incomplete_inputs.append("Generator signals exist without a gateway, transfer switch, or disconnect path, so coexistence remains only partially grounded.")
        if not design.architecture_type:
            incomplete_inputs.append("Architecture type is not recorded, so system direction relies more heavily on partial equipment signals.")
        if not analysis["linked_pathways"]:
            incomplete_inputs.append("No linked pathways are recorded, so inverter/system direction remains less grounded in install-path realism.")
        if load_summary["planning_gap_warning"]:
            incomplete_inputs.append(load_summary["planning_gap_warning"])
        if consistency.warnings:
            incomplete_inputs.extend(consistency.warnings)

        inspectability = provenance_service.build_estimate_inspectability(
            db,
            basis="Inverter and system architecture reasoning is based on current topology classification, recorded architecture type, explicit inverter/control equipment, backup-scope posture, panel/service direction, battery and generator coexistence signals, and pathway context.",
            confidence_level=confidence_level,
            rule_keys=[
                "recommendation.backup_load_selection_v1",
                "recommendation.current_home_energy_architecture_v1",
                "recommendation.panel_service_preliminary_architecture_v1",
                "recommendation.backup_architecture_consistency_v1",
                "recommendation.inverter_system_architecture_v1",
            ],
            input_signals=input_signals,
            estimated_inputs=estimated_inputs,
            incomplete_inputs=incomplete_inputs,
            notes=[
                "This layer reasons about planning architecture posture only and should not be treated as an electrical design approval or final inverter selection.",
            ],
            rule_documents_map=rule_documents_map,
        )

        return InverterSystemArchitectureEstimate(
            recorded_architecture_type=architecture_type,
            inverter_pathway_posture=inverter_pathway_posture,
            recommended_system_architecture=recommended_system_architecture,
            ac_coupled_pathway_suitability=ac_coupled_pathway_suitability,
            hybrid_inverter_pathway_suitability=hybrid_inverter_pathway_suitability,
            battery_integration_assumption=battery_integration_assumption,
            solar_integration_assumption=solar_integration_assumption,
            generator_coexistence_assumption=generator_coexistence_assumption,
            expansion_path_posture=expansion_path_posture,
            confidence_reason=confidence_reason,
            scope_note="Planning estimate only. This inverter/system architecture layer explains likely AC-coupled vs hybrid posture, coexistence assumptions, and expansion direction before final inverter, generator, or interconnection design.",
            architecture_consistency=consistency,
            inspectability=inspectability,
        )

    def _battery_sizing_estimate(
        self, analysis, profile: RecommendationProfile, config
    ) -> BatterySizingEstimate:
        backup_load_energy_need_kwh = self._backup_load_energy_need_kwh(analysis, profile)
        autonomy_min, autonomy_max = calc.AUTONOMY_HOUR_RANGES[config["autonomy_reserve_posture"]]
        usable_range = None
        recommended_range = None
        scope_note = "Planning estimate only. This range is derived from current backup-load modeling and recommendation posture, not final engineered battery design."

        ranges = calc.battery_capacity_ranges(
            backup_load_energy_need_kwh,
            config["autonomy_reserve_posture"],
            config["reserve_margin_posture"],
            config["future_growth_margin_posture"],
        )
        if ranges is not None:
            usable_range = BatteryCapacityRange(
                min_kwh=ranges.usable_min_kwh,
                max_kwh=ranges.usable_max_kwh,
            )
            recommended_range = BatteryCapacityRange(
                min_kwh=ranges.recommended_min_kwh,
                max_kwh=ranges.recommended_max_kwh,
            )
        else:
            scope_note = "Planning estimate unavailable. Record essential or backup load scope before relying on battery guidance."

        return BatterySizingEstimate(
            backup_load_energy_need_kwh=backup_load_energy_need_kwh,
            autonomy_duration_hours_min=autonomy_min,
            autonomy_duration_hours_max=autonomy_max,
            usable_battery_capacity_range_kwh=usable_range,
            reserve_margin_posture=config["reserve_margin_posture"],
            future_growth_margin_posture=config["future_growth_margin_posture"],
            recommended_battery_capacity_range_kwh=recommended_range,
            scope_note=scope_note,
        )

    def _battery_inspectability(
        self,
        db,
        analysis,
        profile: RecommendationProfile,
        config,
        battery_sizing: BatterySizingEstimate,
        confidence: ConfidenceLevel,
        rule_documents_map=None,
    ):
        load_summary = self._backup_load_model_summary(analysis, profile)
        input_signals = [
            {
                "key": "backup_energy_need",
                "label": "Backup load energy need",
                "value": (
                    f"{battery_sizing.backup_load_energy_need_kwh} kWh/day"
                    if battery_sizing.backup_load_energy_need_kwh is not None
                    else "not enough load data yet"
                ),
                "status": "estimated" if battery_sizing.backup_load_energy_need_kwh is not None else "missing",
                "note": (
                    "Derived from the currently selected essential or backup loads and their recorded daily-hour assumptions."
                    if battery_sizing.backup_load_energy_need_kwh is not None
                    else "Battery guidance remains unavailable until an essential or backup load group is recorded."
                ),
            },
            {
                "key": "selected_backup_scope",
                "label": "Selected backup scope",
                "value": f"{load_summary['selected_load_count']} loads from {load_summary['selected_scope_label']}",
                "status": "rule_based" if load_summary["selected_load_count"] else "missing",
                "note": "Battery guidance uses the explicit selected load group rather than assuming broader outage intent.",
            },
            {
                "key": "autonomy_posture",
                "label": "Autonomy duration posture",
                "value": f"{battery_sizing.autonomy_duration_hours_min}-{battery_sizing.autonomy_duration_hours_max} hours",
                "status": "rule_based",
                "note": "Autonomy target is set by the selected recommendation profile, not by a final engineered outage study.",
            },
            {
                "key": "reserve_margin_posture",
                "label": "Reserve margin posture",
                "value": config["reserve_margin_posture"].replace("_", " "),
                "status": "rule_based",
                "note": "Reserve posture expresses planning caution rather than a disclosed reserve formula.",
            },
            {
                "key": "future_growth_margin_posture",
                "label": "Future growth margin posture",
                "value": config["future_growth_margin_posture"].replace("_", " "),
                "status": "rule_based",
                "note": "Growth margin reflects future expansion stance, not a commitment to a final build scope.",
            },
        ]
        estimated_inputs: List[str] = [
            f"Backup energy need is derived from {load_summary['selected_source'].replace('_', ' ')} and current daily-use assumptions."
        ]
        incomplete_inputs: List[str] = []
        if load_summary["missing_daily_hour_loads"]:
            estimated_inputs.append(
                "Some selected loads are missing daily-hour assumptions and weaken confidence in the backup energy estimate."
            )
        if load_summary["fallback_applied"]:
            estimated_inputs.append(
                "Fallback runtime assumptions were required because no recorded daily-hour data was available for the selected load group."
            )
        if not load_summary["selected_load_count"]:
            incomplete_inputs.append("No selected backup load group is recorded, so battery guidance is not grounded in actual load scope.")
        elif load_summary["planning_gap_warning"]:
            incomplete_inputs.append(load_summary["planning_gap_warning"])
        return provenance_service.build_estimate_inspectability(
            db,
            basis="Battery guidance is based on the selected recommendation profile, current backup-load modeling, and planning postures for autonomy, reserve, and future growth.",
            confidence_level=confidence,
            rule_keys=[
                "recommendation.resilience_profile_matrix_v1",
                "recommendation.profile_battery_sizing_v1",
            ],
            input_signals=input_signals,
            estimated_inputs=estimated_inputs,
            incomplete_inputs=incomplete_inputs,
            notes=[
                "Battery range guidance remains planning-only and should be revalidated against site conditions, actual product constraints, and final load modeling.",
            ],
            rule_documents_map=rule_documents_map,
        )

    def _solar_sizing_estimate(self, analysis, config, battery_sizing: BatterySizingEstimate) -> SolarSizingEstimate:
        solar_posture = config["solar_sizing_posture"]
        low_solar_posture = config["low_solar_assumption_posture"]
        recovery_strength = self.RECOVERY_STRENGTH[solar_posture]
        seasonal_conservatism = self.SEASONAL_CONSERVATISM[low_solar_posture]

        site_capacity = self._site_capacity_adjustment(analysis)
        roof_geometry_readiness = self._roof_geometry_readiness(analysis)
        shading = self._shading_adjustment(analysis)
        seasonal_region = self._seasonal_region_adjustment(analysis)
        install_realism = self._install_realism_adjustment(analysis)
        base_recommended_range = None
        recommended_range = None
        scope_note = "Planning estimate only. This range starts from profile-based recovery posture and current backup-load modeling, then applies coarse site-aware caution signals. It is not a final engineered production study."

        battery_recommended = battery_sizing.recommended_battery_capacity_range_kwh
        ranges = calc.solar_capacity_ranges(
            battery_sizing.backup_load_energy_need_kwh,
            battery_recommended.min_kwh if battery_recommended else None,
            battery_recommended.max_kwh if battery_recommended else None,
            solar_posture,
            site_capacity["factor_range"],
            shading["factor_range"],
            seasonal_region["factor_range"],
            install_realism["factor_range"],
        )
        if ranges is not None:
            base_recommended_range = SolarCapacityRange(
                min_kw=ranges.base_recommended_min_kw,
                max_kw=ranges.base_recommended_max_kw,
            )
            recommended_range = SolarCapacityRange(
                min_kw=ranges.recommended_min_kw,
                max_kw=ranges.recommended_max_kw,
            )
        else:
            scope_note = "Planning estimate unavailable. Record essential or backup load scope before relying on solar recovery guidance."

        low_solar_note_map = {
            LowSolarAssumptionPosture.favorable: "Assumes more forgiving solar conditions; resilience weakens faster during extended cloudy periods.",
            LowSolarAssumptionPosture.typical: "Balances normal day-to-day recovery expectations with moderate low-solar caution.",
            LowSolarAssumptionPosture.protective: "Holds more solar headroom against weaker production periods and slower battery refill days.",
            LowSolarAssumptionPosture.defensive: "Preserves the strongest low-solar cushion so battery recovery remains credible during weaker production windows.",
        }
        recovery_relationship_map = {
            RecoveryStrengthPosture.modest: "Solar range is intended to support slower battery recovery after outages while keeping first-phase scope tighter.",
            RecoveryStrengthPosture.balanced: "Solar range is intended to support practical day-to-day battery recovery without pushing into premium overbuild.",
            RecoveryStrengthPosture.strong: "Solar range is intended to restore battery reserves more assertively after outage use or weaker production days.",
            RecoveryStrengthPosture.aggressive: "Solar range is intended to recover battery reserves quickly and preserve future-ready resilience headroom.",
        }

        return SolarSizingEstimate(
            solar_production_posture=solar_posture,
            low_solar_condition_posture=low_solar_posture,
            recovery_strength=recovery_strength,
            seasonal_conservatism=seasonal_conservatism,
            base_recommended_solar_capacity_range_kw=base_recommended_range,
            recommended_solar_capacity_range_kw=recommended_range,
            site_capacity_posture=site_capacity["posture"],
            shading_obstruction_caution=shading["note"],
            seasonal_production_caution=seasonal_region["note"],
            install_realism_caution=install_realism["note"],
            battery_recovery_relationship=recovery_relationship_map[recovery_strength],
            low_solar_resilience_note=low_solar_note_map[low_solar_posture],
            roof_geometry_readiness=roof_geometry_readiness,
            scope_note=scope_note,
        )

    def _solar_inspectability(
        self,
        db,
        analysis,
        profile: RecommendationProfile,
        config,
        battery_sizing: BatterySizingEstimate,
        solar_sizing: SolarSizingEstimate,
        confidence: ConfidenceLevel,
        rule_documents_map=None,
    ):
        load_summary = self._backup_load_model_summary(analysis, profile)
        input_signals = [
            {
                "key": "base_solar_range_guidance",
                "label": "Base solar range before site adjustment",
                "value": (
                    f"{solar_sizing.base_recommended_solar_capacity_range_kw.min_kw}-{solar_sizing.base_recommended_solar_capacity_range_kw.max_kw} kW"
                    if solar_sizing.base_recommended_solar_capacity_range_kw is not None
                    else "not enough load data yet"
                ),
                "status": "estimated" if solar_sizing.base_recommended_solar_capacity_range_kw is not None else "missing",
                "note": (
                    "Initial solar range derived from profile-based recovery posture and current battery/backup-load planning before coarse site-aware adjustments."
                    if solar_sizing.base_recommended_solar_capacity_range_kw is not None
                    else "Solar guidance remains unavailable until a backup load scope is recorded."
                ),
            },
            {
                "key": "solar_range_guidance",
                "label": "Recommended solar range",
                "value": (
                    f"{solar_sizing.recommended_solar_capacity_range_kw.min_kw}-{solar_sizing.recommended_solar_capacity_range_kw.max_kw} kW"
                    if solar_sizing.recommended_solar_capacity_range_kw is not None
                    else "not enough load data yet"
                ),
                "status": "estimated" if solar_sizing.recommended_solar_capacity_range_kw is not None else "missing",
                "note": (
                    "Derived from the base profile-backed solar range plus coarse site-aware adjustment signals."
                    if solar_sizing.recommended_solar_capacity_range_kw is not None
                    else "Without a recorded backup load scope, the system cannot produce credible solar recovery guidance."
                ),
            },
            {
                "key": "solar_production_posture",
                "label": "Solar production posture",
                "value": config["solar_sizing_posture"].replace("_", " "),
                "status": "rule_based",
                "note": "This posture sets how strongly solar is expected to support resilience recovery.",
            },
            {
                "key": "selected_backup_scope",
                "label": "Selected backup scope",
                "value": f"{load_summary['selected_load_count']} loads from {load_summary['selected_scope_label']}",
                "status": "rule_based" if load_summary["selected_load_count"] else "missing",
                "note": "Solar recovery guidance inherits the same explicit selected backup scope used by battery guidance.",
            },
            {
                "key": "low_solar_posture",
                "label": "Low-solar assumption posture",
                "value": config["low_solar_assumption_posture"].replace("_", " "),
                "status": "rule_based",
                "note": "This posture reflects how cautious the planning model is about weaker production periods.",
            },
            {
                "key": "recovery_strength",
                "label": "Recovery posture",
                "value": solar_sizing.recovery_strength.replace("_", " "),
                "status": "rule_based",
                "note": "Recovery posture describes how assertively solar is expected to refill battery reserves after outage use.",
            },
            {
                "key": "battery_recovery_dependency",
                "label": "Battery recovery relationship",
                "value": solar_sizing.battery_recovery_relationship,
                "status": "estimated",
                "note": "Solar guidance is linked to the current battery planning range but does not expose internal recovery formulas.",
            },
            {
                "key": "site_capacity_posture",
                "label": "Site capacity posture",
                "value": solar_sizing.site_capacity_posture,
                "status": "estimated",
                "note": "Uses current roof-placement records when available; otherwise falls back to a conservative placement posture.",
            },
            {
                "key": "roof_data_completeness",
                "label": "Roof sizing confidence",
                "value": solar_sizing.roof_geometry_readiness.roof_measurement_confidence,
                "status": "estimated",
                "note": "Separates inferred placement realism from true measured roof-geometry certainty.",
            },
            {
                "key": "measured_geometry_status",
                "label": "Measured vs estimated status",
                "value": solar_sizing.roof_geometry_readiness.measured_geometry_status,
                "status": "estimated",
                "note": "Future GIS, traced polygons, roof planes, and usable-area estimates should upgrade this state without replacing the recommendation system.",
            },
            {
                "key": "shading_obstruction_posture",
                "label": "Shading and obstruction caution",
                "value": solar_sizing.shading_obstruction_caution,
                "status": "estimated",
                "note": "No explicit shading model exists yet, so this remains a coarse planning caution rather than a measured site factor.",
            },
            {
                "key": "seasonal_region_posture",
                "label": "Seasonal production caution",
                "value": solar_sizing.seasonal_production_caution,
                "status": "estimated",
                "note": "Uses the home state as a coarse production-region proxy rather than site-specific production modeling.",
            },
            {
                "key": "install_realism_posture",
                "label": "Install realism caution",
                "value": solar_sizing.install_realism_caution,
                "status": "estimated",
                "note": "Pathway and siting records influence caution and confidence rather than acting as a detailed engineering constraint model.",
            },
        ]
        estimated_inputs: List[str] = [
            "Solar range guidance is directional and depends on the current battery planning range plus low-solar posture."
        ]
        incomplete_inputs: List[str] = []
        if load_summary["missing_daily_hour_loads"]:
            estimated_inputs.append(
                "Some load-use assumptions remain incomplete, so solar recovery guidance inherits that uncertainty."
            )
        estimated_inputs.append(
            "Roof capacity, shading, and seasonal production are still modeled as coarse postures rather than site-specific production calculations."
        )
        estimated_inputs.append(
            "Roof sizing confidence currently reflects recorded placement realism, not measured roof geometry or scaled area."
        )
        if not analysis["linked_pathways"]:
            incomplete_inputs.append(
                "Pathway planning is incomplete, so solar guidance does not yet reflect a fully grounded install path."
            )
        if not any(location.location_type == "roof" for location in analysis["locations"]):
            incomplete_inputs.append(
                "No roof placement record exists yet, so site-capacity posture is conservative rather than strongly grounded."
            )
        if solar_sizing.roof_geometry_readiness.measured_geometry_status != "measured":
            incomplete_inputs.append(
                "Measured roof geometry is not available yet, so usable roof capacity remains an estimated planning posture."
            )
        if load_summary["planning_gap_warning"]:
            incomplete_inputs.append(load_summary["planning_gap_warning"])
        return provenance_service.build_estimate_inspectability(
            db,
            basis="Solar guidance is based on the selected recommendation profile, battery recovery posture, low-solar assumptions, the current backup-load model, and a coarse site-aware adjustment layer for placement, shading uncertainty, seasonal region, and install realism.",
            confidence_level=confidence,
            rule_keys=[
                "recommendation.resilience_profile_matrix_v1",
                "recommendation.profile_battery_sizing_v1",
                "recommendation.profile_solar_sizing_v1",
                "recommendation.profile_solar_site_adjustment_v1",
                "recommendation.roof_geometry_readiness_v1",
            ],
            input_signals=input_signals,
            estimated_inputs=estimated_inputs,
            incomplete_inputs=incomplete_inputs,
            notes=[
                "Solar range guidance remains planning-only and should be revalidated against site production study inputs, roof constraints, equipment limits, and seasonal conditions.",
            ],
            rule_documents_map=rule_documents_map,
        )

    def _recommended_profile(self, analysis, completeness) -> RecommendationProfile:
        design_goal = analysis["design"].design_goal
        product_types = analysis["product_types"]

        if design_goal == "lowest_cost":
            return RecommendationProfile.critical_efficient
        if design_goal in {"expansion_ready", "workshop_ready"}:
            return RecommendationProfile.premium_future_ready
        if design_goal == "partial_backup":
            return RecommendationProfile.balanced
        if design_goal in {"generator_assisted", "whole_home_backup", "off_grid_capable"}:
            if analysis["workshop_buildings"] or len(analysis["linked_pathways"]) > 1:
                return RecommendationProfile.premium_future_ready
            if "battery" in product_types or self._has_backup_scope(analysis):
                return RecommendationProfile.conservative
            return RecommendationProfile.balanced
        if completeness["completeness_score"] < 50:
            return RecommendationProfile.balanced
        return RecommendationProfile.balanced

    def _confidence_level(self, analysis, completeness) -> ConfidenceLevel:
        signals = 0
        has_load_scope = self._has_backup_scope(analysis)
        if analysis["main_panel"] is not None:
            signals += 1
        if analysis["essential_loads"]:
            signals += 1
        if analysis["assigned_products"]:
            signals += 1
        if analysis["linked_pathways"]:
            signals += 1
        if has_load_scope and completeness["completeness_score"] >= 75:
            return ConfidenceLevel.high
        if signals >= 3 and completeness["completeness_score"] >= 45:
            return ConfidenceLevel.medium
        return ConfidenceLevel.low

    def _fit_reason(
        self,
        profile: RecommendationProfile,
        analysis,
        architecture_fit: Optional[ProfileArchitectureFitAssessment] = None,
    ) -> str:
        design_goal = analysis["design"].design_goal.replace("_", " ")
        if architecture_fit is not None:
            return f"{architecture_fit.summary} {architecture_fit.reason}"
        if profile == RecommendationProfile.critical_efficient:
            return "Current design signals favor essential resilience scope over broader redundancy."
        if profile == RecommendationProfile.balanced:
            return "Current design signals support a middle path: meaningful backup planning without overcommitting future scope too early."
        if profile == RecommendationProfile.conservative:
            return f"Current design goal '{design_goal}' carries stronger resilience expectations, so a more protective posture fits best."
        return "Current design emphasizes future growth or broader continuity, so preserving long-term headroom is the best fit."

    def _reasoning_graph_dependency(
        self,
        source_node_id: str,
        target_node_id: str,
        relationship: str,
        summary: str,
        confidence_level: ConfidenceLevel,
        rule_keys: List[str],
    ) -> ReasoningGraphDependency:
        return ReasoningGraphDependency(
            source_node_id=source_node_id,
            target_node_id=target_node_id,
            relationship=relationship,
            summary=summary,
            confidence_level=confidence_level,
            rule_keys=rule_keys,
        )

    def _structured_system_reasoning_graph(
        self,
        db,
        profile_card: RecommendationProfileCard,
        backup_load_selection: BackupLoadSelectionSummary,
        current_home_energy_architecture: CurrentHomeEnergyArchitectureEstimate,
        panel_service_architecture: PanelServiceArchitectureEstimate,
        inverter_system_architecture: InverterSystemArchitectureEstimate,
        rule_documents_map=None,
    ) -> StructuredSystemReasoningGraph:
        battery_sizing = BatterySizingEstimate.parse_obj(profile_card.battery_sizing_estimate)
        solar_sizing = SolarSizingEstimate.parse_obj(profile_card.solar_sizing_estimate)
        profile_inspectability = EstimateInspectability.parse_obj(profile_card.inspectability)
        graph_rule_keys = [
            "recommendation.backup_load_selection_v1",
            "recommendation.current_home_energy_architecture_v1",
            "recommendation.panel_service_preliminary_architecture_v1",
            "recommendation.backup_architecture_consistency_v1",
            "recommendation.inverter_system_architecture_v1",
            "recommendation.profile_battery_sizing_v1",
            "recommendation.profile_solar_sizing_v1",
            "recommendation.profile_solar_site_adjustment_v1",
            "recommendation.system_reasoning_graph_v1",
        ]

        load_scope_summary = (
            f"{backup_load_selection.selected_load_count} selected loads from {backup_load_selection.selected_scope_label} "
            f"cover {int((backup_load_selection.coverage_ratio_of_recorded_loads or 0) * 100)}% of recorded loads."
            if backup_load_selection.selected_load_count
            else "No selected backup loads currently ground downstream planning layers."
        )
        battery_summary = (
            f"{battery_sizing.recommended_battery_capacity_range_kwh.min_kwh}-{battery_sizing.recommended_battery_capacity_range_kwh.max_kwh} kWh planning range "
            f"with a {battery_sizing.autonomy_duration_hours_min}-{battery_sizing.autonomy_duration_hours_max} hour autonomy posture."
            if battery_sizing.recommended_battery_capacity_range_kwh is not None
            else "Battery planning range remains unavailable until a selected backup scope exists."
        )
        solar_summary = (
            f"{solar_sizing.recommended_solar_capacity_range_kw.min_kw}-{solar_sizing.recommended_solar_capacity_range_kw.max_kw} kW planning range "
            f"with {solar_sizing.recovery_strength.replace('_', ' ')} recovery posture."
            if solar_sizing.recommended_solar_capacity_range_kw is not None
            else "Solar recovery guidance remains unavailable until battery and backup-scope planning are grounded."
        )

        nodes = [
            ReasoningGraphNode(
                node_id="loads",
                label="Recorded Load Grouping",
                category="loads",
                summary=load_scope_summary,
                status=backup_load_selection.selection_basis,
                confidence_level=backup_load_selection.confidence_level,
                rule_keys=["recommendation.backup_load_selection_v1"],
            ),
            ReasoningGraphNode(
                node_id="backup_scope",
                label="Backup Scope Posture",
                category="backup_scope",
                summary=backup_load_selection.outage_posture_reason,
                status=backup_load_selection.outage_posture,
                confidence_level=backup_load_selection.confidence_level,
                rule_keys=["recommendation.backup_load_selection_v1"],
            ),
            ReasoningGraphNode(
                node_id="current_topology",
                label="Current Solar / Inverter Topology",
                category="current_home_energy_architecture",
                summary=current_home_energy_architecture.current_vs_proposed_architecture,
                status=current_home_energy_architecture.inverter_topology,
                confidence_level=current_home_energy_architecture.topology_confidence,
                rule_keys=["recommendation.current_home_energy_architecture_v1"],
            ),
            ReasoningGraphNode(
                node_id="panel_service",
                label="Panel / Service Posture",
                category="panel_service",
                summary=panel_service_architecture.architecture_consistency.summary,
                status=panel_service_architecture.recommended_backup_architecture,
                confidence_level=panel_service_architecture.inspectability.confidence_level,
                rule_keys=[
                    "recommendation.panel_service_preliminary_architecture_v1",
                    "recommendation.backup_architecture_consistency_v1",
                ],
            ),
            ReasoningGraphNode(
                node_id="inverter_system",
                label="Inverter / System Architecture",
                category="inverter_system_architecture",
                summary=inverter_system_architecture.confidence_reason,
                status=inverter_system_architecture.recommended_system_architecture,
                confidence_level=inverter_system_architecture.inspectability.confidence_level,
                rule_keys=["recommendation.inverter_system_architecture_v1"],
            ),
            ReasoningGraphNode(
                node_id="battery_posture",
                label="Battery Posture",
                category="battery_posture",
                summary=battery_summary,
                status=profile_card.battery_sizing_posture.value,
                confidence_level=battery_sizing.inspectability.confidence_level,
                rule_keys=["recommendation.profile_battery_sizing_v1"],
            ),
            ReasoningGraphNode(
                node_id="solar_posture",
                label="Solar Posture",
                category="solar_posture",
                summary=solar_summary,
                status=profile_card.solar_sizing_posture.value,
                confidence_level=solar_sizing.inspectability.confidence_level,
                rule_keys=[
                    "recommendation.profile_solar_sizing_v1",
                    "recommendation.profile_solar_site_adjustment_v1",
                ],
            ),
        ]

        dependencies = [
            self._reasoning_graph_dependency(
                "loads",
                "backup_scope",
                "grounds outage posture",
                "Recorded essential/preferred load grouping determines whether the outage posture resolves to critical-load, partial-home, or whole-home candidate planning.",
                backup_load_selection.confidence_level,
                ["recommendation.backup_load_selection_v1", "recommendation.system_reasoning_graph_v1"],
            ),
            self._reasoning_graph_dependency(
                "current_topology",
                "inverter_system",
                "grounds current-state pathway",
                "Current solar and inverter topology determines whether future battery and backup planning starts from a microinverter, string, hybrid, AC-coupled, or unresolved existing-home posture.",
                current_home_energy_architecture.topology_confidence,
                [
                    "recommendation.current_home_energy_architecture_v1",
                    "recommendation.inverter_system_architecture_v1",
                    "recommendation.system_reasoning_graph_v1",
                ],
            ),
            self._reasoning_graph_dependency(
                "backup_scope",
                "panel_service",
                "bounds backup architecture",
                "Panel and service posture remains bounded by the selected outage posture instead of assuming broader backup architecture than the recorded load scope supports.",
                panel_service_architecture.inspectability.confidence_level,
                [
                    "recommendation.backup_load_selection_v1",
                    "recommendation.panel_service_preliminary_architecture_v1",
                    "recommendation.backup_architecture_consistency_v1",
                    "recommendation.system_reasoning_graph_v1",
                ],
            ),
            self._reasoning_graph_dependency(
                "backup_scope",
                "inverter_system",
                "constrains system direction",
                "Inverter/system direction inherits the current backup architecture direction and outage posture instead of inventing a broader whole-home pathway.",
                inverter_system_architecture.inspectability.confidence_level,
                [
                    "recommendation.backup_load_selection_v1",
                    "recommendation.panel_service_preliminary_architecture_v1",
                    "recommendation.inverter_system_architecture_v1",
                    "recommendation.system_reasoning_graph_v1",
                ],
            ),
            self._reasoning_graph_dependency(
                "current_topology",
                "battery_posture",
                "qualifies retrofit posture",
                "Current solar topology changes how grounded an AC-coupled retrofit versus hybrid-centered storage path appears, even though battery sizing still uses the selected outage scope.",
                battery_sizing.inspectability.confidence_level,
                [
                    "recommendation.current_home_energy_architecture_v1",
                    "recommendation.profile_battery_sizing_v1",
                    "recommendation.system_reasoning_graph_v1",
                ],
            ),
            self._reasoning_graph_dependency(
                "panel_service",
                "inverter_system",
                "anchors pathway realism",
                "Panel/service direction and consistency posture shape which inverter pathway remains coherent at planning time.",
                inverter_system_architecture.inspectability.confidence_level,
                [
                    "recommendation.panel_service_preliminary_architecture_v1",
                    "recommendation.backup_architecture_consistency_v1",
                    "recommendation.inverter_system_architecture_v1",
                    "recommendation.system_reasoning_graph_v1",
                ],
            ),
            self._reasoning_graph_dependency(
                "backup_scope",
                "battery_posture",
                "drives storage sizing basis",
                "Battery planning range is derived from the selected backup-load scope and does not widen beyond that recorded outage posture.",
                battery_sizing.inspectability.confidence_level,
                [
                    "recommendation.backup_load_selection_v1",
                    "recommendation.profile_battery_sizing_v1",
                    "recommendation.system_reasoning_graph_v1",
                ],
            ),
            self._reasoning_graph_dependency(
                "inverter_system",
                "battery_posture",
                "qualifies coexistence posture",
                "Battery posture keeps the same sizing method, but the current inverter/system path explains how grounded storage coexistence appears.",
                battery_sizing.inspectability.confidence_level,
                [
                    "recommendation.inverter_system_architecture_v1",
                    "recommendation.profile_battery_sizing_v1",
                    "recommendation.system_reasoning_graph_v1",
                ],
            ),
            self._reasoning_graph_dependency(
                "battery_posture",
                "solar_posture",
                "sets recovery burden",
                "Solar recovery guidance is derived from the current battery planning range and recovery posture rather than being sized independently.",
                solar_sizing.inspectability.confidence_level,
                [
                    "recommendation.profile_battery_sizing_v1",
                    "recommendation.profile_solar_sizing_v1",
                    "recommendation.system_reasoning_graph_v1",
                ],
            ),
            self._reasoning_graph_dependency(
                "backup_scope",
                "solar_posture",
                "preserves outage-scope discipline",
                "Solar planning inherits the same explicit backup scope used by battery planning so broader resilience claims are not silently implied.",
                solar_sizing.inspectability.confidence_level,
                [
                    "recommendation.backup_load_selection_v1",
                    "recommendation.profile_solar_sizing_v1",
                    "recommendation.profile_solar_site_adjustment_v1",
                    "recommendation.system_reasoning_graph_v1",
                ],
            ),
        ]

        return StructuredSystemReasoningGraph(
            scope_label=f"Recommended profile: {profile_card.label}",
            summary="Inspectable planning-only dependency graph connecting recorded load grouping, outage posture, architecture direction, and recommended battery/solar posture.",
            nodes=nodes,
            dependencies=dependencies,
            scope_note="Planning graph only. It traces deterministic recommendation dependencies for the currently recommended profile and does not represent final electrical design, compliance review, or engineering approval.",
            inspectability=provenance_service.build_estimate_inspectability(
                db,
                basis="This reasoning graph is assembled from the existing deterministic backup-scope, panel/service, inverter/system, battery, and solar outputs for the currently recommended profile.",
                confidence_level=profile_inspectability.confidence_level,
                rule_keys=graph_rule_keys,
                input_signals=[
                    {
                        "key": "recommended_profile",
                        "label": "Recommended profile",
                        "value": profile_card.profile.value.replace("_", " "),
                        "status": "rule_based",
                        "note": "The graph is anchored to the currently recommended profile so battery and solar posture remain concrete rather than generalized across every profile.",
                    },
                    {
                        "key": "backup_scope_posture",
                        "label": "Backup scope posture",
                        "value": backup_load_selection.outage_posture,
                        "status": "rule_based",
                        "note": "This is the root planning posture that downstream architecture and sizing layers consume.",
                    },
                    {
                        "key": "current_topology",
                        "label": "Current home energy topology",
                        "value": current_home_energy_architecture.inverter_topology,
                        "status": "rule_based",
                        "note": "Current-state topology is shown separately so the graph can distinguish existing-home conditions from future recommendations.",
                    },
                    {
                        "key": "panel_service_direction",
                        "label": "Panel/service direction",
                        "value": panel_service_architecture.recommended_backup_architecture,
                        "status": "rule_based",
                        "note": "Panel/service direction is shown as a dependent planning layer, not a final service design.",
                    },
                    {
                        "key": "system_direction",
                        "label": "Inverter/system direction",
                        "value": inverter_system_architecture.recommended_system_architecture,
                        "status": "rule_based",
                        "note": "Inverter/system direction remains planning-only and inherits prior architecture constraints.",
                    },
                ],
                estimated_inputs=[
                    "The reasoning graph is interpretive and assembled from deterministic advisor outputs; it does not introduce new sizing formulas."
                ],
                incomplete_inputs=[
                    "The graph only traces the currently recommended profile, so alternative profile dependency graphs are not expanded yet."
                ],
                notes=[
                    "Dependency summaries are additive traceability aids and should not be treated as standalone engineering determinations."
                ],
                rule_documents_map=rule_documents_map,
            ),
        )

    def recommend(self, db, design_id: str) -> ResilienceRecommendation:
        analysis = design_analysis_service.build(db, design_id)
        completeness = design_completeness_service.evaluate(db, design_id)
        if analysis is None:
            rule_documents_map = provenance_service.get_rule_documents_map(
                db, ["recommendation.resilience_profile_matrix_v1"]
            )
            provenance = provenance_service.build_recommendation_provenance(
                db,
                rule_keys=["recommendation.resilience_profile_matrix_v1"],
                notes=["No design was available, so no recommendation profile could be selected."],
                rule_documents_map=rule_documents_map,
            )
            return ResilienceRecommendation(
                design_id=design_id,
                recommended_profile=None,
                confidence_level=ConfidenceLevel.low,
                panel_service_architecture=None,
                inverter_system_architecture=None,
                profiles=[],
                context_signals={"design_present": False},
                scope_note="Recommendation profiles are planning-oriented guidance only. They do not replace engineering sizing or site validation.",
                basis="No design found for resilience recommendation.",
                data_origin=FactLifecycleState.derived_estimate,
                provenance_summary=provenance,
            )

        profile = self._recommended_profile(analysis, completeness)
        confidence = self._confidence_level(analysis, completeness)
        recommendation_rule_documents = provenance_service.get_rule_documents_map(
            db,
            [
                "recommendation.resilience_profile_matrix_v1",
                "recommendation.backup_load_selection_v1",
                "recommendation.current_home_energy_architecture_v1",
                "recommendation.panel_service_preliminary_architecture_v1",
                "recommendation.backup_architecture_consistency_v1",
                "recommendation.inverter_system_architecture_v1",
                "recommendation.profile_architecture_fit_v1",
                "recommendation.profile_battery_sizing_v1",
                "recommendation.profile_solar_sizing_v1",
                "recommendation.profile_solar_site_adjustment_v1",
                "recommendation.roof_geometry_readiness_v1",
                "recommendation.system_reasoning_graph_v1",
            ],
        )
        backup_load_selection = self._backup_load_selection_summary(
            db, analysis, profile, confidence, recommendation_rule_documents
        )
        current_home_energy_architecture = self._current_home_energy_architecture_estimate(
            db, analysis, backup_load_selection, confidence, recommendation_rule_documents
        )
        panel_service_architecture = self._panel_service_architecture_estimate(
            db, analysis, completeness, profile, confidence, recommendation_rule_documents
        )
        inverter_system_architecture = self._inverter_system_architecture_estimate(
            db,
            analysis,
            profile,
            confidence,
            current_home_energy_architecture,
            panel_service_architecture,
            recommendation_rule_documents,
        )
        profiles: List[RecommendationProfileCard] = []
        for key, config in PROFILE_LIBRARY.items():
            profile_signals, profile_estimated_inputs, profile_incomplete_inputs = self._build_profile_input_signals(
                analysis, completeness, key, current_home_energy_architecture
            )
            architecture_fit = self._profile_architecture_fit(
                analysis,
                key,
                current_home_energy_architecture,
                panel_service_architecture,
                inverter_system_architecture,
            )
            profile_signals.extend(
                [
                    {
                        "key": "equipment_mix_posture",
                        "label": "Equipment mix posture",
                        "value": architecture_fit.equipment_mix_summary,
                        "status": "rule_based" if analysis["assigned_products"] else "missing",
                        "note": "Summarizes how the currently recorded product mix shapes profile fit without introducing inverter or generator sizing logic.",
                    },
                    {
                        "key": "backup_path_fit",
                        "label": "Backup path fit",
                        "value": architecture_fit.status,
                        "status": "rule_based",
                        "note": "Profile fit now reflects outage posture, panel/service direction, and architecture-consistency posture together.",
                    },
                    {
                        "key": "inverter_system_posture",
                        "label": "Inverter/system architecture posture",
                        "value": inverter_system_architecture.recommended_system_architecture,
                        "status": "rule_based",
                        "note": "Profile fit also reflects the current planning-only inverter/system direction without changing sizing formulas.",
                    },
                ]
            )
            if architecture_fit.warnings:
                profile_incomplete_inputs.extend(architecture_fit.warnings)
            battery_sizing = self._battery_sizing_estimate(analysis, key, config)
            battery_inspectability = self._battery_inspectability(
                db, analysis, key, config, battery_sizing, confidence, recommendation_rule_documents
            )
            solar_sizing = self._solar_sizing_estimate(analysis, config, battery_sizing)
            solar_inspectability = self._solar_inspectability(
                db, analysis, key, config, battery_sizing, solar_sizing, confidence, recommendation_rule_documents
            )
            profiles.append(
                RecommendationProfileCard(
                    profile=key,
                    recommended=key == profile,
                    fit_reason=self._fit_reason(key, analysis, architecture_fit),
                    architecture_fit=architecture_fit,
                    battery_sizing_estimate=battery_sizing.copy(
                        update={"inspectability": battery_inspectability}
                    ),
                    solar_sizing_estimate=solar_sizing.copy(update={"inspectability": solar_inspectability}),
                    inspectability=provenance_service.build_estimate_inspectability(
                        db,
                        basis="Profile fit is based on current design goal, load grouping, recorded architecture type, equipment mix, panel/service direction, pathway planning, and overall planning completeness.",
                        confidence_level=confidence,
                        rule_keys=[
                            "recommendation.resilience_profile_matrix_v1",
                            "recommendation.backup_load_selection_v1",
                            "recommendation.current_home_energy_architecture_v1",
                            "recommendation.panel_service_preliminary_architecture_v1",
                            "recommendation.backup_architecture_consistency_v1",
                            "recommendation.inverter_system_architecture_v1",
                            "recommendation.profile_architecture_fit_v1",
                        ],
                        input_signals=profile_signals,
                        estimated_inputs=profile_estimated_inputs,
                        incomplete_inputs=profile_incomplete_inputs,
                        notes=[
                            "Profile fit remains planning guidance only and should not be treated as engineering approval or final ownership advice."
                        ],
                        rule_documents_map=recommendation_rule_documents,
                    ),
                    **config,
                )
            )

        context_signals: Dict[str, object] = {
            "design_goal": analysis["design"].design_goal,
            "essential_load_count": len(analysis["essential_loads"]),
            "backup_load_count": len(analysis["backup_loads"]),
            "selected_backup_load_count": backup_load_selection.selected_load_count,
            "selected_backup_scope_label": backup_load_selection.selected_scope_label,
            "backup_scope_outage_posture": backup_load_selection.outage_posture,
            "backup_scope_confidence_level": backup_load_selection.confidence_level,
            "current_inverter_topology": current_home_energy_architecture.inverter_topology,
            "current_solar_existing_state": current_home_energy_architecture.solar_existing_state,
            "recommended_system_architecture": inverter_system_architecture.recommended_system_architecture,
            "assigned_product_count": len(analysis["assigned_products"]),
            "pathway_count": len(analysis["linked_pathways"]),
            "workshop_building_count": len(analysis["workshop_buildings"]),
            "main_panel_known": analysis["main_panel"] is not None,
            "completeness_score": completeness["completeness_score"],
        }
        recommended_profile_card = next((item for item in profiles if item.recommended), None)
        reasoning_graph = (
            self._structured_system_reasoning_graph(
                db,
                recommended_profile_card,
                backup_load_selection,
                current_home_energy_architecture,
                panel_service_architecture,
                inverter_system_architecture,
                recommendation_rule_documents,
            )
            if recommended_profile_card is not None
            else None
        )
        provenance = provenance_service.build_recommendation_provenance(
            db,
            rule_keys=[
                "recommendation.resilience_profile_matrix_v1",
                "recommendation.backup_load_selection_v1",
                "recommendation.current_home_energy_architecture_v1",
                "recommendation.backup_architecture_consistency_v1",
                "recommendation.inverter_system_architecture_v1",
                "recommendation.profile_architecture_fit_v1",
                "recommendation.system_reasoning_graph_v1",
            ],
            notes=[
                "Recommendation is derived from current design goal, load grouping, product assignments, panel context, and pathway planning.",
                "Backup-scope selection is explicit: broader outage intent is only carried when preferred or broader recorded load grouping exists.",
                "Current home energy architecture keeps existing solar/inverter topology separate from proposed future architecture so microinverter, string, hybrid, and unknown states remain inspectable.",
                "Backup-architecture consistency checks keep panel/service direction bounded by recorded outage posture instead of silently escalating to broader backup assumptions.",
                "Inverter/system architecture reasoning stays planning-only and uses recorded architecture type, inverter/control equipment, and coexistence signals instead of claiming final topology certainty.",
                "Profile-fit explanations now also describe how the current equipment mix and backup-path direction pull each planning posture narrower or broader.",
                "Battery sizing ranges are planning estimates derived from profile posture and current backup-load modeling, not engineering sizing outputs.",
                "Solar sizing ranges are planning estimates derived from recovery posture, low-solar assumptions, and coarse site-aware caution signals, not engineering production studies.",
                "The structured reasoning graph makes those deterministic dependencies inspectable without changing the underlying selection or sizing rules.",
            ],
            rule_documents_map=recommendation_rule_documents,
        )

        return ResilienceRecommendation(
            design_id=design_id,
                recommended_profile=profile,
                confidence_level=confidence,
                backup_load_selection=backup_load_selection,
                current_home_energy_architecture=current_home_energy_architecture,
                panel_service_architecture=panel_service_architecture,
                inverter_system_architecture=inverter_system_architecture,
                reasoning_graph=reasoning_graph,
                profiles=profiles,
            context_signals=context_signals,
            scope_note="Recommendation profiles express planning philosophies, tradeoffs, and resilience posture. They do not expose engineering formulas or imply permit-grade sizing certainty.",
            basis="Deterministic recommendation model based on design goal, backup load grouping, assigned architecture, panel headroom, and pathway context.",
            data_origin=FactLifecycleState.derived_estimate,
            provenance_summary=provenance,
        )


resilience_recommendation_service = ResilienceRecommendationService()

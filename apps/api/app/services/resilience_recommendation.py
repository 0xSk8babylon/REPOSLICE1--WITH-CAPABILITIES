from typing import Dict, List, Optional, Tuple

from app.core.types import (
    AutonomyReservePosture,
    BatterySizingPosture,
    ConfidenceLevel,
    DataOrigin,
    FutureGrowthMarginPosture,
    LowSolarAssumptionPosture,
    RecoveryStrengthPosture,
    ReserveMarginPosture,
    RecommendationProfile,
    SeasonalConservatismPosture,
    SolarSizingPosture,
)
from app.design_advisor.schemas import (
    BackupLoadSelectionSummary,
    BatteryCapacityRange,
    BatterySizingEstimate,
    PanelServiceArchitectureEstimate,
    RecommendationProfileCard,
    ResilienceRecommendation,
    RoofGeometryReadiness,
    SolarCapacityRange,
    SolarSizingEstimate,
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
    AUTONOMY_HOUR_RANGES = {
        AutonomyReservePosture.minimal: (4.0, 8.0),
        AutonomyReservePosture.standard: (8.0, 14.0),
        AutonomyReservePosture.elevated: (14.0, 24.0),
        AutonomyReservePosture.extended: (24.0, 36.0),
    }

    RESERVE_MARGIN_FACTORS = {
        ReserveMarginPosture.lean: (1.05, 1.12),
        ReserveMarginPosture.standard: (1.12, 1.22),
        ReserveMarginPosture.elevated: (1.22, 1.35),
        ReserveMarginPosture.robust: (1.35, 1.5),
    }

    GROWTH_MARGIN_FACTORS = {
        FutureGrowthMarginPosture.tight: (1.0, 1.08),
        FutureGrowthMarginPosture.planned: (1.08, 1.18),
        FutureGrowthMarginPosture.expansion_oriented: (1.18, 1.3),
        FutureGrowthMarginPosture.future_ready: (1.3, 1.45),
    }

    SOLAR_PRODUCTION_FACTORS = {
        SolarSizingPosture.load_matched: (0.52, 0.72),
        SolarSizingPosture.resilience_balanced: (0.68, 0.9),
        SolarSizingPosture.recovery_weighted: (0.88, 1.12),
        SolarSizingPosture.future_weighted: (1.05, 1.32),
    }

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

    def _round_range(self, value: float) -> float:
        return round(value, 1)

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

        return {
            "selected_loads": selected_loads,
            "selection_basis": selection_basis,
            "selected_priority_band": selected_priority_band,
            "selected_scope_label": selected_scope_label,
            "selection_reason": selection_reason,
            "planning_gap_warning": planning_gap_warning,
            "recorded_essential_load_count": len(essential_loads),
            "recorded_preferred_load_count": len(preferred_loads),
            "selected_load_count": len(selected_loads),
            "supports_broader_backup": selection_basis in {"essential_and_preferred", "preferred_only"},
        }

    def _selected_backup_loads(self, analysis, profile: Optional[RecommendationProfile] = None):
        return self._backup_scope_selection(analysis, profile)["selected_loads"]

    def _backup_load_energy_need_kwh(
        self, analysis, profile: Optional[RecommendationProfile] = None
    ) -> Optional[float]:
        selected_loads = self._selected_backup_loads(analysis, profile)
        if not selected_loads:
            return None
        fallback_hours = 4.0
        total_kwh = 0.0
        for load in selected_loads:
            daily_hours = load.estimated_daily_hours if load.estimated_daily_hours is not None else fallback_hours
            total_kwh += (load.running_watts * daily_hours) / 1000
        return round(total_kwh, 2)

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
            "recorded_essential_load_count": selection["recorded_essential_load_count"],
            "recorded_preferred_load_count": selection["recorded_preferred_load_count"],
            "supports_broader_backup": selection["supports_broader_backup"],
            "missing_daily_hour_loads": missing_daily_hours,
            "fallback_applied": fallback_applied,
        }

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
                "key": "selected_backup_scope",
                "label": "Selected backup scope",
                "value": f"{load_summary['selected_load_count']} loads from {load_summary['selected_scope_label']}",
                "status": "rule_based" if load_summary["selected_load_count"] else "missing",
                "note": "Battery, solar, and backup-architecture planning consume this selected scope instead of inferring broader outage intent.",
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
            selection_reason=load_summary["selection_reason"],
            planning_gap_warning=load_summary["planning_gap_warning"],
            scope_note="Planning-only selection summary. It explains which recorded loads currently ground backup architecture and sizing, not final transfer, inverter, or generator design.",
            inspectability=provenance_service.build_estimate_inspectability(
                db,
                basis="Backup scope selection is derived from recorded essential/preferred load grouping plus explicit profile-aware selection rules.",
                confidence_level=confidence,
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
        supports_broader_backup = load_summary["supports_broader_backup"]

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

        if not supports_broader_backup:
            if partial_home_backup_suitability == "conditional":
                partial_home_backup_suitability = "limited"
            elif partial_home_backup_suitability == "favorable":
                partial_home_backup_suitability = "conditional"
            whole_home_backup_suitability = "poor"

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
        elif supports_broader_backup and "smart_panel" in product_types and profile in {
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
                if supports_broader_backup and partial_home_backup_suitability in {"favorable", "conditional"}
                else "critical-loads subpanel"
            )
        elif profile == RecommendationProfile.conservative:
            if (
                supports_broader_backup
                and whole_home_backup_suitability == "conditional"
                and design_goal in {"whole_home_backup", "off_grid_capable"}
            ):
                recommended_backup_architecture = "whole-home backup"
            elif supports_broader_backup:
                recommended_backup_architecture = "partial-home backup"
            else:
                recommended_backup_architecture = "critical-loads subpanel"
        else:
            if (
                supports_broader_backup
                and whole_home_backup_suitability in {"favorable", "conditional"}
                and home is not None
                and (home.service_size or 0) >= 200
            ):
                recommended_backup_architecture = "whole-home backup"
            elif supports_broader_backup and "smart_panel" in product_types:
                recommended_backup_architecture = "smart-panel/load-control assisted"
            else:
                recommended_backup_architecture = "future-ready service upgrade path"

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
            inspectability=inspectability,
        )

    def _build_profile_input_signals(
        self, analysis, completeness, profile: RecommendationProfile
    ) -> Tuple[List[Dict[str, object]], List[str], List[str]]:
        load_summary = self._backup_load_model_summary(analysis, profile)
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

    def _battery_sizing_estimate(
        self, analysis, profile: RecommendationProfile, config
    ) -> BatterySizingEstimate:
        backup_load_energy_need_kwh = self._backup_load_energy_need_kwh(analysis, profile)
        autonomy_min, autonomy_max = self.AUTONOMY_HOUR_RANGES[config["autonomy_reserve_posture"]]
        usable_range = None
        recommended_range = None
        scope_note = "Planning estimate only. This range is derived from current backup-load modeling and recommendation posture, not final engineered battery design."

        if backup_load_energy_need_kwh is not None:
            reserve_min, reserve_max = self.RESERVE_MARGIN_FACTORS[config["reserve_margin_posture"]]
            growth_min, growth_max = self.GROWTH_MARGIN_FACTORS[config["future_growth_margin_posture"]]

            # Internal planning estimate: convert daily energy need into autonomy-window energy,
            # then layer reserve and future-growth posture without exposing the coefficients in UI.
            autonomy_energy_min = backup_load_energy_need_kwh * (autonomy_min / 24.0)
            autonomy_energy_max = backup_load_energy_need_kwh * (autonomy_max / 24.0)
            usable_min = autonomy_energy_min * reserve_min
            usable_max = autonomy_energy_max * reserve_max
            recommended_min = usable_min * growth_min
            recommended_max = usable_max * growth_max
            usable_range = BatteryCapacityRange(
                min_kwh=self._round_range(usable_min),
                max_kwh=self._round_range(usable_max),
            )
            recommended_range = BatteryCapacityRange(
                min_kwh=self._round_range(recommended_min),
                max_kwh=self._round_range(recommended_max),
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
        solar_min_factor, solar_max_factor = self.SOLAR_PRODUCTION_FACTORS[solar_posture]

        site_capacity = self._site_capacity_adjustment(analysis)
        roof_geometry_readiness = self._roof_geometry_readiness(analysis)
        shading = self._shading_adjustment(analysis)
        seasonal_region = self._seasonal_region_adjustment(analysis)
        install_realism = self._install_realism_adjustment(analysis)
        base_recommended_range = None
        recommended_range = None
        scope_note = "Planning estimate only. This range starts from profile-based recovery posture and current backup-load modeling, then applies coarse site-aware caution signals. It is not a final engineered production study."

        if (
            battery_sizing.backup_load_energy_need_kwh is not None
            and battery_sizing.recommended_battery_capacity_range_kwh is not None
        ):
            backup_energy = battery_sizing.backup_load_energy_need_kwh
            battery_min = battery_sizing.recommended_battery_capacity_range_kwh.min_kwh
            battery_max = battery_sizing.recommended_battery_capacity_range_kwh.max_kwh

            # Internal planning estimate: use current backup-load energy and the battery recovery
            # burden implied by the chosen profile to derive a solar range without surfacing the
            # underlying production-credit assumptions.
            base_recovery_need_min = max(backup_energy, battery_min * 0.55)
            base_recovery_need_max = max(backup_energy * 1.1, battery_max * 0.75)
            base_recommended_min = base_recovery_need_min * solar_min_factor
            base_recommended_max = base_recovery_need_max * solar_max_factor

            site_factor_min, site_factor_max = site_capacity["factor_range"]
            shading_factor_min, shading_factor_max = shading["factor_range"]
            seasonal_factor_min, seasonal_factor_max = seasonal_region["factor_range"]
            install_factor_min, install_factor_max = install_realism["factor_range"]

            recommended_min = (
                base_recommended_min
                * site_factor_min
                * shading_factor_min
                * seasonal_factor_min
                * install_factor_min
            )
            recommended_max = (
                base_recommended_max
                * site_factor_max
                * shading_factor_max
                * seasonal_factor_max
                * install_factor_max
            )
            base_recommended_range = SolarCapacityRange(
                min_kw=self._round_range(base_recommended_min),
                max_kw=self._round_range(base_recommended_max),
            )
            recommended_range = SolarCapacityRange(
                min_kw=self._round_range(recommended_min),
                max_kw=self._round_range(recommended_max),
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

    def _fit_reason(self, profile: RecommendationProfile, analysis) -> str:
        design_goal = analysis["design"].design_goal.replace("_", " ")
        if profile == RecommendationProfile.critical_efficient:
            return "Current design signals favor essential resilience scope over broader redundancy."
        if profile == RecommendationProfile.balanced:
            return "Current design signals support a middle path: meaningful backup planning without overcommitting future scope too early."
        if profile == RecommendationProfile.conservative:
            return f"Current design goal '{design_goal}' carries stronger resilience expectations, so a more protective posture fits best."
        return "Current design emphasizes future growth or broader continuity, so preserving long-term headroom is the best fit."

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
                profiles=[],
                context_signals={"design_present": False},
                scope_note="Recommendation profiles are planning-oriented guidance only. They do not replace engineering sizing or site validation.",
                basis="No design found for resilience recommendation.",
                data_origin=DataOrigin.derived_estimate,
                provenance_summary=provenance,
            )

        profile = self._recommended_profile(analysis, completeness)
        confidence = self._confidence_level(analysis, completeness)
        recommendation_rule_documents = provenance_service.get_rule_documents_map(
            db,
            [
                "recommendation.resilience_profile_matrix_v1",
                "recommendation.backup_load_selection_v1",
                "recommendation.panel_service_preliminary_architecture_v1",
                "recommendation.profile_battery_sizing_v1",
                "recommendation.profile_solar_sizing_v1",
                "recommendation.profile_solar_site_adjustment_v1",
                "recommendation.roof_geometry_readiness_v1",
            ],
        )
        backup_load_selection = self._backup_load_selection_summary(
            db, analysis, profile, confidence, recommendation_rule_documents
        )
        panel_service_architecture = self._panel_service_architecture_estimate(
            db, analysis, completeness, profile, confidence, recommendation_rule_documents
        )
        profiles: List[RecommendationProfileCard] = []
        for key, config in PROFILE_LIBRARY.items():
            profile_signals, profile_estimated_inputs, profile_incomplete_inputs = self._build_profile_input_signals(
                analysis, completeness, key
            )
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
                    fit_reason=self._fit_reason(key, analysis),
                    battery_sizing_estimate=battery_sizing.copy(
                        update={"inspectability": battery_inspectability}
                    ),
                    solar_sizing_estimate=solar_sizing.copy(update={"inspectability": solar_inspectability}),
                    inspectability=provenance_service.build_estimate_inspectability(
                        db,
                        basis="Profile fit is based on current design goal, load grouping, assigned architecture, panel context, pathway planning, and overall planning completeness.",
                        confidence_level=confidence,
                        rule_keys=["recommendation.resilience_profile_matrix_v1"],
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
            "assigned_product_count": len(analysis["assigned_products"]),
            "pathway_count": len(analysis["linked_pathways"]),
            "workshop_building_count": len(analysis["workshop_buildings"]),
            "main_panel_known": analysis["main_panel"] is not None,
            "completeness_score": completeness["completeness_score"],
        }
        provenance = provenance_service.build_recommendation_provenance(
            db,
            rule_keys=[
                "recommendation.resilience_profile_matrix_v1",
                "recommendation.backup_load_selection_v1",
            ],
            notes=[
                "Recommendation is derived from current design goal, load grouping, product assignments, panel context, and pathway planning.",
                "Backup-scope selection is explicit: broader outage intent is only carried when preferred or broader recorded load grouping exists.",
                "Battery sizing ranges are planning estimates derived from profile posture and current backup-load modeling, not engineering sizing outputs.",
                "Solar sizing ranges are planning estimates derived from recovery posture, low-solar assumptions, and coarse site-aware caution signals, not engineering production studies.",
            ],
            rule_documents_map=recommendation_rule_documents,
        )

        return ResilienceRecommendation(
            design_id=design_id,
            recommended_profile=profile,
            confidence_level=confidence,
            backup_load_selection=backup_load_selection,
            panel_service_architecture=panel_service_architecture,
            profiles=profiles,
            context_signals=context_signals,
            scope_note="Recommendation profiles express planning philosophies, tradeoffs, and resilience posture. They do not expose engineering formulas or imply permit-grade sizing certainty.",
            basis="Deterministic recommendation model based on design goal, backup load grouping, assigned architecture, panel headroom, and pathway context.",
            data_origin=DataOrigin.derived_estimate,
            provenance_summary=provenance,
        )


resilience_recommendation_service = ResilienceRecommendationService()

from typing import List

from app.compatibility_rules.schemas import CompatibilityExplanation
from app.core.repository import repository
from app.core.types import DataOrigin
from app.services.design_analysis import design_analysis_service
from app.services.provenance import provenance_service


def _matches_building_tokens(pathway, building):
    tokens = [
        building.name.lower(),
        building.type.replace("_", " ").lower(),
        building.type.lower(),
    ]
    source = (pathway.source_location or "").lower()
    destination = (pathway.destination_location or "").lower()
    return any(token and (token in source or token in destination) for token in tokens)


class CompatibilityService:
    def evaluate_design(self, db, design_id: str) -> List[CompatibilityExplanation]:
        analysis = design_analysis_service.build(db, design_id)
        issues = repository.list_compatibility_issues(db, design_id=design_id)
        explanations = [
            CompatibilityExplanation(
                issue=issue.issue,
                why_it_matters=issue.why_it_matters,
                possible_solutions=issue.possible_solutions,
                tradeoff=issue.tradeoff,
                severity=issue.severity,
                category=issue.category,
                related_equipment_ids=issue.related_equipment_ids,
                data_origin=issue.data_origin,
                provenance_summary=provenance_service.build_advisor_issue_provenance(
                    db, issue, related_rule_key="advisor.seeded_compatibility_issue"
                ),
            )
            for issue in issues
        ]
        if analysis is None:
            return explanations

        design = analysis["design"]
        product_types = analysis["product_types"]
        ecosystems = analysis["ecosystems"]
        linked_pathways = analysis["linked_pathways"]
        main_panel = analysis["main_panel"]
        detached_buildings = analysis["detached_buildings"]

        battery_assignments = [item for item in analysis["assigned_products"] if item["product"] and item["product"].product_type == "battery"]
        inverter_present = bool(product_types.intersection({"microinverter", "string_inverter", "hybrid_inverter"}))
        gateway_transfer_present = bool(product_types.intersection({"gateway", "transfer_switch", "disconnect"}))
        generator_present = "generator" in product_types

        if design.design_goal == "whole_home_backup" and not bool(product_types.intersection({"battery", "generator", "hybrid_inverter", "gateway", "transfer_switch"})):
            explanations.append(
                CompatibilityExplanation(
                    issue="Whole-home backup goal is selected without clear backup architecture.",
                    why_it_matters="Whole-home backup usually requires explicit storage, generator, inverter, and transfer strategy choices before resilience claims become credible.",
                    possible_solutions=[
                        "Add battery, generator, or hybrid backup equipment.",
                        "Downgrade the goal to partial backup until the architecture is more explicit.",
                        "Add transfer or gateway strategy records to clarify backup boundaries.",
                    ],
                    tradeoff="Keeping the broader goal without architecture detail can create false confidence in resilience scope.",
                    severity="warning",
                    category="backup",
                    data_origin=DataOrigin.derived_estimate,
                    provenance_summary=provenance_service.build_advisor_issue_provenance(
                        db, type("Issue", (), {"data_origin": DataOrigin.derived_estimate})(), "advisor.whole_home_backup_architecture"
                    ),
                )
            )

        if detached_buildings and not any(
            _matches_building_tokens(pathway, building)
            for building in detached_buildings
            for pathway in linked_pathways
        ):
            explanations.append(
                CompatibilityExplanation(
                    issue="Detached structures exist without design-linked pathway planning.",
                    why_it_matters="Detached buildings often drive trenching, conduit visibility, and labor complexity. Without pathways, scope assumptions remain weak.",
                    possible_solutions=[
                        "Add estimated pathways for detached structures.",
                        "Defer detached-building integration into a later phase.",
                        "Model a separate backed-up zone for the detached structure.",
                    ],
                    tradeoff="Early pathway planning takes more time now but reduces surprise labor and routing changes later.",
                    severity="warning",
                    category="install_complexity",
                    data_origin=DataOrigin.derived_estimate,
                    provenance_summary=provenance_service.build_advisor_issue_provenance(
                        db, type("Issue", (), {"data_origin": DataOrigin.derived_estimate})(), "advisor.detached_structure_pathway"
                    ),
                )
            )

        if battery_assignments and not inverter_present:
            explanations.append(
                CompatibilityExplanation(
                    issue="Battery equipment is assigned without an inverter or hybrid inverter strategy.",
                    why_it_matters="Storage planning depends on how the battery integrates with the rest of the system. Without conversion/control equipment, capability claims are incomplete.",
                    possible_solutions=[
                        "Add a hybrid inverter or compatible inverter strategy.",
                        "Clarify whether the battery ecosystem includes embedded inverter behavior.",
                        "Record gateway or control components that define the storage topology.",
                    ],
                    tradeoff="Adding more explicit conversion equipment may narrow ecosystem choices while increasing architectural clarity.",
                    severity="blocker",
                    category="product_fit",
                    related_equipment_ids=[assignment["equipment"].product_id for assignment in battery_assignments],
                    data_origin=DataOrigin.derived_estimate,
                    provenance_summary=provenance_service.build_advisor_issue_provenance(
                        db, type("Issue", (), {"data_origin": DataOrigin.derived_estimate})(), "advisor.battery_without_inverter"
                    ),
                )
            )

        if design.design_goal == "generator_assisted" and not gateway_transfer_present:
            explanations.append(
                CompatibilityExplanation(
                    issue="Generator-assisted goal is selected without transfer or gateway strategy.",
                    why_it_matters="Generator-assisted systems need explicit switching, gateway, or disconnect planning to define how backup power is introduced.",
                    possible_solutions=[
                        "Add a transfer switch, gateway, or disconnect component.",
                        "Clarify generator interconnection strategy in design notes.",
                        "Reduce the goal scope until integration equipment is represented.",
                    ],
                    tradeoff="Adding transfer strategy detail improves trust but can expose more unresolved site constraints.",
                    severity="warning",
                    category="backup",
                    data_origin=DataOrigin.derived_estimate,
                    provenance_summary=provenance_service.build_advisor_issue_provenance(
                        db, type("Issue", (), {"data_origin": DataOrigin.derived_estimate})(), "advisor.generator_transfer_strategy"
                    ),
                )
            )

        if design.design_goal == "expansion_ready" and not bool(main_panel and main_panel.breaker_spaces_available and main_panel.breaker_spaces_available > 1):
            explanations.append(
                CompatibilityExplanation(
                    issue="Expansion-ready goal is selected without spare panel capacity noted.",
                    why_it_matters="Expansion claims are weaker when panel capacity, breaker space, or distribution headroom has not been captured.",
                    possible_solutions=[
                        "Record breaker space availability on the main service panel.",
                        "Add a load center or smart panel strategy for future expansion.",
                        "Add an estimated pathway showing planned future infrastructure routing.",
                    ],
                    tradeoff="Documenting panel constraints can reduce optimism now but avoids expansion claims that fail later.",
                    severity="warning",
                    category="expansion",
                    data_origin=DataOrigin.derived_estimate,
                    provenance_summary=provenance_service.build_advisor_issue_provenance(
                        db, type("Issue", (), {"data_origin": DataOrigin.derived_estimate})(), "advisor.expansion_panel_capacity"
                    ),
                )
            )

        high_visibility_pathways = [
            pathway for pathway in linked_pathways if pathway.visibility_level == "high" or pathway.route_type == "surface_conduit"
        ]
        if high_visibility_pathways:
            explanations.append(
                CompatibilityExplanation(
                    issue="Chosen pathway assumptions likely create visible conduit or exposed infrastructure.",
                    why_it_matters="Visibility can affect homeowner acceptance, finish quality expectations, and routing choices long before final install planning.",
                    possible_solutions=[
                        "Explore alternate routes such as attic, crawlspace, or mixed routing.",
                        "Record finish expectations and aesthetic constraints in pathway notes.",
                        "Treat current visibility assumptions as planning-only until site verification.",
                    ],
                    tradeoff="Reducing visible conduit can increase labor difficulty or route length.",
                    severity="info",
                    category="install_complexity",
                    data_origin=DataOrigin.derived_estimate,
                    provenance_summary=provenance_service.build_advisor_issue_provenance(
                        db, type("Issue", (), {"data_origin": DataOrigin.derived_estimate})(), "advisor.visible_conduit_assumption"
                    ),
                )
            )

        trench_pathways = [
            pathway
            for pathway in linked_pathways
            if pathway.route_type == "trench_route" and (pathway.estimated_distance_ft or 0) >= 75
        ]
        if trench_pathways:
            explanations.append(
                CompatibilityExplanation(
                    issue="Long trench routing is likely to increase labor complexity.",
                    why_it_matters="Long trench routes usually add excavation coordination, restoration work, and schedule variability.",
                    possible_solutions=[
                        "Shorten the route if possible.",
                        "Phase detached-building integration separately.",
                        "Record trench assumptions explicitly so estimate language stays honest.",
                    ],
                    tradeoff="Keeping long trench assumptions may support the design goal but usually increases cost and uncertainty.",
                    severity="warning",
                    category="cost_driver",
                    data_origin=DataOrigin.derived_estimate,
                    provenance_summary=provenance_service.build_advisor_issue_provenance(
                        db, type("Issue", (), {"data_origin": DataOrigin.derived_estimate})(), "advisor.long_trench_complexity"
                    ),
                )
            )

        if battery_assignments and main_panel is not None:
            mismatched_battery_locations = []
            for assignment in battery_assignments:
                location = assignment["location"]
                if location and location.building_id != main_panel.building_id:
                    mismatched_battery_locations.append(assignment["equipment"].product_id)
            if mismatched_battery_locations:
                explanations.append(
                    CompatibilityExplanation(
                        issue="Battery placement appears far from the main service or primary distribution zone.",
                        why_it_matters="Distance between storage and the main distribution context can add routing complexity and make assumptions less reliable.",
                        possible_solutions=[
                            "Add or refine pathways between battery and service equipment.",
                            "Relocate battery assumptions closer to the service or inverter zone.",
                            "Treat the current siting as exploratory until site verification.",
                        ],
                        tradeoff="Moving battery siting may reduce routing complexity while introducing new placement constraints.",
                        severity="info",
                        category="install_complexity",
                        related_equipment_ids=mismatched_battery_locations,
                        data_origin=DataOrigin.derived_estimate,
                        provenance_summary=provenance_service.build_advisor_issue_provenance(
                            db, type("Issue", (), {"data_origin": DataOrigin.derived_estimate})(), "advisor.battery_distance_from_service"
                        ),
                    )
                )

        if len(ecosystems) > 1:
            explanations.append(
                CompatibilityExplanation(
                    issue="Multiple product ecosystems are mixed within one design.",
                    why_it_matters="Cross-ecosystem planning can complicate controls, monitoring expectations, and future compatibility assumptions.",
                    possible_solutions=[
                        "Consolidate around one ecosystem where practical.",
                        "Record why mixed ecosystems are intentional.",
                        "Flag integration boundaries explicitly in design notes.",
                    ],
                    tradeoff="A mixed ecosystem may broaden equipment options but often raises coordination and support complexity.",
                    severity="warning",
                    category="product_fit",
                    data_origin=DataOrigin.derived_estimate,
                    provenance_summary=provenance_service.build_advisor_issue_provenance(
                        db, type("Issue", (), {"data_origin": DataOrigin.derived_estimate})(), "advisor.mixed_ecosystems"
                    ),
                )
            )

        return explanations


compatibility_service = CompatibilityService()

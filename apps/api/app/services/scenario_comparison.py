from typing import Dict, List

from app.core.types import FactLifecycleState
from app.scenarios.schemas import Scenario
from app.services.design_analysis import design_analysis_service
from app.services.design_completeness import design_completeness_service
from app.services.provenance import provenance_service


def _round_score(value):
    if value is None:
        return None
    return round(value, 2)


def _rank_scenarios(scenarios: List[Dict[str, object]], metric: str, reverse: bool) -> List[Dict[str, object]]:
    ranked = [scenario for scenario in scenarios if scenario.get(metric) is not None]
    ranked.sort(key=lambda item: item[metric], reverse=reverse)
    return [
        {
            "scenario_id": scenario["id"],
            "scenario_name": scenario["name"],
            "value": scenario[metric],
        }
        for scenario in ranked
    ]


class ScenarioComparisonService:
    def _build_lineage_summary(self, db, scenario, analysis) -> Dict[str, object]:
        source_types = set()
        trust_states = {scenario.data_origin}
        verification_statuses = set()
        source_document_ids = set()
        unverified_fields = set()
        notes = []

        scenario_summary = provenance_service.summarize_entity(db, "scenario", scenario.id)
        source_types.update(scenario_summary.source_types)
        trust_states.update(scenario_summary.trust_states)
        verification_statuses.update(scenario_summary.verification_statuses)
        source_document_ids.update(scenario_summary.source_document_ids)
        unverified_fields.update(scenario_summary.unverified_fields)
        notes.extend(scenario_summary.notes[:2])

        if any(
            metric is not None
            for metric in [
                scenario.upfront_cost_placeholder,
                scenario.future_expansion_score,
                scenario.install_complexity_score,
                scenario.backup_capability_score,
            ]
        ):
            trust_states.add(FactLifecycleState.placeholder.value)
            unverified_fields.update(
                {
                    field
                    for field, value in {
                        "upfront_cost_placeholder": scenario.upfront_cost_placeholder,
                        "future_expansion_score": scenario.future_expansion_score,
                        "install_complexity_score": scenario.install_complexity_score,
                        "backup_capability_score": scenario.backup_capability_score,
                    }.items()
                    if value is not None
                }
            )

        for assignment in analysis["assigned_products"]:
            product = assignment["product"]
            if product is None:
                continue
            summary = provenance_service.summarize_entity(db, "equipment_product", product.id)
            source_types.update(summary.source_types)
            trust_states.update(summary.trust_states or [product.data_origin])
            verification_statuses.update(summary.verification_statuses)
            source_document_ids.update(summary.source_document_ids)
            unverified_fields.update(summary.unverified_fields)
            notes.extend(summary.notes[:1])

        for pathway in analysis["linked_pathways"]:
            summary = provenance_service.summarize_entity(db, "estimated_pathway", pathway.id)
            source_types.update(summary.source_types)
            trust_states.update(summary.trust_states or [pathway.data_origin])
            verification_statuses.update(summary.verification_statuses)
            source_document_ids.update(summary.source_document_ids)
            unverified_fields.update(summary.unverified_fields)
            if pathway.confidence_level == "low":
                notes.append(f"Linked pathway '{pathway.name}' is marked low confidence.")

        rule_records = provenance_service.get_rule_documents(
            db,
            [
                "completeness.design_readiness_v1",
                "advisor.detached_structure_pathway",
                "advisor.long_trench_complexity",
                "advisor.mixed_ecosystems",
            ],
        )
        if rule_records:
            source_types.add("internal_rule")
            trust_states.add(FactLifecycleState.derived_estimate.value)
            source_document_ids.update(
                record.source_document_id for record in rule_records if record.source_document_id
            )

        return {
            "authority_layer": "derived",
            "data_classification": "planning_private",
            "derivation_type": "deterministic_summary",
            "source_types": sorted(source_types),
            "trust_states": sorted(trust_states),
            "verification_statuses": sorted(verification_statuses),
            "source_document_ids": sorted(source_document_ids),
            "unverified_fields": sorted(unverified_fields),
            "rule_keys": sorted({record.rule_key for record in rule_records}),
            "limitations": [
                "Scenario comparison is planning intelligence over current records and compact revisions, not a replayable historical advisor payload.",
                "Placeholder scores and costs remain non-authoritative until stronger estimating provenance exists.",
            ],
            "notes": notes[:5],
        }

    def _build_scenario_result(self, db, scenario) -> Dict[str, object]:
        analysis = design_analysis_service.build(db, scenario.linked_design_id)
        completeness = design_completeness_service.evaluate(db, scenario.linked_design_id)
        if analysis is None:
            return {
                **Scenario.from_orm(scenario).dict(),
                "linked_design": None,
                "comparison_summary": {
                    "completeness_score": completeness["completeness_score"],
                    "pathway_count": 0,
                    "low_confidence_pathway_count": 0,
                    "ecosystem_mixing": False,
                    "missing_location_assignment_count": 0,
                    "status": "linked_design_missing",
                },
                "lineage_summary": self._build_lineage_summary(
                    db,
                    scenario,
                    {
                        "assigned_products": [],
                        "linked_pathways": [],
                    },
                ),
                "warnings": ["Linked design record is missing, so comparison depth is limited."],
            }

        pathway_count = len(analysis["linked_pathways"])
        low_confidence_pathway_count = len(
            [pathway for pathway in analysis["linked_pathways"] if pathway.confidence_level == "low"]
        )
        visible_pathway_count = len(
            [pathway for pathway in analysis["linked_pathways"] if pathway.visibility_level == "high"]
        )
        lineage_summary = self._build_lineage_summary(db, scenario, analysis)
        warnings = []
        if low_confidence_pathway_count:
            warnings.append("One or more linked pathways remain low confidence.")
        if analysis["missing_location_assignments"]:
            warnings.append("Some assigned design equipment still has no siting location.")
        if FactLifecycleState.placeholder.value in lineage_summary["trust_states"]:
            warnings.append("Scenario scoring and cost fields still include placeholders.")
        if not lineage_summary["source_document_ids"]:
            warnings.append("No source documents are linked directly to this scenario summary yet.")

        return {
            **Scenario.from_orm(scenario).dict(),
            "linked_design": {
                "id": analysis["design"].id,
                "name": analysis["design"].name,
                "design_goal": analysis["design"].design_goal,
                "architecture_type": analysis["design"].architecture_type,
                "status": analysis["design"].status,
                "effective_status": analysis["effective_status"],
                "status_explanation": analysis["status_explanation"],
            },
            "comparison_summary": {
                "completeness_score": completeness["completeness_score"],
                "pathway_count": pathway_count,
                "low_confidence_pathway_count": low_confidence_pathway_count,
                "visible_pathway_count": visible_pathway_count,
                "ecosystem_mixing": len(analysis["ecosystems"]) > 1,
                "missing_location_assignment_count": len(analysis["missing_location_assignments"]),
                "assigned_product_count": len(analysis["assigned_products"]),
                "detached_building_count": len(analysis["detached_buildings"]),
            },
            "design_completeness": completeness,
            "lineage_summary": lineage_summary,
            "warnings": warnings,
        }

    def compare(self, db, scenarios: List[Scenario]) -> Dict[str, object]:
        scenario_results = [self._build_scenario_result(db, scenario) for scenario in scenarios]
        all_warnings = sorted(
            {
                warning
                for scenario in scenario_results
                for warning in scenario.get("warnings", [])
            }
        )
        return {
            "status": "planning_comparison",
            "view_boundary": {
                "view_name": "scenario_comparison",
                "audience": "consumer",
                "authority_layer": "derived",
                "trust_zone": "derived_planning_intelligence",
                "data_classification": "planning_private",
                "permission_enforcement": "not_enforced",
                "limitations": [
                    "Comparison output is a planning view and does not enforce RBAC, contractor export scope, or utility submission rules.",
                ],
                "excluded_capabilities": [
                    "engineering_approval",
                    "contractor_packet",
                    "utility_submission",
                    "operational_control",
                ],
            },
            "comparison_dimensions": [
                "upfront_cost_placeholder",
                "future_expansion_score",
                "install_complexity_score",
                "backup_capability_score",
                "completeness_score",
                "pathway_count",
                "low_confidence_pathway_count",
            ],
            "scenarios": scenario_results,
            "rankings": {
                "lowest_upfront_cost": _rank_scenarios(
                    scenario_results, "upfront_cost_placeholder", reverse=False
                ),
                "best_expansion_readiness": _rank_scenarios(
                    scenario_results, "future_expansion_score", reverse=True
                ),
                "best_backup_capability": _rank_scenarios(
                    scenario_results, "backup_capability_score", reverse=True
                ),
                "lowest_install_complexity": _rank_scenarios(
                    scenario_results, "install_complexity_score", reverse=False
                ),
                "highest_planning_completeness": [
                    {
                        "scenario_id": scenario["id"],
                        "scenario_name": scenario["name"],
                        "value": scenario["design_completeness"]["completeness_score"],
                    }
                    for scenario in sorted(
                        scenario_results,
                        key=lambda item: item["design_completeness"]["completeness_score"],
                        reverse=True,
                    )
                ],
            },
            "summary": {
                "scenario_count": len(scenario_results),
                "average_upfront_cost_placeholder": _round_score(
                    sum(
                        scenario["upfront_cost_placeholder"]
                        for scenario in scenario_results
                        if scenario["upfront_cost_placeholder"] is not None
                    )
                    / max(
                        1,
                        len(
                            [
                                scenario
                                for scenario in scenario_results
                                if scenario["upfront_cost_placeholder"] is not None
                            ]
                        ),
                    )
                )
                if scenario_results
                else None,
                "average_completeness_score": _round_score(
                    sum(
                        scenario["design_completeness"]["completeness_score"]
                        for scenario in scenario_results
                    )
                    / len(scenario_results)
                )
                if scenario_results
                else None,
                "scenarios_with_low_confidence_pathways": [
                    scenario["name"]
                    for scenario in scenario_results
                    if scenario["comparison_summary"]["low_confidence_pathway_count"] > 0
                ],
                "scenarios_with_mixed_ecosystems": [
                    scenario["name"]
                    for scenario in scenario_results
                    if scenario["comparison_summary"]["ecosystem_mixing"]
                ],
            },
            "warnings": all_warnings,
            "comparison_note": "Scenario comparison remains planning-oriented. It surfaces placeholders, provenance posture, and deterministic tradeoff signals without implying engineering validity.",
        }


scenario_comparison_service = ScenarioComparisonService()

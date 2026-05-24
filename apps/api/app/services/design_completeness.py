from app.core.types import DataOrigin
from app.services.design_analysis import design_analysis_service


BACKUP_GOALS = {"partial_backup", "whole_home_backup", "generator_assisted", "off_grid_capable"}


def _has_inverter_strategy(product_types):
    return bool(product_types.intersection({"microinverter", "string_inverter", "hybrid_inverter"}))


def _has_backup_architecture(product_types):
    return bool(product_types.intersection({"battery", "generator", "gateway", "transfer_switch", "hybrid_inverter"}))


def _category_result(label: str, complete: bool):
    return {"label": label, "complete": complete}


class DesignCompletenessService:
    def evaluate(self, db, design_id: str):
        analysis = design_analysis_service.build(db, design_id)
        if analysis is None:
            return {
                "design_id": design_id,
                "completeness_score": 0,
                "completed_categories": [],
                "missing_categories": ["Design record not found"],
                "recommended_next_steps": ["Select a design before evaluating planning completeness."],
                "scope_note": "Planning completeness only. This is not engineering completeness.",
                "data_origin": DataOrigin.derived_estimate,
            }

        design = analysis["design"]
        product_types = analysis["product_types"]
        panel_count = len(analysis["panels"])
        load_count = len(analysis["loads"])
        backup_load_count = len(analysis["backup_loads"])
        linked_pathway_count = len(analysis["linked_pathways"])
        has_equipment = bool(analysis["assigned_products"])
        has_equipment_locations = bool(analysis["locations"]) and not analysis["missing_location_assignments"]
        main_panel = analysis["main_panel"]

        categories = [
            _category_result("Panel information captured", panel_count > 0),
            _category_result("Backup load grouping captured", backup_load_count > 0 or load_count == 0),
            _category_result("Product assignments exist", has_equipment),
            _category_result("At least one inverter strategy is assigned", _has_inverter_strategy(product_types)),
            _category_result("Assigned equipment has siting locations", has_equipment_locations or not has_equipment),
        ]

        if design.design_goal in BACKUP_GOALS:
            categories.append(
                _category_result(
                    "Backup-oriented architecture is present",
                    _has_backup_architecture(product_types),
                )
            )

        if analysis["detached_buildings"]:
            categories.append(
                _category_result(
                    "Detached structure pathway planning exists",
                    linked_pathway_count > 0,
                )
            )

        if analysis["workshop_buildings"] or design.design_goal == "workshop_ready":
            categories.append(
                _category_result(
                    "Workshop pathway planning exists",
                    linked_pathway_count > 0,
                )
            )

        if design.design_goal == "generator_assisted":
            categories.append(
                _category_result(
                    "Generator transfer strategy is represented",
                    bool(product_types.intersection({"generator", "gateway", "transfer_switch", "disconnect"})),
                )
            )

        if design.design_goal == "expansion_ready":
            categories.append(
                _category_result(
                    "Spare panel capacity is noted",
                    bool(main_panel and main_panel.breaker_spaces_available and main_panel.breaker_spaces_available > 1),
                )
            )
            categories.append(
                _category_result(
                    "Expansion planning pathway exists",
                    linked_pathway_count > 0,
                )
            )

        completed_categories = [entry["label"] for entry in categories if entry["complete"]]
        missing_categories = [entry["label"] for entry in categories if not entry["complete"]]

        next_steps = []
        for missing in missing_categories:
            if missing == "Panel information captured":
                next_steps.append("Capture main service or backup panel information before relying on expansion or backup guidance.")
            elif missing == "Backup load grouping captured":
                next_steps.append("Mark at least essential and preferred loads so backup-oriented designs have a planning basis.")
            elif missing == "Product assignments exist":
                next_steps.append("Assign products to the design so the advisor and derived takeoff can reason over actual composition.")
            elif missing == "At least one inverter strategy is assigned":
                next_steps.append("Assign a microinverter, string inverter, or hybrid inverter so the design has a clear power-conversion strategy.")
            elif missing == "Assigned equipment has siting locations":
                next_steps.append("Attach equipment locations to assigned products so routing and visibility reasoning has spatial context.")
            elif missing == "Backup-oriented architecture is present":
                next_steps.append("Add battery, generator, gateway, transfer, or hybrid equipment to support the selected backup-oriented goal.")
            elif missing == "Detached structure pathway planning exists":
                next_steps.append("Add estimated pathways for detached structures before assuming install scope or visibility is understood.")
            elif missing == "Workshop pathway planning exists":
                next_steps.append("Model a workshop-related pathway so future expansion assumptions have a traceable infrastructure route.")
            elif missing == "Generator transfer strategy is represented":
                next_steps.append("Add generator integration equipment such as a gateway, transfer switch, or disconnect strategy.")
            elif missing == "Spare panel capacity is noted":
                next_steps.append("Record available breaker capacity before describing the design as expansion-ready.")
            elif missing == "Expansion planning pathway exists":
                next_steps.append("Capture at least one expansion-oriented pathway before treating the design as expansion-ready.")

        score = 0 if not categories else round((len(completed_categories) / len(categories)) * 100)
        return {
            "design_id": design_id,
            "completeness_score": score,
            "completed_categories": completed_categories,
            "missing_categories": missing_categories,
            "recommended_next_steps": next_steps,
            "scope_note": "Planning completeness only. This does not indicate engineering, code, or permit completeness.",
            "data_origin": DataOrigin.derived_estimate,
        }


design_completeness_service = DesignCompletenessService()

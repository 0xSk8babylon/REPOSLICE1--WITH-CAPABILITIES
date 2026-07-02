from app.core.repository import repository

STATUS_EXPLANATIONS = {
    "draft": "Early exploration. Core planning inputs may still be missing.",
    "exploratory": "Concept-level planning with broad assumptions still in play.",
    "concept": "Legacy concept status. Treat as exploratory planning, not estimate-ready.",
    "homeowner_reviewed": "The homeowner has reviewed the concept and priorities.",
    "contractor_reviewed": "A contractor has reviewed the planning concept, but site validation may still be needed.",
    "estimate_ready": "Enough planning information exists for rough estimating, not permit-grade engineering.",
    "installation_planning": "Preparing for implementation and site validation. Field checks still govern final decisions.",
    "archived": "Historical design retained for comparison, not an active planning path.",
}


class DesignAnalysisService:
    def build(self, db, design_id: str):
        design = repository.get_design(db, design_id)
        if design is None:
            return None

        home = repository.get_home_by_id(db, design.home_id)
        buildings = repository.list_buildings(db, home_id=design.home_id)
        panels = repository.list_panels(db, home_id=design.home_id)
        loads = repository.list_loads(db, home_id=design.home_id)
        locations = repository.list_equipment_locations(db, home_id=design.home_id)
        pathways = repository.list_estimated_pathways(db, home_id=design.home_id)

        location_by_id = {location.id: location for location in locations}
        building_by_id = {building.id: building for building in buildings}

        assigned_products = []
        product_types = set()
        ecosystems = set()
        assigned_location_ids = set()
        missing_location_assignments = []

        for equipment in design.equipment:
            product = equipment.product or repository.get_product(db, equipment.product_id)
            location = location_by_id.get(equipment.location_id) if equipment.location_id else None
            assigned_products.append({"equipment": equipment, "product": product, "location": location})
            if product is not None:
                product_types.add(product.product_type)
                ecosystems.add(product.ecosystem)
            if equipment.location_id:
                assigned_location_ids.add(equipment.location_id)
            else:
                missing_location_assignments.append(equipment.id)

        detached_buildings = [building for building in buildings if building.type != "main_house"]
        workshop_buildings = [building for building in buildings if building.type == "workshop"]
        backup_loads = [load for load in loads if load.backup_priority in {"essential", "preferred"}]
        essential_loads = [load for load in loads if load.backup_priority == "essential"]
        linked_pathways = [pathway for pathway in pathways if pathway.design_id == design_id]
        home_level_pathways = [pathway for pathway in pathways if pathway.design_id in {None, design_id}]
        main_panel = next((panel for panel in panels if panel.panel_type == "main_service_panel"), None)
        effective_status = "exploratory" if design.status == "concept" else design.status

        return {
            "design": design,
            "home": home,
            "buildings": buildings,
            "building_by_id": building_by_id,
            "panels": panels,
            "loads": loads,
            "locations": locations,
            "location_by_id": location_by_id,
            "pathways": pathways,
            "linked_pathways": linked_pathways,
            "home_level_pathways": home_level_pathways,
            "assigned_products": assigned_products,
            "product_types": product_types,
            "ecosystems": ecosystems,
            "detached_buildings": detached_buildings,
            "workshop_buildings": workshop_buildings,
            "backup_loads": backup_loads,
            "essential_loads": essential_loads,
            "main_panel": main_panel,
            "assigned_location_ids": assigned_location_ids,
            "missing_location_assignments": missing_location_assignments,
            "effective_status": effective_status,
            "status_explanation": STATUS_EXPLANATIONS.get(
                design.status,
                "Planning lifecycle status is present, but it does not imply engineering approval.",
            ),
        }


design_analysis_service = DesignAnalysisService()

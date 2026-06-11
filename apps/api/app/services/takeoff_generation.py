from app.core.repository import repository
from app.core.types import DataOrigin, FactLifecycleState
from app.services.provenance import provenance_service
from app.takeoffs.schemas import TakeoffLineItem, TakeoffRequest


PLACEHOLDER_UNIT_COSTS = {
    "solar_panel": 250,
    "microinverter": 180,
    "string_inverter": 3200,
    "hybrid_inverter": 6500,
    "battery": 9000,
    "generator": 7000,
    "gateway": 1800,
    "smart_panel": 4200,
    "load_center": 900,
    "disconnect": 350,
    "transfer_switch": 1200,
    "ev_charger": 950,
    "other": 500,
}


class TakeoffGenerationService:
    def generate(self, db, design_id: str):
        design = repository.get_design(db, design_id)
        if design is None:
            return {
                "request": TakeoffRequest(
                    id=f"takeoff_{design_id}",
                    design_id=design_id,
                    status="missing_design",
                    requested_by="derived_system",
                    notes="Design not found. No takeoff could be derived.",
                    data_origin=DataOrigin.derived_estimate,
                    trust_notes=[
                        "Derived estimate",
                        "Requires site verification",
                    ],
                    missing_information=["No design was available to derive line items from."],
                    provenance_summary={
                        "basis": "Takeoff could not be derived because no design record was found.",
                        "source_types": ["calculation"],
                        "trust_states": [FactLifecycleState.derived_estimate.value],
                        "rule_keys": [],
                    },
                ),
                "line_items": [],
            }

        line_items = []
        for index, equipment in enumerate(design.equipment, start=1):
            product = equipment.product
            product_type = getattr(product, "product_type", "other")
            unit_cost = None
            if product and isinstance(product.specs, dict):
                unit_cost = product.specs.get("unit_cost_placeholder")
            if unit_cost is None:
                unit_cost = PLACEHOLDER_UNIT_COSTS.get(product_type, PLACEHOLDER_UNIT_COSTS["other"])

            quantity = float(equipment.quantity)
            location_name = equipment.location.name if equipment.location else "Unassigned location"
            item_name = (
                f"{product.manufacturer} {product.model}" if product else f"Unknown product {equipment.product_id}"
            )
            missing_information = []
            if equipment.location is None:
                missing_information.append("No equipment location is assigned.")
            if product is None:
                missing_information.append("Product details are missing.")
            if unit_cost is not None:
                missing_information.append("Unit cost remains a placeholder estimate.")
            provenance_summary = provenance_service.build_takeoff_line_provenance(db, equipment, product, design_id)
            line_items.append(
                TakeoffLineItem(
                    id=f"takeoff_{design_id}_line_{index}",
                    takeoff_request_id=f"takeoff_{design_id}",
                    category=product_type,
                    item_name=item_name,
                    quantity=quantity,
                    unit="each",
                    unit_cost_placeholder=unit_cost,
                    total_cost_placeholder=unit_cost * quantity if unit_cost is not None else None,
                    assumptions=(
                        f"Derived from design role '{equipment.role_in_system}' at '{location_name}'. "
                        "Pricing remains placeholder-only until verified product data is attached."
                    ),
                    notes=equipment.notes,
                    data_origin=DataOrigin.derived_estimate,
                    derivation_basis=f"Derived from persisted design composition for role '{equipment.role_in_system}'.",
                    trust_notes=[
                        "Derived from current design composition",
                        "Planning estimate only",
                        "Not permit-grade",
                    ],
                    missing_information=missing_information,
                    provenance_summary=provenance_summary,
                )
            )

        return {
            "request": TakeoffRequest(
                id=f"takeoff_{design_id}",
                design_id=design_id,
                status="derived" if line_items else "empty",
                requested_by="derived_system",
                notes=(
                    f"Derived from {len(line_items)} persisted design equipment assignment(s). "
                    "Line items remain planning placeholders, not procurement-ready takeoffs."
                ),
                data_origin=DataOrigin.derived_estimate,
                trust_notes=[
                    "Derived from current design composition",
                    "Planning estimate only",
                    "Requires site verification",
                    "Pathways are approximate",
                    "Not permit-grade",
                ],
                missing_information=[
                    "Pricing remains placeholder-only until verified product data exists.",
                    "Takeoff snapshots are intentionally transient in this phase.",
                ],
                provenance_summary={
                    "basis": "Takeoff request is assembled transiently from current design composition.",
                    "source_types": ["calculation", "internal_rule"],
                    "trust_states": [FactLifecycleState.derived_estimate.value],
                    "rule_keys": ["takeoff.design_composition_v1"],
                    "notes": ["Derived takeoff snapshots remain intentionally transient in this phase."],
                },
            ),
            "line_items": line_items,
        }


takeoff_generation_service = TakeoffGenerationService()

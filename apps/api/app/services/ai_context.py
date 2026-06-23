from app.compatibility_rules.schemas import CompatibilityIssue
from app.core.repository import repository
from app.core.schemas import ViewBoundaryMetadata
from app.core.types import ApiViewAudience, AuthorityLayer, DataClassification, FactLifecycleState
from app.designs.schemas import EnergySystemDesign
from app.equipment.schemas import EquipmentProduct
from app.homes.schemas import Home
from app.services.compatibility import compatibility_service
from app.services.design_analysis import design_analysis_service
from app.services.design_completeness import design_completeness_service
from app.services.provenance import provenance_service


class AIContextService:
    def build_design_context(self, db, design_id: str):
        design = repository.get_design(db, design_id)
        analysis = design_analysis_service.build(db, design_id)
        home = repository.get_home_by_id(db, design.home_id) if design else repository.get_home(db)
        products = repository.list_products(db)
        issues = repository.list_compatibility_issues(db, design_id=design_id)
        advisor_issues = compatibility_service.evaluate_design(db, design_id)
        completeness = design_completeness_service.evaluate(db, design_id)
        source_documents = repository.list_source_documents(db)
        provenance_records = repository.list_data_provenance(db)
        rule_provenance = repository.list_rule_provenance(db)
        assigned_products = []
        if analysis:
            for entry in analysis["assigned_products"]:
                product = entry["product"]
                location = entry["location"]
                if product is None:
                    continue
                assigned_products.append(
                    {
                        "product_id": product.id,
                        "manufacturer": product.manufacturer,
                        "model": product.model,
                        "product_type": product.product_type,
                        "ecosystem": product.ecosystem,
                        "quantity": entry["equipment"].quantity,
                        "location_id": location.id if location else None,
                        "location_name": location.name if location else None,
                        "data_origin": entry["equipment"].data_origin,
                        "provenance_summary": provenance_service.summarize_entity(db, "equipment_product", product.id).model_dump(),
                    }
                )

        return {
            "view_boundary": ViewBoundaryMetadata(
                view_name="ai_design_context",
                audience=ApiViewAudience.ai,
                authority_layer=AuthorityLayer.advisory,
                trust_zone="advisory_explanation",
                data_classification=DataClassification.planning_private,
                exposed_authority_layers=[
                    AuthorityLayer.canonical,
                    AuthorityLayer.derived,
                    AuthorityLayer.advisory,
                    AuthorityLayer.historical,
                ],
                limitations=[
                    "This is an AI-grounding context, not a source of new canonical facts.",
                    "Broad raw object exposure is retained for compatibility and grounding inspection only.",
                    "Data classifications are advisory metadata only; no RBAC or tenant isolation is enforced.",
                ],
                excluded_capabilities=[
                    "engineering_approval",
                    "permit_readiness",
                    "utility_submission",
                    "contractor_packet",
                    "operational_control",
                ],
            ).model_dump(),
            "permission_readiness": {
                "account_scaffolding_only": True,
                "role_enforcement": "not_enforced",
                "tenant_isolation": "not_enforced",
                "subscription_enforcement": "not_enforced",
                "notes": [
                    "AI context may include account-linked planning records, but account, role, and subscription fields do not enforce access.",
                    "Future AI-safe views should narrow this broad context through explicit view contracts before adding RBAC or exports.",
                ],
            },
            "design": EnergySystemDesign.model_validate(design).model_dump() if design else None,
            "home": Home.model_validate(home).model_dump() if home else None,
            "products": [
                {
                    **EquipmentProduct.model_validate(product).model_dump(),
                    "provenance_summary": provenance_service.summarize_entity(db, "equipment_product", product.id).model_dump(),
                    "source_documents": [
                        document.model_dump()
                        for document in provenance_service.get_source_documents_for_entity(db, "equipment_product", product.id)
                    ],
                }
                for product in products
            ],
            "compatibility_issues": [CompatibilityIssue.model_validate(issue).model_dump() for issue in issues],
            "advisor_issues": [issue.model_dump() for issue in advisor_issues],
            "design_completeness": completeness,
            "design_maturity": {
                "stored_status": analysis["design"].status if analysis else None,
                "effective_status": analysis["effective_status"] if analysis else None,
                "explanation": analysis["status_explanation"] if analysis else None,
            },
            "trust_summary": {
                "design_data_origin": design.data_origin if design else None,
                "assigned_product_origins": sorted(
                    list({entry["equipment"].data_origin for entry in analysis["assigned_products"]})
                )
                if analysis
                else [],
                "ecosystems_in_design": sorted(list(analysis["ecosystems"])) if analysis else [],
                "ecosystem_mixing": bool(analysis and len(analysis["ecosystems"]) > 1),
                "pathway_confidence_levels": sorted(
                    list({pathway.confidence_level for pathway in analysis["linked_pathways"] if pathway.confidence_level})
                )
                if analysis
                else [],
            },
            "assigned_products": assigned_products,
            "pathway_summary": {
                "linked_pathway_count": len(analysis["linked_pathways"]) if analysis else 0,
                "high_visibility_pathways": [
                    pathway.name for pathway in analysis["linked_pathways"] if pathway.visibility_level == "high"
                ]
                if analysis
                else [],
                "low_confidence_pathways": [
                    pathway.name for pathway in analysis["linked_pathways"] if pathway.confidence_level == "low"
                ]
                if analysis
                else [],
            },
            "missing_categories": completeness["missing_categories"],
            "source_documents": [
                {
                    "id": document.id,
                    "title": document.title,
                    "source_type": document.source_type,
                    "verification_status": document.verification_status,
                    "manufacturer": document.manufacturer,
                    "product_model": document.product_model,
                    "retrieved_at": document.retrieved_at,
                    "notes": document.notes,
                }
                for document in source_documents
            ],
            "provenance_records": [
                {
                    "id": record.id,
                    "entity_type": record.entity_type,
                    "entity_id": record.entity_id,
                    "field_name": record.field_name,
                    "source_type": record.source_type,
                    "trust_state": record.trust_state,
                    "confidence_level": record.confidence_level,
                    "source_document_id": record.source_document_id,
                    "notes": record.notes,
                }
                for record in provenance_records
            ],
            "rule_provenance": [
                {
                    "rule_key": record.rule_key,
                    "rule_name": record.rule_name,
                    "source_type": record.source_type,
                    "trust_state": record.trust_state,
                    "source_document_id": record.source_document_id,
                    "description": record.description,
                    "notes": record.notes,
                }
                for record in rule_provenance
            ],
            "unverified_fields": sorted(
                {
                    field
                    for product in products
                    for field in provenance_service.summarize_entity(db, "equipment_product", product.id).unverified_fields
                }
            ),
            "placeholder_assumptions": [
                record.field_name
                for record in provenance_records
                if record.trust_state
                in {
                    FactLifecycleState.placeholder.value,
                    FactLifecycleState.demo_seed.value,
                    FactLifecycleState.derived_estimate.value,
                }
            ],
            "grounding_warnings": [
                "Placeholder and derived planning outputs must not be presented as verified engineering facts.",
                "Takeoff outputs remain transient and are not persisted snapshots.",
                "Pathway assumptions remain approximate until site verification.",
                "Verification status and trust badges are related but not interchangeable; AI should cite both when available.",
            ],
            "grounding_policy": {
                "structured_facts_are_authoritative": True,
                "ai_should_explain_not_invent": True,
                "rule_outputs_must_be_cited_in_explanations": True,
                "placeholder_and_derived_states_must_remain_visible": True,
                "takeoff_snapshots_remain_transient": True,
            },
        }


ai_context_service = AIContextService()

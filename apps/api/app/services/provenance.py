from typing import Dict, Iterable, List, Optional

from app.core.repository import repository
from app.provenance.schemas import ProvenanceSummary, SourceDocument


class ProvenanceService:
    def summarize_entity(self, db, entity_type: str, entity_id: str) -> ProvenanceSummary:
        records = repository.list_data_provenance(db, entity_type=entity_type, entity_id=entity_id)
        source_document_ids = [record.source_document_id for record in records if record.source_document_id]
        documents = repository.get_source_documents_by_ids(db, source_document_ids)
        document_map = {document.id: document for document in documents}

        verification_statuses = sorted(
            {
                document.verification_status
                for document in documents
                if getattr(document, "verification_status", None)
            }
        )
        last_retrieved_at = max(
            [document.retrieved_at for document in documents if document.retrieved_at],
            default=None,
        )
        last_verified_at = max(
            [record.verified_at for record in records if record.verified_at],
            default=None,
        )
        unverified_fields = sorted(
            {
                record.field_name
                for record in records
                if record.trust_state in {"placeholder", "demo_seed", "derived_estimate"}
                or (
                    record.source_document_id
                    and document_map.get(record.source_document_id)
                    and document_map[record.source_document_id].verification_status != "manufacturer_verified"
                )
            }
        )

        notes: List[str] = []
        for record in records:
            if record.notes:
                notes.append(record.notes)
        for document in documents:
            if document.notes:
                notes.append(document.notes)

        return ProvenanceSummary(
            entity_type=entity_type,
            entity_id=entity_id,
            source_types=sorted({record.source_type for record in records}),
            trust_states=sorted({record.trust_state for record in records}),
            verification_statuses=verification_statuses,
            source_document_ids=sorted({record.source_document_id for record in records if record.source_document_id}),
            last_retrieved_at=last_retrieved_at,
            last_verified_at=last_verified_at,
            unverified_fields=unverified_fields,
            notes=notes,
        )

    def get_source_documents_for_entity(self, db, entity_type: str, entity_id: str) -> List[SourceDocument]:
        records = repository.list_data_provenance(db, entity_type=entity_type, entity_id=entity_id)
        source_document_ids = [record.source_document_id for record in records if record.source_document_id]
        return [
            SourceDocument.from_orm(document)
            for document in repository.get_source_documents_by_ids(db, source_document_ids)
        ]

    def get_rule_documents(self, db, rule_keys: Iterable[str]):
        items = []
        for rule_key in sorted(set(rule_keys)):
            items.extend(repository.list_rule_provenance(db, rule_key=rule_key))
        return items

    def build_takeoff_line_provenance(self, db, equipment, product, design_id: str) -> Dict[str, object]:
        summary = self.summarize_entity(db, "equipment_product", product.id) if product is not None else None
        rule_records = repository.list_rule_provenance(db, rule_key="takeoff.design_composition_v1")
        return {
            "basis": "Derived from current design composition",
            "source_types": ["calculation", "internal_rule"] + (summary.source_types if summary else []),
            "trust_states": ["derived_estimate"] + (summary.trust_states if summary else []),
            "rule_keys": [record.rule_key for record in rule_records],
            "source_document_ids": summary.source_document_ids if summary else [],
            "notes": [
                f"Role '{equipment.role_in_system}' was translated into a transient takeoff line.",
                "No persistent takeoff snapshot was stored in this phase.",
            ]
            + (summary.notes[:2] if summary else []),
        }

    def build_advisor_issue_provenance(self, db, issue, related_rule_key: Optional[str] = None) -> Dict[str, object]:
        rule_keys = [related_rule_key] if related_rule_key else []
        if issue.data_origin == "derived_estimate" and related_rule_key is None:
            rule_keys = ["advisor.derived_planning_issue"]
        rules = self.get_rule_documents(db, rule_keys) if rule_keys else []
        return {
            "basis": "Deterministic planning rule output",
            "source_types": ["internal_rule"],
            "trust_states": [issue.data_origin],
            "rule_keys": [record.rule_key for record in rules],
            "notes": [record.description for record in rules]
            or ["This issue is derived from explicit planning rules, not conversational inference."],
        }


provenance_service = ProvenanceService()

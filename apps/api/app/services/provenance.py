from typing import Dict, Iterable, List, Optional

from app.core.repository import repository
from app.provenance.schemas import ProvenanceSummary, SourceDocument


class ProvenanceService:
    def _build_summary(self, entity_type: str, entity_id: str, records, documents) -> ProvenanceSummary:
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
            confidence_levels=sorted({record.confidence_level for record in records if record.confidence_level}),
            verification_statuses=verification_statuses,
            source_document_ids=sorted({record.source_document_id for record in records if record.source_document_id}),
            last_retrieved_at=last_retrieved_at,
            last_verified_at=last_verified_at,
            unverified_fields=unverified_fields,
            notes=notes,
            limitations=[
                "Provenance summaries are derived metadata and do not make records engineering-verified or access-controlled.",
                "Field-level provenance remains partial unless all important fields have explicit source records.",
            ],
        )

    def summarize_entity(self, db, entity_type: str, entity_id: str) -> ProvenanceSummary:
        return self.summarize_entities(db, entity_type, [entity_id]).get(
            entity_id, ProvenanceSummary(entity_type=entity_type, entity_id=entity_id)
        )

    def summarize_entities(self, db, entity_type: str, entity_ids: List[str]) -> Dict[str, ProvenanceSummary]:
        if not entity_ids:
            return {}
        records = repository.list_data_provenance_for_entities(db, entity_type=entity_type, entity_ids=entity_ids)
        records_by_entity: Dict[str, List[object]] = {entity_id: [] for entity_id in entity_ids}
        for record in records:
            records_by_entity.setdefault(record.entity_id, []).append(record)

        source_document_ids = [
            record.source_document_id for record in records if getattr(record, "source_document_id", None)
        ]
        documents = repository.get_source_documents_by_ids(db, source_document_ids)
        documents_by_id = {document.id: document for document in documents}

        summaries: Dict[str, ProvenanceSummary] = {}
        for entity_id in entity_ids:
            entity_records = records_by_entity.get(entity_id, [])
            entity_documents = list(
                {
                    record.source_document_id: documents_by_id[record.source_document_id]
                    for record in entity_records
                    if getattr(record, "source_document_id", None) and record.source_document_id in documents_by_id
                }.values()
            )
            summaries[entity_id] = self._build_summary(entity_type, entity_id, entity_records, entity_documents)
        return summaries

    def get_source_documents_for_entity(self, db, entity_type: str, entity_id: str) -> List[SourceDocument]:
        records = repository.list_data_provenance(db, entity_type=entity_type, entity_id=entity_id)
        source_document_ids = [record.source_document_id for record in records if record.source_document_id]
        return [
            SourceDocument.from_orm(document)
            for document in repository.get_source_documents_by_ids(db, source_document_ids)
        ]

    def get_rule_documents_map(self, db, rule_keys: Iterable[str]) -> Dict[str, List[object]]:
        normalized_keys = sorted(set(rule_keys))
        if not normalized_keys:
            return {}
        records = repository.list_rule_provenance_for_keys(db, normalized_keys)
        grouped: Dict[str, List[object]] = {rule_key: [] for rule_key in normalized_keys}
        for record in records:
            grouped.setdefault(record.rule_key, []).append(record)
        return grouped

    def get_rule_documents(self, db, rule_keys: Iterable[str]):
        items = []
        for _, records in self.get_rule_documents_map(db, rule_keys).items():
            items.extend(records)
        return items

    def build_takeoff_line_provenance(self, db, equipment, product, design_id: str) -> Dict[str, object]:
        summary = self.summarize_entity(db, "equipment_product", product.id) if product is not None else None
        rule_records = repository.list_rule_provenance(db, rule_key="takeoff.design_composition_v1")
        return {
            "basis": "Derived from current design composition",
            "authority_layer": "derived",
            "data_classification": "planning_private",
            "derivation_type": "deterministic_rule",
            "source_types": ["calculation", "internal_rule"] + (summary.source_types if summary else []),
            "trust_states": ["derived_estimate"] + (summary.trust_states if summary else []),
            "rule_keys": [record.rule_key for record in rule_records],
            "source_document_ids": summary.source_document_ids if summary else [],
            "limitations": [
                "Transient takeoff line only; not a persisted procurement, bid, or installation record.",
            ],
            "notes": [
                f"Role '{equipment.role_in_system}' was translated into a transient takeoff line.",
                "No persistent takeoff snapshot was stored in this phase.",
            ]
            + (summary.notes[:2] if summary else []),
        }

    def build_advisor_issue_provenance(
        self,
        db,
        issue,
        related_rule_key: Optional[str] = None,
        rule_documents_map: Optional[Dict[str, List[object]]] = None,
    ) -> Dict[str, object]:
        rule_keys = [related_rule_key] if related_rule_key else []
        if issue.data_origin == "derived_estimate" and related_rule_key is None:
            rule_keys = ["advisor.derived_planning_issue"]
        normalized_rule_keys = sorted(set(rule_keys))
        if rule_documents_map is not None:
            rules = [record for rule_key in normalized_rule_keys for record in rule_documents_map.get(rule_key, [])]
        else:
            rules = self.get_rule_documents(db, normalized_rule_keys) if normalized_rule_keys else []
        persisted_rule_keys = sorted({record.rule_key for record in rules})
        return {
            "basis": "Deterministic planning rule output",
            "authority_layer": "derived",
            "data_classification": "planning_private",
            "derivation_type": "deterministic_rule",
            "source_types": ["internal_rule"],
            "trust_states": [issue.data_origin],
            "rule_keys": persisted_rule_keys,
            "limitations": [
                "Advisor issues are planning guidance and do not represent engineering, code, permit, or utility approval.",
            ],
            "notes": [record.description for record in rules]
            or ["This issue is derived from explicit planning rules, not conversational inference."],
        }

    def build_recommendation_provenance(
        self,
        db,
        rule_keys: Iterable[str],
        notes: Optional[List[str]] = None,
        rule_documents_map: Optional[Dict[str, List[object]]] = None,
    ):
        normalized_rule_keys = sorted(set(rule_keys))
        if rule_documents_map is not None:
            rules = [record for rule_key in normalized_rule_keys for record in rule_documents_map.get(rule_key, [])]
        else:
            rules = self.get_rule_documents(db, normalized_rule_keys)
        persisted_rule_keys = sorted({record.rule_key for record in rules})
        return {
            "basis": "Deterministic recommendation-profile selection",
            "authority_layer": "derived",
            "data_classification": "planning_private",
            "derivation_type": "deterministic_rule",
            "source_types": ["internal_rule"],
            "trust_states": ["derived_estimate"],
            "rule_keys": persisted_rule_keys,
            "limitations": [
                "Recommendation profiles are advisory planning outputs and do not create canonical site facts or operational authority.",
            ],
            "notes": notes
            or [record.description for record in rules]
            or ["Recommendation profiles are derived from explicit planning rules."],
        }

    def build_estimate_inspectability(
        self,
        db,
        *,
        basis: str,
        confidence_level: str,
        rule_keys: Iterable[str],
        input_signals: List[Dict[str, object]],
        estimated_inputs: Optional[List[str]] = None,
        incomplete_inputs: Optional[List[str]] = None,
        notes: Optional[List[str]] = None,
        rule_documents_map: Optional[Dict[str, List[object]]] = None,
    ):
        normalized_rule_keys = sorted(set(rule_keys))
        if rule_documents_map is not None:
            rules = [record for rule_key in normalized_rule_keys for record in rule_documents_map.get(rule_key, [])]
        else:
            rules = self.get_rule_documents(db, normalized_rule_keys)
        persisted_rule_keys = sorted({record.rule_key for record in rules})
        estimated_inputs = estimated_inputs or []
        incomplete_inputs = incomplete_inputs or []
        warnings: List[str] = []
        if incomplete_inputs:
            warnings.append(
                "Planning-only warning: some recommendation inputs are incomplete, so profile fit and sizing guidance remain partial."
            )
        elif estimated_inputs or confidence_level == "low":
            warnings.append(
                "Planning-only warning: some recommendation inputs remain estimated, so profile fit and sizing guidance should be treated as directional."
            )
        return {
            "basis": basis,
            "authority_layer": "derived",
            "data_classification": "planning_private",
            "derivation_type": "deterministic_rule",
            "confidence_level": confidence_level,
            "trust_state": "derived_estimate",
            "rule_keys": persisted_rule_keys,
            "input_signals": input_signals,
            "estimated_inputs": estimated_inputs,
            "incomplete_inputs": incomplete_inputs,
            "limitations": [
                "Planning-only derived estimate; not an engineered design, permit finding, utility approval, or operational command.",
            ],
            "notes": notes
            or [record.description for record in rules]
            or ["This planning estimate is derived from explicit deterministic rules."],
            "partial_provenance_warning": warnings[0] if warnings else None,
        }


provenance_service = ProvenanceService()

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field

from app.core.schemas import ORMModel
from app.core.types import AuthorityLayer, DataClassification, DataOrigin
from app.provenance.schemas import ProvenanceSummary


class TwinPlanningRecordClassification(str, Enum):
    recorded_fact = "recorded_fact"
    source_backed_fact = "source_backed_fact"
    derived_output = "derived_output"
    advisory_output = "advisory_output"
    placeholder = "placeholder"
    unknown = "unknown"


class TwinPlanningDependencyHook(ORMModel):
    source_entity_type: str
    source_entity_id: Optional[str] = None
    target_entity_type: str
    target_entity_id: Optional[str] = None
    relationship: str
    rule_keys: List[str] = Field(default_factory=list)
    confidence_level: Optional[str] = None
    note: str


class TwinPlanningContextRecord(ORMModel):
    entity_type: str
    entity_id: Optional[str] = None
    label: str
    classification: TwinPlanningRecordClassification
    authority_layer: AuthorityLayer
    data_classification: DataClassification = DataClassification.planning_private
    data_origin: Optional[DataOrigin] = None
    record: Dict[str, Any] = Field(default_factory=dict)
    provenance_summary: Optional[ProvenanceSummary] = None
    source_document_ids: List[str] = Field(default_factory=list)
    rule_keys: List[str] = Field(default_factory=list)
    dependency_hooks: List[TwinPlanningDependencyHook] = Field(default_factory=list)
    classification_reasons: List[str] = Field(default_factory=list)
    missing_fields: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class TwinPlanningContextSection(ORMModel):
    section_key: str
    label: str
    records: List[TwinPlanningContextRecord] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)


class TwinPlanningContext(ORMModel):
    context_id: str
    home_id: str
    anchor_type: str = "home_id"
    context_label: str
    authority_layer: AuthorityLayer = AuthorityLayer.canonical
    data_classification: DataClassification = DataClassification.planning_private
    permission_enforcement: str = "not_enforced"
    implementation_boundary: str
    sections: List[TwinPlanningContextSection] = Field(default_factory=list)
    classification_summary: Dict[str, int] = Field(default_factory=dict)
    provenance_gaps: List[str] = Field(default_factory=list)
    continuity_gaps: List[str] = Field(default_factory=list)
    dependency_hooks: List[TwinPlanningDependencyHook] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)

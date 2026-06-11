from datetime import datetime
from typing import Any, List, Optional

from pydantic import Field

from app.core.schemas import ORMModel
from app.core.types import (
    AuthorityLayer,
    ConfidenceLevel,
    DataClassification,
    DataOrigin,
    FactLifecycleState,
    SourceDocumentType,
    VerificationStatus,
)


class SourceDocumentBase(ORMModel):
    title: str
    source_type: SourceDocumentType
    manufacturer: Optional[str] = None
    product_model: Optional[str] = None
    url: Optional[str] = None
    file_reference: Optional[str] = None
    version: Optional[str] = None
    published_date: Optional[datetime] = None
    retrieved_at: Optional[datetime] = None
    verification_status: VerificationStatus
    notes: Optional[str] = None
    data_origin: DataOrigin = DataOrigin.user_created


class SourceDocument(SourceDocumentBase):
    id: str
    created_at: datetime
    updated_at: datetime


class SourceDocumentCreate(SourceDocumentBase):
    id: str


class SourceDocumentUpdate(ORMModel):
    title: Optional[str] = None
    manufacturer: Optional[str] = None
    product_model: Optional[str] = None
    url: Optional[str] = None
    file_reference: Optional[str] = None
    version: Optional[str] = None
    published_date: Optional[datetime] = None
    retrieved_at: Optional[datetime] = None
    verification_status: Optional[VerificationStatus] = None
    notes: Optional[str] = None


class DataProvenanceBase(ORMModel):
    entity_type: str
    entity_id: str
    field_name: str
    source_document_id: Optional[str] = None
    source_type: SourceDocumentType
    trust_state: FactLifecycleState
    value_snapshot: Optional[Any] = None
    confidence_level: ConfidenceLevel
    verified_at: Optional[datetime] = None
    notes: Optional[str] = None


class DataProvenance(DataProvenanceBase):
    id: str
    created_at: datetime
    updated_at: datetime


class DataProvenanceCreate(DataProvenanceBase):
    id: str


class DataProvenanceUpdate(ORMModel):
    source_document_id: Optional[str] = None
    source_type: Optional[SourceDocumentType] = None
    trust_state: Optional[FactLifecycleState] = None
    value_snapshot: Optional[Any] = None
    confidence_level: Optional[ConfidenceLevel] = None
    verified_at: Optional[datetime] = None
    notes: Optional[str] = None


class RuleProvenanceBase(ORMModel):
    rule_key: str
    rule_name: str
    source_type: SourceDocumentType
    source_document_id: Optional[str] = None
    trust_state: FactLifecycleState
    description: str
    notes: Optional[str] = None


class RuleProvenance(RuleProvenanceBase):
    id: str
    created_at: datetime
    updated_at: datetime


class RuleProvenanceCreate(RuleProvenanceBase):
    id: str


class RuleProvenanceUpdate(ORMModel):
    rule_name: Optional[str] = None
    source_type: Optional[SourceDocumentType] = None
    source_document_id: Optional[str] = None
    trust_state: Optional[FactLifecycleState] = None
    description: Optional[str] = None
    notes: Optional[str] = None


class ProvenanceSummary(ORMModel):
    entity_type: str
    entity_id: str
    authority_layer: AuthorityLayer = AuthorityLayer.derived
    data_classification: DataClassification = DataClassification.planning_private
    source_types: List[str] = Field(default_factory=list)
    trust_states: List[str] = Field(default_factory=list)
    confidence_levels: List[str] = Field(default_factory=list)
    verification_statuses: List[str] = Field(default_factory=list)
    source_document_ids: List[str] = Field(default_factory=list)
    last_retrieved_at: Optional[datetime] = None
    last_verified_at: Optional[datetime] = None
    unverified_fields: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)

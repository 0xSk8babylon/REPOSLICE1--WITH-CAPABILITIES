from typing import Any, Optional

from app.core.schemas import ORMModel
from app.facts.schemas import Fact


class PhotoEvidenceFactCreate(ORMModel):
    evidence_id: str
    file_name: str
    content_type: str
    size_bytes: int
    extracted_key: str
    extracted_value: Any
    unit: Optional[str] = None
    extraction_note: Optional[str] = None


class EvidenceIntakeResult(ORMModel):
    evidence_id: str
    accepted: bool
    fact: Fact
    validation_summary: str
    limitations: list

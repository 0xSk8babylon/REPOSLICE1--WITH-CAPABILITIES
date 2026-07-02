from pathlib import PurePath

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.types import FactConfidenceTier, FactSource
from app.evidence.schemas import EvidenceIntakeResult
from app.facts.schemas import FactCreate
from app.services.facts import fact_lifecycle_service

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}
MAX_EVIDENCE_SIZE_BYTES = 10 * 1024 * 1024
ALLOWED_FACT_PREFIXES = ("service.", "equipment.", "roof.", "load.")


class EvidenceIntakeService:
    def photo_evidence_to_fact(self, db: Session, home_id: str, payload):
        self._validate(payload)
        fact = fact_lifecycle_service.create_fact(
            db,
            home_id,
            FactCreate(
                id=f"fact_from_{payload.evidence_id}",
                key=payload.extracted_key,
                value=payload.extracted_value,
                unit=payload.unit,
                source=FactSource.photo_verified,
                confidence_tier=FactConfidenceTier.known,
                notes=payload.extraction_note,
            ),
        )
        return EvidenceIntakeResult(
            evidence_id=payload.evidence_id,
            accepted=True,
            fact=fact,
            validation_summary="Evidence metadata validated before fact creation.",
            limitations=[
                "No raw file is stored by this endpoint.",
                "No OCR, AI extraction, external provider, or malware scanning is performed.",
                "Photo-verified means accepted evidence metadata created the fact; field verification remains separate.",
            ],
        )

    def _validate(self, payload):
        if payload.content_type not in ALLOWED_CONTENT_TYPES:
            raise HTTPException(status_code=400, detail="Unsupported evidence content type")
        if payload.size_bytes <= 0 or payload.size_bytes > MAX_EVIDENCE_SIZE_BYTES:
            raise HTTPException(status_code=400, detail="Evidence size is outside allowed bounds")
        path = PurePath(payload.file_name)
        if path.name != payload.file_name or ".." in path.parts:
            raise HTTPException(status_code=400, detail="Evidence file name is not allowed")
        if not payload.extracted_key.startswith(ALLOWED_FACT_PREFIXES):
            raise HTTPException(status_code=400, detail="Extracted fact key is outside allowed evidence domains")
        if payload.extracted_value in (None, ""):
            raise HTTPException(status_code=400, detail="Extracted value is required")


evidence_intake_service = EvidenceIntakeService()

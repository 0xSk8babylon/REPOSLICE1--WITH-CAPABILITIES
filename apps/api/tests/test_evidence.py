import unittest

from fastapi import HTTPException  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

import tests.fast_db as fast_db  # noqa: E402
from app.core import models  # noqa: E402
from app.core.database import engine  # noqa: E402
from app.evidence.router import create_photo_evidence_fact  # noqa: E402
from app.evidence.schemas import PhotoEvidenceFactCreate  # noqa: E402
from app.main import app  # noqa: E402

HOME_ID = "home_001"


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        fast_db.reset_and_reseed()
        with Session(engine) as db:
            db.query(models.Fact).delete()
            db.commit()

    def test_route_registration(self):
        paths = set(app.openapi()["paths"])
        self.assertIn("/api/evidence/homes/{home_id}/photo-facts", paths)

    def test_valid_photo_evidence_creates_photo_verified_fact(self):
        payload = PhotoEvidenceFactCreate(
            evidence_id="panel_photo_1",
            file_name="panel.jpg",
            content_type="image/jpeg",
            size_bytes=250000,
            extracted_key="service.main_breaker_amps",
            extracted_value=200,
            unit="A",
        )

        with Session(engine) as db:
            result = create_photo_evidence_fact(HOME_ID, payload, db)

        self.assertTrue(result.accepted)
        self.assertEqual("fact_from_panel_photo_1", result.fact.id)
        self.assertEqual("photo_verified", result.fact.source.value)
        self.assertEqual("known", result.fact.confidence_tier.value)

    def test_rejects_malformed_or_unsupported_evidence(self):
        bad_payloads = [
            PhotoEvidenceFactCreate(
                evidence_id="bad_type",
                file_name="panel.gif",
                content_type="image/gif",
                size_bytes=100,
                extracted_key="service.main_breaker_amps",
                extracted_value=200,
            ),
            PhotoEvidenceFactCreate(
                evidence_id="bad_name",
                file_name="../panel.jpg",
                content_type="image/jpeg",
                size_bytes=100,
                extracted_key="service.main_breaker_amps",
                extracted_value=200,
            ),
            PhotoEvidenceFactCreate(
                evidence_id="bad_key",
                file_name="panel.jpg",
                content_type="image/jpeg",
                size_bytes=100,
                extracted_key="billing.account_number",
                extracted_value="secret",
            ),
        ]

        with Session(engine) as db:
            for payload in bad_payloads:
                with self.assertRaises(HTTPException):
                    create_photo_evidence_fact(HOME_ID, payload, db)
            self.assertEqual(0, db.query(models.Fact).count())


if __name__ == "__main__":
    unittest.main()

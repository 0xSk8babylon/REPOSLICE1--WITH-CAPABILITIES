import unittest
from datetime import datetime

import tests.fast_db as fast_db  # noqa: E402

from sqlalchemy.orm import Session  # noqa: E402

from app.core import models  # noqa: E402
from app.core.database import engine  # noqa: E402
from app.main import app  # noqa: E402
from app.privacy.router import delete_homeowner_record, export_homeowner_record, record_consent  # noqa: E402
from app.privacy.schemas import ConsentRecordCreate  # noqa: E402
from app.security.principal import AuthPrincipal  # noqa: E402


HOME_ID = "home_001"


class PrivacyTests(unittest.TestCase):
    def setUp(self):
        fast_db.reset_and_reseed()
        with Session(engine) as db:
            db.query(models.ConsentRecord).delete()
            db.query(models.Fact).delete()
            db.commit()

    def test_route_registration(self):
        paths = set(app.openapi()["paths"])
        self.assertIn("/api/privacy/homes/{home_id}/export", paths)
        self.assertIn("/api/privacy/homes/{home_id}/consent", paths)
        self.assertIn("/api/privacy/homes/{home_id}", paths)

    def test_export_includes_facts_and_consent_records(self):
        with Session(engine) as db:
            db.add(
                models.Fact(
                    id="privacy_fact",
                    home_id=HOME_ID,
                    key="service.main_breaker_amps",
                    value=200,
                    unit="A",
                    source="homeowner_stated",
                    confidence_tier="assumed",
                    verified_at=datetime(2026, 6, 13),
                    derived_from=[],
                )
            )
            record_consent(
                HOME_ID,
                ConsentRecordCreate(
                    id="consent_1",
                    home_id=HOME_ID,
                    user_id="user_a",
                    consent_type="privacy_export",
                    status="granted",
                ),
                db,
            )
            exported = export_homeowner_record(HOME_ID, db, _owner_principal())

        self.assertEqual("residential_energy_planner_privacy_export_v1", exported.portable_format)
        self.assertEqual("privacy_fact", exported.exported_sections["facts"][0]["id"])
        self.assertEqual("consent_1", exported.exported_sections["consent_records"][0]["id"])

    def test_delete_removes_home_and_local_related_records(self):
        with Session(engine) as db:
            record_consent(
                HOME_ID,
                ConsentRecordCreate(
                    id="consent_delete",
                    home_id=HOME_ID,
                    user_id="user_a",
                    consent_type="delete",
                    status="requested",
                ),
                db,
            )
            result = delete_homeowner_record(HOME_ID, db, _owner_principal())
            remaining_home = db.get(models.Home, HOME_ID)
            remaining_consent = db.query(models.ConsentRecord).filter_by(home_id=HOME_ID).count()

        self.assertTrue(result.deleted)
        self.assertIsNone(remaining_home)
        self.assertEqual(0, remaining_consent)
        self.assertIn("local SQLite", result.limitations[0])


def _owner_principal():
    return AuthPrincipal(
        user_id="privacy_owner",
        allowed_home_ids={HOME_ID},
        auth_source="fake_oidc_bearer",
        account_ids={"account_demo"},
        account_roles={"account_demo": "owner"},
    )


if __name__ == "__main__":
    unittest.main()

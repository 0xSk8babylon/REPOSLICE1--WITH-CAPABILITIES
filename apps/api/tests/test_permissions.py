import unittest
from datetime import datetime

from tests.fast_db import reset_and_reseed  # noqa: E402  must precede app imports

from fastapi import HTTPException  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

from app.core import models  # noqa: E402
from app.core.database import engine  # noqa: E402
from app.designs import router as designs_router  # noqa: E402
from app.homes import router as homes_router  # noqa: E402
from app.homes.schemas import HomeUpdate  # noqa: E402
from app.product_library import router as product_library_router  # noqa: E402
from app.scenarios import router as scenarios_router  # noqa: E402
from app.security.principal import VerifiedIdentityClaims, principal_from_verified_claims  # noqa: E402


class AccountMembershipPermissionsTests(unittest.TestCase):
    def setUp(self):
        reset_and_reseed()
        with Session(engine) as db:
            self._add_extra_scope_records(db)

    def test_home_collection_filters_by_account_membership_and_hides_null_account_homes(self):
        with Session(engine) as db:
            principal = self._principal(db, role="owner")

            homes = homes_router.list_homes(db, principal)

        home_ids = {home.id for home in homes}
        self.assertIn("home_001", home_ids)
        self.assertNotIn("home_other", home_ids)
        self.assertNotIn("home_null", home_ids)

    def test_provider_identity_without_app_membership_cannot_list_homes(self):
        with Session(engine) as db:
            principal = self._principal_without_membership(db)

            homes = homes_router.list_homes(db, principal)

        self.assertEqual([], homes)

    def test_viewer_can_read_but_cannot_write_home(self):
        with Session(engine) as db:
            principal = self._principal(db, role="viewer")

            homes = homes_router.list_homes(db, principal)
            with self.assertRaises(HTTPException) as error:
                homes_router.update_home("home_001", HomeUpdate(notes="viewer attempted write"), db, principal)

        self.assertIn("home_001", {home.id for home in homes})
        self.assertEqual(403, error.exception.status_code)

    def test_member_can_write_home(self):
        with Session(engine) as db:
            principal = self._principal(db, role="member")

            updated = homes_router.update_home("home_001", HomeUpdate(notes="member write allowed"), db, principal)

        self.assertEqual("member write allowed", updated.notes)

    def test_design_collection_filters_by_authorized_homes_and_denies_cross_account_equipment(self):
        with Session(engine) as db:
            principal = self._principal(db, role="owner")

            designs = designs_router.list_designs(db, principal)
            with self.assertRaises(HTTPException) as error:
                designs_router.list_design_equipment("design_other", db, principal)

        design_ids = {design.id for design in designs}
        self.assertIn("design_001", design_ids)
        self.assertIn("design_002", design_ids)
        self.assertNotIn("design_other", design_ids)
        self.assertNotIn("design_null", design_ids)
        self.assertEqual(403, error.exception.status_code)

    def test_scenario_collection_filters_and_cross_account_revisions_are_denied(self):
        with Session(engine) as db:
            principal = self._principal(db, role="owner")

            scenarios = scenarios_router.list_scenarios(db, principal)
            with self.assertRaises(HTTPException) as error:
                scenarios_router.list_scenario_revisions("scenario_other", db, principal)

        scenario_ids = {scenario["id"] for scenario in scenarios}
        self.assertIn("scenario_001", scenario_ids)
        self.assertIn("scenario_002", scenario_ids)
        self.assertNotIn("scenario_other", scenario_ids)
        self.assertNotIn("scenario_null", scenario_ids)
        self.assertEqual(403, error.exception.status_code)

    def test_global_product_library_read_remains_available(self):
        with Session(engine) as db:
            products = product_library_router.list_products(db)

        self.assertGreater(len(products), 0)

    def _principal(self, db, role):
        self._add_user_identity_membership(db, "user_test", "subject_test", role=role)
        principal = principal_from_verified_claims(
            db,
            VerifiedIdentityClaims(issuer="test_issuer", subject="subject_test"),
            auth_source="fake_oidc_bearer",
        )
        self.assertIsNotNone(principal)
        return principal

    def _principal_without_membership(self, db):
        now = datetime.utcnow()
        db.add(
            models.User(
                id="user_no_membership",
                primary_email="nomembership@example.com",
                display_name="No Membership",
                status="active",
            )
        )
        db.add(
            models.OAuthIdentity(
                id="identity_no_membership",
                user_id="user_no_membership",
                provider="fake_oidc",
                issuer="test_issuer",
                subject="subject_no_membership",
                email="nomembership@example.com",
                email_verified=True,
                last_seen_at=now,
            )
        )
        db.commit()
        principal = principal_from_verified_claims(
            db,
            VerifiedIdentityClaims(issuer="test_issuer", subject="subject_no_membership"),
            auth_source="fake_oidc_bearer",
        )
        self.assertIsNotNone(principal)
        return principal

    def _add_user_identity_membership(self, db, user_id, subject, role):
        now = datetime.utcnow()
        db.add(
            models.User(
                id=user_id,
                primary_email=f"{user_id}@example.com",
                display_name=f"{role.title()} User",
                status="active",
            )
        )
        db.add(
            models.OAuthIdentity(
                id=f"identity_{user_id}",
                user_id=user_id,
                provider="fake_oidc",
                issuer="test_issuer",
                subject=subject,
                email=f"{user_id}@example.com",
                email_verified=True,
                last_seen_at=now,
            )
        )
        db.add(
            models.AccountMembership(
                id=f"membership_{user_id}",
                account_id="account_demo",
                user_id=user_id,
                role=role,
                status="active",
            )
        )
        db.commit()

    def _add_extra_scope_records(self, db):
        db.add(
            models.Account(
                id="account_other",
                email="other@example.com",
                name="Other Account",
                role="homeowner",
                subscription_status="active",
                plan_type="demo",
            )
        )
        db.add(
            models.Home(
                id="home_other",
                account_id="account_other",
                name="Other Home",
                address_line_1="2 Other St",
                city="Other",
                state="CA",
                postal_code="90002",
                country="US",
            )
        )
        db.add(
            models.Home(
                id="home_null",
                account_id=None,
                name="Unassigned Home",
                address_line_1="3 Null St",
                city="Nowhere",
                state="CA",
                postal_code="90003",
                country="US",
            )
        )
        db.add(
            models.EnergySystemDesign(
                id="design_other",
                home_id="home_other",
                name="Other Design",
                design_goal="partial_backup",
                architecture_type="ac_coupled",
                status="draft",
            )
        )
        db.add(
            models.EnergySystemDesign(
                id="design_null",
                home_id="home_null",
                name="Null Home Design",
                design_goal="partial_backup",
                architecture_type="ac_coupled",
                status="draft",
            )
        )
        db.add(
            models.Scenario(
                id="scenario_other",
                home_id="home_other",
                name="Other Scenario",
                description="Other account scenario.",
                linked_design_id="design_other",
            )
        )
        db.add(
            models.Scenario(
                id="scenario_null",
                home_id="home_null",
                name="Null Home Scenario",
                description="Unassigned home scenario.",
                linked_design_id="design_null",
            )
        )
        db.commit()


if __name__ == "__main__":
    unittest.main()

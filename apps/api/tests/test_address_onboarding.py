import unittest
from datetime import datetime

from tests.fast_db import reset_and_reseed  # noqa: E402  must precede app imports

from fastapi import HTTPException  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

from app.core import models  # noqa: E402
from app.core.database import engine  # noqa: E402
from app.main import app  # noqa: E402
from app.onboarding import router as onboarding_router  # noqa: E402
from app.onboarding.schemas import AddressOnboardingRequest  # noqa: E402
from app.security.principal import VerifiedIdentityClaims, principal_from_verified_claims  # noqa: E402


class AddressOnboardingTests(unittest.TestCase):
    def setUp(self):
        reset_and_reseed()
        with Session(engine) as db:
            db.query(models.AuditEvent).delete()
            db.query(models.DataProvenance).filter(models.DataProvenance.id.like("prov_address_%")).delete(
                synchronize_session=False
            )
            self._ensure_other_account(db)
            db.commit()

    def test_onboarding_route_is_mounted_under_api_prefix(self):
        paths = set(app.openapi()["paths"])

        self.assertIn("/api/onboarding/address", paths)

    def test_member_can_create_home_with_non_null_account_and_address_provenance(self):
        with Session(engine) as db:
            principal = self._principal(db, "member")
            response = onboarding_router.onboard_address(self._payload(), db, principal)

            home = db.get(models.Home, response.home_id)
            provenance_rows = db.query(models.DataProvenance).filter_by(
                entity_type="home",
                entity_id=response.home_id,
            ).all()
            audit_event = db.query(models.AuditEvent).filter_by(action="onboarding.home.created").first()

        self.assertEqual("created", response.status)
        self.assertEqual("address_recorded", response.readiness_state)
        self.assertEqual("/", response.next_route)
        self.assertEqual("account_demo", response.account_id)
        self.assertIsNotNone(home)
        self.assertEqual("account_demo", home.account_id)
        self.assertEqual("456 New Street", home.address_line_1)
        self.assertEqual("CA", home.state)
        self.assertEqual("US", home.country)
        self.assertIn("address_line_1", {row.field_name for row in provenance_rows})
        self.assertIn("postal_code", {row.field_name for row in provenance_rows})
        self.assertTrue(all(row.value_snapshot is None for row in provenance_rows))
        self.assertIsNotNone(audit_event)
        self.assertEqual("user_member_account_demo", audit_event.actor_user_id)
        self.assertEqual("account_demo", audit_event.account_id)
        self.assertEqual(response.home_id, audit_event.home_id)
        self.assertEqual("address_onboarding", audit_event.source_surface)
        self.assertNotIn("456 New Street", str(audit_event.event_context))

    def test_owner_and_admin_can_create_home(self):
        for role in ("owner", "admin"):
            with self.subTest(role=role):
                reset_and_reseed()
                with Session(engine) as db:
                    db.query(models.AuditEvent).delete()
                    self._ensure_other_account(db)
                    principal = self._principal(db, role)

                    response = onboarding_router.onboard_address(
                        self._payload(address_line_1=f"{role.title()} Created Street"),
                        db,
                        principal,
                    )

                self.assertEqual("created", response.status)
                self.assertEqual("account_demo", response.account_id)

    def test_viewer_and_no_membership_cannot_create_home(self):
        with Session(engine) as db:
            viewer = self._principal(db, "viewer")
            with self.assertRaises(HTTPException) as viewer_error:
                onboarding_router.onboard_address(self._payload(), db, viewer)
            viewer_audit = db.query(models.AuditEvent).filter_by(action="onboarding.address.denied").first()

        self.assertEqual(403, viewer_error.exception.status_code)
        self.assertIsNotNone(viewer_audit)
        self.assertEqual("denied", viewer_audit.decision)

        with Session(engine) as db:
            no_membership = self._principal_without_membership(db)
            with self.assertRaises(HTTPException) as no_membership_error:
                onboarding_router.onboard_address(self._payload(), db, no_membership)

        self.assertEqual(403, no_membership_error.exception.status_code)

    def test_multiple_writable_accounts_require_explicit_account_id(self):
        with Session(engine) as db:
            principal = self._principal(db, "member", extra_account_ids={"account_other"})

            with self.assertRaises(HTTPException) as error:
                onboarding_router.onboard_address(self._payload(), db, principal)

            response = onboarding_router.onboard_address(
                self._payload(account_id="account_other", address_line_1="789 Explicit Account Way"),
                db,
                principal,
            )

        self.assertEqual(400, error.exception.status_code)
        self.assertEqual("created", response.status)
        self.assertEqual("account_other", response.account_id)

    def test_cross_account_account_id_is_denied(self):
        with Session(engine) as db:
            principal = self._principal(db, "member")

            with self.assertRaises(HTTPException) as error:
                onboarding_router.onboard_address(self._payload(account_id="account_other"), db, principal)

        self.assertEqual(403, error.exception.status_code)

    def test_exact_normalized_match_returns_existing_home_in_same_account_only(self):
        with Session(engine) as db:
            principal = self._principal(db, "member")
            self._add_other_account_same_address(db)

            existing = onboarding_router.onboard_address(
                AddressOnboardingRequest(
                    name="Existing Match",
                    address_line_1=" 123   placeholder lane ",
                    city="placerville",
                    state=" ca ",
                    postal_code="95667",
                    country="us",
                ),
                db,
                principal,
            )
            created = onboarding_router.onboard_address(
                self._payload(address_line_1="999 Account Scoped Match Rd"),
                db,
                principal,
            )

        self.assertEqual("existing_home_found", existing.status)
        self.assertEqual("home_001", existing.home_id)
        self.assertEqual("created", created.status)
        self.assertNotEqual("home_other_same_address", created.home_id)

    def test_created_home_is_visible_to_same_account_and_hidden_from_other_account(self):
        with Session(engine) as db:
            demo_principal = self._principal(db, "member")
            response = onboarding_router.onboard_address(self._payload(), db, demo_principal)

        with Session(engine) as db:
            refreshed_demo_principal = self._principal(db, "member")
            other_principal = self._principal(db, "member", account_id="account_other")
            demo_home_ids = {home.id for home in self._visible_homes(db, refreshed_demo_principal)}
            other_home_ids = {home.id for home in self._visible_homes(db, other_principal)}

        self.assertIn(response.home_id, demo_home_ids)
        self.assertNotIn(response.home_id, other_home_ids)

    def _visible_homes(self, db, principal):
        from app.homes.router import list_homes

        return list_homes(db=db, principal=principal)

    def _payload(self, **overrides):
        data = {
            "name": "New Onboarding Home",
            "address_line_1": "456   New Street",
            "city": "Sacramento",
            "state": " ca ",
            "postal_code": " 95814 ",
            "country": " us ",
        }
        data.update(overrides)
        return AddressOnboardingRequest(**data)

    def _principal(self, db, role, account_id="account_demo", extra_account_ids=None):
        user_id = f"user_{role}_{account_id}"
        subject = f"subject_{role}_{account_id}"
        self._add_user_identity_membership(db, user_id, subject, role, account_id)
        for extra_account_id in extra_account_ids or set():
            self._add_membership(db, user_id, role, extra_account_id)
        principal = principal_from_verified_claims(
            db,
            VerifiedIdentityClaims(issuer="test_issuer", subject=subject),
            auth_source="fake_oidc_bearer",
        )
        self.assertIsNotNone(principal)
        return principal

    def _principal_without_membership(self, db):
        now = datetime.utcnow()
        db.add(
            models.User(
                id="user_no_onboarding_membership",
                primary_email="user_no_onboarding_membership@example.com",
                display_name="No Onboarding Membership",
                status="active",
            )
        )
        db.add(
            models.OAuthIdentity(
                id="identity_user_no_onboarding_membership",
                user_id="user_no_onboarding_membership",
                provider="fake_oidc",
                issuer="test_issuer",
                subject="subject_no_onboarding_membership",
                email="user_no_onboarding_membership@example.com",
                email_verified=True,
                last_seen_at=now,
            )
        )
        db.commit()
        principal = principal_from_verified_claims(
            db,
            VerifiedIdentityClaims(issuer="test_issuer", subject="subject_no_onboarding_membership"),
            auth_source="fake_oidc_bearer",
        )
        self.assertIsNotNone(principal)
        return principal

    def _add_user_identity_membership(self, db, user_id, subject, role, account_id):
        now = datetime.utcnow()
        if db.get(models.User, user_id) is None:
            db.add(
                models.User(
                    id=user_id,
                    primary_email=f"{user_id}@example.com",
                    display_name=f"{role.title()} User",
                    status="active",
                )
            )
        if db.get(models.OAuthIdentity, f"identity_{user_id}") is None:
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
        self._add_membership(db, user_id, role, account_id)
        db.commit()

    def _add_membership(self, db, user_id, role, account_id):
        membership_id = f"membership_{user_id}_{account_id}"
        if db.get(models.AccountMembership, membership_id) is None:
            db.add(
                models.AccountMembership(
                    id=membership_id,
                    account_id=account_id,
                    user_id=user_id,
                    role=role,
                    status="active",
                )
            )

    def _ensure_other_account(self, db):
        if db.get(models.Account, "account_other") is None:
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

    def _add_other_account_same_address(self, db):
        if db.get(models.Home, "home_other_same_address") is None:
            db.add(
                models.Home(
                    id="home_other_same_address",
                    account_id="account_other",
                    name="Other Account Same Address",
                    address_line_1="999 Account Scoped Match Rd",
                    city="Sacramento",
                    state="CA",
                    postal_code="95814",
                    country="US",
                )
            )
            db.commit()


if __name__ == "__main__":
    unittest.main()

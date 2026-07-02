import unittest
from datetime import datetime
from types import SimpleNamespace

from fastapi import HTTPException  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

import tests.fast_db  # noqa: F401, E402
from app.auth.router import current_principal, get_me  # noqa: E402
from app.core import models  # noqa: E402
from app.core.config import Settings  # noqa: E402
from app.core.database import engine  # noqa: E402
from app.main import app  # noqa: E402
from app.security.principal import (  # noqa: E402
    VerifiedIdentityClaims,
    fake_verified_claims_from_authorization,
    principal_from_verified_claims,
)


class AuthFoundationTests(unittest.TestCase):
    def setUp(self):
        with Session(engine) as db:
            db.query(models.AccountMembership).delete()
            db.query(models.OAuthIdentity).delete()
            db.query(models.User).delete()
            db.commit()

    def test_auth_models_can_link_user_identity_and_account_membership(self):
        with Session(engine) as db:
            user = self._create_user_graph(db)

            persisted = db.get(models.User, user.id)
            self.assertEqual("test@example.com", persisted.primary_email)
            self.assertEqual("active", persisted.status)
            self.assertEqual(1, len(persisted.oauth_identities))
            self.assertEqual(1, len(persisted.account_memberships))
            self.assertEqual("account_demo", persisted.account_memberships[0].account_id)

    def test_fake_verified_identity_maps_to_app_owned_principal(self):
        with Session(engine) as db:
            self._create_user_graph(db)

            principal = principal_from_verified_claims(
                db,
                VerifiedIdentityClaims(
                    issuer="test_issuer",
                    subject="subject_123",
                    email="test@example.com",
                    email_verified=True,
                ),
                auth_source="fake_oidc_bearer",
            )

            self.assertIsNotNone(principal)
            self.assertEqual("user_test", principal.user_id)
            self.assertEqual({"account_demo"}, principal.account_ids)
            self.assertIn("home_001", principal.allowed_home_ids)
            self.assertEqual("fake_oidc_bearer", principal.auth_source)
            self.assertIn("OAuth provider identity proves authentication only.", principal.limitations)

    def test_fake_bearer_claim_adapter_parses_test_only_token_shape(self):
        claims = fake_verified_claims_from_authorization(
            "Bearer fake-oidc:test_issuer|subject_123|test@example.com|true"
        )

        self.assertIsNotNone(claims)
        self.assertEqual("test_issuer", claims.issuer)
        self.assertEqual("subject_123", claims.subject)
        self.assertEqual("test@example.com", claims.email)
        self.assertTrue(claims.email_verified)

    def test_auth_me_uses_internal_principal_from_fake_verified_identity(self):
        with Session(engine) as db:
            self._create_user_graph(db)
            request = SimpleNamespace(
                headers={"authorization": "Bearer fake-oidc:test_issuer|subject_123|test@example.com|true"}
            )

            principal = current_principal(request, db)
            response = get_me(principal)

            self.assertEqual("user_test", response.user_id)
            self.assertEqual("fake_oidc_bearer", response.auth_source)
            self.assertEqual("identity_test", response.identity.identity_id)
            self.assertEqual(["account_demo"], response.account_ids)
            self.assertIn("home_001", response.authorized_home_ids)

    def test_auth_me_route_is_mounted_under_api_prefix(self):
        paths = set(app.openapi()["paths"])

        self.assertIn("/api/auth/me", paths)

    def test_auth_me_rejects_unknown_identity(self):
        with Session(engine) as db:
            request = SimpleNamespace(
                headers={"authorization": "Bearer fake-oidc:test_issuer|missing_subject|missing@example.com|true"}
            )

            with self.assertRaises(HTTPException) as error:
                current_principal(request, db)

            self.assertEqual(401, error.exception.status_code)

    def test_scaffold_headers_are_disabled_outside_local_or_test(self):
        production_settings = Settings(app_env="production", auth_allow_scaffold_headers=True)
        local_disabled_settings = Settings(app_env="local", auth_allow_scaffold_headers=False)
        test_enabled_settings = Settings(app_env="test", auth_allow_scaffold_headers=True)

        self.assertFalse(production_settings.should_allow_scaffold_auth_headers)
        self.assertFalse(local_disabled_settings.should_allow_scaffold_auth_headers)
        self.assertTrue(test_enabled_settings.should_allow_scaffold_auth_headers)

    def _create_user_graph(self, db):
        now = datetime.utcnow()
        user = models.User(
            id="user_test",
            primary_email="test@example.com",
            display_name="Test User",
            status="active",
        )
        db.add(user)
        db.add(
            models.OAuthIdentity(
                id="identity_test",
                user_id=user.id,
                provider="fake_oidc",
                issuer="test_issuer",
                subject="subject_123",
                email="test@example.com",
                email_verified=True,
                claims_snapshot={"purpose": "test_identity_proof_only"},
                last_seen_at=now,
            )
        )
        db.add(
            models.AccountMembership(
                id="membership_test",
                account_id="account_demo",
                user_id=user.id,
                role="owner",
                status="active",
            )
        )
        db.commit()
        return user


if __name__ == "__main__":
    unittest.main()

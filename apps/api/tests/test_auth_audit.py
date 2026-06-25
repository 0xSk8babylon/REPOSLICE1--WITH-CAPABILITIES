import unittest
from datetime import datetime
from types import SimpleNamespace

import tests.fast_db  # noqa: F401, E402

from starlette.responses import Response  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

from app.core import models  # noqa: E402
from app.core.database import engine  # noqa: E402
from app.main import app  # noqa: E402
from app.security.auth import HomeAccessMiddleware  # noqa: E402


HOME_ID = "home_001"


class AuthAuditTests(unittest.TestCase):
    def setUp(self):
        with Session(engine) as db:
            db.query(models.AuditEvent).delete()
            db.commit()
        self.middleware = HomeAccessMiddleware(app)

    def test_home_data_route_requires_authentication(self):
        response = self._dispatch(f"/api/homes/{HOME_ID}/facts")

        self.assertEqual(401, response.status_code)
        self._assert_audit(status_code=401, authorized="false", home_id=HOME_ID, decision="not_authenticated")

    def test_home_data_route_blocks_cross_home_access(self):
        response = self._dispatch(
            f"/api/homes/{HOME_ID}/facts",
            headers={"x-user-id": "user_a", "x-home-access": "other_home"},
        )

        self.assertEqual(403, response.status_code)
        self._assert_audit(status_code=403, authorized="false", home_id=HOME_ID, decision="denied")

    def test_authorized_home_access_succeeds_and_is_audited(self):
        response = self._dispatch(
            f"/api/homes/{HOME_ID}/facts",
            headers={"x-user-id": "user_a", "x-home-access": HOME_ID},
        )

        self.assertEqual(200, response.status_code)
        event = self._assert_audit(status_code=200, authorized="true", home_id=HOME_ID, decision="allowed")
        self.assertEqual("local_test_headers", event.auth_source)
        self.assertIsNone(event.actor_user_id)
        self.assertIsNone(event.actor_identity_id)
        self.assertEqual("middleware", event.source_surface)
        self.assertEqual("home", event.object_type)
        self.assertEqual(HOME_ID, event.object_id)
        self.assertEqual("/api/homes/{home_id}/facts", event.route_template)
        self.assertEqual({"auth_boundary": "home_access_middleware"}, event.event_context)

    def test_fake_oidc_actor_fields_are_populated_from_app_principal(self):
        self._create_user_graph()

        response = self._dispatch(
            f"/api/homes/{HOME_ID}/facts",
            headers={"authorization": "Bearer fake-oidc:audit_issuer|audit_subject|audit@example.com|true"},
        )

        self.assertEqual(200, response.status_code)
        event = self._assert_audit(status_code=200, authorized="true", home_id=HOME_ID, decision="allowed")
        self.assertEqual("user_audit", event.user_id)
        self.assertEqual("user_audit", event.actor_user_id)
        self.assertEqual("identity_audit", event.actor_identity_id)
        self.assertEqual("fake_oidc_bearer", event.auth_source)
        self.assertEqual("account_demo", event.account_id)

    def test_home_list_requires_authenticated_principal(self):
        response = self._dispatch("/api/homes/all")

        self.assertEqual(401, response.status_code)
        self._assert_audit(status_code=401, authorized="false", home_id=None, decision="not_authenticated")

    def test_scaffold_headers_are_rejected_when_disabled(self):
        from app.security.auth import settings

        original = settings.auth_allow_scaffold_headers
        settings.auth_allow_scaffold_headers = False
        try:
            response = self._dispatch(
                f"/api/homes/{HOME_ID}/facts",
                headers={"x-user-id": "user_a", "x-home-access": HOME_ID},
            )
        finally:
            settings.auth_allow_scaffold_headers = original

        self.assertEqual(401, response.status_code)
        self._assert_audit(status_code=401, authorized="false", home_id=HOME_ID, decision="not_authenticated")

    def test_legacy_audit_rows_load_with_nullable_trust_fields(self):
        with Session(engine) as db:
            db.add(
                models.AuditEvent(
                    id="audit_legacy",
                    user_id="legacy_user",
                    home_id=HOME_ID,
                    action="legacy_action",
                    method="GET",
                    path="/legacy",
                    status_code=200,
                    authorized="true",
                    reason="legacy row",
                )
            )
            db.commit()

            event = db.get(models.AuditEvent, "audit_legacy")

        self.assertEqual("legacy_user", event.user_id)
        self.assertIsNone(event.actor_user_id)
        self.assertIsNone(event.actor_identity_id)
        self.assertIsNone(event.event_context)

    def _dispatch(self, path, headers=None):
        import asyncio

        request = SimpleNamespace(
            url=SimpleNamespace(path=path),
            method="GET",
            headers=headers or {},
            query_params={},
        )

        async def call_next(_request):
            return Response(status_code=200)

        return asyncio.run(self.middleware.dispatch(request, call_next))

    def _assert_audit(self, status_code, authorized, home_id, decision=None):
        with Session(engine) as db:
            event = db.query(models.AuditEvent).order_by(models.AuditEvent.created_at.desc()).first()
            self.assertIsNotNone(event)
            self.assertEqual(status_code, event.status_code)
            self.assertEqual(authorized, event.authorized)
            self.assertEqual(home_id, event.home_id)
            if decision is not None:
                self.assertEqual(decision, event.decision)
            return event

    def _create_user_graph(self):
        now = datetime.utcnow()
        with Session(engine) as db:
            if db.get(models.User, "user_audit") is None:
                db.add(
                    models.User(
                        id="user_audit",
                        primary_email="audit@example.com",
                        display_name="Audit User",
                        status="active",
                    )
                )
            if db.get(models.OAuthIdentity, "identity_audit") is None:
                db.add(
                    models.OAuthIdentity(
                        id="identity_audit",
                        user_id="user_audit",
                        provider="fake_oidc",
                        issuer="audit_issuer",
                        subject="audit_subject",
                        email="audit@example.com",
                        email_verified=True,
                        last_seen_at=now,
                    )
                )
            if db.get(models.AccountMembership, "membership_audit") is None:
                db.add(
                    models.AccountMembership(
                        id="membership_audit",
                        account_id="account_demo",
                        user_id="user_audit",
                        role="owner",
                        status="active",
                    )
                )
            db.commit()


if __name__ == "__main__":
    unittest.main()

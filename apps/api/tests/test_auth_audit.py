import unittest
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
        self._assert_audit(status_code=401, authorized="false", home_id=HOME_ID)

    def test_home_data_route_blocks_cross_home_access(self):
        response = self._dispatch(
            f"/api/homes/{HOME_ID}/facts",
            headers={"x-user-id": "user_a", "x-home-access": "other_home"},
        )

        self.assertEqual(403, response.status_code)
        self._assert_audit(status_code=403, authorized="false", home_id=HOME_ID)

    def test_authorized_home_access_succeeds_and_is_audited(self):
        response = self._dispatch(
            f"/api/homes/{HOME_ID}/facts",
            headers={"x-user-id": "user_a", "x-home-access": HOME_ID},
        )

        self.assertEqual(200, response.status_code)
        self._assert_audit(status_code=200, authorized="true", home_id=HOME_ID)

    def test_home_list_requires_authenticated_principal(self):
        response = self._dispatch("/api/homes/all")

        self.assertEqual(401, response.status_code)
        self._assert_audit(status_code=401, authorized="false", home_id=None)

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

    def _assert_audit(self, status_code, authorized, home_id):
        with Session(engine) as db:
            event = db.query(models.AuditEvent).order_by(models.AuditEvent.created_at.desc()).first()
            self.assertIsNotNone(event)
            self.assertEqual(status_code, event.status_code)
            self.assertEqual(authorized, event.authorized)
            self.assertEqual(home_id, event.home_id)


if __name__ == "__main__":
    unittest.main()

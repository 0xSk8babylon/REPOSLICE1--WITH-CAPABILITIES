import re
import uuid
from dataclasses import dataclass
from typing import Optional, Set

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core import models
from app.core.database import SessionLocal


HOME_PATH_PATTERNS = (
    re.compile(r"^/api/homes/([^/?]+)"),
    re.compile(r"^/api/[^/]+/homes/([^/?]+)"),
    re.compile(r"^/api/twin-planning-context/homes/([^/?]+)"),
)

HOME_DATA_PREFIXES = (
    "/api/homes",
    "/api/buildings",
    "/api/panels",
    "/api/loads",
    "/api/designs",
    "/api/scenarios",
    "/api/equipment",
    "/api/estimated-pathways",
    "/api/takeoffs",
    "/api/planning-exchange",
    "/api/twin-planning-context",
    "/api/estimate-readiness",
    "/api/proposal-option-sets",
    "/api/contractor-workflow",
    "/api/product-preferences",
    "/api/post-install",
    "/api/crm-handoff",
    "/api/energy-passport",
    "/api/program-intelligence",
)


@dataclass(frozen=True)
class Principal:
    user_id: str
    allowed_home_ids: Set[str]


class HomeAccessMiddleware(BaseHTTPMiddleware):
    """Header-based local auth boundary for home data routes.

    This is intentionally provider-free. A future auth provider can populate
    the same request headers or replace this middleware behind the same object
    access checks.
    """

    async def dispatch(self, request, call_next):
        path = request.url.path
        if not self._is_home_data_path(path):
            return await call_next(request)

        principal = self._principal_from_headers(request)
        home_id = self._extract_home_id(path) or request.query_params.get("home_id")
        if principal is None:
            self._write_audit(None, home_id, request.method, path, 401, False, "missing principal")
            return JSONResponse(status_code=401, content={"detail": "Authentication required"})
        if home_id and "*" not in principal.allowed_home_ids and home_id not in principal.allowed_home_ids:
            self._write_audit(principal.user_id, home_id, request.method, path, 403, False, "home access denied")
            return JSONResponse(status_code=403, content={"detail": "Home access denied"})

        response = await call_next(request)
        self._write_audit(principal.user_id, home_id, request.method, path, response.status_code, True, "authorized")
        return response

    def _is_home_data_path(self, path: str) -> bool:
        return any(path == prefix or path.startswith(f"{prefix}/") for prefix in HOME_DATA_PREFIXES)

    def _extract_home_id(self, path: str) -> Optional[str]:
        for pattern in HOME_PATH_PATTERNS:
            match = pattern.match(path)
            if match and match.group(1) != "all":
                return match.group(1)
        return None

    def _principal_from_headers(self, request) -> Optional[Principal]:
        user_id = request.headers.get("x-user-id")
        if not user_id:
            return None
        raw_home_access = request.headers.get("x-home-access", "")
        allowed = {item.strip() for item in raw_home_access.split(",") if item.strip()}
        return Principal(user_id=user_id, allowed_home_ids=allowed)

    def _write_audit(
        self,
        user_id: Optional[str],
        home_id: Optional[str],
        method: str,
        path: str,
        status_code: int,
        authorized: bool,
        reason: str,
    ) -> None:
        db = SessionLocal()
        try:
            db.add(
                models.AuditEvent(
                    id=f"audit_{uuid.uuid4().hex}",
                    user_id=user_id,
                    home_id=home_id,
                    action="home_data_access",
                    method=method,
                    path=path,
                    status_code=status_code,
                    authorized=str(authorized).lower(),
                    reason=reason,
                )
            )
            db.commit()
        finally:
            db.close()

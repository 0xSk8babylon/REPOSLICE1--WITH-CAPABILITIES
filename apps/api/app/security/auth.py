import re
import uuid
from typing import Optional

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core import models
from app.core.config import settings
from app.core.database import SessionLocal
from app.security.principal import (
    AuthPrincipal,
    fake_verified_claims_from_authorization,
    principal_from_verified_claims,
    scaffold_principal_from_headers,
)


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
    "/api/privacy",
    "/api/evidence",
)


class HomeAccessMiddleware(BaseHTTPMiddleware):
    """Provider-neutral auth boundary for home data routes."""

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

    def _principal_from_headers(self, request) -> Optional[AuthPrincipal]:
        if settings.should_allow_fake_oidc_tokens:
            claims = fake_verified_claims_from_authorization(request.headers.get("authorization"))
            if claims is not None:
                db = SessionLocal()
                try:
                    return principal_from_verified_claims(db, claims, auth_source="fake_oidc_bearer")
                finally:
                    db.close()

        if not settings.should_allow_scaffold_auth_headers:
            return None
        return scaffold_principal_from_headers(
            user_id=request.headers.get("x-user-id"),
            raw_home_access=request.headers.get("x-home-access", ""),
        )

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

import uuid
from typing import Any, Optional

from sqlalchemy.orm import Session

from app.core import models
from app.core.database import SessionLocal
from app.security.principal import AuthPrincipal


LOCAL_TEST_AUTH_SOURCE = "local_test_headers"
SENSITIVE_CONTEXT_KEYS = {
    "authorization",
    "bearer",
    "claims",
    "cookie",
    "id_token",
    "password",
    "raw_claims",
    "refresh_token",
    "secret",
    "token",
}


class AuditService:
    def record(
        self,
        db: Session,
        *,
        action: str,
        method: str,
        path: str,
        status_code: int,
        authorized: bool,
        reason: str,
        principal: Optional[AuthPrincipal] = None,
        user_id: Optional[str] = None,
        home_id: Optional[str] = None,
        account_id: Optional[str] = None,
        object_type: Optional[str] = None,
        object_id: Optional[str] = None,
        route_template: Optional[str] = None,
        source_surface: Optional[str] = None,
        decision: Optional[str] = None,
        request_id: Optional[str] = None,
        event_context: Optional[dict] = None,
        provenance_refs: Optional[list] = None,
        commit: bool = True,
    ) -> models.AuditEvent:
        event = models.AuditEvent(
            id=f"audit_{uuid.uuid4().hex}",
            user_id=user_id or (principal.user_id if principal is not None else None),
            home_id=home_id,
            actor_user_id=self._actor_user_id(principal),
            actor_identity_id=principal.identity_id if principal is not None else None,
            auth_source=principal.auth_source if principal is not None else None,
            account_id=account_id or self._account_id_for_home(db, home_id),
            object_type=object_type,
            object_id=object_id,
            route_template=route_template,
            source_surface=source_surface,
            decision=decision or self._decision(principal, status_code, authorized),
            request_id=request_id,
            event_context=self._sanitize_context(event_context),
            provenance_refs=provenance_refs,
            action=action,
            method=method,
            path=path,
            status_code=status_code,
            authorized=str(authorized).lower(),
            reason=reason,
        )
        db.add(event)
        if commit:
            db.commit()
            db.refresh(event)
        return event

    def record_with_new_session(self, **kwargs) -> Optional[models.AuditEvent]:
        db = SessionLocal()
        try:
            return self.record(db, **kwargs)
        finally:
            db.close()

    def _actor_user_id(self, principal: Optional[AuthPrincipal]) -> Optional[str]:
        if principal is None:
            return None
        if principal.auth_source == LOCAL_TEST_AUTH_SOURCE and principal.identity_id is None:
            return None
        return principal.user_id

    def _account_id_for_home(self, db: Session, home_id: Optional[str]) -> Optional[str]:
        if not home_id:
            return None
        home = db.get(models.Home, home_id)
        return home.account_id if home is not None else None

    def _decision(self, principal: Optional[AuthPrincipal], status_code: int, authorized: bool) -> str:
        if principal is None or status_code == 401:
            return "not_authenticated"
        if status_code == 403 or not authorized:
            return "denied"
        return "allowed"

    def _sanitize_context(self, context: Optional[dict]) -> Optional[dict]:
        if context is None:
            return None
        sanitized = self._sanitize_value(context)
        return sanitized if isinstance(sanitized, dict) else None

    def _sanitize_value(self, value: Any) -> Any:
        if isinstance(value, dict):
            clean = {}
            for key, item in value.items():
                key_text = str(key)
                if any(sensitive in key_text.lower() for sensitive in SENSITIVE_CONTEXT_KEYS):
                    clean[key_text] = "[redacted]"
                else:
                    clean[key_text] = self._sanitize_value(item)
            return clean
        if isinstance(value, list):
            return [self._sanitize_value(item) for item in value]
        if isinstance(value, tuple):
            return [self._sanitize_value(item) for item in value]
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        return str(value)


audit_service = AuditService()

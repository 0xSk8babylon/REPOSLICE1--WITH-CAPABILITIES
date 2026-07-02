import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Set

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core import models

FAKE_OIDC_PREFIX = "fake-oidc:"
READ_MEMBERSHIP_ROLES = {"owner", "admin", "member", "viewer"}


@dataclass(frozen=True)
class VerifiedIdentityClaims:
    issuer: str
    subject: str
    provider: str = "fake_oidc"
    email: Optional[str] = None
    email_verified: bool = False


@dataclass(frozen=True)
class AuthPrincipal:
    user_id: str
    allowed_home_ids: Set[str]
    auth_source: str
    identity_id: Optional[str] = None
    provider: Optional[str] = None
    issuer: Optional[str] = None
    subject: Optional[str] = None
    account_ids: Set[str] = field(default_factory=set)
    account_roles: Dict[str, str] = field(default_factory=dict)
    limitations: List[str] = field(default_factory=list)


def fake_verified_claims_from_authorization(authorization: Optional[str]) -> Optional[VerifiedIdentityClaims]:
    if not authorization:
        return None
    prefix = "Bearer "
    if not authorization.startswith(prefix):
        return None
    token = authorization[len(prefix) :].strip()
    if not token.startswith(FAKE_OIDC_PREFIX):
        return None

    parts = token[len(FAKE_OIDC_PREFIX) :].split("|")
    if len(parts) < 2:
        return None
    issuer, subject = parts[0].strip(), parts[1].strip()
    if not issuer or not subject or not _safe_fake_claim(issuer) or not _safe_fake_claim(subject):
        return None
    email = parts[2].strip() if len(parts) > 2 and parts[2].strip() else None
    email_verified = len(parts) > 3 and parts[3].strip().lower() == "true"
    return VerifiedIdentityClaims(
        issuer=issuer,
        subject=subject,
        email=email,
        email_verified=email_verified,
    )


def principal_from_verified_claims(
    db: Session,
    claims: VerifiedIdentityClaims,
    auth_source: str = "oidc_bearer_jwt",
) -> Optional[AuthPrincipal]:
    identity = db.scalars(
        select(models.OAuthIdentity).where(
            models.OAuthIdentity.issuer == claims.issuer,
            models.OAuthIdentity.subject == claims.subject,
        )
    ).first()
    if identity is None:
        return None

    identity.last_seen_at = datetime.utcnow()
    db.add(identity)
    db.commit()

    memberships = db.scalars(
        select(models.AccountMembership).where(
            models.AccountMembership.user_id == identity.user_id,
            models.AccountMembership.status == "active",
        )
    ).all()
    readable_memberships = [
        membership for membership in memberships if membership.role in READ_MEMBERSHIP_ROLES
    ]
    account_ids = {membership.account_id for membership in readable_memberships}
    account_roles = {membership.account_id: membership.role for membership in memberships}
    allowed_home_ids = _home_ids_for_accounts(db, account_ids)

    return AuthPrincipal(
        user_id=identity.user_id,
        identity_id=identity.id,
        provider=identity.provider,
        issuer=identity.issuer,
        subject=identity.subject,
        account_ids=account_ids,
        account_roles=account_roles,
        allowed_home_ids=allowed_home_ids,
        auth_source=auth_source,
        limitations=[
            "OAuth provider identity proves authentication only.",
            "Account and home authorization are derived from app-owned membership records.",
        ],
    )


def scaffold_principal_from_headers(user_id: Optional[str], raw_home_access: str) -> Optional[AuthPrincipal]:
    if not user_id:
        return None
    allowed = {item.strip() for item in raw_home_access.split(",") if item.strip()}
    return AuthPrincipal(
        user_id=user_id,
        allowed_home_ids=allowed,
        auth_source="local_test_headers",
        limitations=[
            "Local/test scaffold principal only.",
            "Do not use x-user-id or x-home-access as production authentication.",
        ],
    )


def _home_ids_for_accounts(db: Session, account_ids: Set[str]) -> Set[str]:
    if not account_ids:
        return set()
    rows = db.scalars(select(models.Home.id).where(models.Home.account_id.in_(account_ids))).all()
    return set(rows)


def _safe_fake_claim(value: str) -> bool:
    return re.fullmatch(r"[A-Za-z0-9_.@/-]+", value) is not None

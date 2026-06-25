from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.auth.schemas import AuthIdentitySummary, AuthMeResponse
from app.core.config import settings
from app.core.database import get_db
from app.security.principal import (
    fake_verified_claims_from_authorization,
    principal_from_verified_claims,
    scaffold_principal_from_headers,
)

router = APIRouter(prefix="/auth", tags=["auth"])


def current_principal(request: Request, db: Session = Depends(get_db)):
    if settings.should_allow_fake_oidc_tokens:
        claims = fake_verified_claims_from_authorization(request.headers.get("authorization"))
        if claims is not None:
            principal = principal_from_verified_claims(db, claims, auth_source="fake_oidc_bearer")
            if principal is not None:
                return principal

    if settings.should_allow_scaffold_auth_headers:
        principal = scaffold_principal_from_headers(
            user_id=request.headers.get("x-user-id"),
            raw_home_access=request.headers.get("x-home-access", ""),
        )
        if principal is not None:
            return principal

    raise HTTPException(status_code=401, detail="Authentication required")


@router.get("/me", response_model=AuthMeResponse)
def get_me(principal=Depends(current_principal)):
    return AuthMeResponse(
        user_id=principal.user_id,
        auth_source=principal.auth_source,
        identity=AuthIdentitySummary(
            identity_id=principal.identity_id,
            provider=principal.provider,
            issuer=principal.issuer,
            subject=principal.subject,
        ),
        account_ids=sorted(principal.account_ids),
        authorized_home_ids=sorted(principal.allowed_home_ids),
        limitations=principal.limitations,
    )

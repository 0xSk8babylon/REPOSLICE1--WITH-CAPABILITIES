from typing import List, Optional

from app.core.schemas import ORMModel


class AuthIdentitySummary(ORMModel):
    identity_id: Optional[str] = None
    provider: Optional[str] = None
    issuer: Optional[str] = None
    subject: Optional[str] = None


class AuthMeResponse(ORMModel):
    user_id: str
    auth_source: str
    identity: AuthIdentitySummary
    account_ids: List[str]
    authorized_home_ids: List[str]
    limitations: List[str]

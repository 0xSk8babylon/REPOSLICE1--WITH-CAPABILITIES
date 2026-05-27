from datetime import datetime
from typing import Optional

from pydantic import Field

from app.core.schemas import ORMModel, PermissionReadinessMetadata
from app.core.types import AccountRole, DataOrigin, PlanType, SubscriptionStatus


class AccountBase(ORMModel):
    email: str
    name: str
    role: AccountRole
    subscription_status: SubscriptionStatus
    plan_type: PlanType
    data_origin: DataOrigin = DataOrigin.user_created


class Account(AccountBase):
    id: str
    created_at: datetime
    updated_at: datetime
    permission_readiness: PermissionReadinessMetadata = Field(
        default_factory=lambda: PermissionReadinessMetadata(
            notes=[
                "Account role, plan, and subscription fields are scaffolding only.",
                "No RBAC, tenant isolation, subscription gating, or export authorization is enforced by these fields.",
            ]
        )
    )


class AccountCreate(AccountBase):
    id: str


class AccountUpdate(ORMModel):
    email: Optional[str] = None
    name: Optional[str] = None
    role: Optional[AccountRole] = None
    subscription_status: Optional[SubscriptionStatus] = None
    plan_type: Optional[PlanType] = None

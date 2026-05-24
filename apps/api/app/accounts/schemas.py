from datetime import datetime
from typing import Optional

from app.core.schemas import ORMModel
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


class AccountCreate(AccountBase):
    id: str


class AccountUpdate(ORMModel):
    email: Optional[str] = None
    name: Optional[str] = None
    role: Optional[AccountRole] = None
    subscription_status: Optional[SubscriptionStatus] = None
    plan_type: Optional[PlanType] = None

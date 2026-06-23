from typing import List

from pydantic import BaseModel, ConfigDict, Field

from app.core.types import ApiViewAudience, AuthorityLayer, DataClassification


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ViewBoundaryMetadata(ORMModel):
    view_name: str
    audience: ApiViewAudience
    authority_layer: AuthorityLayer
    trust_zone: str
    data_classification: DataClassification
    exposed_authority_layers: List[AuthorityLayer] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    excluded_capabilities: List[str] = Field(default_factory=list)
    permission_enforcement: str = "not_enforced"


class PermissionReadinessMetadata(ORMModel):
    account_scaffolding_only: bool = True
    role_enforcement: str = "not_enforced"
    tenant_isolation: str = "not_enforced"
    subscription_enforcement: str = "not_enforced"
    notes: List[str] = Field(default_factory=list)

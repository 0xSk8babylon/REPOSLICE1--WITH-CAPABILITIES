from typing import List, Literal, Optional

from pydantic import Field, field_validator

from app.core.schemas import ORMModel


class AddressOnboardingRequest(ORMModel):
    account_id: Optional[str] = None
    name: str = Field(min_length=1)
    address_line_1: str = Field(min_length=1)
    address_line_2: Optional[str] = None
    city: str = Field(min_length=1)
    state: str = Field(min_length=1)
    postal_code: str = Field(min_length=1)
    country: str = Field(default="US", min_length=1)

    @field_validator(
        "account_id",
        "name",
        "address_line_1",
        "address_line_2",
        "city",
        "state",
        "postal_code",
        "country",
        mode="before",
    )
    @classmethod
    def trim_string_fields(cls, value):
        if isinstance(value, str):
            trimmed = value.strip()
            return trimmed or None
        return value


class AddressOnboardingResponse(ORMModel):
    home_id: str
    account_id: str
    status: Literal["created", "existing_home_found"]
    readiness_state: Literal["address_recorded"] = "address_recorded"
    next_route: str
    next_steps: List[str]
    limitations: List[str]

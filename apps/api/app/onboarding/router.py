import re
import uuid
from typing import Dict, Iterable, Optional, Set

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.router import current_principal
from app.core import models
from app.core.database import get_db
from app.core.repository import repository
from app.core.types import ConfidenceLevel, FactLifecycleState, SourceDocumentType
from app.homes.schemas import HomeCreate
from app.onboarding.schemas import AddressOnboardingRequest, AddressOnboardingResponse
from app.provenance.schemas import DataProvenanceCreate
from app.security import permissions
from app.security.audit import audit_service


router = APIRouter(prefix="/onboarding", tags=["onboarding"])

ADDRESS_FIELD_NAMES = (
    "address_line_1",
    "address_line_2",
    "city",
    "state",
    "postal_code",
    "country",
)
NEXT_STEPS = [
    "Review service panel",
    "Add major loads",
    "Confirm utility provider",
]
LIMITATIONS = [
    "Address is user-entered and not externally verified.",
    "No geocoding, property enrichment, utility inference, climate inference, AHJ inference, or program inference was performed.",
]


@router.post("/address", response_model=AddressOnboardingResponse)
def onboard_address(
    payload: AddressOnboardingRequest,
    db: Session = Depends(get_db),
    principal=Depends(current_principal),
):
    normalized = _normalize_address(payload)
    try:
        account_id = _resolve_writable_account_id(principal, payload.account_id)
    except HTTPException as error:
        _audit_denied(db, principal, payload, error.detail, error.status_code)
        raise

    _audit_submit(db, principal, account_id, payload)
    existing_home = _find_existing_home_for_account(db, account_id, normalized)
    if existing_home is not None:
        _audit_resolved(db, principal, account_id, existing_home.id, payload)
        return _response(existing_home.id, account_id, "existing_home_found")

    home = repository.create_home(db, _home_create_payload(account_id, payload, normalized))
    _create_address_provenance(db, home.id, normalized)
    _audit_created(db, principal, account_id, home.id, payload)
    return _response(home.id, account_id, "created")


def _resolve_writable_account_id(principal, requested_account_id: Optional[str]) -> str:
    writable_account_ids = permissions.writable_account_ids(principal)
    if not writable_account_ids:
        raise HTTPException(status_code=403, detail="No writable account membership")
    if requested_account_id:
        permissions.require_allowed(
            requested_account_id in writable_account_ids,
            "Account is not writable by current principal",
        )
        return requested_account_id
    if len(writable_account_ids) > 1:
        raise HTTPException(status_code=400, detail="account_id is required when multiple writable accounts exist")
    return next(iter(writable_account_ids))


def _normalize_address(payload: AddressOnboardingRequest) -> Dict[str, Optional[str]]:
    return {
        "address_line_1": _collapse_space(payload.address_line_1),
        "address_line_2": _optional_collapsed(payload.address_line_2),
        "city": _collapse_space(payload.city),
        "state": _collapse_space(payload.state).upper(),
        "postal_code": _collapse_space(payload.postal_code),
        "country": _collapse_space(payload.country or "US").upper(),
    }


def _find_existing_home_for_account(db: Session, account_id: str, normalized: Dict[str, Optional[str]]):
    for home in repository.list_homes(db, account_ids={account_id}):
        if _home_address_key(home) == _address_key(normalized):
            return home
    return None


def _home_address_key(home: models.Home):
    return (
        _match_component(home.address_line_1),
        _match_component(home.address_line_2),
        _match_component(home.city),
        _match_component(home.state),
        _match_component(home.postal_code),
        _match_component(home.country),
    )


def _address_key(normalized: Dict[str, Optional[str]]):
    return tuple(_match_component(normalized[field]) for field in ADDRESS_FIELD_NAMES)


def _home_create_payload(account_id: str, payload: AddressOnboardingRequest, normalized: Dict[str, Optional[str]]):
    return HomeCreate(
        id=f"home_{uuid.uuid4().hex}",
        account_id=account_id,
        name=_collapse_space(payload.name),
        address_line_1=normalized["address_line_1"],
        address_line_2=normalized["address_line_2"],
        city=normalized["city"],
        state=normalized["state"],
        postal_code=normalized["postal_code"],
        country=normalized["country"],
        data_origin=FactLifecycleState.user_created,
    )


def _create_address_provenance(db: Session, home_id: str, normalized: Dict[str, Optional[str]]) -> None:
    for field_name in ADDRESS_FIELD_NAMES:
        if normalized.get(field_name) is None:
            continue
        repository.create_data_provenance(
            db,
            DataProvenanceCreate(
                id=f"prov_address_{field_name}_{uuid.uuid4().hex}",
                entity_type="home",
                entity_id=home_id,
                field_name=field_name,
                source_type=SourceDocumentType.user_entry,
                trust_state=FactLifecycleState.user_created,
                confidence_level=ConfidenceLevel.medium,
                notes="Address field was entered by the current app principal and was not externally verified.",
            ),
        )


def _audit_submit(db: Session, principal, account_id: str, payload: AddressOnboardingRequest) -> None:
    _record_audit(
        db,
        principal,
        action="onboarding.address.submit",
        account_id=account_id,
        status_code=200,
        authorized=True,
        reason="address onboarding submitted",
        event_context=_event_context(payload, account_resolution_mode="resolved"),
    )


def _audit_created(db: Session, principal, account_id: str, home_id: str, payload: AddressOnboardingRequest) -> None:
    _record_audit(
        db,
        principal,
        action="onboarding.home.created",
        account_id=account_id,
        home_id=home_id,
        status_code=201,
        authorized=True,
        reason="address onboarding created home",
        event_context=_event_context(payload, duplicate_resolution="created"),
    )


def _audit_resolved(db: Session, principal, account_id: str, home_id: str, payload: AddressOnboardingRequest) -> None:
    _record_audit(
        db,
        principal,
        action="onboarding.home.resolved",
        account_id=account_id,
        home_id=home_id,
        status_code=200,
        authorized=True,
        reason="address onboarding resolved existing home",
        event_context=_event_context(payload, duplicate_resolution="existing_home_found"),
    )


def _audit_denied(
    db: Session,
    principal,
    payload: AddressOnboardingRequest,
    reason: str,
    status_code: int,
) -> None:
    _record_audit(
        db,
        principal,
        action="onboarding.address.denied",
        account_id=payload.account_id,
        status_code=status_code,
        authorized=False,
        reason=reason,
        decision="denied",
        event_context=_event_context(payload, account_resolution_mode="denied"),
    )


def _record_audit(
    db: Session,
    principal,
    *,
    action: str,
    account_id: Optional[str],
    status_code: int,
    authorized: bool,
    reason: str,
    event_context: dict,
    home_id: Optional[str] = None,
    decision: Optional[str] = None,
) -> None:
    audit_service.record(
        db,
        action=action,
        method="POST",
        path="/api/onboarding/address",
        status_code=status_code,
        authorized=authorized,
        reason=reason,
        principal=principal,
        home_id=home_id,
        account_id=account_id,
        object_type="home",
        object_id=home_id,
        route_template="/api/onboarding/address",
        source_surface="address_onboarding",
        decision=decision,
        event_context=event_context,
    )


def _event_context(
    payload: AddressOnboardingRequest,
    *,
    account_resolution_mode: Optional[str] = None,
    duplicate_resolution: Optional[str] = None,
) -> dict:
    context = {
        "fields_present": sorted(_fields_present(payload)),
        "normalization_mode": "local_minimal",
    }
    if account_resolution_mode:
        context["account_resolution_mode"] = account_resolution_mode
    if duplicate_resolution:
        context["duplicate_resolution"] = duplicate_resolution
    return context


def _fields_present(payload: AddressOnboardingRequest) -> Iterable[str]:
    for field_name in ADDRESS_FIELD_NAMES:
        if getattr(payload, field_name) not in {None, ""}:
            yield field_name


def _response(home_id: str, account_id: str, status: str) -> AddressOnboardingResponse:
    return AddressOnboardingResponse(
        home_id=home_id,
        account_id=account_id,
        status=status,
        next_route="/",
        next_steps=NEXT_STEPS,
        limitations=LIMITATIONS,
    )


def _collapse_space(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def _optional_collapsed(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    collapsed = _collapse_space(value)
    return collapsed or None


def _match_component(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    return _collapse_space(value).casefold()

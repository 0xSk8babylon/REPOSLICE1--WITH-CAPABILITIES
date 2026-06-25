from typing import Iterable, Optional, Set

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core import models
from app.security.principal import AuthPrincipal


OWNER = "owner"
ADMIN = "admin"
MEMBER = "member"
VIEWER = "viewer"

READ_ROLES = {OWNER, ADMIN, MEMBER, VIEWER}
WRITE_ROLES = {OWNER, ADMIN, MEMBER}
OWNER_ROLES = {OWNER}

LOCAL_TEST_HEADER_SOURCE = "local_test_headers"


def account_role(principal: AuthPrincipal, account_id: Optional[str]) -> Optional[str]:
    if not account_id:
        return None
    return principal.account_roles.get(account_id)


def can_access_account(principal: AuthPrincipal, account_id: Optional[str]) -> bool:
    return account_role(principal, account_id) in READ_ROLES


def can_write_account(principal: AuthPrincipal, account_id: Optional[str]) -> bool:
    return account_role(principal, account_id) in WRITE_ROLES


def can_admin_account(principal: AuthPrincipal, account_id: Optional[str]) -> bool:
    return account_role(principal, account_id) in {OWNER, ADMIN}


def can_owner_account(principal: AuthPrincipal, account_id: Optional[str]) -> bool:
    return account_role(principal, account_id) in OWNER_ROLES


def can_access_home(db: Session, principal: AuthPrincipal, home_id: Optional[str]) -> bool:
    home = db.get(models.Home, home_id) if home_id else None
    return can_access_home_record(principal, home)


def can_access_home_record(principal: AuthPrincipal, home: Optional[models.Home]) -> bool:
    if home is None:
        return False
    if _local_test_scaffold_can_access_home(principal, home.id):
        return True
    return can_access_account(principal, home.account_id)


def can_write_home(db: Session, principal: AuthPrincipal, home_id: Optional[str]) -> bool:
    home = db.get(models.Home, home_id) if home_id else None
    return can_write_home_record(principal, home)


def can_write_home_record(principal: AuthPrincipal, home: Optional[models.Home]) -> bool:
    if home is None:
        return False
    if _local_test_scaffold_can_access_home(principal, home.id):
        return True
    return can_write_account(principal, home.account_id)


def can_privacy_admin_home(db: Session, principal: AuthPrincipal, home_id: Optional[str]) -> bool:
    home = db.get(models.Home, home_id) if home_id else None
    if home is None:
        return False
    return can_owner_account(principal, home.account_id)


def can_access_design(db: Session, principal: AuthPrincipal, design_id: Optional[str]) -> bool:
    design = db.get(models.EnergySystemDesign, design_id) if design_id else None
    if design is None:
        return False
    return can_access_home(db, principal, design.home_id)


def can_access_design_record(principal: AuthPrincipal, design: Optional[models.EnergySystemDesign]) -> bool:
    if design is None:
        return False
    return _home_id_is_allowed(principal, design.home_id)


def can_write_design(db: Session, principal: AuthPrincipal, design_id: Optional[str]) -> bool:
    design = db.get(models.EnergySystemDesign, design_id) if design_id else None
    if design is None:
        return False
    return can_write_home(db, principal, design.home_id)


def can_write_design_record(principal: AuthPrincipal, design: Optional[models.EnergySystemDesign]) -> bool:
    if design is None:
        return False
    return principal.auth_source == LOCAL_TEST_HEADER_SOURCE and _home_id_is_allowed(principal, design.home_id)


def can_access_scenario(db: Session, principal: AuthPrincipal, scenario_id: Optional[str]) -> bool:
    scenario = db.get(models.Scenario, scenario_id) if scenario_id else None
    if scenario is None:
        return False
    return can_access_home(db, principal, scenario.home_id)


def can_access_scenario_record(principal: AuthPrincipal, scenario: Optional[models.Scenario]) -> bool:
    if scenario is None:
        return False
    return _home_id_is_allowed(principal, scenario.home_id)


def can_write_scenario(db: Session, principal: AuthPrincipal, scenario_id: Optional[str]) -> bool:
    scenario = db.get(models.Scenario, scenario_id) if scenario_id else None
    if scenario is None:
        return False
    return can_write_home(db, principal, scenario.home_id)


def can_write_scenario_record(principal: AuthPrincipal, scenario: Optional[models.Scenario]) -> bool:
    if scenario is None:
        return False
    return principal.auth_source == LOCAL_TEST_HEADER_SOURCE and _home_id_is_allowed(principal, scenario.home_id)


def require_building_matches_home(db: Session, building_id: Optional[str], home_id: str) -> None:
    building = db.get(models.BuildingStructure, building_id) if building_id else None
    require_found_and_allowed(
        building is not None,
        building is not None and building.home_id == home_id,
        "Building not found",
    )


def allowed_account_ids(principal: AuthPrincipal) -> Set[str]:
    return {
        account_id
        for account_id, role in principal.account_roles.items()
        if role in READ_ROLES and account_id in principal.account_ids
    }


def writable_account_ids(principal: AuthPrincipal) -> Set[str]:
    return {
        account_id
        for account_id, role in principal.account_roles.items()
        if role in WRITE_ROLES and account_id in principal.account_ids
    }


def allowed_home_ids(principal: AuthPrincipal) -> Set[str]:
    if principal.auth_source == LOCAL_TEST_HEADER_SOURCE:
        return {home_id for home_id in principal.allowed_home_ids if home_id != "*"}
    return set(principal.allowed_home_ids)


def scoped_home_ids(db: Session, principal: AuthPrincipal) -> Set[str]:
    if principal.auth_source == LOCAL_TEST_HEADER_SOURCE:
        if "*" in principal.allowed_home_ids:
            rows = db.scalars(select(models.Home.id).where(models.Home.account_id.isnot(None))).all()
            return set(rows)
        return allowed_home_ids(principal)

    account_ids = allowed_account_ids(principal)
    if not account_ids:
        return set()
    rows = db.scalars(select(models.Home.id).where(models.Home.account_id.in_(account_ids))).all()
    return set(rows)


def scoped_design_ids(db: Session, principal: AuthPrincipal) -> Set[str]:
    home_ids = scoped_home_ids(db, principal)
    if not home_ids:
        return set()
    rows = db.scalars(
        select(models.EnergySystemDesign.id).where(models.EnergySystemDesign.home_id.in_(home_ids))
    ).all()
    return set(rows)


def require_allowed(condition: bool, detail: str = "Permission denied") -> None:
    if not condition:
        raise HTTPException(status_code=403, detail=detail)


def require_found_and_allowed(found: bool, allowed: bool, not_found_detail: str) -> None:
    if not found:
        raise HTTPException(status_code=404, detail=not_found_detail)
    require_allowed(allowed)


def filter_home_records(principal: AuthPrincipal, homes: Iterable[models.Home]):
    return [home for home in homes if can_access_home_record(principal, home)]


def _home_id_is_allowed(principal: AuthPrincipal, home_id: Optional[str]) -> bool:
    return bool(home_id) and (
        _local_test_scaffold_can_access_home(principal, home_id) or home_id in allowed_home_ids(principal)
    )


def _local_test_scaffold_can_access_home(principal: AuthPrincipal, home_id: str) -> bool:
    return principal.auth_source == LOCAL_TEST_HEADER_SOURCE and (
        "*" in principal.allowed_home_ids or home_id in principal.allowed_home_ids
    )

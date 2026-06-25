from typing import Iterable, List, Optional

from sqlalchemy.orm import Session

from app.core import models
from app.security import permissions
from app.security.principal import AuthPrincipal


GLOBAL_REFERENCE_ENTITY_TYPES = {
    "design_goal_preset",
    "design_goal_presets",
    "equipment_product",
    "equipment_products",
    "rule_provenance",
    "source_document",
    "source_documents",
}

HOME_SCOPED_MODELS = {
    "building": models.BuildingStructure,
    "buildings": models.BuildingStructure,
    "electrical_panel": models.ElectricalPanel,
    "panel": models.ElectricalPanel,
    "fact": models.Fact,
    "geometry_obstruction": models.GeometryObstruction,
    "home": models.Home,
    "load": models.Load,
    "equipment_location": models.EquipmentLocation,
    "roof_plane": models.RoofPlane,
}

DESIGN_SCOPED_MODELS = {
    "compatibility_issue": models.CompatibilityIssue,
    "design": models.EnergySystemDesign,
    "design_equipment": models.DesignEquipment,
    "energy_system_design": models.EnergySystemDesign,
    "energy_system_designs": models.EnergySystemDesign,
    "estimated_pathway": models.EstimatedPathway,
}


def filter_data_provenance(
    db: Session,
    principal: AuthPrincipal,
    records: Iterable[models.DataProvenance],
) -> List[models.DataProvenance]:
    return [record for record in records if can_access_data_provenance(db, principal, record)]


def can_access_data_provenance(
    db: Session,
    principal: AuthPrincipal,
    record: models.DataProvenance,
) -> bool:
    entity_type = _normalize(record.entity_type)
    entity_id = record.entity_id
    if not entity_type or not entity_id:
        return False
    if entity_type in GLOBAL_REFERENCE_ENTITY_TYPES:
        return True
    if entity_type == "load_template":
        return _can_access_load_template(db, principal, entity_id)
    if entity_type == "scenario":
        return permissions.can_access_scenario(db, principal, entity_id)
    if entity_type == "scenario_revision":
        revision = db.get(models.ScenarioRevision, entity_id)
        return revision is not None and permissions.can_access_scenario(db, principal, revision.scenario_id)
    if entity_type == "takeoff_request":
        request = db.get(models.TakeoffRequest, entity_id)
        return request is not None and permissions.can_access_design(db, principal, request.design_id)
    if entity_type == "takeoff_line_item":
        line_item = db.get(models.TakeoffLineItem, entity_id)
        if line_item is None:
            return False
        request = db.get(models.TakeoffRequest, line_item.takeoff_request_id)
        return request is not None and permissions.can_access_design(db, principal, request.design_id)
    if entity_type in DESIGN_SCOPED_MODELS:
        return _can_access_design_scoped_model(db, principal, entity_type, entity_id)
    if entity_type in HOME_SCOPED_MODELS:
        return _can_access_home_scoped_model(db, principal, entity_type, entity_id)
    return False


def _can_access_home_scoped_model(
    db: Session,
    principal: AuthPrincipal,
    entity_type: str,
    entity_id: str,
) -> bool:
    model = HOME_SCOPED_MODELS[entity_type]
    row = db.get(model, entity_id)
    if row is None:
        return False
    if isinstance(row, models.Home):
        return permissions.can_access_home_record(principal, row)
    return permissions.can_access_home(db, principal, row.home_id)


def _can_access_design_scoped_model(
    db: Session,
    principal: AuthPrincipal,
    entity_type: str,
    entity_id: str,
) -> bool:
    model = DESIGN_SCOPED_MODELS[entity_type]
    row = db.get(model, entity_id)
    if row is None:
        return False
    if isinstance(row, models.EnergySystemDesign):
        return permissions.can_access_design_record(principal, row)
    if isinstance(row, models.EstimatedPathway):
        return permissions.can_access_home(db, principal, row.home_id)
    return permissions.can_access_design(db, principal, row.design_id)


def _can_access_load_template(db: Session, principal: AuthPrincipal, template_id: str) -> bool:
    template = db.get(models.LoadTemplate, template_id)
    if template is None:
        return False
    if template.account_id is None:
        return True
    return permissions.can_access_account(principal, template.account_id)


def _normalize(entity_type: Optional[str]) -> Optional[str]:
    return entity_type.strip().lower() if entity_type else None

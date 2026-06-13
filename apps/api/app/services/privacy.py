from typing import Any, Dict, List

from sqlalchemy.orm import Session

from app.core import models
from app.privacy.schemas import ConsentRecord, PrivacyDeletionResult, PrivacyExport


class PrivacyService:
    def export_homeowner_record(self, db: Session, home_id: str) -> PrivacyExport:
        sections: Dict[str, Any] = {
            "home": self._model_dict(db.get(models.Home, home_id)),
            "facts": [self._model_dict(item) for item in db.query(models.Fact).filter_by(home_id=home_id).all()],
            "roof_planes": [self._model_dict(item) for item in db.query(models.RoofPlane).filter_by(home_id=home_id).all()],
            "obstructions": [
                self._model_dict(item) for item in db.query(models.GeometryObstruction).filter_by(home_id=home_id).all()
            ],
            "consent_records": [
                self._model_dict(item) for item in db.query(models.ConsentRecord).filter_by(home_id=home_id).all()
            ],
            "audit_events": [
                self._model_dict(item) for item in db.query(models.AuditEvent).filter_by(home_id=home_id).all()
            ],
        }
        return PrivacyExport(
            home_id=home_id,
            exported_sections=sections,
            limitations=[
                "Export is local application data only.",
                "External provider, utility, contractor, and payment systems are not integrated.",
            ],
        )

    def record_consent(self, db: Session, payload) -> ConsentRecord:
        record = models.ConsentRecord(**payload.dict())
        db.add(record)
        db.commit()
        db.refresh(record)
        return ConsentRecord.from_orm(record)

    def delete_homeowner_record(self, db: Session, home_id: str) -> PrivacyDeletionResult:
        deleted_sections: List[str] = []
        design_ids = [row[0] for row in db.query(models.EnergySystemDesign.id).filter_by(home_id=home_id).all()]
        scenario_ids = [row[0] for row in db.query(models.Scenario.id).filter_by(home_id=home_id).all()]
        takeoff_ids = []
        if design_ids:
            takeoff_ids = [
                row[0] for row in db.query(models.TakeoffRequest.id).filter(models.TakeoffRequest.design_id.in_(design_ids)).all()
            ]
            if takeoff_ids:
                if db.query(models.TakeoffLineItem).filter(models.TakeoffLineItem.takeoff_request_id.in_(takeoff_ids)).delete(synchronize_session=False):
                    deleted_sections.append("takeoff_line_items")
                if db.query(models.TakeoffRequest).filter(models.TakeoffRequest.id.in_(takeoff_ids)).delete(synchronize_session=False):
                    deleted_sections.append("takeoff_requests")
            if db.query(models.DesignEquipment).filter(models.DesignEquipment.design_id.in_(design_ids)).delete(synchronize_session=False):
                deleted_sections.append("design_equipment")
            if db.query(models.CompatibilityIssue).filter(models.CompatibilityIssue.design_id.in_(design_ids)).delete(synchronize_session=False):
                deleted_sections.append("compatibility_issues")
        if scenario_ids:
            if db.query(models.ScenarioRevision).filter(models.ScenarioRevision.scenario_id.in_(scenario_ids)).delete(synchronize_session=False):
                deleted_sections.append("scenario_revisions")

        for model, section in [
            (models.Fact, "facts"),
            (models.RoofPlane, "roof_planes"),
            (models.GeometryObstruction, "obstructions"),
            (models.ConsentRecord, "consent_records"),
            (models.AuditEvent, "audit_events"),
            (models.EstimatedPathway, "estimated_pathways"),
            (models.Scenario, "scenarios"),
            (models.EnergySystemDesign, "designs"),
            (models.Load, "loads"),
            (models.ElectricalPanel, "panels"),
            (models.EquipmentLocation, "equipment_locations"),
            (models.BuildingStructure, "buildings"),
        ]:
            deleted = db.query(model).filter_by(home_id=home_id).delete(synchronize_session=False)
            if deleted:
                deleted_sections.append(section)

        home = db.get(models.Home, home_id)
        if home is not None:
            db.delete(home)
            deleted_sections.append("home_and_cascaded_planning_records")
        db.commit()
        return PrivacyDeletionResult(
            home_id=home_id,
            deleted=bool(deleted_sections),
            deleted_sections=deleted_sections,
            retained_sections=[],
            limitations=[
                "Deletion applies to local SQLite application records only.",
                "External systems are not integrated and are not affected.",
            ],
        )

    def _model_dict(self, item):
        if item is None:
            return None
        return {column.name: getattr(item, column.name) for column in item.__table__.columns}


privacy_service = PrivacyService()

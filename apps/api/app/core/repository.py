from typing import Dict, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core import models
from app.scenarios.schemas import Scenario


def _apply_updates(instance, update_model):
    for field, value in update_model.dict(exclude_unset=True).items():
        setattr(instance, field, value)


class DatabaseRepository:
    def _serialize_scenario(self, db: Session, scenario):
        if scenario is None:
            return None
        from app.services.scenario_revision import scenario_revision_service

        serialized = Scenario.from_orm(scenario).dict()
        serialized["revision_overview"] = scenario_revision_service.build_revision_overview(
            db, scenario.id
        ).dict()
        serialized["revisions"] = [
            revision.dict()
            for revision in scenario_revision_service.list_revision_summaries(db, scenario.id)
        ]
        return serialized

    def list_accounts(self, db: Session):
        statement = select(models.Account).order_by(models.Account.created_at)
        return db.scalars(statement).all()

    def get_account(self, db: Session, account_id: str):
        return db.get(models.Account, account_id)

    def create_account(self, db: Session, payload):
        account = models.Account(**payload.dict())
        db.add(account)
        db.commit()
        db.refresh(account)
        return account

    def update_account(self, db: Session, account_id: str, payload):
        account = self.get_account(db, account_id)
        _apply_updates(account, payload)
        db.commit()
        db.refresh(account)
        return account

    def list_homes(self, db: Session):
        statement = (
            select(models.Home)
            .options(selectinload(models.Home.buildings), selectinload(models.Home.panels))
            .order_by(models.Home.created_at)
        )
        return db.scalars(statement).all()

    def get_home(self, db: Session):
        statement = (
            select(models.Home)
            .options(selectinload(models.Home.buildings), selectinload(models.Home.panels))
            .order_by(models.Home.created_at)
        )
        return db.scalars(statement).first()

    def get_home_by_id(self, db: Session, home_id: str):
        statement = (
            select(models.Home)
            .where(models.Home.id == home_id)
            .options(selectinload(models.Home.buildings), selectinload(models.Home.panels))
        )
        return db.scalars(statement).first()

    def create_home(self, db: Session, payload):
        home = models.Home(**payload.dict())
        db.add(home)
        db.commit()
        db.refresh(home)
        return self.get_home_by_id(db, home.id)

    def update_home(self, db: Session, home_id: str, payload):
        home = db.get(models.Home, home_id)
        _apply_updates(home, payload)
        db.commit()
        return self.get_home_by_id(db, home_id)

    def list_buildings(self, db: Session, home_id: Optional[str] = None):
        statement = select(models.BuildingStructure).order_by(models.BuildingStructure.created_at)
        if home_id:
            statement = statement.where(models.BuildingStructure.home_id == home_id)
        return db.scalars(statement).all()

    def get_building(self, db: Session, building_id: str):
        return db.get(models.BuildingStructure, building_id)

    def create_building(self, db: Session, payload):
        building = models.BuildingStructure(**payload.dict())
        db.add(building)
        db.commit()
        db.refresh(building)
        return building

    def update_building(self, db: Session, building_id: str, payload):
        building = self.get_building(db, building_id)
        _apply_updates(building, payload)
        db.commit()
        db.refresh(building)
        return building

    def delete_building(self, db: Session, building_id: str):
        building = self.get_building(db, building_id)
        db.delete(building)
        db.commit()

    def list_panels(self, db: Session, home_id: Optional[str] = None):
        statement = select(models.ElectricalPanel).order_by(models.ElectricalPanel.created_at)
        if home_id:
            statement = statement.where(models.ElectricalPanel.home_id == home_id)
        return db.scalars(statement).all()

    def get_panel(self, db: Session, panel_id: str):
        return db.get(models.ElectricalPanel, panel_id)

    def create_panel(self, db: Session, payload):
        panel = models.ElectricalPanel(**payload.dict())
        db.add(panel)
        db.commit()
        db.refresh(panel)
        return panel

    def update_panel(self, db: Session, panel_id: str, payload):
        panel = self.get_panel(db, panel_id)
        _apply_updates(panel, payload)
        db.commit()
        db.refresh(panel)
        return panel

    def delete_panel(self, db: Session, panel_id: str):
        panel = self.get_panel(db, panel_id)
        db.delete(panel)
        db.commit()

    def list_loads(self, db: Session, home_id: Optional[str] = None):
        statement = select(models.Load).order_by(models.Load.created_at)
        if home_id:
            statement = statement.where(models.Load.home_id == home_id)
        return db.scalars(statement).all()

    def get_load(self, db: Session, load_id: str):
        return db.get(models.Load, load_id)

    def create_load(self, db: Session, payload):
        load = models.Load(**payload.dict())
        db.add(load)
        db.commit()
        db.refresh(load)
        return load

    def update_load(self, db: Session, load_id: str, payload):
        load = self.get_load(db, load_id)
        _apply_updates(load, payload)
        db.commit()
        db.refresh(load)
        return load

    def delete_load(self, db: Session, load_id: str):
        load = self.get_load(db, load_id)
        db.delete(load)
        db.commit()

    def list_designs(self, db: Session):
        statement = (
            select(models.EnergySystemDesign)
            .options(
                selectinload(models.EnergySystemDesign.equipment).selectinload(models.DesignEquipment.product),
                selectinload(models.EnergySystemDesign.equipment).selectinload(models.DesignEquipment.location),
            )
            .order_by(models.EnergySystemDesign.created_at)
        )
        return db.scalars(statement).all()

    def get_design(self, db: Session, design_id: str):
        statement = (
            select(models.EnergySystemDesign)
            .where(models.EnergySystemDesign.id == design_id)
            .options(
                selectinload(models.EnergySystemDesign.equipment).selectinload(models.DesignEquipment.product),
                selectinload(models.EnergySystemDesign.equipment).selectinload(models.DesignEquipment.location),
            )
        )
        return db.scalars(statement).first()

    def create_design(self, db: Session, payload):
        data = payload.dict()
        equipment = data.pop("equipment", [])
        design = models.EnergySystemDesign(**data)
        db.add(design)
        for index, item in enumerate(equipment, start=1):
            db.add(
                models.DesignEquipment(
                    id=f"{design.id}_equipment_{index}",
                    design_id=design.id,
                    **item,
                )
            )
        db.commit()
        return self.get_design(db, design.id)

    def update_design(self, db: Session, design_id: str, payload):
        design = db.get(models.EnergySystemDesign, design_id)
        _apply_updates(design, payload)
        db.commit()
        return self.get_design(db, design_id)

    def delete_design(self, db: Session, design_id: str):
        design = db.get(models.EnergySystemDesign, design_id)
        db.delete(design)
        db.commit()

    def list_design_equipment(self, db: Session, design_id: str):
        statement = (
            select(models.DesignEquipment)
            .where(models.DesignEquipment.design_id == design_id)
            .options(
                selectinload(models.DesignEquipment.product),
                selectinload(models.DesignEquipment.location),
            )
            .order_by(models.DesignEquipment.created_at)
        )
        return db.scalars(statement).all()

    def get_design_equipment(self, db: Session, equipment_id: str):
        statement = (
            select(models.DesignEquipment)
            .where(models.DesignEquipment.id == equipment_id)
            .options(
                selectinload(models.DesignEquipment.product),
                selectinload(models.DesignEquipment.location),
            )
        )
        return db.scalars(statement).first()

    def create_design_equipment(self, db: Session, payload):
        equipment = models.DesignEquipment(**payload.dict())
        db.add(equipment)
        db.commit()
        return self.get_design_equipment(db, equipment.id)

    def update_design_equipment(self, db: Session, equipment_id: str, payload):
        equipment = db.get(models.DesignEquipment, equipment_id)
        _apply_updates(equipment, payload)
        db.commit()
        return self.get_design_equipment(db, equipment_id)

    def delete_design_equipment(self, db: Session, equipment_id: str):
        equipment = db.get(models.DesignEquipment, equipment_id)
        db.delete(equipment)
        db.commit()

    def list_equipment_locations(self, db: Session, home_id: Optional[str] = None):
        statement = select(models.EquipmentLocation).order_by(models.EquipmentLocation.created_at)
        if home_id:
            statement = statement.where(models.EquipmentLocation.home_id == home_id)
        return db.scalars(statement).all()

    def get_equipment_location(self, db: Session, location_id: str):
        return db.get(models.EquipmentLocation, location_id)

    def create_equipment_location(self, db: Session, payload):
        location = models.EquipmentLocation(**payload.dict())
        db.add(location)
        db.commit()
        db.refresh(location)
        return location

    def update_equipment_location(self, db: Session, location_id: str, payload):
        location = self.get_equipment_location(db, location_id)
        _apply_updates(location, payload)
        db.commit()
        db.refresh(location)
        return location

    def delete_equipment_location(self, db: Session, location_id: str):
        location = self.get_equipment_location(db, location_id)
        db.delete(location)
        db.commit()

    def list_products(self, db: Session):
        statement = select(models.EquipmentProduct).order_by(
            models.EquipmentProduct.ecosystem, models.EquipmentProduct.model
        )
        return db.scalars(statement).all()

    def get_product(self, db: Session, product_id: str):
        return db.get(models.EquipmentProduct, product_id)

    def create_product(self, db: Session, payload):
        product = models.EquipmentProduct(**payload.dict())
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    def update_product(self, db: Session, product_id: str, payload):
        product = self.get_product(db, product_id)
        _apply_updates(product, payload)
        db.commit()
        db.refresh(product)
        return product

    def delete_product(self, db: Session, product_id: str):
        product = self.get_product(db, product_id)
        db.delete(product)
        db.commit()

    def list_compatibility_issues(self, db: Session, design_id: Optional[str] = None):
        statement = select(models.CompatibilityIssue).order_by(models.CompatibilityIssue.created_at)
        if design_id:
            statement = statement.where(models.CompatibilityIssue.design_id == design_id)
        return db.scalars(statement).all()

    def list_scenario_models(self, db: Session):
        statement = (
            select(models.Scenario)
            .options(selectinload(models.Scenario.revisions))
            .order_by(models.Scenario.created_at)
        )
        return db.scalars(statement).all()

    def get_scenario_model(self, db: Session, scenario_id: str):
        statement = (
            select(models.Scenario)
            .where(models.Scenario.id == scenario_id)
            .options(selectinload(models.Scenario.revisions))
        )
        return db.scalars(statement).first()

    def list_scenarios(self, db: Session):
        return [self._serialize_scenario(db, scenario) for scenario in self.list_scenario_models(db)]

    def get_scenario(self, db: Session, scenario_id: str):
        return self._serialize_scenario(db, self.get_scenario_model(db, scenario_id))

    def create_scenario(self, db: Session, payload):
        scenario = models.Scenario(**payload.dict())
        db.add(scenario)
        db.commit()
        db.refresh(scenario)
        return self.get_scenario(db, scenario.id)

    def update_scenario(self, db: Session, scenario_id: str, payload):
        scenario = db.get(models.Scenario, scenario_id)
        _apply_updates(scenario, payload)
        db.commit()
        return self.get_scenario(db, scenario_id)

    def delete_scenario(self, db: Session, scenario_id: str):
        scenario = db.get(models.Scenario, scenario_id)
        db.delete(scenario)
        db.commit()

    def get_takeoff(self, db: Session) -> Dict[str, object]:
        statement = (
            select(models.TakeoffRequest)
            .options(selectinload(models.TakeoffRequest.line_items))
            .order_by(models.TakeoffRequest.created_at)
        )
        request = db.scalars(statement).first()
        if request is None:
            return {"request": None, "line_items": []}
        return {"request": request, "line_items": request.line_items}

    def get_takeoff_by_design(self, db: Session, design_id: str) -> Dict[str, object]:
        statement = (
            select(models.TakeoffRequest)
            .where(models.TakeoffRequest.design_id == design_id)
            .options(selectinload(models.TakeoffRequest.line_items))
            .order_by(models.TakeoffRequest.created_at)
        )
        request = db.scalars(statement).first()
        if request is None:
            return self.get_takeoff(db)
        return {"request": request, "line_items": request.line_items}

    def list_estimated_pathways(self, db: Session, home_id: Optional[str] = None):
        statement = select(models.EstimatedPathway).order_by(models.EstimatedPathway.created_at)
        if home_id:
            statement = statement.where(models.EstimatedPathway.home_id == home_id)
        return db.scalars(statement).all()

    def get_estimated_pathway(self, db: Session, pathway_id: str):
        return db.get(models.EstimatedPathway, pathway_id)

    def create_estimated_pathway(self, db: Session, payload):
        pathway = models.EstimatedPathway(**payload.dict())
        db.add(pathway)
        db.commit()
        db.refresh(pathway)
        return pathway

    def update_estimated_pathway(self, db: Session, pathway_id: str, payload):
        pathway = self.get_estimated_pathway(db, pathway_id)
        _apply_updates(pathway, payload)
        db.commit()
        db.refresh(pathway)
        return pathway

    def delete_estimated_pathway(self, db: Session, pathway_id: str):
        pathway = self.get_estimated_pathway(db, pathway_id)
        db.delete(pathway)
        db.commit()

    def list_load_templates(self, db: Session):
        statement = select(models.LoadTemplate).order_by(models.LoadTemplate.created_at)
        return db.scalars(statement).all()

    def get_load_template(self, db: Session, template_id: str):
        return db.get(models.LoadTemplate, template_id)

    def create_load_template(self, db: Session, payload):
        template = models.LoadTemplate(**payload.dict())
        db.add(template)
        db.commit()
        db.refresh(template)
        return template

    def update_load_template(self, db: Session, template_id: str, payload):
        template = self.get_load_template(db, template_id)
        _apply_updates(template, payload)
        db.commit()
        db.refresh(template)
        return template

    def delete_load_template(self, db: Session, template_id: str):
        template = self.get_load_template(db, template_id)
        db.delete(template)
        db.commit()

    def list_design_goal_presets(self, db: Session):
        statement = select(models.DesignGoalPreset).order_by(models.DesignGoalPreset.created_at)
        return db.scalars(statement).all()

    def get_design_goal_preset(self, db: Session, preset_id: str):
        return db.get(models.DesignGoalPreset, preset_id)

    def create_design_goal_preset(self, db: Session, payload):
        preset = models.DesignGoalPreset(**payload.dict())
        db.add(preset)
        db.commit()
        db.refresh(preset)
        return preset

    def update_design_goal_preset(self, db: Session, preset_id: str, payload):
        preset = self.get_design_goal_preset(db, preset_id)
        _apply_updates(preset, payload)
        db.commit()
        db.refresh(preset)
        return preset

    def delete_design_goal_preset(self, db: Session, preset_id: str):
        preset = self.get_design_goal_preset(db, preset_id)
        db.delete(preset)
        db.commit()

    def list_source_documents(self, db: Session, manufacturer: Optional[str] = None, product_model: Optional[str] = None):
        statement = select(models.SourceDocument).order_by(models.SourceDocument.created_at)
        if manufacturer:
            statement = statement.where(models.SourceDocument.manufacturer == manufacturer)
        if product_model:
            statement = statement.where(models.SourceDocument.product_model == product_model)
        return db.scalars(statement).all()

    def get_source_documents_by_ids(self, db: Session, source_document_ids):
        if not source_document_ids:
            return []
        statement = select(models.SourceDocument).where(models.SourceDocument.id.in_(set(source_document_ids)))
        return db.scalars(statement).all()

    def create_source_document(self, db: Session, payload):
        document = models.SourceDocument(**payload.dict())
        db.add(document)
        db.commit()
        db.refresh(document)
        return document

    def list_data_provenance(self, db: Session, entity_type: Optional[str] = None, entity_id: Optional[str] = None):
        statement = (
            select(models.DataProvenance)
            .options(selectinload(models.DataProvenance.source_document))
            .order_by(models.DataProvenance.created_at)
        )
        if entity_type:
            statement = statement.where(models.DataProvenance.entity_type == entity_type)
        if entity_id:
            statement = statement.where(models.DataProvenance.entity_id == entity_id)
        return db.scalars(statement).all()

    def list_data_provenance_for_entities(self, db: Session, entity_type: str, entity_ids):
        if not entity_ids:
            return []
        statement = (
            select(models.DataProvenance)
            .where(
                models.DataProvenance.entity_type == entity_type,
                models.DataProvenance.entity_id.in_(set(entity_ids)),
            )
            .options(selectinload(models.DataProvenance.source_document))
            .order_by(models.DataProvenance.created_at)
        )
        return db.scalars(statement).all()

    def create_data_provenance(self, db: Session, payload):
        record = models.DataProvenance(**payload.dict())
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    def list_rule_provenance(self, db: Session, rule_key: Optional[str] = None):
        statement = (
            select(models.RuleProvenance)
            .options(selectinload(models.RuleProvenance.source_document))
            .order_by(models.RuleProvenance.created_at)
        )
        if rule_key:
            statement = statement.where(models.RuleProvenance.rule_key == rule_key)
        return db.scalars(statement).all()

    def list_rule_provenance_for_keys(self, db: Session, rule_keys):
        if not rule_keys:
            return []
        statement = (
            select(models.RuleProvenance)
            .where(models.RuleProvenance.rule_key.in_(set(rule_keys)))
            .options(selectinload(models.RuleProvenance.source_document))
            .order_by(models.RuleProvenance.created_at)
        )
        return db.scalars(statement).all()

    def create_rule_provenance(self, db: Session, payload):
        record = models.RuleProvenance(**payload.dict())
        db.add(record)
        db.commit()
        db.refresh(record)
        return record


repository = DatabaseRepository()

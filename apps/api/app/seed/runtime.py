from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import Base, SessionLocal, database_path, engine
from app.core import models
from app.seed.sample_data import (
    DEMO_ACCOUNT,
    SAMPLE_COMPATIBILITY_ISSUES,
    SAMPLE_DATA_PROVENANCE,
    SAMPLE_DESIGNS,
    SAMPLE_DESIGN_GOAL_PRESETS,
    SAMPLE_EQUIPMENT_LOCATIONS,
    SAMPLE_ESTIMATED_PATHWAYS,
    SAMPLE_HOME,
    SAMPLE_LOADS,
    SAMPLE_LOAD_TEMPLATES,
    SAMPLE_PRODUCTS,
    SAMPLE_RULE_PROVENANCE,
    SAMPLE_SCENARIOS,
    SAMPLE_SOURCE_DOCUMENTS,
    SAMPLE_TAKEOFF,
)
from app.services.scenario_revision import scenario_revision_service


DEMO_SEED_HOME_ID = SAMPLE_HOME["id"]
DEMO_SEED_ACCOUNT_ID = DEMO_ACCOUNT["id"]
PROVENANCE_ENTITY_MODELS = {
    "equipment_product": models.EquipmentProduct,
    "estimated_pathway": models.EstimatedPathway,
    "load": models.Load,
    "takeoff_line_item": models.TakeoffLineItem,
}


def _with_demo_origin(record):
    enriched = dict(record)
    enriched.setdefault("data_origin", "demo_seed")
    return enriched


def init_database():
    Base.metadata.create_all(bind=engine)


def _is_demo_seed_dataset(db: Session) -> bool:
    demo_account = db.get(models.Account, DEMO_SEED_ACCOUNT_ID)
    demo_home = db.get(models.Home, DEMO_SEED_HOME_ID)
    if demo_account is None or demo_home is None:
        return False
    return demo_account.data_origin == "demo_seed" and demo_home.data_origin == "demo_seed"


def _existing_entity_ids(db: Session):
    return {
        entity_type: {row[0] for row in db.execute(select(model.id)).all()}
        for entity_type, model in PROVENANCE_ENTITY_MODELS.items()
    }


def _with_global_rule_origin(record):
    enriched = dict(record)
    enriched.setdefault("data_origin", "imported")
    return enriched


def _backfill_global_rule_provenance_rows(db: Session):
    inserted = False
    required_source_document_ids = {
        record["source_document_id"] for record in SAMPLE_RULE_PROVENANCE if record.get("source_document_id")
    }
    source_documents_by_id = {document["id"]: document for document in SAMPLE_SOURCE_DOCUMENTS}

    existing_source_document_ids = {
        row[0] for row in db.execute(select(models.SourceDocument.id)).all()
    }
    for document_id in required_source_document_ids:
        document = source_documents_by_id.get(document_id)
        if document and document["id"] not in existing_source_document_ids:
            db.add(models.SourceDocument(**_with_global_rule_origin(document)))
            existing_source_document_ids.add(document["id"])
            inserted = True

    existing_rule_provenance_ids = {
        row[0] for row in db.execute(select(models.RuleProvenance.id)).all()
    }
    for record in SAMPLE_RULE_PROVENANCE:
        if record["id"] in existing_rule_provenance_ids:
            continue
        if record["source_document_id"] not in existing_source_document_ids:
            continue
        db.add(models.RuleProvenance(**record))
        inserted = True

    if inserted:
        db.commit()


def _backfill_demo_entity_provenance_rows(db: Session):
    inserted = False
    existing_entity_ids = _existing_entity_ids(db)
    required_source_document_ids = {
        record["source_document_id"] for record in SAMPLE_DATA_PROVENANCE if record.get("source_document_id")
    }
    source_documents_by_id = {document["id"]: document for document in SAMPLE_SOURCE_DOCUMENTS}
    existing_source_document_ids = {
        row[0] for row in db.execute(select(models.SourceDocument.id)).all()
    }
    for document_id in required_source_document_ids:
        document = source_documents_by_id.get(document_id)
        if document and document["id"] not in existing_source_document_ids:
            db.add(models.SourceDocument(**_with_demo_origin(document)))
            existing_source_document_ids.add(document["id"])
            inserted = True
    existing_data_provenance_ids = {
        row[0] for row in db.execute(select(models.DataProvenance.id)).all()
    }
    for record in SAMPLE_DATA_PROVENANCE:
        if record["id"] in existing_data_provenance_ids:
            continue
        if record["source_document_id"] not in existing_source_document_ids:
            continue
        entity_ids = existing_entity_ids.get(record["entity_type"])
        if entity_ids is None or record["entity_id"] not in entity_ids:
            continue
        db.add(models.DataProvenance(**record))
        inserted = True

    if inserted:
        db.commit()


def seed_database(db: Session, force: bool = False):
    if not force and db.scalars(select(models.Home.id)).first():
        _backfill_global_rule_provenance_rows(db)
        if _is_demo_seed_dataset(db):
            _backfill_demo_entity_provenance_rows(db)
        scenario_revision_service.ensure_revisions_for_existing_scenarios(db)
        return

    if force:
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()

    db.add(models.Account(**_with_demo_origin(DEMO_ACCOUNT)))
    db.add(
        models.Home(
            **_with_demo_origin(
                {key: value for key, value in SAMPLE_HOME.items() if key not in {"buildings", "panels"}}
            )
        )
    )

    for building in SAMPLE_HOME["buildings"]:
        db.add(models.BuildingStructure(**_with_demo_origin(building)))

    for panel in SAMPLE_HOME["panels"]:
        db.add(models.ElectricalPanel(**_with_demo_origin(panel)))

    for load in SAMPLE_LOADS:
        db.add(models.Load(**_with_demo_origin(load)))

    for location in SAMPLE_EQUIPMENT_LOCATIONS:
        db.add(models.EquipmentLocation(**_with_demo_origin(location)))

    for product in SAMPLE_PRODUCTS:
        db.add(models.EquipmentProduct(**_with_demo_origin(product)))

    for design in SAMPLE_DESIGNS:
        db.add(
            models.EnergySystemDesign(
                **_with_demo_origin({key: value for key, value in design.items() if key != "equipment"})
            )
        )
        for index, equipment in enumerate(design.get("equipment", []), start=1):
            db.add(
                models.DesignEquipment(
                    id=f"{design['id']}_equipment_{index}",
                    **_with_demo_origin(equipment),
                )
            )

    for issue in SAMPLE_COMPATIBILITY_ISSUES:
        db.add(models.CompatibilityIssue(**_with_demo_origin(issue)))

    for scenario in SAMPLE_SCENARIOS:
        db.add(models.Scenario(**_with_demo_origin(scenario)))

    db.add(models.TakeoffRequest(**_with_demo_origin(SAMPLE_TAKEOFF["request"])))
    for item in SAMPLE_TAKEOFF["line_items"]:
        db.add(models.TakeoffLineItem(**_with_demo_origin(item)))

    for template in SAMPLE_LOAD_TEMPLATES:
        db.add(models.LoadTemplate(**_with_demo_origin(template)))

    for preset in SAMPLE_DESIGN_GOAL_PRESETS:
        db.add(models.DesignGoalPreset(**_with_demo_origin(preset)))

    for pathway in SAMPLE_ESTIMATED_PATHWAYS:
        db.add(models.EstimatedPathway(**_with_demo_origin(pathway)))

    for document in SAMPLE_SOURCE_DOCUMENTS:
        db.add(models.SourceDocument(**_with_demo_origin(document)))

    for record in SAMPLE_DATA_PROVENANCE:
        db.add(models.DataProvenance(**record))

    for record in SAMPLE_RULE_PROVENANCE:
        db.add(models.RuleProvenance(**record))

    db.commit()
    scenario_revision_service.ensure_revisions_for_existing_scenarios(db)


def initialize_and_seed(db: Session):
    init_database()
    seed_database(db, force=False)


def reset_and_reseed():
    engine.dispose()
    db_path = database_path()
    if Path(db_path).exists():
        Path(db_path).unlink()
    init_database()
    with SessionLocal() as reset_db:
        seed_database(reset_db, force=False)

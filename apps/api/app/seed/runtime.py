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


def _with_demo_origin(record):
    enriched = dict(record)
    enriched.setdefault("data_origin", "demo_seed")
    return enriched


def init_database():
    Base.metadata.create_all(bind=engine)


def seed_database(db: Session, force: bool = False):
    if not force and db.scalars(select(models.Home.id)).first():
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

from typing import List, Optional

from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.types import FactLifecycleState


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Account(Base, TimestampMixin):
    __tablename__ = "accounts"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String)
    subscription_status: Mapped[str] = mapped_column(String)
    plan_type: Mapped[str] = mapped_column(String)
    data_origin: Mapped[str] = mapped_column(
        String, default=FactLifecycleState.user_created.value, index=True
    )

    homes: Mapped[List["Home"]] = relationship("Home", back_populates="account")


class Home(Base, TimestampMixin):
    __tablename__ = "homes"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    account_id: Mapped[Optional[str]] = mapped_column(ForeignKey("accounts.id"), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String)
    address_line_1: Mapped[str] = mapped_column(String)
    address_line_2: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    city: Mapped[str] = mapped_column(String)
    state: Mapped[str] = mapped_column(String)
    postal_code: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String, default="US")
    utility_provider: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    service_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_origin: Mapped[str] = mapped_column(
        String, default=FactLifecycleState.user_created.value, index=True
    )

    account: Mapped[Optional["Account"]] = relationship("Account", back_populates="homes")
    buildings: Mapped[List["BuildingStructure"]] = relationship(
        "BuildingStructure", back_populates="home", cascade="all, delete-orphan"
    )
    panels: Mapped[List["ElectricalPanel"]] = relationship(
        "ElectricalPanel", back_populates="home", cascade="all, delete-orphan"
    )
    loads: Mapped[List["Load"]] = relationship("Load", back_populates="home", cascade="all, delete-orphan")
    designs: Mapped[List["EnergySystemDesign"]] = relationship(
        "EnergySystemDesign", back_populates="home", cascade="all, delete-orphan"
    )
    equipment_locations: Mapped[List["EquipmentLocation"]] = relationship(
        "EquipmentLocation", back_populates="home", cascade="all, delete-orphan"
    )
    scenarios: Mapped[List["Scenario"]] = relationship(
        "Scenario", back_populates="home", cascade="all, delete-orphan"
    )
    estimated_pathways: Mapped[List["EstimatedPathway"]] = relationship(
        "EstimatedPathway", back_populates="home", cascade="all, delete-orphan"
    )
    facts: Mapped[List["Fact"]] = relationship(
        "Fact", back_populates="home", cascade="all, delete-orphan"
    )
    roof_planes: Mapped[List["RoofPlane"]] = relationship(
        "RoofPlane", back_populates="home", cascade="all, delete-orphan"
    )
    geometry_obstructions: Mapped[List["GeometryObstruction"]] = relationship(
        "GeometryObstruction", back_populates="home", cascade="all, delete-orphan"
    )


class Fact(Base, TimestampMixin):
    __tablename__ = "facts"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    home_id: Mapped[str] = mapped_column(ForeignKey("homes.id"), index=True)
    key: Mapped[str] = mapped_column(String, index=True)
    value: Mapped[object] = mapped_column(JSON)
    unit: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    source: Mapped[str] = mapped_column(String, index=True)
    confidence_tier: Mapped[str] = mapped_column(String, index=True)
    verified_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    decay_policy: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    derived_from: Mapped[List[str]] = mapped_column(JSON, default=list)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    home: Mapped["Home"] = relationship("Home", back_populates="facts")


class RoofPlane(Base, TimestampMixin):
    __tablename__ = "roof_planes"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    home_id: Mapped[str] = mapped_column(ForeignKey("homes.id"), index=True)
    name: Mapped[str] = mapped_column(String)
    area_sqft: Mapped[float] = mapped_column(Float)
    azimuth_degrees: Mapped[float] = mapped_column(Float)
    pitch_degrees: Mapped[float] = mapped_column(Float)
    usable_area_sqft: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    horizon_trace: Mapped[List] = mapped_column(JSON, default=list)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_origin: Mapped[str] = mapped_column(
        String, default=FactLifecycleState.user_created.value, index=True
    )

    home: Mapped["Home"] = relationship("Home", back_populates="roof_planes")


class GeometryObstruction(Base, TimestampMixin):
    __tablename__ = "geometry_obstructions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    home_id: Mapped[str] = mapped_column(ForeignKey("homes.id"), index=True)
    name: Mapped[str] = mapped_column(String)
    obstruction_type: Mapped[str] = mapped_column(String)
    approximate_height_ft: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    azimuth_degrees: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    distance_ft: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_origin: Mapped[str] = mapped_column(
        String, default=FactLifecycleState.user_created.value, index=True
    )

    home: Mapped["Home"] = relationship("Home", back_populates="geometry_obstructions")


class BuildingStructure(Base, TimestampMixin):
    __tablename__ = "buildings"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    home_id: Mapped[str] = mapped_column(ForeignKey("homes.id"), index=True)
    name: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    approximate_distance_from_main_service: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_origin: Mapped[str] = mapped_column(
        String, default=FactLifecycleState.user_created.value, index=True
    )

    home: Mapped["Home"] = relationship("Home", back_populates="buildings")
    panels: Mapped[List["ElectricalPanel"]] = relationship("ElectricalPanel", back_populates="building")
    loads: Mapped[List["Load"]] = relationship("Load", back_populates="building")
    equipment_locations: Mapped[List["EquipmentLocation"]] = relationship(
        "EquipmentLocation", back_populates="building"
    )


class ElectricalPanel(Base, TimestampMixin):
    __tablename__ = "electrical_panels"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    home_id: Mapped[str] = mapped_column(ForeignKey("homes.id"), index=True)
    building_id: Mapped[str] = mapped_column(ForeignKey("buildings.id"), index=True)
    panel_type: Mapped[str] = mapped_column(String)
    amperage: Mapped[int] = mapped_column(Integer)
    busbar_rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    breaker_spaces_total: Mapped[int] = mapped_column(Integer)
    breaker_spaces_available: Mapped[int] = mapped_column(Integer)
    indoor_outdoor: Mapped[str] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_origin: Mapped[str] = mapped_column(
        String, default=FactLifecycleState.user_created.value, index=True
    )

    home: Mapped["Home"] = relationship("Home", back_populates="panels")
    building: Mapped["BuildingStructure"] = relationship("BuildingStructure", back_populates="panels")


class Load(Base, TimestampMixin):
    __tablename__ = "loads"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    home_id: Mapped[str] = mapped_column(ForeignKey("homes.id"), index=True)
    building_id: Mapped[str] = mapped_column(ForeignKey("buildings.id"), index=True)
    name: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    running_watts: Mapped[float] = mapped_column(Float)
    surge_watts: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    estimated_daily_hours: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    backup_priority: Mapped[str] = mapped_column(String)
    phase_type: Mapped[str] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_origin: Mapped[str] = mapped_column(
        String, default=FactLifecycleState.user_created.value, index=True
    )

    home: Mapped["Home"] = relationship("Home", back_populates="loads")
    building: Mapped["BuildingStructure"] = relationship("BuildingStructure", back_populates="loads")


class EquipmentProduct(Base, TimestampMixin):
    __tablename__ = "equipment_products"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    manufacturer: Mapped[str] = mapped_column(String)
    model: Mapped[str] = mapped_column(String)
    product_type: Mapped[str] = mapped_column(String)
    ecosystem: Mapped[str] = mapped_column(String)
    specs: Mapped[dict] = mapped_column(JSON)
    documentation_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_origin: Mapped[str] = mapped_column(
        String, default=FactLifecycleState.user_created.value, index=True
    )

    design_equipment: Mapped[List["DesignEquipment"]] = relationship(
        "DesignEquipment", back_populates="product"
    )


class EquipmentLocation(Base, TimestampMixin):
    __tablename__ = "equipment_locations"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    home_id: Mapped[str] = mapped_column(ForeignKey("homes.id"), index=True)
    building_id: Mapped[str] = mapped_column(ForeignKey("buildings.id"), index=True)
    name: Mapped[str] = mapped_column(String)
    location_type: Mapped[str] = mapped_column(String)
    approximate_coordinates: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_origin: Mapped[str] = mapped_column(
        String, default=FactLifecycleState.user_created.value, index=True
    )

    home: Mapped["Home"] = relationship("Home", back_populates="equipment_locations")
    building: Mapped["BuildingStructure"] = relationship(
        "BuildingStructure", back_populates="equipment_locations"
    )
    design_equipment: Mapped[List["DesignEquipment"]] = relationship(
        "DesignEquipment", back_populates="location"
    )


class EnergySystemDesign(Base, TimestampMixin):
    __tablename__ = "energy_system_designs"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    home_id: Mapped[str] = mapped_column(ForeignKey("homes.id"), index=True)
    name: Mapped[str] = mapped_column(String)
    design_goal: Mapped[str] = mapped_column(String)
    architecture_type: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_origin: Mapped[str] = mapped_column(
        String, default=FactLifecycleState.user_created.value, index=True
    )

    home: Mapped["Home"] = relationship("Home", back_populates="designs")
    equipment: Mapped[List["DesignEquipment"]] = relationship(
        "DesignEquipment", back_populates="design", cascade="all, delete-orphan"
    )
    compatibility_issues: Mapped[List["CompatibilityIssue"]] = relationship(
        "CompatibilityIssue", back_populates="design", cascade="all, delete-orphan"
    )
    scenarios: Mapped[List["Scenario"]] = relationship("Scenario", back_populates="design")
    takeoff_requests: Mapped[List["TakeoffRequest"]] = relationship(
        "TakeoffRequest", back_populates="design"
    )
    estimated_pathways: Mapped[List["EstimatedPathway"]] = relationship(
        "EstimatedPathway", back_populates="design"
    )


class DesignEquipment(Base, TimestampMixin):
    __tablename__ = "design_equipment"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    design_id: Mapped[str] = mapped_column(ForeignKey("energy_system_designs.id"), index=True)
    product_id: Mapped[str] = mapped_column(ForeignKey("equipment_products.id"), index=True)
    quantity: Mapped[float] = mapped_column(Float)
    location_id: Mapped[Optional[str]] = mapped_column(ForeignKey("equipment_locations.id"), nullable=True)
    role_in_system: Mapped[str] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_origin: Mapped[str] = mapped_column(
        String, default=FactLifecycleState.user_created.value, index=True
    )

    design: Mapped["EnergySystemDesign"] = relationship("EnergySystemDesign", back_populates="equipment")
    product: Mapped["EquipmentProduct"] = relationship("EquipmentProduct", back_populates="design_equipment")
    location: Mapped[Optional["EquipmentLocation"]] = relationship(
        "EquipmentLocation", back_populates="design_equipment"
    )


class CompatibilityIssue(Base, TimestampMixin):
    __tablename__ = "compatibility_issues"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    design_id: Mapped[str] = mapped_column(ForeignKey("energy_system_designs.id"), index=True)
    severity: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    issue: Mapped[str] = mapped_column(Text)
    why_it_matters: Mapped[str] = mapped_column(Text)
    possible_solutions: Mapped[List] = mapped_column(JSON)
    tradeoff: Mapped[str] = mapped_column(Text)
    related_equipment_ids: Mapped[List] = mapped_column(JSON)
    data_origin: Mapped[str] = mapped_column(
        String, default=FactLifecycleState.user_created.value, index=True
    )

    design: Mapped["EnergySystemDesign"] = relationship(
        "EnergySystemDesign", back_populates="compatibility_issues"
    )


class Scenario(Base, TimestampMixin):
    __tablename__ = "scenarios"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    home_id: Mapped[str] = mapped_column(ForeignKey("homes.id"), index=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    linked_design_id: Mapped[str] = mapped_column(ForeignKey("energy_system_designs.id"), index=True)
    upfront_cost_placeholder: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    future_expansion_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    install_complexity_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    backup_capability_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_origin: Mapped[str] = mapped_column(
        String, default=FactLifecycleState.user_created.value, index=True
    )

    home: Mapped["Home"] = relationship("Home", back_populates="scenarios")
    design: Mapped["EnergySystemDesign"] = relationship("EnergySystemDesign", back_populates="scenarios")
    revisions: Mapped[List["ScenarioRevision"]] = relationship(
        "ScenarioRevision", back_populates="scenario", cascade="all, delete-orphan"
    )


class ScenarioRevision(Base, TimestampMixin):
    __tablename__ = "scenario_revisions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    scenario_id: Mapped[str] = mapped_column(ForeignKey("scenarios.id"), index=True)
    parent_revision_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("scenario_revisions.id"), nullable=True, index=True
    )
    revision_number: Mapped[int] = mapped_column(Integer)
    revision_label: Mapped[str] = mapped_column(String)
    revision_status: Mapped[str] = mapped_column(String, default="saved_revision")
    linked_design_id: Mapped[str] = mapped_column(String, index=True)
    design_goal_snapshot: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    design_status_snapshot: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    recommended_profile_snapshot: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    planning_summary: Mapped[str] = mapped_column(Text)
    planning_state_snapshot: Mapped[dict] = mapped_column(JSON)
    data_origin: Mapped[str] = mapped_column(
        String, default=FactLifecycleState.derived_estimate.value, index=True
    )

    scenario: Mapped["Scenario"] = relationship("Scenario", back_populates="revisions")
    parent_revision: Mapped[Optional["ScenarioRevision"]] = relationship(
        "ScenarioRevision", remote_side="ScenarioRevision.id"
    )


class TakeoffRequest(Base, TimestampMixin):
    __tablename__ = "takeoff_requests"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    design_id: Mapped[str] = mapped_column(ForeignKey("energy_system_designs.id"), index=True)
    status: Mapped[str] = mapped_column(String)
    requested_by: Mapped[str] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_origin: Mapped[str] = mapped_column(
        String, default=FactLifecycleState.user_created.value, index=True
    )

    design: Mapped["EnergySystemDesign"] = relationship("EnergySystemDesign", back_populates="takeoff_requests")
    line_items: Mapped[List["TakeoffLineItem"]] = relationship(
        "TakeoffLineItem", back_populates="takeoff_request", cascade="all, delete-orphan"
    )


class TakeoffLineItem(Base, TimestampMixin):
    __tablename__ = "takeoff_line_items"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    takeoff_request_id: Mapped[str] = mapped_column(ForeignKey("takeoff_requests.id"), index=True)
    category: Mapped[str] = mapped_column(String)
    item_name: Mapped[str] = mapped_column(String)
    quantity: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String)
    unit_cost_placeholder: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    total_cost_placeholder: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    assumptions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_origin: Mapped[str] = mapped_column(
        String, default=FactLifecycleState.user_created.value, index=True
    )

    takeoff_request: Mapped["TakeoffRequest"] = relationship("TakeoffRequest", back_populates="line_items")


class EstimatedPathway(Base, TimestampMixin):
    __tablename__ = "estimated_pathways"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    home_id: Mapped[str] = mapped_column(ForeignKey("homes.id"), index=True)
    design_id: Mapped[Optional[str]] = mapped_column(ForeignKey("energy_system_designs.id"), nullable=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    lifecycle_stage: Mapped[str] = mapped_column(String, default="concept")
    source_location: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    destination_location: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    estimated_distance_ft: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    route_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    route_difficulty: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    visibility_level: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    confidence_level: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    upfront_cost_placeholder: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    estimated_monthly_savings_placeholder: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    resilience_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_origin: Mapped[str] = mapped_column(
        String, default=FactLifecycleState.user_created.value, index=True
    )

    home: Mapped["Home"] = relationship("Home", back_populates="estimated_pathways")
    design: Mapped[Optional["EnergySystemDesign"]] = relationship(
        "EnergySystemDesign", back_populates="estimated_pathways"
    )


class LoadTemplate(Base, TimestampMixin):
    __tablename__ = "load_templates"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    account_id: Mapped[Optional[str]] = mapped_column(ForeignKey("accounts.id"), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    running_watts: Mapped[float] = mapped_column(Float)
    surge_watts: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    estimated_daily_hours: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    backup_priority: Mapped[str] = mapped_column(String)
    phase_type: Mapped[str] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_origin: Mapped[str] = mapped_column(
        String, default=FactLifecycleState.user_created.value, index=True
    )


class DesignGoalPreset(Base, TimestampMixin):
    __tablename__ = "design_goal_presets"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    design_goal: Mapped[str] = mapped_column(String)
    architecture_type: Mapped[str] = mapped_column(String)
    summary: Mapped[str] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_origin: Mapped[str] = mapped_column(
        String, default=FactLifecycleState.user_created.value, index=True
    )


class SourceDocument(Base, TimestampMixin):
    __tablename__ = "source_documents"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    source_type: Mapped[str] = mapped_column(String, index=True)
    manufacturer: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    product_model: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    file_reference: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    version: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    published_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    retrieved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    verification_status: Mapped[str] = mapped_column(String, index=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_origin: Mapped[str] = mapped_column(
        String, default=FactLifecycleState.user_created.value, index=True
    )


class DataProvenance(Base, TimestampMixin):
    __tablename__ = "data_provenance"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    entity_type: Mapped[str] = mapped_column(String, index=True)
    entity_id: Mapped[str] = mapped_column(String, index=True)
    field_name: Mapped[str] = mapped_column(String, index=True)
    source_document_id: Mapped[Optional[str]] = mapped_column(ForeignKey("source_documents.id"), nullable=True, index=True)
    source_type: Mapped[str] = mapped_column(String, index=True)
    trust_state: Mapped[str] = mapped_column(String, index=True)
    value_snapshot: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    confidence_level: Mapped[str] = mapped_column(String, index=True)
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    source_document: Mapped[Optional["SourceDocument"]] = relationship("SourceDocument")


class RuleProvenance(Base, TimestampMixin):
    __tablename__ = "rule_provenance"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    rule_key: Mapped[str] = mapped_column(String, index=True)
    rule_name: Mapped[str] = mapped_column(String)
    source_type: Mapped[str] = mapped_column(String, index=True)
    source_document_id: Mapped[Optional[str]] = mapped_column(ForeignKey("source_documents.id"), nullable=True, index=True)
    trust_state: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    source_document: Mapped[Optional["SourceDocument"]] = relationship("SourceDocument")

from datetime import datetime
from typing import List, Optional

from pydantic import Field

from app.core.schemas import ORMModel
from app.core.types import DataOrigin


class HorizonPoint(ORMModel):
    azimuth_degrees: float
    elevation_degrees: float


class RoofPlaneBase(ORMModel):
    home_id: str
    name: str
    area_sqft: float
    azimuth_degrees: float
    pitch_degrees: float
    usable_area_sqft: Optional[float] = None
    horizon_trace: List[HorizonPoint] = Field(default_factory=list)
    notes: Optional[str] = None
    data_origin: DataOrigin = DataOrigin.user_created


class RoofPlaneCreate(RoofPlaneBase):
    id: str


class RoofPlane(RoofPlaneBase):
    id: str
    created_at: datetime
    updated_at: datetime


class GeometryObstructionBase(ORMModel):
    home_id: str
    name: str
    obstruction_type: str
    approximate_height_ft: Optional[float] = None
    azimuth_degrees: Optional[float] = None
    distance_ft: Optional[float] = None
    notes: Optional[str] = None
    data_origin: DataOrigin = DataOrigin.user_created


class GeometryObstructionCreate(GeometryObstructionBase):
    id: str


class GeometryObstruction(GeometryObstructionBase):
    id: str
    created_at: datetime
    updated_at: datetime


class RoofPlaneShading(ORMModel):
    roof_plane_id: str
    derate_fraction: float
    production_factor: float
    basis: str


class HomeGeometryExport(ORMModel):
    home_id: str
    roof_planes: List[RoofPlane]
    obstructions: List[GeometryObstruction]
    per_plane_shading: List[RoofPlaneShading]
    home_diagram_format: str = "home_diagram_geometry_v1"
    limitations: List[str] = Field(default_factory=list)

from typing import List

from sqlalchemy.orm import Session

from app.core.repository import repository
from app.engines.calculator_primitives import tier1_shading_derate
from app.geometry.schemas import HomeGeometryExport, RoofPlane, RoofPlaneShading


class GeometryService:
    def export_home_geometry(self, db: Session, home_id: str) -> HomeGeometryExport:
        planes = [RoofPlane.model_validate(plane) for plane in repository.list_roof_planes(db, home_id)]
        obstructions = repository.list_geometry_obstructions(db, home_id)
        shading = self._per_plane_shading(planes)
        return HomeGeometryExport(
            home_id=home_id,
            roof_planes=planes,
            obstructions=obstructions,
            per_plane_shading=shading,
            limitations=[
                "Geometry is a planning model, not field verification.",
                "Per-plane shading uses tier-1 horizon traces only.",
                "No satellite, lidar, permit, AHJ, or utility validation is performed.",
            ],
        )

    def _per_plane_shading(self, planes: List[RoofPlane]) -> List[RoofPlaneShading]:
        results: List[RoofPlaneShading] = []
        for plane in planes:
            trace = [(point.azimuth_degrees, point.elevation_degrees) for point in plane.horizon_trace]
            derate = tier1_shading_derate(trace)
            results.append(
                RoofPlaneShading(
                    roof_plane_id=plane.id,
                    derate_fraction=derate.derate_fraction,
                    production_factor=derate.production_factor,
                    basis=derate.reason,
                )
            )
        return results


geometry_service = GeometryService()

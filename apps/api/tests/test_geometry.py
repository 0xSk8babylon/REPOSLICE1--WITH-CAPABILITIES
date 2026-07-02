import unittest

from sqlalchemy.orm import Session  # noqa: E402

import tests.fast_db  # noqa: F401, E402
from app.core import models  # noqa: E402
from app.core.database import engine  # noqa: E402
from app.geometry.router import (  # noqa: E402
    create_obstruction,
    create_roof_plane,
    export_geometry,
    list_obstructions,
    list_roof_planes,
)
from app.geometry.schemas import GeometryObstructionCreate, HorizonPoint, RoofPlaneCreate  # noqa: E402
from app.main import app  # noqa: E402

HOME_ID = "home_001"


class GeometryTests(unittest.TestCase):
    def setUp(self):
        with Session(engine) as db:
            db.query(models.GeometryObstruction).delete()
            db.query(models.RoofPlane).delete()
            db.commit()

    def test_route_registration(self):
        paths = set(app.openapi()["paths"])
        self.assertIn("/api/homes/{home_id}/geometry/roof-planes", paths)
        self.assertIn("/api/homes/{home_id}/geometry/obstructions", paths)
        self.assertIn("/api/homes/{home_id}/geometry/export", paths)

    def test_roof_planes_and_obstructions_are_storable_and_queryable(self):
        plane = RoofPlaneCreate(
            id="plane_south",
            home_id=HOME_ID,
            name="South roof",
            area_sqft=500,
            usable_area_sqft=420,
            azimuth_degrees=180,
            pitch_degrees=24,
            horizon_trace=[HorizonPoint(azimuth_degrees=180, elevation_degrees=18)],
        )
        obstruction = GeometryObstructionCreate(
            id="tree_south",
            home_id=HOME_ID,
            name="South tree",
            obstruction_type="tree",
            approximate_height_ft=35,
            azimuth_degrees=180,
            distance_ft=45,
        )

        with Session(engine) as db:
            create_roof_plane(HOME_ID, plane, db)
            create_obstruction(HOME_ID, obstruction, db)
            planes = list_roof_planes(HOME_ID, db)
            obstructions = list_obstructions(HOME_ID, db)

        self.assertEqual(["plane_south"], [item.id for item in planes])
        self.assertEqual(["tree_south"], [item.id for item in obstructions])

    def test_geometry_export_feeds_per_plane_shading(self):
        plane = RoofPlaneCreate(
            id="plane_west",
            home_id=HOME_ID,
            name="West roof",
            area_sqft=300,
            azimuth_degrees=270,
            pitch_degrees=18,
            horizon_trace=[
                HorizonPoint(azimuth_degrees=260, elevation_degrees=0),
                HorizonPoint(azimuth_degrees=280, elevation_degrees=90),
            ],
        )

        with Session(engine) as db:
            create_roof_plane(HOME_ID, plane, db)
            exported = export_geometry(HOME_ID, db)

        self.assertEqual("home_diagram_geometry_v1", exported.home_diagram_format)
        self.assertEqual(1, len(exported.roof_planes))
        self.assertEqual(0.5, exported.per_plane_shading[0].derate_fraction)
        self.assertIn("planning model", exported.limitations[0])


if __name__ == "__main__":
    unittest.main()

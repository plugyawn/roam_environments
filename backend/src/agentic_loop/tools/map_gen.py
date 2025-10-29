"""Map generation tool using shapely for spline and region construction."""

from __future__ import annotations

import math
from typing import Dict, List, Tuple

from shapely.affinity import translate
from shapely.geometry import LineString, Polygon


def generate_map(scene_spec: Dict) -> Dict:
    """Produce a terrain plan with labelled regions and a river spline."""

    width = 240
    height = 240
    half_w = width / 2
    half_h = height / 2

    base_polygon = Polygon([(-half_w, -half_h), (half_w, -half_h), (half_w, half_h), (-half_w, half_h)])

    market = _central_square(base_polygon, size=40)
    residential = translate(market.buffer(60, cap_style=3, join_style=2), yoff=-40).intersection(base_polygon)
    farmland = translate(market.buffer(80, cap_style=3, join_style=2), yoff=70).intersection(base_polygon)
    pasture = translate(market.buffer(100, cap_style=3, join_style=2), xoff=-60).intersection(base_polygon)

    regions = _serialize_regions(
        {
            "market": market,
            "residential": residential,
            "farmland": farmland,
            "pasture": pasture,
        }
    )

    spline = _river_spline(base_polygon)
    splines: List[Dict] = [
        {
            "id": "spl:river1",
            "type": "river",
            "points": [[x, 0.0, y] for x, y in spline.coords],
        }
    ]

    return {
        "size": {"w": width, "h": height, "units": "m"},
        "terrain": {"type": "flat", "elevation": 0},
        "regions": regions,
        "splines": splines,
    }


def _central_square(area: Polygon, size: float) -> Polygon:
    half = size / 2
    square = Polygon([(-half, -half), (half, -half), (half, half), (-half, half)])
    return square.intersection(area)


def _river_spline(area: Polygon) -> LineString:
    minx, miny, maxx, maxy = area.bounds
    start = (minx + 20, miny)
    mid1 = ((minx + maxx) / 2 - 30, (miny + maxy) / 2 - 10)
    mid2 = ((minx + maxx) / 2 + 40, (miny + maxy) / 2 + 30)
    end = (maxx - 20, maxy)
    return LineString([start, mid1, mid2, end])


def _serialize_regions(regions: Dict[str, Polygon]) -> List[Dict]:
    serialized: List[Dict] = []
    for idx, (label, polygon) in enumerate(regions.items(), start=1):
        if polygon.is_empty:
            continue
        coords = [(float(x), float(y)) for x, y in polygon.exterior.coords[:-1]]
        serialized.append(
            {
                "id": f"region:{label}:{idx}",
                "label": label,
                "polygon": coords,
            }
        )
    return serialized

"""Map generation tool using shapely for basic region construction."""

from __future__ import annotations

from typing import Dict, List

from shapely.affinity import translate
from shapely.geometry import Polygon


def generate_map(scene_spec: Dict) -> Dict:
    """Produce a terrain plan with labelled regions."""

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

    return {
        "size": {"w": width, "h": height, "units": "m"},
        "terrain": {"type": "flat", "elevation": 0},
        "regions": regions,
    }


def _central_square(area: Polygon, size: float) -> Polygon:
    half = size / 2
    square = Polygon([(-half, -half), (half, -half), (half, half), (-half, half)])
    return square.intersection(area)


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

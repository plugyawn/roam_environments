"""Utilities for chunking scene data into doc cards."""

from __future__ import annotations

from typing import Dict, Iterable, List


def shard_scene_graph(scene_graph: Dict) -> List[Dict]:
    """Break a scene graph into shard documents suited for retrieval."""

    shards: List[Dict] = []
    for placement in scene_graph.get("placements", []):
        ref = placement.get("ref")
        shards.append(
            {
                "id": f"placement:{ref}",
                "type": "placement",
                "tags": [ref],
                "content": str(placement),
            }
        )
    for asset_id in scene_graph.get("assets", []):
        shards.append(
            {
                "id": f"asset:{asset_id}",
                "type": "asset",
                "tags": [asset_id],
                "content": asset_id,
            }
        )
    return shards

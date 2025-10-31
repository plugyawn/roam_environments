"""Fallback pipeline that exercises the local tools without Magentic-One."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Dict, List

from ..config import RuntimeConfig
from ..tools.assets import compile_asset, expand_assets
from ..tools.map_gen import generate_map
from ..tools.persistence import persist_run
from ..tools.placement import place_assets
from ..tools.render import render_snapshot, render_web_view
from ..tools.scene_spec import design_scene_spec
from ..tools.scene_diff import apply_scene_diff, initialize_scene
from ..tools.validation import validate_scene

LOGGER = logging.getLogger(__name__)


def fallback_run(prompt: str, config: RuntimeConfig) -> Dict:
    """Produce a minimal scene graph by chaining tool calls directly."""

    LOGGER.info("Executing fallback pipeline for prompt: %s", prompt)
    requirements = _seed_requirements(prompt)
    init_payload = initialize_scene(prompt=prompt)
    scene_state = init_payload["scene_state"]

    scene_spec = design_scene_spec(requirements)
    recipes = expand_assets(scene_spec)
    manifests: List[Dict] = [compile_asset(recipe) for recipe in recipes]
    asset_ids = [manifest["id"] for manifest in manifests]
    map_plan = generate_map(scene_spec)
    placements = place_assets(map_plan, asset_ids)

    diff_result = apply_scene_diff(
        scene_state,
        {"assets": manifests, "placements": placements},
        allow_overwrite=True,
        purge_orphans=False,
    )
    scene_state = diff_result["scene_state"]
    scene_graph = scene_state.get("scene_graph", {})
    scene_graph["map"] = map_plan

    run_id = datetime.utcnow().strftime("run_%Y%m%d_%H%M%S")
    metadata = scene_state.setdefault("metadata", {})
    metadata.update({"run_id": run_id, "prompt": prompt})
    graph_meta = scene_graph.setdefault("metadata", {})
    graph_meta.update({"run_id": run_id, "template": init_payload.get("template")})

    validation = validate_scene(scene_graph, requirements)
    manifest_payload = {
        "run_id": run_id,
        "prompt": prompt,
        "requirements": requirements,
        "scene_spec": scene_spec,
        "assets": scene_state.get("assets", manifests),
        "map_plan": map_plan,
        "scene_graph": scene_graph,
        "validation": validation,
        "metadata": metadata,
    }
    manifest_info = persist_run(manifest_payload)
    viewer_info: Dict[str, str] = {}
    manifest_path = manifest_info.get("manifest_path")
    if manifest_path:
        try:
            viewer_info = render_web_view(manifest_payload, manifest_path)
        except Exception as exc:  # pragma: no cover - defensive logging
            LOGGER.warning("Failed to render interactive viewer for %s: %s", run_id, exc)
    snapshot_info = render_snapshot(scene_graph)
    return {
        "run_id": run_id,
        "prompt": prompt,
        "requirements": requirements,
        "scene_spec": scene_spec,
    "assets": scene_state.get("assets", manifests),
        "map_plan": map_plan,
        "scene_graph": scene_graph,
        "validation": validation,
        "manifest_path": manifest_info.get("manifest_path"),
        "snapshot_path": snapshot_info.get("snapshot_path"),
        **viewer_info,
    }


def _seed_requirements(prompt: str) -> Dict:
    keywords = {
        "house": 10,
        "tree": 50,
        "river": 1,
        "market": 1,
        "cow": 6,
        "person": 20,
    }
    requirements = []
    lowered = prompt.lower()
    for concept, default_count in keywords.items():
        if concept in lowered or concept == "house":  # always include houses
            req = {"concept": concept, "min_count": default_count}
            if concept == "river":
                req["exactly"] = 1
                req["must_cross_map"] = True
            requirements.append(req)
    return {"requirements": requirements}

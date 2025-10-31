"""Scene graph initialization and diff application utilities."""

from __future__ import annotations

import ast
import json
from copy import deepcopy
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from .placement import place_assets
from ..orchestrator.templates import TEMPLATE_CATALOG, TemplateSpec


def initialize_scene(*, prompt: str, template: str | None = None) -> Dict:
    """Bootstrap a scene graph using the specified template layout."""

    prompt_text = (prompt or "").strip()
    template_spec = _select_template(template)

    metadata = {
        "prompt": prompt_text,
        "template": template_spec.name,
        "template_description": template_spec.description,
    }

    map_plan = {
        "template": template_spec.name,
        "description": template_spec.description,
        "base_terrain": template_spec.base_terrain,
        "seed_assets": list(template_spec.seed_assets),
        "mutation_ideas": list(template_spec.mutation_ideas),
    }

    scene_graph = {
        "metadata": metadata.copy(),
        "placements": [],
        "assets": [],
        "map": map_plan,
    }

    # Track template seed ids for reference; compiled assets join later via apply_scene_diff.
    state: Dict = {
        "metadata": metadata,
        "scene_graph": scene_graph,
        "assets": [],
        "template_seeds": list(template_spec.seed_assets),
    }

    return {
        "scene_state": state,
        "template": template_spec.name,
        "seed_assets": list(template_spec.seed_assets),
        "message": f"Initialized scene with template '{template_spec.name}'.",
    }


def apply_scene_diff(
    scene_state: Dict | str | Any,
    diff: Dict | str | Any,
    *,
    allow_overwrite: bool = False,
    purge_orphans: bool = False,
) -> Dict:
    """Merge assets and placements into an existing scene graph.

    The diff payload can include the following optional keys:
      - "assets": list of asset manifests/dicts to merge (requires "id" per asset)
      - "placements": list of placement entries (ref/asset_id + transform)
      - "remove_assets": list of asset ids to delete
      - "remove_placements": list of placement refs or indices to delete
    """

    state = _coerce_state(scene_state)
    mutations = _coerce_state(diff)

    scene_graph = state.setdefault("scene_graph", {})
    scene_graph.setdefault("placements", [])
    scene_graph.setdefault("assets", [])
    state.setdefault("assets", [])

    report = {
        "assets_added": 0,
        "assets_overwritten": 0,
        "assets_removed": 0,
        "placements_added": 0,
        "placements_removed": 0,
    }

    # Handle asset removals first to avoid re-adding immediately.
    removed_assets = _ensure_list(mutations.get("remove_assets"))
    if removed_assets:
        removed_ids = set(str(asset_id) for asset_id in removed_assets if str(asset_id).strip())
        if removed_ids:
            report["assets_removed"] = _purge_assets(state, removed_ids, purge_orphans)

    # Merge assets supplied in the diff.
    new_assets = _ensure_list(mutations.get("assets"))
    if new_assets:
        added, overwritten = _merge_assets(state, new_assets, allow_overwrite=allow_overwrite)
        report["assets_added"] += added
        report["assets_overwritten"] += overwritten

    # Merge placements.
    new_placements = _ensure_list(mutations.get("placements"))
    if new_placements:
        normalised = place_assets(placements=new_placements, asset_ids=None)
        scene_graph["placements"].extend(normalised)
        report["placements_added"] += len(normalised)
        _sync_asset_ids(scene_graph, state)

    removed_placements = _ensure_list(mutations.get("remove_placements"))
    if removed_placements:
        removed = _remove_placements(scene_graph, removed_placements)
        report["placements_removed"] += removed

    totals = _current_totals(state)
    report.update(totals)

    return {
        "scene_state": state,
        "report": report,
    }


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _select_template(template_name: Optional[str]) -> TemplateSpec:
    if template_name:
        lookup = template_name.strip().lower()
        for template in TEMPLATE_CATALOG:
            if template.name.lower() == lookup:
                return template
    # Fallback to the first template if none specified or not found.
    return TEMPLATE_CATALOG[0]


def _coerce_state(payload: Any) -> Dict:
    if isinstance(payload, dict):
        return deepcopy(payload)
    if isinstance(payload, str):
        trimmed = payload.strip()
        if not trimmed:
            return {}
        try:
            parsed = json.loads(trimmed)
        except json.JSONDecodeError:
            try:
                parsed = ast.literal_eval(trimmed)
            except (ValueError, SyntaxError):
                raise ValueError("Scene state payload must be a dict or JSON string") from None
        if isinstance(parsed, dict):
            return deepcopy(parsed)
    raise ValueError("Scene state payload must be a dict or JSON string")


def _ensure_list(value: Any) -> List:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def _merge_assets(state: Dict, assets: Sequence[Any], *, allow_overwrite: bool) -> Tuple[int, int]:
    scene_assets: List[Dict] = state.setdefault("assets", [])
    scene_graph_assets: List[str] = state.setdefault("scene_graph", {}).setdefault("assets", [])

    added = 0
    overwritten = 0
    existing_index = {entry.get("id"): idx for idx, entry in enumerate(scene_assets) if isinstance(entry, dict) and entry.get("id")}

    for asset in assets:
        if not isinstance(asset, dict):
            continue
        asset_id = asset.get("id")
        if not isinstance(asset_id, str) or not asset_id.strip():
            continue
        asset_id = asset_id.strip()
        if asset_id in existing_index:
            if allow_overwrite:
                scene_assets[existing_index[asset_id]] = asset
                overwritten += 1
            else:
                continue
        else:
            scene_assets.append(asset)
            existing_index[asset_id] = len(scene_assets) - 1
            added += 1
        if asset_id not in scene_graph_assets:
            scene_graph_assets.append(asset_id)

    return added, overwritten


def _purge_assets(state: Dict, asset_ids: Iterable[str], purge_orphans: bool) -> int:
    asset_id_set = set(asset_ids)
    scene_assets: List[Dict] = state.setdefault("assets", [])
    scene_graph = state.setdefault("scene_graph", {})
    graph_assets: List[str] = scene_graph.setdefault("assets", [])

    # Remove from manifests
    original_len = len(scene_assets)
    scene_assets[:] = [asset for asset in scene_assets if str(asset.get("id")) not in asset_id_set]
    removed = original_len - len(scene_assets)

    # Remove from scene graph asset list
    graph_assets[:] = [asset_id for asset_id in graph_assets if asset_id not in asset_id_set]

    if purge_orphans:
        placements: List[Dict] = scene_graph.setdefault("placements", [])
        placements[:] = [placement for placement in placements if _extract_ref(placement) not in asset_id_set]

    return removed


def _remove_placements(scene_graph: Dict, removals: Sequence[Any]) -> int:
    placements: List[Dict] = scene_graph.setdefault("placements", [])
    if not placements:
        return 0

    removal_refs: set[str] = set()
    removal_indices: set[int] = set()

    for item in removals:
        if isinstance(item, int):
            removal_indices.add(item)
        elif isinstance(item, str) and item.strip():
            removal_refs.add(item.strip())
        elif isinstance(item, dict):
            ref = _extract_ref(item)
            if ref:
                removal_refs.add(ref)

    if not removal_refs and not removal_indices:
        return 0

    retained: List[Dict] = []
    removed = 0
    for index, placement in enumerate(placements):
        ref = _extract_ref(placement)
        if index in removal_indices or (ref and ref in removal_refs):
            removed += 1
        else:
            retained.append(placement)
    placements[:] = retained
    return removed


def _extract_ref(placement: Any) -> Optional[str]:
    if not isinstance(placement, dict):
        return None
    for key in ("ref", "asset_id", "asset", "id"):
        value = placement.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _current_totals(state: Dict) -> Dict[str, Any]:
    scene_graph = state.get("scene_graph") or {}
    placements = scene_graph.get("placements") or []
    asset_ids = scene_graph.get("assets") or []
    return {
        "total_placements": len(placements),
        "total_assets": len(asset_ids),
        "asset_ids": list(asset_ids),
    }


def _sync_asset_ids(scene_graph: Dict, state: Dict) -> None:
    """Ensure scene_graph['assets'] mirrors the ids present in state['assets']."""

    manifests = state.get("assets") or []
    asset_ids: List[str] = []
    for manifest in manifests:
        if isinstance(manifest, dict):
            asset_id = manifest.get("id")
            if isinstance(asset_id, str) and asset_id.strip():
                asset_ids.append(asset_id.strip())
    existing = set(asset_ids)

    for placement in scene_graph.get("placements", []):
        ref = _extract_ref(placement)
        if ref and ref not in existing:
            asset_ids.append(ref)
            existing.add(ref)

    scene_graph["assets"] = asset_ids
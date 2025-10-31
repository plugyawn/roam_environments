"""Auditing helpers that enforce asset and placement quotas."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Sequence, Set

MIN_REQUIRED_ASSETS = 12
MIN_REQUIRED_PLACEMENTS = 20
REQUIRED_FEATURE_ASSETS = 10
REQUIRED_ROAD_PLACEMENTS = 5


def audit_asset_requirements(state: Dict) -> Dict:
    """Evaluate whether a scene satisfies asset and placement quotas."""

    if not isinstance(state, dict):
        raise ValueError("audit_asset_requirements expects a dict payload")

    scene_graph = state.get("scene_graph")
    if not isinstance(scene_graph, dict) and _looks_like_scene_graph(state):
        scene_graph = state

    assets_section = state.get("assets")
    return _evaluate(scene_graph or {}, assets_section)


def _looks_like_scene_graph(candidate: Dict) -> bool:
    if not isinstance(candidate, dict):
        return False
    if isinstance(candidate.get("placements"), Sequence):
        return True
    if isinstance(candidate.get("assets"), Sequence):
        return True
    if isinstance(candidate.get("map"), dict):
        return True
    return False


def _evaluate(scene_graph: Dict, assets_section: Any) -> Dict:
    placements = _extract_placements(scene_graph)
    unique_assets = _collect_asset_ids(assets_section, scene_graph)
    coverage = {asset_id: 0 for asset_id in unique_assets}

    placement_refs: List[str] = []
    road_placement_count = 0
    for placement in placements:
        asset_ref = _extract_asset_ref(placement)
        if not asset_ref:
            continue
        placement_refs.append(asset_ref)
        if asset_ref in coverage:
            coverage[asset_ref] += 1
        if _is_road(asset_ref):
            road_placement_count += 1

    placement_count = len(placements)
    unique_asset_count = len(unique_assets)

    messages: List[str] = []
    status = "pass"

    if unique_asset_count < MIN_REQUIRED_ASSETS:
        status = "fail"
        messages.append(
            f"Scene requires at least {MIN_REQUIRED_ASSETS} unique assets but only {unique_asset_count} are present."
        )

    if placement_count < MIN_REQUIRED_PLACEMENTS:
        status = "fail"
        messages.append(
            f"Scene requires at least {MIN_REQUIRED_PLACEMENTS} placements but only {placement_count} are defined."
        )

    feature_assets = [asset_id for asset_id in unique_assets if not _is_road(asset_id) and not _is_background(asset_id)]
    if len(feature_assets) < REQUIRED_FEATURE_ASSETS:
        status = "fail"
        messages.append(
            f"Need at least {REQUIRED_FEATURE_ASSETS} non-road, non-background assets but found {len(feature_assets)}."
        )

    if not any(_is_background(asset_id) for asset_id in unique_assets):
        status = "fail"
        messages.append("Missing background asset (id containing 'background').")

    if not any(_is_road(asset_id) for asset_id in unique_assets):
        status = "fail"
        messages.append("No road asset defined; include a road primitive asset id.")

    if road_placement_count < REQUIRED_ROAD_PLACEMENTS:
        status = "fail"
        messages.append(
            f"Road assets must have at least {REQUIRED_ROAD_PLACEMENTS} placements; only {road_placement_count} recorded."
        )

    missing_assets = [asset_id for asset_id, count in coverage.items() if count == 0]
    if missing_assets:
        status = "fail"
        preview = ", ".join(missing_assets[:5])
        suffix = "..." if len(missing_assets) > 5 else ""
        messages.append(f"{len(missing_assets)} assets are unplaced: {preview}{suffix}.")

    return {
        "status": status,
        "unique_asset_count": unique_asset_count,
        "placement_count": placement_count,
        "min_assets": MIN_REQUIRED_ASSETS,
        "min_placements": MIN_REQUIRED_PLACEMENTS,
        "road_placement_count": road_placement_count,
        "unplaced_assets": missing_assets,
        "placement_refs": placement_refs,
        "asset_ids": sorted(unique_assets),
        "messages": messages,
    }


def _extract_placements(scene_graph: Dict) -> List[Dict]:
    raw = scene_graph.get("placements") if isinstance(scene_graph, dict) else None
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes, bytearray)):
        return []
    placements: List[Dict] = []
    for entry in raw:
        if isinstance(entry, dict):
            placements.append(entry)
    return placements


def _collect_asset_ids(assets_section: Any, scene_graph: Dict) -> Set[str]:
    asset_ids: Set[str] = set()

    for token in _iterate_candidates(assets_section):
        asset_id = _extract_asset_id(token)
        if asset_id:
            asset_ids.add(asset_id)

    if asset_ids:
        return asset_ids

    scene_assets = scene_graph.get("assets") if isinstance(scene_graph, dict) else None
    for token in _iterate_candidates(scene_assets):
        asset_id = _extract_asset_id(token)
        if asset_id:
            asset_ids.add(asset_id)

    if asset_ids:
        return asset_ids

    placements = scene_graph.get("placements") if isinstance(scene_graph, dict) else None
    if isinstance(placements, Sequence):
        for entry in placements:
            if isinstance(entry, dict):
                ref = _extract_asset_ref(entry)
                if ref:
                    asset_ids.add(ref)

    return asset_ids


def _iterate_candidates(value: Any) -> Iterable[Any]:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return value
    return [value]


def _extract_asset_id(candidate: Any) -> str | None:
    if isinstance(candidate, str) and candidate.strip():
        return candidate.strip()
    if isinstance(candidate, dict):
        for key in ("id", "asset_id", "ref", "name"):
            value = candidate.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return None


def _extract_asset_ref(placement: Dict) -> str | None:
    for key in ("ref", "asset_id", "asset", "id"):
        value = placement.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _is_road(identifier: str) -> bool:
    return "road" in identifier.lower()


def _is_background(identifier: str) -> bool:
    lower = identifier.lower()
    return "background" in lower or lower.endswith(":bg")


__all__ = [
    "MIN_REQUIRED_ASSETS",
    "MIN_REQUIRED_PLACEMENTS",
    "REQUIRED_FEATURE_ASSETS",
    "REQUIRED_ROAD_PLACEMENTS",
    "audit_asset_requirements",
]

#!/usr/bin/env python3
"""Quick collision fixer for run manifests.

Usage:
  python tools/fix_collisions.py /absolute/path/to/manifest.json

Behavior:
  - Loads the manifest, examines `validation.issues` for `collision` entries.
  - For each reported collision, nudges the second placement away along the axis with larger overlap.
  - Recomputes validation with `validate_scene`, persists a new manifest with scene_id suffix `_fixed`,
    and emits viewer + snapshot using the existing renderer helpers.

This is a pragmatic helper for interactive debugging; it performs conservative nudges (+1m buffer)
so it may not resolve dense conflicts fully but should address large overlaps.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Local imports from the backend package
try:
    from agentic_loop.tools.validation import validate_scene
    from agentic_loop.tools.persistence import persist_run
    from agentic_loop.tools.render import render_web_view, render_snapshot
except Exception as exc:  # pragma: no cover - best effort in developer environment
    raise


def _load_manifest(path: Path) -> Dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _get_pos(entry: Dict[str, Any]) -> List[float]:
    # placements sometimes use 'pos' or 'position'
    if isinstance(entry.get("pos"), list):
        return entry["pos"]
    if isinstance(entry.get("position"), list):
        return entry["position"]
    # fallback to [0,0,0]
    entry["pos"] = [0.0, 0.0, 0.0]
    return entry["pos"]


def _set_pos(entry: Dict[str, Any], pos: List[float]) -> None:
    if "pos" in entry:
        entry["pos"] = pos
    else:
        entry["position"] = pos


def _apply_nudge(placements: List[Dict[str, Any]], first: Dict, second: Dict, overlap: Tuple[float, float, float]) -> bool:
    # first/second context provide 'index' and 'center'
    i_first = first.get("index")
    i_second = second.get("index")
    if i_first is None or i_second is None:
        return False
    if not (0 <= i_first < len(placements) and 0 <= i_second < len(placements)):
        return False

    place_first = placements[i_first]
    place_second = placements[i_second]

    pos_first = _get_pos(place_first)
    pos_second = _get_pos(place_second)

    ox, oy, oz = (float(overlap[0]), float(overlap[1]), float(overlap[2]))

    # choose axis with larger overlap (x vs z)
    # use sign from centers to push second away from first
    dx = float(pos_second[0]) - float(pos_first[0])
    dz = float(pos_second[2]) - float(pos_first[2])

    if ox >= oz:
        # shift on X
        sign = 1.0 if dx >= 0 else -1.0
        shift = (ox + 1.0) * sign
        pos_second[0] = float(pos_second[0]) + shift
    else:
        sign = 1.0 if dz >= 0 else -1.0
        shift = (oz + 1.0) * sign
        pos_second[2] = float(pos_second[2]) + shift

    _set_pos(place_second, pos_second)
    return True


def fix_manifest(manifest_path: Path) -> Dict[str, Any]:
    manifest = _load_manifest(manifest_path)
    scene_graph = manifest.get("scene_graph") or {}
    requirements = manifest.get("requirements") or {}
    assets = manifest.get("assets") or []

    validation = manifest.get("validation") or validate_scene(scene_graph, requirements, assets)
    issues = validation.get("issues", [])
    placements = scene_graph.get("placements") or []

    collision_issues = [iss for iss in issues if iss.get("code") == "collision"]
    if not collision_issues:
        return {"status": "noop", "message": "No collisions found in manifest validation", "manifest_path": str(manifest_path)}

    moved_indices = set()
    for issue in collision_issues:
        ctx = issue.get("context", {})
        first = ctx.get("first", {})
        second = ctx.get("second", {})
        overlap = ctx.get("overlap") or (0.0, 0.0, 0.0)
        i_second = second.get("index")
        if i_second in moved_indices:
            # already nudged this placement; skip
            continue
        ok = _apply_nudge(placements, first, second, overlap)
        if ok:
            moved_indices.add(i_second)

    # update manifest and recompute validation
    manifest["scene_graph"]["placements"] = placements
    new_scene_id = f"{manifest.get('scene_id','run')}_fixed"
    manifest["scene_id"] = new_scene_id

    new_validation = validate_scene(scene_graph, requirements, assets)
    manifest["validation"] = new_validation

    # persist new manifest
    persisted = persist_run({
        "scene_id": new_scene_id,
        "prompt": manifest.get("prompt"),
        "requirements": manifest.get("requirements"),
        "scene_spec": manifest.get("scene_spec"),
        "assets": manifest.get("assets"),
        "map_plan": manifest.get("map_plan"),
        "scene_graph": manifest.get("scene_graph"),
        "validation": manifest.get("validation"),
    })

    new_manifest_path = Path(persisted.get("manifest_path"))

    # render viewer + snapshot
    try:
        render_web_view(manifest, str(new_manifest_path))
    except Exception as exc:  # pragma: no cover - best effort
        print(f"Renderer error: {exc}")

    try:
        snap = render_snapshot(scene_graph)
    except Exception as exc:  # pragma: no cover - best effort
        snap = {"snapshot_path": None, "error": str(exc)}

    return {
        "manifest_path": str(new_manifest_path),
        "snapshot_path": snap.get("snapshot_path"),
        "validation": new_validation,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tools/fix_collisions.py /path/to/manifest.json")
        sys.exit(1)
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Manifest not found: {path}")
        sys.exit(2)
    out = fix_manifest(path)
    print(json.dumps(out, indent=2))

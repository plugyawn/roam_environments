"""Asset expansion and compilation tools."""

from __future__ import annotations

import ast
import json
import os
from pathlib import Path
from typing import Dict, Iterable, List

from ..geometry import compile_asset_to_gltf


def expand_assets(scene_spec: Dict, asset_ids: Iterable[str] | None = None) -> List[Dict]:
    """Generate primitive recipes for each entity concept or provided asset ids."""

    recipes: List[Dict] = []

    if asset_ids:
        if isinstance(asset_ids, str):
            asset_ids = _coerce_asset_id_list(asset_ids)
        for asset_id in dict.fromkeys(asset_ids):  # preserve order while removing duplicates
            concept = infer_concept_from_id(asset_id)
            recipe = _default_recipe(concept)
            recipe["id"] = asset_id
            tags = recipe.setdefault("tags", [])
            if concept not in tags:
                tags.append(concept)
            if asset_id not in tags:
                tags.append(asset_id)
            recipes.append(recipe)
        return recipes

    for entity in scene_spec.get("entities", []):
        concept = _extract_concept(entity)
        if not concept:
            continue
        recipe = _default_recipe(concept)
        recipe["id"] = f"asset:{concept}:v1"
        tags = recipe.setdefault("tags", [])
        if concept not in tags:
            tags.append(concept)
        recipes.append(recipe)
    return recipes


def compile_asset(recipe: Dict) -> Dict:
    """Compile a recipe into a glTF asset and register basic metadata."""

    output_dir = _asset_root()
    result = compile_asset_to_gltf(recipe, output_dir)
    manifest = {
        "id": result.asset_id,
        "glb_path": str(result.glb_path),
        "bbox": result.bbox,
        "recipe": recipe,
    }
    _write_manifest(result.asset_id, manifest)
    return manifest


def _default_recipe(concept: str) -> Dict:
    concept = concept.lower()

    if "tree" in concept:
        return {
            "recipe": [
                {"primitive": "cylinder", "name": "trunk", "r": 0.4, "h": 4.5},
                {"primitive": "sphere", "name": "crown", "r": 2.5, "offset": [0, 4.5, 0]},
            ],
            "materials": {"trunk": "bark_brown", "crown": "leaf_green"},
        }

    if "path" in concept or "road" in concept or "trail" in concept:
        return {
            "recipe": [
                {"primitive": "plane", "name": "path", "w": 2.5, "d": 12, "offset": [0, -0.05, 0]},
            ],
            "materials": {"path": "packed_earth"},
        }

    if "bridge" in concept:
        return {
            "recipe": [
                {"primitive": "cuboid", "name": "deck", "w": 14, "h": 0.6, "d": 4, "offset": [0, -0.3, 0]},
                {"primitive": "cuboid", "name": "rail_left", "w": 14, "h": 1.1, "d": 0.25, "offset": [0, 0.55, -1.9]},
                {"primitive": "cuboid", "name": "rail_right", "w": 14, "h": 1.1, "d": 0.25, "offset": [0, 0.55, 1.9]},
            ],
            "materials": {"deck": "wood_oak", "rail_left": "wood_oak", "rail_right": "wood_oak"},
        }

    if "dock" in concept or "pier" in concept:
        return {
            "recipe": [
                {"primitive": "cuboid", "name": "platform", "w": 18, "h": 0.4, "d": 3.5, "offset": [0, -0.2, 0]},
                {"primitive": "cuboid", "name": "posts", "w": 18, "h": 1.0, "d": 0.2, "offset": [0, 0.5, -1.6]},
            ],
            "materials": {"platform": "wood_weathered", "posts": "wood_dark"},
        }

    if "mill" in concept:
        return {
            "recipe": [
                {"primitive": "cuboid", "name": "body", "w": 10, "h": 6, "d": 7},
                {"primitive": "pyramid", "name": "roof", "w": 10.4, "h": 3.2, "d": 7.4, "offset": [0, 6, 0]},
                {"primitive": "cylinder", "name": "wheel", "r": 2.5, "h": 0.6, "offset": [5.3, 1.5, 0]},
            ],
            "materials": {"body": "stone_grey", "roof": "wood_shingle", "wheel": "wood_dark"},
        }

    if "church" in concept or "chapel" in concept or "cathedral" in concept:
        return {
            "recipe": [
                {"primitive": "cuboid", "name": "nave", "w": 12, "h": 8, "d": 22},
                {"primitive": "pyramid", "name": "roof", "w": 12.8, "h": 4.0, "d": 22.8, "offset": [0, 8, 0]},
                {"primitive": "cuboid", "name": "tower", "w": 4, "h": 14, "d": 4, "offset": [-6, 7, 6]},
                {"primitive": "pyramid", "name": "spire", "w": 4.6, "h": 4.5, "d": 4.6, "offset": [-6, 14, 6]},
            ],
            "materials": {
                "nave": "stone_light",
                "roof": "slate_dark",
                "tower": "stone_light",
                "spire": "copper_green",
            },
        }

    if "town_hall" in concept or ("hall" in concept and "town" in concept):
        return {
            "recipe": [
                {"primitive": "cuboid", "name": "body", "w": 14, "h": 7, "d": 10},
                {"primitive": "pyramid", "name": "roof", "w": 14.4, "h": 3.5, "d": 10.4, "offset": [0, 7, 0]},
                {"primitive": "cuboid", "name": "tower", "w": 3, "h": 10, "d": 3, "offset": [0, 8, 0]},
            ],
            "materials": {"body": "stone_grey", "roof": "slate_dark", "tower": "stone_grey"},
        }

    if "inn" in concept or "tavern" in concept or "pub" in concept:
        return {
            "recipe": [
                {"primitive": "cuboid", "name": "body", "w": 12, "h": 5.5, "d": 7},
                {"primitive": "pyramid", "name": "roof", "w": 12.4, "h": 3.0, "d": 7.4, "offset": [0, 5.5, 0]},
                {"primitive": "cuboid", "name": "sign", "w": 0.4, "h": 1.4, "d": 2.4, "offset": [6.4, 3.0, 0]},
            ],
            "materials": {
                "body": "timber_frame",
                "roof": "thatch_warm",
                "sign": "wood_dark",
            },
        }

    if "shop" in concept or "store" in concept or "stall" in concept or "market" in concept:
        return {
            "recipe": [
                {"primitive": "cuboid", "name": "counter", "w": 3.0, "h": 0.9, "d": 2.0},
                {"primitive": "pyramid", "name": "canopy", "w": 3.2, "h": 1.2, "d": 2.2, "offset": [0, 1.8, 0]},
            ],
            "materials": {"counter": "wood_oak", "canopy": "canvas_striped"},
        }

    if "flower" in concept or "garden" in concept or "planter" in concept:
        return {
            "recipe": [
                {"primitive": "cylinder", "name": "bed", "r": 1.2, "h": 0.4},
                {"primitive": "sphere", "name": "blooms", "r": 1.0, "offset": [0, 0.8, 0]},
            ],
            "materials": {"bed": "soil_dark", "blooms": "flower_mix"},
        }

    if "fountain" in concept or "well" in concept:
        return {
            "recipe": [
                {"primitive": "cylinder", "name": "base", "r": 1.5, "h": 0.8},
                {"primitive": "cylinder", "name": "column", "r": 0.4, "h": 1.6, "offset": [0, 0.8, 0]},
                {"primitive": "sphere", "name": "top", "r": 0.5, "offset": [0, 2.0, 0]},
            ],
            "materials": {"base": "stone_light", "column": "stone_light", "top": "copper_green"},
        }

    if "cow" in concept or "livestock" in concept:
        return {
            "recipe": [
                {"primitive": "cuboid", "name": "body", "w": 2.2, "h": 1.4, "d": 4.2},
                {"primitive": "sphere", "name": "head", "r": 0.7, "offset": [0, 1.4, 1.8]},
            ],
            "materials": {"body": "fur_brown", "head": "fur_brown"},
        }

    if any(keyword in concept for keyword in ("house", "res", "home", "cottage", "farm", "hut", "residential")):
        return {
            "recipe": [
                {"primitive": "cuboid", "name": "body", "w": 8.0, "h": 5.0, "d": 6.0},
                {"primitive": "pyramid", "name": "roof", "w": 8.4, "h": 3.0, "d": 6.4, "offset": [0, 5.0, 0]},
                {"primitive": "cuboid", "name": "chimney", "w": 1.0, "h": 2.0, "d": 1.0, "offset": [-2.5, 5.5, 1.5]},
            ],
            "materials": {
                "body": "plaster_white",
                "roof": "terracotta_red",
                "chimney": "brick_red",
            },
        }

    if concept == "river":
        return {
            "recipe": [
                {"primitive": "plane", "name": "surface", "w": 20, "d": 200, "offset": [0, -0.2, 0]},
            ],
            "materials": {"surface": "water_blue"},
        }

    # Fallback simple block
    return {
        "recipe": [
            {"primitive": "cuboid", "name": concept or "asset", "w": 1.0, "h": 1.0, "d": 1.0},
        ],
        "materials": {(concept or "asset"): "default_grey"},
    }


def _write_manifest(asset_id: str, manifest: Dict) -> None:
    root = _asset_root()
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"{asset_id}.json"
    path.write_text(json.dumps(manifest, indent=2))


def _asset_root() -> Path:
    return Path(os.environ.get("ASSET_ROOT", "assets"))


def infer_concept_from_id(asset_id: str) -> str:
    """Heuristically derive an asset concept name from an asset identifier."""

    asset_id = str(asset_id)
    if ":" in asset_id:
        asset_id = asset_id.split(":")[-1]
    asset_id = asset_id.replace("\\", "/").split("/")[-1]
    asset_id = Path(asset_id).stem
    parts = [part.lower() for part in asset_id.split("_") if part]
    core = [part for part in parts if not part.isdigit()]
    if not core:
        core = parts or [asset_id.lower()]
    return "_".join(core)


def _extract_concept(entity: Dict) -> str:
    concept = entity.get("concept") or entity.get("class") or entity.get("type") or entity.get("id")
    if not concept:
        return ""
    return str(concept).strip().lower()


def _coerce_asset_id_list(raw: str) -> List[str]:
    raw = raw.strip()
    if not raw:
        return []
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, list):
            return [str(item).strip() for item in parsed if str(item).strip()]
    except json.JSONDecodeError:
        pass

    try:
        parsed = ast.literal_eval(raw)
        if isinstance(parsed, (list, tuple, set)):
            return [str(item).strip() for item in parsed if str(item).strip()]
    except (ValueError, SyntaxError):
        pass

    tokens = []
    for token in raw.split(","):
        cleaned = token.strip().strip("'\"[]")
        if cleaned:
            tokens.append(cleaned)
    return tokens

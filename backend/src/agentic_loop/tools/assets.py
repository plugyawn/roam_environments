"""Asset expansion, mutation, and compilation tools."""

from __future__ import annotations

import ast
import json
import logging
import os
from copy import deepcopy
from pathlib import Path
from typing import Dict, Iterable, List, MutableMapping, Sequence

from ..geometry import compile_asset_to_gltf
from ..config import RuntimeConfig

LOGGER = logging.getLogger(__name__)

_EXPAND_ASSETS_USAGE = (
    "expand_assets expects a call shaped like {\"tool\": \"expand_assets\", \"args\": {\"scene_spec\": {...}, "
    "\"asset_ids\": [\"primitive:ground_plane_flat\", ...]}}. Provide asset_ids as a JSON array (or omit it to "
    "expand every concept in scene_spec); never wrap the list in quotes. Sample input: {\"tool\": \"expand_assets\", "
    "\"args\": {\"scene_spec\": {\"entities\": [{\"concept\": \"runway\", \"attrs\": {\"tag\": \"asphalt\"}}, {\"concept\": "
    "\"moving_walkway\", \"count\": 2}]}, \"asset_ids\": [\"primitive:ground_plane_flat\", "
    "\"primitive:lane_strip\", \"asset:terminal_sign:v1\"]}}. Sample output: [{\"id\": \"primitive:ground_plane_flat\", "
    "\"recipe\": [...], \"materials\": {...}}, {\"id\": \"asset:terminal_sign:v1\", \"recipe\": [...]}]."
)

_COMPILE_ASSET_USAGE = (
    "compile_asset expects the full recipe dictionary returned by expand_assets or mutate_asset. Example input: {\"tool\": "
    "\"compile_asset\", \"args\": {\"recipe\": {\"id\": \"asset:runway_light:v1\", \"recipe\": [{\"primitive\": \"cylinder\", "
    "\"name\": \"post\", \"r\": 0.15, \"h\": 1.1}], \"materials\": {\"post\": \"aluminum_brushed\"}}, \"metadata\": {\"notes\": \"Generated from expand_assets response\"}}}. Sample output: {\"id\": \"asset:runway_light:v1\", \"glb_path\": \"assets/asset:runway_light:v1.glb\", "
    "\"bbox\": {...}, \"recipe\": {...}}."
)

_MUTATE_ASSET_USAGE = (
    "mutate_asset requires JSON like {\"tool\": \"mutate_asset\", \"args\": {\"base_asset_id\": \"primitive:blocker_cube\", "
    "\"mutation_id\": \"asset:security_arch:v1\", \"scale\": [1.2, 2.0, 0.3], \"material_overrides\": {\"block\": \"metal_brushed\"}}}. "
    "Pass scale as a number or array, not a quoted string; pass material_overrides as an object. Sample input: {\"tool\": "
    "\"mutate_asset\", \"args\": {\"base_asset_id\": \"primitive:lane_strip\", \"mutation_id\": \"asset:walkway_lane:v2\", "
    "\"scale\": [1.0, 1.0, 2.5], \"material_overrides\": {\"stripe\": \"paint_safety_yellow\"}, \"notes\": \"Elongated walkway panel\"}}. "
    "Sample output: {\"id\": \"asset:walkway_lane:v2\", \"glb_path\": \"assets/asset:walkway_lane:v2.glb\", \"bbox\": {...}, "
    "\"recipe\": {...}}."
)


def expand_assets(scene_spec: Dict, asset_ids: Iterable[str] | None = None) -> List[Dict]:
    """Generate primitive recipes for each entity concept or provided asset ids."""

    if not isinstance(scene_spec, dict):
        raise ValueError(f"expand_assets requires scene_spec to be a dict. {_EXPAND_ASSETS_USAGE}")

    normalized_ids: List[str] | None = None
    if asset_ids is not None:
        normalized_ids = _normalize_asset_ids(asset_ids)
        if not normalized_ids:
            raise ValueError(f"asset_ids must contain at least one string identifier. {_EXPAND_ASSETS_USAGE}")

    recipes: List[Dict] = []

    if normalized_ids is not None:
        for asset_id in dict.fromkeys(normalized_ids):  # preserve order while removing duplicates
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
        if isinstance(entity, dict):
            entity_data = entity
        elif isinstance(entity, str):
            entity_data = {"id": entity}
        else:
            continue

        explicit_id = _extract_explicit_asset_id(entity_data)
        concept = _extract_concept(entity_data)
        if not concept and explicit_id:
            concept = infer_concept_from_id(explicit_id)
        if not concept:
            continue

        recipe = _default_recipe(concept)
        recipe_id = explicit_id or f"asset:{concept}:v1"
        recipe["id"] = recipe_id

        tags = recipe.setdefault("tags", [])
        if concept and concept not in tags:
            tags.append(concept)
        derived_concept = infer_concept_from_id(recipe_id)
        if derived_concept and derived_concept not in tags:
            tags.append(derived_concept)
        if recipe_id not in tags:
            tags.append(recipe_id)

        recipes.append(recipe)
    if not recipes:
        raise ValueError(
            "expand_assets produced no recipes. Add entity concepts to scene_spec or provide a non-empty asset_ids list. "
            f"{_EXPAND_ASSETS_USAGE}"
        )
    return recipes


def compile_asset(recipe: Dict) -> Dict:
    """Compile a recipe into a glTF asset and register basic metadata."""

    if not isinstance(recipe, dict):
        raise ValueError(f"compile_asset expects a dict recipe. {_COMPILE_ASSET_USAGE}")

    if "id" not in recipe:
        raise ValueError(f"compile_asset requires recipe['id']. {_COMPILE_ASSET_USAGE}")

    steps = recipe.get("recipe")
    if not isinstance(steps, list) or not steps:
        raise ValueError(
            "compile_asset requires recipe['recipe'] to be a non-empty list of primitive steps. "
            f"{_COMPILE_ASSET_USAGE}"
        )

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


def mutate_asset(
    *,
    base_asset_id: str,
    mutation_id: str,
    scale: float | Sequence[float] | str | None = None,
    material_overrides: MutableMapping[str, str] | str | None = None,
    notes: str | None = None,
) -> Dict:
    """Create a mutated variant of an existing asset manifest.

    The base asset manifest must already exist on disk (compiled previously). The
    mutation clones the recipe, applies simple scaling and optional material
    overrides, then recompiles the resulting asset under ``mutation_id``.
    """

    if isinstance(scale, str):
        scale = _parse_scale_string(scale)

    if isinstance(material_overrides, str):
        material_overrides = _parse_material_overrides_string(material_overrides)

    base_manifest_path = _asset_root() / f"{base_asset_id}.json"
    if not base_manifest_path.exists():
        raise FileNotFoundError(
            f"Base asset manifest not found: {base_asset_id}. Ensure you compile the base asset first by calling compile_asset with the recipe returned from expand_assets."
        )

    base_manifest = json.loads(base_manifest_path.read_text())
    recipe = base_manifest.get("recipe")
    if not isinstance(recipe, dict):
        raise ValueError(
            f"Base asset {base_asset_id} does not contain a recipe; recompile the asset before mutating. {_MUTATE_ASSET_USAGE}"
        )

    mutated_recipe = deepcopy(recipe)
    mutated_recipe["id"] = mutation_id

    if material_overrides:
        materials = mutated_recipe.setdefault("materials", {})
        if isinstance(materials, dict):
            for key, value in material_overrides.items():
                materials[key] = value

    if scale is not None:
        _apply_scale(mutated_recipe, scale)

    tags = mutated_recipe.setdefault("tags", [])
    if isinstance(tags, list):
        if mutation_id not in tags:
            tags.append(mutation_id)
        concept = infer_concept_from_id(mutation_id)
        if concept and concept not in tags:
            tags.append(concept)

    if notes:
        mutated_recipe.setdefault("metadata", {})["notes"] = notes

    return compile_asset(mutated_recipe)


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
                {"primitive": "cuboid", "name": "path", "w": 3.0, "h": 0.2, "d": 12.0, "offset": [0, -0.1, 0]},
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
                {"primitive": "cuboid", "name": "channel", "w": 18.0, "h": 0.6, "d": 160.0, "offset": [0, -0.3, 0]},
            ],
            "materials": {"channel": "water_blue"},
        }

    model_recipe = _model_backed_recipe(concept)
    if model_recipe:
        return model_recipe

    # Fallback simple block
    return {
        "recipe": [
            {"primitive": "cuboid", "name": concept or "asset", "w": 1.0, "h": 1.0, "d": 1.0},
        ],
        "materials": {(concept or "asset"): "default_grey"},
    }


def _model_backed_recipe(concept: str) -> Dict | None:
    api_key = os.environ.get("CEREBRAS_API_KEY")
    if not api_key:
        return None

    try:
        from openai import OpenAI
    except ImportError:  # pragma: no cover - optional dependency guard
        LOGGER.warning("openai package not available; skipping model-backed recipe for %s", concept)
        return None

    config = RuntimeConfig()
    client = OpenAI(api_key=api_key, base_url=config.model.base_url)

    system_prompt = (
        "You are a procedural asset designer. Return only valid JSON with top-level keys 'recipe' (list) and optional"
        " 'materials' (object). Supported primitives: cuboid, cylinder, sphere, pyramid, plane. Each entry must include"
        " all required dimensions (w/h/d or r/h) and may specify 'offset'. Names should be short identifiers. For example,"
        " a bridge deck might use {'primitive': 'cuboid', 'name': 'deck', 'w': 12, 'h': 0.5, 'd': 4}, and a tree canopy can"
        " be {'primitive': 'sphere', 'name': 'crown', 'r': 3, 'offset': [0, 6, 0]}."
    )
    user_prompt = (
        "Design a small set of primitives for the asset concept '{concept}'. Use at most four primitives, scale dimensions"
        " in meters to match the real-world object, and prefer simple combinations that suggest the form."
    ).format(concept=concept)

    try:
        completion = client.chat.completions.create(  # type: ignore[attr-defined]
            model=config.model.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )
    except Exception as exc:  # pragma: no cover - network/runtime safety
        LOGGER.warning("Cerebras model request failed for %s: %s", concept, exc)
        return None

    try:
        content = completion.choices[0].message.content  # type: ignore[index]
    except (AttributeError, IndexError) as exc:  # pragma: no cover - defensive
        LOGGER.warning("Unexpected completion payload for %s: %s", concept, exc)
        return None

    if not content:
        return None

    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        LOGGER.warning("Failed to parse model JSON for %s: %s", concept, exc)
        return None

    recipe_entries = data.get("recipe")
    if not isinstance(recipe_entries, list) or not recipe_entries:
        return None

    for entry in recipe_entries:
        if not isinstance(entry, dict) or "primitive" not in entry:
            return None

    materials = data.get("materials")
    if materials is not None and not isinstance(materials, dict):
        data["materials"] = {}

    data.setdefault("materials", {})
    return data


def _write_manifest(asset_id: str, manifest: Dict) -> None:
    root = _asset_root()
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"{asset_id}.json"
    path.write_text(json.dumps(manifest, indent=2))


def _asset_root() -> Path:
    return Path(os.environ.get("ASSET_ROOT", "assets"))


def infer_concept_from_id(asset_id: str) -> str:
    """Heuristically derive an asset concept name from an asset identifier."""

    raw = str(asset_id).strip()
    if not raw:
        return ""

    segments = [segment for segment in raw.split(":") if segment]
    if len(segments) > 1:
        selected = ""
        for segment in reversed(segments):
            lowered = segment.lower()
            if lowered in {"asset", "assets"}:
                continue
            if lowered.startswith("v") and lowered[1:].isdigit():
                continue
            selected = segment
            break
        if not selected:
            selected = segments[-1]
    else:
        selected = segments[0]

    selected = selected.replace("\\", "/").split("/")[-1]
    selected = Path(selected).stem
    selected = selected.replace("-", "_")
    parts = [part.lower() for part in selected.split("_") if part]
    filtered = [part for part in parts if not part.isdigit()]
    if not filtered:
        filtered = parts or [selected.lower()]
    return "_".join(filtered)


def _apply_scale(recipe: Dict, scale: float | Sequence[float]) -> None:
    if isinstance(scale, Sequence) and not isinstance(scale, (str, bytes, bytearray)):
        factors = list(scale)
    else:
        factors = [float(scale)] if scale is not None else [1.0]

    if len(factors) == 1:
        sx = sy = sz = factors[0]
    elif len(factors) >= 3:
        sx, sy, sz = (float(factors[0]), float(factors[1]), float(factors[2]))
    else:
        sx = sy = sz = float(factors[0])

    for step in recipe.get("recipe", []):
        if not isinstance(step, dict):
            continue
        if "w" in step:
            step["w"] = float(step["w"]) * sx
        if "d" in step:
            step["d"] = float(step["d"]) * sz
        if "h" in step:
            step["h"] = float(step["h"]) * sy
        if "r" in step:
            step["r"] = float(step["r"]) * max(sx, sy, sz)
        if "offset" in step and isinstance(step["offset"], Sequence):
            offset = list(step["offset"])
            if len(offset) >= 3:
                step["offset"] = [float(offset[0]) * sx, float(offset[1]) * sy, float(offset[2]) * sz]



def _extract_concept(entity: Dict) -> str:
    concept = entity.get("concept") or entity.get("class") or entity.get("type")
    if not concept:
        identifier = entity.get("id") or entity.get("asset_id")
        if isinstance(identifier, str) and identifier.strip():
            return infer_concept_from_id(identifier)
        return ""
    return str(concept).strip().lower()


def _extract_explicit_asset_id(entity: Dict) -> str:
    for key in ("asset_id", "id"):
        value = entity.get(key)
        if isinstance(value, str):
            cleaned = value.strip()
            if cleaned:
                return cleaned
    return ""


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


def _normalize_asset_ids(candidate: Iterable[str] | str) -> List[str]:
    if isinstance(candidate, str):
        parsed = _coerce_asset_id_list(candidate)
    elif isinstance(candidate, Sequence):
        parsed = [str(item).strip() for item in candidate if str(item).strip()]
    else:
        raise ValueError(f"asset_ids must be a list of strings. {_EXPAND_ASSETS_USAGE}")

    duplicates_removed = [asset_id for asset_id in dict.fromkeys(parsed) if asset_id]
    return duplicates_removed


def _parse_scale_string(raw: str) -> float | List[float]:
    raw = raw.strip()
    if not raw:
        raise ValueError(f"scale cannot be an empty string. {_MUTATE_ASSET_USAGE}")

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        try:
            parsed = ast.literal_eval(raw)
        except (ValueError, SyntaxError) as exc:
            raise ValueError(f"scale must be a number or array. {_MUTATE_ASSET_USAGE}") from exc

    if isinstance(parsed, (int, float)):
        return float(parsed)

    if isinstance(parsed, Sequence) and not isinstance(parsed, (str, bytes, bytearray)):
        values: List[float] = []
        for item in parsed:
            try:
                values.append(float(item))
            except (TypeError, ValueError) as exc:
                raise ValueError(f"scale list must contain only numbers. {_MUTATE_ASSET_USAGE}") from exc
        return values

    raise ValueError(f"scale must be numeric or a list of numbers. {_MUTATE_ASSET_USAGE}")


def _parse_material_overrides_string(raw: str) -> Dict[str, str]:
    raw = raw.strip()
    if not raw:
        raise ValueError(f"material_overrides cannot be empty. {_MUTATE_ASSET_USAGE}")

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        try:
            parsed = ast.literal_eval(raw)
        except (ValueError, SyntaxError) as exc:
            raise ValueError(f"material_overrides must be a JSON object. {_MUTATE_ASSET_USAGE}") from exc

    if not isinstance(parsed, dict):
        raise ValueError(f"material_overrides must resolve to an object. {_MUTATE_ASSET_USAGE}")

    cleaned: Dict[str, str] = {}
    for key, value in parsed.items():
        key_str = str(key).strip()
        value_str = str(value).strip()
        if key_str:
            cleaned[key_str] = value_str

    if not cleaned:
        raise ValueError(f"material_overrides must include at least one key/value pair. {_MUTATE_ASSET_USAGE}")

    return cleaned

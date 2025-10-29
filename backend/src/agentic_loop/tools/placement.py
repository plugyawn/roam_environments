"""Asset placement tool that validates agent-provided transforms."""

from __future__ import annotations

import ast
import json
from typing import Dict, Iterable, List, Sequence


def place_assets(*, placements: List[Dict] | str, asset_ids: Iterable[str] | str | None = None, map_plan: Dict | str | None = None) -> List[Dict]:
    """Validate and return placements authored by the LLM orchestrator.

    The upstream agents occasionally provide arguments as JSON strings or with
    slightly different field names. This helper accepts those variants and
    normalises them before enforcing the strict placement contract expected by
    downstream tooling.
    """

    parsed_asset_ids = _normalise_asset_ids(asset_ids)
    asset_set = set(parsed_asset_ids) if parsed_asset_ids is not None else None

    normalised_map_plan = _maybe_parse_json(map_plan)
    _ = normalised_map_plan  # preserve signature compatibility for callers that expect map feedback

    normalised_placements = _normalise_placements(placements, asset_set)

    used = set()
    for entry in normalised_placements:
        ref = entry["ref"]
        if asset_set is not None:
            used.add(ref)

        transform = entry["transform"]
        pos = transform.get("pos")
        if not _is_vector(pos, length=3):
            raise ValueError(f"Placement '{ref}' transform.pos must be a 3-element list")

        if "scale" in transform and not isinstance(transform["scale"], (int, float)):
            raise ValueError(f"Placement '{ref}' transform.scale must be numeric")

        if "rotY" in transform and not isinstance(transform["rotY"], (int, float)):
            raise ValueError(f"Placement '{ref}' transform.rotY must be numeric")

    if asset_set is not None and asset_set != used:
        missing = asset_set - used
        raise ValueError(f"Missing placements for assets: {sorted(missing)}")

    return normalised_placements


def _normalise_asset_ids(asset_ids: Iterable[str] | str | None) -> List[str] | None:
    if asset_ids is None:
        return None

    parsed = _maybe_parse_json(asset_ids)
    if parsed is None:
        return None

    if isinstance(parsed, str):
        parsed = [parsed]

    if not isinstance(parsed, Sequence) or isinstance(parsed, (bytes, bytearray)):
        raise ValueError("asset_ids must resolve to a sequence of strings")

    result: List[str] = []
    for item in parsed:
        if not isinstance(item, str) or not item.strip():
            raise ValueError("asset_ids entries must be non-empty strings")
        result.append(item.strip())
    return result


def _normalise_placements(placements: List[Dict] | str, asset_set: set[str] | None) -> List[Dict]:
    parsed = _maybe_parse_json(placements)
    if not isinstance(parsed, Sequence) or isinstance(parsed, (str, bytes, bytearray)):
        raise ValueError("placements must resolve to a list of placement objects")

    normalised: List[Dict] = []
    for entry in parsed:
        if not isinstance(entry, dict):
            raise ValueError("Each placement must be a dict")

        resolved_ref = _resolve_ref(entry, asset_set)
        transform = entry.get("transform")
        if isinstance(transform, (str, bytes, bytearray)):
            transform = _maybe_parse_json(transform)
        if not isinstance(transform, dict):
            transform = {}

        if "pos" in transform:
            transform["pos"] = _maybe_parse_json(transform["pos"])

        if "rotY" in transform:
            parsed_rot = _maybe_parse_json(transform["rotY"])
            if isinstance(parsed_rot, (int, float)):
                transform["rotY"] = float(parsed_rot)

        if "scale" in transform:
            parsed_scale = _maybe_parse_json(transform["scale"])
            if isinstance(parsed_scale, (int, float)):
                transform["scale"] = float(parsed_scale)

        if "pos" not in transform:
            pos_source = _first_available(entry, ("pos", "position", "translation"))
            if pos_source is not None:
                transform["pos"] = _maybe_parse_json(pos_source)

        if "rotY" not in transform:
            rot_source = _first_available(entry, ("rotY", "rot_y", "rotation", "yaw"))
            parsed_rot = _maybe_parse_json(rot_source)
            if isinstance(parsed_rot, (int, float)):
                transform["rotY"] = float(parsed_rot)

        if "scale" not in transform:
            scale_source = _first_available(entry, ("scale", "uniform_scale"))
            parsed_scale = _maybe_parse_json(scale_source)
            if isinstance(parsed_scale, (int, float)):
                transform["scale"] = float(parsed_scale)

        if "pos" not in transform:
            raise ValueError(f"Placement '{resolved_ref}' requires a transform.pos vector")

        cleaned_entry = {
            "ref": resolved_ref,
            "transform": transform,
        }

        # Preserve optional metadata if provided (e.g. semantic labels).
        for meta_key in ("label", "notes", "category", "tags", "region"):
            if meta_key in entry:
                cleaned_entry[meta_key] = entry[meta_key]

        normalised.append(cleaned_entry)

    return normalised


def _resolve_ref(entry: Dict, asset_set: set[str] | None) -> str:
    raw_candidates = [
        entry.get("ref"),
        entry.get("asset_id"),
        entry.get("asset"),
        entry.get("id"),
        entry.get("name"),
    ]

    for candidate in raw_candidates:
        if isinstance(candidate, str) and candidate.strip():
            resolved = candidate.strip()
            if asset_set is None or resolved in asset_set:
                return resolved

    if asset_set is None:
        raise ValueError("Placement entries must include a 'ref' field")

    # Attempt fuzzy matching when the agent provides shorthand names such as
    # "market_square" for the asset ID "asset:market_square:v1".
    shorthand = None
    for candidate in raw_candidates:
        if isinstance(candidate, str) and candidate.strip():
            shorthand = candidate.strip()
            break
    if not shorthand:
        raise ValueError("Placement entries must include a 'ref' field")

    matches = [asset_id for asset_id in asset_set if asset_id.endswith(f":{shorthand}") or asset_id.endswith(f":{shorthand}:v1")]
    if len(matches) != 1 and "_" in shorthand:
        base = shorthand.split("_", 1)[0]
        matches = [asset_id for asset_id in asset_set if asset_id.endswith(f":{base}") or asset_id.endswith(f":{base}:v1")]
    if len(matches) == 1:
        return matches[0]

    raise ValueError(f"Placement references unknown asset '{shorthand}'")


def _maybe_parse_json(value):  # type: ignore[no-untyped-def]
    if isinstance(value, (list, dict)):  # already structured
        return value
    if value is None:
        return None
    if isinstance(value, (bytes, bytearray)):
        value = value.decode("utf-8")
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return None
        try:
            return json.loads(stripped)
        except json.JSONDecodeError:
            try:
                return ast.literal_eval(stripped)
            except (ValueError, SyntaxError):
                return stripped
    return value


def _first_available(entry: Dict, keys: Sequence[str]):
    for key in keys:
        if key in entry:
            return entry[key]
    return None


def _is_vector(value: object, *, length: int) -> bool:
    if not isinstance(value, Sequence) or len(value) != length:
        return False
    return all(isinstance(component, (int, float)) for component in value)

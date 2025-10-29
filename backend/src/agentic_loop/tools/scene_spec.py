"""Scene specification tool glue."""

from __future__ import annotations

import json
import re
from typing import Any, Dict, Iterable, List, Tuple


def design_scene_spec(requirements_json: Dict) -> Dict:
    """Generate a first-pass scene specification from loosely structured input."""

    payload: Dict = _coerce_payload(requirements_json)

    if isinstance(payload.get("scene_spec"), dict):
        payload = payload["scene_spec"]

    entities: List[Dict] = _normalise_entities(payload.get("entities"))
    entities = _merge_entities(entities, _normalise_entities(payload.get("requirements")))

    for key in _ENTITY_LIST_KEYS:
        if key in payload:
            entities = _merge_entities(entities, _normalise_entities(payload.get(key)))

    for key, value in payload.items():
        if key in _EXCLUDED_ENTITY_KEYS:
            continue
        if isinstance(value, bool) and value:
            entities = _merge_entities(entities, _normalise_entities([key]))
        elif isinstance(value, str) and value.strip() and key.endswith("_type"):
            entities = _merge_entities(entities, _normalise_entities([value]))

    constraint_sources: Tuple[str, ...] = ("constraints", "guidelines", "notes", "conditions")
    constraints: List[Dict] = []
    for key in constraint_sources:
        constraints.extend(_normalise_constraints(payload.get(key)))

    for key in ("theme", "setting"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            constraints.append({"note": key, "value": value.strip()})

    if not entities:
        fallback = _first_nonempty_string(
            [payload.get("primary_entity"), payload.get("focus"), payload.get("theme"), payload.get("setting")]
        )
        if fallback:
            concept = _slugify(fallback)
            if concept:
                entities.append({"concept": concept, "count": 1, "attrs": {"label": fallback}})

    return {
        "entities": entities,
        "constraints": constraints,
    }


def _coerce_payload(requirements_json: Dict) -> Dict:
    """Attempt to normalise arbitrary payloads into a dict."""

    if isinstance(requirements_json, dict):
        return requirements_json
    if isinstance(requirements_json, str):
        trimmed = requirements_json.strip()
        if not trimmed:
            return {}
        try:
            return json.loads(trimmed)
        except json.JSONDecodeError:
            return {"theme": trimmed}
    return {}


def _slugify(value: str) -> str:
    if not value:
        return ""
    text = str(value).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def _normalise_entities(raw: Any) -> List[Dict]:
    entities: List[Dict] = []
    for item in _ensure_collection(raw):
        entity = _coerce_entity(item)
        if entity:
            _merge_entities(entities, [entity])
    return entities


def _merge_entities(primary: List[Dict], extra: List[Dict]) -> List[Dict]:
    by_concept: Dict[str, Dict] = {entry.get("concept"): entry for entry in primary if entry.get("concept")}
    for entry in extra:
        concept = entry.get("concept")
        if not concept:
            continue
        existing = by_concept.get(concept)
        if existing is None:
            entry.setdefault("attrs", {})
            entry["count"] = _coerce_count(entry.get("count"))
            primary.append(entry)
            by_concept[concept] = entry
            continue
        existing_count = _coerce_count(existing.get("count"))
        incoming_count = _coerce_count(entry.get("count"))
        existing["count"] = max(existing_count, incoming_count)
        existing_attrs = existing.setdefault("attrs", {})
        incoming_attrs = entry.get("attrs") or {}
        if isinstance(incoming_attrs, dict):
            existing_attrs.update({key: value for key, value in incoming_attrs.items() if value is not None})
    return primary


def _normalise_constraints(raw: Any) -> List[Dict]:
    constraints: List[Dict] = []
    for item in _ensure_collection(raw):
        if isinstance(item, dict):
            if item:
                constraints.append(item)
        elif item is not None:
            note = str(item).strip()
            if note:
                constraints.append({"note": note})
    return constraints


def _ensure_collection(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return list(value)
    return [value]


def _coerce_entity(item: Any) -> Dict:
    if isinstance(item, dict):
        candidate = item.get("concept") or item.get("name") or item.get("label") or item.get("id")
        concept = _slugify(candidate or "")
        if not concept:
            return {}
        label = item.get("label") or item.get("name") or candidate
        attrs: Dict[str, Any] = {}
        if isinstance(item.get("attrs"), dict):
            attrs.update(item["attrs"])
        for key, value in item.items():
            if key in {"concept", "name", "label", "count", "min_count", "max_count", "exactly", "quantity", "attrs"}:
                continue
            if value is None:
                continue
            attrs[key] = value
        if label:
            attrs.setdefault("label", label)
        return {
            "concept": concept,
            "count": _coerce_count(
                item.get("count"),
                item.get("min_count"),
                item.get("max_count"),
                item.get("exactly"),
                item.get("quantity"),
            ),
            "attrs": attrs,
        }
    if isinstance(item, str):
        label = item.strip()
        concept = _slugify(label)
        if concept:
            return {"concept": concept, "count": 1, "attrs": {"label": label}}
        return {}
    if isinstance(item, (int, float)):
        label = str(item)
        concept = _slugify(label)
        if concept:
            return {"concept": concept, "count": 1, "attrs": {"label": label}}
    return {}


def _coerce_count(*values: Any) -> int:
    for value in values:
        if value is None or isinstance(value, bool):
            continue
        try:
            count = int(value)
        except (TypeError, ValueError):
            continue
        if count > 0:
            return count
    return 1


def _first_nonempty_string(values: Iterable[Any]) -> str:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


_ENTITY_LIST_KEYS: Tuple[str, ...] = (
    "features",
    "infrastructure",
    "structures",
    "key_buildings",
    "agricultural_buildings",
    "public_buildings",
    "civic_buildings",
    "residential_buildings",
    "landmarks",
    "elements",
    "assets",
)


_EXCLUDED_ENTITY_KEYS: Tuple[str, ...] = (
    "entities",
    "requirements",
    "constraints",
    "guidelines",
    "notes",
    "conditions",
    "theme",
    "setting",
    "scene_spec",
    "map_plan",
)

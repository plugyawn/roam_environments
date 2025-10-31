"""Progress checklist helpers for the Magentic-One workflow."""

from __future__ import annotations

import ast
import json
from typing import Any, Dict, Iterable, List

from .audit import (
    MIN_REQUIRED_ASSETS,
    MIN_REQUIRED_PLACEMENTS,
    REQUIRED_ROAD_PLACEMENTS,
    audit_asset_requirements,
)

ASSET_CREATION_MILESTONES: List[int] = [3, 6, 9, 12]
ASSET_PLACEMENT_MILESTONES: List[int] = [3, 6, 9, 12]
PLACEMENT_COUNT_MILESTONES: List[int] = [5, 10, 15, 20]


def progress_checklist(state: Dict | str | Any) -> Dict:
    """Return progress milestones for assets and placements."""
    state_dict = _coerce_state(state)

    audit = audit_asset_requirements(state_dict)
    unique_asset_count = int(audit.get("unique_asset_count") or 0)
    total_placements = int(audit.get("placement_count") or 0)
    unplaced_assets = list(audit.get("unplaced_assets") or [])
    placed_asset_count = max(unique_asset_count - len(unplaced_assets), 0)

    milestones = []
    milestones.extend(
        _build_milestones(
            "assets_created",
            unique_asset_count,
            ASSET_CREATION_MILESTONES,
        )
    )
    milestones.extend(
        _build_milestones(
            "assets_placed",
            placed_asset_count,
            ASSET_PLACEMENT_MILESTONES,
        )
    )
    milestones.extend(
        _build_milestones(
            "placement_count",
            total_placements,
            PLACEMENT_COUNT_MILESTONES,
        )
    )

    summary_lines = [
        f"Assets compiled: {unique_asset_count}/{MIN_REQUIRED_ASSETS}",
        f"Assets with placements: {placed_asset_count}/{MIN_REQUIRED_ASSETS}",
        f"Total placements: {total_placements}/{MIN_REQUIRED_PLACEMENTS} (roads {audit.get('road_placement_count', 0)}/{REQUIRED_ROAD_PLACEMENTS})",
    ]

    status = "complete" if audit.get("status") == "pass" else "in_progress"

    return {
        "status": status,
        "assets_compiled": unique_asset_count,
        "assets_with_placement": placed_asset_count,
        "total_placements": total_placements,
        "milestones": milestones,
        "messages": audit.get("messages") or [],
        "summary": " | ".join(summary_lines),
    }


def _build_milestones(category: str, current: int, thresholds: Iterable[int]) -> List[Dict]:
    records: List[Dict] = []
    for target in thresholds:
        records.append(
            {
                "category": category,
                "target": int(target),
                "current": current,
                "status": "complete" if current >= target else "pending",
            }
        )
    return records


def _coerce_state(state: Any) -> Dict:
    if isinstance(state, dict):
        return state
    if isinstance(state, str):
        trimmed = state.strip()
        if not trimmed:
            return {}
        try:
            loaded = json.loads(trimmed)
        except json.JSONDecodeError:
            try:
                loaded = ast.literal_eval(trimmed)
            except (ValueError, SyntaxError):
                raise ValueError("progress_checklist expects a dict payload") from None
        if isinstance(loaded, dict):
            return loaded
        raise ValueError("progress_checklist expects a dict payload")
    raise ValueError("progress_checklist expects a dict payload")


__all__ = [
    "progress_checklist",
    "ASSET_CREATION_MILESTONES",
    "ASSET_PLACEMENT_MILESTONES",
    "PLACEMENT_COUNT_MILESTONES",
]

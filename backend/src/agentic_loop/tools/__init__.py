"""Tool registration for Magentic-One function calling."""

from __future__ import annotations

from typing import Callable, List

from .assets import compile_asset, expand_assets, mutate_asset
from .audit import audit_asset_requirements
from .checklist import progress_checklist
from .map_gen import generate_map
from .placement import place_assets
from .persistence import persist_run
from .render import render_snapshot
from .scene_spec import design_scene_spec
from .scene_diff import apply_scene_diff, initialize_scene
from .validation import validate_scene


def tool_registry() -> List[Callable]:
    """Return the callable tool list exposed to the agents."""

    return [
    initialize_scene,
    design_scene_spec,
        expand_assets,
        compile_asset,
        mutate_asset,
        generate_map,
        place_assets,
    apply_scene_diff,
        validate_scene,
        persist_run,
        render_snapshot,
        audit_asset_requirements,
        progress_checklist,
    ]


__all__ = ["tool_registry"]

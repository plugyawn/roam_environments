"""Tool registration for Magentic-One function calling."""

from __future__ import annotations

from typing import Callable, List

from .assets import compile_asset, expand_assets
from .map_gen import generate_map
from .placement import place_assets
from .persistence import persist_run
from .render import render_snapshot
from .scene_spec import design_scene_spec
from .validation import validate_scene


def tool_registry() -> List[Callable]:
    """Return the callable tool list exposed to the agents."""

    return [
        design_scene_spec,
        expand_assets,
        compile_asset,
        generate_map,
        place_assets,
        validate_scene,
        persist_run,
        render_snapshot,
    ]


__all__ = ["tool_registry"]

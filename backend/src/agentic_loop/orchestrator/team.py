"""Team assembly for Magentic-One."""

from __future__ import annotations

from textwrap import dedent
from typing import Any

try:  # pragma: no cover - optional dependency
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.teams import MagenticOneGroupChat
except ImportError:  # pragma: no cover - optional dependency not installed
    AssistantAgent = None  # type: ignore[assignment]
    MagenticOneGroupChat = None  # type: ignore[assignment]
    AUTOGEN_AVAILABLE = False
else:
    AUTOGEN_AVAILABLE = True

from ..config import RuntimeConfig
from ..tools import tool_registry
from .client import CerebrasModelClient

MagenticOneGroupChatType = Any

__all__ = ["AUTOGEN_AVAILABLE", "build_team"]

_BASE_TEAM_INSTRUCTIONS = dedent(
    """
    You are part of a four-agent Magentic-One crew that transforms a user prompt into a shippable
    3D environment payload. Keep teammates aligned and drive toward completion on every turn.
    Deliverable: the final scene_state JSON returned by initialize_scene/apply_scene_diff containing:
      - scene_graph with placements, manifests, and template-grounded map metadata
      - assets describing every compiled recipe that was injected via diffs
      - metadata with run diagnostics (include run_id when available)

        Core operating rhythm:

        Step 0 (Orchestrator): call initialize_scene exactly once at the top of the run. Pick the
        template that best matches the prompt and broadcast the returned scene_state to the team.
        Never hand-edit scene_graph structures—treat the returned object as the single source of truth.

        Step 1 (Orchestrator + Designer): capture one textual checklist before touching other tools.
        The list must cover:
            - one background/environment asset
            - a scalable road primitive
            - at least five specific road segment placements
            - at least ten additional unique feature assets tailored to the prompt
        Keep the checklist in conversation only and call progress_checklist when it is finalized.

        Step 2 (Designer then PlacementHead): work through the checklist in order. For each line:
                1. Designer drafts the recipe, compiles it once, then immediately call
                    apply_scene_diff(scene_state, {"assets": [...]}, allow_overwrite=True when replacing
                    template placeholders) to inject the manifest into the shared scene_state.
                    2. PlacementHead determines transforms, then call
                        apply_scene_diff(scene_state, {"placements": [...]}, allow_overwrite=True when
                        adjusting an existing placement) to append coordinates.
              After each apply_scene_diff call, capture the returned scene_state and share the updated
              reference so everyone keeps working on the latest graph.
        Start with the background, follow with the five road segments, then complete the remaining assets.

        Step 3 (Validator): after every checklist item has both a compiled asset and at least one
        placement, run validation, persist_run, render_snapshot, and share the final JSON payload.
        The last assistant message must contain only the finalized scene_state JSON followed by
        TERMINATE on a separate line.

    Workflow expectations:
    0. Unpack the prompt into environment requirements. Maintain live checklists for fundamentals
       outstanding assets. Revisit them every turn.
    1. Plan before execution. Outline next steps, decide which tools are required, and assign work
       to specific teammates.
    2. Adopt a tight create → compile → inject → place loop. After compile_asset, inject that manifest
       with apply_scene_diff so everyone operates on the same scene_state reference. Placement updates
       must also flow through apply_scene_diff.
    3. When you mention a tool call, invoke it immediately with structured arguments. Do not leave
       pseudo-code, Markdown code blocks, or inline Python.
     4. Keep context tight. Summaries must stay inside the runtime budgets and contain only what the
         next actor needs. After every apply_scene_diff invocation, repost the refreshed scene_state
         reference. Maintain a short asset_log in plain text that records asset ids, manifest paths,
         placements, and timestamps for diffs.
    5. Treat validation findings as blocking issues. Iterate until each failure is resolved.
    6. Do not finish early. Continue refining until the payload is coherent, grounded, and passes
       validation. The final reply must be the JSON payload alone followed by TERMINATE.
    7. Call progress_checklist after each asset is compiled and placed to announce updated counts
       (e.g., "Road segment 3 done: assets placed 4/12, roads 3/5").
    """
).strip()

_ROLE_INSTRUCTIONS = {
    "Orchestrator": dedent(
        """
        Act as the conductor. Call initialize_scene once, share the template choice, and circulate the
        scene_state reference so everyone uses the same object. Keep checklists current, assign work,
        and enforce reflection pauses. Make the group answer "What remains?" at least twice before
        handing off for final approval. Ensure every tool call has a clear purpose and that Validator
        knows when inspection should start. Drive the team line-by-line through the checklist without
        multitasking. Invoke progress_checklist whenever counts change and announce milestone progress
        (e.g., "Assets compiled 6/12, roads placed 3/5"). Guard against redundant tool calls—one
    compile per asset, one apply_scene_diff injection per data change. After every diff, confirm the
    team is referencing the newest scene_state JSON. Start with the background, then five road
    segments, then the remaining feature assets. Move to Validator only after the diff report shows
    all targets satisfied.
        """
    ).strip(),
    "Designer": dedent(
        """
    Own the creative direction and scene specification. Convert each checklist line into a concrete
    recipe before moving to the next. When you reach the road primitive, ensure it is a shallow, wide
    cuboid that scales cleanly per placement. Call compile_asset exactly once per entry, record the
    manifest in asset_log, then immediately invoke apply_scene_diff(scene_state, {"assets": [...]},
    allow_overwrite=True when replacing a template seed). Capture the returned scene_state and repost it
    so the team stays in sync. Brief PlacementHead with the asset id, intended transforms, and any
    constraints. Keep communications concise—structured bullet updates beat prose.
        """
    ).strip(),
    "PlacementHead": dedent(
        """
    Command spatial layout and coordinates. As soon as Designer compiles an asset, capture its id from
    the asset_log, determine exact transforms, and call place_assets with numeric values. Immediately
    feed those placements into apply_scene_diff(scene_state, {"placements": [...]}, allow_overwrite=True
    when adjusting an existing placement). Repost the updated scene_state so everyone is operating on the
    latest graph. Maintain placement details inside asset_log so the team can track progress. Lay the
    background first, then the five road segments (spaced and oriented for
    traversal), then the remaining assets in checklist order. Avoid vague positioning and deliver exact
    values. Call progress_checklist after each placement batch to confirm updated totals. Once all assets
    are placed, hand off to Validator for final checks.
        """
    ).strip(),
    "Validator": dedent(
        """
    Act as the gatekeeper for quality and completeness. Watch every draft for JSON consistency,
    required keys, missing assets, and a complete asset_log that mirrors all placements. Trigger
    progress_checklist to confirm all checklist items are satisfied (background present, >=5 road
    placements, >=10 feature assets). Inspect the latest apply_scene_diff report—if counts lag, send
    the team back. Then run validate_scene, persist_run, and rendering tools as needed. Do not approve
    hand-off until the payload can execute without manual fixes. When the payload is complete, reply
    with the JSON scene_state and immediately follow it with the single message TERMINATE.
        """
    ).strip(),
}

TEAM_DESCRIPTION = "Magentic-One orchestration team for Roam environment authoring."


def _compose_system_message(role: str) -> str:
    role_brief = _ROLE_INSTRUCTIONS.get(role)
    if role_brief is None:
        raise KeyError(f"Unknown role '{role}'")
    return f"{_BASE_TEAM_INSTRUCTIONS}\n\nRole focus - {role}:\n{role_brief}"


def build_team(config: RuntimeConfig) -> MagenticOneGroupChatType:
    """Create and wire the Magentic-One team for the Roam environment workflow."""

    if not AUTOGEN_AVAILABLE:
        raise RuntimeError("autogen-agentchat is not installed; cannot build Magentic-One team")

    model_client = CerebrasModelClient(config)
    shared_tools = tool_registry()

    orchestrator = AssistantAgent(
        name="Orchestrator",
        model_client=model_client,
        system_message=_compose_system_message("Orchestrator"),
        description="Coordinates the workflow, maintains checklists, and delegates tasks.",
        tools=shared_tools,
        max_tool_iterations=4,
    )

    designer = AssistantAgent(
        name="Designer",
        model_client=model_client,
        system_message=_compose_system_message("Designer"),
        description="Translates prompts into environment specs, assets, and references. Comes first.",
        tools=shared_tools,
        max_tool_iterations=4,
    )

    placement_head = AssistantAgent(
        name="PlacementHead",
        model_client=model_client,
        system_message=_compose_system_message("PlacementHead"),
        description="Produces maps and precise asset placements using the tool suite. Comes second.",
        tools=shared_tools,
        max_tool_iterations=4,
    )

    validator = AssistantAgent(
        name="Validator",
        model_client=model_client,
        system_message=_compose_system_message("Validator"),
        description="Audits completeness, runs validation tools, and approves the final payload. Comes third.",
        tools=shared_tools,
        max_tool_iterations=4,
        reflect_on_tool_use=True,
    )

    return MagenticOneGroupChat(
        participants=[orchestrator, designer, placement_head, validator],
        model_client=model_client,
        name="Magentic-One Team",
        description=TEAM_DESCRIPTION,
        max_turns=150,
        max_stalls=6,
    )

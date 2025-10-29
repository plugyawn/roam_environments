"""Team assembly for Magentic-One."""

from __future__ import annotations

from typing import Any, Dict

try:  # pragma: no cover - optional dependency
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.teams import MagenticOneGroupChat
except ImportError:  # pragma: no cover - optional dependency not installed
    AssistantAgent = None  # type: ignore
    MagenticOneGroupChat = None  # type: ignore
    AUTOGEN_AVAILABLE = False
else:
    AUTOGEN_AVAILABLE = True

from ..config import RuntimeConfig
from ..tools import tool_registry
from .client import CerebrasModelClient

MagenticOneGroupChatType = Any


def build_team(config: RuntimeConfig) -> MagenticOneGroupChatType:
    """Create a Magentic-One team wired to the Cerebras client and tools."""

    if not AUTOGEN_AVAILABLE:
        raise RuntimeError("autogen-agentchat is not installed; cannot build Magentic-One team")

    model_client = CerebrasModelClient(config)
    base_instructions = (
        "You are collaboratively producing 3D settlement scenes. The Python tools perform execution only; there are no "
        "built-in heuristics for layout or validation. You must plan, call tools, and iterate until a complete payload is "
        "ready. Follow this workflow for every request:\n"
        "1. Call `design_scene_spec` (and supporting tools) to translate the user goal into structured requirements. Expand "
        "those requirements to cover supporting props, foliage, infrastructure, and landmarks so the scene feels full.\n"
        "2. Produce a map plan that matches those requirements by invoking `generate_map`.\n"
        "3. Use `expand_assets` and `compile_asset` to materialize every asset that will appear in the final scene. Capture "
        "the returned asset IDs and glb paths. Aim for at least 12 distinct assets unless the user explicitly requests a "
        "minimal scene.\n"
        "4. Determine explicit transforms for each asset and call `place_assets` with placements covering every asset ID. "
        "Placements must include numeric `pos` vectors (meters), optional `rotY`, and align with the map plan.\n"
        "5. Build the scene graph object (map + assets + placements) and run `validate_scene`. If validation reports issues, "
        "adjust the assets or placements and retry tools until it passes.\n"
        "6. Run at least two reflective audit rounds after you have a draft scene. Each round, ask yourself \"What important "
        "element is still missing?\" and add the necessary assets/placements before revalidating.\n"
        "7. Persist the finished scene by calling `persist_run` (and `render_snapshot` if a render is required). Retain the "
        "returned artifact paths.\n"
        "8. Finalize by returning a single JSON object, not prose, containing at minimum: `scene_id`, `requirements`, "
        "`scene_spec`, `assets` (detailed manifests), `map_plan`, `scene_graph` with a non-empty `placements` list matching "
        "the asset IDs, `validation`, and any `manifest_path`/`snapshot_path` values from the tools.\n"
        "Never claim success without running the relevant tools. Use retries to fix tool errors instead of assuming success."
    )

    orchestrator = AssistantAgent(
        "Orchestrator",
        model_client=model_client,
        system_message=(
            base_instructions
            + " Direct the team, keep context under the configured budgets, and ensure the final response is exactly the JSON "
            + "payload described above. Lead the reflection rounds: explicitly prompt the group with \"What else is missing?\" "
            + "at least twice before approving completion."
        ),
    )
    coder = AssistantAgent(
        "Coder",
        model_client=model_client,
        tools=tool_registry(),
        system_message=(
            base_instructions
            + " Invoke tools to gather requirements, craft assets, generate maps, devise placements, validate the scene, "
            + "and persist outputs. Maintain the authoritative scene graph structure throughout. During reflection rounds, "
            + "propose additional complementary assets and placements until coverage is rich."
        ),
    )
    validator = AssistantAgent(
        "Validator",
        model_client=model_client,
        tools=tool_registry(),
        system_message=(
            base_instructions
            + " Verify that placements satisfy constraints, insist on rerunning validation after fixes, and block completion "
            + "until every deliverable field is populated. During reflection rounds assess coverage critically and call out "
            + "missing categories (waterfront props, vegetation, lighting, etc.)."
        ),
    )
    return MagenticOneGroupChat([orchestrator, coder, validator], model_client=model_client)


__all__ = ["build_team", "AUTOGEN_AVAILABLE"]

"""Template catalog for Magentic-One scene planning."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True)
class TemplateSpec:
    """Describes a reusable layout archetype for quick scene bootstrapping."""

    name: str
    description: str
    base_terrain: str
    seed_assets: List[str]
    mutation_ideas: List[str]


TEMPLATE_CATALOG: List[TemplateSpec] = [
    TemplateSpec(
        name="Linear Corridor",
        description="Straight traversal strip with gentle segmenting for rhythm.",
        base_terrain="Stretch a ground plane into a corridor floor before any set dressing.",
        seed_assets=[
            "primitive:ground_plane_flat",
            "primitive:lane_strip",
            "primitive:blocker_cube",
            "primitive:guidance_light",
        ],
        mutation_ideas=[
            "Turn blocker cubes into kiosks, pillars, or scanner arches.",
            "Recolour lane strips into moving walkway indicators.",
        ],
    ),
    TemplateSpec(
        name="Multi-Lane Runner",
        description="Parallel lanes (commonly three) with alternating hazard slots.",
        base_terrain="Lay down three adjacent lane strips on a single flattened ground plane.",
        seed_assets=[
            "primitive:ground_plane_flat",
            "primitive:lane_strip",
            "primitive:blocker_cube",
            "primitive:collectible_marker",
        ],
        mutation_ideas=[
            "Mutate lane strips into conveyor walkways or service roads.",
            "Convert blockers into HVAC pods, luggage carts, or security arches.",
        ],
    ),
    TemplateSpec(
        name="Open Plaza",
        description="Broad flat space anchored by a central feature and perimeter clusters.",
        base_terrain="Tile a large ground plane for the plaza before adding focal structures.",
        seed_assets=[
            "primitive:ground_plane_flat",
            "primitive:center_plinth",
            "primitive:planter_block",
            "primitive:bench_strip",
        ],
        mutation_ideas=[
            "Reshape the plinth into statues, fountains, or kiosks.",
            "Extend benches into cafe seating or waiting areas.",
        ],
    ),
    TemplateSpec(
        name="Hub-and-Spoke",
        description="Central node connected to radial branches and satellite pockets.",
        base_terrain="Compose a circular hub plane linked by narrow branch strips.",
        seed_assets=[
            "primitive:hub_disc",
            "primitive:lane_strip",
            "primitive:marker_post",
            "primitive:planter_block",
        ],
        mutation_ideas=[
            "Transform marker posts into info pylons or lighting towers.",
            "Convert planters into barricades or luggage stacks near each spoke.",
        ],
    ),
    TemplateSpec(
        name="Loop Track",
        description="Closed circuit path for repeated traversal with inner/outer decoration bands.",
        base_terrain="Trace a spline loop and drape a thin ground strip along the curve.",
        seed_assets=[
            "primitive:loop_track",
            "primitive:lane_boundary",
            "primitive:blocker_cube",
            "primitive:collectible_marker",
        ],
        mutation_ideas=[
            "Stretch lane boundaries into guard rails or neon edging.",
            "Convert blockers into themed set pieces spaced around the loop.",
        ],
    ),
    TemplateSpec(
        name="Tiered Terrace",
        description="Stacked horizontal platforms connected with ramps or stairs.",
        base_terrain="Extrude three stepped planes to define the terraces before dressing.",
        seed_assets=[
            "primitive:terrace_plate",
            "primitive:ramp_strip",
            "primitive:guard_rail",
            "primitive:planter_block",
        ],
        mutation_ideas=[
            "Morph ramp strips into escalators or jet bridges.",
            "Resize guard rails into glass partitions or safety lights.",
        ],
    ),
    TemplateSpec(
        name="Grid Block",
        description="Orthogonal cell layout suited to modular props and repeatable units.",
        base_terrain="Pixelate the ground plane into grid tiles before instancing assets.",
        seed_assets=[
            "primitive:grid_tile",
            "primitive:blocker_cube",
            "primitive:marker_post",
            "primitive:collectible_marker",
        ],
        mutation_ideas=[
            "Turn grid tiles into parking slots or vendor pads.",
            "Scale blocker cubes into storage racks or security checkpoints.",
        ],
    ),
    TemplateSpec(
        name="Winding Path",
        description="Single meandering spline path cutting through varied scenery.",
        base_terrain="Lay a spline-driven thin ground strip as the primary path.",
        seed_assets=[
            "primitive:path_strip",
            "primitive:ground_plane_flat",
            "primitive:marker_post",
            "primitive:collectible_marker",
        ],
        mutation_ideas=[
            "Stretch path strips into moving walkways or gentle rivers.",
            "Convert markers into lanterns or signage.",
        ],
    ),
    TemplateSpec(
        name="Open Field with Landmarks",
        description="Mostly empty terrain punctuated by a few anchor objects and scatter props.",
        base_terrain="Start with a large ground sheet before sprinkling anchors.",
        seed_assets=[
            "primitive:ground_plane_flat",
            "primitive:anchor_column",
            "primitive:planter_block",
            "primitive:collectible_marker",
        ],
        mutation_ideas=[
            "Transform anchor columns into sculptures, towers, or control beacons.",
            "Use planters as crates, barriers, or billboards.",
        ],
    ),
    TemplateSpec(
        name="Primitive Sandbox",
        description="Blank terrain seeded with generic primitives ready for mutation into bespoke builds.",
        base_terrain="Place a neutral terrain plane and distribute primitive shapes for kitbashing.",
        seed_assets=[
            "primitive:ground_plane_flat",
            "primitive:blocker_cube",
            "primitive:cylinder_stack",
            "primitive:plane_panel",
        ],
        mutation_ideas=[
            "Reform cubes into kiosks, cargo crates, or furniture clusters.",
            "Stretch cylinder stacks into lighting columns or fuel tanks.",
        ],
    ),
]


def render_template_catalog() -> str:
    """Format the template catalog for prompt injection."""

    lines: List[str] = []
    for index, template in enumerate(TEMPLATE_CATALOG, start=1):
        lines.append(f"{index}. {template.name}: {template.description}")
        lines.append(f"   Base terrain: {template.base_terrain}")
        lines.append("   Seed assets: " + ", ".join(template.seed_assets))
        lines.append("   Mutation ideas: " + "; ".join(template.mutation_ideas))
    return "\n".join(lines)


__all__: Iterable[str] = ["TemplateSpec", "TEMPLATE_CATALOG", "render_template_catalog"]

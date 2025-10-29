"""Compile primitive recipes into glTF assets."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import numpy as np
import trimesh


@dataclass(slots=True)
class CompileResult:
    asset_id: str
    glb_path: Path
    bbox: List[float]


def compile_asset_to_gltf(recipe: Dict, output_dir: Path) -> CompileResult:
    """Convert a primitive recipe into a glTF binary and store it on disk."""

    asset_id = recipe["id"]
    primitives = [_primitive_to_mesh(step) for step in recipe["recipe"]]
    combined = trimesh.util.concatenate(primitives)
    glb_path = output_dir / f"{asset_id}.glb"
    _write_glb(combined, glb_path)
    bbox = combined.bounding_box.extents.tolist()
    return CompileResult(asset_id=asset_id, glb_path=glb_path, bbox=bbox)


def _primitive_to_mesh(step: Dict) -> trimesh.Trimesh:
    primitive = step["primitive"]
    if primitive == "cuboid":
        mesh = trimesh.creation.box(extents=[step.get("w", 1.0), step.get("h", 1.0), step.get("d", 1.0)])
    elif primitive == "cylinder":
        mesh = trimesh.creation.cylinder(radius=step.get("r", 0.5), height=step.get("h", 1.0), sections=24)
    elif primitive == "sphere":
        mesh = trimesh.creation.icosphere(subdivisions=3, radius=step.get("r", 0.5))
    elif primitive == "pyramid":
        mesh = _pyramid(step.get("w", 1.0), step.get("h", 1.0), step.get("d", 1.0))
    elif primitive == "plane":
        mesh = trimesh.creation.box(extents=[step.get("w", 1.0), 0.01, step.get("d", 1.0)])
    else:
        raise ValueError(f"Unsupported primitive: {primitive}")

    offset = step.get("offset")
    if offset:
        mesh.apply_translation(offset)
    return mesh


def _write_glb(mesh: trimesh.Trimesh, path: Path) -> None:
    buffer = trimesh.exchange.gltf.export_glb(mesh)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(buffer)


def _pyramid(width: float, height: float, depth: float) -> trimesh.Trimesh:
    base = np.array([
        [-width / 2, 0.0, -depth / 2],
        [width / 2, 0.0, -depth / 2],
        [width / 2, 0.0, depth / 2],
        [-width / 2, 0.0, depth / 2],
    ])
    apex = np.array([[0.0, height, 0.0]])
    vertices = np.vstack([base, apex])
    faces = np.array([
        [0, 1, 4],
        [1, 2, 4],
        [2, 3, 4],
        [3, 0, 4],
        [0, 1, 2],
        [0, 2, 3],
    ])
    return trimesh.Trimesh(vertices=vertices, faces=faces, process=True)

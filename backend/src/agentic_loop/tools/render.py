"""Rendering helpers that emit visualization artifacts for a scene run."""

from __future__ import annotations

import hashlib
import html
import json
import math
import os
import textwrap
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

from .assets import infer_concept_from_id

SNAPSHOT_SIZE = (1600, 1200)
SNAPSHOT_MARGIN = 120
SNAPSHOT_BACKGROUND = "#0f172a"
SNAPSHOT_HEADER_COLOR = "#e2e8f0"
SNAPSHOT_SUBTEXT_COLOR = "#94a3b8"
SNAPSHOT_GRID_COLOR = (71, 85, 105, 80)
SNAPSHOT_AXIS_COLOR = (94, 234, 212, 160)
SNAPSHOT_FRAME_COLOR = (30, 41, 59, 220)
SNAPSHOT_ZONE_ALPHA = 55
SNAPSHOT_PLACEMENT_ALPHA = 185

_BASE_CONCEPT_COLORS: Dict[str, str] = {
    "river": "#38bdf8",
    "water": "#38bdf8",
    "bridge": "#facc15",
    "market": "#f97316",
    "stall": "#f97316",
    "cottage": "#fbbf24",
    "house": "#fbbf24",
    "residential": "#facc15",
    "barn": "#fb7185",
    "silo": "#fb7185",
    "church": "#c084fc",
    "tower": "#c084fc",
    "fountain": "#60a5fa",
    "well": "#60a5fa",
    "tree": "#22c55e",
    "forest": "#16a34a",
    "fence": "#d4d4d8",
    "path": "#94a3b8",
    "wagon": "#f59e0b",
    "field": "#ca8a04",
}

_FALLBACK_COLORS = [
    "#f472b6",
    "#a855f7",
    "#38bdf8",
    "#14b8a6",
    "#34d399",
    "#f59e0b",
    "#f97316",
    "#ef4444",
]

MATERIAL_PALETTE: Dict[str, str] = {
    "default_grey": "#d1d5db",
    "plaster_white": "#f8fafc",
    "terracotta_red": "#b45309",
    "stone_gray": "#94a3b8",
    "timber_brown": "#b97944",
    "leaf_green": "#22c55e",
    "bark_brown": "#92400e",
    "water_blue": "#3b82f6",
    "copper_green": "#2dd4bf",
    "thatched_straw": "#facc15",
    "brick_red": "#ef4444",
    "slate_blue": "#6366f1",
    "sandstone": "#fcd34d",
    "dark_roof": "#1e293b",
    "grass_green": "#15803d",
    "dirt_brown": "#78350f",
    "metal_grey": "#64748b",
}

_FONT_CACHE: Dict[int, ImageFont.ImageFont] = {}


@dataclass(slots=True)
class Placement2D:
    ref: str
    asset_id: str
    concept: str
    position: Tuple[float, float, float]
    scale: Tuple[float, float, float]
    rot_y: float


@dataclass(slots=True)
class ZoneFootprint:
    name: str
    zone_type: str
    center: Tuple[float, float, float]
    size: Tuple[float, float, float]


@dataclass(slots=True)
class _Transform:
    min_x: float
    max_x: float
    min_z: float
    max_z: float
    width: int
    height: int
    margin: int

    @property
    def draw_width(self) -> float:
        return max(self.width - self.margin * 2, 1)

    @property
    def draw_height(self) -> float:
        return max(self.height - self.margin * 2, 1)

    @property
    def span_x(self) -> float:
        return max(self.max_x - self.min_x, 1.0)

    @property
    def span_z(self) -> float:
        return max(self.max_z - self.min_z, 1.0)

    def world_to_image(self, x: float, z: float) -> Tuple[float, float]:
        px = self.margin + ((x - self.min_x) / self.span_x) * self.draw_width
        py = self.height - self.margin - ((z - self.min_z) / self.span_z) * self.draw_height
        return px, py


def render_snapshot(scene_graph: Dict) -> Dict:
    root = _snapshot_root()
    root.mkdir(parents=True, exist_ok=True)

    metadata = scene_graph.get("metadata")
    if not isinstance(metadata, dict):
        metadata = {}
        scene_graph["metadata"] = metadata

    run_label = (
        metadata.get("run_id")
        or scene_graph.get("run_id")
        or scene_graph.get("scene_id")
        or metadata.get("scene_id")
        or datetime.utcnow().strftime("run_%Y%m%d_%H%M%S")
    )
    if not isinstance(run_label, str) or not run_label.strip():
        run_label = datetime.utcnow().strftime("run_%Y%m%d_%H%M%S")
    run_label = run_label.strip()

    scene_graph["run_id"] = run_label
    metadata["run_id"] = run_label

    filename = run_label.replace(os.sep, "_")
    if os.altsep:
        filename = filename.replace(os.altsep, "_")

    path = root / f"{filename}.png"
    _draw_top_down(path, scene_graph)
    return {"snapshot_path": str(path)}


def render_web_view(manifest: Dict, manifest_path: str) -> Dict:
    if not manifest_path:
        return {}

    manifest_file = Path(manifest_path)
    metadata = manifest.get("metadata")
    if not isinstance(metadata, dict):
        metadata = {}
        manifest["metadata"] = metadata

    run_label = (
        manifest.get("run_id")
        or metadata.get("run_id")
        or manifest.get("scene_id")
        or metadata.get("scene_id")
        or manifest_file.stem
        or datetime.utcnow().strftime("run_%Y%m%d_%H%M%S")
    )
    if not isinstance(run_label, str) or not run_label.strip():
        run_label = datetime.utcnow().strftime("run_%Y%m%d_%H%M%S")
    run_label = run_label.strip()

    manifest["run_id"] = run_label
    metadata["run_id"] = run_label

    run_dir = manifest_file.parent
    run_dir.mkdir(parents=True, exist_ok=True)

    filename = run_label.replace(os.sep, "_")
    if os.altsep:
        filename = filename.replace(os.altsep, "_")

    html_path = run_dir / f"{filename}.html"
    tsx_path = run_dir / f"{filename}.Canvas.tsx"

    html_path.write_text(_build_html_view(manifest, run_label), encoding="utf-8")
    tsx_path.write_text(_build_tsx_view(manifest, run_label), encoding="utf-8")

    return {
        "viewer_html_path": str(html_path),
        "viewer_canvas_path": str(tsx_path),
    }


def _build_html_view(manifest: Dict, run_label: str) -> str:
        view_model = _build_view_model(manifest, run_label)
        view_model_json = json.dumps(view_model, indent=2)
        fallback_json = json.dumps(_FALLBACK_COLORS)

        prompt_text = html.escape(view_model.get("prompt") or "").replace("\n", "<br />")
        generated_at = view_model.get("generatedAt", "")
        placement_count = len(view_model.get("placements", []))
        asset_count = len(view_model.get("assets", {}))

        prompt_block = ""
        if prompt_text:
                prompt_block = textwrap.dedent(
                        f"""
                        <details style="margin-top:12px;">
                            <summary style="cursor:pointer; color:#e2e8f0;">Prompt</summary>
                            <p style="margin:8px 0 0; font-size:13px; line-height:1.45; color:#cbd5f5;">{prompt_text}</p>
                        </details>
                        """
                ).strip()

        script = textwrap.dedent(
                """
                const VIEW_MODEL = __VIEW_MODEL__;
                const FALLBACK_COLORS = __FALLBACK__;

                const CDN_SOURCES = [
                    "https://cdn.jsdelivr.net/npm/three@0.160.1/build/three.module.js",
                    "https://unpkg.com/three@0.160.1/build/three.module.js"
                ];

                const statusElement = document.getElementById("status");

                function setStatus(message, isError = false) {
                    if (!statusElement) return;
                    statusElement.textContent = message || "";
                    statusElement.style.color = isError ? "#f87171" : "#94a3b8";
                }

                function toRadians(value) {
                    if (!Number.isFinite(value)) return 0;
                    return Math.abs(value) > Math.PI ? (value * Math.PI) / 180 : value;
                }

                function normalizeArray(value, length, fallback) {
                    const result = new Array(length).fill(fallback);
                    if (Array.isArray(value)) {
                        value.slice(0, length).forEach((entry, index) => {
                            const numeric = Number(entry);
                            result[index] = Number.isFinite(numeric) ? numeric : fallback;
                        });
                    } else if (Number.isFinite(Number(value))) {
                        const numeric = Number(value);
                        result.fill(numeric);
                    }
                    return result;
                }

                function normalizeRotation(rotation) {
                    if (!rotation) {
                        return { x: 0, y: 0, z: 0 };
                    }
                    if (Array.isArray(rotation)) {
                        const values = normalizeArray(rotation, 3, 0);
                        return { x: toRadians(values[0]), y: toRadians(values[1]), z: toRadians(values[2]) };
                    }
                    if (typeof rotation === "object") {
                        return {
                            x: toRadians(Number(rotation.x) || 0),
                            y: toRadians(Number(rotation.y) || 0),
                            z: toRadians(Number(rotation.z) || 0)
                        };
                    }
                    const value = toRadians(Number(rotation) || 0);
                    return { x: 0, y: value, z: 0 };
                }

                function fallbackColor(seed) {
                    let hash = 0;
                    const text = String(seed || "material");
                    for (let index = 0; index < text.length; index += 1) {
                        hash = (hash * 31 + text.charCodeAt(index)) >>> 0;
                    }
                    return FALLBACK_COLORS[hash % FALLBACK_COLORS.length] || "#94a3b8";
                }

                function colorFromMaterial(materialName) {
                    const palette = VIEW_MODEL.materialPalette || {};
                    const key = String(materialName || "").toLowerCase();
                    return palette[key] || fallbackColor(key);
                }

                function buildPrimitiveMesh(THREE, primitive, materials, fallback) {
                    if (!primitive || typeof primitive !== "object") {
                        return null;
                    }
                    const type = String(primitive.primitive || primitive.type || "cuboid").toLowerCase();
                    let geometry;
                    if (type === "plane") {
                        const width = Number(primitive.w ?? primitive.width ?? 20) || 20;
                        const depth = Number(primitive.d ?? primitive.depth ?? width) || width;
                        geometry = new THREE.PlaneGeometry(Math.max(width, 0.1), Math.max(depth, 0.1));
                    } else if (type === "cylinder") {
                        const radius = Number(primitive.r ?? primitive.radius ?? 1) || 1;
                        const height = Number(primitive.h ?? primitive.height ?? 1) || 1;
                        const radiusTop = Number(primitive.radiusTop ?? radius) || radius;
                        const radiusBottom = Number(primitive.radiusBottom ?? radius) || radius;
                        const segments = Math.max(12, Number(primitive.segments ?? primitive.radialSegments ?? 24) || 24);
                        geometry = new THREE.CylinderGeometry(radiusTop, radiusBottom, height, segments);
                    } else if (type === "sphere") {
                        const radius = Number(primitive.r ?? primitive.radius ?? 1) || 1;
                        geometry = new THREE.SphereGeometry(radius, 24, 16);
                    } else if (type === "pyramid") {
                        const width = Number(primitive.w ?? primitive.width ?? 4) || 4;
                        const depth = Number(primitive.d ?? primitive.depth ?? width) || width;
                        const height = Number(primitive.h ?? primitive.height ?? 3) || 3;
                        const radius = Math.max(width, depth) / 2;
                        geometry = new THREE.ConeGeometry(Math.max(radius, 0.1), Math.max(height, 0.1), 4);
                    } else {
                        const width = Number(primitive.w ?? primitive.width ?? 4) || 4;
                        const height = Number(primitive.h ?? primitive.height ?? 4) || 4;
                        const depth = Number(primitive.d ?? primitive.depth ?? width) || width;
                        geometry = new THREE.BoxGeometry(Math.max(width, 0.1), Math.max(height, 0.1), Math.max(depth, 0.1));
                    }

                    const materialName =
                        primitive.material ||
                        (primitive.name && materials[primitive.name]) ||
                        materials[type] ||
                        fallback ||
                        primitive.name;

                    const colorHex = primitive.color || colorFromMaterial(materialName);
                    const material = new THREE.MeshStandardMaterial({
                        color: new THREE.Color(colorHex),
                        metalness: 0.1,
                        roughness: 0.75
                    });

                    const mesh = new THREE.Mesh(geometry, material);
                    mesh.castShadow = true;
                    mesh.receiveShadow = type === "plane";

                    const offset = normalizeArray(primitive.offset || primitive.position || [0, 0, 0], 3, 0);
                    mesh.position.set(offset[0], offset[1], offset[2]);

                    if (type === "plane") {
                        mesh.rotation.x = -Math.PI / 2;
                    }

                    if (primitive.rotation) {
                        const rotation = normalizeRotation(primitive.rotation);
                        mesh.rotation.x += rotation.x;
                        mesh.rotation.y += rotation.y;
                        mesh.rotation.z += rotation.z;
                    }

                    if (primitive.scale) {
                        const scale = normalizeArray(primitive.scale, 3, 1);
                        mesh.scale.set(scale[0], scale[1], scale[2]);
                    }

                    return mesh;
                }

                function buildPlacementGroup(THREE, placement, assetIndex) {
                    const group = new THREE.Group();
                    const asset = assetIndex[placement.assetId] || assetIndex[placement.ref];
                    const materials = (asset && asset.materials) || {};
                    let hasChildren = false;

                    if (asset && Array.isArray(asset.recipe)) {
                        for (const primitive of asset.recipe) {
                            const mesh = buildPrimitiveMesh(THREE, primitive, materials, placement.concept);
                            if (mesh) {
                                group.add(mesh);
                                hasChildren = true;
                            }
                        }
                    }

                    if (!hasChildren) {
                        const fallbackMesh = buildPrimitiveMesh(
                            THREE,
                            { primitive: "cuboid", w: 6, h: 6, d: 6 },
                            {},
                            placement.concept || placement.ref || placement.assetId
                        );
                        if (fallbackMesh) {
                            group.add(fallbackMesh);
                            hasChildren = true;
                        }
                    }

                    if (!hasChildren) {
                        return null;
                    }

                    const bbox = new THREE.Box3().setFromObject(group);
                    if (Number.isFinite(bbox.min.y) && Math.abs(bbox.min.y) > 1e-3) {
                        group.children.forEach((child) => {
                            child.position.y -= bbox.min.y;
                        });
                    }

                    const position = normalizeArray(placement.position, 3, 0);
                    group.position.set(position[0], position[1], position[2]);

                    const rotation = placement.rotation || {};
                    group.rotation.set(
                        Number(rotation.x) || 0,
                        Number(rotation.y) || 0,
                        Number(rotation.z) || 0
                    );

                    const scale = normalizeArray(placement.scale, 3, 1);
                    group.scale.set(scale[0], scale[1], scale[2]);

                    group.userData.placement = placement;
                    return group;
                }

                function createOrbitController(THREE, camera, domElement) {
                    const target = new THREE.Vector3();
                    const spherical = new THREE.Spherical();
                    const pointer = new THREE.Vector2();
                    const defaultState = { target: target.clone(), theta: 0, phi: 0, radius: 150 };
                    let dragging = false;

                    domElement.style.touchAction = "none";
                    domElement.style.cursor = "grab";

                    function syncFromCamera() {
                        const offset = camera.position.clone().sub(target);
                        spherical.setFromVector3(offset);
                    }

                    function apply() {
                        const offset = new THREE.Vector3().setFromSpherical(spherical);
                        camera.position.copy(offset.add(target));
                        camera.lookAt(target);
                    }

                    function update() {
                        apply();
                    }

                    function onPointerDown(event) {
                        dragging = true;
                        pointer.set(event.clientX, event.clientY);
                        domElement.style.cursor = "grabbing";
                    }

                    function onPointerMove(event) {
                        if (!dragging) return;
                        const deltaX = event.clientX - pointer.x;
                        const deltaY = event.clientY - pointer.y;
                        const ROTATE_SPEED = 0.0025;
                        spherical.theta -= deltaX * ROTATE_SPEED;
                        spherical.phi -= deltaY * ROTATE_SPEED;
                        const EPS = 0.05;
                        spherical.phi = Math.max(EPS, Math.min(Math.PI - EPS, spherical.phi));
                        apply();
                        pointer.set(event.clientX, event.clientY);
                    }

                    function onPointerUp() {
                        dragging = false;
                        domElement.style.cursor = "grab";
                    }

                    function onWheel(event) {
                        event.preventDefault();
                        const scale = Math.pow(0.95, event.deltaY * 0.01);
                        const minRadius = 10;
                        const maxRadius = 4000;
                        spherical.radius = Math.max(minRadius, Math.min(maxRadius, spherical.radius * scale));
                        apply();
                    }

                    domElement.addEventListener("pointerdown", onPointerDown);
                    window.addEventListener("pointermove", onPointerMove);
                    window.addEventListener("pointerup", onPointerUp);
                    domElement.addEventListener("wheel", onWheel, { passive: false });

                    syncFromCamera();
                    apply();

                    function setTarget(x, y, z) {
                        target.set(x, y, z);
                        syncFromCamera();
                        apply();
                    }

                    function setRadius(value) {
                        spherical.radius = Math.max(10, Math.min(4000, value));
                        apply();
                    }

                    function setAngles(theta, phi) {
                        spherical.theta = theta;
                        spherical.phi = Math.max(0.05, Math.min(Math.PI - 0.05, phi));
                        apply();
                    }

                    function saveState() {
                        defaultState.target.copy(target);
                        defaultState.theta = spherical.theta;
                        defaultState.phi = spherical.phi;
                        defaultState.radius = spherical.radius;
                    }

                    function reset() {
                        target.copy(defaultState.target);
                        spherical.theta = defaultState.theta;
                        spherical.phi = defaultState.phi;
                        spherical.radius = defaultState.radius;
                        apply();
                    }

                    function dispose() {
                        domElement.removeEventListener("pointerdown", onPointerDown);
                        window.removeEventListener("pointermove", onPointerMove);
                        window.removeEventListener("pointerup", onPointerUp);
                        domElement.removeEventListener("wheel", onWheel);
                    }

                    return {
                        target,
                        update,
                        setTarget,
                        setRadius,
                        setAngles,
                        saveState,
                        reset,
                        dispose
                    };
                }

                async function loadThree() {
                    let lastError = null;
                    for (const url of CDN_SOURCES) {
                        try {
                            const module = await import(url);
                            if (module) {
                                return module;
                            }
                        } catch (error) {
                            lastError = error;
                            console.warn("Failed to load", url, error);
                        }
                    }
                    throw lastError || new Error("Unable to load three.js from CDN.");
                }

                async function bootstrap() {
                    const container = document.getElementById("viewer");
                    if (!container) {
                        throw new Error("Viewer container missing.");
                    }

                    setStatus("Loading renderer…");
                    const THREE = await loadThree();

                    const renderer = new THREE.WebGLRenderer({ antialias: true });
                    if ("outputColorSpace" in renderer && THREE.SRGBColorSpace) {
                        renderer.outputColorSpace = THREE.SRGBColorSpace;
                    } else if ("outputEncoding" in renderer && THREE.sRGBEncoding) {
                        renderer.outputEncoding = THREE.sRGBEncoding;
                    }
                    if ("toneMapping" in renderer && THREE.ACESFilmicToneMapping) {
                        renderer.toneMapping = THREE.ACESFilmicToneMapping;
                        renderer.toneMappingExposure = 1.05;
                    }
                    renderer.shadowMap.enabled = true;
                    renderer.setPixelRatio(window.devicePixelRatio || 1);

                    const width = container.clientWidth || window.innerWidth;
                    const height = container.clientHeight || window.innerHeight;
                    renderer.setSize(width, height);
                    container.appendChild(renderer.domElement);

                    const scene = new THREE.Scene();
                    scene.background = new THREE.Color("#0f172a");
                    scene.fog = new THREE.FogExp2("#0f172a", 0.002);

                    const camera = new THREE.PerspectiveCamera(55, width / Math.max(height, 1), 0.1, 5000);
                    camera.position.set(120, 120, 120);

                    const controls = createOrbitController(THREE, camera, renderer.domElement);

                    const ambient = new THREE.HemisphereLight(0xdbeafe, 0x0f172a, 0.6);
                    scene.add(ambient);
                    const directional = new THREE.DirectionalLight(0xffffff, 0.85);
                    directional.position.set(240, 360, 240);
                    directional.castShadow = true;
                    directional.shadow.mapSize.set(2048, 2048);
                    directional.shadow.camera.near = 1;
                    directional.shadow.camera.far = 1200;
                    directional.shadow.camera.left = -400;
                    directional.shadow.camera.right = 400;
                    directional.shadow.camera.top = 400;
                    directional.shadow.camera.bottom = -400;
                    scene.add(directional);

                    const grid = new THREE.GridHelper(800, 32, 0x1e293b, 0x334155);
                    grid.position.y = 0;
                    scene.add(grid);

                    const placements = Array.isArray(VIEW_MODEL.placements) ? VIEW_MODEL.placements : [];
                    const assetIndex = VIEW_MODEL.assets || {};
                    const bounds = new THREE.Box3();

                    placements.forEach((placement) => {
                        const group = buildPlacementGroup(THREE, placement, assetIndex);
                        if (!group) {
                            return;
                        }
                        scene.add(group);
                        group.updateMatrixWorld(true);
                        bounds.expandByObject(group);
                    });

                    if (placements.length === 0 || bounds.isEmpty()) {
                        bounds.setFromCenterAndSize(new THREE.Vector3(0, 0, 0), new THREE.Vector3(200, 80, 200));
                    }

                    const center = bounds.getCenter(new THREE.Vector3());
                    const size = bounds.getSize(new THREE.Vector3());
                    const radius = Math.max(size.x, size.y, size.z, 60);

                    camera.position.set(center.x + radius * 1.2, center.y + radius * 0.8 + 60, center.z + radius * 1.2);
                    controls.setTarget(center.x, Math.max(center.y, 0) + 5, center.z);
                    controls.setRadius(Math.max(radius * 1.4, 80));
                    controls.saveState();

                    const resetButton = document.getElementById("resetCam");
                    if (resetButton) {
                        resetButton.addEventListener("click", () => {
                            controls.reset();
                        });
                    }

                    function handleResize() {
                        const newWidth = container.clientWidth || window.innerWidth;
                        const newHeight = container.clientHeight || window.innerHeight;
                        renderer.setSize(newWidth, newHeight);
                        camera.aspect = newWidth / Math.max(newHeight, 1);
                        camera.updateProjectionMatrix();
                    }

                    window.addEventListener("resize", handleResize);

                    setStatus("");

                    function render() {
                        controls.update();
                        renderer.render(scene, camera);
                        requestAnimationFrame(render);
                    }

                    render();
                }

                bootstrap().catch((error) => {
                    console.error(error);
                    setStatus("Failed to initialize viewer.", true);
                });
                """
        ).strip()

        script = script.replace("__VIEW_MODEL__", view_model_json)
        script = script.replace("__FALLBACK__", fallback_json)

        template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>__RUN_LABEL__ · Scene Viewer</title>
            <style>
                :root {
                    color-scheme: dark;
                    font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                }
                body {
                    margin: 0;
                    background: #0f172a;
                    color: #e2e8f0;
                }
                #app {
                    position: relative;
                    width: 100vw;
                    height: 100vh;
                    overflow: hidden;
                }
                #viewer {
                    width: 100%;
                    height: 100%;
                }
                #overlay {
                    position: absolute;
                    top: 20px;
                    left: 20px;
                    padding: 16px 20px;
                    border-radius: 12px;
                    background: rgba(15, 23, 42, 0.78);
                    border: 1px solid rgba(148, 163, 184, 0.35);
                    backdrop-filter: blur(6px);
                    max-width: 360px;
                }
                #overlay h1 {
                    margin: 0;
                    font-size: 18px;
                    letter-spacing: 0.02em;
                }
                #overlay p.meta {
                    margin: 6px 0 0;
                    font-size: 13px;
                    color: #94a3b8;
                }
                #overlay .stats {
                    margin-top: 12px;
                    font-size: 13px;
                    line-height: 1.5;
                    color: #cbd5f5;
                }
                #overlay button.control {
                    margin-top: 12px;
                    padding: 8px 12px;
                    border-radius: 8px;
                    border: 1px solid rgba(148, 163, 184, 0.4);
                    background: rgba(30, 41, 59, 0.7);
                    color: #e2e8f0;
                    cursor: pointer;
                }
                #overlay button.control:hover {
                    background: rgba(51, 65, 85, 0.9);
                }
                #status {
                    margin-top: 12px;
                    font-size: 13px;
                }
            </style>
        </head>
        <body>
            <div id="app">
                <div id="viewer"></div>
                <div id="overlay">
                    <h1>__RUN_LABEL__</h1>
                    <p class="meta">Generated __GENERATED_AT__</p>
                    <div class="stats">
                        <div><strong>Placements:</strong> __PLACEMENT_COUNT__</div>
                        <div><strong>Assets:</strong> __ASSET_COUNT__</div>
                    </div>
                    __PROMPT_BLOCK__
                    <button id="resetCam" class="control" type="button">Reset Camera</button>
                    <div id="status"></div>
                </div>
            </div>
            <script type="module">
            __SCRIPT__
            </script>
        </body>
        </html>
        """

        html_content = textwrap.dedent(template).strip()
        html_content = html_content.replace("__RUN_LABEL__", html.escape(run_label))
        html_content = html_content.replace("__GENERATED_AT__", html.escape(generated_at or ""))
        html_content = html_content.replace("__PLACEMENT_COUNT__", str(placement_count))
        html_content = html_content.replace("__ASSET_COUNT__", str(asset_count))
        html_content = html_content.replace("__PROMPT_BLOCK__", prompt_block)
        html_content = html_content.replace("__SCRIPT__", script)
        return html_content


def _build_tsx_view(manifest: Dict, run_label: str) -> str:
        view_model = _build_view_model(manifest, run_label)
        view_model_json = json.dumps(view_model, indent=2)
        fallback_json = json.dumps(_FALLBACK_COLORS, indent=2)

        template = """
        import { useEffect, useRef } from "react";
        import * as THREE from "three";

        const VIEW_MODEL = __VIEW_MODEL__ as const;
        const FALLBACK_COLORS = __FALLBACK__ as const;

        type Placement = {
            ref: string;
            assetId: string;
            concept: string;
            position: [number, number, number];
            rotation: { x: number; y: number; z: number };
            scale: [number, number, number];
        };

        type AssetEntry = {
            id: string;
            recipe?: Array<Record<string, any>>;
            materials?: Record<string, string>;
        };

        type MaterialPalette = Record<string, string>;

        const toRadians = (value: number): number => {
            if (!Number.isFinite(value)) return 0;
            return Math.abs(value) > Math.PI ? (value * Math.PI) / 180 : value;
        };

        const normalizeArray = (value: any, length: number, fallback: number): number[] => {
            const result = new Array<number>(length).fill(fallback);
            if (Array.isArray(value)) {
                value.slice(0, length).forEach((entry, index) => {
                    const numeric = Number(entry);
                    result[index] = Number.isFinite(numeric) ? numeric : fallback;
                });
            } else if (Number.isFinite(Number(value))) {
                const numeric = Number(value);
                result.fill(numeric);
            }
            return result;
        };

        const normalizeRotation = (value: any) => {
            if (!value) {
                return { x: 0, y: 0, z: 0 };
            }
            if (Array.isArray(value)) {
                const [x, y, z] = normalizeArray(value, 3, 0);
                return { x: toRadians(x), y: toRadians(y), z: toRadians(z) };
            }
            if (typeof value === "object") {
                return {
                    x: toRadians(Number(value.x) || 0),
                    y: toRadians(Number(value.y) || 0),
                    z: toRadians(Number(value.z) || 0),
                };
            }
            const numeric = toRadians(Number(value) || 0);
            return { x: 0, y: numeric, z: 0 };
        };

        const fallbackColor = (seed: string): string => {
            const text = seed || "material";
            let hash = 0;
            for (let index = 0; index < text.length; index += 1) {
                hash = (hash * 31 + text.charCodeAt(index)) >>> 0;
            }
            return FALLBACK_COLORS[hash % FALLBACK_COLORS.length] || "#94a3b8";
        };

        const colorFromMaterial = (palette: MaterialPalette, name?: string): string => {
            const key = (name || "").toLowerCase();
            return palette[key] || fallbackColor(key);
        };

        const buildPrimitiveMesh = (
            primitive: Record<string, any>,
            materials: Record<string, string>,
            palette: MaterialPalette,
            fallback: string
        ): THREE.Mesh | null => {
            if (!primitive || typeof primitive !== "object") {
                return null;
            }

            const type = String(primitive.primitive || primitive.type || "cuboid").toLowerCase();
            let geometry: THREE.BufferGeometry;

            if (type === "plane") {
                const width = Number(primitive.w ?? primitive.width ?? 20) || 20;
                const depth = Number(primitive.d ?? primitive.depth ?? width) || width;
                geometry = new THREE.PlaneGeometry(Math.max(width, 0.1), Math.max(depth, 0.1));
            } else if (type === "cylinder") {
                const radius = Number(primitive.r ?? primitive.radius ?? 1) || 1;
                const height = Number(primitive.h ?? primitive.height ?? 1) || 1;
                const radiusTop = Number(primitive.radiusTop ?? radius) || radius;
                const radiusBottom = Number(primitive.radiusBottom ?? radius) || radius;
                const segments = Math.max(12, Number(primitive.segments ?? primitive.radialSegments ?? 24) || 24);
                geometry = new THREE.CylinderGeometry(radiusTop, radiusBottom, height, segments);
            } else if (type === "sphere") {
                const radius = Number(primitive.r ?? primitive.radius ?? 1) || 1;
                geometry = new THREE.SphereGeometry(radius, 24, 16);
            } else if (type === "pyramid") {
                const width = Number(primitive.w ?? primitive.width ?? 4) || 4;
                const depth = Number(primitive.d ?? primitive.depth ?? width) || width;
                const height = Number(primitive.h ?? primitive.height ?? 3) || 3;
                const radius = Math.max(width, depth) / 2;
                geometry = new THREE.ConeGeometry(Math.max(radius, 0.1), Math.max(height, 0.1), 4);
            } else {
                const width = Number(primitive.w ?? primitive.width ?? 4) || 4;
                const height = Number(primitive.h ?? primitive.height ?? 4) || 4;
                const depth = Number(primitive.d ?? primitive.depth ?? width) || width;
                geometry = new THREE.BoxGeometry(Math.max(width, 0.1), Math.max(height, 0.1), Math.max(depth, 0.1));
            }

            const materialName =
                primitive.material ||
                (primitive.name && materials[primitive.name]) ||
                materials[type] ||
                fallback ||
                primitive.name;

            const colorHex = primitive.color || colorFromMaterial(palette, materialName);
            const material = new THREE.MeshStandardMaterial({
                color: new THREE.Color(colorHex),
                metalness: 0.1,
                roughness: 0.75,
            });

            const mesh = new THREE.Mesh(geometry, material);
            mesh.castShadow = true;
            mesh.receiveShadow = type === "plane";

            const offset = normalizeArray(primitive.offset || primitive.position || [0, 0, 0], 3, 0);
            mesh.position.set(offset[0], offset[1], offset[2]);

            if (type === "plane") {
                mesh.rotation.x = -Math.PI / 2;
            }

            if (primitive.rotation) {
                const rotation = normalizeRotation(primitive.rotation);
                mesh.rotation.x += rotation.x;
                mesh.rotation.y += rotation.y;
                mesh.rotation.z += rotation.z;
            }

            if (primitive.scale) {
                const scale = normalizeArray(primitive.scale, 3, 1);
                mesh.scale.set(scale[0], scale[1], scale[2]);
            }

            return mesh;
        };

        const buildPlacementGroup = (
            placement: Placement,
            assets: Record<string, AssetEntry>,
            palette: MaterialPalette
        ): THREE.Group | null => {
            const group = new THREE.Group();
            const asset = assets[placement.assetId] || assets[placement.ref];
            const materials = (asset && asset.materials) || {};
            let hasChildren = false;

            if (asset && Array.isArray(asset.recipe)) {
                for (const primitive of asset.recipe) {
                    const mesh = buildPrimitiveMesh(primitive, materials, palette, placement.concept);
                    if (mesh) {
                        group.add(mesh);
                        hasChildren = true;
                    }
                }
            }

            if (!hasChildren) {
                const fallbackMesh = buildPrimitiveMesh(
                    { primitive: "cuboid", w: 6, h: 6, d: 6 },
                    {},
                    palette,
                    placement.concept || placement.ref || placement.assetId
                );
                if (fallbackMesh) {
                    group.add(fallbackMesh);
                    hasChildren = true;
                }
            }

            if (!hasChildren) {
                return null;
            }

            const bbox = new THREE.Box3().setFromObject(group);
            if (Number.isFinite(bbox.min.y) && Math.abs(bbox.min.y) > 1e-3) {
                group.children.forEach((child) => {
                    child.position.y -= bbox.min.y;
                });
            }

            const position = normalizeArray(placement.position, 3, 0);
            group.position.set(position[0], position[1], position[2]);

            const rotation = placement.rotation || { x: 0, y: 0, z: 0 };
            group.rotation.set(rotation.x, rotation.y, rotation.z);

            const scale = normalizeArray(placement.scale, 3, 1);
            group.scale.set(scale[0], scale[1], scale[2]);

            group.userData.placement = placement;
            return group;
        };

        type OrbitController = {
            update: () => void;
            setTarget: (x: number, y: number, z: number) => void;
            setRadius: (distance: number) => void;
            setAngles: (theta: number, phi: number) => void;
            saveState: () => void;
            reset: () => void;
            dispose: () => void;
        };

        // Lightweight orbit control to avoid depending on examples bundle.
        const createOrbitController = (camera: THREE.PerspectiveCamera, domElement: HTMLElement): OrbitController => {
            const target = new THREE.Vector3();
            const spherical = new THREE.Spherical();
            const pointer = new THREE.Vector2();
            const defaultState = { target: target.clone(), theta: 0, phi: 0, radius: 150 };
            let dragging = false;

            domElement.style.touchAction = "none";
            domElement.style.cursor = "grab";

            const syncFromCamera = () => {
                const offset = camera.position.clone().sub(target);
                spherical.setFromVector3(offset);
            };

            const apply = () => {
                const offset = new THREE.Vector3().setFromSpherical(spherical);
                camera.position.copy(offset.add(target));
                camera.lookAt(target);
            };

            const update = () => {
                apply();
            };

            const onPointerDown = (event: PointerEvent) => {
                dragging = true;
                pointer.set(event.clientX, event.clientY);
                domElement.style.cursor = "grabbing";
            };

            const onPointerMove = (event: PointerEvent) => {
                if (!dragging) return;
                const deltaX = event.clientX - pointer.x;
                const deltaY = event.clientY - pointer.y;
                const ROTATE_SPEED = 0.0025;
                spherical.theta -= deltaX * ROTATE_SPEED;
                spherical.phi -= deltaY * ROTATE_SPEED;
                const EPS = 0.05;
                spherical.phi = Math.max(EPS, Math.min(Math.PI - EPS, spherical.phi));
                apply();
                pointer.set(event.clientX, event.clientY);
            };

            const onPointerUp = () => {
                dragging = false;
                domElement.style.cursor = "grab";
            };

            const onWheel = (event: WheelEvent) => {
                event.preventDefault();
                const scale = Math.pow(0.95, event.deltaY * 0.01);
                const minRadius = 10;
                const maxRadius = 4000;
                spherical.radius = Math.max(minRadius, Math.min(maxRadius, spherical.radius * scale));
                apply();
            };

            domElement.addEventListener("pointerdown", onPointerDown);
            window.addEventListener("pointermove", onPointerMove);
            window.addEventListener("pointerup", onPointerUp);
            domElement.addEventListener("wheel", onWheel, { passive: false });

            syncFromCamera();
            apply();

            const setTarget = (x: number, y: number, z: number) => {
                target.set(x, y, z);
                syncFromCamera();
                apply();
            };

            const setRadius = (distance: number) => {
                spherical.radius = Math.max(10, Math.min(4000, distance));
                apply();
            };

            const setAngles = (theta: number, phi: number) => {
                spherical.theta = theta;
                spherical.phi = Math.max(0.05, Math.min(Math.PI - 0.05, phi));
                apply();
            };

            const saveState = () => {
                defaultState.target.copy(target);
                defaultState.theta = spherical.theta;
                defaultState.phi = spherical.phi;
                defaultState.radius = spherical.radius;
            };

            const reset = () => {
                target.copy(defaultState.target);
                spherical.theta = defaultState.theta;
                spherical.phi = defaultState.phi;
                spherical.radius = defaultState.radius;
                apply();
            };

            const dispose = () => {
                domElement.removeEventListener("pointerdown", onPointerDown);
                window.removeEventListener("pointermove", onPointerMove);
                window.removeEventListener("pointerup", onPointerUp);
                domElement.removeEventListener("wheel", onWheel);
            };

            return { update, setTarget, setRadius, setAngles, saveState, reset, dispose };
        };

        const SceneCanvas = () => {
            const containerRef = useRef<HTMLDivElement | null>(null);

            useEffect(() => {
                const container = containerRef.current;
                if (!container) {
                    return;
                }

                const renderer = new THREE.WebGLRenderer({ antialias: true });
                if ("outputColorSpace" in renderer && (THREE as any).SRGBColorSpace) {
                    (renderer as any).outputColorSpace = (THREE as any).SRGBColorSpace;
                } else if ("outputEncoding" in renderer && (THREE as any).sRGBEncoding) {
                    (renderer as any).outputEncoding = (THREE as any).sRGBEncoding;
                }
                if ("toneMapping" in renderer && (THREE as any).ACESFilmicToneMapping) {
                    renderer.toneMapping = (THREE as any).ACESFilmicToneMapping;
                    renderer.toneMappingExposure = 1.05;
                }
                renderer.shadowMap.enabled = true;
                renderer.setPixelRatio(window.devicePixelRatio || 1);

                const width = container.clientWidth || window.innerWidth;
                const height = container.clientHeight || window.innerHeight;
                renderer.setSize(width, height);
                container.appendChild(renderer.domElement);

                const scene = new THREE.Scene();
                scene.background = new THREE.Color("#0f172a");
                scene.fog = new THREE.FogExp2("#0f172a", 0.002);

                const camera = new THREE.PerspectiveCamera(55, width / Math.max(height, 1), 0.1, 5000);
                camera.position.set(120, 120, 120);

                const controls = createOrbitController(camera, renderer.domElement);

                const ambient = new THREE.HemisphereLight(0xdbeafe, 0x0f172a, 0.6);
                scene.add(ambient);
                const directional = new THREE.DirectionalLight(0xffffff, 0.85);
                directional.position.set(240, 360, 240);
                directional.castShadow = true;
                directional.shadow.mapSize.set(2048, 2048);
                directional.shadow.camera.near = 1;
                directional.shadow.camera.far = 1200;
                directional.shadow.camera.left = -400;
                directional.shadow.camera.right = 400;
                directional.shadow.camera.top = 400;
                directional.shadow.camera.bottom = -400;
                scene.add(directional);

                const grid = new THREE.GridHelper(800, 32, 0x1e293b, 0x334155);
                grid.position.y = 0;
                scene.add(grid);

                const assets = (VIEW_MODEL.assets as Record<string, AssetEntry>) || {};
                const palette = (VIEW_MODEL.materialPalette as MaterialPalette) || {};
                const placements = (VIEW_MODEL.placements as unknown as Placement[]) || [];
                const bounds = new THREE.Box3();

                placements.forEach((placement) => {
                    const group = buildPlacementGroup(placement, assets, palette);
                    if (!group) {
                        return;
                    }
                    scene.add(group);
                    group.updateMatrixWorld(true);
                    bounds.expandByObject(group);
                });

                if (placements.length === 0 || bounds.isEmpty()) {
                    bounds.setFromCenterAndSize(new THREE.Vector3(0, 0, 0), new THREE.Vector3(200, 80, 200));
                }

                const center = bounds.getCenter(new THREE.Vector3());
                const size = bounds.getSize(new THREE.Vector3());
                const radius = Math.max(size.x, size.y, size.z, 60);

                camera.position.set(center.x + radius * 1.2, center.y + radius * 0.8 + 60, center.z + radius * 1.2);
                controls.setTarget(center.x, Math.max(center.y, 0) + 5, center.z);
                controls.setRadius(Math.max(radius * 1.4, 80));
                controls.saveState();

                const handleResize = () => {
                    const newWidth = container.clientWidth || window.innerWidth;
                    const newHeight = container.clientHeight || window.innerHeight;
                    renderer.setSize(newWidth, newHeight);
                    camera.aspect = newWidth / Math.max(newHeight, 1);
                    camera.updateProjectionMatrix();
                };

                window.addEventListener("resize", handleResize);

                let animationId = 0;
                const renderFrame = () => {
                    controls.update();
                    renderer.render(scene, camera);
                    animationId = window.requestAnimationFrame(renderFrame);
                };

                renderFrame();

                return () => {
                    window.cancelAnimationFrame(animationId);
                    window.removeEventListener("resize", handleResize);
                    controls.dispose();
                    scene.traverse((object) => {
                        const mesh = object as THREE.Mesh;
                        if (mesh.isMesh) {
                            mesh.geometry.dispose();
                            if (Array.isArray(mesh.material)) {
                                mesh.material.forEach((material) => material.dispose?.());
                            } else {
                                mesh.material.dispose?.();
                            }
                        }
                    });
                    renderer.dispose();
                    if (renderer.domElement.parentElement === container) {
                        container.removeChild(renderer.domElement);
                    }
                };
            }, []);

            return (
                <div
                    ref={containerRef}
                    style={{ width: "100%", height: "100%", position: "relative", background: "#0f172a" }}
                    aria-label={`scene-viewer-__RUN_LABEL__`}
                />
            );
        };

        export default SceneCanvas;
        """

        code = textwrap.dedent(template).strip()
        code = code.replace("__VIEW_MODEL__", view_model_json)
        code = code.replace("__FALLBACK__", fallback_json)
        code = code.replace("__RUN_LABEL__", run_label)
        return code


def _snapshot_root() -> Path:
    env_root = os.environ.get("SNAPSHOT_ROOT")
    if env_root:
        return Path(env_root).expanduser()
    return Path(__file__).resolve().parents[4] / "snapshots"


def _draw_top_down(path: Path, scene_graph: Dict) -> None:
    placements = _extract_placements(scene_graph)
    zones = _extract_zones(scene_graph)

    width, height = SNAPSHOT_SIZE
    image = Image.new("RGB", (width, height), SNAPSHOT_BACKGROUND)
    draw = ImageDraw.Draw(image, "RGBA")

    transform = _compute_transform(placements, zones, width, height, SNAPSHOT_MARGIN)

    _draw_frame(draw, width, height, SNAPSHOT_MARGIN)
    _draw_grid(draw, transform, width, height, SNAPSHOT_MARGIN)
    _draw_axes(draw, transform)
    _draw_zones(draw, zones, transform)
    _draw_placements(draw, placements, transform)
    _draw_header(draw, scene_graph, placements, width, SNAPSHOT_MARGIN)
    _draw_legend(draw, placements, width, height, SNAPSHOT_MARGIN)

    if not placements:
        _draw_empty_notice(draw, width, height)

    image.save(path, format="PNG")


def _extract_placements(scene_graph: Dict) -> List[Placement2D]:
    raw: Iterable = []
    if isinstance(scene_graph.get("placements"), Iterable):
        raw = scene_graph.get("placements") or []
    elif isinstance(scene_graph.get("scene_graph"), dict):
        raw = scene_graph["scene_graph"].get("placements") or []

    placements: List[Placement2D] = []
    for entry in raw:
        if not isinstance(entry, dict):
            continue
        pos = entry.get("pos") or entry.get("position") or _nested(entry, "transform", "pos")
        if not isinstance(pos, Iterable):
            if all(key in entry for key in ("x", "y", "z")):
                pos = [entry.get("x"), entry.get("y"), entry.get("z")]
        if not isinstance(pos, Iterable):
            continue
        pos_list = list(pos)
        if len(pos_list) < 3:
            continue
        x = float(pos_list[0] or 0)
        y = float(pos_list[1] or 0)
        z = float(pos_list[2] or 0)

        scale_value = entry.get("scale") or _nested(entry, "transform", "scale")
        if not isinstance(scale_value, Iterable) and all(key in entry for key in ("sx", "sy", "sz")):
            scale_value = [entry.get("sx"), entry.get("sy"), entry.get("sz")]
        if scale_value is None:
            scale_value = [1, 1, 1]
        if isinstance(scale_value, (int, float)):
            scale_list = [float(scale_value)] * 3
        elif isinstance(scale_value, Iterable):
            scale_list = [float(value or 1) for value in list(scale_value)[:3]]
        else:
            scale_list = [1.0, 1.0, 1.0]
        while len(scale_list) < 3:
            scale_list.append(scale_list[0])

        rot_value = (
            entry.get("rotY")
            or entry.get("ry")
            or _nested(entry, "rotation", "y")
            or _nested(entry, "transform", "rot", 1)
            or 0
        )
        try:
            rot_y = float(rot_value)
        except (TypeError, ValueError):
            rot_y = 0.0
        if abs(rot_y) > math.tau:
            rot_y = math.radians(rot_y)

        asset_id = (
            entry.get("asset_id")
            or entry.get("asset")
            or entry.get("id")
            or entry.get("ref")
            or "asset"
        )
        asset_id = str(asset_id)
        ref = str(entry.get("ref") or entry.get("name") or asset_id)
        concept = infer_concept_from_id(asset_id)

        placements.append(
            Placement2D(
                ref=ref,
                asset_id=asset_id,
                concept=concept,
                position=(x, y, z),
                scale=(float(scale_list[0]), float(scale_list[1]), float(scale_list[2])),
                rot_y=rot_y,
            )
        )

    return placements


def _extract_zones(scene_graph: Dict) -> List[ZoneFootprint]:
    map_section = scene_graph.get("map")
    if not isinstance(map_section, dict) and isinstance(scene_graph.get("scene_graph"), dict):
        map_section = scene_graph["scene_graph"].get("map")
    if not isinstance(map_section, dict):
        return []

    zones_data = map_section.get("zones")
    if not isinstance(zones_data, Iterable):
        return []

    zones: List[ZoneFootprint] = []
    for zone in zones_data:
        if not isinstance(zone, dict):
            continue
        pos = zone.get("position") or [0, 0, 0]
        size = zone.get("size") or [0, 0, 0]
        if not isinstance(pos, Iterable) or not isinstance(size, Iterable):
            continue
        pos_list = list(pos)
        size_list = list(size)
        while len(pos_list) < 3:
            pos_list.append(0)
        while len(size_list) < 3:
            size_list.append(0)
        zones.append(
            ZoneFootprint(
                name=str(zone.get("name") or "zone"),
                zone_type=str(zone.get("type") or ""),
                center=(float(pos_list[0]), float(pos_list[1]), float(pos_list[2])),
                size=(abs(float(size_list[0])), abs(float(size_list[1])), abs(float(size_list[2]))),
            )
        )
    return zones


def _compute_transform(
    placements: List[Placement2D],
    zones: List[ZoneFootprint],
    width: int,
    height: int,
    margin: int,
) -> _Transform:
    xs: List[float] = []
    zs: List[float] = []

    for placement in placements:
        footprint_w, footprint_d = _footprint_dimensions(placement)
        half_w = footprint_w / 2
        half_d = footprint_d / 2
        xs.extend([placement.position[0] - half_w, placement.position[0] + half_w])
        zs.extend([placement.position[2] - half_d, placement.position[2] + half_d])

    for zone in zones:
        half_w = zone.size[0] / 2
        half_d = zone.size[2] / 2
        xs.extend([zone.center[0] - half_w, zone.center[0] + half_w])
        zs.extend([zone.center[2] - half_d, zone.center[2] + half_d])

    if not xs:
        xs = [-50, 50]
    if not zs:
        zs = [-50, 50]

    min_x = min(xs) - 10
    max_x = max(xs) + 10
    min_z = min(zs) - 10
    max_z = max(zs) + 10

    return _Transform(
        min_x=min_x,
        max_x=max_x,
        min_z=min_z,
        max_z=max_z,
        width=width,
        height=height,
        margin=margin,
    )


def _draw_frame(draw: ImageDraw.ImageDraw, width: int, height: int, margin: int) -> None:
    bounds = [margin - 12, margin - 12, width - margin + 12, height - margin + 12]
    draw.rounded_rectangle(bounds, radius=24, outline=SNAPSHOT_FRAME_COLOR, width=3)


def _draw_grid(draw: ImageDraw.ImageDraw, transform: _Transform, width: int, height: int, margin: int) -> None:
    steps = 10
    for index in range(steps + 1):
        fraction = index / steps
        x = margin + fraction * transform.draw_width
        y = margin + fraction * transform.draw_height
        draw.line([(x, margin), (x, height - margin)], fill=SNAPSHOT_GRID_COLOR, width=1)
        draw.line([(margin, y), (width - margin, y)], fill=SNAPSHOT_GRID_COLOR, width=1)


def _draw_axes(draw: ImageDraw.ImageDraw, transform: _Transform) -> None:
    center_x = (transform.min_x + transform.max_x) / 2
    center_z = (transform.min_z + transform.max_z) / 2
    draw.line(
        [transform.world_to_image(transform.min_x, center_z), transform.world_to_image(transform.max_x, center_z)],
        fill=SNAPSHOT_AXIS_COLOR,
        width=2,
    )
    draw.line(
        [transform.world_to_image(center_x, transform.min_z), transform.world_to_image(center_x, transform.max_z)],
        fill=SNAPSHOT_AXIS_COLOR,
        width=2,
    )


def _draw_zones(draw: ImageDraw.ImageDraw, zones: List[ZoneFootprint], transform: _Transform) -> None:
    font = _load_font(20)
    for zone in zones:
        half_w = zone.size[0] / 2
        half_d = zone.size[2] / 2
        corners = [
            transform.world_to_image(zone.center[0] - half_w, zone.center[2] - half_d),
            transform.world_to_image(zone.center[0] + half_w, zone.center[2] - half_d),
            transform.world_to_image(zone.center[0] + half_w, zone.center[2] + half_d),
            transform.world_to_image(zone.center[0] - half_w, zone.center[2] + half_d),
        ]
        color = _zone_color(zone.zone_type)
        draw.polygon(corners, fill=_hex_to_rgba(color, SNAPSHOT_ZONE_ALPHA), outline=_hex_to_rgba(color, 180))

        label_x, label_y = transform.world_to_image(zone.center[0], zone.center[2])
        text_width, text_height = _measure_text(draw, zone.name, font)
        draw.rounded_rectangle(
            [
                label_x - text_width / 2 - 8,
                label_y - text_height / 2 - 4,
                label_x + text_width / 2 + 8,
                label_y + text_height / 2 + 6,
            ],
            radius=8,
            fill=(15, 23, 42, 200),
        )
        draw.text((label_x - text_width / 2, label_y - text_height / 2), zone.name, font=font, fill=SNAPSHOT_HEADER_COLOR)


def _draw_placements(draw: ImageDraw.ImageDraw, placements: List[Placement2D], transform: _Transform) -> None:
    label_font = _load_font(22)
    for placement in placements:
        color = _concept_color(placement.concept)
        width, depth = _footprint_dimensions(placement)
        half_w = width / 2
        half_d = depth / 2

        cos_r = math.cos(placement.rot_y)
        sin_r = math.sin(placement.rot_y)
        polygon = []
        for local_x, local_z in [(-half_w, -half_d), (half_w, -half_d), (half_w, half_d), (-half_w, half_d)]:
            world_x = placement.position[0] + local_x * cos_r - local_z * sin_r
            world_z = placement.position[2] + local_x * sin_r + local_z * cos_r
            polygon.append(transform.world_to_image(world_x, world_z))

        draw.polygon(polygon, fill=_hex_to_rgba(color, SNAPSHOT_PLACEMENT_ALPHA), outline=_hex_to_rgba(color, 240))

        center = transform.world_to_image(placement.position[0], placement.position[2])
        orient_x = placement.position[0] + math.sin(placement.rot_y) * max(depth / 2, 6)
        orient_z = placement.position[2] + math.cos(placement.rot_y) * max(depth / 2, 6)
        orient = transform.world_to_image(orient_x, orient_z)
        draw.line([center, orient], fill=_hex_to_rgba(color, 255), width=3)
        draw.ellipse([center[0] - 4, center[1] - 4, center[0] + 4, center[1] + 4], fill=_hex_to_rgba(color, 255))

        min_x = min(point[0] for point in polygon)
        min_y = min(point[1] for point in polygon)
        text_width, text_height = _measure_text(draw, placement.ref, label_font)
        text_x = max(min_x, transform.margin + 4)
        text_y = max(min_y - text_height - 6, transform.margin + 4)
        draw.text((text_x, text_y), placement.ref, font=label_font, fill=SNAPSHOT_HEADER_COLOR)


def _draw_header(
    draw: ImageDraw.ImageDraw,
    scene_graph: Dict,
    placements: List[Placement2D],
    width: int,
    margin: int,
) -> None:
    font_title = _load_font(44)
    font_meta = _load_font(26)

    metadata = scene_graph.get("metadata") if isinstance(scene_graph.get("metadata"), dict) else {}
    title = str(
        (metadata or {}).get("run_id")
        or scene_graph.get("run_id")
        or scene_graph.get("scene_id")
        or scene_graph.get("name")
        or "Scene"
    )
    draw.text((margin, 32), title, font=font_title, fill=SNAPSHOT_HEADER_COLOR)
    draw.text((margin, margin - 60), f"Placements: {len(placements)}", font=font_meta, fill=SNAPSHOT_SUBTEXT_COLOR)


def _draw_legend(
    draw: ImageDraw.ImageDraw,
    placements: List[Placement2D],
    width: int,
    height: int,
    margin: int,
) -> None:
    if not placements:
        return

    counts: Dict[str, int] = {}
    for placement in placements:
        counts[placement.concept] = counts.get(placement.concept, 0) + 1

    items = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:10]
    if not items:
        return

    legend_width = 260
    legend_height = 30 + 28 * len(items)
    origin_x = width - margin - legend_width
    origin_y = margin - 20

    draw.rounded_rectangle(
        [origin_x, origin_y, origin_x + legend_width, origin_y + legend_height],
        radius=16,
        fill=(15, 23, 42, 220),
    )

    title_font = _load_font(22)
    item_font = _load_font(20)
    draw.text((origin_x + 16, origin_y + 10), "Legend", font=title_font, fill=SNAPSHOT_HEADER_COLOR)

    for index, (concept, count) in enumerate(items, start=1):
        color = _concept_color(concept)
        y = origin_y + 12 + index * 24
        draw.rectangle([origin_x + 16, y, origin_x + 36, y + 14], fill=_hex_to_rgba(color, 255))
        draw.text((origin_x + 44, y - 4), f"{concept} ({count})", font=item_font, fill=SNAPSHOT_SUBTEXT_COLOR)


def _draw_empty_notice(draw: ImageDraw.ImageDraw, width: int, height: int) -> None:
    font = _load_font(36)
    message = "No placements available"
    text_w, text_h = _measure_text(draw, message, font)
    draw.text(((width - text_w) / 2, (height - text_h) / 2), message, font=font, fill=SNAPSHOT_SUBTEXT_COLOR)


def _footprint_dimensions(placement: Placement2D) -> Tuple[float, float]:
    scale_x = max(abs(placement.scale[0]), 1.0)
    scale_z = max(abs(placement.scale[2]), 1.0)
    base = max(scale_x, scale_z, 1.0)
    width = base * 6
    depth = scale_z * 6
    if "river" in placement.concept:
        width = max(scale_x * 12, 18)
        depth = max(scale_z * 24, 220)
    elif "bridge" in placement.concept:
        width = max(scale_x * 4, 12)
        depth = max(scale_z * 12, 60)
    elif "tree" in placement.concept:
        width = max(scale_x * 3, 8)
        depth = max(scale_z * 3, 8)
    elif "fence" in placement.concept or "path" in placement.concept:
        width = max(scale_x * 2, 6)
        depth = max(scale_z * 12, 40)
    return width, depth


def _concept_color(concept: str) -> str:
    lowered = concept.lower()
    for key, color in _BASE_CONCEPT_COLORS.items():
        if key in lowered:
            return color
    digest = hashlib.sha1(lowered.encode("utf-8")).hexdigest()
    index = int(digest[:8], 16) % len(_FALLBACK_COLORS)
    return _FALLBACK_COLORS[index]


def _zone_color(zone_type: str) -> str:
    zone_type = zone_type.lower()
    if "commercial" in zone_type or "market" in zone_type:
        return "#f97316"
    if "residential" in zone_type:
        return "#22c55e"
    if "agricultural" in zone_type or "farm" in zone_type:
        return "#facc15"
    if "landmark" in zone_type:
        return "#38bdf8"
    if "natural" in zone_type or "forest" in zone_type:
        return "#0ea5e9"
    return "#94a3b8"


def _hex_to_rgba(color: str, alpha: int) -> Tuple[int, int, int, int]:
    color = color.lstrip("#")
    value = int(color, 16)
    r = (value >> 16) & 0xFF
    g = (value >> 8) & 0xFF
    b = value & 0xFF
    return r, g, b, max(0, min(alpha, 255))


def _load_font(size: int) -> ImageFont.ImageFont:
    cached = _FONT_CACHE.get(size)
    if cached:
        return cached
    for candidate in ["SFNSDisplay.ttf", "Arial.ttf", "Helvetica.ttc", "Menlo.ttc", "DejaVuSans.ttf"]:
        try:
            font = ImageFont.truetype(candidate, size)
            _FONT_CACHE[size] = font
            return font
        except (OSError, IOError):
            continue
    fallback = ImageFont.load_default()
    _FONT_CACHE[size] = fallback
    return fallback


def _nested(value: Dict, *keys: int | str) -> Optional[object]:
    current: Optional[object] = value
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        elif isinstance(current, (list, tuple)) and isinstance(key, int) and 0 <= key < len(current):
            current = current[key]
        else:
            return None
    return current


def _measure_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> Tuple[int, int]:
    if hasattr(draw, "textbbox"):
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox:
            width = max(int(bbox[2] - bbox[0]), 0)
            height = max(int(bbox[3] - bbox[1]), 0)
            return width, height
    if hasattr(draw, "textsize"):
        return draw.textsize(text, font=font)
    approximate_width = max(int(len(text) * font.size * 0.55), 1)
    return approximate_width, font.size


def _build_view_model(manifest: Dict, run_label: str) -> Dict:
    placements: List[Dict] = []
    for placement in _extract_placements(manifest):
        placements.append(
            {
                "ref": placement.ref,
                "assetId": placement.asset_id,
                "concept": placement.concept,
                "position": [round(float(placement.position[0]), 4), round(float(placement.position[1]), 4), round(float(placement.position[2]), 4)],
                "rotation": {
                    "x": 0.0,
                    "y": round(float(placement.rot_y), 6),
                    "z": 0.0,
                },
                "rotationDegrees": {
                    "x": 0.0,
                    "y": round(math.degrees(float(placement.rot_y)), 3),
                    "z": 0.0,
                },
                "scale": [
                    round(max(float(placement.scale[0]), 0.001), 4),
                    round(max(float(placement.scale[1]), 0.001), 4),
                    round(max(float(placement.scale[2]), 0.001), 4),
                ],
            }
        )

    asset_index = _extract_asset_index(manifest)
    material_palette: Dict[str, str] = {}
    for name, hex_color in MATERIAL_PALETTE.items():
        material_palette[name.lower()] = hex_color
    for asset in asset_index.values():
        materials = asset.get("materials") or {}
        for material_name in materials.values():
            if not material_name:
                continue
            lowered = str(material_name).lower()
            material_palette.setdefault(lowered, _material_color(lowered))

    return {
        "runId": run_label,
        "sceneId": run_label,
        "prompt": manifest.get("prompt") or "",
        "placements": placements,
        "assets": asset_index,
        "materialPalette": material_palette,
        "generatedAt": datetime.utcnow().isoformat() + "Z",
    }


def _extract_asset_index(manifest: Dict) -> Dict[str, Dict]:
    index: Dict[str, Dict] = {}

    assets = manifest.get("assets")
    if isinstance(assets, list):
        for asset in assets:
            if not isinstance(asset, dict):
                continue
            asset_id = asset.get("id") or asset.get("asset_id") or asset.get("name")
            if not asset_id:
                continue
            asset_id = str(asset_id)
            recipe = asset.get("recipe")
            recipe_dict = recipe if isinstance(recipe, dict) else {}
            primitives = []
            if isinstance(recipe_dict, dict):
                raw_recipe = recipe_dict.get("recipe")
                if isinstance(raw_recipe, list):
                    primitives = [entry for entry in raw_recipe if isinstance(entry, dict)]
            materials = {}
            if isinstance(recipe_dict.get("materials"), dict):
                materials = {str(key): str(value) for key, value in recipe_dict["materials"].items()}
            elif isinstance(asset.get("materials"), dict):
                materials = {str(key): str(value) for key, value in asset["materials"].items()}

            index[asset_id] = {
                "id": asset_id,
                "recipe": primitives,
                "materials": materials,
                "tags": asset.get("tags") or recipe_dict.get("tags") or [],
                "bbox": asset.get("bbox"),
            }

    return index


def _material_color(material_name: str) -> str:
    material_name = material_name.lower().strip()
    if material_name in MATERIAL_PALETTE:
        return MATERIAL_PALETTE[material_name]
    digest = hashlib.sha1(material_name.encode("utf-8")).hexdigest()
    index = int(digest[:8], 16) % len(_FALLBACK_COLORS)
    return _FALLBACK_COLORS[index]

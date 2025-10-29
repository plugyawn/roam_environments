import { useEffect, useRef } from "react";
import * as THREE from "three";

const VIEW_MODEL = {
  "sceneId": "riverside_village_market_001",
  "prompt": "Design a pastoral riverside village with a market square",
  "placements": [
    {
      "ref": "asset_001",
      "assetId": "asset_001",
      "concept": "asset",
      "position": [
        60.0,
        0.0,
        170.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "asset_002",
      "assetId": "asset_002",
      "concept": "asset",
      "position": [
        75.0,
        0.0,
        150.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "asset_003",
      "assetId": "asset_003",
      "concept": "asset",
      "position": [
        30.0,
        0.0,
        200.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 1.57,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 89.954,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "asset_004",
      "assetId": "asset_004",
      "concept": "asset",
      "position": [
        30.0,
        0.0,
        230.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 1.57,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 89.954,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "asset_005",
      "assetId": "asset_005",
      "concept": "asset",
      "position": [
        65.0,
        0.0,
        145.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "asset_005",
      "assetId": "asset_005",
      "concept": "asset",
      "position": [
        85.0,
        0.0,
        145.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "asset_005",
      "assetId": "asset_005",
      "concept": "asset",
      "position": [
        65.0,
        0.0,
        155.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "asset_005",
      "assetId": "asset_005",
      "concept": "asset",
      "position": [
        85.0,
        0.0,
        155.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "asset_006",
      "assetId": "asset_006",
      "concept": "asset",
      "position": [
        90.0,
        0.0,
        170.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "asset_007",
      "assetId": "asset_007",
      "concept": "asset",
      "position": [
        45.0,
        0.0,
        120.0
      ],
      "rotation": {
        "x": 0.0,
        "y": -1.57,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": -89.954,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "asset_008",
      "assetId": "asset_008",
      "concept": "asset",
      "position": [
        30.0,
        0.0,
        100.0
      ],
      "rotation": {
        "x": 0.0,
        "y": -1.57,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": -89.954,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "asset_009",
      "assetId": "asset_009",
      "concept": "asset",
      "position": [
        75.0,
        0.0,
        150.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 1.57,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 89.954,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "asset_010",
      "assetId": "asset_010",
      "concept": "asset",
      "position": [
        100.0,
        0.0,
        130.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 1.57,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 89.954,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "asset_011",
      "assetId": "asset_011",
      "concept": "asset",
      "position": [
        105.0,
        0.0,
        135.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 1.57,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 89.954,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "asset_012",
      "assetId": "asset_012",
      "concept": "asset",
      "position": [
        120.0,
        0.0,
        200.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 3.14,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 179.909,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "asset_013",
      "assetId": "asset_013",
      "concept": "asset",
      "position": [
        5.0,
        0.0,
        150.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "asset_014",
      "assetId": "asset_014",
      "concept": "asset",
      "position": [
        55.0,
        0.0,
        150.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "asset_014",
      "assetId": "asset_014",
      "concept": "asset",
      "position": [
        95.0,
        0.0,
        150.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    }
  ],
  "assets": {
    "asset_001": {
      "id": "asset_001",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "asset",
          "w": 1.0,
          "h": 1.0,
          "d": 1.0
        }
      ],
      "materials": {
        "asset": "default_grey"
      },
      "tags": [
        "asset",
        "asset_001"
      ],
      "bbox": [
        1.0,
        1.0,
        1.0
      ]
    },
    "asset_002": {
      "id": "asset_002",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "asset",
          "w": 1.0,
          "h": 1.0,
          "d": 1.0
        }
      ],
      "materials": {
        "asset": "default_grey"
      },
      "tags": [
        "asset",
        "asset_002"
      ],
      "bbox": [
        1.0,
        1.0,
        1.0
      ]
    },
    "asset_003": {
      "id": "asset_003",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "asset",
          "w": 1.0,
          "h": 1.0,
          "d": 1.0
        }
      ],
      "materials": {
        "asset": "default_grey"
      },
      "tags": [
        "asset",
        "asset_003"
      ],
      "bbox": [
        1.0,
        1.0,
        1.0
      ]
    },
    "asset_004": {
      "id": "asset_004",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "asset",
          "w": 1.0,
          "h": 1.0,
          "d": 1.0
        }
      ],
      "materials": {
        "asset": "default_grey"
      },
      "tags": [
        "asset",
        "asset_004"
      ],
      "bbox": [
        1.0,
        1.0,
        1.0
      ]
    },
    "asset_005": {
      "id": "asset_005",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "asset",
          "w": 1.0,
          "h": 1.0,
          "d": 1.0
        }
      ],
      "materials": {
        "asset": "default_grey"
      },
      "tags": [
        "asset",
        "asset_005"
      ],
      "bbox": [
        1.0,
        1.0,
        1.0
      ]
    },
    "asset_006": {
      "id": "asset_006",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "asset",
          "w": 1.0,
          "h": 1.0,
          "d": 1.0
        }
      ],
      "materials": {
        "asset": "default_grey"
      },
      "tags": [
        "asset",
        "asset_006"
      ],
      "bbox": [
        1.0,
        1.0,
        1.0
      ]
    },
    "asset_007": {
      "id": "asset_007",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "asset",
          "w": 1.0,
          "h": 1.0,
          "d": 1.0
        }
      ],
      "materials": {
        "asset": "default_grey"
      },
      "tags": [
        "asset",
        "asset_007"
      ],
      "bbox": [
        1.0,
        1.0,
        1.0
      ]
    },
    "asset_008": {
      "id": "asset_008",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "asset",
          "w": 1.0,
          "h": 1.0,
          "d": 1.0
        }
      ],
      "materials": {
        "asset": "default_grey"
      },
      "tags": [
        "asset",
        "asset_008"
      ],
      "bbox": [
        1.0,
        1.0,
        1.0
      ]
    },
    "asset_009": {
      "id": "asset_009",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "asset",
          "w": 1.0,
          "h": 1.0,
          "d": 1.0
        }
      ],
      "materials": {
        "asset": "default_grey"
      },
      "tags": [
        "asset",
        "asset_009"
      ],
      "bbox": [
        1.0,
        1.0,
        1.0
      ]
    },
    "asset_010": {
      "id": "asset_010",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "asset",
          "w": 1.0,
          "h": 1.0,
          "d": 1.0
        }
      ],
      "materials": {
        "asset": "default_grey"
      },
      "tags": [
        "asset",
        "asset_010"
      ],
      "bbox": [
        1.0,
        1.0,
        1.0
      ]
    },
    "asset_011": {
      "id": "asset_011",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "asset",
          "w": 1.0,
          "h": 1.0,
          "d": 1.0
        }
      ],
      "materials": {
        "asset": "default_grey"
      },
      "tags": [
        "asset",
        "asset_011"
      ],
      "bbox": [
        1.0,
        1.0,
        1.0
      ]
    },
    "asset_012": {
      "id": "asset_012",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "asset",
          "w": 1.0,
          "h": 1.0,
          "d": 1.0
        }
      ],
      "materials": {
        "asset": "default_grey"
      },
      "tags": [
        "asset",
        "asset_012"
      ],
      "bbox": [
        1.0,
        1.0,
        1.0
      ]
    },
    "asset_013": {
      "id": "asset_013",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "asset",
          "w": 1.0,
          "h": 1.0,
          "d": 1.0
        }
      ],
      "materials": {
        "asset": "default_grey"
      },
      "tags": [
        "asset",
        "asset_013"
      ],
      "bbox": [
        1.0,
        1.0,
        1.0
      ]
    },
    "asset_014": {
      "id": "asset_014",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "asset",
          "w": 1.0,
          "h": 1.0,
          "d": 1.0
        }
      ],
      "materials": {
        "asset": "default_grey"
      },
      "tags": [
        "asset",
        "asset_014"
      ],
      "bbox": [
        1.0,
        1.0,
        1.0
      ]
    }
  },
  "materialPalette": {
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
    "metal_grey": "#64748b"
  },
  "generatedAt": "2025-10-29T03:01:01.850149Z"
} as const;
const FALLBACK_COLORS = [
  "#f472b6",
  "#a855f7",
  "#38bdf8",
  "#14b8a6",
  "#34d399",
  "#f59e0b",
  "#f97316",
  "#ef4444"
] as const;

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
            aria-label={`scene-viewer-riverside_village_market_001`}
        />
    );
};

export default SceneCanvas;
import { useEffect, useRef } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";

const manifestData = {
  "scene_id": "pastoral_riverside_village_001",
  "prompt": "Design a pastoral riverside village with a market square",
  "requirements": {
    "requirements": [
      {
        "concept": "market_square",
        "min_count": 1
      },
      {
        "concept": "river",
        "min_count": 1
      },
      {
        "concept": "cottage",
        "min_count": 1
      },
      {
        "concept": "cottage",
        "min_count": 1
      },
      {
        "concept": "barn",
        "min_count": 1
      },
      {
        "concept": "silo",
        "min_count": 1
      },
      {
        "concept": "church",
        "min_count": 1
      },
      {
        "concept": "bridge",
        "min_count": 1
      },
      {
        "concept": "market_stall",
        "min_count": 1
      },
      {
        "concept": "market_stall",
        "min_count": 1
      },
      {
        "concept": "fountain",
        "min_count": 1
      },
      {
        "concept": "water_well",
        "min_count": 1
      },
      {
        "concept": "tree",
        "min_count": 1
      },
      {
        "concept": "tree",
        "min_count": 1
      },
      {
        "concept": "fence",
        "min_count": 1
      },
      {
        "concept": "wagon",
        "min_count": 1
      }
    ]
  },
  "scene_spec": {
    "theme": "pastoral riverside village",
    "setting": "European-inspired rural village",
    "scale": "small village (500-1000 residents)",
    "key_elements": [
      "meandering river with gentle banks",
      "cobblestone market square with fountain",
      "thatched cottages and stone buildings",
      "wooden market stalls",
      "agricultural structures (barn, silo)",
      "village church with bell tower",
      "stone bridge crossing river",
      "cobblestone streets and pathways",
      "mature trees and green spaces",
      "wooden fences and garden borders"
    ],
    "entities": [
      {
        "concept": "market_square",
        "count": 1,
        "attrs": {}
      },
      {
        "concept": "river",
        "count": 1,
        "attrs": {}
      },
      {
        "concept": "cottage",
        "count": 1,
        "attrs": {}
      },
      {
        "concept": "cottage",
        "count": 1,
        "attrs": {}
      },
      {
        "concept": "barn",
        "count": 1,
        "attrs": {}
      },
      {
        "concept": "silo",
        "count": 1,
        "attrs": {}
      },
      {
        "concept": "church",
        "count": 1,
        "attrs": {}
      },
      {
        "concept": "bridge",
        "count": 1,
        "attrs": {}
      },
      {
        "concept": "market_stall",
        "count": 1,
        "attrs": {}
      },
      {
        "concept": "market_stall",
        "count": 1,
        "attrs": {}
      },
      {
        "concept": "fountain",
        "count": 1,
        "attrs": {}
      },
      {
        "concept": "water_well",
        "count": 1,
        "attrs": {}
      },
      {
        "concept": "tree",
        "count": 1,
        "attrs": {}
      },
      {
        "concept": "tree",
        "count": 1,
        "attrs": {}
      },
      {
        "concept": "fence",
        "count": 1,
        "attrs": {}
      },
      {
        "concept": "wagon",
        "count": 1,
        "attrs": {}
      }
    ],
    "constraints": []
  },
  "assets": [
    {
      "id": "market_square_01",
      "glb_path": "/Users/plugyawn/bounties/roam_environments/backend/assets/market_square_01.glb",
      "bbox": [
        1.0,
        1.0,
        1.0
      ],
      "recipe": {
        "recipe": [
          {
            "primitive": "cuboid",
            "name": "market_square",
            "w": 1.0,
            "h": 1.0,
            "d": 1.0
          }
        ],
        "materials": {
          "market_square": "default_grey"
        },
        "id": "market_square_01",
        "tags": [
          "market_square",
          "market_square_01"
        ]
      }
    },
    {
      "id": "river_01",
      "glb_path": "/Users/plugyawn/bounties/roam_environments/backend/assets/river_01.glb",
      "bbox": [
        20.0,
        0.010000000000000009,
        200.0
      ],
      "recipe": {
        "recipe": [
          {
            "primitive": "plane",
            "name": "surface",
            "w": 20,
            "d": 200,
            "offset": [
              0,
              -0.2,
              0
            ]
          }
        ],
        "materials": {
          "surface": "water_blue"
        },
        "id": "river_01",
        "tags": [
          "river",
          "river_01"
        ]
      }
    },
    {
      "id": "cottage_01",
      "glb_path": "/Users/plugyawn/bounties/roam_environments/backend/assets/cottage_01.glb",
      "bbox": [
        1.0,
        1.0,
        1.0
      ],
      "recipe": {
        "recipe": [
          {
            "primitive": "cuboid",
            "name": "cottage",
            "w": 1.0,
            "h": 1.0,
            "d": 1.0
          }
        ],
        "materials": {
          "cottage": "default_grey"
        },
        "id": "cottage_01",
        "tags": [
          "cottage",
          "cottage_01"
        ]
      }
    },
    {
      "id": "cottage_02",
      "glb_path": "/Users/plugyawn/bounties/roam_environments/backend/assets/cottage_02.glb",
      "bbox": [
        1.0,
        1.0,
        1.0
      ],
      "recipe": {
        "recipe": [
          {
            "primitive": "cuboid",
            "name": "cottage",
            "w": 1.0,
            "h": 1.0,
            "d": 1.0
          }
        ],
        "materials": {
          "cottage": "default_grey"
        },
        "id": "cottage_02",
        "tags": [
          "cottage",
          "cottage_02"
        ]
      }
    },
    {
      "id": "barn_01",
      "glb_path": "/Users/plugyawn/bounties/roam_environments/backend/assets/barn_01.glb",
      "bbox": [
        1.0,
        1.0,
        1.0
      ],
      "recipe": {
        "recipe": [
          {
            "primitive": "cuboid",
            "name": "barn",
            "w": 1.0,
            "h": 1.0,
            "d": 1.0
          }
        ],
        "materials": {
          "barn": "default_grey"
        },
        "id": "barn_01",
        "tags": [
          "barn",
          "barn_01"
        ]
      }
    },
    {
      "id": "silo_01",
      "glb_path": "/Users/plugyawn/bounties/roam_environments/backend/assets/silo_01.glb",
      "bbox": [
        1.0,
        1.0,
        1.0
      ],
      "recipe": {
        "recipe": [
          {
            "primitive": "cuboid",
            "name": "silo",
            "w": 1.0,
            "h": 1.0,
            "d": 1.0
          }
        ],
        "materials": {
          "silo": "default_grey"
        },
        "id": "silo_01",
        "tags": [
          "silo",
          "silo_01"
        ]
      }
    },
    {
      "id": "church_01",
      "glb_path": "/Users/plugyawn/bounties/roam_environments/backend/assets/church_01.glb",
      "bbox": [
        1.0,
        1.0,
        1.0
      ],
      "recipe": {
        "recipe": [
          {
            "primitive": "cuboid",
            "name": "church",
            "w": 1.0,
            "h": 1.0,
            "d": 1.0
          }
        ],
        "materials": {
          "church": "default_grey"
        },
        "id": "church_01",
        "tags": [
          "church",
          "church_01"
        ]
      }
    },
    {
      "id": "bridge_01",
      "glb_path": "/Users/plugyawn/bounties/roam_environments/backend/assets/bridge_01.glb",
      "bbox": [
        1.0,
        1.0,
        1.0
      ],
      "recipe": {
        "recipe": [
          {
            "primitive": "cuboid",
            "name": "bridge",
            "w": 1.0,
            "h": 1.0,
            "d": 1.0
          }
        ],
        "materials": {
          "bridge": "default_grey"
        },
        "id": "bridge_01",
        "tags": [
          "bridge",
          "bridge_01"
        ]
      }
    },
    {
      "id": "market_stall_01",
      "glb_path": "/Users/plugyawn/bounties/roam_environments/backend/assets/market_stall_01.glb",
      "bbox": [
        1.0,
        1.0,
        1.0
      ],
      "recipe": {
        "recipe": [
          {
            "primitive": "cuboid",
            "name": "market_stall",
            "w": 1.0,
            "h": 1.0,
            "d": 1.0
          }
        ],
        "materials": {
          "market_stall": "default_grey"
        },
        "id": "market_stall_01",
        "tags": [
          "market_stall",
          "market_stall_01"
        ]
      }
    },
    {
      "id": "market_stall_02",
      "glb_path": "/Users/plugyawn/bounties/roam_environments/backend/assets/market_stall_02.glb",
      "bbox": [
        1.0,
        1.0,
        1.0
      ],
      "recipe": {
        "recipe": [
          {
            "primitive": "cuboid",
            "name": "market_stall",
            "w": 1.0,
            "h": 1.0,
            "d": 1.0
          }
        ],
        "materials": {
          "market_stall": "default_grey"
        },
        "id": "market_stall_02",
        "tags": [
          "market_stall",
          "market_stall_02"
        ]
      }
    },
    {
      "id": "fountain_01",
      "glb_path": "/Users/plugyawn/bounties/roam_environments/backend/assets/fountain_01.glb",
      "bbox": [
        1.0,
        1.0,
        1.0
      ],
      "recipe": {
        "recipe": [
          {
            "primitive": "cuboid",
            "name": "fountain",
            "w": 1.0,
            "h": 1.0,
            "d": 1.0
          }
        ],
        "materials": {
          "fountain": "default_grey"
        },
        "id": "fountain_01",
        "tags": [
          "fountain",
          "fountain_01"
        ]
      }
    },
    {
      "id": "water_well_01",
      "glb_path": "/Users/plugyawn/bounties/roam_environments/backend/assets/water_well_01.glb",
      "bbox": [
        1.0,
        1.0,
        1.0
      ],
      "recipe": {
        "recipe": [
          {
            "primitive": "cuboid",
            "name": "water_well",
            "w": 1.0,
            "h": 1.0,
            "d": 1.0
          }
        ],
        "materials": {
          "water_well": "default_grey"
        },
        "id": "water_well_01",
        "tags": [
          "water_well",
          "water_well_01"
        ]
      }
    },
    {
      "id": "tree_01",
      "glb_path": "/Users/plugyawn/bounties/roam_environments/backend/assets/tree_01.glb",
      "bbox": [
        5.0,
        7.4,
        5.0
      ],
      "recipe": {
        "recipe": [
          {
            "primitive": "cylinder",
            "name": "trunk",
            "r": 0.4,
            "h": 4.5
          },
          {
            "primitive": "sphere",
            "name": "crown",
            "r": 2.5,
            "offset": [
              0,
              4.5,
              0
            ]
          }
        ],
        "materials": {
          "trunk": "bark_brown",
          "crown": "leaf_green"
        },
        "id": "tree_01",
        "tags": [
          "tree",
          "tree_01"
        ]
      }
    },
    {
      "id": "tree_02",
      "glb_path": "/Users/plugyawn/bounties/roam_environments/backend/assets/tree_02.glb",
      "bbox": [
        5.0,
        7.4,
        5.0
      ],
      "recipe": {
        "recipe": [
          {
            "primitive": "cylinder",
            "name": "trunk",
            "r": 0.4,
            "h": 4.5
          },
          {
            "primitive": "sphere",
            "name": "crown",
            "r": 2.5,
            "offset": [
              0,
              4.5,
              0
            ]
          }
        ],
        "materials": {
          "trunk": "bark_brown",
          "crown": "leaf_green"
        },
        "id": "tree_02",
        "tags": [
          "tree",
          "tree_02"
        ]
      }
    },
    {
      "id": "fence_01",
      "glb_path": "/Users/plugyawn/bounties/roam_environments/backend/assets/fence_01.glb",
      "bbox": [
        1.0,
        1.0,
        1.0
      ],
      "recipe": {
        "recipe": [
          {
            "primitive": "cuboid",
            "name": "fence",
            "w": 1.0,
            "h": 1.0,
            "d": 1.0
          }
        ],
        "materials": {
          "fence": "default_grey"
        },
        "id": "fence_01",
        "tags": [
          "fence",
          "fence_01"
        ]
      }
    },
    {
      "id": "wagon_01",
      "glb_path": "/Users/plugyawn/bounties/roam_environments/backend/assets/wagon_01.glb",
      "bbox": [
        1.0,
        1.0,
        1.0
      ],
      "recipe": {
        "recipe": [
          {
            "primitive": "cuboid",
            "name": "wagon",
            "w": 1.0,
            "h": 1.0,
            "d": 1.0
          }
        ],
        "materials": {
          "wagon": "default_grey"
        },
        "id": "wagon_01",
        "tags": [
          "wagon",
          "wagon_01"
        ]
      }
    }
  ],
  "map_plan": {
    "name": "Riverside Village Map",
    "dimensions": {
      "width": 120,
      "length": 180,
      "height": 30
    },
    "zones": [
      {
        "name": "market_square",
        "type": "commercial",
        "position": [
          60,
          0,
          90
        ],
        "size": [
          40,
          0,
          40
        ],
        "description": "Central cobblestone market square with fountain"
      },
      {
        "name": "residential_area",
        "type": "residential",
        "position": [
          30,
          0,
          50
        ],
        "size": [
          50,
          0,
          70
        ],
        "description": "Cluster of residential cottages with gardens"
      },
      {
        "name": "agricultural_zone",
        "type": "agricultural",
        "position": [
          90,
          0,
          40
        ],
        "size": [
          30,
          0,
          60
        ],
        "description": "Farm buildings and storage structures"
      },
      {
        "name": "river_front",
        "type": "natural",
        "position": [
          0,
          0,
          90
        ],
        "size": [
          20,
          0,
          180
        ],
        "description": "Riverbank area with willow trees"
      },
      {
        "name": "village_center",
        "type": "landmark",
        "position": [
          75,
          0,
          130
        ],
        "size": [
          25,
          0,
          30
        ],
        "description": "Village church and central gathering area"
      }
    ]
  },
  "scene_graph": {
    "map": {
      "name": "Riverside Village Map",
      "dimensions": {
        "width": 120,
        "length": 180,
        "height": 30
      },
      "zones": [
        {
          "name": "market_square",
          "type": "commercial",
          "position": [
            60,
            0,
            90
          ],
          "size": [
            40,
            0,
            40
          ],
          "description": "Central cobblestone market square with fountain"
        },
        {
          "name": "residential_area",
          "type": "residential",
          "position": [
            30,
            0,
            50
          ],
          "size": [
            50,
            0,
            70
          ],
          "description": "Cluster of residential cottages with gardens"
        },
        {
          "name": "agricultural_zone",
          "type": "agricultural",
          "position": [
            90,
            0,
            40
          ],
          "size": [
            30,
            0,
            60
          ],
          "description": "Farm buildings and storage structures"
        },
        {
          "name": "river_front",
          "type": "natural",
          "position": [
            0,
            0,
            90
          ],
          "size": [
            20,
            0,
            180
          ],
          "description": "Riverbank area with willow trees"
        },
        {
          "name": "village_center",
          "type": "landmark",
          "position": [
            75,
            0,
            130
          ],
          "size": [
            25,
            0,
            30
          ],
          "description": "Village church and central gathering area"
        }
      ]
    },
    "placements": [
      {
        "asset_id": "market_square_01",
        "pos": [
          60,
          0,
          90
        ],
        "rotY": 0,
        "description": "Central market square",
        "ref": "market_square_01"
      },
      {
        "asset_id": "river_01",
        "pos": [
          10,
          0,
          90
        ],
        "rotY": 0,
        "description": "Main river flowing through village",
        "ref": "river_01"
      },
      {
        "asset_id": "cottage_01",
        "pos": [
          25,
          0,
          45
        ],
        "rotY": 0,
        "description": "Residential cottage near village entrance",
        "ref": "cottage_01"
      },
      {
        "asset_id": "cottage_02",
        "pos": [
          35,
          0,
          55
        ],
        "rotY": 1.57,
        "description": "Larger residential cottage with garden",
        "ref": "cottage_02"
      },
      {
        "asset_id": "cottage_01",
        "pos": [
          15,
          0,
          65
        ],
        "rotY": 3.14,
        "description": "Additional residential cottage",
        "ref": "cottage_01"
      },
      {
        "asset_id": "cottage_02",
        "pos": [
          45,
          0,
          35
        ],
        "rotY": 4.71,
        "description": "Corner residential cottage",
        "ref": "cottage_02"
      },
      {
        "asset_id": "barn_01",
        "pos": [
          95,
          0,
          45
        ],
        "rotY": 0,
        "description": "Main agricultural barn",
        "ref": "barn_01"
      },
      {
        "asset_id": "silo_01",
        "pos": [
          105,
          0,
          55
        ],
        "rotY": 0,
        "description": "Grain storage silo",
        "ref": "silo_01"
      },
      {
        "asset_id": "church_01",
        "pos": [
          75,
          0,
          135
        ],
        "rotY": 0,
        "description": "Village church with bell tower",
        "ref": "church_01"
      },
      {
        "asset_id": "bridge_01",
        "pos": [
          55,
          5,
          85
        ],
        "rotY": 1.57,
        "description": "Stone bridge crossing river",
        "ref": "bridge_01"
      },
      {
        "asset_id": "market_stall_01",
        "pos": [
          50,
          0,
          85
        ],
        "rotY": 0,
        "description": "Vegetable market stall",
        "ref": "market_stall_01"
      },
      {
        "asset_id": "market_stall_02",
        "pos": [
          70,
          0,
          85
        ],
        "rotY": 0,
        "description": "Bakery market stall",
        "ref": "market_stall_02"
      },
      {
        "asset_id": "market_stall_01",
        "pos": [
          60,
          0,
          100
        ],
        "rotY": 1.57,
        "description": "Additional market stall",
        "ref": "market_stall_01"
      },
      {
        "asset_id": "fountain_01",
        "pos": [
          60,
          0,
          90
        ],
        "rotY": 0,
        "description": "Central market square fountain",
        "ref": "fountain_01"
      },
      {
        "asset_id": "water_well_01",
        "pos": [
          40,
          0,
          95
        ],
        "rotY": 0,
        "description": "Village water well near market",
        "ref": "water_well_01"
      },
      {
        "asset_id": "tree_01",
        "pos": [
          20,
          0,
          40
        ],
        "rotY": 0,
        "description": "Mature oak tree in residential area",
        "ref": "tree_01"
      },
      {
        "asset_id": "tree_02",
        "pos": [
          15,
          0,
          90
        ],
        "rotY": 0,
        "description": "Willow tree along riverbank",
        "ref": "tree_02"
      },
      {
        "asset_id": "tree_01",
        "pos": [
          65,
          0,
          75
        ],
        "rotY": 0,
        "description": "Shade tree near market",
        "ref": "tree_01"
      },
      {
        "asset_id": "fence_01",
        "pos": [
          30,
          0,
          50
        ],
        "rotY": 0,
        "description": "Garden fence around cottage",
        "ref": "fence_01"
      },
      {
        "asset_id": "wagon_01",
        "pos": [
          52,
          0,
          88
        ],
        "rotY": 0.78,
        "description": "Market wagon near stalls",
        "ref": "wagon_01"
      }
    ],
    "scene_id": "pastoral_riverside_village_001",
    "assets": [
      "market_square_01",
      "river_01",
      "cottage_01",
      "cottage_02",
      "barn_01",
      "silo_01",
      "church_01",
      "bridge_01",
      "market_stall_01",
      "market_stall_02",
      "fountain_01",
      "water_well_01",
      "tree_01",
      "tree_02",
      "fence_01",
      "wagon_01"
    ]
  },
  "validation": {
    "status": "pass",
    "issues": [],
    "metrics": {
      "concept_counts": {
        "market_square": 1,
        "river": 1,
        "cottage": 4,
        "barn": 1,
        "silo": 1,
        "church": 1,
        "bridge": 1,
        "market_stall": 3,
        "fountain": 1,
        "water_well": 1,
        "tree": 3,
        "fence": 1,
        "wagon": 1
      }
    }
  }
} as const;

type Placement = {
    id: string;
    position: [number, number, number];
    scale: [number, number, number];
    rotY: number;
};

const buildPlacements = (): Placement[] => {
    const placements = Array.isArray(manifestData?.scene_graph?.placements)
        ? manifestData.scene_graph.placements
        : [];

    return placements
        .map((placement: any) => {
            const pos = placement.pos || placement.position || (placement.transform && placement.transform.pos);
            if (!Array.isArray(pos) || pos.length < 3) {
                return null;
            }
            const scale = placement.scale || (placement.transform && placement.transform.scale) || [1, 1, 1];
            const rot = placement.rotY ?? (placement.rotation && placement.rotation.y) ?? (placement.transform && placement.transform.rot && placement.transform.rot[1]) ?? 0;
            const id = placement.ref || placement.asset_id || placement.asset || placement.id || "unknown";
            const normalizedScale = Array.isArray(scale)
                ? (scale.slice(0, 3).map((value: any) => Number(value)) as [number, number, number])
                : ([Number(scale) || 1, Number(scale) || 1, Number(scale) || 1] as [number, number, number]);

            return {
                id,
                position: pos.slice(0, 3).map((value: any) => Number(value)) as [number, number, number],
                scale: normalizedScale,
                rotY: Number(rot) || 0,
            };
        })
        .filter(Boolean) as Placement[];
};

const SceneCanvas = () => {
    const containerRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        const container = containerRef.current;
        if (!container) {
            return;
        }

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.shadowMap.enabled = true;
        container.appendChild(renderer.domElement);

        const scene = new THREE.Scene();
        scene.background = new THREE.Color("#a8bbd4");

        const camera = new THREE.PerspectiveCamera(
            48,
            container.clientWidth / container.clientHeight,
            0.1,
            2000
        );
        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.08;

        const ambient = new THREE.AmbientLight(0xffffff, 0.65);
        scene.add(ambient);
        const directional = new THREE.DirectionalLight(0xffffff, 0.8);
        directional.position.set(250, 400, 180);
        directional.castShadow = true;
        scene.add(directional);

        const grid = new THREE.GridHelper(600, 24, 0x223344, 0x556677);
        grid.position.y = 0;
        scene.add(grid);

        const placements = buildPlacements();
        const colorCache = new Map<string, number>();
        const palette = [0xd97093, 0x4169e1, 0x2e8b57, 0xc79343, 0x8a36bf, 0xcd5c5c, 0x4682b4, 0x8fbc8f, 0xd2b48c, 0x6495ed];

        placements.forEach((entry) => {
            let color = colorCache.get(entry.id);
            if (!color) {
                color = palette[colorCache.size % palette.length];
                colorCache.set(entry.id, color);
            }

            const geometry = new THREE.BoxGeometry(
                entry.scale[0] || 4,
                entry.scale[1] || 6,
                entry.scale[2] || 4
            );
            const material = new THREE.MeshStandardMaterial({
                color,
                metalness: 0.05,
                roughness: 0.65,
            });
            const mesh = new THREE.Mesh(geometry, material);
            mesh.position.set(entry.position[0], (entry.scale[1] || 6) * 0.5, entry.position[2]);
            mesh.rotation.y = THREE.MathUtils.degToRad(entry.rotY);
            mesh.castShadow = true;
            scene.add(mesh);

            const canvasLabel = document.createElement("canvas");
            canvasLabel.width = 256;
            canvasLabel.height = 128;
            const ctx = canvasLabel.getContext("2d");
            if (ctx) {
                ctx.fillStyle = "rgba(15, 23, 42, 0.85)";
                ctx.fillRect(0, 0, 256, 128);
                ctx.fillStyle = "#f8fafc";
                ctx.font = "24px sans-serif";
                ctx.fillText(entry.id, 12, 72);
                const texture = new THREE.CanvasTexture(canvasLabel);
                const labelMaterial = new THREE.SpriteMaterial({ map: texture, depthTest: false });
                const sprite = new THREE.Sprite(labelMaterial);
                sprite.position.set(entry.position[0], (entry.scale[1] || 6) + 4, entry.position[2]);
                sprite.scale.set(20, 10, 1);
                scene.add(sprite);
            }
        });

        const positions = placements.map((entry) => entry.position);
        const center = positions.reduce<[number, number, number]>((acc, pos) => {
            return [acc[0] + pos[0], acc[1] + pos[1], acc[2] + pos[2]];
        }, [0, 0, 0]);
        if (positions.length) {
            center[0] /= positions.length;
            center[1] /= positions.length;
            center[2] /= positions.length;
        }

        const radius = positions.reduce((max, pos) => {
            const dx = pos[0] - center[0];
            const dz = pos[2] - center[2];
            return Math.max(max, Math.sqrt(dx * dx + dz * dz));
        }, 60);

        camera.position.set(center[0] + radius * 1.4, center[1] + radius * 1.1 + 80, center[2] + radius * 1.4);
        controls.target.set(center[0], center[1], center[2]);

        const handleResize = () => {
            const { clientWidth, clientHeight } = container;
            renderer.setSize(clientWidth, clientHeight);
            camera.aspect = clientWidth / Math.max(clientHeight, 1);
            camera.updateProjectionMatrix();
        };

        window.addEventListener("resize", handleResize);
        handleResize();

        let animationId = 0;
        const animate = () => {
            animationId = window.requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        };

        animate();

        return () => {
            window.cancelAnimationFrame(animationId);
            window.removeEventListener("resize", handleResize);
            controls.dispose();
            renderer.dispose();
            scene.traverse((child: any) => {
                if (child.isMesh) {
                    child.geometry.dispose();
                    if (Array.isArray(child.material)) {
                        child.material.forEach((material: any) => material.dispose?.());
                    } else {
                        child.material.dispose?.();
                    }
                }
            });
            if (renderer.domElement.parentElement === container) {
                container.removeChild(renderer.domElement);
            }
        };
    }, []);

    return (
        <div
            ref={containerRef}
            style={{ width: "100%", height: "100%", position: "relative", background: "#0f172a" }}
            aria-label="scene-viewer-pastoral_riverside_village_001"
        />
    );
};

export default SceneCanvas;
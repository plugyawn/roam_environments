import { useEffect, useRef } from "react";
import * as THREE from "three";

const VIEW_MODEL = {
  "sceneId": "riverside_village_001",
  "prompt": "Design a pastoral riverside village with a market square",
  "placements": [
    {
      "ref": "res_001",
      "assetId": "res_001",
      "concept": "res",
      "position": [
        25.0,
        0.0,
        35.0
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
      "ref": "res_002",
      "assetId": "res_002",
      "concept": "res",
      "position": [
        35.0,
        0.0,
        32.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 0.785398,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 45.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "res_003",
      "assetId": "res_003",
      "concept": "res",
      "position": [
        42.0,
        0.0,
        40.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 1.570796,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 90.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "res_004",
      "assetId": "res_004",
      "concept": "res",
      "position": [
        30.0,
        0.0,
        45.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 3.141593,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 180.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "res_005",
      "assetId": "res_005",
      "concept": "res",
      "position": [
        20.0,
        0.0,
        42.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 4.712389,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 270.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "res_006",
      "assetId": "res_006",
      "concept": "res",
      "position": [
        15.0,
        0.0,
        30.0
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
      "ref": "res_007",
      "assetId": "res_007",
      "concept": "res",
      "position": [
        18.0,
        0.0,
        25.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 0.785398,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 45.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "res_008",
      "assetId": "res_008",
      "concept": "res",
      "position": [
        28.0,
        0.0,
        22.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 1.570796,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 90.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "shop_001",
      "assetId": "shop_001",
      "concept": "shop",
      "position": [
        55.0,
        0.0,
        55.0
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
      "ref": "shop_002",
      "assetId": "shop_002",
      "concept": "shop",
      "position": [
        65.0,
        0.0,
        55.0
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
      "ref": "shop_003",
      "assetId": "shop_003",
      "concept": "shop",
      "position": [
        55.0,
        0.0,
        65.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 3.141593,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 180.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "shop_004",
      "assetId": "shop_004",
      "concept": "shop",
      "position": [
        65.0,
        0.0,
        65.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 3.141593,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 180.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "shop_005",
      "assetId": "shop_005",
      "concept": "shop",
      "position": [
        50.0,
        0.0,
        60.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 4.712389,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 270.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "shop_006",
      "assetId": "shop_006",
      "concept": "shop",
      "position": [
        70.0,
        0.0,
        60.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 1.570796,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 90.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "town_hall_001",
      "assetId": "town_hall_001",
      "concept": "town_hall",
      "position": [
        35.0,
        0.0,
        75.0
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
      "ref": "church_001",
      "assetId": "church_001",
      "concept": "church",
      "position": [
        25.0,
        0.0,
        65.0
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
      "ref": "inn_001",
      "assetId": "inn_001",
      "concept": "inn",
      "position": [
        45.0,
        0.0,
        70.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 1.570796,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 90.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "mill_001",
      "assetId": "mill_001",
      "concept": "mill",
      "position": [
        95.0,
        0.0,
        25.0
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
      "ref": "bridge_001",
      "assetId": "bridge_001",
      "concept": "bridge",
      "position": [
        90.0,
        0.0,
        20.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 1.570796,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 90.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "dock_001",
      "assetId": "dock_001",
      "concept": "dock",
      "position": [
        85.0,
        0.0,
        18.0
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
      "ref": "path_001",
      "assetId": "path_001",
      "concept": "path",
      "position": [
        30.0,
        0.0,
        30.0
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
      "ref": "path_002",
      "assetId": "path_002",
      "concept": "path",
      "position": [
        40.0,
        0.0,
        35.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 0.785398,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 45.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "path_003",
      "assetId": "path_003",
      "concept": "path",
      "position": [
        50.0,
        0.0,
        40.0
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
      "ref": "path_004",
      "assetId": "path_004",
      "concept": "path",
      "position": [
        60.0,
        0.0,
        45.0
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
      "ref": "path_005",
      "assetId": "path_005",
      "concept": "path",
      "position": [
        70.0,
        0.0,
        50.0
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
      "ref": "path_006",
      "assetId": "path_006",
      "concept": "path",
      "position": [
        60.0,
        0.0,
        55.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 1.570796,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 90.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "path_007",
      "assetId": "path_007",
      "concept": "path",
      "position": [
        60.0,
        0.0,
        65.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 1.570796,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 90.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "path_008",
      "assetId": "path_008",
      "concept": "path",
      "position": [
        55.0,
        0.0,
        70.0
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
      "ref": "path_009",
      "assetId": "path_009",
      "concept": "path",
      "position": [
        45.0,
        0.0,
        70.0
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
      "ref": "path_010",
      "assetId": "path_010",
      "concept": "path",
      "position": [
        35.0,
        0.0,
        70.0
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
      "ref": "path_011",
      "assetId": "path_011",
      "concept": "path",
      "position": [
        25.0,
        0.0,
        60.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 1.570796,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 90.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "path_012",
      "assetId": "path_012",
      "concept": "path",
      "position": [
        25.0,
        0.0,
        50.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 1.570796,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 90.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "tree_001",
      "assetId": "tree_001",
      "concept": "tree",
      "position": [
        60.0,
        0.0,
        50.0
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
      "ref": "tree_002",
      "assetId": "tree_002",
      "concept": "tree",
      "position": [
        70.0,
        0.0,
        45.0
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
      "ref": "tree_003",
      "assetId": "tree_003",
      "concept": "tree",
      "position": [
        50.0,
        0.0,
        45.0
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
      "ref": "tree_004",
      "assetId": "tree_004",
      "concept": "tree",
      "position": [
        60.0,
        0.0,
        35.0
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
      "ref": "tree_005",
      "assetId": "tree_005",
      "concept": "tree",
      "position": [
        15.0,
        0.0,
        45.0
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
      "ref": "tree_006",
      "assetId": "tree_006",
      "concept": "tree",
      "position": [
        35.0,
        0.0,
        15.0
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
      "ref": "tree_007",
      "assetId": "tree_007",
      "concept": "tree",
      "position": [
        10.0,
        0.0,
        25.0
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
      "ref": "tree_008",
      "assetId": "tree_008",
      "concept": "tree",
      "position": [
        15.0,
        0.0,
        25.0
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
      "ref": "tree_009",
      "assetId": "tree_009",
      "concept": "tree",
      "position": [
        10.0,
        0.0,
        30.0
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
      "ref": "tree_010",
      "assetId": "tree_010",
      "concept": "tree",
      "position": [
        15.0,
        0.0,
        30.0
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
      "ref": "flowers_001",
      "assetId": "flowers_001",
      "concept": "flowers",
      "position": [
        28.0,
        0.0,
        32.0
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
      "ref": "flowers_002",
      "assetId": "flowers_002",
      "concept": "flowers",
      "position": [
        38.0,
        0.0,
        35.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 0.785398,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 45.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "flowers_003",
      "assetId": "flowers_003",
      "concept": "flowers",
      "position": [
        45.0,
        0.0,
        42.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 1.570796,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 90.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "flowers_004",
      "assetId": "flowers_004",
      "concept": "flowers",
      "position": [
        25.0,
        0.0,
        48.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 3.141593,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 180.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "flowers_005",
      "assetId": "flowers_005",
      "concept": "flowers",
      "position": [
        18.0,
        0.0,
        45.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 4.712389,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 270.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "flowers_006",
      "assetId": "flowers_006",
      "concept": "flowers",
      "position": [
        12.0,
        0.0,
        32.0
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
      "ref": "flowers_007",
      "assetId": "flowers_007",
      "concept": "flowers",
      "position": [
        20.0,
        0.0,
        25.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 0.785398,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 45.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "flowers_008",
      "assetId": "flowers_008",
      "concept": "flowers",
      "position": [
        32.0,
        0.0,
        20.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 1.570796,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 90.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "stall_001",
      "assetId": "stall_001",
      "concept": "stall",
      "position": [
        52.0,
        0.0,
        52.0
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
      "ref": "stall_002",
      "assetId": "stall_002",
      "concept": "stall",
      "position": [
        58.0,
        0.0,
        52.0
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
      "ref": "stall_003",
      "assetId": "stall_003",
      "concept": "stall",
      "position": [
        64.0,
        0.0,
        52.0
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
      "ref": "stall_004",
      "assetId": "stall_004",
      "concept": "stall",
      "position": [
        68.0,
        0.0,
        58.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 1.570796,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 90.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "stall_005",
      "assetId": "stall_005",
      "concept": "stall",
      "position": [
        68.0,
        0.0,
        64.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 1.570796,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 90.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "stall_006",
      "assetId": "stall_006",
      "concept": "stall",
      "position": [
        64.0,
        0.0,
        68.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 3.141593,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 180.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "stall_007",
      "assetId": "stall_007",
      "concept": "stall",
      "position": [
        58.0,
        0.0,
        68.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 3.141593,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 180.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "stall_008",
      "assetId": "stall_008",
      "concept": "stall",
      "position": [
        52.0,
        0.0,
        68.0
      ],
      "rotation": {
        "x": 0.0,
        "y": 3.141593,
        "z": 0.0
      },
      "rotationDegrees": {
        "x": 0.0,
        "y": 180.0,
        "z": 0.0
      },
      "scale": [
        1.0,
        1.0,
        1.0
      ]
    },
    {
      "ref": "fountain_001",
      "assetId": "fountain_001",
      "concept": "fountain",
      "position": [
        60.0,
        0.0,
        60.0
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
    "res_001": {
      "id": "res_001",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "body",
          "w": 8.0,
          "h": 5.0,
          "d": 6.0
        },
        {
          "primitive": "pyramid",
          "name": "roof",
          "w": 8.4,
          "h": 3.0,
          "d": 6.4,
          "offset": [
            0,
            5.0,
            0
          ]
        },
        {
          "primitive": "cuboid",
          "name": "chimney",
          "w": 1.0,
          "h": 2.0,
          "d": 1.0,
          "offset": [
            -2.5,
            5.5,
            1.5
          ]
        }
      ],
      "materials": {
        "body": "plaster_white",
        "roof": "terracotta_red",
        "chimney": "brick_red"
      },
      "tags": [
        "res",
        "res_001"
      ],
      "bbox": [
        8.4,
        10.5,
        6.4
      ]
    },
    "res_002": {
      "id": "res_002",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "body",
          "w": 8.0,
          "h": 5.0,
          "d": 6.0
        },
        {
          "primitive": "pyramid",
          "name": "roof",
          "w": 8.4,
          "h": 3.0,
          "d": 6.4,
          "offset": [
            0,
            5.0,
            0
          ]
        },
        {
          "primitive": "cuboid",
          "name": "chimney",
          "w": 1.0,
          "h": 2.0,
          "d": 1.0,
          "offset": [
            -2.5,
            5.5,
            1.5
          ]
        }
      ],
      "materials": {
        "body": "plaster_white",
        "roof": "terracotta_red",
        "chimney": "brick_red"
      },
      "tags": [
        "res",
        "res_002"
      ],
      "bbox": [
        8.4,
        10.5,
        6.4
      ]
    },
    "res_003": {
      "id": "res_003",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "body",
          "w": 8.0,
          "h": 5.0,
          "d": 6.0
        },
        {
          "primitive": "pyramid",
          "name": "roof",
          "w": 8.4,
          "h": 3.0,
          "d": 6.4,
          "offset": [
            0,
            5.0,
            0
          ]
        },
        {
          "primitive": "cuboid",
          "name": "chimney",
          "w": 1.0,
          "h": 2.0,
          "d": 1.0,
          "offset": [
            -2.5,
            5.5,
            1.5
          ]
        }
      ],
      "materials": {
        "body": "plaster_white",
        "roof": "terracotta_red",
        "chimney": "brick_red"
      },
      "tags": [
        "res",
        "res_003"
      ],
      "bbox": [
        8.4,
        10.5,
        6.4
      ]
    },
    "res_004": {
      "id": "res_004",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "body",
          "w": 8.0,
          "h": 5.0,
          "d": 6.0
        },
        {
          "primitive": "pyramid",
          "name": "roof",
          "w": 8.4,
          "h": 3.0,
          "d": 6.4,
          "offset": [
            0,
            5.0,
            0
          ]
        },
        {
          "primitive": "cuboid",
          "name": "chimney",
          "w": 1.0,
          "h": 2.0,
          "d": 1.0,
          "offset": [
            -2.5,
            5.5,
            1.5
          ]
        }
      ],
      "materials": {
        "body": "plaster_white",
        "roof": "terracotta_red",
        "chimney": "brick_red"
      },
      "tags": [
        "res",
        "res_004"
      ],
      "bbox": [
        8.4,
        10.5,
        6.4
      ]
    },
    "res_005": {
      "id": "res_005",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "body",
          "w": 8.0,
          "h": 5.0,
          "d": 6.0
        },
        {
          "primitive": "pyramid",
          "name": "roof",
          "w": 8.4,
          "h": 3.0,
          "d": 6.4,
          "offset": [
            0,
            5.0,
            0
          ]
        },
        {
          "primitive": "cuboid",
          "name": "chimney",
          "w": 1.0,
          "h": 2.0,
          "d": 1.0,
          "offset": [
            -2.5,
            5.5,
            1.5
          ]
        }
      ],
      "materials": {
        "body": "plaster_white",
        "roof": "terracotta_red",
        "chimney": "brick_red"
      },
      "tags": [
        "res",
        "res_005"
      ],
      "bbox": [
        8.4,
        10.5,
        6.4
      ]
    },
    "res_006": {
      "id": "res_006",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "body",
          "w": 8.0,
          "h": 5.0,
          "d": 6.0
        },
        {
          "primitive": "pyramid",
          "name": "roof",
          "w": 8.4,
          "h": 3.0,
          "d": 6.4,
          "offset": [
            0,
            5.0,
            0
          ]
        },
        {
          "primitive": "cuboid",
          "name": "chimney",
          "w": 1.0,
          "h": 2.0,
          "d": 1.0,
          "offset": [
            -2.5,
            5.5,
            1.5
          ]
        }
      ],
      "materials": {
        "body": "plaster_white",
        "roof": "terracotta_red",
        "chimney": "brick_red"
      },
      "tags": [
        "res",
        "res_006"
      ],
      "bbox": [
        8.4,
        10.5,
        6.4
      ]
    },
    "res_007": {
      "id": "res_007",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "body",
          "w": 8.0,
          "h": 5.0,
          "d": 6.0
        },
        {
          "primitive": "pyramid",
          "name": "roof",
          "w": 8.4,
          "h": 3.0,
          "d": 6.4,
          "offset": [
            0,
            5.0,
            0
          ]
        },
        {
          "primitive": "cuboid",
          "name": "chimney",
          "w": 1.0,
          "h": 2.0,
          "d": 1.0,
          "offset": [
            -2.5,
            5.5,
            1.5
          ]
        }
      ],
      "materials": {
        "body": "plaster_white",
        "roof": "terracotta_red",
        "chimney": "brick_red"
      },
      "tags": [
        "res",
        "res_007"
      ],
      "bbox": [
        8.4,
        10.5,
        6.4
      ]
    },
    "res_008": {
      "id": "res_008",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "body",
          "w": 8.0,
          "h": 5.0,
          "d": 6.0
        },
        {
          "primitive": "pyramid",
          "name": "roof",
          "w": 8.4,
          "h": 3.0,
          "d": 6.4,
          "offset": [
            0,
            5.0,
            0
          ]
        },
        {
          "primitive": "cuboid",
          "name": "chimney",
          "w": 1.0,
          "h": 2.0,
          "d": 1.0,
          "offset": [
            -2.5,
            5.5,
            1.5
          ]
        }
      ],
      "materials": {
        "body": "plaster_white",
        "roof": "terracotta_red",
        "chimney": "brick_red"
      },
      "tags": [
        "res",
        "res_008"
      ],
      "bbox": [
        8.4,
        10.5,
        6.4
      ]
    },
    "shop_001": {
      "id": "shop_001",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "counter",
          "w": 3.0,
          "h": 0.9,
          "d": 2.0
        },
        {
          "primitive": "pyramid",
          "name": "canopy",
          "w": 3.2,
          "h": 1.2,
          "d": 2.2,
          "offset": [
            0,
            1.8,
            0
          ]
        }
      ],
      "materials": {
        "counter": "wood_oak",
        "canopy": "canvas_striped"
      },
      "tags": [
        "shop",
        "shop_001"
      ],
      "bbox": [
        3.2,
        3.45,
        2.2
      ]
    },
    "shop_002": {
      "id": "shop_002",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "counter",
          "w": 3.0,
          "h": 0.9,
          "d": 2.0
        },
        {
          "primitive": "pyramid",
          "name": "canopy",
          "w": 3.2,
          "h": 1.2,
          "d": 2.2,
          "offset": [
            0,
            1.8,
            0
          ]
        }
      ],
      "materials": {
        "counter": "wood_oak",
        "canopy": "canvas_striped"
      },
      "tags": [
        "shop",
        "shop_002"
      ],
      "bbox": [
        3.2,
        3.45,
        2.2
      ]
    },
    "shop_003": {
      "id": "shop_003",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "counter",
          "w": 3.0,
          "h": 0.9,
          "d": 2.0
        },
        {
          "primitive": "pyramid",
          "name": "canopy",
          "w": 3.2,
          "h": 1.2,
          "d": 2.2,
          "offset": [
            0,
            1.8,
            0
          ]
        }
      ],
      "materials": {
        "counter": "wood_oak",
        "canopy": "canvas_striped"
      },
      "tags": [
        "shop",
        "shop_003"
      ],
      "bbox": [
        3.2,
        3.45,
        2.2
      ]
    },
    "shop_004": {
      "id": "shop_004",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "counter",
          "w": 3.0,
          "h": 0.9,
          "d": 2.0
        },
        {
          "primitive": "pyramid",
          "name": "canopy",
          "w": 3.2,
          "h": 1.2,
          "d": 2.2,
          "offset": [
            0,
            1.8,
            0
          ]
        }
      ],
      "materials": {
        "counter": "wood_oak",
        "canopy": "canvas_striped"
      },
      "tags": [
        "shop",
        "shop_004"
      ],
      "bbox": [
        3.2,
        3.45,
        2.2
      ]
    },
    "shop_005": {
      "id": "shop_005",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "counter",
          "w": 3.0,
          "h": 0.9,
          "d": 2.0
        },
        {
          "primitive": "pyramid",
          "name": "canopy",
          "w": 3.2,
          "h": 1.2,
          "d": 2.2,
          "offset": [
            0,
            1.8,
            0
          ]
        }
      ],
      "materials": {
        "counter": "wood_oak",
        "canopy": "canvas_striped"
      },
      "tags": [
        "shop",
        "shop_005"
      ],
      "bbox": [
        3.2,
        3.45,
        2.2
      ]
    },
    "shop_006": {
      "id": "shop_006",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "counter",
          "w": 3.0,
          "h": 0.9,
          "d": 2.0
        },
        {
          "primitive": "pyramid",
          "name": "canopy",
          "w": 3.2,
          "h": 1.2,
          "d": 2.2,
          "offset": [
            0,
            1.8,
            0
          ]
        }
      ],
      "materials": {
        "counter": "wood_oak",
        "canopy": "canvas_striped"
      },
      "tags": [
        "shop",
        "shop_006"
      ],
      "bbox": [
        3.2,
        3.45,
        2.2
      ]
    },
    "town_hall_001": {
      "id": "town_hall_001",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "body",
          "w": 14,
          "h": 7,
          "d": 10
        },
        {
          "primitive": "pyramid",
          "name": "roof",
          "w": 14.4,
          "h": 3.5,
          "d": 10.4,
          "offset": [
            0,
            7,
            0
          ]
        },
        {
          "primitive": "cuboid",
          "name": "tower",
          "w": 3,
          "h": 10,
          "d": 3,
          "offset": [
            0,
            8,
            0
          ]
        }
      ],
      "materials": {
        "body": "stone_grey",
        "roof": "slate_dark",
        "tower": "stone_grey"
      },
      "tags": [
        "town_hall",
        "town_hall_001"
      ],
      "bbox": [
        14.4,
        16.5,
        10.4
      ]
    },
    "church_001": {
      "id": "church_001",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "nave",
          "w": 12,
          "h": 8,
          "d": 22
        },
        {
          "primitive": "pyramid",
          "name": "roof",
          "w": 12.8,
          "h": 4.0,
          "d": 22.8,
          "offset": [
            0,
            8,
            0
          ]
        },
        {
          "primitive": "cuboid",
          "name": "tower",
          "w": 4,
          "h": 14,
          "d": 4,
          "offset": [
            -6,
            7,
            6
          ]
        },
        {
          "primitive": "pyramid",
          "name": "spire",
          "w": 4.6,
          "h": 4.5,
          "d": 4.6,
          "offset": [
            -6,
            14,
            6
          ]
        }
      ],
      "materials": {
        "nave": "stone_light",
        "roof": "slate_dark",
        "tower": "stone_light",
        "spire": "copper_green"
      },
      "tags": [
        "church",
        "church_001"
      ],
      "bbox": [
        14.700000000000001,
        22.5,
        22.8
      ]
    },
    "inn_001": {
      "id": "inn_001",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "body",
          "w": 12,
          "h": 5.5,
          "d": 7
        },
        {
          "primitive": "pyramid",
          "name": "roof",
          "w": 12.4,
          "h": 3.0,
          "d": 7.4,
          "offset": [
            0,
            5.5,
            0
          ]
        },
        {
          "primitive": "cuboid",
          "name": "sign",
          "w": 0.4,
          "h": 1.4,
          "d": 2.4,
          "offset": [
            6.4,
            3.0,
            0
          ]
        }
      ],
      "materials": {
        "body": "timber_frame",
        "roof": "thatch_warm",
        "sign": "wood_dark"
      },
      "tags": [
        "inn",
        "inn_001"
      ],
      "bbox": [
        12.8,
        11.25,
        7.4
      ]
    },
    "mill_001": {
      "id": "mill_001",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "body",
          "w": 10,
          "h": 6,
          "d": 7
        },
        {
          "primitive": "pyramid",
          "name": "roof",
          "w": 10.4,
          "h": 3.2,
          "d": 7.4,
          "offset": [
            0,
            6,
            0
          ]
        },
        {
          "primitive": "cylinder",
          "name": "wheel",
          "r": 2.5,
          "h": 0.6,
          "offset": [
            5.3,
            1.5,
            0
          ]
        }
      ],
      "materials": {
        "body": "stone_grey",
        "roof": "wood_shingle",
        "wheel": "wood_dark"
      },
      "tags": [
        "mill",
        "mill_001"
      ],
      "bbox": [
        13.0,
        12.2,
        7.4
      ]
    },
    "bridge_001": {
      "id": "bridge_001",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "deck",
          "w": 14,
          "h": 0.6,
          "d": 4,
          "offset": [
            0,
            -0.3,
            0
          ]
        },
        {
          "primitive": "cuboid",
          "name": "rail_left",
          "w": 14,
          "h": 1.1,
          "d": 0.25,
          "offset": [
            0,
            0.55,
            -1.9
          ]
        },
        {
          "primitive": "cuboid",
          "name": "rail_right",
          "w": 14,
          "h": 1.1,
          "d": 0.25,
          "offset": [
            0,
            0.55,
            1.9
          ]
        }
      ],
      "materials": {
        "deck": "wood_oak",
        "rail_left": "wood_oak",
        "rail_right": "wood_oak"
      },
      "tags": [
        "bridge",
        "bridge_001"
      ],
      "bbox": [
        14.0,
        1.7000000000000002,
        4.05
      ]
    },
    "dock_001": {
      "id": "dock_001",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "platform",
          "w": 18,
          "h": 0.4,
          "d": 3.5,
          "offset": [
            0,
            -0.2,
            0
          ]
        },
        {
          "primitive": "cuboid",
          "name": "posts",
          "w": 18,
          "h": 1.0,
          "d": 0.2,
          "offset": [
            0,
            0.5,
            -1.6
          ]
        }
      ],
      "materials": {
        "platform": "wood_weathered",
        "posts": "wood_dark"
      },
      "tags": [
        "dock",
        "dock_001"
      ],
      "bbox": [
        18.0,
        1.4,
        3.5
      ]
    },
    "path_001": {
      "id": "path_001",
      "recipe": [
        {
          "primitive": "plane",
          "name": "path",
          "w": 2.5,
          "d": 12,
          "offset": [
            0,
            -0.05,
            0
          ]
        }
      ],
      "materials": {
        "path": "packed_earth"
      },
      "tags": [
        "path",
        "path_001"
      ],
      "bbox": [
        2.5,
        0.009999999999999995,
        12.0
      ]
    },
    "path_002": {
      "id": "path_002",
      "recipe": [
        {
          "primitive": "plane",
          "name": "path",
          "w": 2.5,
          "d": 12,
          "offset": [
            0,
            -0.05,
            0
          ]
        }
      ],
      "materials": {
        "path": "packed_earth"
      },
      "tags": [
        "path",
        "path_002"
      ],
      "bbox": [
        2.5,
        0.009999999999999995,
        12.0
      ]
    },
    "path_003": {
      "id": "path_003",
      "recipe": [
        {
          "primitive": "plane",
          "name": "path",
          "w": 2.5,
          "d": 12,
          "offset": [
            0,
            -0.05,
            0
          ]
        }
      ],
      "materials": {
        "path": "packed_earth"
      },
      "tags": [
        "path",
        "path_003"
      ],
      "bbox": [
        2.5,
        0.009999999999999995,
        12.0
      ]
    },
    "path_004": {
      "id": "path_004",
      "recipe": [
        {
          "primitive": "plane",
          "name": "path",
          "w": 2.5,
          "d": 12,
          "offset": [
            0,
            -0.05,
            0
          ]
        }
      ],
      "materials": {
        "path": "packed_earth"
      },
      "tags": [
        "path",
        "path_004"
      ],
      "bbox": [
        2.5,
        0.009999999999999995,
        12.0
      ]
    },
    "path_005": {
      "id": "path_005",
      "recipe": [
        {
          "primitive": "plane",
          "name": "path",
          "w": 2.5,
          "d": 12,
          "offset": [
            0,
            -0.05,
            0
          ]
        }
      ],
      "materials": {
        "path": "packed_earth"
      },
      "tags": [
        "path",
        "path_005"
      ],
      "bbox": [
        2.5,
        0.009999999999999995,
        12.0
      ]
    },
    "path_006": {
      "id": "path_006",
      "recipe": [
        {
          "primitive": "plane",
          "name": "path",
          "w": 2.5,
          "d": 12,
          "offset": [
            0,
            -0.05,
            0
          ]
        }
      ],
      "materials": {
        "path": "packed_earth"
      },
      "tags": [
        "path",
        "path_006"
      ],
      "bbox": [
        2.5,
        0.009999999999999995,
        12.0
      ]
    },
    "path_007": {
      "id": "path_007",
      "recipe": [
        {
          "primitive": "plane",
          "name": "path",
          "w": 2.5,
          "d": 12,
          "offset": [
            0,
            -0.05,
            0
          ]
        }
      ],
      "materials": {
        "path": "packed_earth"
      },
      "tags": [
        "path",
        "path_007"
      ],
      "bbox": [
        2.5,
        0.009999999999999995,
        12.0
      ]
    },
    "path_008": {
      "id": "path_008",
      "recipe": [
        {
          "primitive": "plane",
          "name": "path",
          "w": 2.5,
          "d": 12,
          "offset": [
            0,
            -0.05,
            0
          ]
        }
      ],
      "materials": {
        "path": "packed_earth"
      },
      "tags": [
        "path",
        "path_008"
      ],
      "bbox": [
        2.5,
        0.009999999999999995,
        12.0
      ]
    },
    "path_009": {
      "id": "path_009",
      "recipe": [
        {
          "primitive": "plane",
          "name": "path",
          "w": 2.5,
          "d": 12,
          "offset": [
            0,
            -0.05,
            0
          ]
        }
      ],
      "materials": {
        "path": "packed_earth"
      },
      "tags": [
        "path",
        "path_009"
      ],
      "bbox": [
        2.5,
        0.009999999999999995,
        12.0
      ]
    },
    "path_010": {
      "id": "path_010",
      "recipe": [
        {
          "primitive": "plane",
          "name": "path",
          "w": 2.5,
          "d": 12,
          "offset": [
            0,
            -0.05,
            0
          ]
        }
      ],
      "materials": {
        "path": "packed_earth"
      },
      "tags": [
        "path",
        "path_010"
      ],
      "bbox": [
        2.5,
        0.009999999999999995,
        12.0
      ]
    },
    "path_011": {
      "id": "path_011",
      "recipe": [
        {
          "primitive": "plane",
          "name": "path",
          "w": 2.5,
          "d": 12,
          "offset": [
            0,
            -0.05,
            0
          ]
        }
      ],
      "materials": {
        "path": "packed_earth"
      },
      "tags": [
        "path",
        "path_011"
      ],
      "bbox": [
        2.5,
        0.009999999999999995,
        12.0
      ]
    },
    "path_012": {
      "id": "path_012",
      "recipe": [
        {
          "primitive": "plane",
          "name": "path",
          "w": 2.5,
          "d": 12,
          "offset": [
            0,
            -0.05,
            0
          ]
        }
      ],
      "materials": {
        "path": "packed_earth"
      },
      "tags": [
        "path",
        "path_012"
      ],
      "bbox": [
        2.5,
        0.009999999999999995,
        12.0
      ]
    },
    "tree_001": {
      "id": "tree_001",
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
      "tags": [
        "tree",
        "tree_001"
      ],
      "bbox": [
        5.0,
        7.4,
        5.0
      ]
    },
    "tree_002": {
      "id": "tree_002",
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
      "tags": [
        "tree",
        "tree_002"
      ],
      "bbox": [
        5.0,
        7.4,
        5.0
      ]
    },
    "tree_003": {
      "id": "tree_003",
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
      "tags": [
        "tree",
        "tree_003"
      ],
      "bbox": [
        5.0,
        7.4,
        5.0
      ]
    },
    "tree_004": {
      "id": "tree_004",
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
      "tags": [
        "tree",
        "tree_004"
      ],
      "bbox": [
        5.0,
        7.4,
        5.0
      ]
    },
    "tree_005": {
      "id": "tree_005",
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
      "tags": [
        "tree",
        "tree_005"
      ],
      "bbox": [
        5.0,
        7.4,
        5.0
      ]
    },
    "tree_006": {
      "id": "tree_006",
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
      "tags": [
        "tree",
        "tree_006"
      ],
      "bbox": [
        5.0,
        7.4,
        5.0
      ]
    },
    "tree_007": {
      "id": "tree_007",
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
      "tags": [
        "tree",
        "tree_007"
      ],
      "bbox": [
        5.0,
        7.4,
        5.0
      ]
    },
    "tree_008": {
      "id": "tree_008",
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
      "tags": [
        "tree",
        "tree_008"
      ],
      "bbox": [
        5.0,
        7.4,
        5.0
      ]
    },
    "tree_009": {
      "id": "tree_009",
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
      "tags": [
        "tree",
        "tree_009"
      ],
      "bbox": [
        5.0,
        7.4,
        5.0
      ]
    },
    "tree_010": {
      "id": "tree_010",
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
      "tags": [
        "tree",
        "tree_010"
      ],
      "bbox": [
        5.0,
        7.4,
        5.0
      ]
    },
    "flowers_001": {
      "id": "flowers_001",
      "recipe": [
        {
          "primitive": "cylinder",
          "name": "bed",
          "r": 1.2,
          "h": 0.4
        },
        {
          "primitive": "sphere",
          "name": "blooms",
          "r": 1.0,
          "offset": [
            0,
            0.8,
            0
          ]
        }
      ],
      "materials": {
        "bed": "soil_dark",
        "blooms": "flower_mix"
      },
      "tags": [
        "flowers",
        "flowers_001"
      ],
      "bbox": [
        2.4,
        3.0,
        2.0
      ]
    },
    "flowers_002": {
      "id": "flowers_002",
      "recipe": [
        {
          "primitive": "cylinder",
          "name": "bed",
          "r": 1.2,
          "h": 0.4
        },
        {
          "primitive": "sphere",
          "name": "blooms",
          "r": 1.0,
          "offset": [
            0,
            0.8,
            0
          ]
        }
      ],
      "materials": {
        "bed": "soil_dark",
        "blooms": "flower_mix"
      },
      "tags": [
        "flowers",
        "flowers_002"
      ],
      "bbox": [
        2.4,
        3.0,
        2.0
      ]
    },
    "flowers_003": {
      "id": "flowers_003",
      "recipe": [
        {
          "primitive": "cylinder",
          "name": "bed",
          "r": 1.2,
          "h": 0.4
        },
        {
          "primitive": "sphere",
          "name": "blooms",
          "r": 1.0,
          "offset": [
            0,
            0.8,
            0
          ]
        }
      ],
      "materials": {
        "bed": "soil_dark",
        "blooms": "flower_mix"
      },
      "tags": [
        "flowers",
        "flowers_003"
      ],
      "bbox": [
        2.4,
        3.0,
        2.0
      ]
    },
    "flowers_004": {
      "id": "flowers_004",
      "recipe": [
        {
          "primitive": "cylinder",
          "name": "bed",
          "r": 1.2,
          "h": 0.4
        },
        {
          "primitive": "sphere",
          "name": "blooms",
          "r": 1.0,
          "offset": [
            0,
            0.8,
            0
          ]
        }
      ],
      "materials": {
        "bed": "soil_dark",
        "blooms": "flower_mix"
      },
      "tags": [
        "flowers",
        "flowers_004"
      ],
      "bbox": [
        2.4,
        3.0,
        2.0
      ]
    },
    "flowers_005": {
      "id": "flowers_005",
      "recipe": [
        {
          "primitive": "cylinder",
          "name": "bed",
          "r": 1.2,
          "h": 0.4
        },
        {
          "primitive": "sphere",
          "name": "blooms",
          "r": 1.0,
          "offset": [
            0,
            0.8,
            0
          ]
        }
      ],
      "materials": {
        "bed": "soil_dark",
        "blooms": "flower_mix"
      },
      "tags": [
        "flowers",
        "flowers_005"
      ],
      "bbox": [
        2.4,
        3.0,
        2.0
      ]
    },
    "flowers_006": {
      "id": "flowers_006",
      "recipe": [
        {
          "primitive": "cylinder",
          "name": "bed",
          "r": 1.2,
          "h": 0.4
        },
        {
          "primitive": "sphere",
          "name": "blooms",
          "r": 1.0,
          "offset": [
            0,
            0.8,
            0
          ]
        }
      ],
      "materials": {
        "bed": "soil_dark",
        "blooms": "flower_mix"
      },
      "tags": [
        "flowers",
        "flowers_006"
      ],
      "bbox": [
        2.4,
        3.0,
        2.0
      ]
    },
    "flowers_007": {
      "id": "flowers_007",
      "recipe": [
        {
          "primitive": "cylinder",
          "name": "bed",
          "r": 1.2,
          "h": 0.4
        },
        {
          "primitive": "sphere",
          "name": "blooms",
          "r": 1.0,
          "offset": [
            0,
            0.8,
            0
          ]
        }
      ],
      "materials": {
        "bed": "soil_dark",
        "blooms": "flower_mix"
      },
      "tags": [
        "flowers",
        "flowers_007"
      ],
      "bbox": [
        2.4,
        3.0,
        2.0
      ]
    },
    "flowers_008": {
      "id": "flowers_008",
      "recipe": [
        {
          "primitive": "cylinder",
          "name": "bed",
          "r": 1.2,
          "h": 0.4
        },
        {
          "primitive": "sphere",
          "name": "blooms",
          "r": 1.0,
          "offset": [
            0,
            0.8,
            0
          ]
        }
      ],
      "materials": {
        "bed": "soil_dark",
        "blooms": "flower_mix"
      },
      "tags": [
        "flowers",
        "flowers_008"
      ],
      "bbox": [
        2.4,
        3.0,
        2.0
      ]
    },
    "stall_001": {
      "id": "stall_001",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "counter",
          "w": 3.0,
          "h": 0.9,
          "d": 2.0
        },
        {
          "primitive": "pyramid",
          "name": "canopy",
          "w": 3.2,
          "h": 1.2,
          "d": 2.2,
          "offset": [
            0,
            1.8,
            0
          ]
        }
      ],
      "materials": {
        "counter": "wood_oak",
        "canopy": "canvas_striped"
      },
      "tags": [
        "stall",
        "stall_001"
      ],
      "bbox": [
        3.2,
        3.45,
        2.2
      ]
    },
    "stall_002": {
      "id": "stall_002",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "counter",
          "w": 3.0,
          "h": 0.9,
          "d": 2.0
        },
        {
          "primitive": "pyramid",
          "name": "canopy",
          "w": 3.2,
          "h": 1.2,
          "d": 2.2,
          "offset": [
            0,
            1.8,
            0
          ]
        }
      ],
      "materials": {
        "counter": "wood_oak",
        "canopy": "canvas_striped"
      },
      "tags": [
        "stall",
        "stall_002"
      ],
      "bbox": [
        3.2,
        3.45,
        2.2
      ]
    },
    "stall_003": {
      "id": "stall_003",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "counter",
          "w": 3.0,
          "h": 0.9,
          "d": 2.0
        },
        {
          "primitive": "pyramid",
          "name": "canopy",
          "w": 3.2,
          "h": 1.2,
          "d": 2.2,
          "offset": [
            0,
            1.8,
            0
          ]
        }
      ],
      "materials": {
        "counter": "wood_oak",
        "canopy": "canvas_striped"
      },
      "tags": [
        "stall",
        "stall_003"
      ],
      "bbox": [
        3.2,
        3.45,
        2.2
      ]
    },
    "stall_004": {
      "id": "stall_004",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "counter",
          "w": 3.0,
          "h": 0.9,
          "d": 2.0
        },
        {
          "primitive": "pyramid",
          "name": "canopy",
          "w": 3.2,
          "h": 1.2,
          "d": 2.2,
          "offset": [
            0,
            1.8,
            0
          ]
        }
      ],
      "materials": {
        "counter": "wood_oak",
        "canopy": "canvas_striped"
      },
      "tags": [
        "stall",
        "stall_004"
      ],
      "bbox": [
        3.2,
        3.45,
        2.2
      ]
    },
    "stall_005": {
      "id": "stall_005",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "counter",
          "w": 3.0,
          "h": 0.9,
          "d": 2.0
        },
        {
          "primitive": "pyramid",
          "name": "canopy",
          "w": 3.2,
          "h": 1.2,
          "d": 2.2,
          "offset": [
            0,
            1.8,
            0
          ]
        }
      ],
      "materials": {
        "counter": "wood_oak",
        "canopy": "canvas_striped"
      },
      "tags": [
        "stall",
        "stall_005"
      ],
      "bbox": [
        3.2,
        3.45,
        2.2
      ]
    },
    "stall_006": {
      "id": "stall_006",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "counter",
          "w": 3.0,
          "h": 0.9,
          "d": 2.0
        },
        {
          "primitive": "pyramid",
          "name": "canopy",
          "w": 3.2,
          "h": 1.2,
          "d": 2.2,
          "offset": [
            0,
            1.8,
            0
          ]
        }
      ],
      "materials": {
        "counter": "wood_oak",
        "canopy": "canvas_striped"
      },
      "tags": [
        "stall",
        "stall_006"
      ],
      "bbox": [
        3.2,
        3.45,
        2.2
      ]
    },
    "stall_007": {
      "id": "stall_007",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "counter",
          "w": 3.0,
          "h": 0.9,
          "d": 2.0
        },
        {
          "primitive": "pyramid",
          "name": "canopy",
          "w": 3.2,
          "h": 1.2,
          "d": 2.2,
          "offset": [
            0,
            1.8,
            0
          ]
        }
      ],
      "materials": {
        "counter": "wood_oak",
        "canopy": "canvas_striped"
      },
      "tags": [
        "stall",
        "stall_007"
      ],
      "bbox": [
        3.2,
        3.45,
        2.2
      ]
    },
    "stall_008": {
      "id": "stall_008",
      "recipe": [
        {
          "primitive": "cuboid",
          "name": "counter",
          "w": 3.0,
          "h": 0.9,
          "d": 2.0
        },
        {
          "primitive": "pyramid",
          "name": "canopy",
          "w": 3.2,
          "h": 1.2,
          "d": 2.2,
          "offset": [
            0,
            1.8,
            0
          ]
        }
      ],
      "materials": {
        "counter": "wood_oak",
        "canopy": "canvas_striped"
      },
      "tags": [
        "stall",
        "stall_008"
      ],
      "bbox": [
        3.2,
        3.45,
        2.2
      ]
    },
    "fountain_001": {
      "id": "fountain_001",
      "recipe": [
        {
          "primitive": "cylinder",
          "name": "base",
          "r": 1.5,
          "h": 0.8
        },
        {
          "primitive": "cylinder",
          "name": "column",
          "r": 0.4,
          "h": 1.6,
          "offset": [
            0,
            0.8,
            0
          ]
        },
        {
          "primitive": "sphere",
          "name": "top",
          "r": 0.5,
          "offset": [
            0,
            2.0,
            0
          ]
        }
      ],
      "materials": {
        "base": "stone_light",
        "column": "stone_light",
        "top": "copper_green"
      },
      "tags": [
        "fountain",
        "fountain_001"
      ],
      "bbox": [
        3.0,
        4.0,
        1.6
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
    "metal_grey": "#64748b",
    "wood_oak": "#ef4444",
    "canvas_striped": "#f97316",
    "stone_grey": "#a855f7",
    "slate_dark": "#ef4444",
    "stone_light": "#f59e0b",
    "timber_frame": "#f472b6",
    "thatch_warm": "#14b8a6",
    "wood_dark": "#ef4444",
    "wood_shingle": "#f59e0b",
    "wood_weathered": "#ef4444",
    "packed_earth": "#f59e0b",
    "soil_dark": "#34d399",
    "flower_mix": "#a855f7"
  },
  "generatedAt": "2025-10-29T03:02:12.212136Z"
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
            aria-label={`scene-viewer-riverside_village_001`}
        />
    );
};

export default SceneCanvas;
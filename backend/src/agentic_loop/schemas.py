"""JSON Schema definitions used for structured outputs and tool contracts."""

from __future__ import annotations

SceneSpecV1 = {
    "type": "object",
    "additionalProperties": False,
    "required": ["entities", "constraints"],
    "properties": {
        "entities": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["concept", "count"],
                "properties": {
                    "concept": {"type": "string", "minLength": 1},
                    "count": {"type": "integer", "minimum": 1},
                    "attrs": {"type": "object", "additionalProperties": True},
                },
            },
        },
        "constraints": {
            "type": "array",
            "items": {"type": "object", "additionalProperties": True},
        },
    },
}

AssetRecipe = {
    "type": "object",
    "additionalProperties": False,
    "required": ["id", "tags", "recipe"],
    "properties": {
        "id": {"type": "string", "minLength": 1},
        "tags": {"type": "array", "items": {"type": "string"}},
        "recipe": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["primitive"],
                "properties": {
                    "primitive": {
                        "type": "string",
                        "enum": ["cuboid", "cylinder", "sphere", "pyramid", "plane"],
                    },
                    "name": {"type": "string"},
                    "w": {"type": "number"},
                    "h": {"type": "number"},
                    "d": {"type": "number"},
                    "r": {"type": "number"},
                    "offset": {
                        "type": "array",
                        "items": {"type": "number"},
                        "minItems": 3,
                        "maxItems": 3,
                    },
                    "material": {"type": "string"},
                },
            },
        },
        "materials": {"type": "object", "additionalProperties": {"type": "string"}},
        "bbox": {
            "type": "array",
            "items": {"type": "number"},
            "minItems": 3,
            "maxItems": 3,
        },
    },
}

MapPlan = {
    "type": "object",
    "additionalProperties": False,
    "required": ["size", "regions"],
    "properties": {
        "size": {
            "type": "object",
            "required": ["w", "h", "units"],
            "additionalProperties": False,
            "properties": {
                "w": {"type": "number", "minimum": 1},
                "h": {"type": "number", "minimum": 1},
                "units": {"type": "string"},
            },
        },
        "terrain": {"type": "object", "additionalProperties": True},
        "regions": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "label", "polygon"],
                "additionalProperties": False,
                "properties": {
                    "id": {"type": "string"},
                    "label": {"type": "string"},
                    "polygon": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {"type": "number"},
                            "minItems": 2,
                            "maxItems": 2,
                        },
                        "minItems": 3,
                    },
                },
            },
        },
    },
}

SceneGraph = {
    "type": "object",
    "additionalProperties": False,
    "required": ["assets", "placements"],
    "properties": {
        "scene_id": {"type": "string"},
        "assets": {"type": "array", "items": {"type": "string"}},
        "placements": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["ref", "transform"],
                "properties": {
                    "ref": {"type": "string"},
                    "transform": {
                        "type": "object",
                        "required": ["pos", "rotY", "scale"],
                        "additionalProperties": False,
                        "properties": {
                            "pos": {
                                "type": "array",
                                "items": {"type": "number"},
                                "minItems": 3,
                                "maxItems": 3,
                            },
                            "rotY": {"type": "number"},
                            "scale": {"type": "number"},
                        },
                    },
                },
            },
        },
        "map": {"type": "object", "additionalProperties": True},
    },
}

ValidationReport = {
    "type": "object",
    "additionalProperties": False,
    "required": ["status", "issues"],
    "properties": {
        "status": {"type": "string", "enum": ["pass", "fail"]},
        "issues": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["severity", "message"],
                "additionalProperties": False,
                "properties": {
                    "severity": {"type": "string", "enum": ["info", "warn", "error"]},
                    "message": {"type": "string"},
                    "context": {"type": "object", "additionalProperties": True},
                },
            },
        },
        "metrics": {"type": "object", "additionalProperties": True},
    },
}

RequirementsLedger = {
    "type": "object",
    "additionalProperties": False,
    "required": ["requirements"],
    "properties": {
        "requirements": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["concept"],
                "properties": {
                    "concept": {"type": "string"},
                    "min_count": {"type": "integer", "minimum": 0},
                    "max_count": {"type": "integer", "minimum": 0},
                    "exactly": {"type": "integer", "minimum": 0},
                    "must_cross_map": {"type": "boolean"},
                },
                "additionalProperties": True,
            },
        }
    },
}

__all__ = [
    "SceneSpecV1",
    "AssetRecipe",
    "MapPlan",
    "SceneGraph",
    "ValidationReport",
    "RequirementsLedger",
]

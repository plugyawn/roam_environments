"""Validation tool for scene graphs."""

from __future__ import annotations

from collections import Counter
from typing import Dict, List

from .assets import infer_concept_from_id


def validate_scene(scene_graph: Dict, requirements: Dict) -> Dict:
    """Check requirement coverage and return a validation report."""

    issues: List[Dict] = []
    placements = scene_graph.get("placements", [])
    counts = Counter()
    for entry in placements:
        if not isinstance(entry, dict):
            continue
        ref = entry.get("ref")
        if not ref:
            for key in ("asset_id", "asset", "id"):
                candidate = entry.get(key)
                if isinstance(candidate, str) and candidate.strip():
                    ref = candidate.strip()
                    break
        if not ref:
            continue
        concept = infer_concept_from_id(ref)
        counts[concept] += 1

    for req in requirements.get("requirements", []):
        concept = req.get("concept")
        if not concept:
            continue
        concept_key = concept.lower()
        actual = counts.get(concept_key, 0)
        min_count = req.get("exactly") or req.get("min_count") or 0
        if actual < min_count:
            issues.append(
                {
                    "severity": "error",
                    "message": f"Missing {concept}: expected at least {min_count}, found {actual}",
                    "context": {"concept": concept, "expected": min_count, "actual": actual},
                }
            )

    status = "pass" if not issues else "fail"
    return {
        "status": status,
        "issues": issues,
        "metrics": {"concept_counts": counts},
    }

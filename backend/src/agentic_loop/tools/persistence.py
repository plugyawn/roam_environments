"""Persistence tool for run manifests."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict


def persist_run(state: Dict) -> Dict:
    """Write the run manifest to disk and return metadata."""

    root = _run_root()
    root.mkdir(parents=True, exist_ok=True)

    prepared: Dict = dict(state or {})

    prepared.pop("scene_id", None)

    metadata = prepared.get("metadata")
    if not isinstance(metadata, dict):
        metadata = {}

    run_id = metadata.get("run_id")
    if not isinstance(run_id, str) or not run_id.strip():
        run_id = datetime.utcnow().strftime("run_%Y%m%d_%H%M%S")
    else:
        run_id = run_id.strip()

    metadata["run_id"] = run_id
    prepared["metadata"] = metadata

    run_filename = run_id.replace(os.sep, "_")
    if os.altsep:
        run_filename = run_filename.replace(os.altsep, "_")
    path = root / f"{run_filename}.json"
    metadata["manifest_path"] = str(path)

    path.write_text(json.dumps(prepared, indent=2))
    return {"run_id": run_id, "manifest_path": str(path)}


def _run_root() -> Path:
    return Path(os.environ.get("RUN_OUTPUT_DIR", "runs"))

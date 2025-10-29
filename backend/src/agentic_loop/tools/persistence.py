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
    run_id = state.get("scene_id") or datetime.utcnow().strftime("run_%Y%m%d_%H%M%S")
    path = root / f"{run_id}.json"
    path.write_text(json.dumps(state, indent=2))
    return {"run_id": run_id, "manifest_path": str(path)}


def _run_root() -> Path:
    return Path(os.environ.get("RUN_OUTPUT_DIR", "runs"))

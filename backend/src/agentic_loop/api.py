"""Minimal FastAPI application exposing scene manifests and assets."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from .config import RuntimeConfig

CONFIG = RuntimeConfig()
CONFIG.ensure_directories()

os.environ.setdefault("ASSET_ROOT", str(CONFIG.paths.asset_root))
os.environ.setdefault("RUN_OUTPUT_DIR", str(CONFIG.paths.run_root))
os.environ.setdefault("SNAPSHOT_ROOT", str(CONFIG.paths.snapshot_root))

app = FastAPI(title="Roam Environments Agentic Loop API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _latest_manifest() -> Optional[Path]:
    manifests = sorted(CONFIG.paths.run_root.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    return manifests[0] if manifests else None


def _manifest_by_run(run_id: str) -> Optional[Path]:
    candidate = CONFIG.paths.run_root / f"{run_id}.json"
    if candidate.exists():
        return candidate
    return None


@app.get("/runs/latest")
def get_latest_run() -> dict:
    """Return the most recent persisted scene manifest."""

    manifest_path = _latest_manifest()
    if manifest_path is None:
        return Response(status_code=204)
    return json.loads(manifest_path.read_text())


@app.get("/runs/{run_id}")
def get_run(run_id: str) -> dict:
    """Return a persisted scene manifest by run identifier."""

    manifest_path = _manifest_by_run(run_id)
    if manifest_path is None:
        raise HTTPException(status_code=404, detail="Run manifest not found")
    return json.loads(manifest_path.read_text())

@app.get("/snapshots/{run_id}")
def get_snapshot(run_id: str) -> FileResponse:
    """Serve a rendered snapshot image for a run."""

    path = CONFIG.paths.snapshot_root / f"{run_id}.png"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Snapshot not found")
    return FileResponse(path)


@app.get("/assets/{asset_id}.manifest")
def get_asset_manifest(asset_id: str) -> dict:
    """Return the compiled asset manifest JSON for a given asset id."""

    path = CONFIG.paths.asset_root / f"{asset_id}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Asset manifest not found")
    return json.loads(path.read_text())


@app.get("/assets/{asset_id}.glb")
def get_asset_glb(asset_id: str) -> FileResponse:
    """Serve the compiled binary glTF for a given asset id."""

    path = CONFIG.paths.asset_root / f"{asset_id}.glb"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Asset binary not found")
    return FileResponse(path, media_type="model/gltf-binary")

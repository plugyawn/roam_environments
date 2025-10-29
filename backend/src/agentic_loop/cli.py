"""Command-line entry point for the agentic loop."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
from typing import Dict

from .config import RuntimeConfig
from .orchestrator.workflow import run_prompt


def _load_keys() -> None:
    """Populate environment variables from backend/keys.json if present."""

    backend_root = Path(__file__).resolve().parents[2]
    keys_path = backend_root / "keys.json"
    if not keys_path.exists():
        return

    try:
        data: Dict[str, str] = json.loads(keys_path.read_text())
    except json.JSONDecodeError:
        return

    mapping = {
        "cerebras": "CEREBRAS_API_KEY",
        "google": "GOOGLE_API_KEY",
    }

    for source_key, env_var in mapping.items():
        if env_var not in os.environ and source_key in data and isinstance(data[source_key], str):
            os.environ[env_var] = data[source_key]


async def _amain(prompt: str, use_faiss: bool | None) -> None:
    _load_keys()
    config = RuntimeConfig()
    if use_faiss is not None:
        config.vector_store.use_faiss = use_faiss
    result = await run_prompt(prompt, config)
    print(json.dumps({
        "scene_id": result.get("scene_id"),
        "manifest_path": result.get("manifest_path"),
        "snapshot_path": result.get("snapshot_path"),
        "assets": len(result.get("assets", [])),
    }, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Agentic loop orchestrator")
    parser.add_argument("prompt", help="Scene prompt, e.g. 'Make a village'")
    parser.add_argument(
        "--disable-faiss",
        action="store_true",
        help="Skip FAISS indexing and rely on simple metadata search",
    )
    args = parser.parse_args()
    faiss_override = False if args.disable_faiss else None
    asyncio.run(_amain(args.prompt, use_faiss=faiss_override))


if __name__ == "__main__":
    main()

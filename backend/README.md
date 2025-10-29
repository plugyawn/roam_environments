# Agentic Loop Backend

Agentic orchestrator that connects Microsoft Magentic-One (AutoGen) with the Cerebras Inference API running the Qwen3-Coder-480B model. The service plans, validates, and produces editable village/world scenes rendered through the front-end viewer.

## Features

- Orchestrator powered by Magentic-One (`autogen-agentchat`) with structured tool calling.
- Cerebras Inference API client (OpenAI-compatible) targeting `qwen-3-coder-480b`.
- Scene memory and retrieval using FAISS + SQLite metadata, designed for long-context efficiency.
- Geometry synthesis pipeline converting primitive recipes to glTF via `trimesh` and `pygltflib`.
- Map generation and placement utilities (`shapely`, `opensimplex`) with collision-aware placement.
- Validation loop ensuring requirements coverage, spatial constraints, and patch-based deltas.

## Project Layout

```
backend/
  pyproject.toml
  requirements.txt
  README.md
  src/
    agentic_loop/
      __init__.py
      config.py
      schemas.py
      tools/
      memory/
      orchestrator/
      geometry/
      validation/
      persistence/
      cli.py
```

## Getting Started

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set environment variables in `.env` (create from the template below):

```
CEREBRAS_API_KEY=your_key
CEREBRAS_BASE_URL=https://api.cerebras.ai/v1
RUN_OUTPUT_DIR=../runs
```

Run the CLI prototype:

```bash
python -m agentic_loop.cli "Make a village"
```

## Development Utilities

```bash
pip install -e .[dev]
ruff check src
mypy src
pytest
```

## Next Steps

- Flesh out tool implementations (geometry generation, map sampling, validation).
- Hook the backend REST API (FastAPI) for the front-end viewer to consume manifests and snapshots.
- Add Dockerized geometry runner for sandboxed mesh exports.


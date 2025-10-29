"""High-level orchestration workflow."""

from __future__ import annotations

import ast
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import BaseAgentEvent, BaseChatMessage, TextMessage
from autogen_core.models import FunctionExecutionResult, FunctionExecutionResultMessage
from autogen_core.utils import extract_json_from_str

from ..config import RuntimeConfig
from ..memory import Embedder, RunRegistry, VectorStore
from ..memory.doc_sharder import shard_scene_graph
from ..tools.assets import compile_asset, expand_assets, infer_concept_from_id
from ..tools.map_gen import generate_map
from ..tools.persistence import persist_run
from ..tools.render import render_snapshot, render_web_view
from ..tools.scene_spec import design_scene_spec
from ..tools.validation import validate_scene
from .team import AUTOGEN_AVAILABLE, build_team

LOGGER = logging.getLogger(__name__)

MAX_AGENT_ATTEMPTS = 3


async def run_prompt(prompt: str, config: RuntimeConfig) -> Dict:
    """Execute the agentic loop for a given prompt."""

    if not AUTOGEN_AVAILABLE:
        raise RuntimeError("autogen-agentchat is not installed; Magentic-One is required for placement")

    config.ensure_directories()
    _apply_env_overrides(config)

    agent_handler, raw_log_path = _attach_agent_logger(config)
    run_data: Dict = {}
    last_error: str | None = None

    try:
        for attempt in range(1, MAX_AGENT_ATTEMPTS + 1):
            team = build_team(config)
            task = prompt if last_error is None else _augment_prompt(prompt, last_error)
            try:
                LOGGER.info("Running Magentic-One orchestrator (attempt %s)", attempt)
                result = await _run_team_with_logging(team, task, raw_log_path)
                run_data = _extract_run_data(result)
                if run_data:
                    validation_error = _validate_scene_payload(run_data)
                    if validation_error is not None:
                        LOGGER.warning("Scene payload incomplete: %s", validation_error)
                        last_error = validation_error
                        run_data = {}
                        continue
                    break
                last_error = "Orchestrator returned an incomplete payload"
            except Exception as exc:  # pragma: no cover - defensive logging
                LOGGER.warning("Magentic-One attempt %s failed: %s", attempt, exc)
                last_error = str(exc)
    finally:
        _detach_agent_logger(agent_handler)

    log_path = _finalize_agent_log(raw_log_path, run_data.get("scene_id"))
    if log_path:
        run_data.setdefault("metadata", {})
        run_data["metadata"]["agent_log_path"] = str(log_path)

    if "scene_graph" not in run_data or "scene_id" not in run_data:
        raise RuntimeError(f"Magentic-One failed after {MAX_AGENT_ATTEMPTS} attempts: {last_error}")

    run_data.setdefault("prompt", prompt)
    _materialize_scene_outputs(run_data, prompt, config)
    _ingest_run_data(run_data, config)
    return run_data


def _apply_env_overrides(config: RuntimeConfig) -> None:
    os.environ.setdefault("ASSET_ROOT", str(config.paths.asset_root.resolve()))
    os.environ.setdefault("RUN_OUTPUT_DIR", str(config.paths.run_root.resolve()))
    os.environ.setdefault("SNAPSHOT_ROOT", str(config.paths.snapshot_root.resolve()))


def _extract_run_data(result: Dict) -> Dict:
    if isinstance(result, dict):
        extracted = _extract_scene_payload(result)
        return extracted if extracted else {}

    if isinstance(result, TaskResult):
        return _extract_from_task_result(result)

    LOGGER.warning("Unhandled team result type: %s", type(result))
    return {}


def _augment_prompt(prompt: str, error: str) -> str:
    return (
        f"{prompt}\n\n"
        "The previous attempt failed. Analyze the error and correct the plan before retrying.\n"
        f"Error details: {error}"
    )


async def _run_team_with_logging(team, task: str, log_path: Path):  # type: ignore[no-untyped-def]
    """Stream team output while writing verbatim logs to disk."""

    async def _consume() -> TaskResult | Dict | None:
        log_file = log_path.open("a", encoding="utf-8")
        try:
            async for message in team.run_stream(task=task, output_task_messages=True):
                _write_log_entry(log_file, message)
                if isinstance(message, TaskResult):
                    return message
            return None
        finally:
            log_file.flush()
            log_file.close()

    return await _consume()


def _attach_agent_logger(config: RuntimeConfig) -> Tuple[logging.Handler, Path]:
    logs_dir = config.paths.run_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("agent_%Y%m%d_%H%M%S_%f")
    log_path = logs_dir / f"{timestamp}.log"
    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    event_logger = logging.getLogger("autogen_agentchat.events")
    console_logger = logging.getLogger("autogen_agentchat")

    for target_logger in (event_logger, console_logger):
        target_logger.setLevel(logging.INFO)
        target_logger.addHandler(handler)

    return handler, log_path


def _detach_agent_logger(handler: logging.Handler) -> None:
    for logger_name in ("autogen_agentchat.events", "autogen_agentchat"):
        logger = logging.getLogger(logger_name)
        if handler in logger.handlers:
            logger.removeHandler(handler)
    handler.close()


def _finalize_agent_log(log_path: Path, scene_id: Optional[str]) -> Optional[Path]:
    if not log_path.exists():
        return None
    if scene_id:
        safe_id = scene_id.replace(os.sep, "_")
        target = log_path.with_name(f"{safe_id}.log")
        if target != log_path:
            try:
                if target.exists():
                    target.unlink()
                log_path.rename(target)
                return target
            except OSError as exc:
                LOGGER.warning("Failed to rename agent log %s -> %s: %s", log_path, target, exc)
                return log_path
    return log_path


def _write_log_entry(log_file, message) -> None:  # type: ignore[no-untyped-def]
    record = {
        "time": datetime.utcnow().isoformat(),
        "type": type(message).__name__,
    }
    payload: object
    if hasattr(message, "model_dump") and callable(getattr(message, "model_dump")):
        try:
            payload = message.model_dump()
        except Exception:  # pragma: no cover - best effort
            payload = repr(message)
    else:
        payload = repr(message)
    record["payload"] = payload
    log_file.write(json.dumps(record, default=str) + "\n")


def _extract_from_task_result(result: TaskResult) -> Dict:
    manifest_info = _manifest_info_from_messages(result.messages)
    if manifest_info:
        run_data = _load_manifest(manifest_info)
        if run_data:
            run_data.setdefault("manifest_path", manifest_info.get("manifest_path"))
            if "run_id" in manifest_info and "scene_id" not in run_data:
                run_data["scene_id"] = manifest_info["run_id"]
            return run_data

    extracted = _extract_scene_payload(getattr(result, "output", None))
    if extracted:
        return extracted

    for message in reversed(result.messages):
        if isinstance(message, TextMessage):
            payload = _parse_json_payload(message.content)
            extracted = _extract_scene_payload(payload)
            if extracted:
                return extracted

    return {}


def _manifest_info_from_messages(messages: Sequence[BaseAgentEvent | BaseChatMessage]) -> Optional[Dict]:
    manifest: Optional[Dict] = None
    for message in messages:
        if isinstance(message, FunctionExecutionResultMessage):
            for result in message.content:
                if isinstance(result, FunctionExecutionResult) and result.name == "persist_run":
                    candidate = _parse_json_payload(result.content)
                    if isinstance(candidate, dict):
                        manifest = candidate
    return manifest


def _parse_json_payload(payload: object) -> Optional[object]:
    if isinstance(payload, (dict, list)):
        return payload
    if isinstance(payload, str):
        stripped = payload.strip()
        if not stripped:
            return None
        try:
            return json.loads(stripped)
        except json.JSONDecodeError:
            if "{" not in stripped or "}" not in stripped:
                return None

            # Some providers return JSON payloads that are double-escaped (e.g. "\n{\n  \"key\": ...}").
            # Attempt to unescape these strings before parsing so we do not lose valid payloads.
            if "\\n" in stripped or "\\\"" in stripped:
                try:
                    unescaped = bytes(stripped, "utf-8").decode("unicode_escape")
                except UnicodeDecodeError:
                    unescaped = None
                if unescaped and unescaped != stripped:
                    decoded = _parse_json_payload(unescaped)
                    if decoded is not None:
                        return decoded

            try:
                extracted = extract_json_from_str(stripped)
            except (json.JSONDecodeError, ValueError):
                extracted = None
            if extracted:
                return extracted[0] if len(extracted) == 1 else extracted

            try:
                literal = ast.literal_eval(stripped)
            except (ValueError, SyntaxError):
                return None
            if isinstance(literal, (dict, list)):
                return literal
    return None


def _extract_scene_payload(candidate: object) -> Optional[Dict]:
    required_keys = {"scene_graph", "scene_id"}

    if isinstance(candidate, dict):
        if required_keys.issubset(candidate.keys()):
            return candidate

        for key in ("payload", "data", "result", "output", "content"):
            nested_value = candidate.get(key)
            extracted = _extract_scene_payload(nested_value)
            if extracted:
                return extracted

    if isinstance(candidate, Sequence) and not isinstance(candidate, (str, bytes, bytearray)):
        for item in candidate:
            extracted = _extract_scene_payload(item)
            if extracted:
                return extracted

    return None


def _validate_scene_payload(run_data: Dict) -> Optional[str]:
    if not isinstance(run_data, dict):
        return "Scene payload is not a dictionary"

    scene_id = run_data.get("scene_id") or (run_data.get("scene_graph") or {}).get("scene_id")
    if not isinstance(scene_id, str) or not scene_id.strip():
        return "Scene payload missing scene_id"

    scene_graph = run_data.get("scene_graph")
    if not isinstance(scene_graph, dict):
        return "Scene graph missing or malformed"

    placements = scene_graph.get("placements")
    if not (isinstance(placements, Sequence) and not isinstance(placements, (str, bytes, bytearray)) and placements):
        return "Scene graph does not include placements"

    asset_ids = _collect_candidate_asset_ids(scene_graph, run_data)
    if not asset_ids:
        return "Scene placements are missing asset references"

    return None


def _collect_candidate_asset_ids(scene_graph: Dict, run_data: Dict) -> List[str]:
    candidate: List[str] = []

    raw_assets = run_data.get("assets")
    if isinstance(raw_assets, Sequence) and not isinstance(raw_assets, (str, bytes, bytearray)):
        for item in raw_assets:
            if isinstance(item, str) and item.strip():
                candidate.append(item.strip())
            elif isinstance(item, dict):
                asset_id = item.get("id")
                if isinstance(asset_id, str) and asset_id.strip():
                    candidate.append(asset_id.strip())

    placements = scene_graph.get("placements")
    if isinstance(placements, Sequence) and not isinstance(placements, (str, bytes, bytearray)):
        for entry in placements:
            if not isinstance(entry, dict):
                continue
            for key in ("ref", "asset", "asset_id", "id"):
                value = entry.get(key)
                if isinstance(value, str) and value.strip():
                    candidate.append(value.strip())
                    break

    asset_manifests = scene_graph.get("asset_manifests")
    if isinstance(asset_manifests, dict):
        for items in asset_manifests.values():
            if isinstance(items, Sequence) and not isinstance(items, (str, bytes, bytearray)):
                for item in items:
                    if isinstance(item, str) and item.strip():
                        candidate.append(item.strip())
                    elif isinstance(item, dict):
                        asset_id = item.get("id")
                        if isinstance(asset_id, str) and asset_id.strip():
                            candidate.append(asset_id.strip())
            elif isinstance(items, str) and items.strip():
                candidate.append(items.strip())

    return [asset_id for asset_id in dict.fromkeys(candidate) if asset_id]


def _load_manifest(info: Dict) -> Optional[Dict]:
    manifest_path_value = info.get("manifest_path")
    if not manifest_path_value:
        LOGGER.warning("persist_run did not provide a manifest_path")
        return None
    manifest_path = Path(manifest_path_value)
    if not manifest_path.exists():
        LOGGER.warning("Manifest path %s does not exist", manifest_path)
        return None
    try:
        data = json.loads(manifest_path.read_text())
    except json.JSONDecodeError as exc:
        LOGGER.warning("Failed to parse manifest %s: %s", manifest_path, exc)
        return None
    data.setdefault("manifest_path", str(manifest_path))
    return data


def _ingest_run_data(run_data: Dict, config: RuntimeConfig) -> None:
    scene_graph = run_data.get("scene_graph")
    if not scene_graph:
        return
    scene_id = run_data.get("scene_id", scene_graph.get("scene_id", "unknown"))
    shards = shard_scene_graph(scene_graph)
    if run_data.get("requirements"):
        shards.append(
            {
                "id": f"requirements:{scene_id}",
                "type": "requirements",
                "tags": ["requirements"],
                "content": str(run_data["requirements"]),
            }
        )

    embedder = Embedder(config.vector_store.embedding_dim, config.vector_store.embedding_model)
    embeddings = embedder.encode(shard["content"] for shard in shards)

    vector_store = VectorStore(
        config.vector_store.faiss_index_path,
        config.vector_store.embedding_dim,
        config.vector_store.use_faiss,
    )
    vector_store.add(embeddings, shards)

    registry = RunRegistry(config.vector_store.sqlite_path)
    registry.upsert_run(scene_id, run_data.get("manifest_path", ""), run_data.get("snapshot_path"))
    registry.add_docs(scene_id, shards)


def _materialize_scene_outputs(run_data: Dict, prompt: str, config: RuntimeConfig) -> None:
    scene_graph = run_data.get("scene_graph") or {}
    if not scene_graph:
        return

    scene_id = run_data.setdefault("scene_id", scene_graph.get("scene_id") or datetime.utcnow().strftime("scene_%Y%m%d_%H%M%S"))
    scene_graph.setdefault("scene_id", scene_id)

    manifest_path = run_data.get("manifest_path")
    snapshot_path = run_data.get("snapshot_path")
    manifest_exists = bool(manifest_path and Path(manifest_path).exists())
    snapshot_exists = bool(snapshot_path and Path(snapshot_path).exists())

    asset_ids = _collect_candidate_asset_ids(scene_graph, run_data)

    # Normalize placement entries so downstream tooling can infer concepts properly.
    placements = scene_graph.get("placements")
    if isinstance(placements, list):
        for entry in placements:
            if not isinstance(entry, dict):
                continue
            ref = entry.get("ref")
            if isinstance(ref, str) and ref.strip():
                entry["ref"] = ref.strip()
                continue
            for key in ("asset_id", "asset", "id"):
                value = entry.get(key)
                if isinstance(value, str) and value.strip():
                    entry["ref"] = value.strip()
                    break

    requirements = run_data.get("requirements")
    if not isinstance(requirements, dict):
        requirements = {"requirements": []}
    run_data["requirements"] = requirements

    scene_spec = run_data.get("scene_spec")
    if not isinstance(scene_spec, dict):
        scene_spec = design_scene_spec(requirements)
    if not scene_spec.get("entities") and asset_ids:
        scene_spec["entities"] = [
            {
                "concept": infer_concept_from_id(asset_id),
                "count": 1,
                "attrs": {},
            }
            for asset_id in asset_ids
        ]
    scene_spec.setdefault("constraints", scene_spec.get("constraints", []))
    run_data["scene_spec"] = scene_spec

    if not requirements.get("requirements") and scene_spec.get("entities"):
        requirements["requirements"] = [
            {
                "concept": entity.get("concept", "asset"),
                "min_count": entity.get("count", 1),
            }
            for entity in scene_spec.get("entities", [])
        ]

    manifests: List[Dict] = []
    if asset_ids:
        recipes = expand_assets(scene_spec, asset_ids=asset_ids)
        for recipe in recipes:
            try:
                manifests.append(compile_asset(recipe))
            except Exception as exc:  # pragma: no cover - defensive logging
                LOGGER.warning("Failed to compile asset %s: %s", recipe.get("id"), exc)
        if manifests:
            run_data["assets"] = manifests
            scene_graph["assets"] = [manifest.get("id") for manifest in manifests if manifest.get("id")]
    if not scene_graph.get("assets") and asset_ids:
        scene_graph["assets"] = asset_ids
    run_data.setdefault("assets", run_data.get("assets", manifests))

    map_plan = run_data.get("map_plan") or scene_graph.get("map")
    if not isinstance(map_plan, dict):
        map_plan = generate_map(scene_spec)
    run_data["map_plan"] = map_plan
    scene_graph["map"] = map_plan

    validation = validate_scene(scene_graph, requirements)
    run_data["validation"] = validation

    manifest_payload: Dict | None = None
    if not manifest_exists:
        manifest_payload = {
            "scene_id": scene_id,
            "prompt": run_data.get("prompt", prompt),
            "requirements": requirements,
            "scene_spec": scene_spec,
            "assets": manifests or run_data.get("assets", []),
            "map_plan": map_plan,
            "scene_graph": scene_graph,
            "validation": validation,
        }
        manifest_info = persist_run(manifest_payload)
        run_data["manifest_path"] = manifest_info.get("manifest_path")
    else:
        # ensure we keep reference for ingestion
        run_data["manifest_path"] = manifest_path
        manifest_payload = None

    viewer_info: Dict[str, str] = {}
    manifest_for_view: Optional[Dict] = manifest_payload
    if manifest_for_view is None and run_data.get("manifest_path"):
        try:
            with Path(run_data["manifest_path"]).open("r", encoding="utf-8") as manifest_file:
                manifest_for_view = json.load(manifest_file)
        except Exception as exc:  # pragma: no cover - defensive logging
            LOGGER.warning("Failed to load manifest %s for viewer export: %s", run_data.get("manifest_path"), exc)

    if manifest_for_view and run_data.get("manifest_path"):
        try:
            viewer_info = render_web_view(manifest_for_view, run_data["manifest_path"])
        except Exception as exc:  # pragma: no cover - defensive logging
            LOGGER.warning("Failed to render interactive view for %s: %s", scene_id, exc)

    if viewer_info:
        run_data.update(viewer_info)

    if not snapshot_exists:
        snapshot_info = render_snapshot(scene_graph)
        run_data["snapshot_path"] = snapshot_info.get("snapshot_path")
    else:
        run_data["snapshot_path"] = snapshot_path

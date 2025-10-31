"""Runtime configuration for the agentic loop."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass(slots=True)
class ModelConfig:
    """Settings for the Cerebras-hosted Qwen model."""

    model_name: str = "qwen-3-coder-480b"
    base_url: str = "https://api.cerebras.ai/v1"
    temperature: float = 0.1
    max_output_tokens: int = -1
    request_timeout: int = 300


@dataclass(slots=True)
class ContextBudgets:
    """Token budgets for various prompt tiers to protect the context window."""

    system_tokens: int = 12000
    run_summary_tokens: int = 12000
    worklist_tokens: int = 12000
    per_turn_tokens: int = 12000
    shard_limit: int = 20
    shard_tokens: int = 150


@dataclass(slots=True)
class PathsConfig:
    """Filesystem layout for run manifests and asset storage."""

    run_root: Path = field(default_factory=lambda: Path("runs"))
    asset_root: Path = field(default_factory=lambda: Path("assets"))
    snapshot_root: Path = field(default_factory=lambda: Path("snapshots"))


@dataclass(slots=True)
class VectorStoreConfig:
    """Configuration for FAISS + SQLite memory layers."""

    faiss_index_path: Path = field(default_factory=lambda: Path("memory") / "faiss.index")
    sqlite_path: Path = field(default_factory=lambda: Path("memory") / "memory.db")
    embedding_model: str = "gemini-embedding-001"
    embedding_dim: int = 768
    use_faiss: bool = False


@dataclass(slots=True)
class RuntimeConfig:
    """Aggregated configuration object used across the system."""

    model: ModelConfig = field(default_factory=ModelConfig)
    context: ContextBudgets = field(default_factory=ContextBudgets)
    paths: PathsConfig = field(default_factory=PathsConfig)
    vector_store: VectorStoreConfig = field(default_factory=VectorStoreConfig)
    max_parallel_tools: int = 3
    enforce_human_gate: bool = True
    dotenv_path: Optional[Path] = None

    def ensure_directories(self) -> None:
        """Create directories that must exist before running the pipeline."""

        self.paths.run_root.mkdir(parents=True, exist_ok=True)
        self.paths.asset_root.mkdir(parents=True, exist_ok=True)
        self.paths.snapshot_root.mkdir(parents=True, exist_ok=True)
        self.vector_store.faiss_index_path.parent.mkdir(parents=True, exist_ok=True)
        self.vector_store.sqlite_path.parent.mkdir(parents=True, exist_ok=True)

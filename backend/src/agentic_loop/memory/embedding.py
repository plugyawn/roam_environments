"""Embedding helper backed by Google Gemini, with deterministic fallback."""

from __future__ import annotations

import hashlib
import logging
import os
from typing import Iterable, List

import numpy as np

try:  # pragma: no cover - optional dependency
    from google import genai
except ImportError:  # pragma: no cover - allow offline testing
    genai = None

LOGGER = logging.getLogger(__name__)


class Embedder:
    """Generate fixed-size embeddings for text snippets."""

    def __init__(self, dim: int, model: str = "gemini-embedding-001") -> None:
        if dim <= 0:
            raise ValueError("Embedding dimension must be positive")
        self.dim = dim
        self.model = model
        self._client = None
        if genai is not None:
            api_key = os.environ.get("GOOGLE_API_KEY")
            if api_key:
                try:
                    self._client = genai.Client(api_key=api_key)
                except Exception as exc:  # pragma: no cover - network failure
                    LOGGER.warning("Failed to initialise Gemini client; falling back to hashing: %s", exc)
            else:
                LOGGER.info("GOOGLE_API_KEY not set; using deterministic embeddings")
        else:
            LOGGER.info("google-genai library not available; using deterministic embeddings")

    def encode(self, texts: Iterable[str]) -> List[np.ndarray]:
        texts = list(texts)
        if not texts:
            return []
        if self._client is not None:
            try:
                response = self._client.models.embed_content(
                    model=self.model,
                    contents=texts,
                )
                embeddings = []
                for embedding in response.embeddings:
                    values = np.array(embedding.values, dtype="float32")
                    if values.shape[0] != self.dim:
                        values = _resize(values, self.dim)
                    embeddings.append(values)
                if len(embeddings) == len(texts):
                    return embeddings
                LOGGER.warning("Gemini returned %s embeddings for %s inputs; falling back", len(embeddings), len(texts))
            except Exception as exc:  # pragma: no cover - API failure
                LOGGER.warning("Gemini embedding call failed; falling back to deterministic hashes: %s", exc)
        return [_deterministic_embedding(text, self.dim) for text in texts]


def _deterministic_embedding(text: str, dim: int) -> np.ndarray:
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    repeated = (digest * ((dim + len(digest) - 1) // len(digest)))[: dim]
    arr = np.frombuffer(repeated, dtype=np.uint8).astype("float32")
    return (arr - arr.mean()) / (arr.std() + 1e-6)


def _resize(values: np.ndarray, dim: int) -> np.ndarray:
    if values.size == dim:
        return values
    if values.size > dim:
        return values[:dim]
    repeats = (dim + values.size - 1) // values.size
    tiled = np.tile(values, repeats)[:dim]
    return tiled

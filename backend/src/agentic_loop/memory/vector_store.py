"""FAISS-backed vector store wrapper with metadata fallback."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Iterable, List

import numpy as np

try:
    import faiss  # type: ignore
except ImportError:  # pragma: no cover - faiss may not be available during linting
    faiss = None


LOGGER = logging.getLogger(__name__)


class VectorStore:
    """Thin wrapper managing an IVF-PQ index with doc metadata persistence."""

    def __init__(self, index_path: Path, dim: int, use_faiss: bool = True) -> None:
        self.index_path = index_path
        self.dim = dim
        self._use_faiss = bool(use_faiss and faiss is not None)
        self._meta_path = index_path.with_suffix(".meta.json")
        self._metadata = self._load_metadata()
        self._index = self._load_index()

    def _load_index(self):  # type: ignore[no-untyped-def]
        if not self._use_faiss:
            return None
        if self.index_path.exists():
            return faiss.read_index(str(self.index_path))
        quantizer = faiss.IndexFlatL2(self.dim)
        index = faiss.IndexIVFFlat(quantizer, self.dim, 64)
        index.nprobe = 8
        return index

    def _load_metadata(self) -> List[dict]:
        if self._meta_path.exists():
            return json.loads(self._meta_path.read_text())
        return []

    def add(self, embeddings: Iterable[np.ndarray], docs: Iterable[dict]) -> None:
        vector_list = list(embeddings)
        doc_list = list(docs)
        if not doc_list:
            return
        self._metadata.extend(doc_list)
        self._persist_metadata()
        if not vector_list or not self._use_faiss or self._index is None:
            return
        vectors = np.vstack(vector_list).astype("float32")
        try:
            if not self._index.is_trained:
                self._index.train(vectors)
            self._index.add(vectors)
            faiss.write_index(self._index, str(self.index_path))
        except Exception as exc:  # pragma: no cover - defensive fallback
            LOGGER.warning("FAISS index update failed, disabling index: %s", exc)
            self._use_faiss = False
            self._index = None
            if self.index_path.exists():
                try:
                    self.index_path.unlink()
                except OSError:
                    LOGGER.debug("Failed to remove FAISS index after failure", exc_info=True)

    def search(self, embedding: np.ndarray, top_k: int = 10) -> List[dict]:
        if not self._use_faiss or self._index is None or self._index.ntotal == 0:
            return self._metadata[:top_k]
        embedding = embedding.astype("float32").reshape(1, -1)
        distances, indices = self._index.search(embedding, top_k)
        hits: List[dict] = []
        for idx in indices[0]:
            if idx == -1:
                continue
            if 0 <= idx < len(self._metadata):
                hits.append(self._metadata[idx])
        return hits

    def _persist_metadata(self) -> None:
        self._meta_path.write_text(json.dumps(self._metadata, indent=2))

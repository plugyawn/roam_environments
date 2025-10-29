"""SQLite registry tracking run manifests and assets."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Dict, Iterable, List


class RunRegistry:
    """Record run manifests and asset metadata."""

    def __init__(self, sqlite_path: Path) -> None:
        self.sqlite_path = sqlite_path
        self.sqlite_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_tables()

    def _ensure_tables(self) -> None:
        with sqlite3.connect(self.sqlite_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS runs (
                    run_id TEXT PRIMARY KEY,
                    manifest_path TEXT NOT NULL,
                    snapshot_path TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS docs (
                    doc_id TEXT PRIMARY KEY,
                    run_id TEXT,
                    type TEXT,
                    tags TEXT,
                    content TEXT,
                    FOREIGN KEY(run_id) REFERENCES runs(run_id)
                )
                """
            )
            conn.commit()

    def upsert_run(self, run_id: str, manifest_path: str, snapshot_path: str | None = None) -> None:
        with sqlite3.connect(self.sqlite_path) as conn:
            conn.execute(
                """
                INSERT INTO runs(run_id, manifest_path, snapshot_path)
                VALUES(?,?,?)
                ON CONFLICT(run_id) DO UPDATE SET manifest_path=excluded.manifest_path, snapshot_path=excluded.snapshot_path
                """,
                (run_id, manifest_path, snapshot_path),
            )
            conn.commit()

    def add_docs(self, run_id: str, docs: Iterable[Dict]) -> None:
        with sqlite3.connect(self.sqlite_path) as conn:
            records = []
            dropped: List[str] = []
            for doc in docs:
                doc_id = doc.get("id")
                if not doc_id:  # malformed shard; skip instead of crashing
                    dropped.append("<missing id>")
                    continue
                raw_tags = doc.get("tags") or []
                tags = [str(tag).strip() for tag in raw_tags if isinstance(tag, (str, int, float))]
                records.append(
                    (
                        doc_id,
                        run_id,
                        doc.get("type"),
                        ",".join(filter(None, tags)),
                        doc.get("content"),
                    )
                )
                if len(tags) != len(raw_tags):
                    dropped.append(doc_id)
            if not records:
                if dropped:
                    print(  # use print to avoid pulling logging into hot path
                        f"Skipping {len(dropped)} malformed docs for run {run_id}: {', '.join(dropped[:3])}"
                    )
                return
            conn.executemany(
                """
                INSERT OR REPLACE INTO docs(doc_id, run_id, type, tags, content)
                VALUES(?,?,?,?,?)
                """,
                records,
            )
            conn.commit()
        if dropped:
            print(f"Sanitized {len(dropped)} doc(s) for run {run_id}: {', '.join(dropped[:3])}")

    def fetch_docs_by_tags(self, tags: List[str]) -> List[Dict]:
        if not tags:
            return []
        pattern = "%" + "%".join(tags) + "%"
        with sqlite3.connect(self.sqlite_path) as conn:
            cursor = conn.execute(
                "SELECT doc_id, type, tags, content FROM docs WHERE tags LIKE ?",
                (pattern,),
            )
            rows = cursor.fetchall()
        docs: List[Dict] = []
        for row in rows:
            doc_id, doc_type, tags_csv, content = row
            docs.append(
                {
                    "id": doc_id,
                    "type": doc_type,
                    "tags": tags_csv.split(",") if tags_csv else [],
                    "content": content,
                }
            )
        return docs

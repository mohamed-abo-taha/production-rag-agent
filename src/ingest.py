"""Corpus ingestion: load documents, chunk with overlap, embed, and upsert into Qdrant.

Also persists the raw chunks to disk so the BM25 (sparse) index can be rebuilt at query time
without re-reading the source corpus.
"""

from __future__ import annotations

import json
import re
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import get_settings
from .embeddings import get_embedder
from .vector_store import get_vector_store


@dataclass
class Chunk:
    id: str
    text: str
    source: str
    chunk_index: int


def _read_corpus(corpus_dir: Path) -> list[tuple[str, str]]:
    """Return (source_name, text) for every .md/.txt file under corpus_dir."""
    docs: list[tuple[str, str]] = []
    for path in sorted(corpus_dir.rglob("*")):
        if path.suffix.lower() in {".md", ".txt"} and path.is_file():
            docs.append((path.name, path.read_text(encoding="utf-8")))
    return docs


def _split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Paragraph-aware sliding window. Keeps paragraphs together until the size budget is hit."""
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks: list[str] = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) + 2 <= chunk_size:
            current = f"{current}\n\n{para}".strip()
        else:
            if current:
                chunks.append(current)
            # If a single paragraph exceeds the budget, hard-split it.
            if len(para) > chunk_size:
                for i in range(0, len(para), chunk_size - overlap):
                    chunks.append(para[i : i + chunk_size])
                current = ""
            else:
                current = para
    if current:
        chunks.append(current)

    # Add overlap by prepending the tail of the previous chunk.
    if overlap > 0 and len(chunks) > 1:
        overlapped = [chunks[0]]
        for prev, cur in zip(chunks, chunks[1:]):
            tail = prev[-overlap:]
            overlapped.append(f"{tail}\n{cur}")
        chunks = overlapped
    return chunks


def build_chunks(corpus_dir: Path, chunk_size: int, overlap: int) -> list[Chunk]:
    chunks: list[Chunk] = []
    for source, text in _read_corpus(corpus_dir):
        for idx, piece in enumerate(_split_text(text, chunk_size, overlap)):
            chunks.append(
                Chunk(
                    id=str(uuid.uuid5(uuid.NAMESPACE_URL, f"{source}:{idx}")),
                    text=piece,
                    source=source,
                    chunk_index=idx,
                )
            )
    return chunks


def chunks_path() -> Path:
    return Path(get_settings().qdrant_path).parent / "chunks.jsonl"


def ingest() -> int:
    """Full ingestion pipeline. Returns the number of chunks indexed."""
    settings = get_settings()
    corpus_dir = Path(settings.corpus_dir)
    if not corpus_dir.exists():
        raise FileNotFoundError(f"Corpus directory not found: {corpus_dir}")

    chunks = build_chunks(corpus_dir, settings.chunk_size, settings.chunk_overlap)
    if not chunks:
        raise ValueError(f"No .md/.txt documents found under {corpus_dir}")

    embedder = get_embedder()
    vectors = embedder.embed([c.text for c in chunks])

    store = get_vector_store(vector_size=vectors.shape[1])
    store.reset()
    store.upsert(
        ids=[c.id for c in chunks],
        vectors=vectors,
        payloads=[{"text": c.text, "source": c.source, "chunk_index": c.chunk_index} for c in chunks],
    )

    # Persist chunks for the BM25 index.
    out = chunks_path()
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(asdict(c)) + "\n")

    return len(chunks)


def load_chunks() -> list[Chunk]:
    path = chunks_path()
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run `python -m scripts.run_ingest` (or `make ingest`) first."
        )
    return [Chunk(**json.loads(line)) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

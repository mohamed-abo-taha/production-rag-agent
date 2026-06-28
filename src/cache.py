"""Semantic cache: returns a prior answer when a new query is near-duplicate of a cached one.

Cuts cost and latency on repeated/paraphrased questions. Cosine similarity over query embeddings
with a high threshold (default 0.95) so only genuinely equivalent questions hit the cache.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .config import get_settings
from .embeddings import get_embedder


@dataclass
class CacheEntry:
    query: str
    answer: str
    vector: np.ndarray


@dataclass
class SemanticCache:
    threshold: float
    _entries: list[CacheEntry] = field(default_factory=list)

    def lookup(self, query_vector: np.ndarray) -> str | None:
        for entry in self._entries:
            if float(np.dot(query_vector, entry.vector)) >= self.threshold:
                return entry.answer
        return None

    def add(self, query: str, query_vector: np.ndarray, answer: str) -> None:
        self._entries.append(CacheEntry(query=query, answer=answer, vector=query_vector))

    def __len__(self) -> int:  # for /stats and tests
        return len(self._entries)


_cache: SemanticCache | None = None


def get_cache() -> SemanticCache:
    global _cache
    if _cache is None:
        _cache = SemanticCache(threshold=get_settings().cache_similarity_threshold)
    return _cache


def embed_query(query: str) -> np.ndarray:
    return get_embedder().embed_one(query)

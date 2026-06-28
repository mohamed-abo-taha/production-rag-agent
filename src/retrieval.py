"""Hybrid retrieval: dense (vector) + sparse (BM25) candidates fused, then cross-encoder reranking.

This is the quality core of the system. Naive vector search alone misses exact-keyword matches
(IDs, error codes, rare terms); BM25 alone misses paraphrases. Fusing both and reranking with a
cross-encoder gives materially better context precision than any single retriever.
"""

from __future__ import annotations

from dataclasses import dataclass

from .config import get_settings
from .embeddings import get_embedder, get_reranker
from .ingest import Chunk, load_chunks
from .vector_store import ScoredChunk, get_vector_store


@dataclass
class RetrievedContext:
    chunks: list[ScoredChunk]
    weak: bool  # True when the best rerank score is below threshold → agent should self-correct


def _tokenize(text: str) -> list[str]:
    return [t for t in "".join(c.lower() if c.isalnum() else " " for c in text).split() if t]


class HybridRetriever:
    def __init__(self) -> None:
        self._settings = get_settings()
        self._embedder = get_embedder()
        self._reranker = get_reranker()
        self._store = get_vector_store()
        self._chunks: list[Chunk] = load_chunks()
        self._by_id = {c.id: c for c in self._chunks}
        self._build_bm25()

    def _build_bm25(self) -> None:
        from rank_bm25 import BM25Okapi

        self._corpus_tokens = [_tokenize(c.text) for c in self._chunks]
        self._bm25 = BM25Okapi(self._corpus_tokens)

    def _dense(self, query: str) -> list[str]:
        qv = self._embedder.embed_one(query)
        hits = self._store.search(qv, top_k=self._settings.dense_top_k)
        return [h.id for h in hits]

    def _sparse(self, query: str) -> list[str]:
        scores = self._bm25.get_scores(_tokenize(query))
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        return [self._chunks[i].id for i in ranked[: self._settings.bm25_top_k]]

    def retrieve(self, query: str) -> RetrievedContext:
        # 1. Gather candidates from both retrievers and dedupe.
        candidate_ids: list[str] = []
        for cid in self._dense(query) + self._sparse(query):
            if cid not in candidate_ids:
                candidate_ids.append(cid)
        candidates = [self._by_id[cid] for cid in candidate_ids if cid in self._by_id]
        if not candidates:
            return RetrievedContext(chunks=[], weak=True)

        # 2. Rerank with the cross-encoder for precision.
        scores = self._reranker.score(query, [c.text for c in candidates])
        ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
        top = ranked[: self._settings.rerank_top_k]

        chunks = [
            ScoredChunk(
                id=c.id, text=c.text, source=c.source, chunk_index=c.chunk_index, score=float(s)
            )
            for c, s in top
        ]
        weak = (not chunks) or chunks[0].score < self._settings.min_rerank_score
        return RetrievedContext(chunks=chunks, weak=weak)


_retriever: HybridRetriever | None = None


def get_retriever() -> HybridRetriever:
    global _retriever
    if _retriever is None:
        _retriever = HybridRetriever()
    return _retriever

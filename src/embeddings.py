"""Local sentence-transformer embeddings and cross-encoder reranking.

Models are downloaded once and cached by sentence-transformers. No API key required, so the
retrieval stack is fully testable offline / in CI.
"""

from __future__ import annotations

import numpy as np

from .config import get_settings


class Embedder:
    def __init__(self) -> None:
        from sentence_transformers import SentenceTransformer

        self._model = SentenceTransformer(get_settings().embedding_model)

    def embed(self, texts: list[str]) -> np.ndarray:
        """Return L2-normalised embeddings (so dot product == cosine similarity)."""
        return self._model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=len(texts) > 64,
        )

    def embed_one(self, text: str) -> np.ndarray:
        return self.embed([text])[0]


class Reranker:
    def __init__(self) -> None:
        from sentence_transformers import CrossEncoder

        self._model = CrossEncoder(get_settings().reranker_model)

    def score(self, query: str, passages: list[str]) -> list[float]:
        if not passages:
            return []
        pairs = [(query, p) for p in passages]
        return [float(s) for s in self._model.predict(pairs)]


_embedder: Embedder | None = None
_reranker: Reranker | None = None


def get_embedder() -> Embedder:
    global _embedder
    if _embedder is None:
        _embedder = Embedder()
    return _embedder


def get_reranker() -> Reranker:
    global _reranker
    if _reranker is None:
        _reranker = Reranker()
    return _reranker

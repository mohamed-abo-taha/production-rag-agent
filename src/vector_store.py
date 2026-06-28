"""Qdrant wrapper. Defaults to a local on-disk collection so no server is required to run the demo.

Set QDRANT_URL to point at a real Qdrant instance (e.g. the one in docker-compose) for production.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .config import get_settings


@dataclass
class ScoredChunk:
    id: str
    text: str
    source: str
    chunk_index: int
    score: float


class VectorStore:
    def __init__(self, vector_size: int) -> None:
        from qdrant_client import QdrantClient
        from qdrant_client.models import Distance, VectorParams

        settings = get_settings()
        self._collection = settings.collection_name
        if settings.qdrant_url:
            # api_key is honoured automatically for authenticated Qdrant Cloud clusters.
            self._client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key or None)
        else:
            self._client = QdrantClient(path=settings.qdrant_path)
        self._vector_size = vector_size
        self._VectorParams = VectorParams
        self._Distance = Distance

    def reset(self) -> None:
        self._client.recreate_collection(
            collection_name=self._collection,
            vectors_config=self._VectorParams(size=self._vector_size, distance=self._Distance.COSINE),
        )

    def upsert(self, ids: list[str], vectors: np.ndarray, payloads: list[dict]) -> None:
        from qdrant_client.models import PointStruct

        points = [
            PointStruct(id=i, vector=v.tolist(), payload=p)
            for i, v, p in zip(ids, vectors, payloads)
        ]
        self._client.upsert(collection_name=self._collection, points=points)

    def search(self, query_vector: np.ndarray, top_k: int) -> list[ScoredChunk]:
        # qdrant-client >= 1.12 replaced .search() with .query_points().
        hits = self._client.query_points(
            collection_name=self._collection,
            query=query_vector.tolist(),
            limit=top_k,
            with_payload=True,
        ).points
        return [
            ScoredChunk(
                id=str(h.id),
                text=h.payload["text"],
                source=h.payload["source"],
                chunk_index=h.payload["chunk_index"],
                score=float(h.score),
            )
            for h in hits
        ]


_store: VectorStore | None = None


def get_vector_store(vector_size: int = 384) -> VectorStore:
    global _store
    if _store is None:
        _store = VectorStore(vector_size=vector_size)
    return _store

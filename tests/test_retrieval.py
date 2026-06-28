"""Tests that run without an API key — they exercise chunking, the semantic cache, and metrics.

Retrieval/agent tests that need embedding-model downloads are marked `integration` and skipped
by default in CI's fast lane. Run everything with `pytest -m ''`.
"""

from __future__ import annotations

import numpy as np
import pytest

from eval.metrics import abstention_correct, context_recall
from src.cache import SemanticCache
from src.ingest import _split_text


def test_split_text_respects_size():
    text = "\n\n".join(f"Paragraph number {i} with some filler words." for i in range(20))
    chunks = _split_text(text, chunk_size=120, overlap=20)
    assert len(chunks) > 1
    # No chunk should wildly exceed the budget (overlap adds a bounded prefix).
    assert all(len(c) <= 120 + 20 + 5 for c in chunks)


def test_split_text_hard_splits_long_paragraph():
    long_para = "x" * 500
    chunks = _split_text(long_para, chunk_size=100, overlap=10)
    assert len(chunks) >= 5


def test_semantic_cache_hit_and_miss():
    cache = SemanticCache(threshold=0.95)
    v1 = np.array([1.0, 0.0, 0.0])
    cache.add("q1", v1, "answer one")
    assert cache.lookup(v1) == "answer one"          # identical vector → hit
    v_far = np.array([0.0, 1.0, 0.0])
    assert cache.lookup(v_far) is None                # orthogonal → miss
    assert len(cache) == 1


def test_context_recall():
    assert context_recall(["a.md", "b.md"], ["a.md"]) == 1.0
    assert context_recall(["b.md"], ["a.md"]) == 0.0
    assert context_recall(["x.md"], []) == 1.0        # nothing required → full recall


def test_abstention_correct():
    abstain = "I don't have enough information in the provided documents to answer that."
    assert abstention_correct(abstain, should_abstain=True)
    assert not abstention_correct(abstain, should_abstain=False)
    assert abstention_correct("Compute is $0.000012/vCPU-s.", should_abstain=False)


@pytest.mark.integration
def test_end_to_end_retrieval_requires_ingest():
    """Smoke test for the retrieval stack; requires `make ingest` to have run first."""
    from src.retrieval import get_retriever

    ctx = get_retriever().retrieve("What is the transformer architecture based on?")
    assert ctx.chunks
    # The most relevant doc for this query should be the transformer article.
    assert any("transformer" in c.source for c in ctx.chunks)

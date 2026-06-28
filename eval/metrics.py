"""Retrieval and answer metrics computed without an LLM (cheap, deterministic, CI-friendly)."""

from __future__ import annotations


def context_recall(retrieved_sources: list[str], expected_sources: list[str]) -> float:
    """Fraction of expected source docs that appear in the retrieved context."""
    if not expected_sources:
        return 1.0  # nothing required (abstain cases)
    hits = sum(1 for s in expected_sources if s in retrieved_sources)
    return hits / len(expected_sources)


def abstained(answer: str) -> bool:
    return "don't have enough information" in answer.lower()


def abstention_correct(answer: str, should_abstain: bool) -> bool:
    """Did the agent abstain exactly when it should have? Guards against hallucination."""
    return abstained(answer) == should_abstain

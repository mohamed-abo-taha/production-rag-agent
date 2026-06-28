"""The agentic answer loop: retrieve → (self-correct if weak) → generate grounded, cited answer.

The "agent" here is deliberately small and legible rather than a black-box framework:
  1. Retrieve hybrid context for the question.
  2. If the reranker says context is weak, rewrite the query and retrieve again (self-correction).
  3. Generate an answer constrained to the retrieved context, with inline [source] citations.
  4. If the model still cannot answer from context, it abstains instead of hallucinating.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from .cache import embed_query, get_cache
from .config import get_settings
from .llm import get_llm
from .observability import record_query
from .retrieval import RetrievedContext, get_retriever

ANSWER_SYSTEM = (
    "You answer strictly from the provided context. "
    "Cite the source filename in square brackets after each claim, e.g. [transformer.md]. "
    "If the context does not contain the answer, reply exactly: "
    "\"I don't have enough information in the provided documents to answer that.\" "
    "Never use outside knowledge. Be concise."
)

REWRITE_SYSTEM = (
    "Rewrite the user's question into a single, keyword-rich search query that would retrieve "
    "the relevant passages. Return only the rewritten query, no preamble."
)


@dataclass
class AgentAnswer:
    answer: str
    sources: list[str]
    contexts: list[dict] = field(default_factory=list)
    self_corrected: bool = False
    cached: bool = False
    latency_ms: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0


def _format_context(ctx: RetrievedContext) -> str:
    blocks = []
    for c in ctx.chunks:
        blocks.append(f"[{c.source}] (relevance={c.score:.2f})\n{c.text}")
    return "\n\n---\n\n".join(blocks)


def _rewrite_query(question: str) -> str:
    llm = get_llm()
    result = llm.complete(question, system=REWRITE_SYSTEM, temperature=0.0, max_tokens=128)
    return result.text.strip() or question


def answer_question(question: str) -> AgentAnswer:
    settings = get_settings()
    start = time.perf_counter()

    # --- Semantic cache ---
    qvec = embed_query(question)
    cache = get_cache()
    if settings.cache_enabled:
        hit = cache.lookup(qvec)
        if hit is not None:
            latency = (time.perf_counter() - start) * 1000
            record_query(latency_ms=latency, cached=True, input_tokens=0, output_tokens=0, abstained=False)
            return AgentAnswer(answer=hit, sources=[], cached=True, latency_ms=latency)

    retriever = get_retriever()
    ctx = retriever.retrieve(question)

    # --- Self-correction: if context is weak, rewrite the query and retry once. ---
    self_corrected = False
    if ctx.weak and settings.max_self_corrections > 0 and settings.has_llm:
        rewritten = _rewrite_query(question)
        if rewritten and rewritten.lower() != question.lower():
            retry = retriever.retrieve(rewritten)
            if not retry.weak or (retry.chunks and ctx.chunks and retry.chunks[0].score > ctx.chunks[0].score):
                ctx = retry
                self_corrected = True

    # --- Generate grounded answer ---
    llm = get_llm()
    context_str = _format_context(ctx) if ctx.chunks else "(no relevant context found)"
    prompt = f"Context:\n{context_str}\n\nQuestion: {question}\n\nAnswer (cite sources):"
    result = llm.complete(prompt, system=ANSWER_SYSTEM, model=settings.resolved_answer_model, temperature=0.0)

    sources = sorted({c.source for c in ctx.chunks})
    abstained = "don't have enough information" in result.text.lower()

    latency = (time.perf_counter() - start) * 1000
    answer = AgentAnswer(
        answer=result.text.strip(),
        sources=sources,
        contexts=[{"source": c.source, "score": c.score, "text": c.text} for c in ctx.chunks],
        self_corrected=self_corrected,
        cached=False,
        latency_ms=latency,
        input_tokens=result.input_tokens,
        output_tokens=result.output_tokens,
    )

    if settings.cache_enabled and not abstained:
        cache.add(question, qvec, answer.answer)
    record_query(
        latency_ms=latency,
        cached=False,
        input_tokens=result.input_tokens,
        output_tokens=result.output_tokens,
        abstained=abstained,
    )
    return answer

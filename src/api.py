"""FastAPI serving layer. Exposes /ask, /health, and /stats."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .agent import answer_question
from .config import get_settings
from .llm import LLMNotConfigured
from .observability import snapshot

app = FastAPI(
    title="Production RAG Agent",
    version="0.1.0",
    description="Hybrid-retrieval, self-correcting RAG agent with citations and live metrics.",
)


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3, examples=["How is Nimbus billing calculated?"])


class ContextOut(BaseModel):
    source: str
    score: float
    text: str


class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    contexts: list[ContextOut]
    self_corrected: bool
    cached: bool
    latency_ms: float
    input_tokens: int
    output_tokens: int


@app.get("/health")
def health() -> dict:
    s = get_settings()
    return {
        "status": "ok",
        "provider": s.provider,
        "llm_configured": s.has_llm,
        "answer_model": s.resolved_answer_model,
    }


@app.get("/stats")
def stats() -> dict:
    return snapshot()


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest) -> AskResponse:
    try:
        result = answer_question(req.question)
    except LLMNotConfigured as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except FileNotFoundError as e:
        raise HTTPException(status_code=409, detail=f"{e} (have you ingested the corpus?)") from e
    return AskResponse(
        answer=result.answer,
        sources=result.sources,
        contexts=[ContextOut(**c) for c in result.contexts],
        self_corrected=result.self_corrected,
        cached=result.cached,
        latency_ms=round(result.latency_ms, 1),
        input_tokens=result.input_tokens,
        output_tokens=result.output_tokens,
    )

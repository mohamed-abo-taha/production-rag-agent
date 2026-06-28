"""Central configuration. All knobs live here so behaviour is reproducible and CI can override via env."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- LLM provider selection ---
    # "auto" picks groq if GROQ_API_KEY is set, else anthropic if ANTHROPIC_API_KEY is set.
    llm_provider: str = Field(default="auto", alias="LLM_PROVIDER")  # auto | groq | anthropic

    # --- Anthropic Claude ---
    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")
    answer_model: str = Field(default="claude-sonnet-4-6", alias="ANSWER_MODEL")
    judge_model: str = Field(default="claude-opus-4-8", alias="JUDGE_MODEL")

    # --- Groq (OpenAI-compatible, serves open models like Llama) ---
    groq_api_key: str = Field(default="", alias="GROQ_API_KEY")
    groq_answer_model: str = Field(default="llama-3.3-70b-versatile", alias="GROQ_ANSWER_MODEL")
    # Judge: use the strongest available model so the grader is at least as capable as the student.
    groq_judge_model: str = Field(default="llama-3.3-70b-versatile", alias="GROQ_JUDGE_MODEL")

    max_tokens: int = Field(default=1024, alias="MAX_TOKENS")

    # --- Embeddings / reranking (local, no API key required) ---
    embedding_model: str = Field(default="sentence-transformers/all-MiniLM-L6-v2", alias="EMBEDDING_MODEL")
    reranker_model: str = Field(default="cross-encoder/ms-marco-MiniLM-L-6-v2", alias="RERANKER_MODEL")

    # --- Vector store (Qdrant, local on-disk by default — no server needed) ---
    qdrant_path: str = Field(default=str(PROJECT_ROOT / "data" / "qdrant"), alias="QDRANT_PATH")
    qdrant_url: str = Field(default="", alias="QDRANT_URL")  # set to run against a Qdrant server instead
    qdrant_api_key: str = Field(default="", alias="QDRANT_API_KEY")  # for authenticated Qdrant Cloud
    collection_name: str = Field(default="documents", alias="COLLECTION_NAME")

    # --- Chunking ---
    chunk_size: int = Field(default=900, alias="CHUNK_SIZE")          # characters
    chunk_overlap: int = Field(default=150, alias="CHUNK_OVERLAP")

    # --- Retrieval ---
    dense_top_k: int = Field(default=10, alias="DENSE_TOP_K")
    bm25_top_k: int = Field(default=10, alias="BM25_TOP_K")
    rerank_top_k: int = Field(default=4, alias="RERANK_TOP_K")        # context passages handed to the LLM
    min_rerank_score: float = Field(default=-4.0, alias="MIN_RERANK_SCORE")  # below this, context is "weak"

    # --- Agent ---
    max_self_corrections: int = Field(default=1, alias="MAX_SELF_CORRECTIONS")

    # --- Semantic cache ---
    cache_enabled: bool = Field(default=True, alias="CACHE_ENABLED")
    cache_similarity_threshold: float = Field(default=0.95, alias="CACHE_SIMILARITY_THRESHOLD")

    # --- Paths ---
    corpus_dir: str = Field(default=str(PROJECT_ROOT / "data" / "corpus"), alias="CORPUS_DIR")

    @property
    def provider(self) -> str:
        """Resolve the active provider, honouring an explicit override or auto-detecting by key."""
        if self.llm_provider != "auto":
            return self.llm_provider
        if self.groq_api_key:
            return "groq"
        if self.anthropic_api_key:
            return "anthropic"
        return "none"

    @property
    def has_llm(self) -> bool:
        return self.provider in {"groq", "anthropic"}

    @property
    def resolved_answer_model(self) -> str:
        return self.groq_answer_model if self.provider == "groq" else self.answer_model

    @property
    def resolved_judge_model(self) -> str:
        return self.groq_judge_model if self.provider == "groq" else self.judge_model


@lru_cache
def get_settings() -> Settings:
    return Settings()

"""Streamlit UI for the Production RAG Agent.

Run from the project root:
    streamlit run streamlit_app.py

Lets you ask questions, see the grounded answer with citations, inspect the exact retrieved
passages and their rerank scores, and watch live latency / cost / cache metrics — the same
signals exposed by the API's /stats endpoint.
"""

from __future__ import annotations

import streamlit as st

from src.config import get_settings
from src.ingest import chunks_path, ingest
from src.llm import LLMNotConfigured
from src.observability import snapshot

st.set_page_config(page_title="RAG Agent", page_icon="🔎", layout="wide")


@st.cache_resource(show_spinner="Loading embedding + reranker models (first run only)...")
def warm_retriever():
    """Load the retriever (and its models) once per process, reused across reruns."""
    from src.retrieval import get_retriever

    return get_retriever()


def index_exists() -> bool:
    return chunks_path().exists()


# --------------------------------------------------------------------------------------
# Sidebar — status, settings, live metrics
# --------------------------------------------------------------------------------------
settings = get_settings()

with st.sidebar:
    st.header("⚙️ Status")
    if settings.has_llm:
        st.success(f"Provider: **{settings.provider}**")
        st.caption(f"Answer model: `{settings.resolved_answer_model}`")
    else:
        st.error("No LLM key configured. Add GROQ_API_KEY or ANTHROPIC_API_KEY to .env")

    st.divider()
    st.subheader("Retrieval")
    st.caption(
        f"dense top-k = {settings.dense_top_k} · BM25 top-k = {settings.bm25_top_k} · "
        f"rerank → {settings.rerank_top_k} passages"
    )
    st.caption("Hybrid (dense + BM25) → cross-encoder rerank → grounded answer")

    st.divider()
    st.subheader("📊 Live metrics")
    stats = snapshot()
    if stats["total_queries"]:
        c1, c2 = st.columns(2)
        c1.metric("Queries", stats["total_queries"])
        c2.metric("Cache hit rate", f"{stats['cache_hit_rate']*100:.0f}%")
        c1.metric("p95 latency", f"{stats['latency_ms']['p95']:.0f} ms")
        c2.metric("Abstention rate", f"{stats['abstention_rate']*100:.0f}%")
        st.caption(f"Est. spend this session: ${stats['est_cost_usd']:.4f}")
    else:
        st.caption("Ask a question to populate metrics.")


# --------------------------------------------------------------------------------------
# Main panel
# --------------------------------------------------------------------------------------
st.title("🔎 Production RAG Agent")
st.caption(
    "Hybrid retrieval · cross-encoder reranking · self-correction · grounded citations · "
    "abstains instead of hallucinating."
)

# Guard: index must be built first.
if not index_exists():
    st.warning("The document index hasn't been built yet.")
    if st.button("📥 Build index now (ingests data/corpus)"):
        with st.spinner("Ingesting corpus and building the index..."):
            n = ingest()
        st.success(f"Indexed {n} chunks. Reloading...")
        st.rerun()
    st.stop()

if not settings.has_llm:
    st.stop()

# Warm the retriever (loads models once).
retriever = warm_retriever()

EXAMPLES = [
    "What is retrieval-augmented generation?",
    "What mechanism is the transformer based on?",
    "What is reinforcement learning?",
    "What is the capital of Australia?",  # abstention trap (outside the ML corpus)
]

st.write("**Try an example:**")
cols = st.columns(len(EXAMPLES))
for i, ex in enumerate(EXAMPLES):
    if cols[i].button(ex, use_container_width=True):
        st.session_state["question"] = ex

question = st.text_input(
    "Ask a question about machine learning / AI:",
    value=st.session_state.get("question", ""),
    placeholder="e.g. How does self-attention work? What is overfitting?",
)

if question:
    from src.agent import answer_question

    try:
        with st.spinner("Retrieving + reasoning..."):
            result = answer_question(question)
    except LLMNotConfigured as e:
        st.error(str(e))
        st.stop()
    except Exception as e:  # noqa: BLE001 — surface provider/runtime errors cleanly, not as a traceback
        msg = str(e)
        if "rate_limit" in msg.lower() or "429" in msg:
            st.error(
                "⏳ **Groq rate limit reached.** The free tier has a daily token budget per model "
                "(resets at 00:00 UTC).\n\n"
                "**Fixes:** switch `GROQ_ANSWER_MODEL` in `.env` to a model with remaining quota "
                "(e.g. `llama-3.1-8b-instant`), wait for the daily reset, or upgrade your Groq plan."
            )
        else:
            st.error(f"Something went wrong calling the LLM:\n\n```\n{msg}\n```")
        st.stop()

    # Answer
    st.markdown("### Answer")
    st.markdown(result.answer)

    # Status chips
    chips = []
    if result.cached:
        chips.append("⚡ cached")
    if result.self_corrected:
        chips.append("🔁 self-corrected")
    if "don't have enough information" in result.answer.lower():
        chips.append("🛑 abstained (no hallucination)")
    if chips:
        st.caption(" · ".join(chips))

    # Metadata row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Latency", f"{result.latency_ms:.0f} ms")
    m2.metric("Sources", len(result.sources))
    m3.metric("Input tokens", result.input_tokens)
    m4.metric("Output tokens", result.output_tokens)

    if result.sources:
        st.caption("Cited sources: " + ", ".join(f"`{s}`" for s in result.sources))

    # Retrieved context inspector
    if result.contexts:
        with st.expander(f"🔍 Retrieved context ({len(result.contexts)} passages, reranked)"):
            for i, c in enumerate(result.contexts, 1):
                st.markdown(f"**{i}. `{c['source']}`** — rerank score `{c['score']:.2f}`")
                st.text(c["text"][:700] + ("…" if len(c["text"]) > 700 else ""))
                st.divider()

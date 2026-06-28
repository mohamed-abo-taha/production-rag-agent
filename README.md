# Production RAG Agent with Automated Eval Harness

A production-grade, self-correcting retrieval-augmented generation (RAG) agent with a
**pluggable LLM backend** (Groq / Llama or Anthropic Claude — auto-detected from your API key),
**hybrid retrieval + cross-encoder reranking**, **semantic caching**, live
**observability**, and — the centrepiece — an **automated LLM-as-judge evaluation harness that
runs as a CI quality gate** to block hallucination regressions before they ship.

> Most RAG demos stop at "embed → vector search → prompt." The hard, hireable parts are the ones
> that make a model *trustworthy in production*: retrieval that actually finds the right context,
> an agent that abstains instead of hallucinating, and an eval pipeline that proves it — and
> catches regressions automatically. That's what this project is about.

📖 **Deep dive:** [BLOG.md](BLOG.md) — design, the retrieval A/B benchmark, and the real tradeoffs.
🚀 **Deploy it:** [DEPLOY.md](DEPLOY.md) — free Streamlit Cloud / Render / Fly + Qdrant Cloud.

![Architecture](docs/architecture.svg)

---

## Architecture

```
                                  ┌──────────────────────────────────────────┐
   POST /ask  ──────────────────► │              Agent loop (agent.py)        │
                                  │                                            │
                                  │  1. Semantic cache lookup (cache.py)       │
                                  │        hit ─► return cached answer         │
                                  │                                            │
                                  │  2. Hybrid retrieval (retrieval.py)        │
                                  │       ┌─────────────┐   ┌──────────────┐   │
                                  │       │ Dense / kNN │   │  BM25 sparse │   │
                                  │       │  (Qdrant)   │   │ (rank_bm25)  │   │
                                  │       └──────┬──────┘   └──────┬───────┘   │
                                  │              └──── fuse ───────┘           │
                                  │            Cross-encoder rerank            │
                                  │                                            │
                                  │  3. Weak context?  ─► rewrite query,       │
                                  │       retrieve again (self-correction)     │
                                  │                                            │
                                  │  4. Claude generates grounded, cited       │
                                  │       answer — or abstains                 │
                                  └──────────────────┬─────────────────────────┘
                                                     │
                              records latency / tokens / cost / abstention
                                     (observability.py → GET /stats)

   Offline / CI:  eval/evaluate.py  ──►  runs the live agent over eval/golden_set.jsonl
                                         scores faithfulness, relevance, correctness,
                                         context-recall, abstention  ──►  CI gate
```

## Why these choices (the talking points for interviews)

| Decision | Rationale |
|---|---|
| **Hybrid retrieval (dense + BM25)** | Vector search misses exact tokens (IDs, error codes like `NIMBUS_RATE_LIMITED`); BM25 misses paraphrases. Fusing both raises recall. |
| **Cross-encoder reranking** | Bi-encoder similarity is coarse. A cross-encoder re-scores query–passage pairs jointly for much higher *context precision* — fewer distractor passages reach the LLM. |
| **Self-correction on weak context** | When the reranker's top score is below threshold, the agent rewrites the query and retries instead of answering on bad context. |
| **Abstention over hallucination** | The system prompt forces "I don't have enough information" when context is insufficient. Measured explicitly by the eval harness. |
| **Automated eval as a CI gate** | Quality is a *number with a threshold*, not a vibe. Regressions fail the build. This is the differentiator. |
| **Semantic cache** | Near-duplicate questions skip retrieval + generation → lower p95 latency and cost. |
| **Local embeddings/reranker** | No API key needed for the retrieval stack, so it's fully testable offline and in CI. |

## Quickstart

```bash
# 1. Install
pip install -r requirements.txt           # or: make install

# 2. Add ONE provider key (answering + eval need it; retrieval/ingest don't)
cp .env.example .env                       # set GROQ_API_KEY (Groq/Llama) or ANTHROPIC_API_KEY (Claude)

# 3. Build the index (downloads the embedding model on first run)
python -m scripts.run_ingest              # or: make ingest

# 4a. Ask questions from the CLI
python -m scripts.demo "What mechanism is the transformer based on?"

# 4b. ...or launch the Streamlit UI
streamlit run streamlit_app.py            # or: make ui  → http://localhost:8501

# 4c. ...or serve the API
python -m scripts.run_api                 # open http://localhost:8000/docs

# 5. Run the evaluation harness (the headline feature)
python -m eval.evaluate                   # or: make eval
```

### Example

```bash
$ python -m scripts.demo "Which paper introduced the transformer architecture?"
======================================================================
Q: Which paper introduced the transformer architecture?
----------------------------------------------------------------------
The transformer architecture was introduced in the 2017 paper
"Attention Is All You Need". [transformer.md]
----------------------------------------------------------------------
sources=['transformer.md']  latency=520ms
======================================================================

$ python -m scripts.demo "What is the capital of Australia?"
... I don't have enough information in the provided documents to answer that.
# ^ abstains on out-of-domain questions instead of guessing — exactly what the eval harness checks.
```

## Two evaluations: answer quality + retrieval quality

Answer quality and retrieval quality are different things, so there are two harnesses.

### A) Answer eval — LLM-as-judge (`make eval`)

`python -m eval.evaluate` runs the live agent over every question in
[`eval/golden_set.jsonl`](eval/golden_set.jsonl) (**31 questions incl. 3 "should-abstain" traps**)
and scores each answer, then enforces thresholds:

| Metric | What it measures | Gate |
|---|---|---|
| `faithfulness` | Every claim grounded in retrieved context (LLM judge) | ≥ 0.85 |
| `answer_relevance` | Answer addresses the question (LLM judge) | ≥ 0.85 |
| `answer_correctness` | Matches the reference answer (LLM judge) | ≥ 0.80 |
| `abstention_correct` | Abstains exactly when it should (deterministic) | ≥ 0.90 |

It writes `eval/report.json` and **exits non-zero if any gate fails**, so the GitHub Actions
workflow in [`.github/workflows/eval.yml`](.github/workflows/eval.yml) blocks merges that regress
quality. Add an example to the golden set → it's covered forever.

Latest run — Groq `llama-3.1-8b-instant`, 319-doc corpus, 31 questions:

| faithfulness | answer_relevance | answer_correctness | abstention_correct |
|---|---|---|---|
| **0.904** ✅ | **0.913** ✅ | **0.855** ✅ | **1.000** ✅ |

`QUALITY GATE PASSED`. (On Llama-3.3-70B the same harness scores ~1.0 / 0.96 / 0.93 / 1.0 — the
model-capability tradeoff, documented in [BLOG.md](BLOG.md).)

### B) Retrieval eval — IR metrics, A/B of strategies (`make retrieval-eval`)

`python -m eval.retrieval_eval` is an offline, LLM-free benchmark over **212 labelled queries** that
quantifies *why* the pipeline is built the way it is — `recall@k` and `NDCG@k` for four retrieval
strategies, on the real **319-doc / 6,254-chunk** corpus:

| strategy | recall@1 | recall@3 | NDCG@10 | ms/query |
|---|---|---|---|---|
| BM25 (sparse only) | 0.901 | 0.953 | 0.950 | **8** |
| dense (vector only) | 0.962 | 1.000 | 0.983 | 24 |
| hybrid (dense + BM25) | 0.962 | 1.000 | 0.983 | 31 |
| **hybrid + rerank** (production) | **0.972** | 0.995 | **0.988** | 95 |

Reranking delivers the best **recall@1 (0.972)** and **NDCG@10 (0.988)** — it puts the right document
first most often, which is what matters when only the top passages reach the LLM. BM25 alone is
weakest; hybrid preserves dense's recall while adding keyword-match safety. Full interpretation +
the latency tradeoff in [BLOG.md](BLOG.md).

## Observability

`GET /stats` returns live metrics: total queries, **p50/p95/p99 latency**, cache hit rate,
abstention rate, token usage, and an estimated USD cost. Swap the in-process collector in
`observability.py` for Prometheus or Arize Phoenix without touching the agent.

## Project layout

```
src/
  config.py         pydantic settings — every knob, env-overridable
  llm.py            provider-agnostic LLM wrapper (Groq/Claude) + token accounting
  embeddings.py     sentence-transformer embedder + cross-encoder reranker
  vector_store.py   Qdrant wrapper (local on-disk or hosted server)
  ingest.py         load → chunk (paragraph-aware, overlapping) → embed → index
  retrieval.py      hybrid dense+BM25 fusion → rerank → weak-context flag
  cache.py          semantic cache over query embeddings
  agent.py          retrieve → self-correct → grounded cited answer / abstain
  observability.py  latency/cost/abstention metrics + structured logs
  api.py            FastAPI: /ask /health /stats
eval/
  golden_set.jsonl    labelled Q&A incl. abstention traps
  evaluate.py         LLM-as-judge answer harness + CI quality gate
  retrieval_eval.py   IR benchmark: recall@k / NDCG@k, A/B of strategies
  metrics.py          deterministic metric helpers
scripts/
  fetch_wikipedia.py  reproducible corpus pipeline (Wikipedia API)
  run_ingest.py · run_api.py · demo.py
streamlit_app.py    interactive UI
data/corpus/        real Wikipedia ML/AI articles (swap in your own)
docs/architecture.svg
BLOG.md · DEPLOY.md · render.yaml · Procfile · Dockerfile · docker-compose.yml
tests/              unit tests (run without an API key)
```

## Swap in your own data

Drop `.md`/`.txt` files into `data/corpus/`, delete the old golden set, write a few labelled
Q&A pairs for your domain, and re-run `make ingest && make eval`. The whole pipeline is
domain-agnostic.

## Tech stack

Python · Groq (Llama) / Anthropic Claude · sentence-transformers · Qdrant · rank-bm25 · FastAPI · Docker · GitHub Actions · pytest

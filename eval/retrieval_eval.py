"""Offline retrieval benchmark — an A/B/C/D comparison of four retrieval strategies.

Computes recall@k and NDCG@k (LLM-free, deterministic, fast) for:

    A. dense        — vector / kNN search only
    B. bm25         — sparse keyword search only
    C. hybrid       — dense + BM25 candidates fused
    D. hybrid+rerank — fused candidates re-scored by the cross-encoder (the production config)

Why this matters: it quantifies *why* the production pipeline is built the way it is. Instead of
asserting "hybrid + reranking is better," it shows the recall@k / NDCG@k lift with numbers, at the
real corpus scale, and reports per-query latency for each strategy.

Query set (labelled, document-level relevance):
  * one "What is <title>?" query per corpus document (auto-generated, scales with the corpus)
  * plus the curated conceptual questions from the golden set
Run:
    python -m eval.retrieval_eval --max-doc-queries 200
"""

from __future__ import annotations

import argparse
import json
import math
import time
from collections import OrderedDict
from pathlib import Path

import numpy as np

from src.config import get_settings
from src.embeddings import get_embedder, get_reranker
from src.ingest import load_chunks
from src.retrieval import _tokenize
from src.vector_store import get_vector_store

CANDIDATE_POOL = 30      # chunks pulled from each base retriever before mapping to docs
DOC_CUTOFF = 10          # evaluate ranking over the top-N distinct docs
KS = [1, 3, 5, 10]
GOLDEN_PATH = Path(__file__).parent / "golden_set.jsonl"
REPORT_PATH = Path(__file__).parent / "retrieval_report.json"


def _doc_title(md_path: Path) -> str:
    first = md_path.read_text(encoding="utf-8").splitlines()[0]
    return first.lstrip("# ").strip() or md_path.stem


def build_queries(max_doc_queries: int) -> list[dict]:
    """One 'What is <title>?' query per document + the curated golden-set questions."""
    corpus = Path(get_settings().corpus_dir)
    files = sorted(corpus.glob("*.md"))
    # Deterministic, even sample across the corpus so we don't just test the first N alphabetically.
    if len(files) > max_doc_queries:
        step = len(files) / max_doc_queries
        files = [files[int(i * step)] for i in range(max_doc_queries)]

    queries = [{"query": f"What is {_doc_title(f)}?", "relevant": {f.name}} for f in files]

    if GOLDEN_PATH.exists():
        for line in GOLDEN_PATH.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if not row.get("should_abstain") and row.get("expected_sources"):
                queries.append({"query": row["question"], "relevant": set(row["expected_sources"])})
    return queries


class Strategies:
    def __init__(self) -> None:
        self.embedder = get_embedder()
        self.reranker = get_reranker()
        self.store = get_vector_store()
        self.chunks = load_chunks()
        self.text_by_id = {c.id: c.text for c in self.chunks}
        self.src_by_id = {c.id: c.source for c in self.chunks}
        from rank_bm25 import BM25Okapi

        self.ids = [c.id for c in self.chunks]
        self.bm25 = BM25Okapi([_tokenize(c.text) for c in self.chunks])

    def dense_ids(self, query: str) -> list[str]:
        qv = self.embedder.embed_one(query)
        return [h.id for h in self.store.search(qv, top_k=CANDIDATE_POOL)]

    def bm25_ids(self, query: str) -> list[str]:
        scores = self.bm25.get_scores(_tokenize(query))
        order = np.argsort(scores)[::-1][:CANDIDATE_POOL]
        return [self.ids[i] for i in order]

    @staticmethod
    def _fuse(a: list[str], b: list[str]) -> list[str]:
        out: list[str] = []
        for cid in a + b:
            if cid not in out:
                out.append(cid)
        return out

    def ranked_docs(self, strategy: str, query: str) -> list[str]:
        if strategy == "dense":
            cand = self.dense_ids(query)
        elif strategy == "bm25":
            cand = self.bm25_ids(query)
        elif strategy == "hybrid":
            cand = self._fuse(self.dense_ids(query), self.bm25_ids(query))
        elif strategy == "hybrid+rerank":
            cand = self._fuse(self.dense_ids(query), self.bm25_ids(query))
            scores = self.reranker.score(query, [self.text_by_id[c] for c in cand])
            cand = [c for c, _ in sorted(zip(cand, scores), key=lambda x: x[1], reverse=True)]
        else:
            raise ValueError(strategy)
        # Map chunk ranking → distinct document ranking (first occurrence wins).
        docs = list(OrderedDict((self.src_by_id[c], None) for c in cand).keys())
        return docs[:DOC_CUTOFF]


def recall_at_k(ranked: list[str], relevant: set[str], k: int) -> float:
    return 1.0 if any(d in relevant for d in ranked[:k]) else 0.0


def ndcg_at_k(ranked: list[str], relevant: set[str], k: int) -> float:
    dcg = sum(1.0 / math.log2(i + 2) for i, d in enumerate(ranked[:k]) if d in relevant)
    ideal = sum(1.0 / math.log2(i + 2) for i in range(min(len(relevant), k)))
    return dcg / ideal if ideal else 0.0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-doc-queries", type=int, default=200)
    args = ap.parse_args()

    print("Loading retrieval stack...", flush=True)
    strat = Strategies()
    queries = build_queries(args.max_doc_queries)
    print(f"Corpus: {len(set(strat.src_by_id.values()))} docs / {len(strat.chunks)} chunks", flush=True)
    print(f"Benchmark queries: {len(queries)}\n", flush=True)

    strategies = ["dense", "bm25", "hybrid", "hybrid+rerank"]
    agg = {s: {f"recall@{k}": 0.0 for k in KS} | {f"ndcg@{k}": 0.0 for k in (5, 10)} for s in strategies}
    latency = {s: 0.0 for s in strategies}

    n = 0
    for q in queries:
        if not q["query"].strip() or q["query"].strip() == "What is ?":
            continue  # skip degenerate queries from malformed docs
        try:
            ranked_by_strategy = {}
            timing = {}
            for s in strategies:
                t0 = time.perf_counter()
                ranked_by_strategy[s] = strat.ranked_docs(s, q["query"])
                timing[s] = (time.perf_counter() - t0) * 1000
        except Exception:
            continue  # one bad query shouldn't sink the whole benchmark
        for s in strategies:
            latency[s] += timing[s]
            for k in KS:
                agg[s][f"recall@{k}"] += recall_at_k(ranked_by_strategy[s], q["relevant"], k)
            for k in (5, 10):
                agg[s][f"ndcg@{k}"] += ndcg_at_k(ranked_by_strategy[s], q["relevant"], k)
        n += 1

    print(f"Scored {n} queries (skipped {len(queries) - n}).\n", flush=True)
    for s in strategies:
        for key in agg[s]:
            agg[s][key] = round(agg[s][key] / n, 3)
        latency[s] = round(latency[s] / n, 1)

    # Pretty table
    cols = [f"recall@{k}" for k in KS] + ["ndcg@5", "ndcg@10", "ms/query"]
    print(f"{'strategy':<16}" + "".join(f"{c:>11}" for c in cols))
    print("-" * (16 + 11 * len(cols)))
    for s in strategies:
        row = "".join(f"{agg[s][c]:>11.3f}" for c in cols[:-1]) + f"{latency[s]:>11.1f}"
        print(f"{s:<16}{row}")

    REPORT_PATH.write_text(
        json.dumps({"n_queries": n, "n_docs": len(set(strat.src_by_id.values())),
                    "n_chunks": len(strat.chunks), "metrics": agg, "latency_ms": latency}, indent=2),
        encoding="utf-8",
    )
    print(f"\nReport written to {REPORT_PATH}")


if __name__ == "__main__":
    main()

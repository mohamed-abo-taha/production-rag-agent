"""Lightweight, dependency-free observability: in-process metrics + structured query logs.

Tracks the numbers that matter for a serving system — latency percentiles, cache hit rate,
token cost, and abstention rate — and exposes them via the API's /stats endpoint. Swap this for
Prometheus/Arize Phoenix in a real deployment; the interface (record_query/snapshot) stays the same.
"""

from __future__ import annotations

import json
import threading
from collections import deque
from dataclasses import dataclass, field

# Approx Anthropic pricing ($ per 1M tokens) for a rough live cost estimate. Tune to your model.
_PRICE_PER_MTok = {"input": 3.0, "output": 15.0}


@dataclass
class Metrics:
    total_queries: int = 0
    cache_hits: int = 0
    abstentions: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    _latencies: deque = field(default_factory=lambda: deque(maxlen=1000))
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def record(self, latency_ms: float, cached: bool, input_tokens: int, output_tokens: int, abstained: bool) -> None:
        with self._lock:
            self.total_queries += 1
            if cached:
                self.cache_hits += 1
            if abstained:
                self.abstentions += 1
            self.input_tokens += input_tokens
            self.output_tokens += output_tokens
            self._latencies.append(latency_ms)

    def _pct(self, p: float) -> float:
        if not self._latencies:
            return 0.0
        ordered = sorted(self._latencies)
        idx = min(len(ordered) - 1, int(round(p / 100 * (len(ordered) - 1))))
        return round(ordered[idx], 1)

    def snapshot(self) -> dict:
        with self._lock:
            est_cost = (
                self.input_tokens / 1_000_000 * _PRICE_PER_MTok["input"]
                + self.output_tokens / 1_000_000 * _PRICE_PER_MTok["output"]
            )
            return {
                "total_queries": self.total_queries,
                "cache_hit_rate": round(self.cache_hits / self.total_queries, 3) if self.total_queries else 0.0,
                "abstention_rate": round(self.abstentions / self.total_queries, 3) if self.total_queries else 0.0,
                "latency_ms": {
                    "p50": self._pct(50),
                    "p95": self._pct(95),
                    "p99": self._pct(99),
                },
                "tokens": {"input": self.input_tokens, "output": self.output_tokens},
                "est_cost_usd": round(est_cost, 4),
            }


_metrics = Metrics()


def record_query(*, latency_ms: float, cached: bool, input_tokens: int, output_tokens: int, abstained: bool) -> None:
    _metrics.record(latency_ms, cached, input_tokens, output_tokens, abstained)
    # Structured log line — pipe to your log aggregator in production.
    print(
        json.dumps(
            {
                "event": "query",
                "latency_ms": round(latency_ms, 1),
                "cached": cached,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "abstained": abstained,
            }
        ),
        flush=True,
    )


def snapshot() -> dict:
    return _metrics.snapshot()

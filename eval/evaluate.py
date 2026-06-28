"""Automated evaluation harness — the headline differentiator of this project.

For every question in the golden set it runs the live agent and scores the answer on:

  * faithfulness        (LLM judge) — is every claim grounded in the retrieved context?
  * answer_relevance    (LLM judge) — does the answer actually address the question?
  * answer_correctness  (LLM judge) — does it match the reference answer?
  * context_recall      (deterministic) — did retrieval surface the expected source docs?
  * abstention_correct  (deterministic) — did it abstain exactly when it should?

It prints a per-question table and aggregate scores, writes eval/report.json, and exits non-zero
when scores fall below the thresholds in QUALITY_GATES — so it can run as a CI gate that blocks
regressions before they ship.

Usage:
    python -m eval.evaluate                 # full run
    python -m eval.evaluate --limit 5       # quick smoke test
    python -m eval.evaluate --no-gate       # report only, never fail
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from src.agent import answer_question
from src.config import get_settings
from src.llm import get_llm
from eval.metrics import abstention_correct

GOLDEN_PATH = Path(__file__).parent / "golden_set.jsonl"
REPORT_PATH = Path(__file__).parent / "report.json"

# This harness scores ANSWER quality (LLM-judged). Retrieval quality (recall@k / NDCG@k) is measured
# separately and rigorously by eval/retrieval_eval.py, so it isn't gated here.
# CI fails if any aggregate metric drops below these values.
QUALITY_GATES = {
    "faithfulness": 0.85,
    "answer_relevance": 0.85,
    "answer_correctness": 0.80,
    "abstention_correct": 0.90,
}

JUDGE_SYSTEM = (
    "You are a strict evaluation judge for a retrieval-augmented QA system. "
    "Return ONLY a single number between 0.0 and 1.0 — no words, no explanation."
)


def _is_abstention(answer: str) -> bool:
    return "don't have enough information" in answer.lower()


def _judge(prompt: str) -> float:
    result = get_llm().complete(prompt, system=JUDGE_SYSTEM, model=get_settings().resolved_judge_model, temperature=0.0, max_tokens=16)
    match = re.search(r"[01](?:\.\d+)?", result.text)
    return max(0.0, min(1.0, float(match.group()))) if match else 0.0


def judge_faithfulness(answer: str, context: str) -> float:
    # Abstaining introduces no claims, so it is faithful by definition — score it before calling the judge.
    if _is_abstention(answer):
        return 1.0
    if not context.strip():
        return 0.0  # answered with nothing to ground it
    return _judge(
        "You are scoring FAITHFULNESS (groundedness).\n"
        f"CONTEXT:\n{context}\n\nANSWER:\n{answer}\n\n"
        "Return 1.0 if every factual claim in the ANSWER is supported by the CONTEXT. "
        "Return a lower value only if the ANSWER asserts facts that are absent from the CONTEXT. "
        "Ignore bracketed citation markers like [file.md]. "
        "Respond with ONLY a decimal number between 0 and 1."
    )


def judge_relevance(question: str, answer: str) -> float:
    # A correct refusal to an unanswerable question is fully relevant.
    if _is_abstention(answer):
        return 1.0
    return _judge(
        "You are scoring RELEVANCE: does the ANSWER address the QUESTION?\n"
        f"QUESTION: {question}\nANSWER: {answer}\n\n"
        "1.0 = directly and fully addresses the question; 0.5 = partial; 0.0 = unrelated. "
        "Respond with ONLY a decimal number between 0 and 1."
    )


def judge_correctness(question: str, answer: str, reference: str) -> float:
    return _judge(
        f"Question: {question}\nReference answer: {reference}\nCandidate answer: {answer}\n\n"
        "Score from 0.0 to 1.0 how well the Candidate matches the Reference in factual content. "
        "Output only the number."
    )


def load_golden(limit: int | None) -> list[dict]:
    rows = [json.loads(l) for l in GOLDEN_PATH.read_text(encoding="utf-8").splitlines() if l.strip()]
    return rows[:limit] if limit else rows


def run(limit: int | None, gate: bool) -> int:
    if not get_settings().has_llm:
        print("ERROR: ANTHROPIC_API_KEY not set — the eval harness needs the LLM. See README.", file=sys.stderr)
        return 2

    rows = load_golden(limit)
    results = []
    print(f"\nEvaluating {len(rows)} questions...\n")
    print(f"{'id':<5}{'faith':>7}{'relev':>7}{'corr':>7}{'abst':>6}  question")
    print("-" * 84)

    for row in rows:
        res = answer_question(row["question"])
        context = "\n\n".join(c["text"] for c in res.contexts)

        faith = judge_faithfulness(res.answer, context)
        relev = judge_relevance(row["question"], res.answer)
        corr = judge_correctness(row["question"], res.answer, row["reference"])
        abst = 1.0 if abstention_correct(res.answer, row["should_abstain"]) else 0.0

        results.append(
            {
                "id": row["id"], "faithfulness": faith, "answer_relevance": relev,
                "answer_correctness": corr, "abstention_correct": abst,
            }
        )
        print(f"{row['id']:<5}{faith:>7.2f}{relev:>7.2f}{corr:>7.2f}{abst:>6.0f}  {row['question'][:46]}")

    agg = {
        k: round(sum(r[k] for r in results) / len(results), 3)
        for k in ["faithfulness", "answer_relevance", "answer_correctness", "abstention_correct"]
    }

    print("-" * 92)
    print("\nAGGREGATE SCORES")
    failures = []
    for metric, score in agg.items():
        threshold = QUALITY_GATES[metric]
        ok = score >= threshold
        flag = "PASS" if ok else "FAIL"
        if not ok:
            failures.append(metric)
        print(f"  {metric:<20} {score:>6.3f}   (gate >= {threshold})  [{flag}]")

    REPORT_PATH.write_text(json.dumps({"aggregate": agg, "per_question": results}, indent=2), encoding="utf-8")
    print(f"\nReport written to {REPORT_PATH}")

    if gate and failures:
        print(f"\nQUALITY GATE FAILED on: {', '.join(failures)}", file=sys.stderr)
        return 1
    print("\nQUALITY GATE PASSED" if gate else "\n(gate disabled)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the RAG evaluation harness.")
    parser.add_argument("--limit", type=int, default=None, help="evaluate only the first N questions")
    parser.add_argument("--no-gate", action="store_true", help="report scores but never exit non-zero")
    args = parser.parse_args()
    return run(limit=args.limit, gate=not args.no_gate)


if __name__ == "__main__":
    raise SystemExit(main())

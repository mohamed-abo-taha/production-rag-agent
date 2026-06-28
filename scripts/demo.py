"""Interactive command-line demo. Ask the agent questions and see citations + latency.

Usage:
    python -m scripts.demo                       # interactive REPL
    python -m scripts.demo "How is billing calculated?"   # one-shot
"""

from __future__ import annotations

import sys

from src.agent import answer_question
from src.config import get_settings
from src.observability import snapshot


def ask_and_print(question: str) -> None:
    res = answer_question(question)
    print("\n" + "=" * 70)
    print(f"Q: {question}")
    print("-" * 70)
    print(res.answer)
    print("-" * 70)
    tags = []
    if res.cached:
        tags.append("CACHED")
    if res.self_corrected:
        tags.append("SELF-CORRECTED")
    meta = f"sources={res.sources}  latency={res.latency_ms:.0f}ms"
    if tags:
        meta += "  [" + ", ".join(tags) + "]"
    print(meta)
    print("=" * 70)


def main() -> None:
    if not get_settings().has_llm:
        print("ANTHROPIC_API_KEY not set. Copy .env.example to .env and add your key.")
        sys.exit(1)

    if len(sys.argv) > 1:
        ask_and_print(" ".join(sys.argv[1:]))
        return

    print("RAG agent demo. Ask a question about Nimbus Cloud (Ctrl-C to quit).")
    print("Try: 'How is Compute billed?'  or  'What database engines does Nimbus support?'\n")
    try:
        while True:
            q = input("> ").strip()
            if not q:
                continue
            ask_and_print(q)
    except (KeyboardInterrupt, EOFError):
        print("\n\nSession stats:")
        for k, v in snapshot().items():
            print(f"  {k}: {v}")
        print("Bye.")


if __name__ == "__main__":
    main()

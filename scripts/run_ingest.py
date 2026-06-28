"""Ingest the corpus into the vector store and build the BM25 index.

Usage:
    python -m scripts.run_ingest
"""

from __future__ import annotations

import time

from src.ingest import ingest


def main() -> None:
    start = time.perf_counter()
    print("Ingesting corpus (downloading embedding model on first run)...")
    n = ingest()
    elapsed = time.perf_counter() - start
    print(f"Indexed {n} chunks in {elapsed:.1f}s. Ready to serve.")


if __name__ == "__main__":
    main()

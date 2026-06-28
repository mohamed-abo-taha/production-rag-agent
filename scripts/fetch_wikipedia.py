"""Reproducible data pipeline: build a large AI/ML corpus from Wikipedia.

Gathers article titles from several Wikipedia categories (and their subcategories), then downloads
the plain-text extract of each into data/corpus/. Uses only the standard library (urllib) so it has
no extra dependencies. Re-run any time to refresh / grow the corpus.

    python -m scripts.fetch_wikipedia --max-articles 700

The 8 hand-curated "core" articles used by the LLM-judged golden set are preserved under their
original filenames and skipped here, so the answer-eval references stay valid.
"""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://en.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "rag-agent-portfolio-demo/1.0 (educational)"}

# Broad AI/ML/CS categories — gives a coherent, on-topic knowledge base.
CATEGORIES = [
    "Machine learning",
    "Machine learning algorithms",
    "Artificial intelligence",
    "Artificial neural networks",
    "Deep learning",
    "Natural language processing",
    "Computer vision",
    "Statistical classification",
    "Cluster analysis",
    "Data mining",
    "Computational statistics",
    "Supervised learning",
    "Unsupervised learning",
    "Reinforcement learning",
    "Large language models",
]

SKIP_PREFIXES = ("List of", "Category:", "Template:", "Wikipedia:", "Portal:", "File:", "Help:")

# Core articles already curated for the golden answer-eval (keep their original slugs; don't duplicate).
CORE_TITLES = {
    "Machine learning",
    "Deep learning",
    "Transformer (deep learning architecture)",
    "Large language model",
    "Retrieval-augmented generation",
    "Neural network (machine learning)",
    "Natural language processing",
    "Reinforcement learning",
}


def _get(params: dict) -> dict:
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def gather_titles(categories: list[str], per_cat: int = 600) -> list[str]:
    titles: dict[str, bool] = {}
    for cat in categories:
        cmcontinue, got = None, 0
        while got < per_cat:
            params = {
                "action": "query", "list": "categorymembers", "cmtitle": f"Category:{cat}",
                "cmlimit": "500", "cmtype": "page", "format": "json",
            }
            if cmcontinue:
                params["cmcontinue"] = cmcontinue
            try:
                data = _get(params)
            except Exception:
                break
            for m in data.get("query", {}).get("categorymembers", []):
                t = m["title"]
                if not t.startswith(SKIP_PREFIXES) and t not in CORE_TITLES:
                    titles[t] = True
                got += 1
            cmcontinue = data.get("continue", {}).get("cmcontinue")
            if not cmcontinue:
                break
            time.sleep(0.1)
        print(f"  [{cat}] unique titles so far: {len(titles)}", flush=True)
    return list(titles.keys())


def slugify(title: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", title.lower()).strip("-")
    return (s[:80] or "article")


def fetch_extract(title: str, retries: int = 2) -> tuple[str | None, str]:
    params = {
        "action": "query", "prop": "extracts", "explaintext": "1", "redirects": "1",
        "format": "json", "titles": title,
    }
    for attempt in range(retries + 1):
        try:
            data = _get(params)
            pages = data.get("query", {}).get("pages", {})
            for _, p in pages.items():
                return p.get("title"), p.get("extract", "") or ""
            return None, ""
        except Exception:
            if attempt < retries:
                time.sleep(1.5 * (attempt + 1))  # back off, then retry
            else:
                return None, ""
    return None, ""


def _write_article(corpus: Path, real_title: str, text: str, seen: set, min_chars: int) -> bool:
    if not text or len(text) < min_chars:
        return False
    slug = slugify(real_title)
    if slug in seen:
        return False
    seen.add(slug)
    url = "https://en.wikipedia.org/wiki/" + urllib.parse.quote(real_title.replace(" ", "_"))
    (corpus / f"{slug}.md").write_text(f"# {real_title}\n\nSource: Wikipedia ({url})\n\n{text}", encoding="utf-8")
    return True


def batched_fetch(corpus: Path, categories: list[str], max_articles: int, min_chars: int) -> int:
    """Fast path: use a category generator + prop=extracts to pull up to 20 full extracts per request."""
    written, seen = 0, set()
    for cat in categories:
        gcmcontinue = None
        while written < max_articles:
            params = {
                "action": "query", "format": "json", "redirects": "1",
                "generator": "categorymembers", "gcmtitle": f"Category:{cat}",
                "gcmtype": "page", "gcmlimit": "20",
                "prop": "extracts", "explaintext": "1", "exlimit": "20",
            }
            if gcmcontinue:
                params["gcmcontinue"] = gcmcontinue
            try:
                data = _get(params)
            except Exception:
                time.sleep(1.0)
                break
            for _, p in data.get("query", {}).get("pages", {}).items():
                title = p.get("title", "")
                if title.startswith(SKIP_PREFIXES) or title in CORE_TITLES:
                    continue
                if _write_article(corpus, title, p.get("extract", "") or "", seen, min_chars):
                    written += 1
                    if written % 25 == 0:
                        print(f"  wrote {written} articles...", flush=True)
            cont = data.get("continue", {})
            gcmcontinue = cont.get("gcmcontinue")
            if not gcmcontinue:
                break
            time.sleep(0.2)
        print(f"  [{cat}] running total: {written}", flush=True)
    return written


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-articles", type=int, default=700)
    ap.add_argument("--min-chars", type=int, default=800, help="skip stubs shorter than this")
    ap.add_argument("--pace", type=float, default=0.5, help="seconds between requests (gentle = no throttling)")
    args = ap.parse_args()

    corpus = Path(__file__).resolve().parent.parent / "data" / "corpus"
    corpus.mkdir(parents=True, exist_ok=True)

    # Pre-seed 'seen' with existing files so re-runs add NEW articles instead of redoing work.
    seen = {f.stem for f in corpus.glob("*.md")}
    start_count = len(seen)

    print("Gathering candidate titles from AI/ML categories...", flush=True)
    titles = gather_titles(CATEGORIES)
    print(f"Collected {len(titles)} titles. Have {start_count} docs; fetching toward {args.max_articles} new...", flush=True)

    written = 0
    for title in titles:
        if written >= args.max_articles:
            break
        time.sleep(args.pace)  # steady, gentle pacing avoids Wikipedia throttling
        real_title, text = fetch_extract(title)
        if _write_article(corpus, real_title or title, text, seen, args.min_chars):
            written += 1
            if written % 25 == 0:
                print(f"  wrote {written} new articles (corpus now ~{start_count + written})...", flush=True)

    total_files = len(list(corpus.glob("*.md")))
    print(f"Done. Wrote {written} new articles. Corpus now has {total_files} documents.", flush=True)


if __name__ == "__main__":
    main()

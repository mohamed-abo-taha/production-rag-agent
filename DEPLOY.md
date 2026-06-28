# Deploying the RAG Agent

Three deployment paths, cheapest first. All serve the **Streamlit demo**; the FastAPI service
(`src/api.py`) deploys the same way — just change the start command.

> **Memory reality:** the embedding + reranker models (PyTorch) need ~1.5–2 GB RAM. A 512 MB free
> instance will OOM. Either use a small **paid** instance (~$7/mo) **or** keep the live corpus small
> (tens of articles, not the 50k-chunk benchmark corpus, which is for local scale testing). The
> two big knobs are **corpus size** (how much you ingest) and **instance RAM**.

---

## Option A — Streamlit Community Cloud (free, easiest) ⭐

Best for a free, shareable demo URL with a **small corpus** (≤ ~50 articles).

1. Push this repo to GitHub.
2. Keep `data/corpus/` small for the hosted demo (e.g. the 8 core articles). Big corpora won't fit
   in the free tier's RAM.
3. Go to <https://share.streamlit.io> → **New app** → pick your repo → main file `streamlit_app.py`.
4. **Advanced settings → Secrets**, paste:
   ```toml
   GROQ_API_KEY = "gsk_..."
   LLM_PROVIDER = "groq"
   GROQ_ANSWER_MODEL = "llama-3.1-8b-instant"
   ```
5. Deploy. On first load click **"Build index now"** (the app ingests `data/corpus/` into a local
   on-disk index). Done — you have a public URL for your resume.

---

## Option B — Render (Docker, ~$7/mo, more headroom)

Best when you want the **larger corpus** and a always-on instance. Uses [`render.yaml`](render.yaml).

1. Push to GitHub.
2. <https://dashboard.render.com> → **New → Blueprint** → select your repo. Render reads `render.yaml`.
3. Set the **`GROQ_API_KEY`** env var in the dashboard (marked `sync: false`, so it's not committed).
4. Deploy. The Docker build runs `scripts.run_ingest`, baking the index into the image, then starts
   Streamlit. Health check: `/_stcore/health`.

The `starter` plan (2 GB) handles a few hundred articles. For the full 50k-chunk corpus, bump the
plan and/or use Qdrant Cloud (below) so the vector index lives outside the instance.

---

## Option C — Railway / Fly.io

Both build the `Dockerfile` directly.

- **Railway:** New Project → Deploy from repo. Add `GROQ_API_KEY` as a variable. The `Procfile`
  start command is picked up automatically (or set it to the `dockerCommand` from `render.yaml`).
- **Fly.io:** `fly launch` (detects the Dockerfile) → `fly secrets set GROQ_API_KEY=gsk_...` → `fly deploy`.
  Give it a 2 GB VM: `fly scale memory 2048`.

---

## Optional — Qdrant Cloud (managed vector DB)

To run a large index without fattening your app instance (and to allow concurrent readers — the
local on-disk Qdrant is single-process):

1. Create a free cluster at <https://cloud.qdrant.io> (1 GB free).
2. Set env vars on your host:
   ```
   QDRANT_URL=https://<your-cluster>.qdrant.io:6333
   QDRANT_API_KEY=<key>     # see note below
   ```
3. Run `python -m scripts.run_ingest` once (locally or as a one-off job) to populate the cluster.

> `src/vector_store.py` passes `QDRANT_API_KEY` through automatically, so authenticated Qdrant Cloud
> clusters work out of the box — just set the two env vars above.

---

## Secrets hygiene

- `.env` is git-ignored — never commit your key. Set secrets in the host's dashboard/secret store.
- Rotate any key that has been shared in plaintext (e.g. pasted into a chat or screenshot).

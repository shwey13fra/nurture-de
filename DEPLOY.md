# Deploying the thin slice to HuggingFace Spaces

A public URL an expat can type a question into. Free CPU tier, Gradio, Chroma in-container. The
**only** production swap is the reranker (offloaded to Jina — the local CPU cross-encoder is
86–89 % of query latency). Everything else runs as-is; `graph.py` is untouched (the hosted reranker
is injected at startup by `app.py`).

The steps below are **yours to run** — they involve creating an account, generating API keys, and
entering secrets, which the assistant cannot do.

## 0. Get the two keys (never commit these)

- **A NEW Anthropic key, scoped to this deployment, with a spend limit** set in the Anthropic
  console (`https://console.anthropic.com` → API keys + Limits). Do **not** reuse your dev key.
- **A Jina key** — free, 10M tokens (`https://jina.ai/reranker`). (Fallback: a Cohere key, if
  verification below fails on Jina.)

## 1. Verify cross-lingual recovery BEFORE anything is public

The headline finding (English question → German answer, recovered by reranking) must still hold on
the hosted reranker. Run locally first:

```bash
# put the key in the gitignored .env (or export it); it is never committed
echo "JINA_API_KEY=jina_..." >> .env
set -a; . ./.env; set +a          # or: export JINA_API_KEY=...
python src/tools/verify_hosted_rerank.py
```

Expect `✅ all 4 cross-lingual cases recovered fam_mutterschutz into the top-4`. If it fails,
switch to Cohere (`export RERANK_PROVIDER=cohere COHERE_API_KEY=...`) and re-run. **Do not ship a
reranker that fails this.**

## 2. Create the Space

HuggingFace → **New Space** → SDK **Gradio**, hardware **CPU basic (free)**. This gives a git repo
and a public `*.hf.space` URL.

## 3. Put the code + the built index in the Space repo

The Space needs the app, the `src/` package, the runtime requirements, and the **prebuilt index**
(committing it avoids a ~45-minute E5 embed at container start — measured). Copy into the Space repo:

```
app.py
requirements.txt          <- copy from requirements-space.txt in this repo
src/                       <- the whole package (graph.py, retrieval.py, generate.py,
                              hosted_rerank.py, tools/, prompts/, vendor/)
data/bm25.pkl              <- your local built index  (~0.7 MB)
chroma_db/                 <- your local built index  (~7 MB; total index ~8 MB)
```

Your local `chroma_db/` + `data/bm25.pkl` already exist (built by `python src/index.py`). They are
gitignored in *this* repo on purpose; add them to the **Space** repo directly.

> **Portability note:** the committed Chroma index was built on Windows; the Space runs Linux. Same
> `chromadb==1.5.9` and same x86 architecture make it very likely to load as-is. If the Space logs
> a Chroma load error or `chroma count != 225`, the robust fix is to rebuild the index once on the
> Space (or on any Linux box) with `python src/index.py` and commit that — slow, but one-time.

Add the Space README front-matter (HuggingFace reads this to configure the Space):

```yaml
---
title: NurtureDE
emoji: 🤰
colorFrom: green
colorTo: gray
sdk: gradio
app_file: app.py
pinned: false
---
```

## 4. Set the secrets (Space Settings → Variables and secrets)

Add as **secrets** (not variables — secrets are hidden), never in code:

- `ANTHROPIC_API_KEY` = the new scoped key from step 0
- `JINA_API_KEY` = your Jina key   (or `COHERE_API_KEY` + `RERANK_PROVIDER=cohere` if you fell back)

`app.py` reads these from the environment; the Space injects secrets as env vars.

## 5. Push, then verify on the LIVE url

Once the Space builds and starts, confirm on the public URL:

1. The four scenario questions answer end to end (e.g. *"When does Mutterschutz start if I'm due
   2027-03-15 and employed?"*).
2. A medical question (*"Is cramping at 30 weeks normal?"*) **refuses** and refers to a doctor/112.
3. An English question about a German-only topic (*"When do I have to tell my employer I'm
   pregnant?"*) answers **cross-lingually**, citing `fam_mutterschutz`.
4. Note the **query latency** on the deployed instance — with the reranker offloaded, generation
   should now dominate (the Phase-11 prediction for the production topology). Record it.

Then update the README: replace the deploy-skip section with the live link (the costed reasoning
for pgvector + a hosted embedder stays as roadmap).

## Cost & data

- **~$0.05–0.06 / query**, dominated by Opus generation; Jina rerank ~$0.001 (free within 10M
  tokens); Haiku judge calls ~$0.008. Under the $0.10 line, so Opus stays. (Sonnet would cut
  generation ~4× if you want more headroom.)
- **Stores nothing** — Gradio telemetry is disabled (`analytics_enabled=False`), no logging, no
  persistence. Stated on the page (GDPR Art. 9 special-category inputs).

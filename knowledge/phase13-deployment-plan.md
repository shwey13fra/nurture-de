# Phase 13 — deployment: the costed plan (scoped, priced, then SHIPPED)

> **Correction (2026-08-16, after deploying):** the "$0 idle / free CPU tier" figures below were
> wrong — **HuggingFace now requires PRO ($9/mo) for Gradio Spaces**; only Static Spaces are free,
> and Static can't run this Python backend. So the real cost is **~$0.05/query + $9/mo PRO**, not
> $0 idle. The thin slice was deployed anyway (live: https://huggingface.co/spaces/Shwey13/nurture-de),
> with one extra change not in this plan: the built index is shipped as **text** and rebuilt in
> the container at startup, because HF rejects binary files in normal git. The plan below is kept
> as written (with this correction on top) rather than silently edited.

---


Written so the research survives the decision to skip (PM-10: a plan not on disk is a memory).
Deployment was **scoped and costed, then deliberately skipped on value grounds** — see the
BUILD_JOURNAL Phase-13 entry. This is the plan that would be executed if/when a live URL is wanted;
kept as a costed roadmap item, not a half-built system.

## The narrow first slice (smallest deployment → working public URL)

The corpus embeds **once, offline**, so only the short *query* embeds at runtime — which runs fine
on CPU. And a free CPU tier with 16 GB RAM fits E5-large fp16 (1.1 GB). So the **only** thing that
must be offloaded is the **reranker** (the 86–89 % latency sink); everything else runs in one
container from the committed index.

1. **HF Spaces (free CPU, 2 vCPU / 16 GB)** running the existing graph as a FastAPI app with a
   minimal query form; public `*.hf.space` URL, Git-push deploy, sleeps when idle.
2. **E5 query-embed + Chroma + BM25 in-container** — index built from committed
   `data/chunks.jsonl` / `data/bm25.pkl` at startup (no external vector store).
3. **One swap:** `retrieval.Reranker` → a hosted reranker API behind the existing interface (the
   seam already exists). This is the piece that makes the demo interactive (sub-second vs ~2 min).
4. **Generation** via the Anthropic API (Opus, or Sonnet to cut per-query cost).
5. **Roadmap, NOT in the slice:** Chroma → Supabase **pgvector** (only needed for multi-instance /
   scale), a **hosted embedder** (only needed to shed the CPU E5 + ~17 s cold start), auth, rate
   limiting, monitoring.

## Cost (researched 2026-08; pay-per-call, near-zero idle)

| piece | choice | cost |
|---|---|---|
| App + E5 query-embed + Chroma + BM25 | HF Spaces free CPU (16 GB fits E5 fp16) | **$0/mo**, public URL, idle-sleep |
| Reranker (the 86–89 % latency) | Cohere Rerank 3.5 (~$0.002/search) **or** Jina reranker ($0.05/M tok, 10M free ≈ hundreds of queries) | **~$0.002/query**, $0 idle |
| Vector store | Chroma in-container | $0 (Supabase/pgvector not needed for one instance) |
| Generation | Anthropic API (Opus ~$0.05–0.08/query; Sonnet cheaper) | per-query only |

**Stand-up ≈ $0. Idle ≈ $0/mo. Per-query ≈ $0.05–0.08, almost entirely generation.** A portfolio
demo (100–500 queries/mo) ≈ **$5–40/mo**, controllable to ~$1–5 with Sonnet. Cost was **not** the
constraint.

**A loop it would have closed:** with rerank offloaded, generation becomes the dominant latency —
validating the Phase-11 prediction that generation dominates in the *production* topology (on the
CPU dev box, rerank dominated at 86–89 %; see the Phase-11 addendum).

**Sources (2026-08):** [Cohere Rerank pricing](https://www.aipricing.guru/cohere-pricing/) ·
[Jina reranker/embeddings](https://www.linkstartai.com/en/agents/jina) ·
[Supabase pricing](https://uibakery.io/blog/supabase-pricing) ·
[HF Spaces free tier](https://huggingface.co/docs/hub/en/spaces-zerogpu).

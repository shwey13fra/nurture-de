"""Phase-13 thin slice — a public URL an expat can type a question into. HuggingFace Spaces,
Gradio, free CPU. NOT a production system: a question and an answer, nothing else.

The ONLY change from the local system is the reranker: it is offloaded to a hosted API (the local
CPU cross-encoder is 86–89 % of query latency). Everything else runs in-container — E5 query
embedding, Chroma, BM25 from the committed index — and the LangGraph workflow is unchanged; the
hosted reranker is injected into its module global at startup, so graph.py is not touched.

Stores nothing: no query logging, no analytics, no persistence (inputs can include pregnancy
status and employment — GDPR Art. 9 special-category data; not storing removes most of the duty).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("GRADIO_ANALYTICS_ENABLED", "False")   # store nothing: kill Gradio telemetry

_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(_ROOT / "src"))
sys.path.insert(0, str(_ROOT / "src" / "tools"))

import gradio as gr          # noqa: E402
import graph                 # noqa: E402  (the existing workflow, unchanged)
from hosted_rerank import make_reranker   # noqa: E402
from space_index import ensure_index      # noqa: E402

REPO_URL = "https://github.com/shwey13fra/nurture-de"

# rebuild Chroma + BM25 from the committed TEXT index (no binary files shipped; seconds, no E5 embed)
ensure_index()

# --- the one swap: inject the hosted reranker into the graph's module global (graph.py untouched) ---
graph._reranker = make_reranker()

EMPLOYMENT = ["(prefer not to say)", "employed", "self-employed", "student",
              "civil-servant", "marginally-employed", "not-employed"]
INSURANCE = ["(prefer not to say)", "statutory", "private", "family-insured"]


def _profile(employment: str, insurance: str) -> dict:
    p = {}
    if employment and not employment.startswith("("):
        p["employment_status"] = employment
    if insurance and not insurance.startswith("("):
        p["insurance_type"] = insurance
    return p


def _render(state: dict) -> str:
    resp = state.get("response") or {}
    kind = resp.get("kind")
    if kind == "safe_referral":
        return "### 🩺 A question for a professional\n\n" + resp["message"]
    if kind == "request_attributes":
        return "### One more thing\n\n" + resp["message"]
    if kind == "plan":
        plan = resp["plan"]
        out = ["### Answer\n", plan.get("summary", ""), ""]
        tl = plan.get("timeline") or []
        if tl:
            out.append("**Dates (computed in Python from your due date):**")
            for t in tl:
                out.append(f"- **{t['event'].replace('_', ' ')}: {t['date']}** — {t.get('rule','')}")
            out.append("")
        cites = plan.get("citations") or []
        if cites:
            out.append("**Sources** (this is what the citation is grounded in):")
            for c in cites:
                out.append(f"- {c.get('authority','?')} "
                           f"({c.get('authority_tier','?')}) · verified {c.get('last_verified','?')} "
                           f"· `{c.get('chunk_id','?')}`")
        nc = plan.get("needs_professional_confirmation") or []
        if nc:
            out.append("\n**Confirm with the authority that decides:** " + ", ".join(nc))
        if resp.get("issues"):
            out.append("\n_Note: the citation check flagged a claim to double-check against the "
                       "source above._")
        return "\n".join(out)
    return "Something went wrong producing an answer. Please try rephrasing."


def answer(question: str, employment: str, insurance: str) -> str:
    question = (question or "").strip()
    if not question:
        return "Type a question above — for example, *When does Mutterschutz start if I'm due 15 March and employed?*"
    try:
        state = graph.run(question, profile=_profile(employment, insurance))
        return _render(state)
    except Exception as e:   # noqa: BLE001 — never crash the box; report plainly
        return f"Sorry — the assistant hit an error handling that question.\n\n`{type(e).__name__}: {e}`"


BANNER = """
> ## ⚠️ Not medical or legal advice
> NurtureDE reports what **official German sources** say and cites them. It **never** decides what
> applies to *you*, never states your eligibility, and **refuses medical questions** — see a
> doctor, a midwife (*Hebamme*), or call **112** in an emergency.
"""

SUBLINE = (
    "A **prototype** over ~22 official German sources (federal portals, statutory-insurer pages) "
    "about pregnancy, *Mutterschutz*, and family benefits. Ask in English or German. "
    f"[Source code and build journal →]({REPO_URL})"
)

PRIVACY = (
    "🔒 **Stores nothing.** No query logging, no analytics, no accounts. Your inputs (which can "
    "include pregnancy status and employment — GDPR Art. 9 special-category data) are used only to "
    "answer this one request and are never saved."
)

with gr.Blocks(title="NurtureDE", analytics_enabled=False) as demo:
    gr.Markdown(BANNER)
    gr.Markdown(SUBLINE)
    with gr.Row():
        q = gr.Textbox(label="Your question", lines=2,
                       placeholder="When do I have to tell my employer I'm pregnant?")
    with gr.Row():
        emp = gr.Dropdown(EMPLOYMENT, value="(prefer not to say)", label="Employment (optional)")
        ins = gr.Dropdown(INSURANCE, value="(prefer not to say)", label="Insurance (optional)")
    btn = gr.Button("Ask", variant="primary")
    out = gr.Markdown()
    btn.click(answer, inputs=[q, emp, ins], outputs=out)
    q.submit(answer, inputs=[q, emp, ins], outputs=out)
    gr.Markdown(PRIVACY)

def _warm() -> None:
    # warm E5 (and confirm the hosted reranker) so the first real query isn't a cold load.
    # runs in a BACKGROUND thread so it never blocks the web port from binding — on the Space's
    # first boot the E5 download (~2.2 GB) must not delay startup past HuggingFace's health check.
    try:
        graph._retrieve_reranked("Mutterschutz", None)
    except Exception:   # noqa: BLE001 — warmup is best-effort
        pass


import threading   # noqa: E402
threading.Thread(target=_warm, daemon=True).start()   # module-level: runs however HF invokes app.py

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.getenv("PORT", "7860")))

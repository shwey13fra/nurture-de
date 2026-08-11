"""NurtureDE — MCP server (Phase 10).

Why MCP: the N x M problem. Without a shared protocol, every model host (Claude Desktop, Claude
Code, an IDE, ...) needs a bespoke integration with every capability (our retriever, our timeline
tool, ...) — N hosts x M capabilities of glue. MCP collapses that: we write ONE server, and any
MCP client can consume it. This server exposes the NurtureDE corpus + the Phase-9 timeline tool
over stdio.

Three primitives:
  - tools     (actions the model may call): search, timeline, term explanation
  - resource  (readable data): the topic-coverage list
  - prompt    (a reusable template): the expat pregnancy-plan workflow

SDK: the modern `mcp` v2 line (MCPServer). Run:  python mcp_server.py   (stdio transport)
Inspect:  npx @modelcontextprotocol/inspector python mcp_server.py

Scope (same as everywhere in this project): the tools report what official sources SAY and always
return chunk_ids so a client can cite. They never state a benefit amount and never determine that
a specific person is eligible for anything. Medical questions are steered away, in the tool
descriptions themselves — the description is what the model reads to decide whether to call a tool.
"""

from __future__ import annotations

import json
import sys
import threading
from collections import Counter
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(_ROOT / "src"))

from mcp.server import MCPServer          # noqa: E402  (v2 high-level server)

from retrieval import Retriever           # noqa: E402  (reuse existing retrieval — do not reimplement)
from tools.timeline import calculate_timeline  # noqa: E402  (Phase-9 deterministic tool)

mcp = MCPServer(
    name="germany-family-support",
    version="0.1.0",
    instructions=(
        "Official-source information for people living in Germany navigating pregnancy, "
        "maternity protection (Mutterschutz), maternity and parental benefits, and birth "
        "registration. Tools return cited excerpts (with chunk_ids) and deterministic dates. "
        "They report what sources say; they never decide eligibility, never state a benefit "
        "amount, and never answer medical questions — those go to a doctor or midwife."
    ),
)


# --- warmed retriever singleton -------------------------------------------------------------
# The E5 embedder + BM25 index take ~15-17s to load on the first query. Warm them in a daemon
# thread at startup so the MCP handshake stays instant; a search that arrives before warm-up
# finishes simply blocks on the same lock and then returns (it never hangs indefinitely).
# NB: model-load logging goes to STDERR (verified) — stdout is the JSON-RPC channel and must
# stay clean on the stdio transport.
_retriever: Retriever | None = None
_rlock = threading.Lock()


def _get_retriever() -> Retriever:
    global _retriever
    with _rlock:
        if _retriever is None:
            print("[germany-family-support] loading retrieval models…", file=sys.stderr, flush=True)
            _retriever = Retriever()
            print("[germany-family-support] retrieval ready.", file=sys.stderr, flush=True)
    return _retriever


threading.Thread(target=_get_retriever, daemon=True).start()


def _excerpt(text: str, limit: int) -> str:
    s = " ".join(text.split())
    return s if len(s) <= limit else s[:limit].rstrip() + " …"


# --- tools ----------------------------------------------------------------------------------
@mcp.tool()
def search_official_information(
    query: str,
    topic: str | None = None,
    user_type: str | None = None,
    insurance_type: str | None = None,
    language: str | None = None,
) -> str:
    """Searches official German government and health-portal documents about pregnancy, maternity
    protection (Mutterschutz), maternity and parental benefits (Mutterschaftsgeld, Elterngeld,
    Elternzeit), prenatal care, midwives (Hebammen), and birth registration (Standesamt). Returns
    ranked excerpts, each with the issuing authority, the authority tier (federal / statutory-
    insurer / land), the date the source was last verified, and the chunk_id so the answer can be
    cited.

    Use this for questions about German rules, entitlements, deadlines, forms, and processes — and
    for figuring out which official body holds a given fact. Do NOT use it for medical questions
    (symptoms, pain, bleeding, medication, whether something is normal or an emergency, or
    interpreting a test result): those must go to a doctor or midwife, not this corpus. Everything
    returned is source text to be summarised and cited — never a determination of what applies to a
    specific person, and never a benefit amount stated as advice.

    Args:
        query: The question or keywords, in English or German. The index is cross-lingual, so an
            English question is matched against German sources and vice-versa.
        topic: Optional filter, e.g. 'maternity-protection', 'parental-leave',
            'family-benefits-overview'. See the germany-family-support://topics resource for the
            available topics and how many documents each has.
        user_type: Optional filter by situation: 'employed', 'self-employed', 'student',
            'civil-servant', 'marginally-employed'. Documents that apply to everyone are always
            included alongside the filtered ones.
        insurance_type: Optional filter: 'statutory', 'private', 'family-insured'.
        language: Optional filter for the source language: 'de' or 'en'.
    """
    filters = {k: v for k, v in (("topic", topic), ("user_type", user_type),
                                 ("insurance_type", insurance_type), ("language", language)) if v}
    hits = _get_retriever().search(query, k=6, filters=filters or None, mode="hybrid")
    if not hits:
        tail = f" with filters {filters}" if filters else ""
        return f"No matching official documents were found for {query!r}{tail}."

    head = f"{len(hits)} excerpt(s) for {query!r}" + (f"  (filters: {filters})" if filters else "")
    out = [head, ""]
    for i, h in enumerate(hits, 1):
        m = h.metadata
        out += [
            f"[{i}] {m.get('authority', '?')} — tier: {m.get('authority_tier', '?')} "
            f"— last verified: {m.get('last_verified_date', '?')}",
            f"    chunk_id: {h.chunk_id}",
            f"    topic: {m.get('topic', '?')} | source: {m.get('source_id', '?')} "
            f"| language: {m.get('language', '?')}",
            f"    {_excerpt(h.text, 700)}",
            "",
        ]
    return "\n".join(out)


@mcp.tool()
def calculate_pregnancy_timeline(
    due_date: str,
    employment_status: str,
    actual_birth_date: str | None = None,
    multiple_birth: bool = False,
    premature: bool = False,
    disability_diagnosed_within_8_weeks: bool = False,
) -> dict[str, Any]:
    """Computes the German maternity-protection (Mutterschutz) timeline from an expected — or
    actual — date of birth, using deterministic Python date arithmetic, NOT a language-model
    estimate. A wrong legal deadline can cost someone a benefit or a job protection, so these dates
    must be calculated, not guessed. Returns the protection start and end dates, the Elterngeld
    application window, the exact rules applied (each with the official source chunk_id), caveats,
    and who must confirm the dates.

    Use this whenever the user asks WHEN their Mutterschutz starts or ends, or by when to apply for
    Elterngeld. Dates only: it never states a benefit amount and never decides eligibility. On bad
    input it returns an {"error": ...} object rather than raising.

    Args:
        due_date: Expected date of birth, ISO 'YYYY-MM-DD'.
        employment_status: 'employed', 'self-employed', 'marginally-employed', 'student',
            'civil-servant', or 'not-employed'.
        actual_birth_date: Optional real birth date ('YYYY-MM-DD') if the child is already born;
            the after-period then follows the early / late rules exactly.
        multiple_birth: True for twins or more — extends the period after birth to 12 weeks.
        premature: True if the birth was medically premature (Frühgeburt). This is a doctor's
            determination, not something this tool decides; pass it in if it is known.
        disability_diagnosed_within_8_weeks: True if a disability was diagnosed in the newborn
            within 8 weeks of birth (12 weeks after birth, on application to the health insurer).
    """
    try:
        return calculate_timeline(
            due_date,
            employment_status,
            actual_birth_date=actual_birth_date,
            multiple_birth=multiple_birth,
            premature=premature,
            disability_diagnosed_within_8_weeks=disability_diagnosed_within_8_weeks,
        )
    except ValueError as e:
        return {"error": str(e)}


@mcp.tool()
def explain_german_administrative_term(term: str, target_language: str = "en") -> str:
    """Explains a specific German administrative or benefits term (for example 'Mutterschutzfrist',
    'Elternzeit', 'Beschäftigungsverbot', 'Mutterpass', 'Beleghebamme', 'Elterngeldstelle') using
    the official corpus, and cites the source. If the term is NOT covered by the corpus, it says so
    plainly and declines — it never invents a definition from general knowledge, because a
    confident wrong definition of a legal term is exactly the failure this project guards against.

    Use this for 'what does <German term> mean?' questions. It returns the corpus passage that
    defines or describes the term, with the issuing authority and the chunk_id. It is not for
    medical terms, and it does not translate whole documents.

    Args:
        term: The German term to explain.
        target_language: Preferred language of the explanation, 'en' or 'de'. The source passage is
            returned in its original language (this tool does not itself translate); the language is
            noted so the caller can translate if needed.
    """
    hits = _get_retriever().search(term, k=5, mode="hybrid")
    needle = term.lower().strip()
    for h in hits:
        hay = (h.text + " " + " ".join(h.metadata.get("heading_path") or [])).lower()
        if needle and needle in hay:
            m = h.metadata
            note = ""
            if (target_language or "en") != m.get("language"):
                note = (f"\n\n(Source is in {m.get('language', '?')}; this tool does not translate "
                        f"— the answer layer does that.)")
            return (
                f"**{term}** — from {m.get('authority', '?')} "
                f"(tier: {m.get('authority_tier', '?')}, last verified {m.get('last_verified_date', '?')}):\n\n"
                f"{_excerpt(h.text, 900)}\n\nchunk_id: {h.chunk_id}{note}"
            )
    return (
        f"I don't have '{term}' in my sources. This corpus covers German pregnancy, Mutterschutz, "
        f"maternity and parental benefits, and birth registration — this term isn't in it, so I "
        f"won't guess. Try search_official_information with related keywords, or ask the relevant "
        f"authority."
    )


# --- resource -------------------------------------------------------------------------------
@mcp.resource("germany-family-support://topics")
def list_topics() -> str:
    """The topics the corpus covers, with the number of source chunks per topic, so a client can
    see where coverage is strong or thin before relying on it."""
    counts: Counter = Counter()
    for line in (_ROOT / "data" / "chunks.jsonl").open(encoding="utf-8"):
        if line.strip():
            counts[json.loads(line).get("topic") or "(untagged)"] += 1
    total = sum(counts.values())
    out = [f"NurtureDE corpus coverage — {total} chunks across {len(counts)} topics:", ""]
    out += [f"  {topic}: {n}" for topic, n in counts.most_common()]
    return "\n".join(out)


# --- prompt ---------------------------------------------------------------------------------
@mcp.prompt()
def prepare_expat_pregnancy_plan(
    due_date: str,
    employment_status: str,
    insurance_type: str,
    language: str = "en",
) -> str:
    """A reusable template that guides the model to build a personalised, fully-cited pregnancy and
    benefits plan for someone living in Germany, using this server's tools."""
    return (
        f"You are helping someone living in Germany prepare for pregnancy and birth. Their "
        f"details: expected birth {due_date}, employment status '{employment_status}', insurance "
        f"'{insurance_type}'. Answer in {language}.\n\n"
        f"Build the plan by USING THE TOOLS, and cite every fact with its authority and "
        f"last-verified date:\n\n"
        f"1. Call calculate_pregnancy_timeline(due_date='{due_date}', "
        f"employment_status='{employment_status}') and report when Mutterschutz starts and ends "
        f"and by when to apply for Elterngeld, with the rule sources it returns.\n"
        f"2. Call search_official_information for: Mutterschutz workplace rules; Mutterschaftsgeld "
        f"and Elterngeld; and birth registration (Standesamt) — using user_type="
        f"'{employment_status}' and insurance_type='{insurance_type}' where it helps.\n"
        f"3. Call explain_german_administrative_term for any German term the reader will meet on a "
        f"form (e.g. Mutterschutzfrist, Elternzeit, Mutterpass).\n\n"
        f"Rules: report what the sources say and cite them; give the German terms alongside plain "
        f"explanations; do NOT tell the person they are eligible for anything and do NOT compute an "
        f"amount — name who decides instead (employer, Krankenkasse, Elterngeldstelle); and for any "
        f"medical question, refer to a doctor or midwife rather than the documents."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")

"""Phase 10 — protocol roundtrip for mcp_server.py (the MCP Inspector's job, headless + portable).

    py tests/test_mcp_server.py

Launches the server over real stdio, initializes, then lists and calls every primitive and
asserts the results. No API key needed (the server itself never calls a model); it does load the
retrieval models once, so this takes ~15-20s. Protocol correctness only — the docstring-as-prompt
routing check (does a model pick the right tool?) is a separate, API-costing probe, recorded in
the Phase-10 journal entry rather than run here.
"""

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters, stdio_client

_REPO = Path(__file__).resolve().parents[1]


def _text(result) -> str:
    return "\n".join(getattr(c, "text", str(c)) for c in (getattr(result, "content", []) or []))


async def _run() -> None:
    params = StdioServerParameters(command=sys.executable, args=[str(_REPO / "mcp_server.py")])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as s:
            await s.initialize()

            tools = {t.name for t in (await s.list_tools()).tools}
            assert tools == {"search_official_information", "calculate_pregnancy_timeline",
                             "explain_german_administrative_term"}, tools
            print("tools OK:", sorted(tools))

            # deterministic tool — no model needed
            r = await s.call_tool("calculate_pregnancy_timeline",
                                  {"due_date": "2027-03-15", "employment_status": "employed"})
            body = _text(r)
            assert '"protection_starts": "2027-02-01"' in body, body
            assert '"protection_ends": "2027-05-10"' in body, body
            print("timeline OK")

            r = await s.call_tool("calculate_pregnancy_timeline",
                                  {"due_date": "not-a-date", "employment_status": "employed"})
            assert '"error"' in _text(r), _text(r)
            print("timeline invalid-input OK")

            r = await s.call_tool("search_official_information",
                                  {"query": "Wann beginnt die Mutterschutzfrist?"})
            assert "chunk_id:" in _text(r), "search missing chunk_id"
            print("search OK")

            r = await s.call_tool("explain_german_administrative_term", {"term": "Mutterschutzfrist"})
            assert "chunk_id:" in _text(r), _text(r)
            r = await s.call_tool("explain_german_administrative_term", {"term": "Bausparvertrag"})
            assert "don't have" in _text(r).lower(), "uncovered term should refuse"
            print("explain-term (covered + refuse) OK")

            uris = [str(x.uri) for x in (await s.list_resources()).resources]
            assert "germany-family-support://topics" in uris, uris
            rr = await s.read_resource("germany-family-support://topics")
            assert "chunks across" in "\n".join(getattr(c, "text", "") for c in rr.contents)
            print("resource OK")

            names = [p.name for p in (await s.list_prompts()).prompts]
            assert "prepare_expat_pregnancy_plan" in names, names
            gp = await s.get_prompt("prepare_expat_pregnancy_plan",
                                    {"due_date": "2027-03-15", "employment_status": "employed",
                                     "insurance_type": "statutory", "language": "en"})
            assert gp.messages, "prompt returned no messages"
            print("prompt OK")

    print("\nALL PRIMITIVES OK")


if __name__ == "__main__":
    asyncio.run(_run())

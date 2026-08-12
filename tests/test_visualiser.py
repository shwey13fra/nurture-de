import sys, unittest
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "src"))

from retrieval import RetrievedChunk, RetrievalTrace          # noqa: E402
from graph import GraphTrace                                  # noqa: E402
from tools.visualiser_serialize import (                      # noqa: E402
    chunk_summary, serialize_retrieval_trace, serialize_graph_trace)


class TestSerialisers(unittest.TestCase):
    def _chunk(self):
        return RetrievedChunk("fam_mutterschutz__x__abc", "text here", 0.4213,
                              {"source_id": "fam_mutterschutz", "language": "de",
                               "authority": "Familienportal", "last_verified_date": "2026-08-03"})

    def test_chunk_summary_picks_display_fields(self):
        s = chunk_summary(self._chunk())
        self.assertEqual(s["source_id"], "fam_mutterschutz")
        self.assertEqual(s["language"], "de")
        self.assertEqual(s["chunk_id"], "fam_mutterschutz__x__abc")
        self.assertEqual(s["score"], 0.4213)
        self.assertNotIn("text", s)          # never ship chunk text to the page

    def test_serialize_retrieval_trace_roundtrips_funnel(self):
        rt = RetrievalTrace(query="q", mode="hybrid")
        rt.final_context = ["a", "b"]
        rt.timings_ms = {"total_ms": 165000.0}
        d = serialize_retrieval_trace(rt)
        self.assertEqual(d["final_context"], ["a", "b"])
        self.assertEqual(d["timings_ms"]["total_ms"], 165000.0)
        self.assertEqual(d["query"], "q")

    def test_serialize_graph_trace_embeds_retrievals(self):
        tr = GraphTrace()
        tr.visit("classify_intent", branch="informational")
        tr.node_timings = [{"node": "classify_intent", "ms": 1900.0}]
        tr.final_node = "verify_citations"
        rt = RetrievalTrace(query="q", mode="hybrid"); rt.final_context = ["a"]
        tr.retrievals.append(rt)
        d = serialize_graph_trace(tr)
        self.assertEqual(d["final_node"], "verify_citations")
        self.assertEqual(d["node_timings"][0]["node"], "classify_intent")
        self.assertEqual(len(d["retrievals"]), 1)
        self.assertEqual(d["retrievals"][0]["final_context"], ["a"])

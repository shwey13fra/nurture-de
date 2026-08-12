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


from tools.visualiser_serialize import answerable_figures, strip_metrics   # noqa: E402
_EVAL = _ROOT / "eval"

class TestEvalFigures(unittest.TestCase):
    def test_baseline_hybrid_rerank_answerable(self):
        f = answerable_figures(_EVAL / "last_run.json", config="hybrid_rerank")
        self.assertEqual(f["n"], 26)
        self.assertEqual(f["pct"], 38)          # 10/26 as-measured
        self.assertEqual(f["recall"], 0.75)

    def test_phase8b_answerable_measured_and_corrected(self):
        m = answerable_figures(_EVAL / "last_run_phase8b.json")
        self.assertEqual(m["n"], 26)
        self.assertEqual(m["pct"], 58)          # 15/26 as-measured
        self.assertEqual(m["recall"], 0.90)
        c = answerable_figures(_EVAL / "last_run_phase8b.json", corrected=True)
        self.assertEqual(c["pct"], 69)          # 18/26 after 5 relabels

    def test_strip_metrics_shape_and_values(self):
        s = strip_metrics()
        self.assertEqual(s["recall"]["before"], 0.75)
        self.assertEqual(s["recall"]["after"], 0.90)
        self.assertEqual(s["behaviour_measured"]["before"], 38)
        self.assertEqual(s["behaviour_measured"]["after"], 58)
        self.assertEqual(s["behaviour_labels_fixed"]["before"], 58)
        self.assertEqual(s["behaviour_labels_fixed"]["after"], 69)
        self.assertEqual(s["cross_lingual_recovery"]["recovered"], 5)
        self.assertEqual(s["cross_lingual_recovery"]["of"], 6)
        for k in ("recall", "behaviour_measured", "behaviour_labels_fixed"):
            self.assertIn("source", s[k])        # every figure names its file


from tools.visualiser_serialize import assemble_hero, inject           # noqa: E402

class TestHeroAndInject(unittest.TestCase):
    def _c(self, cid, sid, lang, score):
        return RetrievedChunk(cid, "t", score, {"source_id": sid, "language": lang})

    def test_assemble_hero_finds_discard_and_recovery(self):
        before = RetrievalTrace(query="q", mode="hybrid")
        before.fused = [{"chunk_id": "tk__0"}, {"chunk_id": "tk__1"}, {"chunk_id": "tk__2"},
                        {"chunk_id": "tk__3"}, {"chunk_id": "x__4"}, {"chunk_id": "x__5"},
                        {"chunk_id": "fam__ans"}]                       # answer at rank 6
        before._chunks = {"tk__0": self._c("tk__0", "tk_maternity_pay", "en", .9),
                          "tk__1": self._c("tk__1", "tk_maternity_pay", "en", .8),
                          "tk__2": self._c("tk__2", "tk_maternity_benefits", "en", .7),
                          "tk__3": self._c("tk__3", "tk_maternity_pay", "en", .6),
                          "fam__ans": self._c("fam__ans", "fam_mutterschutz", "de", .5)}
        after = [self._c("fam__ans", "fam_mutterschutz", "de", .99),
                 self._c("tk__0", "tk_maternity_pay", "en", .5)]
        h = assemble_hero("q", before, after, "fam_mutterschutz", "cut by top-4")
        self.assertEqual(h["before"]["answer_rank"], 6)
        self.assertEqual(h["after"]["answer_rank"], 0)
        self.assertEqual(h["before"]["cutoff"], 4)
        self.assertEqual(h["after"]["items"][0]["source_id"], "fam_mutterschutz")

    def test_assemble_hero_rejects_non_reproducing_case(self):
        before = RetrievalTrace(query="q", mode="hybrid")
        before.fused = [{"chunk_id": "fam__ans"}]                       # answer already at rank 0
        before._chunks = {"fam__ans": self._c("fam__ans", "fam_mutterschutz", "de", .9)}
        after = [self._c("fam__ans", "fam_mutterschutz", "de", .9)]
        with self.assertRaises(ValueError):
            assemble_hero("q", before, after, "fam_mutterschutz", "c")

    def test_inject_replaces_placeholder(self):
        tpl = '<script id="traces" type="application/json">/*__TRACES__*/</script>'
        out = inject(tpl, {"a": 1})
        self.assertIn('{"a": 1}', out)
        self.assertNotIn("/*__TRACES__*/", out)

    def test_inject_requires_placeholder(self):
        with self.assertRaises(ValueError):
            inject("<html></html>", {"a": 1})

"""Phase 4 validation gate — all three must pass before the index is 'done'.

    py tests/validate_phase4.py

Test 1  cross-lingual alignment  (HARD gate: cosine of parallel DE/EN content;
                                  ~0.5 means the multilingual space failed -> STOP)
Test 2  prefix verification      (with/without "passage: " must differ measurably)
Test 3  smoke retrieval          (dense-only top-5, scores + heading paths)

Exit code != 0 if the hard gate (Test 1) fails, so this doubles as a CI check.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT / "src"))

import numpy as np  # noqa: E402
from retrieval import E5Embedder, ChromaStore, Retriever  # noqa: E402

PAIR_DE, PAIR_EN = "gesund_vorsorge_de", "gesund_vorsorge_en"
GATE_EXPECT, GATE_STOP = 0.85, 0.70  # expected / collapse thresholds


def _vectors(store: ChromaStore, source_id: str):
    got = store.collection.get(where={"source_id": source_id},
                               include=["embeddings", "metadatas", "documents"])
    V = np.array(got["embeddings"])          # already L2-normalised at index time
    return V, got["metadatas"], got["documents"]


def test1_cross_lingual(store: ChromaStore) -> bool:
    print("\n" + "=" * 70)
    print("TEST 1 — cross-lingual alignment  (parallel content: "
          f"{PAIR_DE} <-> {PAIR_EN})")
    print("=" * 70)
    DE, dm, dd = _vectors(store, PAIR_DE)
    EN, em, ed = _vectors(store, PAIR_EN)
    print(f"DE chunks: {len(DE)}   EN chunks: {len(EN)}   "
          "(not 1:1 — using best cross-lingual match per chunk)")
    S = DE @ EN.T  # cosine (normalised) between every DE and EN chunk

    print("\nBest EN match for each DE chunk:")
    de_best = []
    for i in range(len(DE)):
        j = int(np.argmax(S[i]))
        de_best.append(S[i, j])
        print(f"  {S[i, j]:.3f}  DE «{dm[i]['heading_path'][:44]}»  ->  "
              f"EN «{em[j]['heading_path'][:44]}»")
    en_best = [float(np.max(S[:, j])) for j in range(len(EN))]

    mean_best = float(np.mean(de_best + en_best))
    print(f"\nmean best-match cosine (both directions): {mean_best:.3f}  "
          f"(expected > {GATE_EXPECT})")
    if mean_best < GATE_STOP:
        print(f"*** STOP: cosine {mean_best:.3f} < {GATE_STOP} — the multilingual "
              "space is NOT aligning DE/EN. The whole EN/DE test design collapses.")
        return False
    verdict = "PASS" if mean_best >= GATE_EXPECT else "PASS (below target, above collapse)"
    print(f"Test 1: {verdict}")
    return True


def test2_prefix(store: ChromaStore, embedder: E5Embedder) -> bool:
    print("\n" + "=" * 70)
    print("TEST 2 — prefix verification  (same passage, with vs without 'passage: ')")
    print("=" * 70)
    # a chunk we can aim a query at, plus the query
    got = store.collection.get(where={"source_id": PAIR_EN},
                               include=["documents", "metadatas"])
    doc = got["documents"][0]
    query = "What happens at a prenatal check-up?"

    q = embedder.embed_query(query)                    # "query: " + text
    with_prefix = embedder.embed_passages([doc])[0]    # "passage: " + text
    without_prefix = embedder._encode([doc])[0]        # raw, no prefix

    sim_with = float(q @ with_prefix)
    sim_without = float(q @ without_prefix)
    drift = float(with_prefix @ without_prefix)
    print(f"query: «{query}»")
    print(f"  cosine(query, passage WITH 'passage: ')   = {sim_with:.4f}")
    print(f"  cosine(query, passage WITHOUT prefix)     = {sim_without:.4f}")
    print(f"  delta from prefixing                      = {sim_with - sim_without:+.4f}")
    print(f"  cosine(with-prefix vec, no-prefix vec)    = {drift:.4f}  "
          "(<1.0 proves the prefix changes the vector)")
    ok = abs(sim_with - sim_without) > 1e-3 and drift < 0.9999
    print(f"Test 2: {'PASS — prefixing is applied and measurably changes retrieval' if ok else 'FAIL'}")
    return ok


def test3_smoke(retriever: Retriever) -> bool:
    print("\n" + "=" * 70)
    print("TEST 3 — smoke retrieval (dense only, top-5)")
    print("=" * 70)
    queries = [
        "Wann beginnt die Mutterschutzfrist?",
        "When does maternity protection start?",
        "Wie beantrage ich Elterngeld?",
        "What is prenatal care for?",
        "Wie finde ich eine Hebamme?",
    ]
    for query in queries:
        print(f"\nQ: {query}")
        for r in retriever.search(query, k=5, mode="dense"):
            print(f"  {r.score:.3f}  [{r.metadata['language']}] {r.source_id:28s} "
                  f"{r.heading_path[:50]}")
    print("\nTest 3: (visual check — nothing catastrophically wrong?)")
    return True


def main() -> int:
    embedder = E5Embedder()
    store = ChromaStore()
    retriever = Retriever(embedder=embedder, store=store)

    t1 = test1_cross_lingual(store)
    t2 = test2_prefix(store, embedder)
    test3_smoke(retriever)

    print("\n" + "=" * 70)
    print(f"GATE: Test1={'PASS' if t1 else 'STOP'}  Test2={'PASS' if t2 else 'FAIL'}  "
          "Test3=visual")
    print("=" * 70)
    return 0 if (t1 and t2) else 2


if __name__ == "__main__":
    raise SystemExit(main())

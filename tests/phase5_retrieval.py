"""Phase 5 validation — the six queries, with trace on, showing dense/sparse divergence.

    py tests/phase5_retrieval.py

For each query: top-5 dense, top-5 sparse, top-5 after RRF, and where a chunk ranked
highly in one index and poorly/absent in the other (the hybrid argument). Query 3
(bare legal term "Mutterschutzfrist") is the one where BM25 should beat dense. Then
query 5 is run WITH and WITHOUT a self-employed filter to show filtering changes the set.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT / "src"))

from retrieval import Retriever  # noqa: E402

# chunk_id -> compact label (language, source, heading tail) for readable output
LABELS: dict[str, tuple] = {}
for _l in (_ROOT / "data" / "chunks.jsonl").open(encoding="utf-8"):
    _r = json.loads(_l)
    _hp = _r["heading_path"]
    LABELS[_r["chunk_id"]] = (_r["language"], _r["source_id"],
                              (_hp[-1] if _hp else "")[:38], _r["user_type"])


def lab(cid: str) -> str:
    lang, sid, head, _ = LABELS.get(cid, ("?", "?", "?", "?"))
    return f"[{lang}] {sid:28s} {head}"


QUERIES = [
    "Wann beginnt die Mutterschutzfrist?",
    "When does maternity protection start?",
    "Mutterschutzfrist",
    "Wie beantrage ich Elterngeld?",
    "I am self-employed, do I get maternity pay?",
    "Wie finde ich eine Hebamme?",
]


def show(R: Retriever, query: str, filters=None, header: str = "") -> tuple:
    results, tr = R.search(query, k=10, filters=filters, mode="hybrid", trace=True)
    print("\n" + "=" * 78)
    print(f"Q: {query}   {header}")
    if filters:
        print(f"   filters={filters}")
    print("=" * 78)

    print("  top-5 DENSE (cosine):")
    for d in tr.dense[:5]:
        print(f"    {d['rank']:>2}. {d['similarity']:.3f}  {lab(d['chunk_id'])}")
    print("  top-5 SPARSE (BM25):")
    for s in tr.sparse[:5]:
        print(f"    {s['rank']:>2}. {s['bm25']:6.2f}  {lab(s['chunk_id'])}")
    print("  top-5 FUSED (RRF)   [dR=dense rank, sR=sparse rank; '-' = not in that pool]:")
    for f in tr.fused[:5]:
        dR = f["dense_rank"] if f["dense_rank"] is not None else "-"
        sR = f["sparse_rank"] if f["sparse_rank"] is not None else "-"
        print(f"    {f['rrf']:.5f}  dR={str(dR):>2} sR={str(sR):>2}  {lab(f['chunk_id'])}")

    # divergence: fused top-5 chunks whose two ranks disagree sharply (or absent in one)
    print("  DIVERGENCE (fused top-5 where the two indexes disagree):")
    any_div = False
    for f in tr.fused[:5]:
        dR, sR = f["dense_rank"], f["sparse_rank"]
        if dR is None or sR is None or abs(dR - sR) >= 4:
            any_div = True
            if dR is None:
                msg = f"BM25 rank {sR}, dense MISSED it"
            elif sR is None:
                msg = f"dense rank {dR}, BM25 MISSED it"
            else:
                msg = f"dense {dR} vs BM25 {sR} (gap {abs(dR - sR)})"
            print(f"    * {lab(f['chunk_id'])}  —  {msg}")
    if not any_div:
        print("    (none — the two indexes agree on the top of this query)")

    print(f"  in BOTH indexes: {len(tr.both)}   "
          f"context: {len(tr.final_context)} chunks / {tr.context_tokens} cl100k tokens"
          + (f"   UNDERFILLED: {tr.underfilled}" if tr.underfilled else ""))
    t = tr.timings_ms
    print("  timings ms: " + "  ".join(f"{k}={t[k]:.1f}" for k in
          ("dense_ms", "sparse_ms", "filter_ms", "fusion_ms", "total_ms") if k in t))
    return results, tr


def main() -> None:
    R = Retriever()  # one model load, reused across every query

    for q in QUERIES:
        show(R, q)

    # --- filtering proof: query 5 with vs without the self-employed filter ---
    print("\n\n" + "#" * 78)
    print("# FILTERING PROOF — query 5, WITHOUT filter vs WITH user_type=self-employed")
    print("#" * 78)
    res_no, _ = show(R, QUERIES[4], header="(no filter)")
    res_yes, tr_yes = show(R, QUERIES[4], filters={"user_type": "self-employed"},
                           header="(filtered)")

    ids_no = [r.chunk_id for r in res_no]
    ids_yes = [r.chunk_id for r in res_yes]
    print("\n--- difference ---")
    print(f"  unfiltered final: {len(ids_no)} chunks")
    print(f"  filtered   final: {len(ids_yes)} chunks")
    dropped = [c for c in ids_no if c not in ids_yes]
    added = [c for c in ids_yes if c not in ids_no]
    print(f"  dropped by filter ({len(dropped)}):")
    for c in dropped:
        ut = LABELS.get(c, ("", "", "", "?"))[3]
        print(f"    (user_type={ut}) {lab(c)}")
    print(f"  newly surfaced ({len(added)}):")
    for c in added:
        ut = LABELS.get(c, ("", "", "", "?"))[3]
        print(f"    (user_type={ut}) {lab(c)}")
    # show the self-employed-specific chunks that made the filtered set
    se = [c for c in ids_yes if LABELS.get(c, (None,)*4)[3] == "self-employed"]
    print(f"  self-employed-specific chunks in filtered result: {len(se)}")
    for c in se:
        print(f"    {lab(c)}")
    if ids_no == ids_yes:
        print("  !!! IDENTICAL — filtering did nothing (BUG)")
    else:
        print("  => filtering changed the result set (working).")


if __name__ == "__main__":
    main()

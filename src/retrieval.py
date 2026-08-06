"""NurtureDE retrieval layer — one interface, swappable parts.

`search(query, k, filters) -> list[RetrievedChunk]` is the single entry point the
rest of the system (and Phase 12's visualiser) sees. Behind it, the embedding model
and the vector store are each hidden behind a small surface so the production swap
(local E5 -> hosted endpoint; Chroma -> Supabase pgvector) is a contained change,
not a rewrite. A 2.2GB local model will not fit in a serverless function, so this
seam is load-bearing, not speculative.

Dense + sparse are complementary on this corpus:
  * dense (multilingual-E5) carries the cross-lingual and compound *semantics* — an
    English query must retrieve a German passage with zero shared words.
  * BM25 over the *displayed* `text` carries exact rare-token matching, including
    whole German compounds ("Mutterschutzfrist") that the dense space blurs.
They are fused with Reciprocal Rank Fusion (rank-based, so the two incomparable
score scales never have to be normalised against each other).
"""

from __future__ import annotations

import re
import time
import pickle
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol, Sequence

import numpy as np

# --- paths / constants -------------------------------------------------------
_ROOT = Path(__file__).resolve().parent.parent
CHROMA_DIR = _ROOT / "chroma_db"
BM25_PATH = _ROOT / "data" / "bm25.pkl"
COLLECTION = "nurture_chunks"

MODEL_NAME = "intfloat/multilingual-e5-large"
# E5 is asymmetric: documents and queries are embedded with different prefixes.
# Omitting these does NOT error — it silently degrades retrieval — so the prefix
# actually applied is recorded in each vector's metadata (embed_prefix) and can be
# verified rather than assumed (see index.py + validation Test 2).
PASSAGE_PREFIX = "passage: "
QUERY_PREFIX = "query: "

RRF_K = 60  # standard Reciprocal Rank Fusion damping constant


# --- German-aware tokenizer for BM25 ----------------------------------------
# Unicode word tokens, keeping umlauts (ä ö ü) as themselves. `casefold()` lowercases
# AND folds ß -> ss, which is the right German normalisation (many sources write
# "Strasse" for "Straße"). Deliberately does NOT decompose compounds:
# "Beschäftigungsverbot" stays one token. That is a known BM25 limitation, accepted
# here on purpose — BM25's job is exact whole-token / rare-term matching (a query
# term "Mutterschutzfrist" hits the compound directly); the dense E5 index is what
# handles sub-compound semantics. The two indexes cover each other's weakness.
_TOKEN_RE = re.compile(r"[0-9a-zA-ZÀ-ɏ]+")


def tokenize_de(text: str) -> list[str]:
    """Tokenize for BM25. Same function used at index and query time (must match)."""
    return [t.casefold() for t in _TOKEN_RE.findall(text)]


# --- result + trace types ----------------------------------------------------
@dataclass
class RetrievedChunk:
    chunk_id: str
    text: str
    score: float           # fused score (or single-index score in dense/sparse mode)
    metadata: dict

    @property
    def heading_path(self) -> str:
        return self.metadata.get("heading_path", "")

    @property
    def source_id(self) -> str:
        return self.metadata.get("source_id", "")


@dataclass
class RetrievalTrace:
    """Optional, off by default. Every stage the Phase-12 visualiser will render.

    Built as data is produced so instrumentation never has to be retrofitted into
    working retrieval code later.
    """
    query: str
    mode: str
    filters: dict | None = None
    dense: list[dict] = field(default_factory=list)     # {chunk_id, similarity, rank}
    sparse: list[dict] = field(default_factory=list)    # {chunk_id, bm25, rank}
    fused: list[dict] = field(default_factory=list)     # {chunk_id, rrf, dense_rank, sparse_rank}
    filter_exclusions: list[dict] = field(default_factory=list)  # {chunk_id, reason}
    rerank: list[dict] | None = None                    # populated when a reranker lands (Phase 5+)
    final_context: list[str] = field(default_factory=list)       # chunk_ids returned, in order
    timings_ms: dict = field(default_factory=dict)


# --- embedder ---------------------------------------------------------------
class Embedder(Protocol):
    def embed_passages(self, texts: Sequence[str]) -> np.ndarray: ...
    def embed_query(self, text: str) -> np.ndarray: ...


class E5Embedder:
    """multilingual-e5-large with the required asymmetric prefixes.

    The model (~2.2GB fp32) is loaded lazily on first use so importing this module
    is cheap. On this memory-constrained box it is loaded directly in **fp16**
    (~1.1GB) via `model_kwargs={"torch_dtype": float16}` — loading straight into
    fp16 avoids the transient fp32 peak that a post-hoc `.half()` would incur.
    fp16 vs fp32 is negligible for embedding quality. Vectors are cast back to
    fp32 for storage/scoring (tiny arrays; better downstream precision) and are
    L2-normalised, so cosine == inner product. Passages AND queries go through the
    same model/dtype, so their vectors are directly comparable.
    """

    def __init__(self, model_name: str = MODEL_NAME, dtype: str = "float16",
                 batch_size: int = 8):
        self.model_name = model_name
        self.dtype = dtype
        self.batch_size = batch_size
        self._model = None

    @property
    def model(self):
        if self._model is None:
            import torch
            from sentence_transformers import SentenceTransformer
            kwargs = {}
            if self.dtype:
                kwargs["model_kwargs"] = {"torch_dtype": getattr(torch, self.dtype)}
            self._model = SentenceTransformer(self.model_name, **kwargs)
        return self._model

    def _encode(self, texts: Sequence[str], batch_size: int | None = None) -> np.ndarray:
        emb = self.model.encode(
            list(texts),
            batch_size=batch_size or self.batch_size,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return emb.astype(np.float32)  # store/score in fp32 regardless of compute dtype

    def embed_passages(self, texts: Sequence[str], batch_size: int | None = None) -> np.ndarray:
        return self._encode([PASSAGE_PREFIX + t for t in texts], batch_size)

    def embed_query(self, text: str) -> np.ndarray:
        return self._encode([QUERY_PREFIX + text])[0]


# --- vector store -----------------------------------------------------------
class ChromaStore:
    """Chroma persistent collection, cosine space. Swap target: Supabase pgvector."""

    def __init__(self, path: Path = CHROMA_DIR, collection: str = COLLECTION):
        import chromadb
        self.client = chromadb.PersistentClient(path=str(path))
        self.collection = self.client.get_or_create_collection(
            name=collection, metadata={"hnsw:space": "cosine"}
        )

    def upsert(self, ids, embeddings, documents, metadatas):
        # upsert keyed on id => re-running the build never duplicates a chunk.
        self.collection.upsert(
            ids=list(ids),
            embeddings=[e.tolist() for e in embeddings],
            documents=list(documents),
            metadatas=list(metadatas),
        )

    def count(self) -> int:
        return self.collection.count()

    def query(self, embedding: np.ndarray, n: int) -> list[dict]:
        """Return up to n candidates as {chunk_id, similarity, text, metadata}.

        Filters are applied client-side by the Retriever (only 201 chunks) so that
        the trace can record *why* each excluded candidate was dropped — Chroma's
        server-side `where` would hide that.
        """
        res = self.collection.query(
            query_embeddings=[embedding.tolist()],
            n_results=n,
            include=["documents", "metadatas", "distances"],
        )
        out = []
        for cid, doc, meta, dist in zip(
            res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0]
        ):
            out.append(
                {"chunk_id": cid, "similarity": 1.0 - dist, "text": doc, "metadata": meta}
            )
        return out


# --- sparse index -----------------------------------------------------------
class SparseIndex:
    """BM25 over the displayed `text` (never embed_text — its bracketed authority/
    heading prefix would inflate term frequencies with authority names)."""

    def __init__(self, bm25, chunk_ids, texts, metadatas):
        self.bm25 = bm25
        self.chunk_ids = chunk_ids
        self.texts = texts
        self.metadatas = metadatas

    @classmethod
    def build(cls, chunk_ids, texts, metadatas) -> "SparseIndex":
        from rank_bm25 import BM25Okapi
        corpus = [tokenize_de(t) for t in texts]
        return cls(BM25Okapi(corpus), list(chunk_ids), list(texts), list(metadatas))

    def save(self, path: Path = BM25_PATH):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as fh:
            pickle.dump(
                {"bm25": self.bm25, "chunk_ids": self.chunk_ids,
                 "texts": self.texts, "metadatas": self.metadatas}, fh
            )

    @classmethod
    def load(cls, path: Path = BM25_PATH) -> "SparseIndex":
        with open(path, "rb") as fh:
            d = pickle.load(fh)
        return cls(d["bm25"], d["chunk_ids"], d["texts"], d["metadatas"])

    def query(self, text: str, n: int) -> list[dict]:
        scores = self.bm25.get_scores(tokenize_de(text))
        order = np.argsort(scores)[::-1][:n]
        out = []
        for i in order:
            out.append({
                "chunk_id": self.chunk_ids[i],
                "bm25": float(scores[i]),
                "text": self.texts[i],
                "metadata": self.metadatas[i],
            })
        return out


# --- filters ----------------------------------------------------------------
def _passes(meta: dict, filters: dict | None) -> tuple[bool, str]:
    """Exact-match metadata filter. Returns (passed, reason_if_excluded)."""
    if not filters:
        return True, ""
    for key, want in filters.items():
        got = meta.get(key)
        if isinstance(want, (list, tuple, set)):
            if got not in want:
                return False, f"{key}={got!r} not in {list(want)!r}"
        elif got != want:
            return False, f"{key}={got!r} != {want!r}"
    return True, ""


# --- the interface ----------------------------------------------------------
class Retriever:
    """The one retrieval interface. Construct once, reuse (holds the loaded model)."""

    POOL = 50  # candidates pulled from each index before filtering + fusion

    def __init__(self, embedder: Embedder | None = None,
                 store: ChromaStore | None = None,
                 sparse: SparseIndex | None = None):
        self.embedder = embedder or E5Embedder()
        self.store = store or ChromaStore()
        self.sparse = sparse  # loaded lazily; not needed for dense-only mode

    def _sparse_index(self) -> SparseIndex:
        if self.sparse is None:
            self.sparse = SparseIndex.load()
        return self.sparse

    def search(self, query: str, k: int = 5, filters: dict | None = None,
               mode: str = "hybrid", trace: bool = False):
        """mode: 'hybrid' (RRF of dense+sparse) | 'dense' | 'sparse'.

        Returns list[RetrievedChunk]; if trace=True, returns (list, RetrievalTrace).
        """
        tr = RetrievalTrace(query=query, mode=mode, filters=filters) if trace else None
        t0 = time.perf_counter()

        dense_hits: list[dict] = []
        if mode in ("hybrid", "dense"):
            ts = time.perf_counter()
            qv = self.embedder.embed_query(query)
            dense_hits = self.store.query(qv, self.POOL)
            if tr:
                tr.timings_ms["dense"] = (time.perf_counter() - ts) * 1000

        sparse_hits: list[dict] = []
        if mode in ("hybrid", "sparse"):
            ts = time.perf_counter()
            sparse_hits = self._sparse_index().query(query, self.POOL)
            if tr:
                tr.timings_ms["sparse"] = (time.perf_counter() - ts) * 1000

        # client-side filtering (records exclusions for the trace)
        def keep(hits):
            kept = []
            for h in hits:
                ok, why = _passes(h["metadata"], filters)
                if ok:
                    kept.append(h)
                elif tr:
                    tr.filter_exclusions.append({"chunk_id": h["chunk_id"], "reason": why})
            return kept

        dense_hits = keep(dense_hits)
        sparse_hits = keep(sparse_hits)

        dense_rank = {h["chunk_id"]: i for i, h in enumerate(dense_hits)}
        sparse_rank = {h["chunk_id"]: i for i, h in enumerate(sparse_hits)}
        meta_by_id = {h["chunk_id"]: h for h in (*dense_hits, *sparse_hits)}

        if tr:
            tr.dense = [{"chunk_id": h["chunk_id"], "similarity": round(h["similarity"], 4),
                         "rank": i} for i, h in enumerate(dense_hits)]
            tr.sparse = [{"chunk_id": h["chunk_id"], "bm25": round(h["bm25"], 4),
                          "rank": i} for i, h in enumerate(sparse_hits)]

        # fuse
        if mode == "dense":
            ranked = [(h["chunk_id"], h["similarity"]) for h in dense_hits]
        elif mode == "sparse":
            ranked = [(h["chunk_id"], h["bm25"]) for h in sparse_hits]
        else:
            ids = set(dense_rank) | set(sparse_rank)
            fused = []
            for cid in ids:
                rrf = 0.0
                if cid in dense_rank:
                    rrf += 1.0 / (RRF_K + dense_rank[cid])
                if cid in sparse_rank:
                    rrf += 1.0 / (RRF_K + sparse_rank[cid])
                fused.append((cid, rrf))
            fused.sort(key=lambda x: x[1], reverse=True)
            ranked = fused
            if tr:
                tr.fused = [{"chunk_id": cid, "rrf": round(s, 6),
                             "dense_rank": dense_rank.get(cid),
                             "sparse_rank": sparse_rank.get(cid)} for cid, s in fused[:k]]

        results = []
        for cid, score in ranked[:k]:
            h = meta_by_id[cid]
            results.append(RetrievedChunk(cid, h["text"], float(score), h["metadata"]))

        if tr:
            tr.final_context = [r.chunk_id for r in results]
            tr.timings_ms["total"] = (time.perf_counter() - t0) * 1000
            return results, tr
        return results

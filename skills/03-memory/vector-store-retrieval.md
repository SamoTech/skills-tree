---
title: "Vector Store Retrieval"
category: 03-memory
level: intermediate
stability: stable
added: "2025-03"
updated: "2026-04"
version: v3
description: "Look up the top-k items in a vector store by cosine similarity to a query embedding. The retrieval primitive that powers RAG, semantic search, deduplication, recommendation, and clustering."
tags: [memory, retrieval, embeddings, search, similarity]
dependencies:
  - package: openai
    min_version: "1.30.0"
    tested_version: "1.45.0"
    confidence: verified
  - package: numpy
    min_version: "1.26.0"
    tested_version: "2.0.0"
    confidence: verified
code_blocks:
  - id: "example-vector-retrieval"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-03-memory-vector-store-retrieval.json)

# Vector Store Retrieval

## Description

A vector store is a (id, vector, metadata, payload) collection plus a similarity-search index. **Vector store retrieval** is the act of embedding a query into the same space and returning the top-k items by cosine similarity (or dot-product, or L2). It's the lookup primitive underneath RAG, semantic dedup, recommendation, and "find me similar tickets" features.

This skill covers the retrieval-side contract and shows the same in-memory implementation hardened with normalisation, optional metadata filtering, and a clean swap-point for production stores (pgvector, Qdrant, Pinecone, Weaviate).

## When to Use

- You have an indexed corpus of vectors and a stream of query embeddings.
- You want **semantic** matches, not lexical (BM25 doesn't match "renew" → "extend").
- The corpus is **too large** to scan linearly per query (>~10k items) — production needs an ANN index, not Python loops.
- **Don't use** when an exact lexical match suffices (use grep/BM25), or the entire corpus fits in the context window.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `query_embedding` | `np.ndarray (d,)` | Unit-normalised dense vector |
| `top_k` | `int` | Items to return (default 5) |
| `filter` | `dict \| None` | Metadata predicates ANDed together |
| `score_threshold` | `float` | Drop hits below this similarity (default 0.0) |
| → `hits` | `list[Hit]` | Sorted by similarity, descending |
| → `hits[i].score` | `float` | Cosine similarity in [-1, 1] |

## Runnable Example

```python
# pip install openai numpy
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable
import numpy as np
from openai import OpenAI

client = OpenAI()
EMBED_MODEL = "text-embedding-3-small"

@dataclass
class Item:
    id: str
    text: str
    metadata: dict = field(default_factory=dict)
    vector: np.ndarray | None = None

@dataclass
class Hit:
    item: Item
    score: float

def embed(texts: list[str]) -> np.ndarray:
    r = client.embeddings.create(model=EMBED_MODEL, input=texts)
    v = np.asarray([d.embedding for d in r.data], dtype=np.float32)
    # Normalise so dot-product ≡ cosine similarity.
    return v / np.linalg.norm(v, axis=1, keepdims=True)

class InMemoryVectorStore:
    """Reference implementation. Swap for pgvector/Qdrant/Pinecone in prod."""

    def __init__(self) -> None:
        self._items: list[Item] = []
        self._matrix: np.ndarray | None = None  # shape (N, d), unit-normalised

    def upsert(self, items: list[Item]) -> None:
        new = [it for it in items if it.vector is None]
        if new:
            vecs = embed([it.text for it in new])
            for it, v in zip(new, vecs):
                it.vector = v
        # Replace any existing id with the new entry (idempotent upsert).
        by_id = {it.id: it for it in self._items}
        for it in items:
            by_id[it.id] = it
        self._items = list(by_id.values())
        self._matrix = np.stack([it.vector for it in self._items])

    def search(
        self,
        query: np.ndarray,
        *,
        top_k: int = 5,
        filter: Callable[[Item], bool] | None = None,
        score_threshold: float = 0.0,
    ) -> list[Hit]:
        if self._matrix is None or len(self._items) == 0:
            return []
        # Apply metadata filter first to a candidate mask.
        if filter is not None:
            mask = np.array([filter(it) for it in self._items], dtype=bool)
            if not mask.any():
                return []
            scores = self._matrix[mask] @ query
            cand = [it for it, m in zip(self._items, mask) if m]
        else:
            scores = self._matrix @ query
            cand = self._items
        # argpartition for O(N) top-k, then sort the small slice.
        k = min(top_k, len(cand))
        idx = np.argpartition(-scores, k - 1)[:k]
        idx = idx[np.argsort(-scores[idx])]
        return [
            Hit(cand[i], float(scores[i]))
            for i in idx if scores[i] >= score_threshold
        ]

if __name__ == "__main__":
    store = InMemoryVectorStore()
    store.upsert([
        Item("t-1", "How do I reset my password?", {"lang": "en"}),
        Item("t-2", "Where is the billing portal?",  {"lang": "en"}),
        Item("t-3", "Comment réinitialiser mon mot de passe ?", {"lang": "fr"}),
    ])
    q = embed(["I forgot my login"])[0]
    for h in store.search(q, top_k=2, filter=lambda it: it.metadata["lang"] == "en"):
        print(f"{h.score:.3f}  {h.item.id}  {h.item.text}")
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Top-1 is irrelevant but high score | Embedding model conflates topic with intent | Switch model, or add a re-ranker (cross-encoder) |
| Recent items never surface | Index isn't being updated | `upsert` on every write; never rebuild from scratch |
| Latency spikes at >100k items | Linear scan in Python | Move to ANN index (HNSW, IVF) — pgvector, Qdrant, Pinecone |
| Wrong distance metric | Mixed cosine/L2 between index and query | Normalise on write AND on query; document the metric |
| Stale duplicates | Two different ids for the same content | Hash text → id (SHA-1 first 12 chars); upsert by hash |
| Filter excludes everything | Over-strict metadata predicates | Apply filter loosely first; tighten only if too many hits |

## Variants

| Variant | When |
|---|---|
| **Pure cosine** (above) | Default; fast and well-understood |
| **Hybrid (cosine + BM25)** | Mixed semantic + keyword queries (codes, IDs, names) |
| **Re-rank with cross-encoder** | When top-k precision matters (RAG, search quality) |
| **MMR (Maximal Marginal Relevance)** | When diversity in results matters more than raw similarity |
| **Filtered search** | Multi-tenant: filter by `tenant_id` BEFORE the vector scan |

## Frameworks & Models

| Framework | Notes |
|---|---|
| In-memory NumPy (above) | <10k items; tests; prototyping |
| pgvector | Postgres-native; great if you already run PG |
| Qdrant / Weaviate / Milvus | Purpose-built; HNSW; rich filtering |
| Pinecone | Managed; pay-per-query; simple ops |
| FAISS | Local C++; fastest single-machine ANN |

## Model Comparison

| Capability | text-embedding-3-small | text-embedding-3-large | voyage-3 |
|---|---|---|---|
| Dimensions | 1536 | 3072 | 1024 |
| Quality | 4 | 5 | 5 |
| Cost | 5 | 3 | 4 |
| Latency | 5 | 4 | 4 |

## Related Skills

- [RAG](rag.md) — uses this primitive end-to-end
- [Embedding Generation](../12-data/embedding-generation.md) — how `vector` is produced
- [Memory Injection](memory-injection.md) — broader pattern for stitching context into a prompt

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Stub |
| 2026-04 | v3 | Battle-tested: typed Item/Hit, normalised cosine, metadata filter, ANN swap-point, failure modes |

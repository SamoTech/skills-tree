---
title: "Embedding Generation"
category: 12-data
level: intermediate
stability: stable
added: "2025-03"
updated: "2026-04"
version: v3
description: "Turn text (or images, audio) into dense unit-normalised vectors with a hosted embedding model. Batch the API calls, cache by content hash, and handle the per-token / per-input limits explicitly."
tags: [data, embeddings, vectors, retrieval, semantic-search]
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
  - id: "example-embedding-generation"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-embedding-generation.json)

# Embedding Generation

## Description

Embedding generation converts arbitrary inputs (most commonly text) into **fixed-dimensional dense vectors** that encode semantic similarity: similar inputs land near each other in vector space. The vectors are produced by a frozen pre-trained model and consumed by retrieval, clustering, classification, and recommendation systems.

This skill covers the production-grade contract: deterministic batching to maximise throughput, content-hash caching so you don't re-embed unchanged inputs, dimension reduction (via Matryoshka truncation when supported), and the silent-failure modes — wrong tokenizer, mixing dimensions, missing normalisation — that bite teams six months in.

## When to Use

- You need a **vector representation** that downstream code (vector store, classifier, ranker) can consume.
- The input is **text** (most common), or images/audio with a multimodal embedding model.
- You're embedding once and querying many times → **cache** by content hash; embeddings are deterministic for fixed model+content.
- **Don't use** when a sparse keyword index (BM25, tf-idf) is sufficient or when you need a probability distribution rather than a similarity vector.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `texts` | `list[str]` | Up to 2048 inputs per request (OpenAI limit) |
| `model` | `str` | Embedding model name |
| `dimensions` | `int \| None` | Truncate output (Matryoshka); requires supporting model |
| `batch_size` | `int` | Inputs per HTTP call (default 100) |
| `normalize` | `bool` | L2-normalise so dot product equals cosine (default `True`) |
| → `vectors` | `np.ndarray (N, d)` | One vector per input |
| → `tokens` | `int` | Total tokens billed |

## Runnable Example

```python
# pip install openai numpy
from __future__ import annotations
import hashlib
import os
from typing import Iterable
import numpy as np
from openai import OpenAI

client = OpenAI()
DEFAULT_MODEL = "text-embedding-3-small"
MAX_BATCH = 100  # well under OpenAI's 2048 hard cap; tunable per environment

_CACHE: dict[str, np.ndarray] = {}

def _key(model: str, dim: int | None, text: str) -> str:
    h = hashlib.sha256()
    h.update(model.encode())
    h.update(b"|")
    h.update(str(dim or "").encode())
    h.update(b"|")
    h.update(text.encode("utf-8"))
    return h.hexdigest()

def _chunk(seq: list, n: int) -> Iterable[list]:
    for i in range(0, len(seq), n):
        yield seq[i:i + n]

def embed_texts(
    texts: list[str],
    *,
    model: str = DEFAULT_MODEL,
    dimensions: int | None = None,
    normalize: bool = True,
    batch_size: int = MAX_BATCH,
) -> tuple[np.ndarray, int]:
    """Return (vectors of shape (N, d), total tokens billed)."""
    if not texts:
        return np.empty((0, 0), dtype=np.float32), 0

    out: list[np.ndarray | None] = [None] * len(texts)
    misses_idx: list[int] = []
    misses_text: list[str] = []
    for i, t in enumerate(texts):
        v = _CACHE.get(_key(model, dimensions, t))
        if v is None:
            misses_idx.append(i)
            misses_text.append(t)
        else:
            out[i] = v

    total_tokens = 0
    batch_start = 0  # offset into misses_idx for the current batch
    for batch in _chunk(misses_text, batch_size):
        kwargs = {"model": model, "input": batch}
        if dimensions is not None:
            kwargs["dimensions"] = dimensions
        r = client.embeddings.create(**kwargs)
        total_tokens += r.usage.total_tokens
        # r.data[k].index is 0-indexed within the BATCH; map back to misses_idx.
        for d in r.data:
            v = np.asarray(d.embedding, dtype=np.float32)
            if normalize:
                v = v / np.linalg.norm(v)
            i_global = misses_idx[batch_start + d.index]
            out[i_global] = v
            _CACHE[_key(model, dimensions, texts[i_global])] = v
        batch_start += len(batch)

    matrix = np.stack(out)  # type: ignore[arg-type]
    return matrix, total_tokens

if __name__ == "__main__":
    docs = [
        "Refunds are processed within 5 business days.",
        "Premium plan includes 24/7 support.",
        "Refunds are processed within 5 business days.",  # duplicate → cached
    ]
    v, n = embed_texts(docs, dimensions=512)
    print(f"shape={v.shape}  billed_tokens={n}")
    print(f"cosine(0,1)={float(v[0] @ v[1]):.3f}")
    print(f"cosine(0,2)={float(v[0] @ v[2]):.3f}  # near 1.0, identical text")
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Inputs silently truncated | Single text exceeds model's max-tokens (8192 for `text-embedding-3-*`) | Pre-chunk; reject or split with overlap |
| Re-billed for unchanged docs | No caching | Hash by `(model, dim, content)` and persist (Redis, disk) |
| Dimension mismatch with index | Embedded with `text-embedding-3-large` (3072) but index expects 1536 | Pin the (`model`, `dimensions`) pair in your index metadata |
| Cosine drift over time | Switched model without re-embedding the corpus | Embedding-model version is **part of the index identity**; rebuild on switch |
| Slow throughput | Sequential single-input calls | Batch up to `batch_size`; the API charges per token, not per call |
| Non-deterministic results | Random seed in some open-source models | Pin model+version; cache by content hash |
| Multilingual queries miss | Used a monolingual English model | Use a multilingual model (`text-embedding-3-*` is) or per-language indexes |

## Variants

| Variant | When |
|---|---|
| **Hosted text** (above) | Default for production; pay-per-token, low ops |
| **Local sentence-transformers** | Offline / sensitive data; CPU-OK for <100 dims |
| **Matryoshka truncation** | Cut dimensions (e.g. 3072 → 512) for cheap storage at small quality cost |
| **Image embeddings (CLIP)** | Cross-modal search (text ↔ image) |
| **Late-interaction (ColBERT)** | Per-token vectors, much higher recall, much higher index cost |

## Frameworks & Models

| Provider / Model | Dim | Notes |
|---|---|---|
| OpenAI `text-embedding-3-small` | 1536 (truncatable) | Default; cheapest; multilingual |
| OpenAI `text-embedding-3-large` | 3072 (truncatable) | Highest quality; ~5× cost |
| Voyage `voyage-3` | 1024 | Strong on retrieval benchmarks |
| Cohere `embed-v3` | 1024 / 384 | Solid multilingual; rerank-ready |
| `sentence-transformers` (local) | 384–768 | Free; fine for <1M items |

## Model Comparison

| Capability | text-embedding-3-small | text-embedding-3-large | voyage-3 |
|---|---|---|---|
| Retrieval quality | 4 | 5 | 5 |
| Cost-per-million-tokens | 5 | 3 | 4 |
| Latency | 5 | 4 | 4 |
| Multilingual | 4 | 5 | 4 |

## Related Skills

- [Vector Store Retrieval](../03-memory/vector-store-retrieval.md) — consumes these vectors
- [RAG](../03-memory/rag.md) — full retrieval + generation loop
- [Similarity Search](similarity-search.md) — variants beyond top-k cosine

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Stub |
| 2026-04 | v3 | Battle-tested: batching, content-hash cache, Matryoshka, multilingual notes, model comparison |

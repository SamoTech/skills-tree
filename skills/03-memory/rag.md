---
title: "RAG (Retrieval-Augmented Generation)"
category: 03-memory
level: intermediate
stability: stable
added: "2025-03"
updated: "2026-04"
version: v3
description: "Augment an LLM call with the top-k most relevant chunks from a private corpus, retrieved by embedding similarity. The standard recipe for grounding answers, citing sources, and shrinking hallucinations on a known knowledge base."
tags: [memory, retrieval, embeddings, grounding, hallucination]
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
  - id: "example-rag"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-03-memory-rag.json)

# RAG (Retrieval-Augmented Generation)

## Description

RAG ([Lewis et al., 2020](https://arxiv.org/abs/2005.11401)) is the dominant pattern for grounding LLMs on private or fast-moving data: at query time, embed the question, fetch the **top-k most similar chunks** from a vector store, stuff them into the prompt as context, and let the LLM answer with citations. It's cheaper than fine-tuning, easy to update (just re-embed), and the citations make hallucinations auditable.

This skill is the minimal end-to-end recipe — chunk → embed → store → retrieve → prompt — with the knobs that actually matter (chunk size, top-k, similarity threshold, citation format) and the failure modes you will absolutely hit in production.

## When to Use

- The answer must come from a **specific corpus** (your docs, your tickets, your codebase) and the model alone doesn't know it.
- The corpus is **larger than the context window**, or queries touch a small unpredictable subset.
- You need **citations / provenance** — RAG returns the exact chunks used.
- **Don't use** when: the corpus fits in the context (just stuff it), the answer requires multi-hop reasoning across the whole corpus (use a graph-RAG / agentic retrieval pattern instead), or the corpus is the *open web* (use [Web Search](../11-web/web-search.md)).

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `question` | `str` | User query in natural language |
| `corpus` | `list[Document]` | Pre-chunked documents with `text` + `metadata` |
| `k` | `int` | Number of chunks to retrieve (default 4) |
| `min_similarity` | `float` | Cosine threshold; chunks below are dropped (default 0.25) |
| → `answer` | `str` | Grounded answer with inline citations |
| → `sources` | `list[Document]` | Chunks actually used (subset of top-k after threshold) |
| → `confidence` | `float` | Top similarity score; useful for cascade gating |

## Runnable Example

```python
# pip install openai numpy
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from openai import OpenAI

client = OpenAI()
EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o"

@dataclass
class Document:
    id: str
    text: str
    metadata: dict
    embedding: np.ndarray | None = None

def embed(texts: list[str]) -> np.ndarray:
    r = client.embeddings.create(model=EMBED_MODEL, input=texts)
    vecs = np.array([d.embedding for d in r.data], dtype=np.float32)
    # Normalise so dot product == cosine similarity.
    return vecs / np.linalg.norm(vecs, axis=1, keepdims=True)

def index(corpus: list[Document]) -> list[Document]:
    vecs = embed([d.text for d in corpus])
    for d, v in zip(corpus, vecs):
        d.embedding = v
    return corpus

def retrieve(question: str, corpus: list[Document], k: int = 4,
             min_similarity: float = 0.25) -> list[tuple[Document, float]]:
    q = embed([question])[0]
    scored = [(d, float(q @ d.embedding)) for d in corpus]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [(d, s) for d, s in scored[:k] if s >= min_similarity]

SYSTEM = (
    "Answer using ONLY the provided context. Cite sources inline as [id]. "
    "If the context does not contain the answer, say 'I don't know.' Do not "
    "guess and do not use prior knowledge."
)

def rag_answer(question: str, corpus: list[Document], *, k: int = 4) -> dict:
    hits = retrieve(question, corpus, k=k)
    if not hits:
        return {"answer": "I don't know.", "sources": [], "confidence": 0.0}
    context = "\n\n".join(f"[{d.id}] {d.text}" for d, _ in hits)
    r = client.chat.completions.create(
        model=CHAT_MODEL, temperature=0.0,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
    )
    return {
        "answer": r.choices[0].message.content,
        "sources": [d for d, _ in hits],
        "confidence": hits[0][1],
    }

if __name__ == "__main__":
    corpus = index([
        Document("doc-1", "Refunds are processed within 5 business days.", {"src": "policy.md"}),
        Document("doc-2", "Our office hours are 9am-5pm Eastern, Mon-Fri.", {"src": "contact.md"}),
        Document("doc-3", "Premium plan includes 24/7 support and SLA.", {"src": "pricing.md"}),
    ])
    out = rag_answer("How long do refunds take?", corpus)
    print(out["answer"])  # → "Refunds are processed within 5 business days. [doc-1]"
    print([s.id for s in out["sources"]])
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Wrong chunk retrieved (low recall) | Chunks too large, query specific to a sub-paragraph | Smaller chunks (200–500 tokens) with overlap, or hierarchical indexing |
| Right chunk retrieved, ignored by LLM | Buried in the middle of a large context | Use top-k≤6, put question last ("lost in the middle"), reduce noise |
| Hallucinated citation `[doc-X]` | Model invented an id that wasn't in context | Validate cited ids against `sources`; on mismatch, mark answer untrusted |
| "I don't know" when answer IS in corpus | `min_similarity` too high or chunk too long | Lower threshold; switch to hybrid (BM25 + dense); add a re-ranker |
| Stale answers | Corpus re-embedded on a slow schedule | Stream updates; use upsert with `metadata.updated_at` and prefer fresher |
| Cost spikes on long contexts | Large k × large chunks | Re-rank with a cross-encoder, then keep only the top 2-3 |

## Variants

| Variant | When |
|---|---|
| **Naïve RAG** (above) | Default, well-trodden, works for FAQ/support/docs |
| **Hybrid retrieval** | Add BM25/keyword score and fuse — fixes "exact-match" queries embeddings miss |
| **Re-ranking RAG** | Retrieve k=20, re-rank with a cross-encoder, keep top 4 — best precision |
| **Multi-query RAG** | Have the LLM rewrite the question into N variants, union the hits |
| **Graph-RAG / Agentic RAG** | Multi-hop questions; the agent decides what to retrieve next |
| **Long-context RAG** | Skip retrieval, stuff the corpus, rely on a 1M-token model — wasteful but simple |

## Frameworks & Models

| Framework | Notes |
|---|---|
| Direct API (above) | Maximum control; ~80 lines |
| LangChain `RetrievalQA` | Pre-baked chains; verbose but feature-complete |
| LlamaIndex | Best DX for multi-source, hybrid, hierarchical |
| Haystack | Strong on enterprise pipelines + production deploy |
| pgvector / Qdrant / Pinecone | Pick based on ops; pgvector wins if you already run Postgres |

## Model Comparison

| Capability | claude-opus-4-5 | gpt-4o | claude-haiku-4-5 |
|---|---|---|---|
| Citation discipline | 5 | 4 | 4 |
| "I don't know" calibration | 5 | 4 | 4 |
| Synthesis across chunks | 5 | 5 | 4 |
| Latency for k=4 | 3 | 4 | 5 |

## Related Skills

- [Vector Store Retrieval](vector-store-retrieval.md) — the retrieval primitive
- [Embedding Generation](../12-data/embedding-generation.md) — how chunks become vectors
- [Memory Injection](memory-injection.md) — broader pattern for stitching context into a prompt
- [Web Search](../11-web/web-search.md) — when the corpus is the open web instead

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Stub |
| 2026-04 | v3 | Battle-tested: end-to-end runnable example, threshold + citation handling, failure modes, variants, model comparison |

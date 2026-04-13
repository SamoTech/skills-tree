---
title: RAG — Retrieval-Augmented Generation
category: 09-agentic-patterns
level: intermediate
stability: stable
added: "2025-03"
description: "Apply rag in AI agent workflows."
version: v3
tags: [rag, retrieval, embeddings, knowledge-base]
updated: 2026-04
---


![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-rag.json)

# RAG — Retrieval-Augmented Generation

## What It Does

RAG grounds model responses in external knowledge by retrieving relevant documents at query time and injecting them into the prompt. The model uses the retrieved context to answer — preventing hallucination and enabling up-to-date or domain-specific knowledge without fine-tuning.

**Pipeline:** Query → Embed → Retrieve top-K → Inject → Generate → Cite

## When to Use

- Questions over private or proprietary knowledge bases
- Up-to-date information (news, docs, code, policies)
- Reducing hallucination on factual questions
- Any domain where the model lacks sufficient training data

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `query` | `str` | User's question |
| `documents` | `list[str]` | Corpus to index (or pre-indexed vector store) |
| `top_k` | `int` | Number of chunks to retrieve (default: 5) |
| `chunk_size` | `int` | Tokens per chunk (default: 512) |
| → `answer` | `str` | Grounded, cited answer |
| → `sources` | `list[str]` | Retrieved chunks used |

## Runnable Example

```python
import anthropic
import numpy as np
from typing import List, Tuple

client = anthropic.Anthropic()

# --- Step 1: Chunk documents ---
def chunk_text(text: str, chunk_size: int = 512) -> List[str]:
    words = text.split()
    return [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]

# --- Step 2: Embed chunks ---
def embed(texts: List[str]) -> np.ndarray:
    # Production: use voyage-3 or text-embedding-3-small
    # Demo: random vectors (replace with real embeddings)
    return np.random.rand(len(texts), 256)

# --- Step 3: Retrieve top-K ---
def retrieve(query: str, chunks: List[str], embeddings: np.ndarray, top_k: int = 5) -> List[str]:
    query_vec = embed([query])[0]
    scores = embeddings @ query_vec / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_vec) + 1e-8
    )
    top_indices = np.argsort(scores)[::-1][:top_k]
    return [chunks[i] for i in top_indices]

# --- Step 4: Generate with context ---
def rag(query: str, documents: List[str], top_k: int = 5) -> dict:
    # Index
    chunks = []
    for doc in documents:
        chunks.extend(chunk_text(doc))
    embeddings = embed(chunks)

    # Retrieve
    relevant = retrieve(query, chunks, embeddings, top_k)
    context = "\n\n---\n\n".join(f"[{i+1}] {c}" for i, c in enumerate(relevant))

    # Generate
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system="""Answer the question using ONLY the provided context.
Cite sources as [1], [2], etc.
If the answer is not in the context, say: 'I don't have enough context to answer this.'""",
        messages=[{
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {query}"
        }]
    )

    return {
        "answer": response.content[0].text,
        "sources": relevant
    }

# Usage
docs = [
    "Skills Tree is a community-powered AI agent skill OS with 515+ production-ready skills across 16 categories.",
    "The project includes systems, blueprints, benchmarks, and labs for building production AI agents.",
    "Every skill file includes a description, typed I/O, runnable code, failure modes, and a version history."
]
result = rag("What does Skills Tree include?", docs)
print(result["answer"])
```

## RAG Variants

| Variant | Description | When to Use |
|---|---|---|
| **Naive RAG** | Embed → retrieve → generate | Simple Q&A, baseline |
| **HyDE** | Generate hypothetical answer, embed that to retrieve | Low-recall corpora, +12% recall |
| **Multi-query** | Generate N query variants, merge results | Ambiguous questions |
| **Rerank** | Retrieve 20, rerank to top 5 with cross-encoder | Precision-critical tasks |
| **GraphRAG** | Build knowledge graph, traverse for context | Complex entity relationships |
| **Corrective RAG** | Evaluate retrieved docs, web-search if poor quality | Dynamic/recent info needed |

## Failure Modes

| Failure | Cause | Fix |
|---|---|---|
| Retrieves irrelevant chunks | Poor embedding or chunk boundaries | Try HyDE; fix chunking strategy |
| Ignores retrieved context | Model over-relies on training data | Reinforce with "use ONLY context" in system prompt |
| Hallucinated citations | Model invents [3] that doesn't exist | Number chunks explicitly, validate in post-processing |
| Chunk too large | Model ignores middle of long chunks | Keep chunks ≤ 512 tokens; use sentence boundaries |

## Blueprint

For a full production-ready RAG stack: → [`blueprints/rag-stack.md`](../../blueprints/rag-stack.md)

## Related Skills

- [`memory-injection.md`](../03-memory/memory-injection.md) — User-specific memory
- [`react.md`](../02-reasoning/react.md) — Use RAG as a tool inside ReAct
- [`web-search.md`](../11-web/web-search.md) — Live retrieval from the web

## Changelog

| Version | Date | Change |
|---|---|---|
| v1 | 2025-01 | Initial entry |
| v2 | 2025-06 | Added HyDE, reranking variants |
| v3 | 2026-04 | Full runnable pipeline, variants table, blueprint link |

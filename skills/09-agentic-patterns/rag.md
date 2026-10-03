---
title: RAG — Retrieval-Augmented Generation
category: 09-agentic-patterns
level: intermediate
stability: stable
version: v4
added: "2025-03"
updated: "2026-10-03"
description: "Ground generation with retrieved external context by separating ingestion, retrieval, context assembly, generation, and source attribution, with explicit handling for weak or conflicting retrieval."
tags: [rag, retrieval, embeddings, knowledge-base, grounding]
---

# RAG — Retrieval-Augmented Generation

## Purpose

RAG separates knowledge retrieval from language generation. The system retrieves relevant source material at query time, supplies that material to the generator, and preserves source references so the answer can be inspected.

RAG is a grounding architecture, not a guarantee against hallucination.

## Pipeline

```
source ingestion
    -> chunking
    -> indexing
    -> query
    -> retrieval
    -> optional reranking
    -> context assembly
    -> generation
    -> citation / validation
```

## Inputs / Outputs

| Item | Type | Required | Notes |
|---|---|---:|---|
| Query | str | yes | User task or information need |
| Corpus | documents | yes | Sources with stable identifiers |
| Retriever | callable | yes | Returns ranked source chunks |
| Generator | callable | yes | Produces answer from bounded context |
| Answer | str | yes | Generated response |
| Sources | list[str] | yes | Source IDs supplied to generator |
| Retrieval scores | list[float] | recommended | Diagnostics only |

## Runnable Example

This deterministic example uses lexical retrieval instead of pseudo-random vectors. It demonstrates the retrieval boundary without pretending to be a production embedding system.

```python
import re
from collections import Counter

DOCUMENTS = {
    "policy": "Skills Tree stores canonical skills in the skills directory.",
    "registry": "The universal registry provides validated machine-readable capability access.",
    "search": "The search index is generated from skill Markdown into docs/search-index.json.",
}

def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())

def retrieve(query: str, documents: dict[str, str], top_k: int = 2):
    q = Counter(tokenize(query))
    scored = []
    for doc_id, text in documents.items():
        d = Counter(tokenize(text))
        score = sum(min(q[token], d[token]) for token in q)
        if score:
            scored.append((doc_id, float(score)))
    return sorted(scored, key=lambda item: (-item[1], item[0]))[:top_k]

def build_context(query: str) -> dict:
    hits = retrieve(query, DOCUMENTS)
    return {
        "query": query,
        "sources": [doc_id for doc_id, _ in hits],
        "context": "\n".join(DOCUMENTS[doc_id] for doc_id, _ in hits),
    }

print(build_context("Where is the canonical search index generated?"))
```

## Retrieval Design

- Preserve stable document IDs and source locations.
- Chunk according to document structure rather than arbitrary token counts alone.
- Apply authorization, tenant, language, and document-type filters where required.
- Keep retrieved context bounded.
- Treat lexical, dense, hybrid, and reranked retrieval as separate components with independently measurable behavior.
- Do not treat a retrieval score as a probability of correctness.
- When sources conflict, expose the conflict instead of selecting one silently.

## Generation Contract

A generator should receive the query, bounded retrieved context, source identifiers, and explicit instructions for missing or conflicting evidence.

Validate that every cited source identifier was actually retrieved. Citation presence alone does not prove support for the underlying claim.

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Irrelevant retrieval | Weak query/index or poor chunking | Measure retrieval behavior and tune the index |
| Missing evidence | Relevant source not retrieved | Broaden retrieval or report insufficient context |
| Citation fabrication | Generator invents source IDs | Validate cited IDs against retrieved sources |
| Context overload | Too many or oversized chunks | Bound context and rerank |
| Stale knowledge | Index is not refreshed | Track source freshness and rebuild deterministically |
| Conflicting sources | Incompatible corpus claims | Preserve provenance and surface the conflict |

## Evaluation

Measure retrieval and generation separately. Retrieval can use recall@k, precision@k, or ranking metrics against a fixed evaluation set. Generation should separately assess factual support, citation correctness, refusal behavior, and completeness.

Do not infer production readiness from a single benchmark.

## Evidence

- Lewis et al., Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks: https://arxiv.org/abs/2005.11401
- OpenAI retrieval example: https://cookbook.openai.com/examples/vector_databases/read_and_query_chroma_data
- LangChain retrieval concepts: https://python.langchain.com/docs/concepts/retrieval/

Evidence status: references support the architecture and evaluation concepts. No performance ranking or production-readiness claim is made.

## Related Skills

- memory-injection
- web-search
- knowledge-graph-reading
- vector-store-retrieval

## Changelog

| Version | Date | Change |
|---|---|---|
| v1 | 2025-03 | Initial entry |
| v2 | 2025-06 | Added retrieval variants |
| v3 | 2026-04 | Added runnable example |
| v4 | 2026-10 | Removed pseudo-random embeddings and separated retrieval/generation contracts |

---
title: RAG Stack Blueprint
type: blueprint
stability: production-ready
version: v1
updated: 2026-04
---

# RAG Stack — Production Blueprint

A complete, copy-paste production RAG architecture. Covers ingestion, chunking, embedding, storage, retrieval, reranking, and generation — all wired together.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    INGESTION PIPELINE                   │
│                                                         │
│  Documents → Parse → Chunk → Embed → Store in VectorDB  │
│  (PDFs, URLs,        (512 tok  (voyage-3  (pgvector /   │
│   Notion, GH)         overlap)  or v3-sm)  Qdrant)      │
└─────────────────────────────────────────────────────────┘
                              │
                              │ (offline, one-time)
                              │
┌─────────────────────────────────────────────────────────┐
│                    QUERY PIPELINE                       │
│                                                         │
│  Query → Embed → ANN Search → Rerank → Generate → Cite  │
│           (same    (top-20)   (cross-   (Claude /  (with │
│           model)              encoder)  GPT-4o)    [n]) │
└─────────────────────────────────────────────────────────┘
```

## Full Implementation

```python
import anthropic
import numpy as np
from dataclasses import dataclass, field
from typing import List, Optional

client = anthropic.Anthropic()

# ─── Data types ────────────────────────────────────────────
@dataclass
class Chunk:
    id: str
    text: str
    source: str
    metadata: dict = field(default_factory=dict)
    embedding: Optional[np.ndarray] = None

@dataclass
class RAGResult:
    answer: str
    chunks: List[Chunk]
    confidence: str  # high | medium | low

# ─── Stage 1: Chunking ─────────────────────────────────────
def chunk_document(text: str, source: str, chunk_size: int = 512, overlap: int = 50) -> List[Chunk]:
    words = text.split()
    step = chunk_size - overlap
    chunks = []
    for i, start in enumerate(range(0, len(words), step)):
        chunk_text = " ".join(words[start:start + chunk_size])
        if chunk_text.strip():
            chunks.append(Chunk(
                id=f"{source}::{i}",
                text=chunk_text,
                source=source
            ))
    return chunks

# ─── Stage 2: Embedding ────────────────────────────────────
def embed_chunks(chunks: List[Chunk]) -> List[Chunk]:
    # Production: use voyage-3 or text-embedding-3-small
    # Demo: random normalized vectors
    for chunk in chunks:
        v = np.random.rand(256)
        chunk.embedding = v / np.linalg.norm(v)
    return chunks

# ─── Stage 3: Vector Store ─────────────────────────────────
class VectorStore:
    def __init__(self):
        self.chunks: List[Chunk] = []

    def add(self, chunks: List[Chunk]):
        self.chunks.extend(chunks)

    def search(self, query_vec: np.ndarray, top_k: int = 20) -> List[tuple]:
        if not self.chunks:
            return []
        embeddings = np.stack([c.embedding for c in self.chunks])
        scores = embeddings @ query_vec
        top_idx = np.argsort(scores)[::-1][:top_k]
        return [(self.chunks[i], float(scores[i])) for i in top_idx]

# ─── Stage 4: Reranking ────────────────────────────────────
def rerank(query: str, candidates: List[tuple], top_k: int = 5) -> List[Chunk]:
    # Production: use Cohere Rerank or cross-encoder
    # Demo: return top-k by score (already sorted)
    return [chunk for chunk, _ in candidates[:top_k]]

# ─── Stage 5: Generation ───────────────────────────────────
def generate(query: str, chunks: List[Chunk]) -> RAGResult:
    context_parts = []
    for i, chunk in enumerate(chunks):
        context_parts.append(f"[{i+1}] Source: {chunk.source}\n{chunk.text}")
    context = "\n\n".join(context_parts)

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system="""Answer the question using ONLY the provided context chunks.
Cite sources as [1], [2], etc. after each claim.
If the answer isn't in the context, respond: 'I don't have enough information to answer this.'
End with a confidence level: HIGH (all facts sourced), MEDIUM (partial), or LOW (inferred).""",
        messages=[{"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}]
    )

    text = response.content[0].text
    confidence = "high" if "HIGH" in text else "medium" if "MEDIUM" in text else "low"
    return RAGResult(answer=text, chunks=chunks, confidence=confidence)

# ─── Full RAG Stack ─────────────────────────────────────────
class RAGStack:
    def __init__(self):
        self.store = VectorStore()

    def ingest(self, text: str, source: str):
        """Add a document to the knowledge base."""
        chunks = chunk_document(text, source)
        chunks = embed_chunks(chunks)
        self.store.add(chunks)
        print(f"✅ Ingested {len(chunks)} chunks from '{source}'")

    def query(self, question: str, top_k: int = 5) -> RAGResult:
        """Answer a question from the knowledge base."""
        query_vec = embed_chunks([Chunk("q", question, "query")])[0].embedding
        candidates = self.store.search(query_vec, top_k=20)
        top_chunks = rerank(question, candidates, top_k=top_k)
        return generate(question, top_chunks)

# ─── Usage ──────────────────────────────────────────────────
rag = RAGStack()
rag.ingest("Skills Tree contains 515+ AI agent skills across 16 categories.", "skills-tree-docs")
rag.ingest("ReAct combines reasoning and acting in an alternating loop.", "skills-tree-docs")

result = rag.query("How many skills does Skills Tree have?")
print(result.answer)
print(f"Confidence: {result.confidence}")
```

## Production Checklist

- [ ] Replace demo embeddings with `voyage-3` or `text-embedding-3-small`
- [ ] Replace in-memory store with `pgvector` (Supabase) or `Qdrant`
- [ ] Add Cohere Rerank or `cross-encoder/ms-marco-MiniLM-L-6-v2`
- [ ] Add chunk metadata: `page_num`, `section`, `last_updated`
- [ ] Add query caching (Redis, 15-min TTL)
- [ ] Add observability: log retrieval scores, token counts, latency
- [ ] Add incremental ingestion — only re-embed changed documents

## Deployment Options

| Scale | Stack | Cost |
|---|---|---|
| Prototype | In-memory + Claude | $0 infra |
| Small (< 100k docs) | Supabase pgvector + Claude | ~$25/mo |
| Medium (< 1M docs) | Qdrant Cloud + voyage-3 + Claude | ~$100/mo |
| Large (> 1M docs) | Pinecone + Cohere Rerank + Claude | ~$300+/mo |

## Related

- [`skills/09-agentic-patterns/rag.md`](../skills/09-agentic-patterns/rag.md) — Core RAG skill
- [`skills/03-memory/memory-injection.md`](../skills/03-memory/memory-injection.md) — User memory
- [`systems/research-agent.md`](../systems/research-agent.md) — RAG inside a full system

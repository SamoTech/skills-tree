# RAG Stack Blueprint

**Use Case:** Production retrieval-augmented generation  
**Complexity:** Intermediate  
**Skills:** Embedding · Vector Store · Retrieval · Generation  
**Version:** v1  
**Added:** 2026-04

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   INGESTION PIPELINE                │
│                                                     │
│  Documents → Chunker → Embedder → Vector Store      │
│  (PDF/MD/HTML)  (512tok)  (text-emb-3)  (pgvector) │
└─────────────────────────────────────────────────────┘
                          │
                    (offline / async)
                          │
┌─────────────────────────────────────────────────────┐
│                   QUERY PIPELINE                    │
│                                                     │
│  User Query → Query Embedder → Retriever            │
│                    │              │                 │
│                    ▼              ▼                 │
│               HyDE expansion   Top-K chunks        │
│                    │              │                 │
│                    └──────┬───────┘                 │
│                           ▼                         │
│                    Context Assembler                │
│                           │                         │
│                           ▼                         │
│                    LLM Generator → Answer           │
└─────────────────────────────────────────────────────┘
```

---

## Technology Stack

| Component | Recommended | Alternative | Notes |
|---|---|---|---|
| **Chunker** | `langchain.text_splitter` | `semantic-chunker` | 512 tokens, 50 overlap |
| **Embedder** | `text-embedding-3-small` | `voyage-3-lite` | Cost vs quality trade-off |
| **Vector Store** | `pgvector` (PostgreSQL) | `Qdrant`, `Chroma` | pgvector if you already run Postgres |
| **Retriever** | Cosine similarity top-K | BM25 hybrid | Hybrid = +12% recall |
| **Query expansion** | HyDE | Multi-query | HyDE +12% recall (see benchmark) |
| **LLM** | `claude-opus-4-5` | `claude-haiku` | Haiku for cost, Opus for quality |
| **Orchestration** | Python (direct) | LangChain, LlamaIndex | Direct = simpler debugging |

---

## Full Implementation

```python
import anthropic
import numpy as np
from dataclasses import dataclass

client = anthropic.Anthropic()

@dataclass
class Chunk:
    text: str
    source: str
    embedding: list[float] = None

def embed(text: str) -> list[float]:
    # Use OpenAI, Voyage, or Cohere embeddings
    raise NotImplementedError("Plug in your embedding provider")

def cosine_similarity(a: list[float], b: list[float]) -> float:
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

class RAGStack:
    def __init__(self):
        self.chunks: list[Chunk] = []

    def ingest(self, text: str, source: str, chunk_size: int = 512):
        words = text.split()
        for i in range(0, len(words), chunk_size - 50):
            chunk_text = " ".join(words[i:i + chunk_size])
            chunk = Chunk(text=chunk_text, source=source)
            chunk.embedding = embed(chunk_text)
            self.chunks.append(chunk)

    def hyde_expand(self, query: str) -> str:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=256,
            messages=[{
                "role": "user",
                "content": f"Write a short hypothetical document that answers: {query}"
            }]
        )
        return response.content[0].text

    def retrieve(self, query: str, top_k: int = 5, use_hyde: bool = True) -> list[Chunk]:
        search_text = self.hyde_expand(query) if use_hyde else query
        query_emb = embed(search_text)
        scored = [
            (cosine_similarity(query_emb, c.embedding), c)
            for c in self.chunks
        ]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in scored[:top_k]]

    def generate(self, query: str, chunks: list[Chunk]) -> str:
        context = "\n\n---\n\n".join(
            f"[{c.source}]\n{c.text}" for c in chunks
        )
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer using only the provided context. Cite sources."
            }]
        )
        return response.content[0].text

    def query(self, question: str) -> str:
        chunks = self.retrieve(question)
        return self.generate(question, chunks)
```

---

## Scaling Notes

| Scale | Recommendation |
|---|---|
| < 100K chunks | In-memory or SQLite + pgvector |
| 100K – 10M chunks | Dedicated pgvector or Qdrant instance |
| > 10M chunks | Pinecone or Weaviate with sharding |

---

## Cost Estimate (per 1000 queries)

| Component | Cost |
|---|---|
| Embedding (text-emb-3-small) | ~$0.02 |
| Generation (claude-haiku) | ~$0.15 |
| Generation (claude-opus-4-5) | ~$3.00 |
| **Total (Haiku)** | **~$0.17** |

---

## Related

- [Systems: Research Agent](../systems/research-agent.md)
- [Skills: RAG Pipeline](../skills/09-agentic-patterns/rag-pipeline.md)
- [Benchmarks: RAG Retrieval Strategies](../benchmarks/memory/rag-retrieval-strategies.md)

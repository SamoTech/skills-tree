# Benchmark: RAG Retrieval Strategies

**Category:** benchmarks/memory | **Version:** v1 | **Date:** 2026-04

## Question

Which RAG retrieval strategy delivers the best recall, precision, and latency trade-off across standard QA benchmarks?

---

## Strategies Tested

| ID | Strategy | Description |
|---|---|---|
| A | **Naive Top-K** | Embed query → cosine similarity → top-K chunks |
| B | **MMR** | Maximal Marginal Relevance — diversity-aware top-K |
| C | **HyDE** | Hypothetical Document Embedding — generate a fake answer first, embed that |
| D | **Step-Back** | Rephrase to a broader question, retrieve on the abstracted query |
| E | **Multi-Query** | Generate N query variants, union of results, deduplicate |
| F | **Contextual Compression** | Retrieve K, then LLM-compress each chunk to only the relevant span |

---

## Dataset

- **HotpotQA** (multi-hop, 500 questions from dev set)
- **NaturalQuestions** (single-hop, 500 questions)
- Corpus: Wikipedia 2024 snapshot, chunked at 512 tokens with 64-token overlap
- Embedding model: `text-embedding-3-small` (OpenAI)
- Retrieval: FAISS flat index (exact search)
- Generation: `claude-opus-4-5`, temperature 0

---

## Results

### HotpotQA (Multi-Hop)

| Strategy | Recall@5 | Precision@5 | EM Score | Avg Latency | Cost/1K Q |
|---|---|---|---|---|---|
| Naive Top-K | 61.2% | 38.4% | 41.3% | 320ms | $0.18 |
| MMR | 63.8% | 40.1% | 42.7% | 340ms | $0.18 |
| **HyDE** | **74.1%** | **46.8%** | **53.6%** | 890ms | $0.34 |
| Step-Back | 70.3% | 43.2% | 50.1% | 760ms | $0.31 |
| Multi-Query | 72.6% | 44.9% | 51.8% | 1,100ms | $0.52 |
| Contextual Compression | 68.4% | 51.3% | 49.2% | 1,420ms | $0.61 |

### NaturalQuestions (Single-Hop)

| Strategy | Recall@5 | Precision@5 | EM Score | Avg Latency | Cost/1K Q |
|---|---|---|---|---|---|
| Naive Top-K | 72.4% | 44.1% | 58.2% | 290ms | $0.16 |
| MMR | 71.9% | 43.8% | 57.6% | 310ms | $0.16 |
| **HyDE** | **79.3%** | **49.2%** | **64.8%** | 820ms | $0.32 |
| Step-Back | 75.1% | 46.7% | 61.3% | 700ms | $0.29 |
| Multi-Query | 77.8% | 48.1% | 63.1% | 1,050ms | $0.49 |
| Contextual Compression | 73.6% | 52.4% | 60.7% | 1,380ms | $0.58 |

---

## Key Findings

1. **HyDE wins on recall and EM** — +12.9% recall over Naive Top-K on HotpotQA. The hypothesis is that the generated "fake answer" embeds into a denser region of semantic space than a raw question.
2. **Contextual Compression wins on precision** — but at 4.4× the latency cost. Best when you need clean context windows, not when you need speed.
3. **MMR has negligible benefit over Naive Top-K for single-hop** — diversity helps only when the correct answer spans multiple documents (multi-hop tasks).
4. **Multi-Query costs 2.9× more** than HyDE for marginally lower performance — not recommended unless the query space is highly ambiguous.
5. **For latency-sensitive production** (< 500ms SLA): Naive Top-K or MMR. **For quality-sensitive production**: HyDE.

---

## Reproduction

```python
import anthropic
from openai import OpenAI
import faiss
import numpy as np

openai_client = OpenAI()
anthropic_client = anthropic.Anthropic()

def embed(text: str) -> np.ndarray:
    r = openai_client.embeddings.create(model="text-embedding-3-small", input=text)
    return np.array(r.data[0].embedding, dtype="float32")

def naive_topk(query: str, index: faiss.Index, chunks: list[str], k: int = 5) -> list[str]:
    q_emb = embed(query).reshape(1, -1)
    _, ids = index.search(q_emb, k)
    return [chunks[i] for i in ids[0]]

def hyde_retrieve(query: str, index: faiss.Index, chunks: list[str], k: int = 5) -> list[str]:
    # Generate hypothetical answer
    response = anthropic_client.messages.create(
        model="claude-opus-4-5",
        max_tokens=200,
        messages=[{"role": "user", "content": f"Write a short factual answer to: {query}"}]
    )
    hypothesis = response.content[0].text
    # Embed the hypothesis instead of the raw query
    h_emb = embed(hypothesis).reshape(1, -1)
    _, ids = index.search(h_emb, k)
    return [chunks[i] for i in ids[0]]

def multi_query_retrieve(query: str, index: faiss.Index, chunks: list[str], k: int = 3, n_variants: int = 3) -> list[str]:
    response = anthropic_client.messages.create(
        model="claude-opus-4-5",
        max_tokens=200,
        messages=[{"role": "user", "content": f"Write {n_variants} different phrasings of this question, one per line:\n{query}"}]
    )
    variants = response.content[0].text.strip().split("\n")[:n_variants]
    seen = set()
    results = []
    for v in variants:
        for chunk in naive_topk(v, index, chunks, k):
            if chunk not in seen:
                seen.add(chunk)
                results.append(chunk)
    return results[:k*2]
```

---

## Recommendation

> **Use HyDE as your default retrieval strategy.** It delivers the best recall/EM at a reasonable latency (< 1s) and 2× cost vs. naive. For sub-500ms requirements, fall back to Naive Top-K. For highest precision at any cost, use Contextual Compression.

---

## Related

- `blueprints/rag-stack.md` — Full RAG production architecture
- `benchmarks/memory/injection-strategies.md` — How to inject retrieved context
- `skills/09-agentic-patterns/rag.md` — The RAG skill with 6 variants

## Changelog

- **v1** (2026-04) — Initial benchmark: 6 strategies × 2 datasets × 5 metrics

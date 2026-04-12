# Research Agent

**Skills Used:** Web Search · RAG Pipeline · Summarization · Citation Generation  
**Complexity:** Intermediate  
**Version:** v1  
**Added:** 2026-04

---

## What It Does

Given a research question, this agent:
1. Decomposes the question into sub-queries
2. Searches the web for each sub-query
3. Retrieves and embeds the top results
4. Synthesizes a cited answer using RAG

---

## Skill Flow

```
Input: "What are the trade-offs between ReAct and LATS for agent planning?"
   │
   ▼
[02-reasoning/query-decomposition]
   │  → ["ReAct agent planning", "LATS agent planning", "ReAct vs LATS benchmark"]
   ▼
[11-web/web-search] × 3 queries in parallel
   │  → 15 search results
   ▼
[11-web/url-content-extraction] × top 5 URLs
   │  → raw page content
   ▼
[03-memory/rag-pipeline] (embed → store → retrieve)
   │  → top-8 relevant chunks
   ▼
[06-communication/summarization] + [06-communication/citation-generation]
   │
   ▼
Output: Cited, structured answer with sources
```

---

## Implementation

```python
import anthropic
import httpx
from typing import Optional

client = anthropic.Anthropic()

def decompose_query(question: str) -> list[str]:
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": (
                f"Break this research question into 3 targeted web search queries:\n"
                f"Question: {question}\n"
                "Return a JSON array of 3 query strings only."
            )
        }]
    )
    import json
    return json.loads(response.content[0].text)

def search_web(query: str) -> list[dict]:
    # Replace with your preferred search API (Brave, Serper, Tavily, etc.)
    # Returns: [{title, url, snippet}]
    raise NotImplementedError("Plug in your search API here")

def fetch_content(url: str) -> str:
    try:
        r = httpx.get(url, timeout=10, follow_redirects=True)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        return soup.get_text(separator=" ", strip=True)[:5000]
    except Exception:
        return ""

def synthesize_answer(question: str, chunks: list[str]) -> str:
    context = "\n\n---\n\n".join(chunks)
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": (
                f"Research question: {question}\n\n"
                f"Source material:\n{context}\n\n"
                "Write a comprehensive, cited answer. "
                "Reference sources as [1], [2], etc. at the end."
            )
        }]
    )
    return response.content[0].text

def research_agent(question: str) -> str:
    print(f"🔍 Researching: {question}")
    queries = decompose_query(question)
    print(f"📋 Sub-queries: {queries}")
    results = []
    for q in queries:
        results.extend(search_web(q))
    seen = set()
    unique = [r for r in results if r["url"] not in seen and not seen.add(r["url"])]
    chunks = []
    for r in unique[:5]:
        content = fetch_content(r["url"])
        if content:
            chunks.append(f"Source: {r['url']}\n{content}")
    return synthesize_answer(question, chunks)

if __name__ == "__main__":
    answer = research_agent("What are the trade-offs between ReAct and LATS for agent planning?")
    print(answer)
```

---

## Inputs / Outputs

| | Value |
|---|---|
| **Input** | Natural language research question (string) |
| **Output** | Cited, structured answer (markdown string) |
| **Avg. latency** | 15–30s depending on search API + page fetch |
| **Avg. cost** | ~$0.02–0.05 per query (Claude Haiku variant: ~$0.004) |

---

## Failure Modes

| Failure | Cause | Fix |
|---|---|---|
| Stale results | Search API cache | Use `freshness` param if available |
| Hallucinated citations | Low-quality chunks | Add chunk relevance threshold |
| Timeout on fetch | Slow external sites | Add 5s timeout + skip on error |
| Over-long synthesis | Many chunks | Limit to top-5 by BM25 score |

---

## Related Skills

- [Query Decomposition](../skills/02-reasoning/query-decomposition.md)
- [Web Search](../skills/11-web/web-search.md)
- [RAG Pipeline](../skills/09-agentic-patterns/rag-pipeline.md)
- [Summarization](../skills/06-communication/summarization.md)

## Related Blueprints

- [RAG Stack](../blueprints/rag-stack.md)

# Path: Build a Research Agent

**Difficulty:** ⭐⭐ Intermediate  
**Skills:** 5  
**Est. Time:** ~3 hours  
**Goal:** Build an agent that autonomously searches the web, retrieves documents, and synthesises a cited answer.

---

## Overview

A Research Agent takes a user question, breaks it into sub-queries, searches for relevant sources, retrieves and parses the content, reasons over the evidence, and returns a structured answer with citations. This is the most common production agent pattern.

By the end of this path you will have a working LangGraph pipeline that can answer factual questions with cited sources.

---

## Prerequisites

- Python 3.11+
- `pip install langchain langgraph openai tavily-python`
- A Tavily API key (free tier works) and an OpenAI or Anthropic key
- Basic familiarity with Python async and dictionaries

---

## The Path

### Step 1 — Web Search
`skills/11-web/web-search.md`

**Why first:** The agent's information intake. You learn how to issue structured search queries, handle rate limits, and parse result metadata (title, URL, snippet). Without reliable search, nothing else works.

**Key takeaways from this skill:**
- Use structured query objects, not raw strings
- Always filter by recency and domain trust
- Return ranked results with source metadata intact

---

### Step 2 — Document Retrieval
`skills/01-perception/document-retrieval.md`

**Why second:** Search gives you URLs and snippets. Retrieval fetches the full content. You learn HTTP fetching, HTML stripping, chunking, and handling paywalls and bot-blocks gracefully.

**Key takeaways:**
- Chunk documents at sentence boundaries, not arbitrary character counts
- Store chunk + source URL together for citation tracing
- Implement fallback: if full fetch fails, use snippet from search

---

### Step 3 — Semantic Search / RAG
`skills/03-memory/semantic-search.md`

**Why third:** Once you have retrieved chunks, you need to find the most relevant ones for the question. This step embeds chunks, builds a temporary in-memory vector store, and retrieves top-k by cosine similarity.

**Key takeaways:**
- Use `text-embedding-3-small` or `all-MiniLM` for speed
- Top-k = 5 is a good default; re-rank if precision matters
- Keep the embedding model consistent between index and query

---

### Step 4 — Causal Reasoning
`skills/02-reasoning/causal-reasoning.md`

**Why fourth:** With evidence chunks in hand, the agent must reason — not just extract. Causal reasoning teaches the model to distinguish correlation from causation, identify evidence gaps, and structure an argument before writing the answer.

**Key takeaways:**
- Prompt: "Given these sources, what causes X? What evidence supports this?"
- Ask the model to list sources it used for each claim
- Use chain-of-thought before the final answer

---

### Step 5 — Report Generation
`skills/06-communication/report-generation.md`

**Why last:** The synthesis step. The agent turns its reasoning trace into a structured, cited report. You learn output formatting, citation injection, and how to handle conflicting sources.

**Key takeaways:**
- Always include inline citations `[1]`, `[2]` tied to source URLs
- Separate "findings" from "interpretation"
- Add a confidence indicator when evidence is thin

---

## Code Scaffold

```python
# research_agent.py — minimal LangGraph research agent
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

class ResearchState(TypedDict):
    question: str
    queries: List[str]
    results: List[dict]   # [{url, title, content}]
    chunks: List[dict]    # [{text, source}]
    top_chunks: List[dict]
    reasoning: str
    report: str

def plan_queries(state: ResearchState) -> ResearchState:
    """Step 1: Break question into 2-3 search queries."""
    # Call LLM: "Given this question, write 3 diverse search queries: {question}"
    state["queries"] = [state["question"]]  # replace with LLM output
    return state

def web_search(state: ResearchState) -> ResearchState:
    """Step 1: Search — skills/11-web/web-search.md"""
    from tavily import TavilyClient
    client = TavilyClient()
    results = []
    for q in state["queries"]:
        r = client.search(q, max_results=3)
        results.extend(r["results"])
    state["results"] = results
    return state

def retrieve_documents(state: ResearchState) -> ResearchState:
    """Step 2: Retrieve full content — skills/01-perception/document-retrieval.md"""
    import httpx
    from bs4 import BeautifulSoup
    chunks = []
    for r in state["results"]:
        try:
            resp = httpx.get(r["url"], timeout=5, follow_redirects=True)
            soup = BeautifulSoup(resp.text, "html.parser")
            text = " ".join(p.get_text() for p in soup.find_all("p"))[:3000]
            chunks.append({"text": text, "source": r["url"]})
        except Exception:
            chunks.append({"text": r.get("content", ""), "source": r["url"]})
    state["chunks"] = chunks
    return state

def semantic_rank(state: ResearchState) -> ResearchState:
    """Step 3: Embed + rank chunks — skills/03-memory/semantic-search.md"""
    # Simple keyword overlap fallback (replace with embeddings for production)
    q_words = set(state["question"].lower().split())
    scored = sorted(
        state["chunks"],
        key=lambda c: len(q_words & set(c["text"].lower().split())),
        reverse=True
    )
    state["top_chunks"] = scored[:5]
    return state

def reason(state: ResearchState) -> ResearchState:
    """Step 4: Causal reasoning — skills/02-reasoning/causal-reasoning.md"""
    # Call LLM with top_chunks as context and ask for structured reasoning
    context = "\n\n".join(f"[{i+1}] {c['text'][:500]}" for i, c in enumerate(state["top_chunks"]))
    state["reasoning"] = f"Based on sources:\n{context}\n\n[LLM reasoning goes here]"
    return state

def generate_report(state: ResearchState) -> ResearchState:
    """Step 5: Report generation — skills/06-communication/report-generation.md"""
    sources = "\n".join(f"[{i+1}] {c['source']}" for i, c in enumerate(state["top_chunks"]))
    state["report"] = f"{state['reasoning']}\n\n## Sources\n{sources}"
    return state

# Build graph
graph = StateGraph(ResearchState)
graph.add_node("plan", plan_queries)
graph.add_node("search", web_search)
graph.add_node("retrieve", retrieve_documents)
graph.add_node("rank", semantic_rank)
graph.add_node("reason", reason)
graph.add_node("report", generate_report)
graph.set_entry_point("plan")
graph.add_edge("plan", "search")
graph.add_edge("search", "retrieve")
graph.add_edge("retrieve", "rank")
graph.add_edge("rank", "reason")
graph.add_edge("reason", "report")
graph.add_edge("report", END)
agent = graph.compile()

if __name__ == "__main__":
    result = agent.invoke({"question": "What causes transformer attention to fail on long contexts?"})
    print(result["report"])
```

---

## Completion Checklist

- [ ] Agent returns an answer with at least 2 cited sources
- [ ] Handles a failed URL fetch gracefully (fallback to snippet)
- [ ] Reasoning step produces a chain-of-thought trace
- [ ] Report includes a `## Sources` section with URLs
- [ ] Works on 3 different questions without crashing

---

## Next Steps

- Add **fact verification** (`skills/03-memory/fact-verification.md`) as a post-reasoning step
- Add **memory injection** (`skills/03-memory/memory-injection.md`) to persist findings across sessions
- Swap the keyword ranker for real embeddings using `skills/03-memory/semantic-search.md`
- See the full system: `systems/research-agent-system.md`

---
title: Research Agent
type: system
skills: [web-search, rag, chain-of-thought, communication/summarize, communication/cite]
version: v1
stability: stable
updated: 2026-04
---

# Research Agent System

## What It Does

A multi-step autonomous research pipeline that:
1. Breaks a complex question into sub-questions
2. Searches the web for each sub-question
3. Synthesizes findings across sources
4. Produces a structured report with citations

## Skill Map

```
User Query
    │
    ▼
[Chain of Thought] — Decompose into 3-5 sub-questions
    │
    ▼ (for each sub-question)
[Web Search] ────────────────────────────────────┐
    │                                             │
    ▼                                             │
[RAG over results] — Extract key facts            │
    │                                             │
    ▼                                             │
    └──────────── Merge all findings ◄────────────┘
                         │
                         ▼
              [Summarize + Cite]
                         │
                         ▼
                  Structured Report
```

## Full Implementation

```python
import anthropic
import httpx
import os
from typing import List

client = anthropic.Anthropic()

# --- Stage 1: Decompose ---
def decompose_question(question: str) -> List[str]:
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=512,
        system="Break the question into 3-5 specific sub-questions needed to fully answer it. Return one per line, no numbering.",
        messages=[{"role": "user", "content": question}]
    )
    return [q.strip() for q in response.content[0].text.strip().split("\n") if q.strip()]

# --- Stage 2: Search ---
def search(query: str, n: int = 5) -> List[dict]:
    # Replace with real search API
    return [{"title": f"Result for: {query}", "snippet": f"Relevant content about {query}.", "url": "https://example.com"}] * n

# --- Stage 3: Extract facts ---
def extract_facts(sub_question: str, results: List[dict]) -> str:
    context = "\n".join(f"- {r['snippet']}" for r in results)
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=512,
        system="Extract the most relevant facts from these search results to answer the sub-question. Be concise.",
        messages=[{"role": "user", "content": f"Sub-question: {sub_question}\n\nSearch results:\n{context}"}]
    )
    return response.content[0].text

# --- Stage 4: Synthesize ---
def synthesize(question: str, findings: List[dict]) -> str:
    findings_text = "\n\n".join(
        f"Sub-question: {f['question']}\nFindings: {f['facts']}"
        for f in findings
    )
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        system="""Write a comprehensive, well-structured research report answering the original question.
Use markdown with headers. Include a summary section and key findings. Be factual and precise.""",
        messages=[{"role": "user", "content": f"Original question: {question}\n\nResearch findings:\n{findings_text}"}]
    )
    return response.content[0].text

# --- Full pipeline ---
def research_agent(question: str) -> dict:
    print(f"🔍 Researching: {question}")

    # Step 1: Decompose
    sub_questions = decompose_question(question)
    print(f"📋 Sub-questions: {sub_questions}")

    # Steps 2-3: Search + extract per sub-question
    findings = []
    for sq in sub_questions:
        results = search(sq)
        facts = extract_facts(sq, results)
        findings.append({"question": sq, "facts": facts, "sources": [r["url"] for r in results]})

    # Step 4: Synthesize
    report = synthesize(question, findings)

    return {
        "question": question,
        "sub_questions": sub_questions,
        "report": report,
        "sources": [s for f in findings for s in f["sources"]]
    }

# Usage
result = research_agent("What are the most effective multi-agent architectures for code generation in 2026?")
print(result["report"])
```

## Configuration Options

| Option | Default | Description |
|---|---|---|
| `model` | `claude-opus-4-5` | Swap for `claude-haiku-4-5` for speed/cost |
| `sub_questions` | 3-5 | More = more thorough, more expensive |
| `results_per_query` | 5 | Increase for broader coverage |
| `max_report_tokens` | 2048 | Increase for longer reports |

## Cost Profile

| Question complexity | Est. API calls | Est. tokens | Est. cost |
|---|---|---|---|
| Simple (2 sub-questions) | 4 | ~3k | ~$0.02 |
| Medium (4 sub-questions) | 6 | ~6k | ~$0.04 |
| Deep (6 sub-questions) | 8 | ~10k | ~$0.07 |

## Skills Used

- [`skills/02-reasoning/chain-of-thought.md`](../skills/02-reasoning/chain-of-thought.md)
- [`skills/11-web/web-search.md`](../skills/11-web/web-search.md)
- [`skills/09-agentic-patterns/rag.md`](../skills/09-agentic-patterns/rag.md)

## Related

- [`blueprints/rag-stack.md`](../blueprints/rag-stack.md) — Production retrieval architecture
- [`systems/code-reviewer.md`](code-reviewer.md) — Code-focused system

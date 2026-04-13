---
title: Web Search
category: 11-web
level: basic
stability: stable
added: "2025-03"
description: "Apply web search in AI agent workflows."
version: v2
tags: [web, search, retrieval, tool-use]
updated: 2026-04
---


![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-11-web-web-search.json)

# Web Search

## What It Does

Enables an agent to query the live web and incorporate current, factual information into its responses. Bridges the gap between the model's training cutoff and today's reality.

## When to Use

- Questions about current events, prices, availability
- Research tasks requiring multiple sources
- Fact-checking and citation gathering
- Any task where training data is stale or insufficient

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `query` | `str` | The search query |
| `num_results` | `int` | How many results to fetch (default: 5) |
| `provider` | `str` | `brave`, `serper`, `tavily`, `bing` |
| → `results` | `list[dict]` | `{title, url, snippet}` per result |
| → `answer` | `str` | Synthesized answer with citations |

## Runnable Example

```python
import anthropic
import httpx
import os

client = anthropic.Anthropic()

def brave_search(query: str, num_results: int = 5) -> list:
    """Call Brave Search API"""
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": os.environ["BRAVE_API_KEY"]
    }
    resp = httpx.get(
        "https://api.search.brave.com/res/v1/web/search",
        params={"q": query, "count": num_results},
        headers=headers
    )
    results = resp.json().get("web", {}).get("results", [])
    return [{"title": r["title"], "url": r["url"], "snippet": r["description"]} for r in results]

def search_and_answer(query: str) -> dict:
    # Define tool for the model
    search_tool = {
        "name": "web_search",
        "description": "Search the web for current information",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"]
        }
    }

    messages = [{"role": "user", "content": query}]
    sources = []

    # Agentic loop
    while True:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            tools=[search_tool],
            system="Search the web to answer the question. Cite your sources with [1], [2], etc.",
            messages=messages
        )

        if response.stop_reason == "end_turn":
            break

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []

            for block in response.content:
                if block.type == "tool_use" and block.name == "web_search":
                    results = brave_search(block.input["query"])
                    sources.extend(results)
                    formatted = "\n".join(
                        f"[{i+1}] {r['title']}\n{r['snippet']}\nURL: {r['url']}"
                        for i, r in enumerate(results)
                    )
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": formatted
                    })

            messages.append({"role": "user", "content": tool_results})

    answer = "".join(
        block.text for block in response.content
        if hasattr(block, "text")
    )
    return {"answer": answer, "sources": sources}

result = search_and_answer("What are the most popular AI agent frameworks in 2026?")
print(result["answer"])
```

## Provider Comparison

| Provider | Free Tier | Latency | Best For |
|---|---|---|---|
| **Brave Search** | 2k/mo | ~300ms | Privacy-respecting, good coverage |
| **Serper** | 100/mo | ~200ms | Google results, fast |
| **Tavily** | 1k/mo | ~500ms | AI-optimized, returns clean snippets |
| **Bing Search API** | 1k/mo | ~250ms | Microsoft ecosystem |
| **SerpAPI** | 100/mo | ~400ms | Any search engine, flexible |

## Failure Modes

| Failure | Cause | Fix |
|---|---|---|
| Stale results | Cache hit from search provider | Add date filter to query (`after:2026-01-01`) |
| No results | Overly specific query | Broaden query; try 2-3 variants |
| Paywalled content | URL returns 403/paywall | Filter URLs before returning to model |
| Rate limit | Too many queries | Implement exponential backoff |

## Related Skills

- [`web-scraping.md`](web-scraping.md) — Extract full content from URLs
- [`react.md`](../02-reasoning/react.md) — Use search inside a ReAct loop
- [`rag.md`](../09-agentic-patterns/rag.md) — Search over private documents

## Changelog

| Version | Date | Change |
|---|---|---|
| v1 | 2025-04 | Initial entry |
| v2 | 2026-04 | Full agentic loop example, provider comparison table |

---
title: "Web Search"
category: 11-web
level: intermediate
stability: stable
added: "2025-03"
updated: "2026-04"
version: v3
description: "Query a search API (Tavily, Serper, Bing, Brave, Exa) and return ranked URLs + snippets. The agent's bridge to fresh, open-web information when its training cutoff or private corpus isn't enough."
tags: [web, search, retrieval, fresh-information]
dependencies:
  - package: httpx
    min_version: "0.28.0"
    tested_version: "0.28.1"
    confidence: verified
code_blocks:
  - id: "example-web-search"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-11-web-web-search.json)

# Web Search

## Description

Web search is the agent's escape hatch from the training cutoff: when it doesn't know, it searches. The contract is simple — query string in, ranked list of `(title, url, snippet, published_at)` out — but the choice of provider, query rewriting, and result re-ranking dictate whether the agent finds the answer or makes one up.

This skill wraps a single provider (Tavily by default — small, agent-tuned, returns clean snippets) behind a stable interface, then adds query rewriting, caching, and a host-allowlist guard. You can swap providers without touching the consumer.

## When to Use

- The question is about **fresh** events, prices, releases, news, or anything past the model's cutoff.
- The corpus is the **open web**, not a private collection (use [RAG](../03-memory/rag.md) for the latter).
- You need **citations** with publication dates — search APIs return both.
- **Don't use** when the question is purely conceptual (the model already knows), or when the answer must come from your own data.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `query` | `str` | Natural-language search query |
| `top_k` | `int` | Results to return (default 5) |
| `recency_days` | `int \| None` | Drop results older than this |
| `allowed_hosts` | `list[str] \| None` | Only return URLs whose host matches |
| → `results` | `list[SearchHit]` | Ranked results |
| → `results[i].url` | `str` | Canonical URL |
| → `results[i].title` | `str` | Page title |
| → `results[i].snippet` | `str` | Cleaned excerpt with the matched terms |
| → `results[i].published_at` | `str \| None` | ISO date if known |

## Runnable Example

```python
# pip install httpx
from __future__ import annotations
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse
import httpx

@dataclass
class SearchHit:
    url: str
    title: str
    snippet: str
    published_at: str | None
    score: float

_CACHE: dict[tuple, tuple[float, list[SearchHit]]] = {}
_CACHE_TTL_SEC = 60 * 5  # 5 minutes is usually fine for "fresh" queries

def web_search(
    query: str,
    *,
    top_k: int = 5,
    recency_days: int | None = None,
    allowed_hosts: list[str] | None = None,
    api_key: str | None = None,
    timeout: float = 10.0,
) -> list[SearchHit]:
    api_key = api_key or os.environ["TAVILY_API_KEY"]
    cache_key = (query, top_k, recency_days, tuple(allowed_hosts or ()))
    now = time.time()
    cached = _CACHE.get(cache_key)
    if cached and now - cached[0] < _CACHE_TTL_SEC:
        return cached[1]

    payload = {
        "api_key": api_key,
        "query": query,
        "max_results": max(top_k * 2, 10),  # over-fetch for filtering
        "include_raw_content": False,
        "search_depth": "basic",
    }
    r = httpx.post("https://api.tavily.com/search", json=payload, timeout=timeout)
    r.raise_for_status()
    raw = r.json().get("results", [])

    cutoff = (
        datetime.now(timezone.utc) - timedelta(days=recency_days)
        if recency_days else None
    )
    out: list[SearchHit] = []
    for h in raw:
        url = h["url"]
        if allowed_hosts and urlparse(url).netloc not in allowed_hosts:
            continue
        published = h.get("published_date")
        if cutoff and published:
            try:
                if datetime.fromisoformat(published.replace("Z", "+00:00")) < cutoff:
                    continue
            except ValueError:
                pass  # unknown format → don't drop
        out.append(SearchHit(
            url=url,
            title=h.get("title", "").strip(),
            snippet=h.get("content", "").strip(),
            published_at=published,
            score=float(h.get("score", 0.0)),
        ))
        if len(out) >= top_k:
            break

    _CACHE[cache_key] = (now, out)
    return out

if __name__ == "__main__":
    for h in web_search("claude opus latest model release", top_k=3, recency_days=180):
        print(f"{h.score:.2f}  {h.url}\n  {h.title}\n  {h.snippet[:160]}\n")
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Stale-but-popular pages outrank fresh ones | Provider's recency boost is weak | `recency_days` filter + sort by `published_at` for time-sensitive queries |
| Query is verbose / agent-style | Models write essays as queries | Rewrite query to ≤10 keywords before search |
| Provider rate-limited | Bursty agent loops | Cache, dedupe across the conversation, add backoff |
| Results from sketchy hosts | No allowlist | `allowed_hosts` for high-stakes domains (medical, legal, finance) |
| Snippet missing the actual answer | Search snippets are short | Pair with [Web Scraping](web-scraping.md) — fetch the URL on top hit |
| Costs balloon | Every step searches | Cache per (query, params) tuple; let agent decide when to search |

## Variants

| Variant | When |
|---|---|
| **Tavily** (above) | Agent-tuned; cheap; clean snippets |
| **Serper / SerpAPI** | Google SERP scraping; richer features (knowledge panel, news) |
| **Brave Search** | Independent index; privacy-friendly; cheap |
| **Bing Web Search** | Strong news; Azure-integrated |
| **Exa** | Vector-native; great for "find me similar pages" |
| **Two-step: search → scrape** | When snippets aren't enough |

## Frameworks & Models

| Framework | Notes |
|---|---|
| Direct API (above) | Maximum control |
| LangChain `TavilySearchResults` | Pre-baked agent tool |
| LlamaIndex `WebTool` | Same, retrieval-flavoured |
| OpenAI / Claude built-in browsing | Provider-managed; less control over hosts |

## Model Comparison

| Provider | Quality | Cost | Recency control |
|---|---|---|---|
| Tavily | 4 | 5 | 4 |
| Serper | 5 | 3 | 5 |
| Brave | 4 | 5 | 3 |
| Bing | 4 | 4 | 5 |
| Exa | 5 | 3 | 4 |

## Related Skills

- [Web Scraping](web-scraping.md) — fetch full page content for the top result
- [HTTP Request](../04-action-execution/http-request.md) — generic HTTP for non-search APIs
- [RAG](../03-memory/rag.md) — alternative when the corpus is private

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Stub |
| 2026-04 | v3 | Battle-tested: typed SearchHit, recency + host filters, TTL cache, provider comparison |

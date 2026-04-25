---
title: "Web Scraping"
category: 11-web
level: intermediate
stability: stable
added: "2025-03"
updated: "2026-04"
version: v3
description: "Fetch a URL and extract its main readable content + metadata. Pairs with web-search to follow promising hits, with HTML→Markdown conversion + boilerplate stripping so the output is LLM-friendly."
tags: [web, scraping, html, extraction, fetch]
dependencies:
  - package: httpx
    min_version: "0.28.0"
    tested_version: "0.28.1"
    confidence: verified
  - package: beautifulsoup4
    min_version: "4.12.0"
    tested_version: "4.12.3"
    confidence: verified
  - package: trafilatura
    min_version: "1.12.0"
    tested_version: "1.12.2"
    confidence: verified
code_blocks:
  - id: "example-web-scraping"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-11-web-web-scraping.json)

# Web Scraping

## Description

Web scraping pulls a URL and returns its **main readable content** as clean text or Markdown — stripped of nav, ads, footer, JS warnings, cookie banners. It's the second half of agentic browsing: web search picks the URL, scrape gets the actual answer.

Naive `requests.get(url).text` floods the LLM with chrome and JavaScript stubs. This skill uses `trafilatura` (state of the art readability extraction) with a `BeautifulSoup` fallback, follows redirects, sets a real User-Agent, respects timeouts, and returns metadata (title, author, published_at) so downstream RAG can cite it.

## When to Use

- You have a URL (from search, the user, or a previous answer) and need its **content**.
- The page is **server-rendered HTML** — most news, docs, blogs, GitHub, MDN, Wikipedia.
- The site permits scraping (check `robots.txt`; respect rate limits).
- **Don't use** for SPAs that render client-side (use a headless browser like Playwright instead), API-providing sites (use the API), or paywalled content.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `url` | `str` | Page to fetch |
| `output` | `Literal["markdown","text"]` | Format (default `markdown`) |
| `max_chars` | `int` | Truncate to fit context (default 20000) |
| `user_agent` | `str` | Identify yourself (default `skills-tree/1.0`) |
| → `title` | `str` | Page title |
| → `content` | `str` | Cleaned main content |
| → `author` | `str \| None` | If detected |
| → `published_at` | `str \| None` | ISO date if detected |
| → `final_url` | `str` | After redirects |

## Runnable Example

```python
# pip install httpx beautifulsoup4 trafilatura
from __future__ import annotations
from dataclasses import dataclass
import httpx
import trafilatura
from bs4 import BeautifulSoup

DEFAULT_UA = "skills-tree/1.0 (+https://github.com/SamoTech/skills-tree)"

@dataclass
class ScrapeResult:
    url: str
    final_url: str
    title: str
    content: str
    author: str | None
    published_at: str | None

def fetch(url: str, *, user_agent: str = DEFAULT_UA, timeout: float = 15.0) -> tuple[str, str]:
    with httpx.Client(
        follow_redirects=True,
        headers={"User-Agent": user_agent, "Accept-Language": "en;q=0.9,*;q=0.5"},
        timeout=timeout,
    ) as client:
        r = client.get(url)
    r.raise_for_status()
    return r.text, str(r.url)

def _bs4_fallback(html: str) -> tuple[str, str]:
    """Extractor of last resort if trafilatura returns nothing."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "aside", "noscript"]):
        tag.decompose()
    title = soup.title.text.strip() if soup.title else ""
    body = soup.find("article") or soup.find("main") or soup.body or soup
    text = "\n".join(line.strip() for line in body.get_text("\n").splitlines() if line.strip())
    return title, text

def scrape(
    url: str,
    *,
    output: str = "markdown",
    max_chars: int = 20000,
    user_agent: str = DEFAULT_UA,
) -> ScrapeResult:
    html, final_url = fetch(url, user_agent=user_agent)
    extracted = trafilatura.extract(
        html,
        url=final_url,
        output_format="markdown" if output == "markdown" else "txt",
        include_links=False,
        include_images=False,
    )
    meta = trafilatura.extract_metadata(html)
    title = (meta.title if meta and meta.title else "").strip()
    author = meta.author if meta else None
    published = meta.date if meta else None

    if not extracted or len(extracted.strip()) < 200:
        title, extracted = _bs4_fallback(html)

    extracted = (extracted or "").strip()
    if len(extracted) > max_chars:
        extracted = extracted[: max_chars] + "\n\n…[truncated]"

    return ScrapeResult(
        url=url, final_url=final_url, title=title,
        content=extracted, author=author, published_at=published,
    )

if __name__ == "__main__":
    out = scrape("https://en.wikipedia.org/wiki/Retrieval-augmented_generation")
    print(f"title: {out.title}")
    print(f"author: {out.author}  published: {out.published_at}")
    print("---")
    print(out.content[:600])
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Empty content | SPA renders client-side | Fall back to headless browser (Playwright / Puppeteer) |
| 403 Forbidden | Site blocks default UAs / no JS | Set realistic User-Agent; respect `robots.txt`; some sites require JS |
| Garbage encoding (mojibake) | Wrong charset detection | `httpx` honours `content-type`; for legacy sites, force `r.encoding="utf-8"` |
| Boilerplate leaks (cookie banners) | Trafilatura missed it | Layer a regex post-filter; or use the BS4 fallback with explicit selectors |
| Hits the site too fast | No rate limiting | Per-host token bucket; sleep between calls |
| Login wall | Page requires auth | Don't scrape; use the API or skip |
| Truncation drops the answer | `max_chars` too small | Chunk + retrieve, not truncate, for large pages |

## Variants

| Variant | When |
|---|---|
| **Trafilatura** (above) | Default for static HTML; best readability extraction |
| **BeautifulSoup + selectors** | Site has a stable DOM structure you can target |
| **Playwright / Puppeteer** | JS-rendered SPAs (React, Vue, Angular) |
| **Reader API** (Diffbot, Mercury, Jina-reader) | Outsource the readability problem |
| **Sitemap-driven crawl** | Bulk: parse `sitemap.xml` and scrape each |

## Frameworks & Models

| Framework | Notes |
|---|---|
| Direct (above) | Maximum control |
| `requests-html` | Built-in JS rendering for simple cases |
| Scrapy | Production crawler with throttling, dedup, persistence |
| Playwright | Full browser; slow but handles anything |
| Jina Reader (`r.jina.ai/<url>`) | Hosted; free quota; one-line scrape |

## Related Skills

- [Web Search](web-search.md) — picks the URL to scrape
- [HTML Reading](../01-perception/html-reading.md) — parsing structured pages
- [HTTP Request](../04-action-execution/http-request.md) — generic non-HTML fetches
- [Rate Limiting](../14-security/rate-limiting.md) — be a good citizen

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Stub |
| 2026-04 | v3 | Battle-tested: trafilatura + BS4 fallback, metadata extraction, redirect handling, failure modes |

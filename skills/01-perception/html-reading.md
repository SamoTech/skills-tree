---
title: "HTML Reading"
category: 01-perception
level: basic
stability: stable
description: "Enable AI agents to parse HTML documents into structured DOM trees, extract text content, links, and semantic elements for web scraping and content analysis workflows."
added: "2025-03"
version: "v2"
last_updated: "2026-07"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-html-reading.json)

# HTML Reading

**Category:** `01-perception`
**Skill Level:** `basic`
**Stability:** `stable`
**Version:** `v2`
**Added:** `2025-03`
**Last Updated:** `2026-07`

---

## Description

HTML Reading enables an agent to parse raw HTML markup into a queryable DOM structure, extract clean text, follow hyperlinks, and identify semantic elements such as headings, tables, forms, and metadata. It is the foundational skill for web scraping agents, research assistants, and any pipeline that ingests content from web pages. The skill supports both static HTML and dynamic content via browser rendering.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `source` | `string` | ✅ | Raw HTML string, file path, or URL |
| `source_type` | `string` | ❌ | `html_string` \| `file` \| `url` (auto-detected) |
| `selector` | `string` | ❌ | CSS selector to target a specific DOM subtree |
| `extract` | `string` | ❌ | `text` \| `links` \| `tables` \| `metadata` \| `all` (default: `text`) |
| `render_js` | `bool` | ❌ | Render JavaScript before parsing (requires Playwright/Selenium; default: false) |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `text` | `string` | Clean plain text content (tags stripped) |
| `links` | `list[dict]` | Extracted hyperlinks `[{"text": "...", "href": "..."}]` |
| `tables` | `list[list[list[string]]]` | Tables as 2D arrays of cell strings |
| `metadata` | `dict` | `<meta>` tags: title, description, og:*, charset, etc. |
| `headings` | `list[dict]` | Heading hierarchy `[{"level": 1, "text": "..."}]` |

---

## Example

```python
from bs4 import BeautifulSoup
import requests

def read_html(source: str, extract: str = "text", selector: str = None) -> dict:
    if source.startswith("http"):
        html = requests.get(source, timeout=10).text
    elif source.endswith(".html"):
        with open(source) as f:
            html = f.read()
    else:
        html = source

    soup = BeautifulSoup(html, "lxml")
    if selector:
        soup = soup.select_one(selector) or soup

    result = {}
    if extract in ("text", "all"):
        result["text"] = soup.get_text(separator=" ", strip=True)
    if extract in ("links", "all"):
        result["links"] = [{"text": a.get_text(strip=True), "href": a.get("href", "")}
                           for a in soup.find_all("a", href=True)]
    if extract in ("metadata", "all"):
        result["metadata"] = {m.get("name", m.get("property", "")): m.get("content", "")
                               for m in soup.find_all("meta") if m.get("content")}
    if extract in ("tables", "all"):
        result["tables"] = [[[td.get_text(strip=True) for td in tr.find_all(["td","th"])]
                              for tr in table.find_all("tr")]
                             for table in soup.find_all("table")]
    return result

result = read_html("https://example.com", extract="all")
print(result["metadata"])
# → {"description": "Example Domain", "og:title": "Example", ...}
```

```python
# Extended — JavaScript-rendered page via Playwright
from playwright.sync_api import sync_playwright

def read_dynamic_html(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state("networkidle")
        html = page.content()
        browser.close()
    return BeautifulSoup(html, "lxml").get_text(separator=" ", strip=True)
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| Python `beautifulsoup4` | `BeautifulSoup(html, "lxml")` — industry-standard HTML parser | v1 |
| Python `lxml` | Fast C-based HTML/XML parser, used as bs4 backend | v1 |
| Python `httpx` / `requests` | HTTP client to fetch HTML from URLs | v1 |
| Playwright | Full browser rendering for JS-heavy pages | v1 |
| Selenium | Alternative browser automation for dynamic content | v1 |
| LangChain `WebBaseLoader` | `BeautifulSoup`-based loader for LLM pipelines | v0.1 |
| LlamaIndex `SimpleWebPageReader` | Fetches and cleans HTML for indexing | v0.8 |
| GPT-4o | Reads raw HTML natively; strong at extracting structured content | 2024-05 |
| Claude 3.7 Sonnet | Excellent at HTML table extraction and semantic understanding | 2025-01 |

---

## Model Comparison

| Capability | GPT-4o | Claude 3.7 Sonnet | Gemini 2.0 Flash | Notes |
|---|---|---|---|---|
| Text extraction accuracy | 5 | 5 | 4 | |
| Table parsing from HTML | 4 | 5 | 4 | Claude handles nested tables better |
| Metadata extraction | 5 | 5 | 4 | |
| JS-rendered content | 2 | 2 | 2 | All models need browser rendering for SPA pages |
| Instruction following | 5 | 5 | 4 | |

---

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Empty content | JavaScript-rendered SPA returns empty `<body>` | Use Playwright with `wait_for_load_state("networkidle")` |
| Encoding errors | Non-UTF-8 pages (Latin-1, GB2312) | Detect with `chardet`; pass `from_encoding` to bs4 |
| Excessive boilerplate | Navigation, ads, and footers dominate extracted text | Use `selector` to target `<main>` or `<article>` |
| Broken HTML | Malformed tags cause parse tree inconsistencies | Use `lxml` parser which is more fault-tolerant than `html.parser` |
| Rate limiting / bot detection | Too many requests to the same domain | Respect `robots.txt`; add delays; rotate user-agents |

---

## Prompt Patterns

### Pattern 1 — Content Extraction
```
Extract the main article content from this HTML page.
Ignore navigation, ads, headers, and footers.
Return only the article title and body text.

HTML:
{html_content}
```

### Pattern 2 — Link Extraction
```
From this HTML, extract all hyperlinks.
For each link return: {"text": "...", "href": "...", "is_internal": true/false}
Base URL: {base_url}

HTML:
{html_content}
```

### Pattern 3 — Table Extraction
```
Find all tables in this HTML and convert them to JSON.
Each table should be: {"headers": [...], "rows": [[...], ...]}

HTML:
{html_content}
```

---

## Notes

- Always use `lxml` as the bs4 parser — it is significantly faster and more tolerant of broken HTML than `html.parser`.
- Respect `robots.txt` and `Crawl-delay` headers when scraping public sites.
- For large-scale scraping, use `scrapy` instead of `requests` + bs4 for built-in rate limiting and middleware.
- Extracted text from `<script>` and `<style>` tags must be explicitly removed — bs4 does not strip them by default in `get_text()`.

---

## Related Skills

- [URL DOM Inspection](./url-dom-inspection.md) — live browser-based DOM querying
- [Document Parsing](./document-parsing.md) — for HTML files treated as documents
- [API Response Parsing](./api-response-parsing.md) — REST APIs often return HTML fragments
- [Table Extraction](./table-extraction.md) — specialized table parsing from HTML and images

---

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-04` | v1 | Initial entry |
| `2026-07` | v2 | Added typed I/O tables, extended examples, full frameworks table, model comparison, prompt patterns, detailed failure modes |

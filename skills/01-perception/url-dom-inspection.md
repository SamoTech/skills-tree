---
title: "URL / DOM Inspection"
category: 01-perception
level: intermediate
stability: stable
description: "Apply url / dom inspection in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-url-dom-inspection.json)

# URL / DOM Inspection

**Category:** `perception`  
**Skill Level:** `intermediate`  
**Stability:** `stable`  
**Added:** 2025-03  
**Last Updated:** 2026-04

---

## Description

Fetch web pages and inspect their DOM structure, metadata, and rendered content. Extracts titles, headings, links, Open Graph tags, structured data (JSON-LD, microdata), main body text, and interactive element inventory. Used in web agents for page comprehension before taking action, and in scrapers for extracting targeted data without brittle XPath selectors.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `url` | `string` | ✅ | Public URL to fetch and inspect |
| `extract` | `list` | ❌ | Fields to extract: `text`, `links`, `meta`, `structured_data` |
| `rendered` | `bool` | ❌ | Use Playwright for JS-rendered pages (default: false) |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `page_type` | `string` | Detected page type (article, product, landing, etc.) |
| `main_topic` | `string` | Primary subject of the page |
| `key_entities` | `list` | Names, orgs, products mentioned |
| `has_login_form` | `bool` | Whether a login form is present |
| `summary` | `string` | One-paragraph page summary |

---

## Example

```python
import anthropic
import httpx
from bs4 import BeautifulSoup
import json

client = anthropic.Anthropic()

def inspect_url(url: str) -> dict:
    """Fetch a URL and return structured page intelligence."""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; SkillsBot/1.0)"}
    r = httpx.get(url, headers=headers, follow_redirects=True, timeout=15)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.find("title")
    title = title.get_text(strip=True) if title else ""
    meta_desc = soup.find("meta", attrs={"name": "description"})
    description = meta_desc["content"] if meta_desc else ""
    headings = [h.get_text(strip=True) for h in soup.find_all(["h1","h2","h3"])[:20]]
    body_text = soup.get_text(separator=" ", strip=True)[:5000]

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": (
                f"URL: {url}\nTitle: {title}\nDescription: {description}\n"
                f"Headings: {headings}\nContent preview:\n{body_text}\n\n"
                "Return JSON with: page_type, main_topic, key_entities, "
                "has_login_form (bool), has_search (bool), language, summary"
            )
        }]
    )
    return json.loads(response.content[0].text)

result = inspect_url("https://github.com/SamoTech/skills-tree")
print(json.dumps(result, indent=2))
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| Claude claude-opus-4-5 | Direct text prompt with parsed HTML | 2024-06 |
| LangChain | `WebBaseLoader` + LLM chain | v0.1 |
| Playwright | JS-rendered DOM for SPAs | any |

---

## Notes

- For JavaScript-heavy SPAs, use Playwright to get rendered DOM
- Respect `robots.txt` and rate-limit requests to avoid IP blocks
- Combine with [Screen Reading](screen-reading.md) for full visual + DOM analysis

---

## Related Skills

- [Screen Reading](screen-reading.md) — visual UI analysis
- [Text Reading](text-reading.md) — general text extraction
- [Structured Data Reading](structured-data-reading.md) — JSON-LD / microdata parsing

---

## Changelog

| Date | Change |
|---|---|
| `2026-04` | Expanded from stub: full description, I/O table, httpx+BeautifulSoup example |
| `2025-03` | Initial stub entry |

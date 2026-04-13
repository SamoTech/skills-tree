---
title: "HTML Reading"
category: 01-perception
level: intermediate
stability: stable
description: "Apply html reading in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-html-reading.json)

# HTML Reading
Category: perception | Level: basic | Stability: stable | Version: v1

## Description
Extract clean text and structured data from HTML pages, stripping navigation, ads, and boilerplate.

## Inputs
- `html`: raw HTML string or URL
- `extract`: `text` | `links` | `metadata` | `all`

## Outputs
- Clean article text, list of links, meta tags

## Example
```python
from bs4 import BeautifulSoup
import httpx
html = httpx.get("https://example.com").text
soup = BeautifulSoup(html, "html.parser")
for tag in soup(["script", "style", "nav", "footer"]):
    tag.decompose()
text = soup.get_text(separator="\n", strip=True)
```

## Frameworks
| Framework | Method |
|---|---|
| Python | `BeautifulSoup4`, `trafilatura` |
| LangChain | `WebBaseLoader` |
| LlamaIndex | `SimpleWebPageReader` |

## Failure Modes
- JavaScript-rendered content invisible to static parsers
- Anti-bot measures block HTTP clients

## Related
- `url-dom-inspection.md` · `document-parsing.md`

## Changelog
- v1 (2026-04): Initial entry

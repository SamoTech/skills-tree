---
title: "Web Scraping"
category: 11-web
level: intermediate
stability: stable
description: "Apply web scraping in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-11-web-web-scraping.json)

# Web Scraping

**Category:** `web`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Extract structured data from web pages by parsing HTML with CSS selectors or XPath.

### Example

```python
from bs4 import BeautifulSoup
import httpx

html = httpx.get('https://news.ycombinator.com').text
soup = BeautifulSoup(html, 'html.parser')
titles = [a.text for a in soup.select('.titleline > a')]
```

### Frameworks

- Python `beautifulsoup4`, `lxml`, `playwright`
- Scrapy (full crawling framework)
- Apify, Bright Data (managed)

### Related Skills

- [URL Fetching](url-fetching.md)
- [Browser Navigation](browser-navigation.md)
- [Web Crawling](web-crawling.md)

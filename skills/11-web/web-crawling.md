---
title: "Web Crawling"
category: 11-web
level: intermediate
stability: stable
description: "Crawl and scrape web pages systematically in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-11-web-web-crawling.json)

# Web Crawling
Category: web | Level: intermediate | Stability: stable | Version: v1

## Description
Crawl web pages, follow links, and extract structured content for agent ingestion. Handles pagination, rate limiting, and robots.txt compliance.

## Inputs
- `start_url`: seed URL string
- `max_pages`: int — maximum pages to crawl
- `allowed_domains`: optional list to restrict crawl scope
- `extract_css`: CSS selector for content extraction

## Outputs
- List of dicts with `url`, `title`, `content`, `links`

## Example
```python
import scrapy
from scrapy.crawler import CrawlerProcess

class AgentSpider(scrapy.Spider):
    name = "agent"
    def parse(self, response):
        yield {
            "url": response.url,
            "title": response.css("title::text").get(),
            "content": " ".join(response.css("p::text").getall()),
        }
        for href in response.css("a::attr(href)").getall():
            yield response.follow(href, self.parse)
```

## Frameworks
| Framework | Method |
|---|---|
| Python | `scrapy`, `crawlee`, `playwright` |
| LangChain | `AsyncChromiumLoader`, `WebBaseLoader` |
| LlamaIndex | `SimpleWebPageReader` |

## Dependencies
- package: scrapy
  tested_version: "2.12.0"
  confidence: verified
  notes: "Patched GHSA-h7wm-ph43-c39p (open redirect via spider middleware) and PYSEC-2017-83 (DNS rebinding). Use scrapy>=2.12.0 and pin DNS resolver to prevent rebinding attacks."

## Failure Modes
- JavaScript-rendered pages require Playwright/Splash integration
- IP bans from aggressive crawling — implement polite delays and rotate user-agents
- Robots.txt violations — always set `ROBOTSTXT_OBEY = True`

## Related
- `url-dom-inspection.md` · `html-reading.md` · `structured-data-reading.md`

## Changelog
- v1 (2026-02): Initial entry
- v1.1 (2026-05): Bump scrapy to 2.12.0 (CVE patch)

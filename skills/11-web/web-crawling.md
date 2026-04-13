![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-11-web-web-crawling.json)

# Web Crawling

**Category:** `web`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Recursively follow hyperlinks from a seed URL, fetching and processing multiple pages to build a structured dataset or search index. Respects `robots.txt` and rate limits.

### Example

```python
import scrapy

class DocsSpider(scrapy.Spider):
    name = 'docs'
    start_urls = ['https://docs.example.com']
    allowed_domains = ['docs.example.com']

    def parse(self, response):
        # Extract content from this page
        yield {
            'url': response.url,
            'title': response.css('h1::text').get(),
            'content': ' '.join(response.css('p::text').getall())
        }
        # Follow all internal links
        for href in response.css('a::attr(href)').getall():
            yield response.follow(href, self.parse)
```

### Related Skills

- [Link Extraction](link-extraction.md)
- [Web Scraping](web-scraping.md)
- [Sitemap Parsing](sitemap-parsing.md)

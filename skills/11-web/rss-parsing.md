# RSS/Atom Feed Parsing

**Category:** `web`
**Skill Level:** `basic`
**Stability:** `stable`
**Added:** 2025-03

### Description

Fetch and parse RSS 2.0 or Atom 1.0 XML feeds to extract structured news articles, blog posts, or podcast episodes without scraping HTML.

### Example

```python
import feedparser

feed = feedparser.parse('https://news.ycombinator.com/rss')

print(f"Feed: {feed.feed.title}")
for entry in feed.entries[:5]:
    print(f"- {entry.title}")
    print(f"  {entry.link}")
    print(f"  Published: {entry.published}")
```

### Related Skills

- [URL Fetching](url-fetching.md)
- [Web Scraping](web-scraping.md)
- [Sitemap Parsing](sitemap-parsing.md)

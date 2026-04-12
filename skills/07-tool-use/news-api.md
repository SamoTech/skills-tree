# News API

**Category:** `tool-use`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Fetch current news articles by topic, keyword, or source from news aggregation APIs.

### Example

```python
import httpx

r = httpx.get(
    'https://newsapi.org/v2/everything',
    params={'q': 'AI agents', 'sortBy': 'publishedAt', 'pageSize': 5, 'apiKey': NEWS_KEY}
)
articles = r.json()['articles']
for a in articles:
    print(a['title'], a['url'])
```

### Related Skills

- [Web Search](web-search.md)
- [RSS Parsing](../11-web/rss-parsing.md)

# Web Search

**Category:** `web`  
**Skill Level:** `basic`  
**Stability:** `stable`

### Description

Submit queries to search engines and retrieve a ranked list of results with titles, URLs, and snippets.

### Example

```python
from tavily import TavilyClient
client = TavilyClient(api_key=TAVILY_KEY)
results = client.search('LangGraph multi-agent tutorial 2026')
```

### Related Skills

- [URL Fetching](url-fetching.md)
- [Web Scraping](web-scraping.md)

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-web-search.json)

# Web Search

**Category:** `tool-use`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Search the web via search engine APIs and return relevant results (titles, URLs, snippets).

### Example

```python
import requests
params = {'q': 'LangGraph tutorial 2026', 'key': SERPAPI_KEY}
results = requests.get('https://serpapi.com/search', params=params).json()
for r in results['organic_results'][:5]:
    print(r['title'], r['link'])
```

### Frameworks

- SerpAPI, Tavily, Brave Search API
- Bing Web Search API
- DuckDuckGo (unofficial)
- Perplexity API

### Related Skills

- [URL Fetching](../11-web/url-fetching.md)
- [Web Scraping](../11-web/web-scraping.md)

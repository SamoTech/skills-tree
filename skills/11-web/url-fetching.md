![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-11-web-url-fetching.json)

# URL Fetching

**Category:** `web`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Fetch the full HTML or text content of a URL via HTTP GET.

### Example

```python
import httpx
from markdownify import markdownify

html = httpx.get('https://example.com').text
markdown = markdownify(html)  # Convert to clean markdown
```

### Related Skills

- [Web Scraping](web-scraping.md)
- [DOM Inspection](dom-inspection.md)
- [Browser Navigation](browser-navigation.md)

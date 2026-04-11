# URL / DOM Inspection

**Category:** `perception`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Inspect the DOM structure, metadata, links, and content of a web page by parsing its HTML or using a live browser context.

### Example

```python
from bs4 import BeautifulSoup
import httpx
html = httpx.get('https://example.com').text
soup = BeautifulSoup(html, 'html.parser')
title = soup.find('title').text
links = [a['href'] for a in soup.find_all('a', href=True)]
```

### Related Skills

- [Web Scraping](../11-web/web-scraping.md)
- [DOM Inspection](../11-web/dom-inspection.md)

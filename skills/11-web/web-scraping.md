# Web Scraping

**Category:** `web`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

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

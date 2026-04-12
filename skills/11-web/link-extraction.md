# Link Extraction

**Category:** `web`
**Skill Level:** `basic`
**Stability:** `stable`

### Description

Extract all hyperlinks (`<a href>`) from a web page's HTML, optionally filtering by domain, path pattern, or link text. Foundation for web crawlers and site mappers.

### Example

```python
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

base_url = 'https://github.com/SamoTech'
response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

links = set()
for a in soup.find_all('a', href=True):
    full_url = urljoin(base_url, a['href'])
    if urlparse(full_url).netloc == urlparse(base_url).netloc:
        links.add(full_url)

print(f"Found {len(links)} internal links")
```

### Related Skills

- [Web Scraping](web-scraping.md)
- [Web Crawling](web-crawling.md)
- [Sitemap Parsing](sitemap-parsing.md)

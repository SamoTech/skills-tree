# Sitemap Parsing

**Category:** `web`
**Skill Level:** `basic`
**Stability:** `stable`

### Description

Fetch and parse XML sitemaps (`sitemap.xml`, sitemap indexes) to discover all crawlable URLs of a website without recursively following links.

### Example

```python
import requests
import xml.etree.ElementTree as ET

response = requests.get('https://example.com/sitemap.xml')
root = ET.fromstring(response.content)

ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls = [loc.text for loc in root.findall('.//sm:loc', ns)]

for url in urls[:10]:
    print(url)
```

### Related Skills

- [URL Fetching](url-fetching.md)
- [RSS/Atom Feed Parsing](rss-parsing.md)
- [Web Crawling](web-crawling.md)

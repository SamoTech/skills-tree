# API Endpoint Discovery

**Category:** `web`
**Skill Level:** `advanced`
**Stability:** `experimental`
**Added:** 2025-03

### Description

Intercept browser network traffic to discover undocumented REST or GraphQL API endpoints that a website uses internally, enabling direct programmatic access.

### Example

```python
from playwright.sync_api import sync_playwright

requests_log = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    # Intercept all XHR / fetch requests
    page.on('request', lambda req: requests_log.append({
        'url': req.url,
        'method': req.method,
        'headers': dict(req.headers)
    }))

    page.goto('https://example.com/dashboard')
    page.wait_for_timeout(3000)
    browser.close()

# Inspect discovered API calls
for r in requests_log:
    if '/api/' in r['url']:
        print(r['method'], r['url'])
```

### Related Skills

- [Web Scraping](web-scraping.md)
- [DOM Inspection](dom-inspection.md)
- [JavaScript Execution](js-execution.md)

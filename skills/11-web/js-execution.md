# JavaScript Execution

**Category:** `web`
**Skill Level:** `advanced`
**Stability:** `stable`

### Description

Inject and execute arbitrary JavaScript in the browser context to interact with the DOM, extract data, trigger events, or bypass limitations of standard automation APIs.

### Example

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://example.com')

    # Extract data via JS
    title = page.evaluate("document.title")
    links = page.evaluate("[...document.querySelectorAll('a')].map(a => a.href)")

    # Trigger a hidden event
    page.evaluate("document.querySelector('#hidden-btn').click()")

    # Scroll to bottom
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    browser.close()
```

### Related Skills

- [DOM Inspection](dom-inspection.md)
- [Browser Navigation](browser-navigation.md)
- [Web Scraping](web-scraping.md)

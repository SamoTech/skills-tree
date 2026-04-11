# Browser Navigation

**Category:** `web`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Launch a real browser, navigate to URLs, click elements, fill forms, and interact with dynamic JavaScript-rendered pages.

### Example

```python
from playwright.async_api import async_playwright
async with async_playwright() as p:
    browser = await p.chromium.launch()
    page = await browser.new_page()
    await page.goto('https://github.com')
    await page.click('text=Sign in')
    await browser.close()
```

### Frameworks

- Playwright (preferred)
- Selenium, Puppeteer
- Browser Use (LLM-native browser)
- Playwright MCP

### Related Skills

- [Form Filling](form-filling.md)
- [Web Scraping](web-scraping.md)
- [Screenshot Capture](../10-computer-use/screenshot-capture.md)

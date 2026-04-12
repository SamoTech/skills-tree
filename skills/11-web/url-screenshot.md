# Screenshot of URL

**Category:** `web`
**Skill Level:** `basic`
**Stability:** `stable`
**Added:** 2025-03

### Description

Capture a full-page or viewport screenshot of any URL without human interaction. Used for visual verification, archiving, and feeding page images to multimodal agents.

### Example

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(page.set_viewport_size({"width": 1280, "height": 800}))
    page.goto('https://github.com/SamoTech/skills-tree')

    # Full-page screenshot
    page.screenshot(path='skills-tree.png', full_page=True)
    browser.close()
```

### Related Skills

- [Browser Navigation](browser-navigation.md)
- [Screenshot Capture](../10-computer-use/screenshot-capture.md)
- [DOM Inspection](dom-inspection.md)

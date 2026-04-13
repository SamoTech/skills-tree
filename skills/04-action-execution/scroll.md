![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-04-action-execution-scroll.json)

# Scroll

**Category:** `action-execution`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Scroll a page, list, or element vertically or horizontally to reveal content or navigate long pages.

### Example

```python
import pyautogui
pyautogui.scroll(-5)  # Scroll down 5 clicks

# Playwright
page.evaluate('window.scrollBy(0, 500)')
```

### Related Skills

- [Browser Navigation](../11-web/browser-navigation.md)
- [Mouse Input](mouse-input.md)

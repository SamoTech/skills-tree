![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-browser-tool.json)

# Browser Tool

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Control a real browser as an agent tool — navigate, click, fill forms, and extract content from any website.

### Example

```python
# Playwright MCP or Browser Use
from browser_use import Agent
agent = Agent(task='Go to github.com/SamoTech/skills-tree and count the skill files.')
result = await agent.run()
```

### Frameworks

- Browser Use
- Playwright MCP
- Selenium, Puppeteer

### Related Skills

- [Browser Navigation](../11-web/browser-navigation.md)
- [Web Scraping](../11-web/web-scraping.md)

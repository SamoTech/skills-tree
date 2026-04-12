# Wikipedia API

**Category:** `tool-use`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Fetch Wikipedia article summaries, full text, and page metadata as a grounding data source for agents.

### Example

```python
import wikipedia

summary = wikipedia.summary('Retrieval-augmented generation', sentences=3)
print(summary)
```

### Related Skills

- [Web Search](web-search.md)
- [Wolfram API](wolfram-api.md)

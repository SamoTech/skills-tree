# Regex Generation

**Category:** `code`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Generate, explain, and test regular expressions for pattern matching, extraction, and validation tasks.

### Example

```python
import re

# Match GitHub repo URLs
pattern = r'https://github\.com/([\w-]+)/([\w-]+)'
text = 'Check out https://github.com/SamoTech/skills-tree for all skills!'
match = re.search(pattern, text)
if match:
    owner, repo = match.group(1), match.group(2)
```

### Related Skills

- [Code Generation](code-generation.md)
- [Text Reading](../01-perception/text-reading.md)

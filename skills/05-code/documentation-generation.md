---
title: "Documentation Generation"
category: 05-code
level: intermediate
stability: stable
description: "Apply documentation generation in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-documentation-generation.json)

# Documentation Generation

**Category:** `code`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Automatically generate docstrings, README files, API documentation, and inline comments from source code.

### Example

```python
prompt = f"""Generate a complete Google-style docstring for this Python function:\n{source_code}"""
docstring = llm.invoke(prompt)
```

### Related Skills

- [Code Explanation](code-explanation.md)
- [Code Generation](code-generation.md)

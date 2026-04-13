---
title: "Unit Test Generation"
category: 05-code
level: intermediate
stability: stable
description: "Apply unit test generation in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-unit-test-generation.json)

# Unit Test Generation

**Category:** `code`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Automatically generate unit test cases for functions and classes, covering happy paths, edge cases, and error conditions.

### Example

```python
prompt = f"""Write pytest unit tests for this function:\n{source_code}"""
tests = llm.invoke(prompt)
```

### Related Skills

- [Code Generation](code-generation.md)
- [Debugging](debugging.md)
- [Code Review](code-review.md)

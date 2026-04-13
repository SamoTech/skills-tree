---
title: "Wolfram Alpha API"
category: 07-tool-use
level: intermediate
stability: stable
description: "Apply wolfram alpha api in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-wolfram-api.json)

# Wolfram Alpha API

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Query Wolfram Alpha for precise mathematical computations, scientific facts, unit conversions, and structured knowledge.

### Example

```python
import httpx

r = httpx.get(
    'https://api.wolframalpha.com/v2/query',
    params={
        'input': 'integral of x^2 dx',
        'appid': WOLFRAM_KEY,
        'output': 'json'
    }
)
result = r.json()['queryresult']['pods'][1]['subpods'][0]['plaintext']
print(result)
```

### Related Skills

- [Calculator](calculator.md)
- [Mathematical Reasoning](../02-reasoning/mathematical-reasoning.md)

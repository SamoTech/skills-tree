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

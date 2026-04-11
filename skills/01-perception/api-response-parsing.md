# API Response Parsing

**Category:** `perception`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Parse structured API responses (JSON, XML, GraphQL) and extract relevant fields for downstream use.

### Example

```python
import httpx
response = httpx.get('https://api.github.com/repos/SamoTech/skills-tree').json()
stars = response['stargazers_count']
description = response['description']
```

### Related Skills

- [JSON Transformation](../12-data/json-transformation.md)
- [HTTP Request](../04-action-execution/http-request.md)

---
title: "JSON Transformation"
category: 12-data
level: basic
stability: stable
description: "Apply json transformation in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-json-transformation.json)

# JSON Transformation

**Category:** `data`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Parse and transform JSON data structures — flatten, filter, reshape, or extract specific fields.

### Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `json_data` | `string/dict` | ✅ | Raw JSON string or parsed dict |
| `transform_spec` | `string` | ❌ | jq-style or natural language spec |

### Outputs

| Output | Type | Description |
|---|---|---|
| `result` | `dict/list` | Transformed JSON structure |

### Example

```python
import json, jq
data = json.loads(raw_json)
result = jq.first('.users[] | {name, email}', data)
```

### Frameworks

- Python `json`, `jq`
- LangChain JSONLoader
- OpenAI function calling with structured output

### Related Skills

- [CSV Processing](csv-processing.md)
- [Structured Data Reading](../01-perception/structured-data-reading.md)

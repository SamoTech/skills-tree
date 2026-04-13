---
title: "API Client Generation"
category: 05-code
level: intermediate
stability: stable
description: "Apply api client generation in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-api-client-generation.json)

# API Client Generation

**Category:** `code`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Generate typed API client code from an OpenAPI/Swagger spec or by inspecting an existing API.

### Example

```bash
# Generate Python client from OpenAPI spec
openapi-python-client generate --path openapi.yaml

# Or use httpx manually
class SkillsAPIClient:
    def __init__(self, base_url, api_key):
        self.client = httpx.Client(base_url=base_url, headers={'Authorization': f'Bearer {api_key}'})

    def list_skills(self):
        return self.client.get('/skills').json()
```

### Related Skills

- [Code Generation](code-generation.md)
- [HTTP Request](../04-action-execution/http-request.md)

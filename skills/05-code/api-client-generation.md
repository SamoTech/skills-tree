# API Client Generation

**Category:** `code`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

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

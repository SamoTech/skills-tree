![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-04-action-execution-http-request.json)

# HTTP Request

**Category:** `action-execution`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Make outbound HTTP requests (GET, POST, PUT, DELETE, PATCH) to APIs and web servers.

### Example

```python
import httpx
response = httpx.post(
    'https://api.example.com/users',
    json={'name': 'Ossama', 'role': 'admin'},
    headers={'Authorization': f'Bearer {token}'}
)
data = response.json()
```

### Related Skills

- [API Response Parsing](../01-perception/api-response-parsing.md)
- [Custom API Wrapper](../07-tool-use/custom-api-wrapper.md)

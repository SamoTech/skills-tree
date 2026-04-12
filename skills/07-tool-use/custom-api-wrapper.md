# Custom API Wrapper

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Wrap any REST API as a reusable agent tool with a defined schema, authentication, and error handling.

### Example

```python
def call_api(endpoint: str, method: str = 'GET', payload: dict = None) -> dict:
    import httpx
    headers = {'Authorization': f'Bearer {API_KEY}'}
    r = httpx.request(method, f'{BASE_URL}/{endpoint}', json=payload, headers=headers)
    r.raise_for_status()
    return r.json()
```

### Related Skills

- [Function Calling](function-calling.md)
- [HTTP Request](../04-action-execution/http-request.md)
- [MCP Tool](mcp-tool.md)

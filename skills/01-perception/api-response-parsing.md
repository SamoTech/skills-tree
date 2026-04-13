---
Category: Perception
Skill Level: Advanced
Stability: Stable
Tags: [api, json, xml, grpc, parsing, schema-validation]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-api-response-parsing.json)

# API Response Parsing

### Description
Structured extraction and validation of data from REST, GraphQL, gRPC, and WebSocket API responses. Handles deeply nested payloads, pagination envelopes, error schemas, partial responses, and dynamic field resolution. Includes schema validation, type coercion, and tolerance for malformed or evolving APIs.

### When to Use
- Consuming third-party REST or GraphQL APIs where the schema may drift
- Extracting structured data from paginated or cursor-based response envelopes
- Validating API responses against OpenAPI / JSON Schema before downstream processing
- Handling gRPC Protobuf responses that must be decoded and mapped to domain objects

### Example
```python
import httpx, jsonpath_ng
from jsonschema import validate

SCHEMA = {
  "type": "object",
  "required": ["data", "meta"],
  "properties": {
    "data": {"type": "array", "items": {"type": "object"}},
    "meta": {"type": "object", "properties": {"next_cursor": {"type": "string"}}}
  }
}

def fetch_all_pages(url: str, headers: dict) -> list[dict]:
    results, cursor = [], None
    while True:
        params = {"cursor": cursor} if cursor else {}
        r = httpx.get(url, headers=headers, params=params, timeout=10)
        r.raise_for_status()
        body = r.json()
        validate(instance=body, schema=SCHEMA)  # raises on malformed payload
        expr = jsonpath_ng.parse("$.data[*].id")
        ids = [m.value for m in expr.find(body)]
        results.extend(body["data"])
        cursor = body.get("meta", {}).get("next_cursor")
        if not cursor:
            break
    return results
```

### Advanced Techniques
- **GraphQL fragment unpacking**: recursively resolve `__typename` to dispatch handlers per concrete type
- **Protobuf → dict**: use `google.protobuf.json_format.MessageToDict` with `preserving_proto_field_name=True`
- **Delta patching**: for PATCH-style APIs returning only changed fields, merge with a local baseline using `deepmerge`
- **Rate-limit header parsing**: extract `X-RateLimit-Remaining` / `Retry-After` to back off gracefully

### Related Skills
- `web-scraping`, `json-transformation`, `schema-inference`, `http-request`, `data-cleaning`

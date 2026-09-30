---
title: "API Response Parsing"
category: 01-perception
level: intermediate
stability: stable
version: v2
added: "2025-03"
description: "Parse and validate REST, GraphQL, gRPC, and WebSocket responses into bounded, typed structures, including pagination, error envelopes, schema drift, and partial responses."
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


## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Untrusted input causes incorrect extraction | Malformed, adversarial, or incomplete source data | Validate structure, bound input size, preserve source provenance, and reject ambiguous results when required |
| Model or parser overstates certainty | Heuristic extraction is treated as authoritative | Return source spans or structured evidence and distinguish extraction from verification |
| Context or resource exhaustion | Large files, histories, responses, or media are processed without limits | Apply size, time, row, page, or token limits and process incrementally |


## Evidence

The skill's implementation guidance is grounded in the following primary references:
- JSON Schema 2020-12: https://json-schema.org/specification
- JSON Schema Validation: https://json-schema.org/draft/2020-12/json-schema-validation
- Python jsonschema validator API: https://python-jsonschema.readthedocs.io/

Evidence status: implementation guidance verified against the cited documentation; no benchmark claim is made unless a reproducible benchmark is included in this file.

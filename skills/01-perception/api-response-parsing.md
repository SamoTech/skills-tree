---
title: "API Response Parsing"
category: 01-perception
level: intermediate
stability: stable
description: "Parse bounded API response payloads into deterministic records while preserving schema errors, pagination state, and untrusted response content for explicit downstream validation."
added: "2025-03"
related:
  - "structured-data-reading"
  - "json-schema-validation"
  - "http-request"
  - "document-parsing"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-api-response-parsing.json)

# API Response Parsing
Category: perception | Level: intermediate | Stability: stable | Version: v2

## Description
Parse bounded HTTP/API response bodies into deterministic records without confusing transport success with application-level success. The parser separates response metadata, payload decoding, schema validation, pagination hints, and error reporting so downstream agent steps can make explicit decisions.

This skill is appropriate for JSON and JSON-like API payloads, including common envelope patterns such as `data`, `items`, `results`, and cursor/page metadata. It does not claim that an arbitrary response conforms to OpenAPI, JSON Schema, GraphQL, or Protobuf semantics unless the caller supplies the relevant schema or decoder.

## When to Use
Use API response parsing when an agent needs structured fields from an already-retrieved response. Use `http-request` for transport, authentication, retries, and network policy. Use `json-schema-validation` when a schema is available and conformance must be checked separately. Use `structured-data-reading` when the input is a structured document rather than an API response.

## Inputs
| Input | Type | Required | Description |
|---|---|---|---|
| `status` | `int` | yes | HTTP/application status code observed by the transport layer |
| `headers` | `dict[str, str]` | no | Response headers; treated as untrusted metadata |
| `body` | `str` / `bytes` | yes | Bounded response body to decode |
| `content_type` | `str` | no | Media type supplied by the transport layer |
| `format` | `str` | no | `json`, `text`, or `auto`; `auto` only makes conservative decoding decisions |
| `max_bytes` | `int` | no | Maximum body size accepted by the parser |
| `schema` | `dict` | no | Optional JSON Schema-like object for caller-owned validation |

## Outputs
Each response produces one deterministic parse result containing:

- `ok`: whether decoding and requested validation completed successfully.
- `status`: the supplied status code.
- `data`: decoded JSON data when decoding succeeds, otherwise `None`.
- `error`: structured error information when parsing or validation fails.
- `pagination`: conservative pagination hints discovered from known fields.
- `metadata`: selected non-secret response metadata needed for auditing.
- `raw`: the bounded original body when the caller explicitly requests retention.

A successful transport status must not be interpreted as application success. Likewise, a valid JSON document is not proof that its fields satisfy a business contract.

## Contract
| Aspect | Contract |
|---|---|
| Input | Bounded response body plus caller-supplied transport metadata |
| Output | Deterministic parse result; preserve explicit errors instead of silently dropping data |
| Decoding | JSON is decoded only when selected by `format` or a conservative `auto` rule |
| Ordering | Preserve JSON object/list order as decoded by the runtime; never invent missing fields |
| Limits | Enforce `max_bytes` before decoding |
| Schema | Validate only against a schema explicitly supplied by the caller |
| Pagination | Report recognized hints without issuing follow-up requests |
| Security | Treat body, headers, URLs, and error messages as untrusted data |

## Deterministic Reference Implementation
The reference implementation uses only the Python standard library. It does not make network calls, follow pagination links, execute embedded content, or claim schema conformance without a supplied schema. The optional schema checker intentionally supports only a small deterministic subset (`type`, `required`, and `properties`) so callers can see exactly what is validated.

```python
import json
from typing import Any


def _type_matches(value: Any, expected: str) -> bool:
    return {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
        "null": value is None,
    }.get(expected, True)


def validate_subset(value: Any, schema: dict, path: str = "$", errors=None):
    errors = [] if errors is None else errors
    expected = schema.get("type")
    if isinstance(expected, str) and not _type_matches(value, expected):
        errors.append({"path": path, "reason": "type-mismatch", "expected": expected})
        return errors

    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append({"path": f"{path}.{key}", "reason": "missing-required-field"})
        for key, child_schema in schema.get("properties", {}).items():
            if key in value and isinstance(child_schema, dict):
                validate_subset(value[key], child_schema, f"{path}.{key}", errors)
    return errors


def parse_api_response(
    status: int,
    headers: dict[str, str] | None,
    body: str | bytes,
    content_type: str | None = None,
    format: str = "auto",
    max_bytes: int = 1_048_576,
    schema: dict | None = None,
    retain_raw: bool = False,
) -> dict:
    if max_bytes <= 0:
        raise ValueError("max_bytes must be positive")
    raw_bytes = body.encode("utf-8") if isinstance(body, str) else body
    if len(raw_bytes) > max_bytes:
        return {
            "ok": False,
            "status": status,
            "data": None,
            "error": {"code": "body-too-large", "max_bytes": max_bytes},
            "pagination": {},
            "metadata": {"content_type": content_type},
            "raw": raw_bytes[:max_bytes].decode("utf-8", errors="replace") if retain_raw else None,
        }

    text = raw_bytes.decode("utf-8", errors="replace")
    wants_json = format == "json" or (format == "auto" and "json" in (content_type or "").lower())
    data = None
    error = None

    if wants_json:
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            error = {"code": "invalid-json", "line": exc.lineno, "column": exc.colno}
    elif format == "text":
        data = text
    elif format == "auto":
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = text
    else:
        error = {"code": "unsupported-format", "format": format}

    if error is None and schema is not None:
        schema_errors = validate_subset(data, schema)
        if schema_errors:
            error = {"code": "schema-validation-failed", "details": schema_errors}

    pagination = {}
    if isinstance(data, dict):
        for key in ("next_cursor", "nextPageToken", "next_page_token", "next"):
            if key in data and data[key] not in (None, ""):
                pagination[key] = data[key]
        for envelope in ("meta", "metadata", "pagination"):
            nested = data.get(envelope)
            if isinstance(nested, dict):
                for key in ("next_cursor", "nextPageToken", "next_page_token", "next"):
                    if key in nested and nested[key] not in (None, ""):
                        pagination[key] = nested[key]

    safe_headers = {}
    for key, value in (headers or {}).items():
        lowered = key.lower()
        if lowered in {"content-type", "retry-after", "etag", "x-ratelimit-remaining"}:
            safe_headers[key] = str(value)

    return {
        "ok": error is None,
        "status": status,
        "data": data,
        "error": error,
        "pagination": pagination,
        "metadata": {"content_type": content_type, "headers": safe_headers},
        "raw": text if retain_raw else None,
    }


sample = parse_api_response(
    200,
    {"Content-Type": "application/json", "X-RateLimit-Remaining": "9"},
    '{"data":[{"id":7}],"meta":{"next_cursor":"abc"}}',
    content_type="application/json",
    schema={"type": "object", "required": ["data"], "properties": {"data": {"type": "array"}}},
)
assert sample["ok"] is True
assert sample["pagination"]["next_cursor"] == "abc"

invalid = parse_api_response(200, {}, '{"data":', content_type="application/json")
assert invalid["error"]["code"] == "invalid-json"
```

## Pagination Guidance
Pagination parsing is observation only. The parser may expose a cursor, page token, or next-link value already present in the response, but it must not follow that value. A separate transport/orchestration step should enforce request limits, authentication, retry policy, deduplication, and termination conditions.

| Pattern | Recognition | Boundary |
|---|---|---|
| `next_cursor` | top-level or common metadata envelope | Report value; do not request the next page |
| `nextPageToken` | top-level or common metadata envelope | Preserve token as opaque data |
| `next_page_token` | top-level or common metadata envelope | Do not infer endpoint semantics |
| `next` | top-level or common metadata envelope | Treat as untrusted URL/data; do not follow |
| page number | `page`/`page_size` fields | Do not infer total pages without an explicit contract |

## Failure Modes
| Failure | Detection | Required behavior |
|---|---|---|
| Body too large | Byte limit exceeded | Return `body-too-large`; do not decode beyond the limit |
| Invalid UTF-8 | Decode replacement required | Preserve replacement characters and report loss if byte fidelity matters |
| Invalid JSON | Decoder error | Return `invalid-json` with location; do not fabricate a partial object |
| Wrong root type | Supplied schema mismatch | Return `schema-validation-failed` |
| Missing required field | Supplied schema declares it | Return a structured validation error |
| Unknown schema keyword | Keyword outside the supported subset | Do not claim full JSON Schema validation |
| API error payload | Status or body indicates failure | Preserve payload; do not reinterpret it as successful domain data |
| Pagination loop | Repeated token observed by caller | Leave loop detection to the orchestration layer |
| Secret-bearing headers | Authorization/cookie-like headers supplied | Do not copy them into the output metadata |

## Safety Boundaries
API responses are untrusted external data. Never execute code, templates, SQL, shell commands, serialized objects, or URLs found in a response. Never follow a `next` URL merely because it was parsed. Do not expose authorization, cookie, proxy, or set-cookie headers through the normalized metadata. Parsing does not establish authenticity, authorization, freshness, or business correctness.

## Validation Rules
A conforming implementation must enforce a byte limit before decoding, preserve explicit parse/validation failures, avoid network side effects, and never silently convert malformed JSON into a fabricated structure. If a schema is supplied, validation scope must be stated accurately. Pagination values are opaque observations until a separately authorized transport layer acts on them.

## Provenance
Keep the original bounded response available only when the caller requests `retain_raw`. Record the transport status and selected non-secret metadata separately from parsed business data so downstream systems can distinguish source evidence from derived interpretation.

## Related Skills
- `structured-data-reading.md` — general structured payload interpretation.
- `json-schema-validation.md` — full schema validation when a schema contract is available.
- `http-request.md` — transport, authentication, retries, and network policy.
- `document-parsing.md` — parsing structured documents outside an API transport context.

## Changelog
- v1 (2025-03): Initial entry.
- v2 (2026-09): Added bounded deterministic parsing, explicit I/O/error contracts, conservative pagination extraction, validation scope, provenance, and safety boundaries.

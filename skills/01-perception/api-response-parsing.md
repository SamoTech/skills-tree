---
title: "API Response Parsing"
category: 01-perception
level: intermediate
stability: stable
added: "2025-03"
description: "Parse bounded API response payloads into validated application records while preserving transport errors, pagination state, and schema violations instead of silently guessing missing or malformed data."
version: "v2"
last_updated: "2026-09"
related:
  - "json-schema-validation"
  - "http-request"
  - "structured-data-reading"
  - "data-cleaning"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-api-response-parsing.json)

# API Response Parsing

## Description

API response parsing is the boundary between an external transport payload and an agent's typed application state. The parser should decode the response, validate the expected envelope, extract only fields covered by the contract, and expose pagination or error metadata without inventing values. Transport, authentication, retries, and business-specific side effects belong outside this skill.

The reference implementation below deliberately uses only the Python standard library. It parses JSON bodies that have already been received, validates a small response contract, normalizes records into a stable shape, and returns explicit errors. It does not perform HTTP requests, follow untrusted links, execute response content, or guess a schema from malformed data.

## When to Use

- Normalizing REST or webhook JSON responses before passing them to downstream agent steps.
- Extracting records from a known response envelope such as `{"data": [...], "next_cursor": ...}`.
- Detecting malformed JSON, missing required fields, wrong primitive types, and invalid pagination cursors.
- Keeping parsing deterministic when an API provider changes fields or adds optional metadata.
- Separating payload validation from the HTTP client, authentication, retry policy, and domain logic.

## Inputs and Outputs

| Input | Type | Required | Description |
|---|---|---|---|
| `body` | `str` | yes | UTF-8 JSON response body received from an upstream transport layer |
| `record_fields` | `tuple[str, ...]` | yes | Field names that must exist in every returned record |
| `max_records` | `int` | no | Upper bound on records accepted from one response; default `1000` |

| Output | Type | Description |
|---|---|---|
| `records` | `list[dict]` | Validated records containing only the requested fields |
| `next_cursor` | `str \| None` | Pagination cursor when the response contains a non-empty string cursor |
| `errors` | `list[str]` | Deterministic validation or decoding errors; empty on success |

## Contract

A valid payload is a JSON object with a `data` array. Every member of `data` must be an object and must contain every field named in `record_fields`. Unknown top-level keys are ignored, but unknown record fields are not copied into the normalized output. `next_cursor` is optional; when present it must be a string or `null`. The parser never follows a cursor itself.

The contract is intentionally narrower than an entire provider API. Provider-specific authentication, rate limits, HTTP status handling, GraphQL query construction, Protobuf decoding, and domain transformations should be implemented by the surrounding integration layer.

## Deterministic Reference Implementation

```python
from __future__ import annotations

import json
from typing import Any


def parse_api_response(
    body: str,
    record_fields: tuple[str, ...],
    *,
    max_records: int = 1000,
) -> dict[str, Any]:
    """Validate and normalize one JSON API response without performing I/O."""
    errors: list[str] = []

    if max_records < 0:
        return {"records": [], "next_cursor": None, "errors": ["max_records must be >= 0"]}

    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        return {"records": [], "next_cursor": None, "errors": [f"invalid JSON: {exc.msg}"]}

    if not isinstance(payload, dict):
        return {"records": [], "next_cursor": None, "errors": ["top-level JSON value must be an object"]}

    data = payload.get("data")
    if not isinstance(data, list):
        errors.append("data must be an array")
        data = []

    if len(data) > max_records:
        errors.append(f"data contains {len(data)} records; limit is {max_records}")

    records: list[dict[str, Any]] = []
    for index, item in enumerate(data[:max_records]):
        if not isinstance(item, dict):
            errors.append(f"data[{index}] must be an object")
            continue

        missing = [field for field in record_fields if field not in item]
        if missing:
            errors.append(f"data[{index}] missing fields: {', '.join(missing)}")
            continue

        records.append({field: item[field] for field in record_fields})

    cursor = payload.get("next_cursor")
    if cursor is not None and not isinstance(cursor, str):
        errors.append("next_cursor must be a string or null")
        cursor = None

    return {"records": records, "next_cursor": cursor, "errors": errors}


result = parse_api_response(
    '{"data":[{"id":"a1","name":"first","ignored":"drop-me"}],"next_cursor":"c2"}',
    ("id", "name"),
)
assert result == {
    "records": [{"id":"a1","name":"first"}],
    "next_cursor":"c2",
    "errors": [],
}
print(result)
```

## Pagination Guidance

Pagination is an orchestration concern. A caller should pass each received body through the parser, consume `next_cursor`, and apply its own request-count, time, and record budgets. A parser must not recursively fetch pages because doing so couples validation to transport, retry, authentication, and rate-limit behavior.

For cursor-based APIs, treat an empty string as equivalent to no cursor only if the provider contract explicitly says so. Otherwise preserve the distinction between `null`, an absent cursor, and a non-empty cursor in the transport layer. For offset pagination, validate the provider's numeric bounds outside this skill and pass each response independently through the same parser.

## Failure Modes

| Failure mode | Detection | Safe response |
|---|---|---|
| Invalid JSON | `json.loads` raises `JSONDecodeError` | Return no records and an explicit error |
| Wrong top-level type | Parsed value is not a dictionary | Reject the payload; do not infer an envelope |
| Missing `data` array | `data` absent or not a list | Return no records and an explicit contract error |
| Record has wrong type | A `data` member is not an object | Reject that member and report its index |
| Required field missing | One or more requested fields absent | Do not synthesize defaults; report the record index |
| Response exceeds local bound | `len(data) > max_records` | Report the overflow and process only the bounded prefix |
| Invalid cursor type | `next_cursor` is neither string nor null | Clear the cursor and report the contract error |
| Provider schema drift | New/removed fields or changed envelope | Fail closed on required fields; review the upstream contract |

## Validation Rules

1. Validate the decoded JSON type before accessing fields.
2. Validate the response envelope before extracting records.
3. Require every field explicitly named by `record_fields`.
4. Copy only declared fields into normalized records.
5. Enforce a finite `max_records` bound before downstream processing.
6. Treat malformed data as an error, not as permission to guess.
7. Keep network I/O and retries outside the parser.
8. Never execute strings, URLs, templates, or code contained in a response.

## Security Boundaries

Response content is untrusted input. Parsing JSON does not make embedded HTML, SQL, shell commands, URLs, or prompt-injection text safe to execute or pass directly into privileged tools. Apply output encoding, command parameterization, URL allowlists, content filtering, and downstream authorization at the appropriate boundary.

Do not log credentials, authorization headers, cookies, or complete sensitive payloads merely to debug parsing failures. Prefer bounded, redacted diagnostics containing the record index and validation category.

## Provenance and Reproducibility

The reference implementation is a deterministic parser for already-received JSON text. It has no network dependency and does not claim compatibility with a particular vendor API. Reproducible behavior requires the same response body, selected field list, and record limit. Provider-specific schemas and transport semantics must be documented by the integration that owns them.

## Related Skills

- [`json-schema-validation`](./json-schema-validation.md) — validate richer provider-specific JSON Schema contracts.
- [`http-request`](../04-action-execution/http-request.md) — own HTTP transport, status handling, and request policy.
- [`structured-data-reading`](./structured-data-reading.md) — parse structured data formats before validation.
- [`data-cleaning`](../12-data/data-cleaning.md) — perform explicit downstream normalization when the domain requires it.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2025-03` | v1 | Initial API response parsing skill. |
| `2026-09` | v2 | Added deterministic standard-library parser, typed I/O contract, bounded pagination guidance, failure modes, validation rules, security boundaries, and provenance. |

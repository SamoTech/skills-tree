---
title: "Custom Api Wrapper"
category: 07-tool-use
level: advanced
stability: stable
version: v2
description: "Integrate a custom API through a documented wrapper with validated requests, responses, errors, and authentication boundaries."
added: "2026-09"
related: [tool-schema-design, tool-output-validation, api-pagination]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-custom-api-wrapper.json)

# Custom Api Wrapper

**Category:** `tool-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2026-09

### Description

Integrate a custom API through a documented wrapper with validated requests, responses, errors, and authentication boundaries. The invocation is contract-first: validate the tool interface and inputs before calling, and verify the observable outcome afterwards rather than trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | api_contract | object | Endpoint, method, auth scheme, request/response schema, and error model |
| Input | request | object | Payload validated against the wrapper schema |
| Output | response | object | Parsed, schema-validated response or classified error |
| Output | verification | object | Independent confirmation of important outcomes |

### Procedure
1. Document the API contract (endpoints, auth, schemas, errors) before writing the wrapper.
2. Validate requests against the schema; fail fast on contract violations.
3. Keep credentials in the authorized channel only; never in code, logs, or URLs.
4. Handle the documented error model explicitly: timeouts, rate limits, partial results.
5. Paginate and bound result sets; never assume a single response is complete.
6. Verify important outcomes by re-reading state; record evidence.

### Example

```python
contract = {'method': 'POST', 'path': '/v1/items', 'auth': 'bearer', 'max_page': 100}
request = {'method': 'POST', 'path': '/v1/items'}
assert request['method'] == contract['method']
assert request['path'] == contract['path']
print('request matches the documented wrapper contract')
```

### Related Skills

- [Tool Schema Design](tool-schema-design.md) - define the wrapper contract
- [Tool Output Validation](tool-output-validation.md) - validate responses
- [API Pagination](api-pagination.md) - bound and complete result sets

## Failure Modes

- Calling undocumented endpoints or assuming response shapes.
- Hard-coding credentials or leaking them in logs.
- Unbounded pagination or retries.
- Treating a 2xx response as proof of the business outcome.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/AI_CONSTITUTION.md pointers where present).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; provider behavior must be checked against current provider documentation; no benchmark claim is made without reproducible evidence.

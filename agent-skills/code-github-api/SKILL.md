---
name: code-github-api
description: Work with GitHub APIs using documented endpoints, authentication boundaries, pagination, error handling, and least-privilege access.
metadata:
  source: skills/05-code/github-api.md
  category: 05-code
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-github-api.json)

# GitHub API (Code Integration)

**Category:** `code`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2026-09

### Description

Work with GitHub APIs using documented endpoints, authentication boundaries, pagination, error handling, and least-privilege access. The skill is evidence-first: inspect actual state before acting, preserve existing contracts, and verify the result before reporting completion.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | operation | object | Endpoint, method, and payload confirmed against current API documentation |
| Input | credential | reference | Least-privilege token reference; never an inline secret |
| Output | response | object | Parsed, fully paginated response with validated semantics |
| Output | verification | object | Independent state check confirming the intended effect |

### Procedure
1. Confirm the endpoint and method against current API documentation; do not rely on remembered behavior.
2. Use the least-privilege credential scoped to the operation; never log or inline the token.
3. Handle pagination and rate limits explicitly: follow pagination links and honor Retry-After.
4. Validate response semantics (status and payload shape) before interpreting the result.
5. Verify the resulting state through a second read; a 2xx response is not proof of the intended effect.
6. Treat write operations on shared resources as requiring explicit approval.

### Example

```python
from urllib.parse import urlparse

url = 'https://api.github.com/repos/example/project/pulls?per_page=100&page=2'
parts = urlparse(url)
assert parts.netloc == 'api.github.com'
assert 'page=2' in parts.query
print('request parsed; pagination and rate limits handled explicitly')
```

### Related Skills

- [Git Operations](git-operations.md) - local Git state and remote API state must agree
- [Approval Before Destructive Tools](../14-security/approval-before-destructive-tools.md) - write operations on shared resources need approval

## Failure Modes

- Using undocumented endpoint behavior.
- Exposing credentials in source, logs, or error output.
- Ignoring pagination or rate limits and reporting partial results as complete.
- Treating a request response as proof without verifying the resulting state.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic request-parsing example, an execution procedure, and corpus-verified related links.
- v1 (2026-11): Title disambiguated per DECISION-2026-11-26-TITLE-UNIQUENESS; capability contract unchanged.
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.

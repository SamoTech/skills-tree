---
title: "GitHub API"
category: 07-tool-use
level: intermediate
stability: stable
version: v2
description: "Use GitHub REST APIs for bounded repository, issue, pull-request, and metadata operations with explicit scopes and verified mutations."
added: "2026-09"
related: [tool-guardrails, function-calling, api-pagination]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-github-api.json)

# GitHub API

**Category:** `tool-use`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2026-09

### Description

Use GitHub REST APIs for bounded repository, issue, pull-request, and metadata operations with explicit scopes and verified mutations. The invocation is contract-first: validate the tool interface and inputs before calling, and verify the observable outcome afterwards rather than trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | operation | object | Endpoint, method, and bounded target resource confirmed against current docs |
| Input | credential | reference | Least-privilege token reference; never an inline secret |
| Output | response | object | Fully paginated, schema-validated response |
| Output | verification | object | Independent re-read confirming the intended mutation |

### Procedure
1. Confirm the endpoint and method against current GitHub REST documentation.
2. Scope the credential to the minimum permission the operation needs; never log the token.
3. Bound the target repository, resource, and result set before calling.
4. Follow pagination explicitly and honor rate limits (Retry-After, remaining counters).
5. Verify mutations by re-reading the resulting state; a 2xx response is not proof.
6. Treat destructive or shared-resource mutations as requiring explicit approval.

### Example

```python
from urllib.parse import urlparse, parse_qs

url = 'https://api.github.com/repos/example/project/issues?state=open&per_page=100&page=2'
parts = urlparse(url)
q = parse_qs(parts.query)
assert parts.netloc == 'api.github.com'
assert q['per_page'] == ['100']
print('bounded, paginated request constructed')
```

### Related Skills

- [Tool Guardrails](tool-guardrails.md) - invocation boundaries
- [Function Calling](function-calling.md) - structured tool invocation
- [API Pagination](api-pagination.md) - complete bounded result sets
- [Approval Before Destructive Tools](../14-security/approval-before-destructive-tools.md) - gate destructive mutations

## Failure Modes

- Hard-coding credentials or placing secrets in tool arguments.
- Assuming identifiers or schemas are portable across accounts.
- Performing mutations without authorization and current-state checks.
- Treating a successful response as proof of the desired outcome.
- Unbounded retries, pagination, or result sets.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/AI_CONSTITUTION.md pointers where present).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification
- https://docs.github.com/en/rest

Evidence status: implementation guidance only; provider behavior must be checked against current provider documentation; no benchmark claim is made without reproducible evidence.

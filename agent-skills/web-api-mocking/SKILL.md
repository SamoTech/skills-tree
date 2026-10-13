---
name: web-api-mocking
description: Create deterministic mocks of web APIs for agent testing with explicit fixture matching and verification that no live traffic occurred.
metadata:
  source: skills/11-web/web-api-mocking.md
  category: 11-web
  version: "v1"
---

# Web API Mocking

## Description
Create deterministic mocks of web APIs for agent testing with explicit fixture matching and verification that no live traffic occurred. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- agent behavior must be tested against a deterministic API without live calls.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for web api mocking work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the web api mocking steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def fixture_for(request, fixtures):
    key = (request['method'], request['path'])
    if key not in fixtures:
        raise ValueError('no fixture for %s' % (key,))
    return fixtures[key]

fx = {('GET', '/api/status'): {'status': 200}}
assert fixture_for({'method': 'GET', 'path': '/api/status'}, fx)['status'] == 200
```

## Failure Modes
- A mock that silently falls through to the live endpoint.
- Fixtures that drift from the real response schema.
- No assertion that live traffic was absent during the test.
- Matching on URL only and ignoring method or body.
- Mocks so loose they accept any request and prove nothing.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Deterministic API mocking for agent regression tests appears in 2026 CI-for-agents requests; this is a dated signal, not an adoption metric.

## Related
- api-discovery.md
- web-session-replay.md
- headless-browser-configuration.md

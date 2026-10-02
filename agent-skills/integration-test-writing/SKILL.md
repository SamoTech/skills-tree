---
name: integration-test-writing
description: Create integration tests that verify interactions between real application components, external boundaries, persistence, or services.
metadata:
  source: skills/05-code/integration-test-writing.md
  category: 05-code
---

## Description
Create integration tests that verify interactions between real application components, external boundaries, persistence, or services. Use realistic boundaries while keeping tests deterministic, isolated, and aligned with documented behavior.

## When to Use
Use when correctness depends on interactions that unit tests alone cannot establish.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Inputs | Component contracts, test environment, fixtures, persistence or service boundaries, and expected behavior. |
| Outputs | Repeatable integration coverage with clear failure diagnostics. |
| Failure modes | Flaky dependencies, shared state, weak assertions, or tests that do not exercise the real boundary. |

## Runnable Example

```python
from dataclasses import dataclass

@dataclass
class Response:
    status: int

response = Response(status=200)
assert response.status == 200
print('integration tests should assert observable boundary behavior')
```

## Failure modes
- Testing only mocks when the integration boundary is the requirement.
- Shared mutable state between tests.
- Weak assertions that permit regressions.
- Environment-dependent tests without controlled prerequisites.

## Related
- 05-code
- AI_CONSTITUTION.md
- meta/AGENT_OPERATING_MODEL.md

## Evidence
Repository-backed implementation guidance grounded in repository governance and validation workflows; no external benchmark claim is made.

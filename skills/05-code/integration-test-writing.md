---
title: "Integration Test Writing"
category: 05-code
level: advanced
stability: stable
version: v2
description: "Create integration tests that verify interactions between real application components, external boundaries, persistence, or services."
added: "2026-09"
related: [unit-test-generation, debugging]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-integration-test-writing.json)

# Integration Test Writing

**Category:** `code`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2026-09

### Description

Create integration tests that verify interactions between real application components, external boundaries, persistence, or services. The skill is evidence-first: inspect actual state before acting, preserve existing contracts, and verify the result before reporting completion.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | contracts | object | Component boundaries and the interactions that must be verified |
| Input | environment | object | Fixtures, test-double policy, and persistence or service boundaries |
| Output | tests | list | Deterministic, isolated tests asserting observable boundary behavior |
| Output | evidence | object | Green run output plus failure diagnostics that locate broken interactions |

### Procedure
1. Identify the real boundary the test must exercise (HTTP, queue, database) and what unit tests cannot cover.
2. Decide per dependency: real instance, in-memory equivalent, or contract-tested fake; record the choice.
3. Isolate state: per-test fixtures with setup and teardown; no ordering dependence.
4. Assert on observable boundary behavior (status codes, persisted rows, messages), not internals.
5. Keep tests deterministic: controlled seeds, ports, and time; fail with diagnostics that locate the broken interaction.
6. Run locally and under CI-equivalent conditions before merge.

### Example

```python
from dataclasses import dataclass

@dataclass
class BoundaryResponse:
    status: int
    persisted: bool

response = BoundaryResponse(status=200, persisted=True)
assert response.status == 200
assert response.persisted is True
print('boundary assertions check observable effects, not internals')
```

### Related Skills

- [Unit Test Generation](unit-test-generation.md) - unit coverage complements boundary coverage
- [Debugging](debugging.md) - diagnose interactions these tests expose

## Failure Modes

- Testing only mocks when the real boundary is the requirement.
- Sharing mutable state between tests.
- Weak assertions that permit regressions.
- Environment-dependent tests without controlled prerequisites.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic boundary-assertion example, an execution procedure, and corpus-verified related links.
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.

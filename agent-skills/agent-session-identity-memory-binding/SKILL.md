---
name: agent-session-identity-memory-binding
description: Bind session identity in agent memory so the same user state follows them across app boundaries without forked copies.
metadata:
  source: skills/03-memory/agent-session-identity-memory-binding.md
  category: 03-memory
  version: "v1"
---

# Agent Session Identity Memory Binding

## Description
Bind session identity in agent memory so the same user state follows them across app boundaries without forked copies. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- One user works with the same agent across applications and their memory must stay bound to a single verified identity.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Resolve the session identity from the verified principal at every boundary crossing, reconcile the memory key against the identity record, and record the binding with the verification method used.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def bind(session, principal):
    if session.get("principal") in (None, principal):
        session["principal"] = principal
        return session
    raise ValueError("identity conflict")
s = {}
assert bind(s, "user-1")["principal"] == "user-1"
try:
    bind(s, "user-2")
    assert False
except ValueError:
    pass
```

## Failure Modes
- Memory is keyed by platform handle and one user accumulates forked state.
- Identity is asserted from the request path without verification.
- A second device session merges state without reconciling conflicts.
- The binding method is not recorded and later audits cannot reproduce it.
- Identity conflicts are resolved by overwriting instead of failing closed.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 Google Gemini agents maintain the same memory, business context, and identity across different applications while running hours-long tasks (cloud.google.com, dated October 2026) ([public signal](https://cloud.google.com/blog/products/ai-machine-learning/welcome-to-gemini-at-work-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Memory Injection](../03-memory/memory-injection.md)
- [Hierarchical Memory Organization](../03-memory/hierarchical-memory-organization.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

---
title: "Cloud Agent Session State Scoping"
category: 03-memory
level: advanced
stability: experimental
description: "Scope what repository state, context, and agent work persists in a cloud-backed session before any task runs there."
added: "2026-11"
version: v1
related: [session-persistent-context-compression, automation-outcome-learning-memory]
tags: [memory, sessions, cloud, scoping]
---

# Cloud Agent Session State Scoping

## Description
Scope what repository state, context, and agent work persists in a cloud-backed session before any task runs there. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A cloud agent session persists code, context, and agent work across surfaces and the persisted-state boundary must be declared first.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the cloud session surface, the state classes in scope, and the declared pilot task and visibility review. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Declare which state classes such as code, context, and agent work may persist in the cloud session and which stay local.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Run a non-sensitive reproducible pilot task through the cloud session and record exactly what persisted.
4. Compare the persisted state against the declared scope and record deviations.
5. On unexpected persistence, halt and re-scope, and never continue a session with undeclared state in it.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def scope_check(persisted, declared):
    unexpected = [k for k in persisted if k not in declared]
    return {"ok": not unexpected, "unexpected": unexpected}
r = scope_check(["code", "context", "tokens"], ["code", "context"])
assert r["ok"] is False and r["unexpected"] == ["tokens"]
```

## Failure Modes
- A sensitive repository is sent to the cloud session because it was the default surface.
- What the cloud session persists is never reviewed so the scope is discovered from an incident.
- The pilot task is skipped and the first real task defines the persisted state.
- State classes are declared but never compared against what actually persisted.
- Re-scoping is postponed while sessions keep accumulating undeclared state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- GitHub Copilot launching a connected cloud experience that preserves a cloud-backed session of code, context, and agent work so a task can start on one surface and continue on another, with guidance to pilot a non-sensitive reproducible task first (AI Agent News Today, dated November 2, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Session Persistent Context Compression](session-persistent-context-compression.md)
- [Automation Outcome Learning Memory](automation-outcome-learning-memory.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |

---
title: "Agent Data Access Ledger Keeping"
category: 03-memory
level: advanced
stability: experimental
description: "Keep a durable ledger of what data an agent read, with which credential, and when, so unauthorized reads can be found even when no one noticed them happen."
added: "2026-10"
version: v1
related: [cross-agent-shared-memory-store, session-history-exposure-prevention]
tags: [ledger, data-access, audit, credentials]
---
# Agent Data Access Ledger Keeping

## Description
Keep a durable ledger of what data an agent read, with which credential, and when, so unauthorized reads can be found even when no one noticed them happen. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An audit later needs to show which records an agent touched even though no alert fired at the time.
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
3. Record every data access with credential scope, target, timestamp, and purpose into an append-only ledger, and reconcile it against authorized task scopes on a schedule.
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
def reconcile(ledger, scope):
    return [e for e in ledger if e["target"] not in scope]
ledger = [{"target": "orders"}, {"target": "hr-salaries"}]
assert reconcile(ledger, {"orders"}) == [{"target": "hr-salaries"}]
```

## Failure Modes
- Logs rotate away before anyone looks and the read history is gone.
- The credential scope in use is not recorded so authorization cannot be reconstructed.
- Logging is best-effort and drops entries under load.
- The ledger can be edited after the fact.
- The ledger exists but is never reconciled against task scopes.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the India CERT-In report that agents from several labs read personal and business data through exposed credentials while none of the victims noticed (accesso newsroom, dated October 31, 2026) ([public signal](https://accesso.com/news/accesso-intelligence-introduces-100-decision-skills-for-visitor-attractions/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Cross Agent Shared Memory Store](cross-agent-shared-memory-store.md)
- [Session History Exposure Prevention](session-history-exposure-prevention.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

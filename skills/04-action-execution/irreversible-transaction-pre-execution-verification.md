---
title: "Irreversible Transaction Pre Execution Verification"
category: 04-action-execution
level: advanced
stability: experimental
description: "Verify every precondition before an irreversible agent transaction by confirming authority, data confidence, and fallback state at the boundary."
added: "2026-11"
version: v1
related: [sms-booking-transaction-execution, lab-procedure-action-execution]
tags: [action, verification, irreversible, boundary]
---
# Irreversible Transaction Pre Execution Verification

## Description
Verify every precondition before an irreversible agent transaction by confirming authority, data confidence, and fallback state at the boundary. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent about to trigger a paid or irreversible action must verify preconditions immediately before execution.
- The outcome would change if the action fired with unverified data confidence or missing fallback state.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The transaction plan, the source data confidence record, and the fallback definition. |
| Outputs | A go or no-go boundary verdict with the verified preconditions and preserved state. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Freeze the transaction plan and list every precondition it depends on.
2. Verify the executing agent holds authority for this transaction class and amount.
3. Verify the source data record with its freshness, confidence, and provenance.
4. Verify a fallback exists for each failure mode of the transaction.
5. Re-check all preconditions atomically at the boundary, immediately before execution.
6. Emit the verdict and preserve the pre-execution state for any post-failure review.

## Outputs
| Area | Contract |
|---|---|
| Primary | A boundary verdict naming each verified precondition and the preserved pre-execution state for rollback. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def verify_boundary(plan, authority, data, fallback):
    checks = {"authority": authority, "confidence": data["confidence"] >= 0.9, "fallback": bool(fallback)}
    return {"go": all(checks.values()), "checks": checks}
r = verify_boundary({}, True, {"confidence": 0.95}, "refund-flow")
assert r["go"] is True and r["checks"]["confidence"] is True
```

## Failure Modes
- Preconditions are verified minutes before execution and the data changes in between.
- Authority is assumed from a previous transaction instead of re-checked at the boundary.
- A transaction fires with a confidence score below the declared threshold.
- The fallback is named but never tested, so the first failure has no recovery path.
- The pre-execution state is discarded after a successful transaction, blocking audit.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Dataline advising operators to record the source, freshness, confidence, and fallback behavior for every external data call before connecting an agent to paid or irreversible actions (AI Agent News Today, dated November 2, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Sms Booking Transaction Execution](sms-booking-transaction-execution.md)
- [Lab Procedure Action Execution](lab-procedure-action-execution.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |

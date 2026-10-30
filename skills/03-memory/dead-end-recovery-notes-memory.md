---
title: "Dead End Recovery Notes Memory"
category: 03-memory
level: advanced
stability: experimental
description: "Record explored dead ends during long-horizon tasks so that later sessions never re-walk a failed path."
added: "2026-10"
version: v1
related: [model-release-ledger-delta-memory, long-horizon-planning]
tags: [dead-ends, notes, memory, recovery]
---
# Dead End Recovery Notes Memory

## Description
Record explored dead ends during long-horizon tasks so that later sessions never re-walk a failed path. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent works across days on a hard problem and needs durable notes on which approaches already failed and why.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Write each dead end as a dated note naming the attempted approach, the observed failure, and the evidence, then check new plans against the ledger before starting.
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
def record(ledger, approach, why):
    entry = {"approach": approach, "why": why, "checked": False}
    ledger.append(entry)
    return entry
def blocked(ledger, approach):
    return any(e["approach"] == approach for e in ledger)
l = []
record(l, "binary search on sorted prefix", "input not sorted")
assert blocked(l, "binary search on sorted prefix") and not blocked(l, "linear scan")
```

## Failure Modes
- Dead ends are recorded without the failure reason and later sessions cannot tell why they failed.
- The ledger is consulted only on resume and fresh plans walk the same path the same day.
- Notes are keyed by vague descriptions and distinct approaches collide.
- A partial success is recorded as a dead end and a working path is lost.
- The ledger grows unbounded and lookup cost makes it unusable.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the Gemini 4 Carbon internal validation describes the model autonomously navigating dead ends across multi-day engineering runs (blog.luandnh.com, dated October 29, 2026) ([public signal](https://blog.luandnh.com/en/ai-daily/2026-10-29/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Model Release Ledger Delta Memory](model-release-ledger-delta-memory.md)
- [Long Horizon Planning](../02-reasoning/long-horizon-planning.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

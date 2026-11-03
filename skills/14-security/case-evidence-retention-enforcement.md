---
title: "Case Evidence Retention Enforcement"
category: 14-security
level: advanced
stability: experimental
description: "Enforce evidence retention for consequential cases by keeping every decision reconstructable with its evidence for the full retention period."
added: "2026-11"
version: v1
related: [cross-surface-session-data-minimization, preflight-credential-check-verification]
tags: [security, retention, evidence, audit]
---
# Case Evidence Retention Enforcement

## Description
Enforce evidence retention for consequential cases by keeping every decision reconstructable with its evidence for the full retention period. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Every consequential case decision must remain reconstructable from retained evidence.
- The outcome would change if evidence were deleted while the decision it supported still stood.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The case decision record, the evidence set, and the retention policy per case class. |
| Outputs | A retention ledger per case with evidence completeness verified. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Record every decision with the evidence set that supported it at decision time.
2. Resolve the retention period for the case class from the written policy.
3. Store the evidence under the case identifier for the resolved period.
4. Verify completeness: each decision references only retained, readable evidence.
5. Block deletions that would break a live decision trace and record the block.
6. Emit the retention ledger with completeness results for audit review.

## Outputs
| Area | Contract |
|---|---|
| Primary | A retention ledger naming each case, its retained evidence, the policy period, and completeness verification results. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def enforce_retention(decisions, evidence, policy_days):
    broken = [d["id"] for d in decisions if any(e not in evidence for e in d["evidence_refs"])]
    return {"complete": not broken, "broken_decisions": broken}
d = [{"id": "c1", "evidence_refs": ["e1", "e2"]}]
r = enforce_retention(d, {"e1": "doc", "e3": "x"}, 365)
assert r["complete"] is False and r["broken_decisions"] == ["c1"]
```

## Failure Modes
- Evidence is deleted on a storage schedule without checking live decision traces.
- Retention periods are set per case by the agent instead of the written policy.
- Completeness is verified once at retention start and never re-checked.
- Deletion blocks are logged but the deletion still proceeds manually.
- The ledger lists cases without completeness results, so audit cannot classify them.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Persona defining which decisions an agent may recommend, which require human approval, and what evidence must be retained for every case (AI Agent News Today, dated November 2, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Cross Surface Session Data Minimization](cross-surface-session-data-minimization.md)
- [Preflight Credential Check Verification](preflight-credential-check-verification.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |

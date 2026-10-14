---
title: "Legal Contract Clause Risk Flagging"
category: 16-domain-specific
level: advanced
stability: experimental
description: "Flag high-risk contract clauses such as indemnities, auto-renewals, and liability caps with the triggering language."
added: "2026-10"
version: v1
related: [contract-review, compliance-checking, legal-research]
tags: [legal, contract, clause, risk]
---
# Legal Contract Clause Risk Flagging

## Description
Flag high-risk contract clauses such as indemnities, auto-renewals, and liability caps with the triggering language. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires legal contract clause risk flagging before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for legal contract clause risk flagging. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the legal contract clause risk flagging steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
RISK = ["indemnify", "auto-renew"]
def flag(clause):
    return [r for r in RISK if r in clause.lower()]
assert flag("Supplier shall indemnify Buyer") == ["indemnify"]
```

## Failure Modes
- Acting outside the declared task boundary.
- Assuming an estimate or preview equals the verified effect.
- Retrying without preserving state or evidence.
- Using stale inputs as if they were current.
- Reporting success without checking the resulting state.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Contract analysis requests in 2026 focus on flagging risky clause types with cited language. These are dated public signals, not adoption metrics.

## Related
- contract-review.md
- compliance-checking.md
- legal-research.md

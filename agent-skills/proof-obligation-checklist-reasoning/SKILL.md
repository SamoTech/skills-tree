---
name: proof-obligation-checklist-reasoning
description: Derive a checklist of proof obligations from a claim and its assumptions, then discharge each obligation with recorded evidence.
metadata:
  source: skills/02-reasoning/proof-obligation-checklist-reasoning.md
  category: 02-reasoning
  version: "v1"
---
# Proof Obligation Checklist Reasoning

## Description
Derive a checklist of proof obligations from a claim and its assumptions, then discharge each obligation with recorded evidence. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires proof obligation checklist reasoning before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for proof obligation checklist reasoning. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the proof obligation checklist reasoning steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def discharged(claims, proofs):
    return set(claims) <= set(proofs)
assert discharged(["a", "b"], ["a", "b"]) is True
assert discharged(["a", "b"], ["a"]) is False
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
Formal-methods style proof obligations appear in recurring requests for auditable agent reasoning steps. These are dated public signals, not adoption metrics.

## Related
- deductive-reasoning.md
- assumption-mapping.md
- solution-verification.md

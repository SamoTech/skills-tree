---
name: chain-of-verification
description: Generate verification questions for a draft answer, answer them independently, and revise the draft from verified facts.
metadata:
  source: skills/02-reasoning/chain-of-verification.md
  category: 02-reasoning
  version: "v1"
---
# Chain of Verification

## Description
Generate verification questions for a draft answer, answer them independently, and revise the draft from verified facts. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires chain of verification before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for chain of verification. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the chain of verification steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def revise(draft, checks):
    return all(checks) if draft else False
assert revise(True, [True, True]) is True
assert revise(True, [True, False]) is False
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
Chain-of-verification is a recurring 2026 request for reducing hallucinations in multi-step agent answers. These are dated public signals, not adoption metrics.

## Related
- chain-of-thought.md
- self-consistency.md
- solution-verification.md

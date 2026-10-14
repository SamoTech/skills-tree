---
name: securities-disclosure-drafting
description: Draft securities disclosure sections with required item coverage, materiality language, and internal-consistency checks.
metadata:
  source: skills/16-domain-specific/securities-disclosure-drafting.md
  category: 16-domain-specific
  version: "v1"
---
# Securities Disclosure Drafting

## Description
Draft securities disclosure sections with required item coverage, materiality language, and internal-consistency checks. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires securities disclosure drafting before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for securities disclosure drafting. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the securities disclosure drafting steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def covered(items, required):
    return sorted(set(required) - set(items))
assert covered(["risk", "mgmt"], ["risk", "mgmt", "legal"]) == ["legal"]
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
Regulated disclosure drafting with coverage checks is a recurring financial-agent request. These are dated public signals, not adoption metrics.

## Related
- compliance-checking.md
- regulatory-change-monitoring.md
- financial-statement.md

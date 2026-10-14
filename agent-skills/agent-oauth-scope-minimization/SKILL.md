---
name: agent-oauth-scope-minimization
description: Request the minimal OAuth scopes an agent needs, with per-task elevation and periodic scope review.
metadata:
  source: skills/14-security/agent-oauth-scope-minimization.md
  category: 14-security
  version: "v1"
---
# Agent Oauth Scope Minimization

## Description
Request the minimal OAuth scopes an agent needs, with per-task elevation and periodic scope review. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires agent oauth scope minimization before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for agent oauth scope minimization. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent oauth scope minimization steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def minimize(requested, needed):
    drop = set(requested) - set(needed)
    return sorted(drop)
assert minimize(["read", "write", "admin"], ["read"]) == ["admin", "write"]
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
Scope minimization for agents is a recurring 2026 enterprise guardrail checklist item. These are dated public signals, not adoption metrics.

## Related
- short-lived-credential-acquisition.md
- tool-guardrails.md
- need-to-know-memory-scoping.md

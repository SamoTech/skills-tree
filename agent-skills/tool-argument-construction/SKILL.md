---
name: tool-argument-construction
description: Construct tool call arguments from task context with explicit unit, format, and constraint checks before invocation, and validate against the tool schema.
metadata:
  source: skills/07-tool-use/tool-argument-construction.md
  category: 07-tool-use
  version: "v1"
---

# Tool Argument Construction

## Description
Construct tool call arguments from task context with explicit unit, format, and constraint checks before invocation, and validate against the tool schema. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires tool argument construction before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for tool argument construction. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the tool argument construction steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# Tool Argument Construction: deterministic check
allowed = {"idle": {"running"}, "running": {"done", "failed"}, "failed": {"idle"}}

def transition(state, nxt):
    return nxt in allowed.get(state, set())

assert transition("idle", "running")
assert not transition("idle", "done")
print("transitions checked")
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
Function-calling reliability recurs in 2026 agent failure reports; argument construction with schema validation is a published mitigation. These are dated public signals, not adoption metrics.

## Related
- function-calling.md
- tool-schema-design.md
- tool-output-validation.md

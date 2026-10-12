---
name: inter-agent-protocol-compliance
description: Verify that agent-to-agent exchanges conform to the declared protocol contract, including schema and trust-boundary rules.
metadata:
  source: skills/09-agentic-patterns/inter-agent-protocol-compliance.md
  category: 09-agentic-patterns
  version: "v1"
---

# Inter-Agent Protocol Compliance

## Description
Verify that agent-to-agent exchanges conform to the declared protocol contract, including schema and trust-boundary rules. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires inter-agent protocol compliance before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for inter-agent protocol compliance. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the inter-agent protocol compliance steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# Inter-Agent Protocol Compliance: deterministic check
def check_budget(estimate, limit):
    if estimate > limit:
        raise ValueError("estimate %s exceeds limit %s" % (estimate, limit))
    return "approved"

assert check_budget(3, 5) == "approved"
try:
    check_budget(7, 5)
    raise AssertionError("should have raised")
except ValueError:
    print("guard held")
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
A2A and MCP interop testing across trust boundaries is an active 2026 ecosystem workstream. These are dated public signals, not adoption metrics.

## Related
- agent-handoffs.md
- agent-as-tool.md
- subagent-delegation.md

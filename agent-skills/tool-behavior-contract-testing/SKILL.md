---
name: tool-behavior-contract-testing
description: Test third-party tools against their declared behavior contracts, including schemas, side effects, latency, and error semantics, before relying on them in production flows.
metadata:
  source: skills/07-tool-use/tool-behavior-contract-testing.md
  category: 07-tool-use
  version: "v1"
---

# Tool Behavior Contract Testing

## Description
Test third-party tools against their declared behavior contracts, including schemas, side effects, latency, and error semantics, before relying on them in production flows. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- Multiple inputs or candidates compete and must be resolved by explicit criteria.
- A wrong intermediate result would propagate into consequential actions.
- The task repeats and benefits from a deterministic procedure.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for tool behavior contract testing. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the tool behavior contract testing procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Tool Behavior Contract Testing: deterministic check
candidates = [{"id": "a", "score": 0.8, "cost": 2}, {"id": "b", "score": 0.95, "cost": 9}]
eligible = [c for c in candidates if c["score"] >= 0.8]
selected = min(eligible, key=lambda c: c["cost"])
assert selected["id"] == "a"
print("selected:", selected["id"])
```

## Failure Modes
- Proceeding with tool behavior contract testing without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Agent evaluation is the top 2026 developer pain point; tool contract testing is a named component of agent test suites. These are dated public signals, not adoption metrics.

## Related
- tool-output-validation.md
- tool-review-loops.md
- tool-schema-design.md

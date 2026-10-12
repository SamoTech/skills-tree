---
name: theory-of-mind-reasoning
description: Model the beliefs, goals, and knowledge states of other agents and users explicitly, and check communication against what the other party can actually know.
metadata:
  source: skills/02-reasoning/theory-of-mind-reasoning.md
  category: 02-reasoning
  version: "v1"
---

# Theory of Mind Reasoning

## Description
Model the beliefs, goals, and knowledge states of other agents and users explicitly, and check communication against what the other party can actually know. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- Multiple inputs or candidates compete and must be resolved by explicit criteria.
- A wrong intermediate result would propagate into consequential actions.
- The task repeats and benefits from a deterministic procedure.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for theory of mind reasoning. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the theory of mind reasoning procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Theory of Mind Reasoning: deterministic check
def validate(record, required):
    missing = [k for k in required if k not in record]
    return (True, []) if not missing else (False, missing)

ok, missing = validate({"id": "x", "source": "y"}, ["id", "source"])
assert ok and not missing
print("validated")
```

## Failure Modes
- Proceeding with theory of mind reasoning without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Multi-agent and A2A interop work in 2026 requires modeling counterpart state across trust boundaries; published agent research names theory of mind as an open challenge. These are dated public signals, not adoption metrics.

## Related
- meta-cognition.md
- commonsense.md
- negotiation.md

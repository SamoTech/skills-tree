---
name: hierarchical-memory-organization
description: Organize memories into layered stores such as working, session, and long-term, with explicit promotion, demotion, and lookup rules between layers.
metadata:
  source: skills/03-memory/hierarchical-memory-organization.md
  category: 03-memory
  version: "v1"
---
# Hierarchical Memory Organization

## Description
Organize memories into layered stores such as working, session, and long-term, with explicit promotion, demotion, and lookup rules between layers. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires hierarchical memory organization before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for hierarchical memory organization. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the hierarchical memory organization procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Hierarchical Memory Organization: deterministic check
def validate(record, required):
    missing = [k for k in required if k not in record]
    return (True, []) if not missing else (False, missing)

ok, missing = validate({"id": "x", "source": "y"}, ["id", "source"])
assert ok and not missing
print("validated")
```

## Failure Modes
- Proceeding with hierarchical memory organization without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Hierarchical memory management is explicitly requested in public issue #87 of this repository and recurs in 2026 agent-memory architecture discussions. These are dated public signals, not adoption metrics.

## Related
- memory-indexing.md
- long-term-memory.md
- memory-consolidation.md

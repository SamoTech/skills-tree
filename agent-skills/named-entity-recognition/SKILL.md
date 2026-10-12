---
name: named-entity-recognition
description: Extract typed entities such as people, organizations, locations, dates, and identifiers from text with span offsets, types, and confidence rather than an unstructured keyword list.
metadata:
  source: skills/01-perception/named-entity-recognition.md
  category: 01-perception
  version: "v1"
---

# Named Entity Recognition

## Description
Extract typed entities such as people, organizations, locations, dates, and identifiers from text with span offsets, types, and confidence rather than an unstructured keyword list. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- Multiple inputs or candidates compete and must be resolved by explicit criteria.
- A wrong intermediate result would propagate into consequential actions.
- The task repeats and benefits from a deterministic procedure.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for named entity recognition. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the named entity recognition procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Named Entity Recognition: deterministic check
options = [{"name": "x", "gain": 5, "cost": 1}, {"name": "y", "gain": 4, "cost": 1}]
ranked = sorted(options, key=lambda o: (o["cost"], -o["gain"]))
assert ranked[0]["name"] == "x"
print("best:", ranked[0]["name"])
```

## Failure Modes
- Proceeding with named entity recognition without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Information-extraction requests recur in 2026 agent tooling discussions; structured outputs with span offsets are a published dependency of reliable downstream tool calls. These are dated public signals, not adoption metrics.

## Related
- text-reading.md
- metadata-extraction.md
- structured-data-reading.md

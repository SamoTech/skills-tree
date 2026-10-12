---
name: a2a-agent-card-authoring
description: Create and maintain A2A agent cards that accurately declare skills, endpoints, authentication, and constraints, so counterpart agents can make trust decisions.
metadata:
  source: skills/07-tool-use/a2a-agent-card-authoring.md
  category: 07-tool-use
  version: "v1"
---

# A2A Agent Card Authoring

## Description
Create and maintain A2A agent cards that accurately declare skills, endpoints, authentication, and constraints, so counterpart agents can make trust decisions. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires a2a agent card authoring before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for a2a agent card authoring. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the a2a agent card authoring procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# A2A Agent Card Authoring: deterministic check
seen = {}
conflicts = []
for item in [{"k": "a", "v": 1}, {"k": "a", "v": 2}, {"k": "b", "v": 3}]:
    if item["k"] in seen and seen[item["k"]] != item["v"]:
        conflicts.append(item["k"])
    seen[item["k"]] = item["v"]
assert conflicts == ["a"]
print("conflicts:", conflicts)
```

## Failure Modes
- Proceeding with a2a agent card authoring without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
A2A interoperability across trust boundaries is a 2026 trend; agent cards are the published discovery artifact. These are dated public signals, not adoption metrics.

## Related
- a2a-tool.md
- function-calling.md
- tool-schema-design.md

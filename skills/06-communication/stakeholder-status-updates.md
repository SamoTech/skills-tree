---
title: "Stakeholder Status Updates"
category: 06-communication
level: advanced
stability: experimental
description: "Write concise progress updates for stakeholders that state what changed, what is next, and what is blocked, with evidence links and no status inflation."
added: "2026-10"
version: v1
related: [report-writing, summarization, incident-communication]
tags: [stakeholder, status, updates, communication]
---

# Stakeholder Status Updates

## Description
Write concise progress updates for stakeholders that state what changed, what is next, and what is blocked, with evidence links and no status inflation. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- Multiple inputs or candidates compete and must be resolved by explicit criteria.
- A wrong intermediate result would propagate into consequential actions.
- The task repeats and benefits from a deterministic procedure.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for stakeholder status updates. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the stakeholder status updates procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Stakeholder Status Updates: deterministic check
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
- Proceeding with stakeholder status updates without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Progress, plans, and problems style updates are a recurring 2026 team-communication request; report-writing agents need explicit honesty contracts. These are dated public signals, not adoption metrics.

## Related
- report-writing.md
- summarization.md
- incident-communication.md

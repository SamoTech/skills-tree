---
title: "Preference Drift Detection"
category: 03-memory
level: basic
stability: experimental
description: "Detect when stored user preferences contradict recent behavior and propose a memory update with evidence rather than silently keeping stale facts."
added: "2026-10"
version: v1
related: [user-profile-memory, fact-verification-memory, user-profile]
tags: [preference, drift, detection, memory]
---
# Preference Drift Detection

## Description
Detect when stored user preferences contradict recent behavior and propose a memory update with evidence rather than silently keeping stale facts. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- The task has explicit constraints such as time, budget, or safety that must gate the outcome.
- A silent failure mode exists that must be surfaced rather than swallowed.
- Verification evidence is required before the result is trusted.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for preference drift detection. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the preference drift detection procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Preference Drift Detection: deterministic check
options = [{"name": "x", "gain": 5, "cost": 1}, {"name": "y", "gain": 4, "cost": 1}]
ranked = sorted(options, key=lambda o: (o["cost"], -o["gain"]))
assert ranked[0]["name"] == "x"
print("best:", ranked[0]["name"])
```

## Failure Modes
- Proceeding with preference drift detection without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Personalization agents in 2026 must handle changing preferences; drift detection appears in published user-modeling guidance. These are dated public signals, not adoption metrics.

## Related
- user-profile-memory.md
- fact-verification-memory.md
- user-profile.md

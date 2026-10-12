---
title: "Tool Deprecation Handling"
category: 07-tool-use
level: basic
stability: experimental
description: "Detect deprecated tool versions and migrate calls to supported alternatives with a compatibility plan, instead of staying pinned to end-of-life versions."
added: "2026-10"
version: v1
related: [api-version-pinning, tool-schema-design, tool-inventory-cataloging]
tags: [tool, deprecation, handling, tool]
---

# Tool Deprecation Handling

## Description
Detect deprecated tool versions and migrate calls to supported alternatives with a compatibility plan, instead of staying pinned to end-of-life versions. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- The task has explicit constraints such as time, budget, or safety that must gate the outcome.
- A silent failure mode exists that must be surfaced rather than swallowed.
- Verification evidence is required before the result is trusted.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for tool deprecation handling. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the tool deprecation handling procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Tool Deprecation Handling: deterministic check
options = [{"name": "x", "gain": 5, "cost": 1}, {"name": "y", "gain": 4, "cost": 1}]
ranked = sorted(options, key=lambda o: (o["cost"], -o["gain"]))
assert ranked[0]["name"] == "x"
print("best:", ranked[0]["name"])
```

## Failure Modes
- Proceeding with tool deprecation handling without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
API churn handling recurs in 2026 agent maintenance threads; version-pinning guidance recommends planned migration. These are dated public signals, not adoption metrics.

## Related
- api-version-pinning.md
- tool-schema-design.md
- tool-inventory-cataloging.md

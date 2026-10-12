---
title: "Need-to-Know Memory Scoping"
category: 03-memory
level: advanced
stability: experimental
description: "Restrict which memories a subagent or tool context can access to the minimum set the task requires, with explicit grants and audit of scope expansion."
added: "2026-10"
version: v1
related: [retention-policy, user-profile-memory, least-privilege-scoping]
tags: [need, to, know, memory, memory]
---
# Need-to-Know Memory Scoping

## Description
Restrict which memories a subagent or tool context can access to the minimum set the task requires, with explicit grants and audit of scope expansion. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- Multiple inputs or candidates compete and must be resolved by explicit criteria.
- A wrong intermediate result would propagate into consequential actions.
- The task repeats and benefits from a deterministic procedure.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for need-to-know memory scoping. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the need-to-know memory scoping procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Need-to-Know Memory Scoping: deterministic check
attempts = []
def flaky(n):
    attempts.append(n)
    return n >= 3

tries, max_tries, done = 0, 5, False
while tries < max_tries:
    tries += 1
    if flaky(tries):
        done = True
        break
assert done and tries == 3
print("succeeded after", tries, "attempts")
```

## Failure Modes
- Proceeding with need-to-know memory scoping without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Privacy-by-design and least-privilege agent contexts are named 2026 requirements in enterprise agent adoption guidance. These are dated public signals, not adoption metrics.

## Related
- retention-policy.md
- user-profile-memory.md
- least-privilege-scoping.md

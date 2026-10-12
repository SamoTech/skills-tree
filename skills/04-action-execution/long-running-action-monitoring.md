---
title: "Long-Running Action Monitoring"
category: 04-action-execution
level: intermediate
stability: experimental
description: "Track actions whose completion outlives a single turn, such as jobs, deploys, and exports, with polling cadence, progress thresholds, and explicit timeout escalation."
added: "2026-10"
version: v1
related: [process-management, scheduled-execution, wait-sleep]
tags: [long, running, action, monitoring, action]
---
# Long-Running Action Monitoring

## Description
Track actions whose completion outlives a single turn, such as jobs, deploys, and exports, with polling cadence, progress thresholds, and explicit timeout escalation. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires long-running action monitoring before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for long-running action monitoring. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the long-running action monitoring procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Long-Running Action Monitoring: deterministic check
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
- Proceeding with long-running action monitoring without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Long-running orchestration is a 2026 MCP Tasks theme; the 2026-07-28 specification release candidate introduces Tasks for exactly this class of work. These are dated public signals, not adoption metrics.

## Related
- process-management.md
- scheduled-execution.md
- wait-sleep.md

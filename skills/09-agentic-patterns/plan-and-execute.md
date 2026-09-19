---
title: Plan-and-Execute
category: 09-agentic-patterns
level: intermediate
stability: stable
description: Separate planning from execution so a planner produces a bounded task graph and an executor performs and verifies each step.
related: [09-agentic-patterns/react, 02-reasoning/planning-decomposition]
added: "2025-03"
version: v2
---

# Plan-and-Execute

## Description

Separate planning from execution: a planner produces a bounded sequence or task graph, then an executor performs each step and records its result. Replanning is allowed only when a step fails or new evidence invalidates the remaining plan.

## When to Use

Use for multi-step work where explicit decomposition improves verification or recovery. Avoid it for simple deterministic operations where planning overhead exceeds the task itself.

## Inputs / Outputs

Input: task, constraints, available tools, and a verification policy. Output: plan steps with explicit status, execution results, verification results, and unresolved failures.

## Example

```python
from dataclasses import dataclass

@dataclass
class Step:
    name: str
    status: str = "pending"


def execute(plan: list[Step], run):
    for step in plan:
        result = run(step.name)
        step.status = "passed" if result else "failed"
        if step.status == "failed":
            break
    return plan
```

## Failure Modes

- Invalid plan: reject missing prerequisites or unverifiable steps before execution.
- Step failure: stop or replan according to the declared recovery policy; do not silently skip the failed step.
- Stale assumptions: invalidate affected downstream steps when new evidence changes a prerequisite.
- Tool failure: distinguish infrastructure failure from task failure.
- Unverified completion: never mark a step complete solely because an action was attempted.

## Output Contract

Every step has a stable identifier or name and an explicit status. A completed step must have a verification result when the policy requires verification. Failed or skipped steps must retain a reason.

## Design Rules

Keep planning and execution state separate. Bound plan size and replanning attempts. Make dependencies explicit. Verify outputs before allowing dependent steps to proceed. Preserve an execution trace sufficient to reconstruct why the final state was reached.

## Related Skills

- `09-agentic-patterns/react`
- `02-reasoning/planning-decomposition`

## Changelog

- v2 (2026-09): normalized metadata and added explicit planning, execution, recovery, and verification contracts.

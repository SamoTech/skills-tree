---
name: deadline-propagation
description: Carry one absolute end-time deadline through every orchestration hop so each step budgets its remaining time, children inherit a tightened deadline, and late results are discarded rather than delivered.
metadata:
  source: skills/15-orchestration/deadline-propagation.md
  category: 15-orchestration
  version: "v1"
---

# Deadline Propagation

Category: Orchestration | Level: advanced | Stability: experimental | Version: v1

## Description

Relative timeouts do not compose: three sequential steps with a 5-second timeout each can stall a caller for 15 seconds. Deadline propagation fixes the arithmetic by carrying one absolute end time: each hop computes remaining time against the same clock, children receive the tighter of their own budget and the parent's remaining time, and results that arrive after the deadline are discarded instead of patched into the run late.

## When to Use

Use in any multi-hop orchestration — service calls, subagent trees, pipelines — where a caller's total wait must stay bounded.

Do not substitute per-hop timeouts without checking the sum; a chain of local limits is not a global one.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `deadline` | `timestamp` | Yes | The absolute end time for the whole run |
| `now` | `timestamp` | Yes | Injectable current time for deterministic decisions |
| `step_budget` | `duration` | No | The step's own preferred local budget |
| `children` | `list[step]` | No | Downstream hops inheriting the deadline |

## Procedure

1. Set one absolute deadline at run start, from the caller's wall-clock budget; it is a timestamp, not a duration.
2. At each hop, compute remaining time as deadline minus now; a hop with no remaining time fails fast without starting.
3. Give each child the tighter of its own budget and the parent's remaining time minus the parent's reserve.
4. Reject late results even if they eventually complete; a result after the deadline is not a result for this run.
5. Record per-step time consumption so postmortems can show where the budget went.
6. Reserve a margin for serialization and cleanup; a deadline with no reserve fails at the packaging step.

## Outputs

| Output | Type | Description |
|---|---|---|
| `remaining` | `duration` | Time left at the decision point |
| `child_deadline` | `timestamp | null` | The tightened deadline handed to a child |
| `disposition` | `proceed | skip | late` | Whether the step or result is usable |

## Runnable Example

```python
def child_deadline(deadline, now, parent_reserve=0.5):
    """Tighten the parent deadline for a child hop."""
    remaining = deadline - now - parent_reserve
    if remaining <= 0:
        return None, "skip"
    return deadline - parent_reserve, "proceed"

def classify_result(ready_at, deadline):
    return "late" if ready_at > deadline else "usable"

print(child_deadline(deadline=100, now=40))
print(classify_result(ready_at=99, deadline=100))
print(classify_result(ready_at=101, deadline=100))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Relative-only budgets | Per-step timeouts whose sum exceeds the caller's budget | Propagate one absolute deadline |
| Deadline-blind queues | Enqueued work starts without checking the clock | Check remaining time at dequeue, not just enqueue |
| Children outliving parents | Children keep their local budget after the parent expired | Hand children the tighter of own budget and parent remaining |
| Late results accepted | Stragglers patched in after expiry | Classify post-deadline results as late and discard |
| No time accounting | Postmortems cannot say where time went | Record per-step consumption against budget |

## Security and Authority Boundary

Deadline propagation bounds wall-clock time; it does not certify the quality of what was rushed to fit. Quality gates, evaluation, and review apply the same standards regardless of how much budget a step had.

## Evidence

This skill is grounded in dated public implementation references:

1. The gRPC core concepts documentation on deadlines and cancellation (https://grpc.io/docs/what-is-grpc/core-concepts/).
2. Wikipedia's overview of timeouts in computing (https://en.wikipedia.org/wiki/Timeout_%28computing%29).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Budget Management](budget-management.md) — the cost-budgeting sibling of time budgets.
- [Parallel Execution](parallel-execution.md) — parallel dispatch where each branch must inherit the shared deadline.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |

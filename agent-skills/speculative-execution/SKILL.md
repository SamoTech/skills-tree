---
name: speculative-execution
description: Reduce latency by running multiple candidate paths concurrently and taking the first acceptable result, with explicit acceptance criteria, duplicate-write guards, and cost accounting.
metadata:
  source: skills/15-orchestration/speculative-execution.md
  category: 15-orchestration
  version: "v1"
---

# Speculative Execution

Category: Orchestration | Level: advanced | Stability: experimental | Version: v1

## Description

Speculation buys latency with resources. The skill covers choosing which steps are worth speculating, defining acceptance criteria per path before launch, launching redundant candidates against independent resources, taking the first result that passes the criteria, and cancelling the losers. Because duplicated work multiplies cost and side effects, every speculative path must be idempotent and side-effect-free until acceptance.

## When to Use

Use when a step is both slow and uncertain: slow model calls, flaky external services, or retrieval where any of several paths can satisfy the caller.

Do not speculate on steps with external side effects before acceptance. Two accepted writes is a correctness bug that costs more than the latency saved.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `step` | `object` | Yes | The slow or uncertain step eligible for speculation |
| `candidate_paths` | `list` | Yes | Independent paths expected to produce an acceptable result |
| `acceptance` | `object` | Yes | Pass criteria and the rule for cancelling losers |

## Procedure

1. Confirm the step is worth speculating: latency saved must exceed added resource cost.
2. Write acceptance criteria before launching anything, including how the winner is judged.
3. Verify every candidate path is idempotent and free of external side effects before acceptance.
4. Launch candidates concurrently against independent resources to avoid correlated failure.
5. Take the first result that passes acceptance and cancel the losers immediately.
6. Record per-path outcomes and cost so the speculation decision can be audited and retuned.

## Outputs

| Output | Type | Description |
|---|---|---|
| `winner` | `object` | The accepted result with its path and acceptance evidence |
| `cancellation_log` | `list` | Cancelled candidates with their progress at cancellation |
| `cost_report` | `object` | Resource spent on losers versus latency saved |

## Runnable Example

```python
def pick_winner(results, accept_fn):
    """results: [(path, value, elapsed)] in completion order"""
    for path, value, elapsed in results:
        if accept_fn(value):
            return {"winner": path, "value": value, "elapsed": elapsed}
    return {"winner": None, "reason": "no candidate accepted"}

print(pick_winner(
    [("fast-model", {"score": 0.62}, 2.0), ("big-model", {"score": 0.91}, 9.0)],
    lambda v: v["score"] >= 0.9,
))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Duplicated side effects | Candidates mutated external state pre-acceptance | Idempotent paths with side effects only after acceptance |
| Winner without criteria | First finisher accepted regardless of quality | Written acceptance criteria evaluated per result |
| Correlated failure | Candidates shared the same rate-limited resource | Independent resources per candidate path |
| Cost runaway | Speculation applied to cheap steps | Speculate only where latency saved exceeds cost |
| Zombie candidates | Losers kept running after a winner was accepted | Cancel immediately and verify cancellation |

## Security and Authority Boundary

Speculation multiplies external calls, which multiplies exposure to rate limits and data egress. Scope candidate paths to the least privilege needed, do not speculate across security boundaries where one path has wider authority than the task requires, and audit cancelled paths for partial writes.

## Evidence

This skill is grounded in dated public implementation references:

1. The Wikipedia article on speculative execution as a latency strategy (https://en.wikipedia.org/wiki/Speculative_execution).
2. The Apache Hadoop documentation, which uses speculative task execution for stragglers (https://hadoop.apache.org/docs/stable/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Parallel Execution](parallel-execution.md) — the concurrency primitive speculation launches candidates on.
- [Cost-Aware Model Routing](cost-aware-model-routing.md) — the cost accounting that decides whether speculation pays.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |

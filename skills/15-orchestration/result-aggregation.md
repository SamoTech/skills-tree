---
title: "Result Aggregation"
category: 15-orchestration
level: intermediate
stability: experimental
description: "Collect parallel task results into one ordered report with per-task status, explicit handling of failures and stragglers, and deterministic merge order so the combined output stays reproducible."
added: "2026-10"
version: v1
related: ["parallel-execution", "subagent-spawning"]
---

# Result Aggregation

Category: Orchestration | Level: intermediate | Stability: experimental | Version: v1

## Description

Parallel execution multiplies results and failure shapes at the same time. Aggregation turns a cloud of futures into one report: each task contributes a (id, status, output) tuple, missing tasks appear as missing instead of vanishing, and the merge order is deterministic. The aggregate carries per-task provenance, so any claim in the combined output can be traced back to the task that produced it.

## When to Use

Use whenever work is split across parallel subagents or workers and the caller needs one combined, trustworthy answer.

Do not use unordered ad-hoc merging; a merge that depends on arrival order produces a different output on every run.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `expected_ids` | `list[task_id]` | Yes | Every task the plan dispatched |
| `results` | `map[task_id -> result]` | Yes | Completed results, keyed by task id |
| `merge_policy` | `per_status` | Yes | How completed, failed, and missing tasks are merged |
| `timeout` | `duration` | Yes | How long the aggregate waits for stragglers |

## Procedure

1. Register the full expected task id set at dispatch time; the plan, not the arrival count, defines completeness.
2. Collect results as (id, status, output) tuples; failures are results, not exceptions to swallow.
3. On aggregation, subtract completed ids from expected ids; anything unaccounted is missing — with the timeout recorded.
4. Apply the merge policy per status: include completed, record failed, mark missing; the policy decides what missing means for the whole.
5. Merge in task id order, never arrival order, so identical inputs produce identical output.
6. Emit the aggregate with per-task provenance: which task produced which part of the combined result.

## Outputs

| Output | Type | Description |
|---|---|---|
| `aggregate` | `merged_payload` | The combined result under the merge policy |
| `task_report` | `list[(id, status, note)]` | Per-task disposition with provenance |
| `complete` | `boolean` | Whether all expected tasks completed |

## Runnable Example

```python
def aggregate_results(expected_ids, results):
    """Merge per-task results in deterministic id order."""
    report = []
    for task_id in sorted(expected_ids):
        outcome = results.get(task_id)
        if outcome is None:
            report.append((task_id, "missing", "no result by timeout"))
        elif outcome.get("error"):
            report.append((task_id, "failed", outcome["error"]))
        else:
            report.append((task_id, "completed", outcome["output"]))
    return report

expected = ["scan-a", "scan-b", "scan-c"]
results = {"scan-c": {"output": "clean"}, "scan-a": {"error": "timeout"}}
for row in aggregate_results(expected, results):
    print(row)
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Arrival-order merges | Results folded in completion order | Merge in task id order |
| Vanished tasks | Dispatched ids never checked again | Diff expected ids against collected ids |
| Exception swallowing | Worker errors absorbed into nothing | Record failures as first-class results |
| Unbounded waits | Aggregate blocks on stragglers indefinitely | Enforce the timeout and mark missing |
| Provenance loss | Merge output loses task attribution | Carry per-task provenance into the aggregate |

## Security and Authority Boundary

Aggregation preserves and reports what subagents returned; it cannot judge whether the content is correct. Validation of merged content — sources, calculations, claims — remains a separate, explicit step.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia's overview of futures and promises (https://en.wikipedia.org/wiki/Futures_and_promises).
2. The Python standard library documentation for concurrent.futures (https://docs.python.org/3/library/concurrent.futures.html).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Parallel Execution](parallel-execution.md) — the dispatch layer that produces the tuples aggregated here.
- [Subagent Spawning](subagent-spawning.md) — spawned subagents whose outputs need this merge discipline.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |

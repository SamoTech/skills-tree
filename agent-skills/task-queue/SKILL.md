---
name: task-queue
description: Manage pending work with declared ordering, visibility timeouts, dead-letter handling, and explicit backpressure.
metadata:
  source: skills/15-orchestration/task-queue.md
  category: 15-orchestration
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-15-orchestration-task-queue.json)

# Task Queue

**Category:** `orchestration`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Manage pending work with declared ordering, visibility timeouts, dead-letter handling, and explicit backpressure. The orchestration step is contract-first: validate state and inputs before acting, and verify the resulting state transition instead of trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | task | object | The queued work item with priority, payload, and deadline |
| Input | queue_policy | object | Ordering key, visibility timeout, and retry/dead-letter rules |
| Output | dequeue_result | object | The next task by policy order, or an explicit empty signal |
| Output | queue_state | object | Depths, in-flight counts, and dead-letter totals |

### Procedure
1. Enqueue each task with its priority, payload, and deadline in one atomic write.
2. Dequeue by the declared ordering key; never cherry-pick outside the policy.
3. Hold dequeued tasks under a visibility timeout so crashes requeue them.
4. Move exhausted tasks to a dead-letter queue instead of retrying forever.
5. Apply backpressure by bounding the queue depth and rejecting overflow explicitly.
6. Report queue depth and dead-letter counts so backlog drift is visible.

### Example

```python
tasks = [{'id': 't1', 'priority': 5}, {'id': 't2', 'priority': 1}, {'id': 't3', 'priority': 3}]
order = sorted(tasks, key=lambda t: t['priority'])
next_task = order[0]
assert next_task['id'] == 't2' and order[-1]['id'] == 't1'
dead_letter = []
attempts = {'t1': 3}
if attempts['t1'] >= 3:
    dead_letter.append('t1')
assert dead_letter == ['t1']
print({'next': next_task['id'], 'dead_lettered': dead_letter})
```

### Related Skills

- [Task Priority Queue Orchestration](task-priority-queue-orchestration.md) - order work by priority across agents
- [Dead Letter Queuing](dead-letter-queuing.md) - isolate poison messages
- [Backpressure Handling](backpressure-handling.md) - bound queues under load

## Failure Modes

- Tasks enqueued without a priority or deadline, breaking ordering guarantees.
- Lost in-flight work after a crash because no visibility timeout was set.
- Poison messages retried forever with no dead-letter path.
- Silent unbounded queue growth instead of explicit backpressure.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing framework's documentation; no benchmark claim is made without reproducible evidence.

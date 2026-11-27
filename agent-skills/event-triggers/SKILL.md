---
name: event-triggers
description: Start workflow actions from explicit events, filters, deduplication rules, and authorization boundaries.
metadata:
  source: skills/15-orchestration/event-triggers.md
  category: 15-orchestration
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-15-orchestration-event-triggers.json)

# Event Triggers

**Category:** `orchestration`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Start workflow actions from explicit events, filters, deduplication rules, and authorization boundaries. The orchestration step is contract-first: validate state and inputs before acting, and verify the resulting state transition instead of trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | event | object | Event with a stable identity, source, and payload schema |
| Input | rules | list of object | Declared filters, deduplication keys, and authorized actions |
| Output | dispatch | object | The action started, its idempotency key, and the matching rule |
| Output | suppressed | list of object | Duplicates or unauthorized events rejected, with reasons |

### Procedure
1. Validate the event's schema and source before acting on its payload.
2. Deduplicate on a declared idempotency key so redelivery cannot re-execute the action.
3. Apply the declared filters; unmatched events are logged, not improvised on.
4. Check the authorization boundary for the action the event would start.
5. Dispatch at most once per idempotency key and record the dispatch identity.
6. Treat delayed, duplicated, or spoofed events as expected failure modes with explicit handling.

### Example

```python
event = {'id': 'evt-881', 'type': 'pr.merged', 'payload': {'pr': 42}}
seen = {'evt-880'}
key = event['id']
if key in seen:
    dispatch, reason = None, 'duplicate'
else:
    seen.add(key); dispatch, reason = {'key': key, 'action': 'deploy-staging'}, 'new'
assert dispatch is not None and reason == 'new' and dispatch['key'] == 'evt-881'
print({'dispatched': dispatch['action'], 'idempotency_key': dispatch['key']})
```

### Related Skills

- [Idempotency Keys](idempotency-keys.md) - exactly-once dispatch
- [Backpressure Handling](backpressure-handling.md) - bound event-driven load
- [Dead Letter Queuing](dead-letter-queuing.md) - park unprocessable events

## Failure Modes

- Duplicate or redelivered events causing repeated execution.
- Acting on events that fail schema or source validation.
- Missing authorization check on the triggered action.
- Filters so broad that unrelated events start workflows.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing framework's documentation; no benchmark claim is made without reproducible evidence.

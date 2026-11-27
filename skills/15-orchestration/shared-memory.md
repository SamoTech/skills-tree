---
title: "Shared Memory"
category: 15-orchestration
level: advanced
stability: stable
version: v2
description: "Coordinate shared workflow state across agents using explicit schemas, ownership, synchronization, and provenance."
added: "2025-03"
related: [state-machine, agent-checkpointing]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-15-orchestration-shared-memory.json)

# Shared Memory

**Category:** `orchestration`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Coordinate shared workflow state across agents using explicit schemas, ownership, synchronization, and provenance. The orchestration step is contract-first: validate state and inputs before acting, and verify the resulting state transition instead of trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | state_schema | object | The shared record types, fields, and allowed transitions |
| Input | ownership | object | Which agent owns each record and who may write it |
| Output | state_update | object | The versioned write with owner, timestamp, and provenance |
| Output | conflict_report | list | Stale or concurrent writes detected, with their resolution |

### Procedure
1. Define the shared record schema and each record's single writer before storing state.
2. Read state with its version; reject reads lacking version and ownership metadata.
3. Write conditionally on the version (compare-and-swap) so stale writers fail loudly.
4. Record every state change with owner, version, and reason for provenance.
5. Resolve conflicts by re-applying the newest state, never by blind overwrite.
6. Expose the current state and its history so any agent can audit the workflow.

### Example

```python
state, version = {'owner': 'planner', 'status': 'running'}, 3
write = {'owner': 'planner', 'status': 'done'}
recorded = {'data': state, 'version': version}
accepted = {'data': write, 'version': version + 1}
assert recorded['version'] == 3 and accepted['version'] == 4
assert accepted['data']['owner'] == recorded['data']['owner']
print({'accepted_version': accepted['version'], 'owner': accepted['data']['owner']})
```

### Related Skills

- [State Machine](state-machine.md) - model state transitions explicitly
- [Agent Checkpointing](../09-agentic-patterns/agent-checkpointing.md) - persist and restore agent progress

## Failure Modes

- Two agents writing the same record without ownership or versioning.
- Stale reads spreading outdated state to downstream steps.
- Unversioned writes that cannot be audited or rolled back.
- Shared state growing into an unbounded context dump.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing framework's documentation; no benchmark claim is made without reproducible evidence.

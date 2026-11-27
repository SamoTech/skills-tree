---
name: agent-handoff
description: Transfer an active task between agents with a complete state snapshot, pending actions, evidence, and acceptance criteria.
metadata:
  source: skills/15-orchestration/agent-handoff.md
  category: 15-orchestration
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-15-orchestration-agent-handoff.json)

# Agent Handoff

**Category:** `orchestration`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Transfer an active task between agents with a complete state snapshot, pending actions, evidence, and acceptance criteria. The orchestration step is contract-first: validate state and inputs before acting, and verify the resulting state transition instead of trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | handoff | object | State snapshot, pending actions, and evidence references |
| Input | acceptance_criteria | list of string | What the receiver must verify to own the task |
| Output | ownership | object | New owner id and the accepted state version |
| Output | unresolved | list of string | Conditions the receiver could not reconstruct |

### Procedure
1. Snapshot the workflow state, pending actions, and evidence before releasing ownership.
2. Validate the receiving agent's authority and capability against the task scope.
3. Transfer atomically: exactly one owner at any state version.
4. Have the receiver reconstruct the state and next action before the handoff completes.
5. Record the acceptance criteria check as the handoff evidence.
6. Apply the declared recovery path when the receiver cannot reconstruct the state.

### Example

```python
snapshot = {'state': 'step-3/5', 'pending': ['run tests'], 'evidence': ['ci-log-88']}
criteria = ['state reconstructable', 'pending listed']
reconstructed = snapshot['state'] == 'step-3/5' and snapshot['pending'] == ['run tests']
ownership = {'owner': 'agent-b', 'state_version': 7}
assert reconstructed and all(criteria) and ownership['owner'] != 'agent-a'
print({'handed_off': True, 'owner': ownership['owner'], 'evidence': snapshot['evidence']})
```

### Related Skills

- [Execution Handoff](execution-handoff.md) - the execution-stage variant
- [Agent Communication](agent-communication.md) - message channels between agents
- [Human-in-Loop](../14-security/human-in-loop.md) - escalate handoffs that need human ownership

## Failure Modes

- Ambiguous ownership or two agents acting on the same state version.
- A handoff the receiver cannot reconstruct (missing state snapshot or pending actions).
- Transferring authority the receiver is not scoped to hold.
- Completion reported without the acceptance-criteria check.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing framework's documentation; no benchmark claim is made without reproducible evidence.

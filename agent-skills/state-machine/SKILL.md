---
name: state-machine
description: Model workflow progress as an explicit finite state machine with declared states, guarded transitions, and auditable history.
metadata:
  source: skills/15-orchestration/state-machine.md
  category: 15-orchestration
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-15-orchestration-state-machine.json)

# State Machine

**Category:** `orchestration`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Model workflow progress as an explicit finite state machine with declared states, guarded transitions, and auditable history. The orchestration step is contract-first: validate state and inputs before acting, and verify the resulting state transition instead of trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | states | list of string | The declared, finite set of workflow states |
| Input | transitions | list of object | Allowed from/to pairs with guard conditions |
| Output | current_state | enum | The state after applying the event, with history |
| Output | transition_log | list | Each applied or rejected transition with its guard result |

### Procedure
1. Declare the finite state set before defining any transition.
2. Define transitions as explicit from/to pairs with guard conditions.
3. Apply one event at a time; reject any transition not declared in the table.
4. Evaluate guards before mutating; log rejected transitions with reasons.
5. Record the transition history so the path to the current state is auditable.
6. Declare terminal states and reject events applied after them.

### Example

```python
states = ['queued', 'running', 'done', 'failed']
transitions = {('queued', 'start'): 'running', ('running', 'ok'): 'done', ('running', 'err'): 'failed'}
state, event = 'queued', 'start'
assert state in states and (state, event) in transitions
state = transitions[(state, event)]
assert state == 'running' and ('running', 'ok') in transitions
print({'state': state, 'terminal_reached': False})
```

### Related Skills

- [Conditional Branching](conditional-branching.md) - route control flow on conditions
- [LangGraph Checkpointing](langgraph-checkpointing.md) - persist graph state between steps
- [Durable Execution Guarantees](durable-execution-guarantees.md) - resume workflows after failures

## Failure Modes

- Implicit states reached by side effects instead of declared transitions.
- Guard conditions evaluated after the state has already changed.
- Missing terminal states letting finished workflows accept events.
- Unbounded state growth that defeats the finite-state contract.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing framework's documentation; no benchmark claim is made without reproducible evidence.

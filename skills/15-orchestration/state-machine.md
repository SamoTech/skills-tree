---
title: "State Machine"
category: 15-orchestration
level: advanced
stability: stable
description: "Apply state machine in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-15-orchestration-state-machine.json)

**Category:** Orchestration
**Skill Level:** Advanced
**Stability:** stable
**Added:** 2025-03

### Description
Models complex agent workflows as explicit finite state machines with defined states, transitions, guards, and actions. Prevents invalid state transitions, enables checkpoint/resume, and makes workflow logic auditable and testable.

### Example
```python
from enum import Enum, auto
from typing import Optional

class State(Enum):
    IDLE = auto()
    RESEARCHING = auto()
    WRITING = auto()
    REVIEWING = auto()
    DONE = auto()
    FAILED = auto()

TRANSITIONS: dict[State, list[State]] = {
    State.IDLE:        [State.RESEARCHING],
    State.RESEARCHING: [State.WRITING, State.FAILED],
    State.WRITING:     [State.REVIEWING, State.FAILED],
    State.REVIEWING:   [State.DONE, State.WRITING],
    State.DONE:        [],
    State.FAILED:      [],
}

class WorkflowStateMachine:
    def __init__(self):
        self.state = State.IDLE
        self.history: list[State] = [State.IDLE]

    def transition(self, new_state: State) -> None:
        allowed = TRANSITIONS[self.state]
        if new_state not in allowed:
            raise ValueError(f"Invalid transition: {self.state} → {new_state}. Allowed: {allowed}")
        self.state = new_state
        self.history.append(new_state)
        print(f"State → {new_state.name}")

wf = WorkflowStateMachine()
wf.transition(State.RESEARCHING)
wf.transition(State.WRITING)
wf.transition(State.REVIEWING)
wf.transition(State.DONE)
print(f"History: {[s.name for s in wf.history]}")
```

### Related Skills
- [Sequential Workflow](sequential-workflow.md)
- [Conditional Branching](conditional-branching.md)
- [Logging and Observability](logging-observability.md)

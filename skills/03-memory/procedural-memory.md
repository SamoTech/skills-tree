---
title: "Procedural Memory"
category: 03-memory
level: intermediate
stability: stable
tags: [memory, procedures, workflows, skills, planning]
description: "Store and recall step-by-step procedures, learned workflows, and repeatable skill patterns so an agent can execute tasks consistently without re-deriving the steps every time."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-03-memory-procedural-memory.json)

# Procedural Memory

**Category:** `memory`  
**Skill Level:** `intermediate`  
**Stability:** `stable`  
**Added:** 2025-03

---

## Description

Procedural memory is the agent's library of *how-to* knowledge. Where semantic memory holds facts ("PostgreSQL uses port 5432") and episodic memory records events ("I ran that migration on Tuesday"), procedural memory encodes sequences of actions — the specific steps required to accomplish a goal reliably.

Storing procedures explicitly has two major benefits. First, it dramatically reduces the prompt reasoning budget: instead of re-deriving the deployment steps from scratch every run, the agent retrieves a validated 10-step sequence and executes it. Second, it enables learning: if a step fails or a better approach is discovered, the procedure can be updated, and every future invocation benefits immediately.

---

## When to Use

- Repeatable operational tasks with a known correct sequence (deploys, incident runbooks, data pipelines)
- Onboarding flows where the agent guides a user through a multi-step process
- Any scenario where the same task appears frequently enough to justify caching the plan
- Cross-session skill transfer: the agent learns a procedure once and can apply it in future sessions

---

## Data Model

```python
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Step:
    index: int
    instruction: str
    tool: Optional[str] = None       # tool name if step calls a tool
    expected_output: Optional[str] = None
    on_failure: Optional[str] = None  # fallback instruction


@dataclass
class Procedure:
    name: str                         # machine-readable key, e.g. "deploy_service"
    description: str                  # human-readable summary
    steps: list[Step]
    version: int = 1
    tags: list[str] = field(default_factory=list)
    last_used: Optional[str] = None
    success_count: int = 0
    failure_count: int = 0
```

---

## Implementation Pattern

```python
import json
from pathlib import Path
from dataclasses import asdict


class ProceduralMemory:
    """Persist and retrieve learned agent procedures."""

    def __init__(self, store_path: str = ".procedures.json"):
        self._path = Path(store_path)
        self._store: dict[str, dict] = self._load()

    def _load(self) -> dict:
        if self._path.exists():
            return json.loads(self._path.read_text(encoding="utf-8"))
        return {}

    def save_procedure(self, proc: Procedure) -> None:
        self._store[proc.name] = asdict(proc)
        self._path.write_text(
            json.dumps(self._store, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def get_procedure(self, name: str) -> Procedure | None:
        raw = self._store.get(name)
        if not raw:
            return None
        raw["steps"] = [Step(**s) for s in raw["steps"]]
        return Procedure(**raw)

    def list_procedures(self, tag: str | None = None) -> list[str]:
        if tag is None:
            return list(self._store.keys())
        return [k for k, v in self._store.items() if tag in v.get("tags", [])]

    def record_outcome(self, name: str, success: bool) -> None:
        if name in self._store:
            key = "success_count" if success else "failure_count"
            self._store[name][key] = self._store[name].get(key, 0) + 1
            self._path.write_text(
                json.dumps(self._store, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
```

### Executing a stored procedure

```python
memory = ProceduralMemory()

def execute(procedure_name: str, agent) -> bool:
    proc = memory.get_procedure(procedure_name)
    if not proc:
        raise ValueError(f"Unknown procedure: {procedure_name}")

    for step in proc.steps:
        print(f"[Step {step.index}] {step.instruction}")
        try:
            if step.tool:
                agent.run_tool(step.tool, step.instruction)
            else:
                agent.act(step.instruction)
        except Exception as exc:
            print(f"Step {step.index} failed: {exc}")
            if step.on_failure:
                agent.act(step.on_failure)
            memory.record_outcome(procedure_name, success=False)
            return False

    memory.record_outcome(procedure_name, success=True)
    return True
```

---

## Learning New Procedures

Procedures can be injected by a human (static definition), derived by the agent from a successful run (retrospective logging), or inferred from user instructions ("whenever you deploy, always run tests first").

For retrospective learning:
1. Log every step the agent takes during task execution
2. After successful completion, prompt the LLM: *"Summarise the steps you just took as a reusable procedure."*
3. Parse the response into a `Procedure` dataclass and persist it

For instruction-based learning:
- Detect imperative patterns in user messages ("always", "whenever you", "make sure to")
- Extract the trigger condition and the action sequence
- Store as a conditional procedure with a named trigger

---

## Pitfalls

- **Rigid procedures break on context change**: A procedure that works for staging may fail in production. Tag procedures with their environment/context and validate before executing.
- **Version drift**: The environment changes but the stored procedure doesn't. Track `version` and add a `last_validated` timestamp; trigger re-validation after N days.
- **Looping on failure**: If a procedure's `on_failure` step also fails, you get an infinite retry loop. Set a maximum retry count per step.
- **Privacy in step instructions**: Procedures may capture credentials or environment-specific paths. Scrub secrets before persisting.

---

## Related Skills

- [Semantic Memory](semantic-memory.md)
- [Procedural (full)](procedural.md)
- [Planning](../02-reasoning/planning.md)
- [Cross-Session Persistence](cross-session-persistence.md)

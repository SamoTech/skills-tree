---
name: prompt-engineering
description: Design, structure, test, and refine prompts so language models receive clear objectives, constraints, context, output contracts, and evaluation criteria.
metadata:
  source: skills/02-reasoning/prompt-engineering.md
  category: 02-reasoning
  version: "v1"
---

# Prompt Engineering

## Description

Prompt Engineering is the disciplined design and refinement of model instructions. A production prompt should make the task objective explicit, constrain important behavior, provide the context the model needs, and define an output contract that downstream code can validate.

## When to Use

- A model must follow a repeatable task contract.
- Output quality depends on explicit context or constraints.
- A workflow needs structured output that can be validated automatically.
- You need to compare prompt variants using a repeatable evaluation set.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `task` | `str` | Objective the model must complete |
| `context` | `str` | Relevant facts, examples, or retrieved material |
| `constraints` | `list[str]` | Explicit behavioral or formatting constraints |
| `output_schema` | `dict` | Expected machine-readable output contract |
| → `prompt` | `str` | Complete model instruction |

## Minimal Runnable Pattern

```python
def build_prompt(task, context, constraints):
    instructions = f"Task: {task}\nContext: {context}"
    return f"{instructions}\nConstraints: {'; '.join(constraints)}"
```

## Core Practices

1. State the objective before implementation details.
2. Separate trusted context from instructions.
3. Make constraints explicit rather than relying on implied behavior.
4. Define structured outputs with a schema when software consumes the result.
5. Use representative evaluation cases before accepting a prompt change.
6. Keep prompts versioned when prompt behavior is part of a production contract.

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Ambiguous output | Objective or schema is underspecified | Add explicit output requirements |
| Instruction conflict | Multiple requirements have unclear precedence | Define precedence and constraints explicitly |
| Prompt regression | Changes are not evaluated consistently | Maintain a deterministic evaluation set |
| Context overload | Too much irrelevant context | Retrieve or summarize only task-relevant context |

## Related Skills

- [Meta-Prompting](meta-prompting.md) — dynamically generates or refines prompts
- [Step-Back Prompting](step-back-prompting.md) — adds abstraction before solving a task
- [Goal Decomposition](goal-decomposition.md) — clarifies objectives before prompt construction
- [ReAct Pattern](../09-agentic-patterns/react.md) — combines reasoning, action, and observation in a tool loop

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Canonical prompt engineering skill source restored as an explicit graph node |
| 2026-09 | v1 | Added production-oriented output contract and evaluation guidance |

## Evidence
The canonical skill file is the authoritative repository implementation. Repository schema, validation workflows, and the Agent Skills projection contract define structural conformance. Implementation guidance must remain traceable to supplied or independently verified authoritative sources; no benchmark claim is made without reproducible evidence.

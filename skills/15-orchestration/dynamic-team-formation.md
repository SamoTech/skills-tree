---
title: "Dynamic Team Formation"
category: 15-orchestration
level: advanced
stability: experimental
description: "Assemble and disband multi-agent teams at run time by matching task requirements against agent capabilities, with explicit role contracts and budget-aware sizing."
added: "2026-10"
version: v1
related: ["subagent-spawning","role-assignment"]
---

# Dynamic Team Formation

Category: Orchestration | Level: advanced | Stability: experimental | Version: v1

## Description

Not every task deserves a team. The skill covers deciding when a single agent suffices, deriving required roles from the task decomposition, selecting agents by declared capability rather than identity, writing per-role contracts with inputs, outputs, and authority limits, and sizing the team against a budget. Teams disband on completion with artifacts returned, because lingering agents are cost and confusion.

## When to Use

Use when a task decomposes into heterogeneous subtasks that benefit from specialists working in parallel or in sequence within one run.

Do not spawn a full team for every task. Larger teams pay communication overhead that simple tasks cannot amortize, and unnecessary agents multiply cost and failure surface.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `task_decomposition` | `table` | Yes | Subtasks with required capabilities and dependencies |
| `agent_registry` | `object` | Yes | Available agents with declared capabilities and cost model |
| `budget` | `object` | No | Cost, concurrency, and time bounds for the whole team |

## Procedure

1. Decide whether the task needs a team at all: single-agent unless decomposition shows real heterogeneity.
2. Derive required roles from the subtasks, one role per distinct capability cluster.
3. Select agents by declared capability fit, recording the second choice for each role.
4. Write per-role contracts: inputs, outputs, authority limits, and escalation path.
5. Size the team against the budget, trading concurrency against cost per unit of work.
6. Disband on completion, returning artifacts and freeing capacity explicitly.

## Outputs

| Output | Type | Description |
|---|---|---|
| `team_plan` | `table` | Roles, assigned agents, and the capability evidence for each match |
| `role_contracts` | `array` | Per-role input, output, authority, and escalation terms |
| `formation_record` | `object` | Sizing rationale, budget usage, and disband event |

## Runnable Example

```python
def select_agents(subtasks, registry):
    """subtasks: [(subtask, capability)]; registry: {agent: [capabilities]}"""
    plan = {}
    for subtask, cap in subtasks:
        candidates = sorted(a for a, caps in registry.items() if cap in caps)
        plan[subtask] = candidates[0] if candidates else None
    return plan

print(select_agents(
    [("extract-tables", "vision"), ("write-summary", "writing"), ("cite-check", "search")],
    {"agent-a": ["vision"], "agent-b": ["writing", "search"], "agent-c": ["search"]},
))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Team bloat | Agents added for symmetry rather than need | Size from the decomposition, not a fixed template |
| Capability mismatch | Agents selected by name or affinity | Select on declared capabilities and record evidence |
| Orphaned subtasks | No agent holds a required capability | Fail formation or split the subtask; never silently drop |
| Lingering agents | Team never disbanded after completion | Make disband an explicit step with artifact handoff |
| Contract ambiguity | Roles overlap or authority undefined | Per-role contracts before any work starts |

## Security and Authority Boundary

Dynamically formed teams can expand the blast radius of a compromised member. Scope each agent to the minimum authorities its role contract needs, audit capability declarations in the registry, and never allow formation logic to grant authority it cannot revoke.

## Evidence

This skill is grounded in dated public implementation references:

1. The LangGraph multi-agent orchestration framework (https://github.com/langchain-ai/langgraph).
2. The AutoGen multi-agent conversation framework (https://github.com/microsoft/autogen).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Subagent Spawning](subagent-spawning.md) — the lifecycle primitive a formed team is built from.
- [Role Assignment](role-assignment.md) — the role taxonomy formation selects against.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |

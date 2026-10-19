---
title: "Workflow Dataflow Dependency Analysis"
category: 15-orchestration
level: advanced
stability: experimental
description: "Analyze a workflow as a dataflow graph so that ordering follows actual data dependencies instead of assumed sequence."
added: "2026-10"
version: v1
related: [action-dependency-resolution, workflow-versioning]
tags: [dataflow, dependencies, workflows, analysis]
---
# Workflow Dataflow Dependency Analysis

## Description
Analyze a workflow as a dataflow graph so that ordering follows actual data dependencies instead of assumed sequence. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A workflow under-performs or races because step order was guessed rather than derived.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Extract the read and write sets of every step, build the dependency graph from actual data flow, and reorder steps only where the graph proves independence before execution.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def independent(steps):
    edges = []
    for a in steps:
        for b in steps:
            if a is b:
                continue
            if a["writes"] & b["reads"]:
                edges.append((a["id"], b["id"]))
    return edges
s = [{"id": "a", "writes": {"x"}, "reads": set()},
     {"id": "b", "writes": set(), "reads": {"x"}}]
assert independent(s) == [("a", "b")]
```

## Failure Modes
- The graph is built from step order and justifies the existing sequence instead of testing it..
- Hidden shared state via a cache is missed and two steps race on one key..
- Read-write sets are extracted once and never refreshed after step changes..
- Reordering proceeds on unproven independence and corrupts downstream state..
- External side effects are modeled as pure writes and their ordering constraints are dropped..

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 agent execution guidance covers deriving execution order from recorded data flow for acting agents (futransolutions.com, dated October 2026) ([public signal](https://futransolutions.com/blog/ai-agent-observability-in-2026-how-to-trace-evaluate-and-debug-ai-that-takes-action/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Action Dependency Resolution](../04-action-execution/action-dependency-resolution.md)
- [Workflow Versioning](../15-orchestration/workflow-versioning.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

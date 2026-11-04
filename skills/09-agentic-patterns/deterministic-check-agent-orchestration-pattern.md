---
title: "Deterministic Check Agent Orchestration Pattern"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Orchestrate an agent team where deterministic tool checks gate what agents may do next, so every agent step is preceded by a verifiable check result."
added: "2026-11"
version: v1
related: [multi-step-planning]
tags: [agentic-patterns, determinism, gating, orchestration]
---
# Deterministic Check Agent Orchestration Pattern

## Description
Orchestrate an agent team where deterministic tool checks gate what agents may do next, so every agent step is preceded by a verifiable check result. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A multi-agent workflow must guarantee each step's precondition was machine-checked, not assumed.
- The outcome would change if an agent proceeded on an assumption the deterministic check had refuted.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The workflow graph, the deterministic checker contracts, and the agent role boundaries. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Bind every agent step to a deterministic precondition check that must pass before the step runs.
4. Route check failures to a bounded retry or human path, never letting the agent restate the precondition.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | An orchestration record with per-step check results and the gate decisions they produced. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def run_gated(graph, checks):
    done = []
    for step in graph:
        gate = checks[step["check"]]
        if not gate():
            return {"status": "blocked", "at": step["name"], "done": done}
        done.append(step["name"])
    return {"status": "completed", "done": done}
g = [{"name": "build", "check": "clean"}, {"name": "deploy", "check": "tests_pass"}]
assert run_gated(g, {"clean": lambda: True, "tests_pass": lambda: False})["status"] == "blocked"
assert run_gated(g, {"clean": lambda: True, "tests_pass": lambda: True})["status"] == "completed"
```

## Failure Modes
- An agent rewrites the precondition narrative instead of running the check.
- Check failures are retried until they pass instead of routing to a bounded path.
- A check is marked deterministic although it calls a model.
- Steps with no bound check run by default.
- Check results are not recorded, so gating cannot be audited.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- AWS published a planner-specialist blueprint where agents work with deterministic tools in a workflow and every plan step must pass a check before execution (AI Agent News Today, dated November 3, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Multi-Step Planning](../02-reasoning/multi-step-planning.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |

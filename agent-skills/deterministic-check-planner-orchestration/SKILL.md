---
name: deterministic-check-planner-orchestration
description: Build a plan graph where every plan step carries a deterministic check id, and the orchestrator refuses to schedule steps whose checks have not been computed.
metadata:
  source: skills/15-orchestration/deterministic-check-planner-orchestration.md
  category: 15-orchestration
  version: "v1"
---

# Deterministic Check Planner Orchestration

## Description
Build a plan graph where every plan step carries a deterministic check id, and the orchestrator refuses to schedule steps whose checks have not been computed. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A plan must be executable only after each step's success condition is machine-checkable.
- The outcome would change if steps executed whose success condition was never defined.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The plan draft, the check registry, and the scheduler contract. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Attach a check id from the registry to every plan step before scheduling.
4. Refuse to schedule steps with missing or unregistered checks and report them as blocked.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A schedulable plan graph with per-step check ids and a blocked list for unchecked steps. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def schedule(plan, registry):
    ready, blocked = [], []
    for step in plan:
        if step.get("check") in registry:
            ready.append(step)
        else:
            blocked.append(step["name"])
    return {"ready": ready, "blocked": blocked}
r = schedule([{"name": "build", "check": "c1"}, {"name": "deploy", "check": "c9"}], {"c1"})
assert [s["name"] for s in r["ready"]] == ["build"] and r["blocked"] == ["deploy"]
```

## Failure Modes
- Steps without checks are scheduled anyway with success judged by the agent.
- Check ids reference checks that were never implemented in the registry.
- The blocked list is dropped, so unchecked steps vanish silently.
- Checks are reordered after scheduling, decoupling them from their steps.
- A step is rescheduled repeatedly after its check keeps failing, without escalation.

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

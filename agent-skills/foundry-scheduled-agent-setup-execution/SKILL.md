---
name: foundry-scheduled-agent-setup-execution
description: Configure scheduled agents in an agent platform with recorded schedules, scopes, and failure routing before first run.
metadata:
  source: skills/04-action-execution/foundry-scheduled-agent-setup-execution.md
  category: 04-action-execution
  version: "v1"
---

# Foundry Scheduled Agent Setup Execution

## Description
Configure scheduled agents in an agent platform with recorded schedules, scopes, and failure routing before first run. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent must provision a scheduled agent with an explicit schedule and a bounded permission scope.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Register the agent with its cron schedule, its least-privilege scope, and a failure route, and record the resulting configuration id for audit before the first run.
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
def register_scheduled_agent(name, cron, scope, failure_route):
    if "*" in scope:
        raise ValueError("scope must be least-privilege")
    return {"name": name, "cron": cron, "scope": scope, "on_failure": failure_route, "id": name + "-sched"}
cfg = register_scheduled_agent("nightly-report", "0 3 * * *", ["reports:read"], "queue:ops")
assert cfg["id"] == "nightly-report-sched" and cfg["on_failure"] == "queue:ops"
```

## Failure Modes
- The schedule is registered with a wildcard scope and the agent exceeds its task boundary on first run.
- Failure routing is omitted and failed runs disappear silently until an owner notices.
- The cron expression is never validated and the agent runs at an unintended time.
- The configuration id is not recorded and later audits cannot map runs to a registered scope.
- The first run happens before the scope review and unreviewed automation executes with standing access.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The October 2026 Microsoft Foundry update that introduces scheduled AI agents is the dated capability signal for this setup procedure. ([public signal](https://visualstudiomagazine.com/articles/2026/10/19/microsoft-foundry-update-brings-scheduled-ai-agents-smarter-tool-use-and-gpt-6-models.aspx))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Scheduled Execution](../04-action-execution/scheduled-execution.md)
- [Foundry Agent Lifecycle Orchestration](../15-orchestration/foundry-agent-lifecycle-orchestration.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

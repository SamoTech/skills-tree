---
title: "Unattended Coding Agent Supervision Orchestration"
category: 15-orchestration
level: advanced
stability: experimental
description: "Orchestrate supervision of unattended coding agents with attempt budgets, periodic checkpoints, and stop conditions that hand control back to a human."
added: "2026-11"
version: v1
related: [retry-backoff, consensus-voting]
tags: [orchestration, supervision, coding-agents]
---

# Unattended Coding Agent Supervision Orchestration

## Description
Orchestrate supervision of unattended coding agents with attempt budgets, periodic checkpoints, and stop conditions that hand control back to a human. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A coding agent runs unattended on a task list.
- Attempt budgets and checkpoints must be enforced.
- A stop must hand control back to a human.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The task list, the attempt budget, and the checkpoint review contract. |
| Outputs | A supervision log naming per-task attempts, checkpoint outcomes, and stop decisions. |
| Safety | Fail closed by stopping the run when the attempt budget or checkpoint contract is exceeded. |

## Procedure
1. Split the workload into tasks with attempt budgets.
2. Define checkpoint reviews between task groups.
3. Run tasks and record attempts and outcomes.
4. Review checkpoints against the contract.
5. Stop or continue per the stop conditions.
6. Emit the supervision log with handoff state.

## Outputs
| Area | Contract |
|---|---|
| Primary | A supervision log naming per-task attempts, checkpoint outcomes, and stop decisions. |
| Verification | The recorded inputs and intermediate values that reproduce the primary output from the runnable example. |
| Failure | A fail-closed hold naming the unmet precondition and the withheld primary output. |

## Runnable Example
```python
def supervision(tasks, budget):
    log = []
    for t in tasks:
        stop = t["attempts"] >= budget
        log.append({"task": t["name"], "attempts": t["attempts"], "decision": "stop" if stop else "checkpoint"})
    return log

r = supervision([{"name": "fix", "attempts": 3}], 3)
assert r[0]["decision"] == "stop"
assert supervision([{"name": "fix", "attempts": 1}], 3)[0]["decision"] == "checkpoint"
```

## Failure Modes
- Attempt budgets are set after the run has looped..
- Checkpoints are scheduled but not reviewed..
- Stop conditions end the task instead of the run..
- The handoff state is undocumented..
- Supervision logs record successes only..

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Harness Leaderboard v0.1.1 scores reliability when a coding agent is left unattended, comparing nine harnesses on three-attempt reliability bars (ExplainX, November 7, 2026) ([public signal](https://www.explainx.ai/news))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Retry Backoff](retry-backoff.md)
- [Consensus Voting](consensus-voting.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |

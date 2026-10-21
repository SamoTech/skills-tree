---
title: "Agent Incident Response Runbook Orchestration"
category: 15-orchestration
level: advanced
stability: experimental
description: "Orchestrate AI agent incident response through runbooks so detection, containment, and recovery steps execute in recorded order."
added: "2026-10"
version: v1
related: [runbook-driven-orchestration, agent-incident-command]
tags: [incident-response, runbooks, orchestration, security]
---
# Agent Incident Response Runbook Orchestration

## Description
Orchestrate AI agent incident response through runbooks so detection, containment, and recovery steps execute in recorded order. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A security operations team responds to AI agent control incidents and must execute a defined runbook.
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
3. Load the incident runbook for the incident class, execute detection, containment, and recovery phases in declared order with per-step evidence, and abort on the first phase whose verification fails.
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
def execute(runbook):
    done = []
    for step in runbook:
        if not step["verify"]:
            raise RuntimeError("phase failed: " + step["name"])
        done.append(step["name"])
    return done
rb = [{"name": "detect", "verify": True}, {"name": "contain", "verify": True}]
assert execute(rb) == ["detect", "contain"]
```

## Failure Modes
- Phases execute out of order and containment precedes evidence capture.
- A failed phase is skipped instead of aborting the runbook.
- Runbook steps have no verification and report completion by default.
- Incident class is guessed and the wrong runbook executes.
- Executions are not recorded and post-incident reviews reconstruct by memory.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- NIST, NSA and CISA published AI agent control incident response guidance (windowsforum.com, dated October 16, 2026) ([public signal](https://windowsforum.com/news/nist-nsa-and-cisa-publish-ai-agent-control-incident-response-guidance.448667/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Runbook Driven Orchestration](../15-orchestration/runbook-driven-orchestration.md)
- [Agent Incident Command](../15-orchestration/agent-incident-command.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

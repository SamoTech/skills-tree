---
title: "On Device Agent Task Orchestration"
category: 15-orchestration
level: advanced
stability: experimental
description: "Orchestrate on-device agent tasks so that local execution respects device budgets and falls back deliberately."
added: "2026-10"
version: v1
related: [on-device-agent-fallback-pattern, appfunctions-mcp-tool-implementation]
tags: [on-device, orchestration, agents, routing]
---
# On Device Agent Task Orchestration

## Description
Orchestrate on-device agent tasks so that local execution respects device budgets and falls back deliberately. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A system routes tasks between cloud and an on-device agent runtime and must orchestrate the split honestly.
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
3. Classify tasks by latency and privacy needs, bind on-device tasks to the local runtime with its measured limits, and route fallbacks to the cloud only with an explicit disclosure.
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
def classify(task):
    if task["latency_ms"] <= 200:
        return "device"
    if task["private"]:
        return "device"
    return "cloud"
assert classify({"latency_ms": 100, "private": False}) == "device"
assert classify({"latency_ms": 900, "private": False}) == "cloud"
assert classify({"latency_ms": 900, "private": True}) == "device"
```

## Failure Modes
- A privacy-sensitive task is routed to the cloud without disclosure.
- On-device limits are copied from marketing and not measured on target hardware.
- Fallback loops between device and cloud and never terminates.
- Battery and thermal budgets are ignored in routing decisions.
- The local runtime is assumed offline-safe and network calls leak in.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the Android Dev Summit launched the Gemini Nano 4-powered Agentic API for local on-device task orchestration (blog.luandnh.com, dated October 29, 2026) ([public signal](https://blog.luandnh.com/en/ai-daily/2026-10-29/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [On Device Agent Fallback Pattern](on-device-agent-fallback-pattern.md)
- [Appfunctions Mcp Tool Implementation](../05-code/appfunctions-mcp-tool-implementation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

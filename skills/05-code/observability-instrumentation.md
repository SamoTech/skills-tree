---
title: "Observability Instrumentation"
category: 05-code
level: basic
stability: experimental
description: "Add tracing, metrics, and structured logs to code with explicit spans, correlation identifiers, and bounded cardinality, so agent and service behavior can be measured in production."
added: "2026-10"
version: v1
related: [structured-logging, performance-profiling, logging-observability]
tags: [observability, instrumentation, code]
---

# Observability Instrumentation

## Description
Add tracing, metrics, and structured logs to code with explicit spans, correlation identifiers, and bounded cardinality, so agent and service behavior can be measured in production. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- The task has explicit constraints such as time, budget, or safety that must gate the outcome.
- A silent failure mode exists that must be surfaced rather than swallowed.
- Verification evidence is required before the result is trusted.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for observability instrumentation. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the observability instrumentation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# Observability Instrumentation: deterministic check
allowed = {"idle": {"running"}, "running": {"done", "failed"}, "failed": {"idle"}}

def transition(state, nxt):
    return nxt in allowed.get(state, set())

assert transition("idle", "running")
assert not transition("idle", "done")
print("transitions checked")
```

## Failure Modes
- Acting outside the declared task boundary.
- Assuming an estimate or preview equals the verified effect.
- Retrying without preserving state or evidence.
- Using stale inputs as if they were current.
- Reporting success without checking the resulting state.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Agent observability is a named 2026 production requirement; OpenTelemetry-style instrumentation is published across agent stacks. These are dated public signals, not adoption metrics.

## Related
- structured-logging.md
- performance-profiling.md
- logging-observability.md

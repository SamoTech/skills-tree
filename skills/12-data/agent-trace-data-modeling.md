---
title: "Agent Trace Data Modeling"
category: 12-data
level: advanced
stability: experimental
description: "Model agent runs, spans, tool calls, and token events into a queryable trace schema aligned with GenAI semantic conventions."
added: "2026-10"
version: v1
related: [observability-instrumentation, log-parsing, time-series-reading]
tags: [agent, trace, data, modeling]
---
# Agent Trace Data Modeling

## Description
Model agent runs, spans, tool calls, and token events into a queryable trace schema aligned with GenAI semantic conventions. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires agent trace data modeling before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for agent trace data modeling. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent trace data modeling steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def span(run_id, name, ms):
    return {"run": run_id, "name": name, "duration_ms": ms}
def total(spans):
    return sum(s["duration_ms"] for s in spans)
assert total([span("r", "llm", 10), span("r", "tool", 5)]) == 15
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
Agent observability in 2026 converges on OTel GenAI semantic conventions for traces. These are dated public signals, not adoption metrics.

## Related
- observability-instrumentation.md
- log-parsing.md
- time-series-reading.md

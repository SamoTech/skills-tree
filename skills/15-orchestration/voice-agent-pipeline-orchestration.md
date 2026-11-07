---
title: "Voice Agent Pipeline Orchestration"
category: 15-orchestration
level: advanced
stability: experimental
description: "Orchestrate voice agent pipelines by chaining transcription, reasoning, tool calls, and synthesis stages with per-stage latency budgets."
added: "2026-11"
version: v1
related: [voice-agent-sdk-action-wiring, agent-tool-tracing-adoption]
tags: [voice, pipelines, orchestration]
---

# Voice Agent Pipeline Orchestration

## Description
Orchestrate voice agent pipelines by chaining transcription, reasoning, tool calls, and synthesis stages with per-stage latency budgets. Orchestration is bounded by declared stage contracts and latency budgets rather than an end-to-end black box.

## When to Use
- A voice agent chains multiple stages from audio in to audio out.
- Per-stage latency budgets must be declared and measured.
- Stage failures must fail forward with recorded state, not hang.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The stage list with contracts, the latency budgets, and the failure policy. |
| Outputs | An orchestrated pipeline run with per-stage outcomes and measured latencies. |
| Safety | Fail closed by aborting the turn when any stage exceeds its budget without a recorded fallback. |

## Procedure
1. Declare each pipeline stage with its input and output contract.
2. Assign a latency budget per stage for the end-to-end budget to hold.
3. Run each stage and measure its latency against its budget.
4. Apply the failure policy: fallback, retry once, or abort the turn.
5. Record per-stage outcomes with latency and contract checks.
6. Emit the turn result with the stage trace and end-to-end latency.

## Outputs
| Area | Contract |
|---|---|
| Primary | A pipeline run with per-stage outcomes, latencies, and contract checks. |
| Verification | The stage contracts that reproduce the orchestration. |
| Failure | An aborted turn with the budget overrun and fallback state. |

## Runnable Example
```python
def run_turn(stages, budgets, inputs):
    trace = []
    for stage in stages:
        out = stage(inputs)
        if out["latency"] > budgets[stage.__name__]:
            trace.append({"stage": stage.__name__, "overrun": True})
            return {"ok": False, "aborted": stage.__name__, "trace": trace}
        inputs = out["data"]
        trace.append({"stage": stage.__name__, "latency": out["latency"], "overrun": False})
    return {"ok": True, "trace": trace}

def stt(d): return {"data": "text", "latency": 80}
def think(d): return {"data": "reply", "latency": 900}
assert run_turn([stt, think], {"stt": 200, "think": 500}, "audio")["ok"] is False
assert run_turn([stt], {"stt": 200}, "audio")["ok"] is True
```

## Failure Modes
- End-to-end latency is measured without per-stage budgets.
- Stage contracts are implicit, so stages pass untyped data.
- Overrunning stages are retried indefinitely, stalling the turn.
- Stage failures hang instead of applying the declared policy.
- The stage trace is discarded, making latency regressions unattributable.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Mistral released Voxtral 3 speech models together with a voice agent SDK for building voice agent pipelines (AIBriefs, November 7, 2026) ([public signal](https://aibriefs.news/ai-news-today))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Voice Agent Sdk Action Wiring](voice-agent-sdk-action-wiring.md)
- [Agent Tool Tracing Adoption](agent-tool-tracing-adoption.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |

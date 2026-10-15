---
name: realtime-speech-to-speech-agent-loop
description: Assemble a realtime speech-to-speech loop with barge-in, partial-turn handling, and latency budget enforcement.
metadata:
  source: skills/08-multimodal/realtime-speech-to-speech-agent-loop.md
  category: 08-multimodal
  version: "v1"
---

# Realtime Speech To Speech Agent Loop

## Description
Assemble a realtime speech-to-speech loop with barge-in, partial-turn handling, and latency budget enforcement. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires realtime speech to speech agent loop before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for realtime speech to speech agent loop. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the realtime speech to speech agent loop steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def within_budget(asr_ms, llm_ms, tts_ms, budget_ms):
    return asr_ms + llm_ms + tts_ms <= budget_ms
assert within_budget(100, 200, 150, 500) is True
assert within_budget(200, 200, 200, 500) is False
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
Realtime voice agents are a top 2026 multimodal request with explicit latency and barge-in requirements. These are dated public signals, not adoption metrics.

## Related
- text-to-speech.md
- streaming-asr-partial-parsing.md
- voice-activity-detection.md

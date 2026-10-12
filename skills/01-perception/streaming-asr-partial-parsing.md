---
title: "Streaming ASR Partial Parsing"
category: 01-perception
level: intermediate
stability: experimental
description: "Consume partial and final results from streaming automatic speech recognition with stable hypothesis handling, endpointing signals, and monotonic ordering rather than treating every partial transcript as final."
added: "2026-10"
version: v1
related: [audio-transcription, sensor-reading, conversation-history-reading]
tags: [streaming, asr, partial, parsing, perception]
---
# Streaming ASR Partial Parsing

## Description
Consume partial and final results from streaming automatic speech recognition with stable hypothesis handling, endpointing signals, and monotonic ordering rather than treating every partial transcript as final. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires streaming asr partial parsing before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for streaming asr partial parsing. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the streaming asr partial parsing procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Streaming ASR Partial Parsing: deterministic check
candidates = [{"id": "a", "score": 0.8, "cost": 2}, {"id": "b", "score": 0.95, "cost": 9}]
eligible = [c for c in candidates if c["score"] >= 0.8]
selected = min(eligible, key=lambda c: c["cost"])
assert selected["id"] == "a"
print("selected:", selected["id"])
```

## Failure Modes
- Proceeding with streaming asr partial parsing without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Voice-agent work in 2026 targets streaming ASR pipelines and interruption handling; public framework issues request explicit partial-hypothesis handling. These are dated public signals, not adoption metrics.

## Related
- audio-transcription.md
- sensor-reading.md
- conversation-history-reading.md

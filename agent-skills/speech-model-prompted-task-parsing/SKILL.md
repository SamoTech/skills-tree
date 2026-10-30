---
name: speech-model-prompted-task-parsing
description: Parse task-conditioned speech model outputs so that agents separate transcription, translation, and diarization fields from a single response.
metadata:
  source: skills/01-perception/speech-model-prompted-task-parsing.md
  category: 01-perception
  version: "v1"
---

# Speech Model Prompted Task Parsing

## Description
Parse task-conditioned speech model outputs so that agents separate transcription, translation, and diarization fields from a single response. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent drives a prompt-conditioned speech model that returns several task outputs in one record and must split them correctly.
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
3. Validate the response envelope, split each task field into its own typed record, and check every field against its declared schema before dispatch.
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
def split(resp):
    out = {"transcript": resp["transcript"], "translation": resp.get("translation"),
           "speakers": list(resp.get("speakers", []))}
    assert out["transcript"], "empty transcript"
    return out
r = split({"transcript": "hello", "translation": "bonjour", "speakers": ["A"]})
assert r == {"transcript": "hello", "translation": "bonjour", "speakers": ["A"]}
```

## Failure Modes
- A missing translation field is silently substituted with the transcript.
- Speaker labels are propagated without checking they index into the transcript segments.
- Task fields are dispatched as one opaque blob and downstream parsers guess the layout.
- A model response with an unknown task key fails open and floods consumers.
- Diarization offsets are accepted without checking monotonic order.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the Nvidia Nemotron 3.5 Transcribe release processes speech via textual prompts and unifies transcription, translation, and diarization (blog.luandnh.com, dated October 29, 2026) ([public signal](https://blog.luandnh.com/en/ai-daily/2026-10-29/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Streaming Transcription Output Parsing](streaming-transcription-output-parsing.md)
- [Audio Diarization](../08-multimodal/audio-diarization.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

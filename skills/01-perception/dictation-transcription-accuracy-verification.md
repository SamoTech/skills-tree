---
title: "Dictation Transcription Accuracy Verification"
category: 01-perception
level: advanced
stability: experimental
description: "Measure local dictation transcription accuracy against known reference phrases before trusting dictated text for real entry or command use."
added: "2026-11"
version: v1
related: [local-voice-dictation-pipeline, dictation-output-paste-targeting]
tags: [dictation, accuracy-verification, benchmarking, perception]
---
# Dictation Transcription Accuracy Verification

## Description
Measure local dictation transcription accuracy against known reference phrases before trusting dictated text for real entry or command use. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A local dictation engine is about to be used for tasks where misheard words change the outcome, and no accuracy baseline exists.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the local transcription engine, a fixed set of reference phrases, and the accuracy threshold the workflow requires. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Fix a reference phrase set that covers the vocabulary the workflow will actually use.
2. Transcribe each reference phrase with the production engine settings.
3. Score word-level differences between transcription and reference for every phrase.
4. Compare the aggregate accuracy against the declared threshold and record the margin.
5. On a threshold miss, block adoption and report the weakest phrases with their scores.
6. Emit a structured result with the per-phrase scores, the threshold, and the decision.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def score_transcriptions(engine, refs, threshold):
    rows = []
    for ref in refs:
        got = engine["transcribe"](ref)
        wrong = sum(1 for a, b in zip(ref.split(), got.split()) if a != b)
        rows.append({"ref": ref, "wrong": wrong})
    worst = max(r["wrong"] for r in rows)
    return {"adopt": worst <= threshold, "worst": worst}
eng = {"transcribe": lambda s: s}
assert score_transcriptions(eng, ["book a table", "cancel my booking"], 0)["adopt"] is True
eng2 = {"transcribe": lambda s: s.replace("table", "tables")}
assert score_transcriptions(eng2, ["book a table"], 0)["adopt"] is False
```

## Failure Modes
- Accuracy is claimed from vendor marketing instead of measured against a fixed reference set.
- The reference set does not cover domain vocabulary, so the score is unrepresentative.
- A threshold miss is waived verbally and the engine is adopted anyway.
- Engine or model updates are not re-scored against the same reference set.
- Per-phrase scores are discarded and only the aggregate is reported.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Hex 3.0 from Anomaly starting fresh with local transcription that must be verified before dictation workflows rely on it (Munder Difflin agent-tools daily, dated November 1, 2026) ([public signal](https://munderdiffl.in/blog/agent-tools-today-2026-11-01/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Local Voice Dictation Pipeline](local-voice-dictation-pipeline.md)
- [Dictation Output Paste Targeting](dictation-output-paste-targeting.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |

---
title: "On Device Dictation Perception"
category: 01-perception
level: advanced
stability: experimental
description: "Perceive spoken input through local on-device dictation that transcribes on the machine and pastes the text so no audio leaves the device."
added: "2026-11"
version: v1
related: [privacy-sensitive-snapshot-perception, animation-fidelity-diff-perception]
tags: [agents, voice, dictation, privacy]
---

# On Device Dictation Perception

## Description
Perceive spoken input through local on-device dictation that transcribes on the machine and pastes the text so no audio leaves the device. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A voice-driven agent must accept spoken input without sending audio or transcripts to a cloud service.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the dictation engine, the target input fields, and the declared platform support and fallback path. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Declare which surfaces receive dictated text, the local transcription engine boundary, and the platform support state per operating system.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Bind the dictation output to the target fields with paste semantics and verify the text arrives verbatim.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On an unsupported or beta platform, route to the declared fallback input path, and never send audio to a cloud service to complete the task.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def perceive_dictation(event, engine_local, target):
    if not engine_local:
        return {"accepted": False, "reason": "engine is not local"}
    pasted = target.send(event["text"])
    return {"accepted": pasted == event["text"], "verbatim": pasted}
r = perceive_dictation({"text": "hello"}, True, {"send": lambda t: t})
assert r["accepted"] is True and r["verbatim"] == "hello"
```

## Failure Modes
- Audio or transcripts are routed to a cloud service without the user being told.
- A beta platform is treated as stable so dictation silently fails in production.
- Transcribed text is pasted into a different field than the active one without verification.
- The pasted text is assumed verbatim and never compared with the engine output.
- The fallback input path is undeclared so an unsupported platform has no route forward.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Hex 3.0 and 3.1 local voice dictation from Anomaly that transcribes on your machine and pastes the text, with Windows and Linux still labeled beta (Munder Difflin agent-tools daily brief, dated November 1, 2026) ([public signal](https://munderdiffl.in/blog/agent-tools-today-2026-11-01/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Privacy Sensitive Snapshot Perception](privacy-sensitive-snapshot-perception.md)
- [Animation Fidelity Diff Perception](animation-fidelity-diff-perception.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |

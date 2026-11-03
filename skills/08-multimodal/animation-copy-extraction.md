---
title: "Animation Copy Extraction"
category: 08-multimodal
level: advanced
stability: experimental
description: "Extract the text copy displayed in a recorded animation so the rebuilt version reproduces the exact wording instead of approximating it."
added: "2026-11"
version: v1
related: [machine-teardown-visual-simulation, animation-diff-numeric-comparison]
tags: [copy-extraction, animation, transcription, multimodal]
---
# Animation Copy Extraction

## Description
Extract the text copy displayed in a recorded animation so the rebuilt version reproduces the exact wording instead of approximating it. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An animation rebuild must carry the original wording and transcription drift has already changed meaning between versions.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the source recording, the frame region of interest, and the transcription vocabulary. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Identify the frames where text is fully rendered and not mid-transition.
2. Extract the text from each identified frame region and record frame indices as evidence.
3. Deduplicate across frames and order the copy by first appearance.
4. Verify each extracted string against the declared vocabulary and flag unknown tokens.
5. On ambiguous extraction, fail closed and mark the copy as unverified rather than guessing.
6. Emit a structured result with the ordered copy, frame evidence, and verification flags.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def extract_copy(frames):
    lines, seen = [], set()
    for idx, text in frames:
        if text in seen:
            continue
        seen.add(text)
        lines.append({"frame": idx, "text": text})
    return {"copy": lines}
fr = [(3, "Welcome back"), (7, "Welcome back"), (9, "Your table is ready")]
c = extract_copy(fr)
assert [x["text"] for x in c["copy"]] == ["Welcome back", "Your table is ready"]
assert c["copy"][0]["frame"] == 3
```

## Failure Modes
- Mid-transition frames are transcribed and blurred text becomes the canonical copy.
- Duplicate strings across frames are kept and the copy loop repeats.
- Unknown tokens are silently corrected into plausible words.
- Frame indices are dropped, so no one can re-verify where each string came from.
- Ambiguous extractions are shipped as final copy without an unverified flag.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the reanimate skill recording the copy alongside the rebuilt animation so wording matches the original recording (Munder Difflin agent-tools daily, dated November 1, 2026) ([public signal](https://munderdiffl.in/blog/agent-tools-today-2026-11-01/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Machine Teardown Visual Simulation](machine-teardown-visual-simulation.md)
- [Animation Diff Numeric Comparison](animation-diff-numeric-comparison.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |

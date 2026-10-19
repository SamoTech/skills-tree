---
name: audio-watermark-embedding
description: Embed provenance watermarks into generated speech so that synthetic audio stays traceable without degrading the audible signal.
metadata:
  source: skills/08-multimodal/audio-watermark-embedding.md
  category: 08-multimodal
  version: "v1"
---
# Audio Watermark Embedding

## Description
Embed provenance watermarks into generated speech so that synthetic audio stays traceable without degrading the audible signal. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Generated voice output must carry a detectable provenance mark before release.
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
3. Encode the provenance payload, embed it at the declared signal parameters, and verify round-trip detection on the encoded output before release, recording the detection digest.
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
def embed(samples, payload_bits):
    out = list(samples)
    for i, bit in enumerate(payload_bits):
        out[i] = out[i] + (1 if bit == "1" else -1) * 0.001
    return out
assert embed([0.5, 0.5], "11")[0] > 0.5
```

## Failure Modes
- The watermark is embedded at parameters that do not survive the target codec and is undetectable after encoding..
- Embedding pushes the signal past clipping thresholds and degrades audible quality..
- The payload has no version field, so detector updates cannot read older marks..
- Detection is verified on the studio master but not on the delivered compressed artifact..
- The watermark key is committed beside the embedding code, letting anyone strip the mark..

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 voice-agent regulation reporting increases provenance requirements for synthetic audio (aiagentstore.ai weekly news, dated October 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Audio Mixing](../08-multimodal/audio-mixing.md)
- [Watermark Detection](../08-multimodal/watermark-detection.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

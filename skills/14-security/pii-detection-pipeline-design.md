---
title: "Pii Detection Pipeline Design"
category: 14-security
level: advanced
stability: experimental
description: "Design PII detection and redaction pipelines with entity types, confidence thresholds, and audit trails."
added: "2026-10"
version: v1
related: [memory-redaction, redacted-content-detection, security-scanning]
tags: [pii, detection, pipeline, design]
---
# Pii Detection Pipeline Design

## Description
Design PII detection and redaction pipelines with entity types, confidence thresholds, and audit trails. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires pii detection pipeline design before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for pii detection pipeline design. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the pii detection pipeline design steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def redact(text, entities):
    for e in entities:
        text = text.replace(e, "[REDACTED]")
    return text
assert redact("call 555-0100", ["555-0100"]) == "call [REDACTED]"
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
PII detection tooling such as Microsoft Presidio is cited in 2026 AI security developer guides. These are dated public signals, not adoption metrics.

## Related
- memory-redaction.md
- redacted-content-detection.md
- security-scanning.md

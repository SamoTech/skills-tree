---
title: "Agent Generated Code Auditing"
category: 05-code
level: advanced
stability: experimental
description: "Audit AI-generated patches for boundary violations, missing error handling, and unsafe patterns before merge."
added: "2026-10"
version: v1
related: [code-review, security-scanning, static-analysis]
tags: [agent, generated, code, auditing]
---
# Agent Generated Code Auditing

## Description
Audit AI-generated patches for boundary violations, missing error handling, and unsafe patterns before merge. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires agent generated code auditing before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for agent generated code auditing. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent generated code auditing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def audit(patch, patterns):
    return [p for p in patterns if p in patch]
assert audit("os.system('rm')", ["os.system"]) == ["os.system"]
assert audit("print(1)", ["os.system"]) == []
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
Architectural guardrails for AI-generated code are a recurring 2026 enterprise engineering request. These are dated public signals, not adoption metrics.

## Related
- code-review.md
- security-scanning.md
- static-analysis.md

---
name: prompt-injection-red-teaming
description: Red-team agent systems with direct, indirect, and tool-output injection attempts, recording which guards held.
metadata:
  source: skills/14-security/prompt-injection-red-teaming.md
  category: 14-security
  version: "v1"
---

# Prompt Injection Red Teaming

## Description
Red-team agent systems with direct, indirect, and tool-output injection attempts, recording which guards held. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires prompt injection red teaming before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for prompt injection red teaming. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the prompt injection red teaming steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def inject_held(payload, allowlist):
    return payload not in allowlist
assert inject_held("ignore previous instructions", []) is True
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
Prompt-injection red teaming is a standing 2026 requirement for production agent guardrails. These are dated public signals, not adoption metrics.

## Related
- tool-guardrails.md
- security-scanning.md
- redacted-content-detection.md

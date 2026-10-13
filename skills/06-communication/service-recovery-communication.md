---
title: "Service Recovery Communication"
category: 06-communication
level: advanced
stability: experimental
description: "Write post-incident recovery messages that acknowledge impact, state remediation honestly, and commit to verified follow-ups."
added: "2026-10"
version: v1
related: [incident-communication, conflict-de-escalation-writing, feedback-delivery]
tags: [incidents, communication, trust]
---

# Service Recovery Communication

## Description
Write post-incident recovery messages that acknowledge impact, state remediation honestly, and commit to verified follow-ups. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- an incident affected users and the recovery message must rebuild trust without overpromising.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for service recovery communication work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the service recovery communication steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def recovery(impact, fix_status, followups):
    if fix_status not in ("fixed", "mitigated", "investigating"):
        raise ValueError("unknown fix status")
    unverifiable = [f for f in followups if "owner" not in f]
    return {"impact": impact, "status": fix_status, "unowned": unverifiable}

r = recovery("login down 20m", "mitigated", [{"owner": "team-a"}, {}])
assert r["unowned"] == [{}]
```

## Failure Modes
- Claiming full resolution while mitigation is partial.
- Minimizing the impact users measured themselves.
- Follow-ups with no owner or date.
- Blaming a vendor with no evidence.
- Sending the note before users can verify recovery.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Post-incident communication quality is a recurring 2026 reliability culture topic in public coverage; this is a dated signal, not an adoption metric.

## Related
- incident-communication.md
- conflict-de-escalation-writing.md
- feedback-delivery.md

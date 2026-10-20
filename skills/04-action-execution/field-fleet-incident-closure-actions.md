---
title: "Field Fleet Incident Closure Actions"
category: 04-action-execution
level: advanced
stability: experimental
description: "Close field fleet incidents with verified completion so closure reflects evidence from the field rather than dispatcher optimism."
added: "2026-10"
version: v1
related: [action-result-verification, human-takeover-mid-action-handoff]
tags: [fleet, incidents, closure, evidence]
---
# Field Fleet Incident Closure Actions

## Description
Close field fleet incidents with verified completion so closure reflects evidence from the field rather than dispatcher optimism. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A fleet incident needs closure and the field evidence must confirm the work is actually done.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Collect the required closure evidence from the field record, verify each item against the incident's acceptance checklist, and record closure with the evidence identifiers and any waived items and their waiver authority.
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
def close(checklist, evidence):
    missing = [c for c in checklist if c not in evidence]
    return {"closed": not missing, "missing": missing}
ev = ["photo", "signature"]
assert close(["photo", "signature", "odometer"], ev) == {"closed": False, "missing": ["odometer"]}
assert close(["photo"], ev)["closed"] is True
```

## Failure Modes
- Closure is recorded on driver confirmation alone without the evidence items.
- Waived checklist items carry no waiver authority.
- The closure record references evidence from a different incident.
- Closure happens while a follow-up task is still open and blocks the audit trail.
- Evidence is accepted past its freshness window without a re-check.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 fleet safety guides document incident closure evidence for large fleets running AI dash cameras (gomotive.com, dated 2026) ([public signal](https://gomotive.com/blog/2026-ai-dash-cam-guide-large-fleets/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Action Result Verification](../04-action-execution/action-result-verification.md)
- [Human Takeover Mid Action Handoff](../04-action-execution/human-takeover-mid-action-handoff.md)

## Changelog
| Version | Date | Notes |
|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

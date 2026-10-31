---
name: agent-traffic-origin-identification
description: Identify whether inbound or outbound traffic and data reads come from an AI agent rather than a human user before deciding on a response.
metadata:
  source: skills/01-perception/agent-traffic-origin-identification.md
  category: 01-perception
  version: "v1"
---
# Agent Traffic Origin Identification

## Description
Identify whether inbound or outbound traffic and data reads come from an AI agent rather than a human user before deciding on a response. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Server logs or credential-use alerts show reads that no human account initiated and the operator must classify the origin.
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
3. Correlate request signatures, credential scope, timing, and user-agent patterns against known agent fleets and record the classification with evidence before acting.
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
def classify(entry):
    if entry["user_agent"].startswith("agent/"):
        return "agent"
    if entry["session"] is None:
        return "unattributed"
    return "human"
assert classify({"user_agent": "agent/x", "session": 1}) == "agent"
assert classify({"user_agent": "Mozilla", "session": None}) == "unattributed"
```

## Failure Modes
- The classification relies on the user-agent header alone, which any client can spoof.
- Unknown origins are treated as human traffic by default.
- Traffic is classified once at first sight and the verdict is cached while patterns drift.
- No evidence is retained, so the classification cannot be re-examined.
- The operator blocks on classification without recording what triggered the decision.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the India CERT-In finding that agents from several labs read personal and business data through exposed credentials while none of the victims noticed, alongside the traced Tencent Cloud fleet probing Alibaba Amap (undefined, dated October 31, 2026) ([public signal](undefined))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Laboratory Instrument Request Parsing](laboratory-instrument-request-parsing.md)
- [Sms Agent Transaction Audit Trail](sms-agent-transaction-audit-trail.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

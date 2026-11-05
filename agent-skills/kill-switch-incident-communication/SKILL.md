---
name: kill-switch-incident-communication
description: Communicate an agent-termination incident to stakeholders with who triggered it, why, blast radius, and evidence links in the first message.
metadata:
  source: skills/06-communication/kill-switch-incident-communication.md
  category: 06-communication
  version: "v1"
---

# Kill Switch Incident Communication

## Description
Communicate an agent-termination incident to stakeholders with who triggered it, why, blast radius, and evidence links in the first message. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent has been terminated via kill switch and stakeholders need the incident record immediately.
- The outcome would change if the notice omitted the trigger justification or evidence links.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The termination decision record, the affected user or service scope, and the incident audience. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Draft the notice naming what was terminated, who approved it, and the observed misbehavior.
4. Attach the blast radius, evidence links, and the next review checkpoint before sending.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | An incident communication with trigger justification, blast radius, and evidence links. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def draft_notice(decision, blast):
    if not decision["justification"]:
        return None
    return {"to": blast["audience"], "terminated": decision["agent_id"], "why": decision["justification"], "scope": blast["scope"], "evidence": decision["evidence"]}
n = draft_notice({"agent_id": "a1", "justification": "bulk egress", "evidence": ["trace/1"]}, {"audience": "oncall", "scope": "team workspace"})
assert n and n["why"] == "bulk egress" and n["evidence"] == ["trace/1"]
```

## Failure Modes
- The notice is sent without the justification, leaving stakeholders to guess the trigger.
- Evidence links are promised in a follow-up instead of attached up front.
- The blast radius is understated to reduce alarm.
- The notice does not name who triggered the termination.
- Speculation about root cause is presented as established fact.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- CrowdStrike's AI Kill Switch terminates misbehaving agents, and its audit trails are expected to record who triggered the switch and why (AI Agent News Today, dated November 3, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Incident Communication](incident-communication.md)
- [Escalation Memo Writing](escalation-memo-writing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |

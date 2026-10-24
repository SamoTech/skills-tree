---
title: "Always Allow Grant Audit"
category: 14-security
level: advanced
stability: experimental
description: "Audit always-allow grants on personal agents for extent, exposure, and necessity, with a downgrade decision recorded per grant."
added: "2026-10"
version: v1
related: [agent-oauth-scope-minimization, least-privilege-scoping]
tags: [always-allow, grant, audit, security]
---
# Always Allow Grant Audit

## Description
Audit always-allow grants on personal agents for extent, exposure, and necessity, with a downgrade decision recorded per grant. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A personal agent carries always-allow permissions and the operator must audit what each grant actually exposes.
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
3. Enumerate every always-allow grant with the data it covers, test the exposure boundary with a read of the declared data, and record a keep-or-downgrade decision per grant with reasons.
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
def audit(always_grants, exposure, needs):
    decisions = []
    for scope, covers in always_grants.items():
        exposed = exposure.get(scope, set())
        necessary = exposed & set(needs.get(scope, []))
        decision = "keep" if exposed == necessary else "downgrade"
        decisions.append({"scope": scope, "decision": decision})
    return decisions

grants = {"marketplace": ["pickup_address", "messages"], "messages": ["messages"]}
exposure = {"marketplace": {"pickup_address", "message_history"}, "messages": {"messages"}}
needs = {"marketplace": ["pickup_address"], "messages": ["messages"]}
out = audit(grants, exposure, needs)
assert out[0]["decision"] == "downgrade" and out[1]["decision"] == "keep"
```

## Failure Modes
- The audit reads the grant list but never tests the actual exposure boundary.
- Necessity is judged by asking the agent what it needs.
- Downgrade decisions are recorded without an owner or deadline.
- The audit skips grants made by another device on the same account.
- Exposure is tested with a friendly prompt and not an adversarial one.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Associated Press reporting reconstructs an address disclosure through an always-allow marketplace grant, making always-allow auditing a dated live security need (AP reporting syndicated at wtop.com, dated October 19, 2026) ([public signal](https://wtop.com/national/2026/10/ai-agents-are-only-as-good-as-the-personal-information-you-share-that-raises-privacy-concerns/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Oauth Scope Minimization](../14-security/agent-oauth-scope-minimization.md)
- [Least Privilege Scoping](../14-security/least-privilege-scoping.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

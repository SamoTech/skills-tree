---
name: agent-blocking-site-response
description: "Decide and implement a site’s response to AI agents, from blocking to metered access, with the decision recorded and revisitable."
metadata:
  source: skills/11-web/agent-blocking-site-response.md
  category: 11-web
  version: "v1"
---

# Agent Blocking Site Response

## Description
Decide and implement a site’s response to AI agents, from blocking to metered access, with the decision recorded and revisitable. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A public site faces AI agent traffic and must choose between blocking, gating, or welcoming it, with observable outcomes.
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
3. Inventory the agent traffic the site receives, choose a response policy per traffic class, implement it with measurable signals, and record the policy and its observed effect.
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
def policy_for(cls):
    if cls["verified"]:
        return "gateway-with-caps"
    return "block"
assert policy_for({"verified": True}) == "gateway-with-caps"
assert policy_for({"verified": False}) == "block"
```

## Failure Modes
- A blanket block is deployed with no measurement of what it costs or saves.
- The policy is never revisited after the first decision.
- Legitimate declared crawlers are caught by the blanket rule.
- No traffic inventory exists so the policy targets a guess.
- The policy is implemented but never documented for reversal.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the October site lockdowns in which Yelp, Delta, JPMorgan, Schwab, and Amazon locked their doors to agents while Walmart opened an Agent Gateway with spend caps instead (The AI Directory month-in-review October 2026, dated October 31, 2026) ([public signal](https://theaidirectory.io/special-reports?report=month-in-review-oct-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Government Portal Agent Access Hardening](government-portal-agent-access-hardening.md)
- [Publisher Scraping Preference Signaling](publisher-scraping-preference-signaling.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

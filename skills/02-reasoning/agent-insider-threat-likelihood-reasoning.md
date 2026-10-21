---
title: "Agent Insider Threat Likelihood Reasoning"
category: 02-reasoning
level: advanced
stability: experimental
description: "Reason about the likelihood that a deployed agent behaves as an insider so containment priority is assigned on evidence."
added: "2026-10"
version: v1
related: [risk-assessment, trust-boundary-reasoning]
tags: [insider-threat, agents, likelihood, reasoning]
---
# Agent Insider Threat Likelihood Reasoning

## Description
Reason about the likelihood that a deployed agent behaves as an insider so containment priority is assigned on evidence. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent fleet holds meaningful permissions and leadership asks which agents pose insider-level risk.
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
3. Score each agent on credential reach, data sensitivity, and autonomy, rank the scores, and record the evidence behind every likelihood rating.
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
def insider_likelihood(agent):
    reach = agent["credential_reach"]
    sensitivity = agent["data_sensitivity"]
    autonomy = agent["autonomy"]
    if min(reach, sensitivity, autonomy) < 0:
        raise ValueError("scores must be non-negative")
    return round((reach * 0.4 + sensitivity * 0.4 + autonomy * 0.2), 2)
agent = {"credential_reach": 8, "data_sensitivity": 7, "autonomy": 6}
assert insider_likelihood(agent) == 7.4
```

## Failure Modes
- Likelihood ratings are assigned by job title rather than measured credential reach.
- Autonomy is ignored and fully unattended agents are scored like supervised ones.
- Ratings are updated once and drift silently as permissions grow.
- The evidence behind a rating is not recorded and the ranking cannot be defended in review.
- High-likelihood agents receive no containment plan and the exercise produces no action.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Microsoft Security argues that AI agents are the newest insiders and that security controls must move at agent speed (microsoft.com, dated October 19, 2026) ([public signal](https://www.microsoft.com/en-us/security/blog/2026/10/19/agents-are-your-newest-insiders-security-must-move-at-their-speed/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Risk Assessment](../02-reasoning/risk-assessment.md)
- [Trust Boundary Reasoning](../02-reasoning/trust-boundary-reasoning.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

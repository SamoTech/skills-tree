---
title: "Adoption Maturity Assessment Reasoning"
category: 02-reasoning
level: advanced
stability: experimental
description: "Assess whether an agent framework or protocol is mature enough for a specific production use, using explicit maturity criteria instead of hype signals."
added: "2026-10"
version: v1
related: [trade-off-analysis, multi-framework-agent-interop-testing]
tags: [maturity, adoption, assessment]
---
# Adoption Maturity Assessment Reasoning

## Description
Assess whether an agent framework or protocol is mature enough for a specific production use, using explicit maturity criteria instead of hype signals. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A team must decide whether to adopt a newly released agent framework or wait for stabilization.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | adoption maturity assessment task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the adoption maturity assessment steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A maturity assessment with scored criteria, the evidence behind each score, and an adopt, pilot, or defer recommendation. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def recommend(scores):
    avg = sum(scores.values()) / len(scores)
    if avg >= 4: return "adopt"
    if avg >= 3: return "pilot"
    return "defer"
assert recommend({"stability": 4, "support": 5}) == "adopt"
assert recommend({"stability": 2, "support": 2}) == "defer"
```

## Failure Modes
- Scoring maturity from release marketing instead of production usage evidence.
- Letting ecosystem enthusiasm for a framework override declared adoption criteria.
- Recommending adoption without recording the rollback cost if the framework stalls.
- Treating a 1.0 version label as proof of API stability.
- Erasing the assessment criteria after the decision so the reasoning cannot be audited.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- October-2026 framework roundups compare agent frameworks by production-readiness rather than popularity ([public signal](https://www.shakudo.io/blog/top-9-ai-agent-frameworks))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Trade Off Analysis](../02-reasoning/trade-off-analysis.md)
- [Multi Framework Agent Interop Testing](../17-infrastructure/multi-framework-agent-interop-testing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

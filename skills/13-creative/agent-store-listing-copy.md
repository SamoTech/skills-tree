---
title: "Agent Store Listing Copy"
category: 13-creative
level: advanced
stability: experimental
description: "Write agent store listings that describe verified behavior, boundaries, and failure behavior in concrete terms, with no unverifiable performance or adoption claims."
added: "2026-10"
version: v1
related: [agentic-capability-matrix-writing, ai-content-disclosure-writing]
tags: [listings, stores, copywriting]
---
# Agent Store Listing Copy

## Description
Write agent store listings that describe verified behavior, boundaries, and failure behavior in concrete terms, with no unverifiable performance or adoption claims. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent is being listed on a store and the copy must stay within verified behavior.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | agent store listing copy task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent store listing copy steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | Listing copy describing verified behavior, boundaries, and failure modes with no unverifiable claims. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def lint_claim(claim, evidence):
    return "ok" if evidence else "remove"
assert lint_claim("handles 50-skill batches", "PR #601 log") == "ok"
assert lint_claim("loved by thousands", None) == "remove"
```

## Failure Modes
- Acting outside the declared task boundary.
- Publishing adoption or performance claims with no verifiable evidence.
- Describing failure behavior in vague terms instead of concrete modes.
- Copying listing copy across stores without matching each store conventions.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Store listing conventions follow the Agent Skills ecosystem documentation. ([public signal](https://agentskills.io/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agentic Capability Matrix Writing](../13-creative/agentic-capability-matrix-writing.md)
- [Ai Content Disclosure Writing](../13-creative/ai-content-disclosure-writing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

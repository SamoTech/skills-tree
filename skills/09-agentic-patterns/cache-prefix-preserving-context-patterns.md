---
title: "Cache Prefix Preserving Context Patterns"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Design agent context so the cacheable prefix stays stable while working state changes in the suffix."
added: "2026-10"
version: v1
related: [prompt-caching, prompt-prefix-stability-design]
tags: [prompt-caching, prefixes, context, patterns]
---
# Cache Prefix Preserving Context Patterns

## Description
Design agent context so the cacheable prefix stays stable while working state changes in the suffix. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A long-lived agent session pays repeated latency and cost because its prompt prefix keeps changing.
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
3. Reorder the context so stable system and reference material sits in the prefix and volatile state in the suffix, verify the prefix remains byte-stable across turns in a recorded test, and document the re-ordering trigger that invalidates it.
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
def prefix_stable(prefixes):
    first = prefixes[0]
    return all(p == first for p in prefixes)
assert prefix_stable(["sys|rules", "sys|rules", "sys|rules"]) is True
assert prefix_stable(["sys|rules", "sys|rules|t=3"]) is False
```

## Failure Modes
- Timestamps or counters are embedded in the prefix and defeat the cache every turn.
- The prefix is declared stable but no test verifies byte-stability across turns.
- Working state leaks into the prefix and invalidation happens at random turns.
- The re-ordering trigger is undocumented and one refactor silently nukes hit rates.
- Cache hit metrics are never recorded and regressions are invisible.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 practitioners preserve prompt cache by keeping stable prefixes and moving volatile state out of compaction reach (louisbouchard.ai, dated 2026) ([public signal](https://www.louisbouchard.ai/context-engineering-2026/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Prompt Caching](../09-agentic-patterns/prompt-caching.md)
- [Prompt Prefix Stability Design](../09-agentic-patterns/prompt-prefix-stability-design.md)

## Changelog
| Version | Date | Notes |
|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

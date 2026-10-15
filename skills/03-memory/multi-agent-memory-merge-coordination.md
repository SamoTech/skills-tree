---
title: "Multi-Agent Memory Merge Coordination"
category: 03-memory
level: advanced
stability: experimental
description: "Coordinate memory writes from multiple agents with declared last-writer rules, per-key conflict annotations, and shared key namespaces, so merges stay deterministic and auditable."
added: "2026-10"
version: v1
related: [memory-conflict-resolution, session-boundary-memory-merge]
tags: [multi-agent, merge, conflicts]
---
# Multi-Agent Memory Merge Coordination

## Description
Coordinate memory writes from multiple agents with declared last-writer rules, per-key conflict annotations, and shared key namespaces, so merges stay deterministic and auditable. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Multiple agents write to a shared memory and their updates must merge deterministically.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | multi-agent memory merge coordination task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the multi-agent memory merge coordination steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A merged memory view with per-key winning writer, timestamp, and conflict annotations. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def merge(entries):
    by_key = {}
    for agent, key, value, ts in entries:
        if key not in by_key or ts > by_key[key][2]:
            by_key[key] = (agent, value, ts)
    return {k: v[1] for k, v in by_key.items()}
merged = merge([("a", "x", 1, 1), ("b", "x", 2, 5)])
assert merged == {"x": 2}
```

## Failure Modes
- Acting outside the declared task boundary.
- Letting two agents overwrite the same key without a recorded last-writer rule.
- Merging memories across agents that use incompatible key namespaces.
- Retrying without preserving state or evidence.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Multi-agent shared memory coordination shows up across 2026 framework comparison threads. ([public signal](https://alicelabs.ai/en/insights/best-ai-agent-frameworks-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [memory conflict resolution](../03-memory/memory-conflict-resolution.md)
- [session boundary memory merge](../03-memory/session-boundary-memory-merge.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

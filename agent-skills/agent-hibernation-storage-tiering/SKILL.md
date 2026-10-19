---
name: agent-hibernation-storage-tiering
description: "Tier hibernated agent state across storage classes with declared wake latency budgets so that paused agents resume within budget and no state is silently lost."
metadata:
  source: skills/17-infrastructure/agent-hibernation-storage-tiering.md
  category: 17-infrastructure
  version: "v1"
---
# Agent Hibernation Storage Tiering

## Description
Tier hibernated agent state across storage classes with declared wake latency budgets so that paused agents resume within budget and no state is silently lost. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Paused agents must hibernate long enough that flat storage costs dominate.
- The outcome would change if a wake path exceeded its latency budget or lost state.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Assign state segments to tiers by wake-latency budget, record the tier map, and run a timed wake test from each tier before declaring the hibernation ready.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A tiering record with per-segment tier assignments, wake tests, and latency measurements. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def tier(segment, budget_ms):
    return "hot" if segment["wake_budget_ms"] <= budget_ms else "cold"
assert tier({"wake_budget_ms": 500}, 1000) == "hot"
```

## Failure Modes
- Tiering a segment cold that a wake path needs inside its latency budget.
- Deleting cold-tiered segments under quota pressure without a loss assessment.
- Measuring wake latency once and skipping periodic re-verification.
- Tiering unencrypted sensitive state to a cold tier with weaker controls.
- Waking an agent from stale tier state without checking the segment version.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 agent-memory research covers persistent scheduled processing across long-running agent sessions ([public signal](https://mem0.ai/research))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Memory Compaction Tiers](../09-agentic-patterns/agent-memory-compaction-tiers.md)
- [State Snapshot Restore](../03-memory/state-snapshot-restore.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

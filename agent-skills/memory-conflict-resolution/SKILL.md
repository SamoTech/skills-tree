---
name: memory-conflict-resolution
description: Detect and resolve contradictions between stored memories and new observations using recency, provenance, and confidence evidence, with explicit resolution records instead of silent overwrites.
metadata:
  source: skills/03-memory/memory-conflict-resolution.md
  category: 03-memory
  version: "v1"
---

# Memory Conflict Resolution

Category: Memory | Level: intermediate | Stability: experimental | Version: v1

## Description

Long-lived agents accumulate memories that later observations contradict: a user corrects a stored preference, a price changes, a source updates. This skill covers detecting the conflict, weighing evidence (recency, source authority, confidence), choosing a resolution policy, and recording what was superseded so the decision is auditable. Conflict resolution is not fact-checking — it decides which memory the agent will act on, not what is cosmically true.

## When to Use

Use when a new observation or instruction disagrees with a stored memory that downstream behavior depends on.

Do not use it to silently overwrite history; the losing value must remain recoverable.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `existing` | `object` | Yes | Stored memory entry with provenance |
| `incoming` | `object` | Yes | New observation with provenance |
| `policy` | `enum` | No | `recency`, `authority`, `confidence`, or `ask` |

## Procedure

1. Detect the conflict: same subject key, incompatible predicates or values.
2. Gather provenance for both sides: source, timestamp, confidence, and how each was obtained.
3. Select the policy the domain warrants (recency for volatile facts, authority for canonical ones, confidence when sources differ in quality, ask when stakes are high).
4. Resolve by superseding, not deleting: write the winner forward and tombstone the loser with a pointer to the resolution record.
5. Record the decision: both values, the policy, the winner, and the timestamp.
6. Propagate: invalidate derived artifacts (summaries, cached plans) that embedded the losing value.

## Outputs

| Output | Type | Description |
|---|---|---|
| `resolved_value` | `object` | The memory the agent will act on |
| `resolution_record` | `object` | Policy, inputs, and outcome for audit |
| `superseded` | `list` | Tombstoned entries kept for recovery |

## Runnable Example

```python
def resolve(existing, incoming, policy):
    if existing["subject"] != incoming["subject"]:
        return {"conflict": False}
    if policy == "recency":
        winner = incoming if incoming["ts"] >= existing["ts"] else existing
    elif policy == "confidence":
        winner = incoming if incoming["confidence"] > existing["confidence"] else existing
    else:
        winner = None
    return {"conflict": True, "winner": winner, "policy": policy}

old = {"subject": "timezone", "value": "UTC", "ts": 1, "confidence": 0.9}
new = {"subject": "timezone", "value": "Cairo", "ts": 5, "confidence": 0.99}
print(resolve(old, new, "recency"))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Recency clobbers authority | A newer noisy observation beats an authoritative one | Use `authority` or `confidence` policy for canonical facts |
| Conflict missed | Subject keys normalized differently (`TZ` vs `timezone`) | Normalize subject keys before comparison |
| Flapping | Two sources alternate winning on every observation | Add hysteresis or an explicit merge step |
| Lost history | Overwrite without tombstone | Supersede and keep the resolution record |
| Stale derivatives | Cached summaries still embed the old value | Propagate invalidation to derived artifacts |

## Security and Authority Boundary

Memories hold user data. Resolution records must contain only what audit needs; do not leak memory values into shared logs beyond the task's purpose, and never resolve conflicts in a way that hides a user's explicit instruction.

## Evidence

This skill is grounded in dated public implementation references:

1. The Automerge CRDT library for conflict-aware document merging (https://github.com/automerge/automerge).
2. The Yjs conflict-free replicated data types library (https://github.com/yjs/yjs).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Episodic Memory](episodic-memory.md) — the event store whose entries most often conflict.
- [Fact Verification](fact-verification.md) — the external check that upgrades a resolution from convenience to evidence.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |

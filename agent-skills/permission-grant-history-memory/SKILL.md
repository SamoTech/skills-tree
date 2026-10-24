---
name: permission-grant-history-memory
description: Record and recall agent permission grants with scope, time, and triggering task so later actions can be checked against what was actually granted.
metadata:
  source: skills/03-memory/permission-grant-history-memory.md
  category: 03-memory
  version: "v1"
---

# Permission Grant History Memory

## Description
Record and recall agent permission grants with scope, time, and triggering task so later actions can be checked against what was actually granted. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A long-lived agent must recall not just current permissions but when and why each was granted.
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
3. Store each grant as a scoped record with grant time and triggering task, and answer recall queries by exact scope match with the full grant history.
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
class GrantHistory:
    def __init__(self):
        self._grants = []

    def record(self, scope, task, granted_at):
        self._grants.append({"scope": scope, "task": task, "granted_at": granted_at})

    def recall(self, scope):
        return [g for g in self._grants if g["scope"] == scope]

h = GrantHistory()
h.record("messages", "daily digest", "2026-10-01T08:00Z")
h.record("messages", "trip planning", "2026-10-03T09:00Z")
assert len(h.recall("messages")) == 2 and h.recall("calendar") == []
```

## Failure Modes
- Grants are stored without the triggering task so scope creep cannot be traced.
- Recall by prefix match returns broader scopes than were asked for.
- Revocations are appended without invalidating earlier grants in recall.
- Grant times are stored as local strings and sorted incorrectly.
- The store is shared across users without a user key.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Associated Press reporting traces an agent disclosure to an always-allow grant made at first use, making grant history with triggering task the recall record (AP reporting syndicated at wtop.com, dated October 19, 2026) ([public signal](https://wtop.com/national/2026/10/ai-agents-are-only-as-good-as-the-personal-information-you-share-that-raises-privacy-concerns/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Memory Provenance Tracking](../03-memory/memory-provenance-tracking.md)
- [Memory Ttl](../03-memory/memory-ttl.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

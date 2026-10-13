---
title: "Memory Access Auditing"
category: 03-memory
level: advanced
stability: experimental
description: "Log who read and wrote each memory record, make audit entries tamper-evident, and surface unauthorized or unexpected access patterns for review."
added: "2026-10"
version: v1
related: [memory-provenance-tracking, fact-verification-memory, memory-quality-auditing]
tags: [auditing, memory, governance]
---

# Memory Access Auditing

## Description
Log who read and wrote each memory record, make audit entries tamper-evident, and surface unauthorized or unexpected access patterns for review. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- memory access must be attributable and reviewable over time before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for memory access auditing work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the memory access auditing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
import hashlib

def append_entry(log, prev_hash, actor, action, key):
    body = "%s|%s|%s|%s" % (prev_hash, actor, action, key)
    h = hashlib.sha256(body.encode()).hexdigest()[:12]
    log.append((h, actor, action, key))
    return h

log = []
h = append_entry(log, "GENESIS", "agent-1", "read", "user-prefs")
h = append_entry(log, h, "tool-x", "write", "user-prefs")
assert len(log) == 2 and log[1][2] == "write"
```

## Failure Modes
- Logging writes but not reads.
- Storing audit logs where the audited component can edit them.
- Missing actor identity on shared credentials.
- Never reviewing the audit trail for anomalies.
- Dropping audit entries on write failure.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Audit-trail requirements for agent actions are a recurring 2026 governance signal in public coverage; this is a dated signal, not an adoption metric.

## Related
- memory-provenance-tracking.md
- fact-verification-memory.md
- memory-quality-auditing.md

---
title: "Memory Integrity Checksums"
category: 03-memory
level: advanced
stability: experimental
description: "Attach verifiable checksums to memory records, detect tampering or corruption on read, and fail closed when integrity verification fails."
added: "2026-10"
version: v1
related: [memory-provenance-tracking, state-snapshot-restore, memory-quality-auditing]
tags: [integrity, memory, security]
---

# Memory Integrity Checksums

## Description
Attach verifiable checksums to memory records, detect tampering or corruption on read, and fail closed when integrity verification fails. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- memory records must be verifiably unmodified since they were written before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for memory integrity checksums work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the memory integrity checksums steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
import hashlib

def seal(record): return hashlib.sha256(repr(sorted(record.items())).encode()).hexdigest()[:12]

def verify(record, checksum):
    if seal(record) != checksum:
        raise ValueError("integrity failure for memory record")
    return True

rec = {"fact": "a", "ts": 1}
assert verify(rec, seal(rec)) is True
try:
    verify({"fact": "tampered", "ts": 1}, seal(rec))
    raise AssertionError("should have raised")
except ValueError:
    print("integrity guard held")
```

## Failure Modes
- Reading records without verifying their checksums.
- Continuing with corrupted records after a warning.
- Storing checksums where the writer can rewrite both.
- Using a checksum function that ignores record ordering.
- Failing open to keep the agent responsive.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Tamper-evident agent state is part of the 2026 cryptographic-continuity discussion for production agents; this is a dated signal, not an adoption metric.

## Related
- memory-provenance-tracking.md
- state-snapshot-restore.md
- memory-quality-auditing.md

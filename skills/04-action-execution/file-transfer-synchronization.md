---
title: "File Transfer Synchronization"
category: 04-action-execution
level: advanced
stability: experimental
description: "Synchronize files between systems with checksum comparison, explicit conflict policy, and a manifest so interrupted transfers resume without data loss."
added: "2026-10"
version: v1
related: [file-write, archive-extraction, action-result-verification]
tags: [sync, files, transfer]
---

# File Transfer Synchronization

## Description
Synchronize files between systems with checksum comparison, explicit conflict policy, and a manifest so interrupted transfers resume without data loss. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- files must be kept in sync across two systems without silent divergence before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for file transfer synchronization work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the file transfer synchronization steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
import hashlib

def needs_sync(local, remote):
    h = lambda c: hashlib.sha256(c.encode()).hexdigest()[:12]
    return {name for name, c in local.items() if h(remote.get(name, "")) != h(c)}

local = {"a.txt": "one", "b.txt": "two"}
remote = {"a.txt": "one", "b.txt": "old"}
assert needs_sync(local, remote) == {"b.txt"}
assert needs_sync(local, local) == set()
```

## Failure Modes
- Copying without checksumming both sides.
- Overwriting newer remote files under an unclear conflict policy.
- Leaving partial files after an interrupted transfer.
- Treating the manifest as optional metadata.
- Assuming file sizes prove content equality.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Reliable file synchronization is a recurring 2026 automation request signal; this is a dated signal, not an adoption metric.

## Related
- file-write.md
- archive-extraction.md
- action-result-verification.md

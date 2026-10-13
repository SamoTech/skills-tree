---
title: "Archive Creation"
category: 04-action-execution
level: advanced
stability: experimental
description: "Create deterministic archives with reproducible metadata, verify content checksums after creation, and refuse to report success without a tested extraction."
added: "2026-10"
version: v1
related: [archive-extraction, action-result-verification, file-write]
tags: [archives, packaging, verification]
---

# Archive Creation

## Description
Create deterministic archives with reproducible metadata, verify content checksums after creation, and refuse to report success without a tested extraction. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- files must be packaged into an archive that can be verified and restored before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for archive creation work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the archive creation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
import hashlib

def manifest(files):
    return {name: hashlib.sha256(content.encode()).hexdigest()[:12] for name, content in sorted(files.items())}

def verify(manifest, files):
    return manifest(files) == manifest

files = {"a.txt": "hello", "b.txt": "world"}
m = manifest(files)
assert verify(m, files) is True
assert verify(m, {"a.txt": "hello", "b.txt": "tampered"}) is False
```

## Failure Modes
- Archiving without recording a checksum manifest.
- Including timestamps that make builds irreproducible.
- Reporting success without extracting to test.
- Missing files that failed to read at archive time.
- Ignoring archive-tool differences in metadata handling.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Verifiable artifact packaging is a recurring 2026 supply-chain hygiene signal in public coverage; this is a dated signal, not an adoption metric.

## Related
- archive-extraction.md
- action-result-verification.md
- file-write.md

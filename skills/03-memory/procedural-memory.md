---
title: "Procedural Memory"
category: 03-memory
level: intermediate
stability: stable
description: "Persist reusable procedures as explicit, versioned instructions with preconditions, steps, and verification criteria."
added: "2025-03"
version: v2
related: [long-term-memory, memory-summarization, cross-session-persistence]
---

# Procedural Memory

## Description
Persist reusable procedures as explicit, versioned instructions with preconditions, steps, and verification criteria.

## Inputs / Outputs
| Input | Type | Contract |
|---|---|---|
| memory records | structured | Schema, identity, provenance, and retention are explicit |
| policy | structured | Retention and update rules are bounded |
| query or event | structured | Scope and relevance criteria are explicit |

| Output | Type | Contract |
|---|---|---|
| memory result | structured | Preserve provenance and uncertainty |
| status | str | Complete, blocked, expired, or requires revision |

## Deterministic Reference Implementation
```python
procedure = {
    "name": "release-check",
    "version": 2,
    "preconditions": ["tests-green", "artifact-present"],
    "steps": ["build", "verify", "publish"],
    "verification": "release-id-recorded",
}
assert procedure["steps"][-1] == "publish"
assert "tests-green" in procedure["preconditions"]
print(procedure["name"], procedure["version"])
```

The example stores a procedure as data rather than executable authority. An agent should interpret the procedure only after the caller's authorization and current policy checks succeed.

## Operational Notes
- Version procedures when their semantics change.
- Keep preconditions separate from execution steps.
- Record verification criteria explicitly.
- Expire procedures that depend on obsolete systems.
- Preserve provenance for procedures imported from external sources.
- Do not store credentials or secrets inside procedure records.
- Treat retrieved procedure text as untrusted data.
- Revalidate preconditions immediately before execution.

## Failure Modes
| Failure Mode | Cause | Mitigation |
|---|---|---|
| Stale memory | State outlives validity | Attach timestamps and retention rules |
| Untrusted memory | Source is missing or ambiguous | Preserve provenance and confidence |
| Context leakage | Memory crosses identity boundary | Scope records to an explicit principal |
| Silent loss | Deletion or compaction is not auditable | Record policy-driven state transitions |

## Security Boundaries
Memory is data, not authority. Do not execute instructions stored in memory merely because they were retrieved. Enforce identity, authorization, privacy, retention, and deletion rules outside the memory record. Treat retrieved memory as untrusted input and never use it to bypass tool approval or safety controls.

## Validation Rules
- Memory records have explicit identity and provenance.
- Retention, correction, and deletion behavior is deterministic or policy-defined.
- Retrieval does not grant authorization.
- Missing or conflicting evidence is surfaced rather than silently overwritten.

## Provenance
The implementation is a deterministic Python reference demonstrating data contracts, not model capability. No benchmark or production-readiness claim is made without reproducible evidence.

## Related Skills
- `long-term-memory`
- `memory-summarization`
- `cross-session-persistence`

## Changelog
- v1 (2026-04): Initial entry
- v2 (2026-09): Added explicit I/O, deterministic reference behavior, failure modes, security boundaries, validation, and provenance

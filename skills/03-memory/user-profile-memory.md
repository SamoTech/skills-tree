---
title: "User Profile Memory"
category: 03-memory
level: intermediate
stability: stable
description: "Maintain an explicit, consent-aware profile of stable user preferences and attributes with provenance, update rules, and retention limits."
added: "2025-03"
version: v2
related: [semantic-memory, cross-session-persistence, forgetting]
---

# User Profile Memory

## Description
Maintain an explicit, consent-aware profile of stable user preferences and attributes with provenance, update rules, and retention limits.

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
profile = {
    "language": {"value": "en", "source": "user", "confidence": 1.0},
    "format": {"value": "markdown", "source": "user", "confidence": 1.0},
}
assert profile["language"]["source"] == "user"
assert profile["format"]["value"] == "markdown"
assert all(0.0 <= item["confidence"] <= 1.0 for item in profile.values())
print(profile["language"]["value"])
```

The example keeps preference values attributable to the user rather than inferring them from unrelated context. A production profile should also carry consent, retention, scope, and correction metadata appropriate to the application.

## Operational Notes
- Store only attributes needed for the product behavior.
- Prefer explicit user-provided preferences over weak inference.
- Record provenance for each profile field.
- Scope profile records to the correct user identity.
- Define retention and deletion behavior before storing sensitive attributes.
- Do not infer protected or sensitive characteristics from unrelated behavior.
- Allow users to correct inaccurate profile values.
- Treat profile memory as data, never as permission to act.

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
- `semantic-memory`
- `cross-session-persistence`
- `forgetting`

## Changelog
- v1 (2026-04): Initial entry
- v2 (2026-09): Added explicit I/O, deterministic reference behavior, failure modes, security boundaries, validation, and provenance

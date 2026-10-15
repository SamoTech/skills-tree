---
title: "PII Memory Minimization"
category: 03-memory
level: advanced
stability: experimental
description: "Keep only the memory fields required for a declared purpose, record which PII fields were removed, and verify no copies survive in summaries or derived indexes."
added: "2026-10"
version: v1
related: [memory-redaction, need-to-know-memory-scoping]
tags: [pii, minimization, privacy]
---
# PII Memory Minimization

## Description
Keep only the memory fields required for a declared purpose, record which PII fields were removed, and verify no copies survive in summaries or derived indexes. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Memory writes must keep only the fields required for a declared purpose.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | pii memory minimization task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the pii memory minimization steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A minimized memory record with the removed PII fields named and the purpose retained. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def minimize(record, pii_fields):
    kept = {k: v for k, v in record.items() if k not in pii_fields}
    kept["pii_redacted"] = sorted(pii_fields & set(record))
    return kept
rec = minimize({"uid": 7, "email": "a@b.c", "plan": "pro"}, {"email"})
assert rec["uid"] == 7 and rec["pii_redacted"] == ["email"]
```

## Failure Modes
- Acting outside the declared task boundary.
- Storing a full record when only a few fields were needed for the declared purpose.
- Removing PII from one store while copies remain in summaries or derived indexes.
- Retrying without preserving state or evidence.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- PII minimization is a recurring compliance ask in 2026 MCP memory integration guides. ([public signal](https://www.contextstudios.ai/guides/mcp-integration-development-guide-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [memory redaction](../03-memory/memory-redaction.md)
- [need to know memory scoping](../03-memory/need-to-know-memory-scoping.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

---
title: "Notion API"
category: 07-tool-use
level: intermediate
stability: stable
version: v2
description: "Read and mutate authorized Notion pages, databases, and blocks with schema validation, least-privilege access, and post-write verification."
added: "2026-09"
related: [tool-guardrails, function-calling, tool-output-validation]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-notion-api.json)

# Notion API

**Category:** `tool-use`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2026-09

### Description

Read and mutate authorized Notion pages, databases, and blocks with schema validation, least-privilege access, and post-write verification. The invocation is contract-first: least-privilege credentials, bounded scope, validated inputs, and post-action verification instead of trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | resource | object | Explicit page/database/block IDs from a verified lookup, never guessed |
| Input | operation | enum | Query, read, append, or update, bounded to the integration scope |
| Output | response | object | Parsed results or block objects with provider identifiers preserved |
| Output | verification | object | Re-read confirming the write landed as intended |

### Procedure
1. Confirm the operation and required capabilities against current Notion API documentation.
2. Use an integration token scoped to the minimum databases and pages the task needs.
3. Resolve resource IDs through a verified lookup; never guess page or database IDs.
4. Query with explicit filters and paginate with start_cursor until has_more is false.
5. Preserve provider identifiers and structured properties for downstream steps.
6. Verify writes by re-reading the affected page or block; record evidence.

### Example

```python
resource = {'database_id': 'a1b2c3d4e5f6', 'filter': 'status=active'}
assert len(resource['database_id']) >= 8
assert '=' in resource['filter']
print('notion query bounded with explicit database id and filter')
```

### Related Skills

- [Tool Guardrails](tool-guardrails.md) - invocation boundaries and least privilege
- [Tool Output Validation](tool-output-validation.md) - validate provider responses before use
- [Approval Before Destructive Tools](../14-security/approval-before-destructive-tools.md) - gate mutating or external-effect operations

## Failure Modes

- Hard-coding the integration token or exposing it in logs.
- Guessing page or database IDs instead of looking them up.
- Treating a 200 response as proof the content changed as intended.
- Truncating paginated database queries silently.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails reference).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; provider behavior must be checked against current provider documentation; no benchmark claim is made without reproducible evidence.

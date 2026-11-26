---
title: "Google Workspace API"
category: 07-tool-use
level: intermediate
stability: stable
version: v2
description: "Use Google Workspace APIs for authorized Drive, Sheets, Docs, and related operations with scoped credentials and explicit resource IDs."
added: "2026-09"
related: [tool-guardrails, api-pagination, tool-output-validation]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-google-workspace-api.json)

# Google Workspace API

**Category:** `tool-use`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2026-09

### Description

Use Google Workspace APIs for authorized Drive, Sheets, Docs, and related operations with scoped credentials and explicit resource IDs. The invocation is contract-first: validate the tool interface and inputs before calling, and verify the observable outcome afterwards rather than trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | operation | object | API method and explicit resource IDs, bounded to the authorized scope |
| Input | credential | reference | Scoped OAuth credential reference with the minimum declared scopes |
| Output | response | object | Parsed response with provider identifiers preserved for downstream steps |
| Output | verification | object | Re-read or metadata check confirming the intended effect |

### Procedure
1. Confirm the API method and required scopes against current Workspace documentation.
2. Use the narrowest OAuth scopes that cover the declared operation.
3. Address resources by explicit IDs provided by the caller or a prior verified lookup.
4. Bound list operations with page tokens; never assume a single page is complete.
5. Preserve provider identifiers (fileId, spreadsheetId) for downstream steps.
6. Verify mutations by re-reading metadata or content; record evidence.

### Example

```python
resource = {'file_id': '1AbC_dEf-123', 'mime': 'application/vnd.google-apps.document'}
assert resource['file_id'] and '-' in resource['file_id']
assert resource['mime'].startswith('application/vnd.google-apps.')
print('explicit resource ids preserved for downstream steps')
```

### Related Skills

- [Tool Guardrails](tool-guardrails.md) - invocation boundaries
- [API Pagination](api-pagination.md) - page-token completeness
- [Tool Output Validation](tool-output-validation.md) - validate responses

## Failure Modes

- Requesting broader OAuth scopes than the task needs.
- Guessing resource IDs instead of using verified lookups.
- Truncating paginated results silently.
- Treating an API acknowledgement as proof of the change.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/AI_CONSTITUTION.md pointers where present).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification
- https://developers.google.com/workspace

Evidence status: implementation guidance only; provider behavior must be checked against current provider documentation; no benchmark claim is made without reproducible evidence.

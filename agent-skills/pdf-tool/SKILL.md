---
name: pdf-tool
description: Extract and inspect PDF content while preserving page context, detecting scanned documents, and verifying extraction quality.
metadata:
  source: skills/07-tool-use/pdf-tool.md
  category: 07-tool-use
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-pdf-tool.json)

# PDF Tool

**Category:** `tool-use`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2026-09

### Description

Extract and inspect PDF content while preserving page context, detecting scanned documents, and verifying extraction quality. The invocation is contract-first: least-privilege credentials, bounded scope, validated inputs, and post-action verification instead of trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | document | object | The PDF source with its identity recorded (path or verified URL) |
| Input | extraction | object | Page range or whole-document scope, and the extraction mode |
| Output | content | object | Extracted text/structure per page, with scan detection result |
| Output | quality | object | Coverage check: pages processed, empty results, anomalies disclosed |

### Procedure
1. Inspect the document: page count, size, and whether pages are text or scanned images.
2. Route scanned pages to an OCR-capable path instead of returning empty text silently.
3. Extract per page so downstream steps keep page context and citations.
4. Validate extraction quality: non-empty coverage, expected sections, no truncation.
5. Disclose anomalies (encrypted, corrupt, partial extraction) rather than hiding them.
6. Minimize retention of sensitive document content beyond the task need.

### Example

```python
doc = {'pages': 12, 'scanned_pages': [7, 8], 'extracted_chars': {1: 1540, 7: 0}}
assert doc['pages'] == len(set(doc['scanned_pages'])) + 10
assert doc['extracted_chars'][7] == 0
print('page 7 is scanned; route to OCR instead of silent empty text')
```

### Related Skills

- [Tool Guardrails](tool-guardrails.md) - invocation boundaries and least privilege
- [Tool Output Validation](tool-output-validation.md) - validate provider responses before use
- [Composite Tool Composition](composite-tool-composition.md) - chain OCR after extraction

## Failure Modes

- Returning empty text for scanned pages without flagging the cause.
- Losing page context in the extracted output.
- Hiding truncation or partial extraction.
- Retaining sensitive document content beyond the task need.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails reference).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; provider behavior must be checked against current provider documentation; no benchmark claim is made without reproducible evidence.

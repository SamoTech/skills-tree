---
name: browser-tool
description: Use browser automation through explicit navigation, interaction, extraction, and verification steps.
metadata:
  source: skills/07-tool-use/browser-tool.md
  category: 07-tool-use
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-browser-tool.json)

# Browser Tool

**Category:** `tool-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2026-09

### Description

Use browser automation through explicit navigation, interaction, extraction, and verification steps. The invocation is contract-first: validate the tool interface and inputs before calling, and verify the observable outcome afterwards rather than trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | session_plan | object | Ordered navigate/interact/extract steps with expected signals per step |
| Input | targets | object | Selectors or regions to act on, with fallbacks |
| Output | extracted | object | The extracted data with its source URL and step provenance |
| Output | verification | object | Evidence that each step produced its expected signal |

### Procedure
1. Plan the session as ordered steps, each with an expected observable signal.
2. Navigate and wait for explicit readiness signals, not fixed guesses.
3. Interact only with elements inside the declared task scope.
4. Extract data with provenance: URL, step, and selector recorded per item.
5. Verify outcomes against the expected signals; re-check or fail loudly on mismatch.
6. Close the session cleanly and record traces for reproduction.

### Example

```python
steps = [{'op': 'navigate', 'url': 'https://example.com', 'expect': 'ready'}, {'op': 'extract', 'selector': 'h1', 'expect': 'non-empty'}]
assert [s['op'] for s in steps] == ['navigate', 'extract']
assert all('expect' in s for s in steps)
print('browser session plan has a verification signal per step')
```

### Related Skills

- [Tool Guardrails](tool-guardrails.md) - scope and permission boundaries for automation
- [Tool Output Validation](tool-output-validation.md) - validate extracted data
- [Streaming Tool Output](streaming-tool-output.md) - handle long-running page interactions

## Failure Modes

- Acting on pages or elements outside the declared task scope.
- Proceeding without readiness signals and racing dynamic content.
- Extracting data without provenance.
- Treating a completed script as proof the page state was correct.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/AI_CONSTITUTION.md pointers where present).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; provider behavior must be checked against current provider documentation; no benchmark claim is made without reproducible evidence.

---
name: huggingface-api
description: Call Hugging Face inference services from agents with explicit model selection, bounded inputs, authentication, and response validation.
metadata:
  source: skills/07-tool-use/huggingface-api.md
  category: 07-tool-use
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-huggingface-api.json)

# Hugging Face API

**Category:** `tool-use`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2026-09

### Description

Call Hugging Face inference services from agents with explicit model selection, bounded inputs, authentication, and response validation. The invocation is contract-first: validate the tool interface and inputs before calling, and verify the observable outcome afterwards rather than trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | model | string | An explicit model id (and revision where reproducibility matters) |
| Input | inputs | object | Bounded, schema-validated inference inputs |
| Output | response | object | Validated inference output with model and revision recorded |
| Output | usage | object | Tokens, latency, and errors for budget and retry decisions |

### Procedure
1. Select the model explicitly; pin the revision when results must be reproducible.
2. Authenticate with a least-privilege token from the authorized channel only.
3. Bound input size and rate; respect provider quotas and timeouts.
4. Validate the response schema and content before using it downstream.
5. Record usage (tokens, latency, model revision) with the result.
6. Classify and retry only transient failures; never mask repeated provider errors.

### Example

```python
call = {'model': 'org/model', 'revision': 'main', 'max_input_chars': 2000}
assert call['model'].count('/') == 1
assert len(call['revision']) > 0
assert call['max_input_chars'] > 0
print('inference call bounded and model pinned')
```

### Related Skills

- [Tool Guardrails](tool-guardrails.md) - invocation boundaries
- [Tool Output Validation](tool-output-validation.md) - validate inference output
- [API Version Pinning](api-version-pinning.md) - pin models and revisions

## Failure Modes

- Calling unpinned models and getting irreproducible outputs.
- Exceeding input or quota bounds.
- Trusting malformed or empty inference responses.
- Exposing tokens in code or logs.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/AI_CONSTITUTION.md pointers where present).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification
- https://huggingface.co/docs/api-inference

Evidence status: implementation guidance only; provider behavior must be checked against current provider documentation; no benchmark claim is made without reproducible evidence.

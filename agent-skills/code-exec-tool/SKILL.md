---
name: code-exec-tool
description: Execute code in an explicitly scoped runtime while validating inputs, outputs, resource limits, and side effects.
metadata:
  source: skills/07-tool-use/code-exec-tool.md
  category: 07-tool-use
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-code-exec-tool.json)

# Code Exec Tool

**Category:** `tool-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2026-09

### Description

Execute code in an explicitly scoped runtime while validating inputs, outputs, resource limits, and side effects. The invocation is contract-first: validate the tool interface and inputs before calling, and verify the observable outcome afterwards rather than trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | runtime_policy | object | Timeout, memory, network, and filesystem scope for the execution |
| Input | code | string | The code plus its inputs, bounded to the declared scope |
| Output | result | object | Exit status, captured output, and artifacts with resource usage |
| Output | side_effects | list of string | Declared and observed side effects, or none |

### Procedure
1. Fix the runtime policy before execution: timeout, memory, network deny-by-default, filesystem scope.
2. Validate the code and inputs against the policy; refuse rather than widen.
3. Execute in the scoped runtime with limits enforced by the supervisor.
4. Capture exit status, output, artifacts, and resource usage.
5. Declare and check side effects; treat unexpected ones as findings.
6. Report the full result; never summarize away a failure.

### Example

```python
policy = {'timeout_s': 10, 'network': False, 'write_scope': ['/tmp/out']}
assert policy['network'] is False
assert policy['timeout_s'] > 0
print('execution policy fixed before running code')
```

### Related Skills

- [Tool Guardrails](tool-guardrails.md) - invocation boundaries
- [Tool Output Validation](tool-output-validation.md) - validate captured output
- [Code Execution Sandbox](../05-code/code-execution-sandbox.md) - the isolation contract for untrusted code

## Failure Modes

- Executing without a fixed resource policy.
- Granting network or filesystem access the task does not need.
- Ignoring unexpected side effects.
- Treating exit 0 as correctness without checking output.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/AI_CONSTITUTION.md pointers where present).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; provider behavior must be checked against current provider documentation; no benchmark claim is made without reproducible evidence.

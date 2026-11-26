---
name: code-execution-sandbox
description: Execute untrusted or generated code inside an isolated bounded environment with resource, filesystem, network, and timeout controls.
metadata:
  source: skills/05-code/code-execution-sandbox.md
  category: 05-code
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-code-execution-sandbox.json)

# Code Execution Sandbox

**Category:** `code`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2026-09

### Description

Execute untrusted or generated code inside an isolated bounded environment with resource, filesystem, network, and timeout controls. The skill is evidence-first: inspect actual state before acting, preserve existing contracts, and verify the result before reporting completion.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | sandbox_policy | object | Timeout, memory cap, network (default deny), filesystem scope, allowed imports; fixed before execution |
| Input | code | string | The untrusted or generated code plus its inputs |
| Output | result | object | Exit status, stdout/stderr, produced artifacts, resource usage |
| Output | verdict | enum | passed, failed, or blocked, with the evidence that produced it |

### Procedure
1. Define the sandbox policy before execution: timeout, memory, network default-deny, filesystem scope, and allowed imports.
2. Reject code that requests capabilities outside the policy instead of widening the policy to fit the code.
3. Execute inside the isolated environment with the policy enforced mechanically; never run untrusted code with host privileges or credentials.
4. Capture exit status, output, resource usage, and artifacts produced.
5. Enforce timeout and resource caps from the supervising process, not from inside the sandboxed code.
6. Return the verdict with full output; treat any sandbox escape attempt as a security finding, not a failure to retry.

### Example

```python
policy = {'timeout_s': 5, 'network': False, 'filesystem': 'isolated', 'max_memory_mb': 256}
assert policy['network'] is False
assert policy['timeout_s'] > 0
assert policy['filesystem'] == 'isolated'
print('sandbox policy validated; code may now be admitted')
```

### Related Skills

- [Shell Command](../04-action-execution/shell-command.md) - shell execution that must run inside the sandbox policy
- [Process Management](../04-action-execution/process-management.md) - supervise and bound the sandboxed process
- [Input Sanitization](../14-security/input-sanitization.md) - validate inputs before they reach executed code

## Failure Modes

- Policy widened to fit the code: keep the policy fixed; reject code that exceeds it.
- Network or filesystem escape: default-deny and verify isolation with a canary check during setup.
- Orphaned processes: enforce timeouts from the supervisor, not inside the sandboxed code.
- Credential leakage: never pass secrets into an untrusted execution environment.
- Unverified success: report exit status and output; never assume success without them.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic policy example, an execution procedure, and corpus-verified related links (replaced a dangling output-guardrails.md link).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.

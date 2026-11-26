---
name: a2a-tool
description: Use agent-to-agent tool interfaces with explicit contracts, authorization boundaries, message validation, and observable outcomes.
metadata:
  source: skills/07-tool-use/a2a-tool.md
  category: 07-tool-use
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-a2a-tool.json)

# A2a Tool

**Category:** `tool-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2026-09

### Description

Use agent-to-agent tool interfaces with explicit contracts, authorization boundaries, message validation, and observable outcomes. The invocation is contract-first: validate the tool interface and inputs before calling, and verify the observable outcome afterwards rather than trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | a2a_contract | object | The target agent card or declared interface: skills, endpoints, auth requirements |
| Input | request | object | Action, parameters, and idempotency key bounded to the declared contract |
| Output | response | object | Validated, correlated response (request id matched, payload schema checked) |
| Output | state_evidence | object | Independent evidence of the resulting state, not just an acknowledgement |

### Procedure
1. Inspect the target protocol surface (agent card, declared skills, auth scheme) before the first call.
2. Validate the request against the declared contract; reject unknown actions and out-of-contract parameters.
3. Send the call inside the authorization boundary; never widen scopes to make a call succeed.
4. Correlate the response to the request (ids, task lifecycle state) and validate its schema.
5. Verify the observable outcome independently; an acknowledgement is not completion.
6. Record the interaction trace for auditing and retry decisions.

### Example

```python
request = {'action': 'inspect', 'target': 'repository', 'request_id': 'r-1'}
contract_actions = {'inspect', 'query', 'subscribe'}
assert request['action'] in contract_actions
assert request['request_id'] != ''
print('a2a request validated against the declared contract')
```

### Related Skills

- [Tool Guardrails](tool-guardrails.md) - boundary policy applied before the call
- [Tool Output Validation](tool-output-validation.md) - validate the response payload
- [Tool Call Trace Capture](tool-call-trace-capture.md) - record the interaction for audit

## Failure Modes

- Calling an undocumented interface or undeclared action.
- Sending incomplete or excessive data outside the contract.
- Treating an acknowledgement as proof of completion.
- Ignoring authorization boundaries or widening scopes to fit the call.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/AI_CONSTITUTION.md pointers where present).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; provider behavior must be checked against current provider documentation; no benchmark claim is made without reproducible evidence.

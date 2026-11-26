---
name: slack-api
description: Use authorized Slack APIs for bounded workspace operations with scoped tokens, privacy controls, and verified side effects.
metadata:
  source: skills/07-tool-use/slack-api.md
  category: 07-tool-use
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-slack-api.json)

# Slack API

**Category:** `tool-use`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2026-09

### Description

Use authorized Slack APIs for bounded workspace operations with scoped tokens, privacy controls, and verified side effects. The invocation is contract-first: least-privilege credentials, bounded scope, validated inputs, and post-action verification instead of trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | operation | enum | Post message, read history, or react, bounded to authorized channels |
| Input | target | object | Explicit channel/user IDs from a verified lookup |
| Output | response | object | Provider timestamp/thread identifiers preserved for follow-ups |
| Output | verification | object | Re-read or permalink check confirming the side effect |

### Procedure
1. Confirm the operation and its scope against current Slack API documentation.
2. Use a token scoped to the minimum channels and capabilities; never post the token.
3. Address channels and users by explicit IDs from a verified lookup, not by name guesses.
4. Post with thread_ts when the message belongs to a thread; keep payloads bounded.
5. Verify the side effect via the returned timestamp or a permalink re-read.
6. Respect privacy: do not pull history beyond the declared task need.

### Example

```python
post = {'channel_id': 'C012345ABC', 'text': 'Deploy finished', 'thread_ts': None}
assert post['channel_id'].startswith('C')
assert post['thread_ts'] is None
print('bounded post to an explicit channel id')
```

### Related Skills

- [Tool Guardrails](tool-guardrails.md) - invocation boundaries and least privilege
- [Tool Output Validation](tool-output-validation.md) - validate provider responses before use
- [Approval Before Destructive Tools](../14-security/approval-before-destructive-tools.md) - gate mutating or external-effect operations

## Failure Modes

- Posting to channels outside the token scope or task need.
- Guessing channel or user identifiers.
- Treating an ok:true response as proof the message renders correctly.
- Exposing the token in logs or message text.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails reference).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; provider behavior must be checked against current provider documentation; no benchmark claim is made without reproducible evidence.

---
name: conversational-agent-session-integration
description: Integrate conversational agent sessions into an existing agent runtime with explicit state handling and missing-credential prompts.
metadata:
  source: skills/05-code/conversational-agent-session-integration.md
  category: 05-code
  version: "v1"
---

# Conversational Agent Session Integration

## Description
Integrate conversational agent sessions into an existing agent runtime with explicit state handling and missing-credential prompts. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A framework's conversational sessions must be integrated without duplicating session state.
- Missing API credentials must be prompted and validated at session start, not at first failure.
- Session semantics must be verified against the runtime's existing state model.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The framework session API, the runtime's state model, and the credential prompt policy. |
| Outputs | An integration report naming the session state mapping, credential validation results, and verified session transitions. |
| Safety | Fail closed by refusing session start when a required credential cannot be validated. |

## Procedure
1. Map the framework's session model onto the runtime's existing state.
2. Intercept session start to prompt for missing credentials when required.
3. Validate provided credentials before admitting the session.
4. Exercise session transitions such as open, continue, and end against the mapping.
5. Record error classes when session operations fail, not just exit codes.
6. Emit the integration report with the state mapping and validation results.

## Outputs
| Area | Contract |
|---|---|
| Primary | An integration report naming the session state mapping, credential validation results, and verified session transitions. |
| Verification | Session transition traces and credential checks that reproduce the mapping. |
| Failure | A fail-closed abort naming the invalid credential or unmapped session transition. |

## Runnable Example
```python
def start_session(config, creds, required):
    missing = [k for k in required if k not in creds]
    if missing:
        return {"started": False, "prompt_for": missing}
    if config.get("session_mode") == "stateless" and config.get("state_store"):
        return {"started": False, "reason": "duplicate_state"}
    return {"started": True, "mode": config.get("session_mode", "stateless")}

assert start_session({"session_mode": "stateless"}, {"k": "v"}, ["k"])["started"] is True
r = start_session({"session_mode": "stateless"}, {}, ["k"])
assert r["started"] is False and r["prompt_for"] == ["k"]
assert start_session({"session_mode": "stateful", "state_store": "x"}, {"k": "v"}, ["k"])["reason"] == "duplicate_state"
```

## Failure Modes
- Session state is duplicated between the framework and the runtime.
- Credentials are prompted only after the first tool call fails.
- Error classes are swallowed, so session failures look like task failures.
- Session transitions are exercised only for the happy path.
- Prompted credentials are stored unvalidated for later runs.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- CrewAI's release adds experimental conversational agent sessions, prompting for a missing API key when a run starts and recording the error class when a run cannot proceed (olud.ai daily, November 6, 2026) ([public signal](https://olud.ai/news/2026-11-06.html))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Ag Ui Frontend Agent Binding Generation](ag-ui-frontend-agent-binding-generation.md)
- [Agent Client Protocol Integration Implementation](agent-client-protocol-integration-implementation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |

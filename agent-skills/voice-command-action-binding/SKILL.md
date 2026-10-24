---
name: voice-command-action-binding
description: Bind parsed voice-command intents to executable actions with explicit argument checks and a confirmation gate before execution.
metadata:
  source: skills/04-action-execution/voice-command-action-binding.md
  category: 04-action-execution
  version: "v1"
---
# Voice Command Action Binding

## Description
Bind parsed voice-command intents to executable actions with explicit argument checks and a confirmation gate before execution. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A voice-driven agent must convert a parsed command into a concrete action without executing anything unconfirmed.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Resolve each parsed intent to its declared action, validate the argument against the action contract, and hold execution until the confirmation gate is satisfied.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def bind_action(parsed, actions):
    action = actions.get(parsed["intent"])
    if action is None:
        raise ValueError("no action bound for intent: " + parsed["intent"])
    if parsed["confidence"] < action["min_confidence"]:
        return {"status": "needs_confirmation", "action": action["name"]}
    return {"status": "ready", "action": action["name"], "arg": parsed["arg"]}

actions = {"run_tests": {"name": "pytest", "min_confidence": 0.8}}
assert bind_action({"intent": "run_tests", "arg": "", "confidence": 0.9}, actions)["status"] == "ready"
assert bind_action({"intent": "run_tests", "arg": "", "confidence": 0.6}, actions)["status"] == "needs_confirmation"
```

## Failure Modes
- The argument is passed to the action without contract validation.
- Low-confidence bindings execute because the gate defaults to auto-approve.
- Intent names are matched loosely so the wrong action binds.
- Confirmation is recorded as granted without an actual user response.
- Unbound intents fall through to a fallback action instead of failing.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The OpenAI Codex CLI 0.163 release adds voice control to a coding agent, making the voice-intent to action binding the execution boundary (trendintech.com, dated October 2026) ([public signal](https://trendintech.com/openai-codex-cli-0-163-voice-control-2026/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Dry Run Execution](../04-action-execution/dry-run-execution.md)
- [Human Approval Gate Implementation](../04-action-execution/human-approval-gate-implementation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

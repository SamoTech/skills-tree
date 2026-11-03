---
name: piped-permission-prompt-delegation
description: ""
metadata:
  source: skills/09-agentic-patterns/piped-permission-prompt-delegation.md
  category: 09-agentic-patterns
  version: "v1"
---

# Piped Permission Prompt Delegation

## Description
Delegate agent permission prompts to a hosting application through a piped protocol so the host answers approvals with an explicit recorded policy. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent runs embedded inside a host application and permission prompts must be answered by the host's policy rather than a human watching a terminal.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the agent permission prompt stream, the host policy, and the piped response contract. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Enable the piped permission mode and confirm the agent stops prompting on the terminal.
2. Define the host policy mapping each prompt class to allow, deny, or escalate to a human.
3. Answer each piped prompt through the contract and record the prompt, decision, and rule applied.
4. Verify every prompt received a response and none timed out into a default allow.
5. On an unmapped prompt class, deny by default and record the escalation.
6. Emit a structured result with the prompt log, decisions, and policy version.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def answer_prompt(prompt, policy):
    rule = policy.get(prompt["class"], "deny")
    return {"decision": rule, "prompt": prompt["class"]}
policy = {"file_read": "allow", "net_post": "deny"}
assert answer_prompt({"class": "file_read"}, policy)["decision"] == "allow"
assert answer_prompt({"class": "net_post"}, policy)["decision"] == "deny"
assert answer_prompt({"class": "shell_exec"}, policy)["decision"] == "deny"
```

## Failure Modes
- The pipe is enabled but a terminal prompt path still exists and silently answers some prompts.
- Unmapped prompt classes default to allow instead of deny.
- Prompt responses are not logged, so no one can audit which rule fired.
- The host policy is edited while a run is active and decisions mix two versions.
- A prompt timeout is treated as approval rather than a failure to decide.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Crush 0.99.0 letting an app that hosts it answer its permission prompts with CRUSH_PERMISSIONS_PIPED=1 (Munder Difflin agent-tools daily, dated November 1, 2026) ([public signal](https://munderdiffl.in/blog/agent-tools-today-2026-11-01/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Tool Selection Competing Interest Disclosure](tool-selection-competing-interest-disclosure.md)
- [Full Run Lifecycle Hook Instrumentation](full-run-lifecycle-hook-instrumentation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |

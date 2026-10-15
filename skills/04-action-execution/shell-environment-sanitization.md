---
title: "Shell Environment Sanitization"
category: 04-action-execution
level: advanced
stability: experimental
description: "Run child shells with an allowlisted environment that drops hook and preload variables, and re-sanitize per target shell instead of reusing one sanitized map."
added: "2026-10"
version: v1
related: [shell-command, env-vars]
tags: [shell, environment, injection]
---
# Shell Environment Sanitization

## Description
Run child shells with an allowlisted environment that drops hook and preload variables, and re-sanitize per target shell instead of reusing one sanitized map. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A child shell must run without inheriting injection-prone environment variables.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | shell environment sanitization task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the shell environment sanitization steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A sanitized environment allowlist with the dropped variables and the injection vectors they enabled. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def sanitize(env, drop=("LD_PRELOAD", "BASH_ENV", "PROMPT_COMMAND")):
    return {k: v for k, v in env.items() if k not in drop}
env = {"PATH": "/usr/bin", "BASH_ENV": "/tmp/x"}
assert sanitize(env) == {"PATH": "/usr/bin"}
```

## Failure Modes
- Acting outside the declared task boundary.
- Passing the whole parent environment to a child shell including hook variables.
- Reusing sanitized output across different shells with different load mechanisms.
- Retrying without preserving state or evidence.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Shell environment injection hardening recurs in 2026 coding-agent issue threads. ([public signal](https://github.com/anthropics/claude-code/issues/75376))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [shell command](../04-action-execution/shell-command.md)
- [env vars](../04-action-execution/env-vars.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

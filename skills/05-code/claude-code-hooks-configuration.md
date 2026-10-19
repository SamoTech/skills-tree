---
title: "Claude Code Hooks Configuration"
category: 05-code
level: advanced
stability: experimental
description: "Configure coding-agent lifecycle hooks such as pre-action checks, post-action formatters, and stop conditions so the harness enforces repo policy automatically."
added: "2026-10"
version: v1
related: [system-prompt-refactoring, ide-integration]
tags: [harness, hooks, policy]
---
# Claude Code Hooks Configuration

## Description
Configure coding-agent lifecycle hooks such as pre-action checks, post-action formatters, and stop conditions so the harness enforces repo policy automatically. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent must wire harness hooks that enforce repo policy at defined lifecycle points.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | claude code hooks configuration task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the claude code hooks configuration steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A hooks configuration with lifecycle event, matcher, command, and recorded enforcement result. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def hook_allows(event, cmd_exit):
    return event == "PreToolUse" and cmd_exit == 0
assert hook_allows("PreToolUse", 0) is True
assert hook_allows("PreToolUse", 2) is False
```

## Failure Modes
- Acting outside the declared task boundary.
- Blocking hooks that fail closed with no documented fallback for policy exceptions.
- Hooks that print diagnostics but never affect the decision.
- Hook scripts that assume a working directory the harness does not guarantee.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Agent-framework comparisons document lifecycle hooks as first-class coding-agent configuration. ([public signal](https://shakudo.io/blog/top-9-ai-agent-frameworks))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [System Prompt Refactoring](../05-code/system-prompt-refactoring.md)
- [Ide Integration](../05-code/ide-integration.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

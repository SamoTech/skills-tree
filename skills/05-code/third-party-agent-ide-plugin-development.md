---
title: "Third Party Agent Ide Plugin Development"
category: 05-code
level: advanced
stability: experimental
description: "Develop CLI plugins that expose IDE capabilities to third-party coding agents so that agent sessions use native tooling instead of screen scraping."
added: "2026-10"
version: v1
related: [agent-client-protocol-integration-implementation, tool-review-loops]
tags: [cli, plugins, ide, agents]
---
# Third Party Agent Ide Plugin Development

## Description
Develop CLI plugins that expose IDE capabilities to third-party coding agents so that agent sessions use native tooling instead of screen scraping. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A team builds a CLI plugin so an external coding agent can drive IDE features directly.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Map each IDE capability the plugin exposes to its native API, implement the CLI surface against the declared contract, and test every command against a stub IDE before release.
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
def cmd(name, args):
    table = {"preview": lambda a: "render:" + a[0], "logcat": lambda a: "tail:" + a[0]}
    if name not in table:
        raise ValueError("unknown command: " + name)
    return table[name](args)
assert cmd("preview", ["Home.kt"]) == "render:Home.kt"
try:
    cmd("shell", ["x"]); assert False
except ValueError:
    pass
```

## Failure Modes
- A command shells out to the IDE UI instead of the native API and breaks on theme changes.
- Plugin commands default to permissive behavior when argument validation fails.
- IDE API versions are not pinned and plugin updates silently change semantics.
- Errors are swallowed and the agent receives empty success output.
- The plugin bypasses the protocol layer and talks to internal IDE state directly.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the Android Dev Summit introduced dedicated Android CLI plugins for Claude Code and Codex inside the BYOA architecture (blog.luandnh.com, dated October 29, 2026) ([public signal](https://blog.luandnh.com/en/ai-daily/2026-10-29/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Client Protocol Integration Implementation](agent-client-protocol-integration-implementation.md)
- [Tool Review Loops](../07-tool-use/tool-review-loops.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

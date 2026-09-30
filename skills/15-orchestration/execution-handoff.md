---
title: "Execution Handoff"
category: 15-orchestration
level: advanced
stability: stable
description: "Execute repository work under the established governance model and leave a complete continuation packet."
added: "2026-09"
related:
  - repository-state-load
  - evidence-verification
  - documentation-drift-resolution
---

# Execution Handoff

## Description

Carry work from verified intake through bounded execution, validation, documentation synchronization, and a continuation-ready handoff. A handoff must preserve enough evidence for another agent to continue without reconstructing hidden context.

1. Load authoritative state before execution.
2. Convert the objective into a bounded execution plan.
3. Inspect before changing and preserve existing functionality.
4. Escalate strategic, destructive, breaking, or high-impact decisions.
5. Execute specialist work within scope.
6. Validate implementation, security, CI, and documentation.
7. Synchronize current state and decisions when material state changes.
8. Before closing, preserve objective, decision source, files, tests, evidence, risks, remaining work, documentation updates, and next action.

## Runnable example

```bash
git status --short
git diff --check
git log -5 --oneline
```

## Inputs / outputs / failure modes

| Input | Output | Failure mode |
|---|---|---|
| Objective and constraints | Bounded work plan | Scope expands without authority |
| Repository state | Safe execution context | Baseline is stale |
| Implementation changes | Verified result | Existing behavior is unintentionally broken |
| CI/security evidence | Completion state | Gates remain unresolved |
| Current state and decisions | Continuation packet | Handoff omits material context |

## Related

- `repository-state-load.md`
- `evidence-verification.md`
- `documentation-drift-resolution.md`

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- meta/AGENT_OPERATING_MODEL.md
- meta/AGENT_HANDOFF_PROTOCOL.md

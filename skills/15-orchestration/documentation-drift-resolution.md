---
title: "Documentation Drift Resolution"
category: 15-orchestration
level: advanced
stability: stable
description: "Detect, reconcile, and document drift between implementation and authoritative repository documentation."
added: "2026-09"
related:
  - repository-state-load
  - evidence-verification
  - execution-handoff
---

# Documentation Drift Resolution

## Description

Reconcile implementation state with the repository's authoritative documentation without inventing history or silently changing strategic decisions. Documentation is updated only from verified implementation and decision evidence.

1. Identify the authoritative document for the affected concern.
2. Inspect live implementation and verification evidence.
3. Classify the mismatch as stale documentation, stale implementation, or unresolved strategic conflict.
4. Correct authoritative documentation to verified state when the decision is already established.
5. Record historically significant changes in the decision log.
6. Update only the relevant current-state, roadmap, architecture, security, testing, or deployment documents.
7. Do not declare completion until the documentation gate passes.

## Runnable example

```bash
git diff -- meta/CURRENT-STATE.md meta/memory/DECISIONS.md
git status --short
git log -1 --oneline
```

## Inputs / outputs / failure modes

| Input | Output | Failure mode |
|---|---|---|
| Live implementation | Verified current state | Implementation evidence is incomplete |
| Authoritative docs | Corrected documentation | Wrong document is treated as authoritative |
| Decisions | Historical continuity | Strategic conflict is silently resolved |
| CI/test evidence | Completion evidence | Documentation claims exceed verification |

## Failure modes

- Creating duplicate status documents.
- Copying historical metrics into current state.
- Calling documentation complete without CI or repository verification.
- Silently resolving a strategic conflict that requires CEO/CIO authority.

## Related

- `repository-state-load.md`
- `evidence-verification.md`
- `execution-handoff.md`

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- meta/CURRENT-STATE.md
- meta/memory/DECISIONS.md

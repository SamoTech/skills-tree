---
name: documentation-drift-resolution
description: Detect, reconcile, and document drift between implementation and authoritative repository documentation.
license: MIT
metadata:
  source: skills/15-orchestration/documentation-drift-resolution.md
  version: "v1"
---

# Documentation Drift Resolution

1. Identify the authoritative document for the affected concern.
2. Inspect live implementation and verification evidence.
3. Classify the mismatch as stale documentation, stale implementation, or unresolved strategic conflict.
4. Correct authoritative documentation to verified state when the decision is already established.
5. Record historically significant changes in the decision log.
6. Update only the relevant current-state, roadmap, architecture, security, testing, or deployment documents.
7. Do not declare completion until the documentation gate passes.

## Failure modes

- Creating duplicate status documents.
- Copying historical metrics into current state.
- Calling documentation complete without CI or repository verification.
- Silently resolving a strategic conflict that requires CEO/CIO authority.

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- meta/CURRENT-STATE.md
- meta/memory/DECISIONS.md

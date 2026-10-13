---
title: "Dead Code Elimination Verification"
category: 05-code
level: advanced
stability: experimental
description: "Verify that code flagged as unused is truly unreferenced across reflection and dynamic dispatch before deletion."
added: "2026-10"
version: v1
related: [static-analysis, refactoring, code-search]
tags: [dead-code, verification, hygiene]
---

# Dead Code Elimination Verification

## Description
Verify that code flagged as unused is truly unreferenced across reflection and dynamic dispatch before deletion. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- static analysis flags code as unused and deletion must be proven safe first.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for dead code elimination verification work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the dead code elimination verification steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def verify(references, candidate, dynamic_paths):
    if candidate in references:
        return "referenced"
    if any(candidate in p for p in dynamic_paths):
        return "dynamic-possible"
    return "safe-delete"

refs = {"a", "b"}
assert verify(refs, "a", []) == "referenced"
assert verify(refs, "c", ["call:c:late"]) == "dynamic-possible"
assert verify(refs, "d", []) == "safe-delete"
```

## Failure Modes
- Deleting on a single tool recommendation.
- Ignoring string-based dynamic lookups.
- Deleting public API surface without a deprecation window.
- Not searching generated code and configs for references.
- No revert plan when a hidden caller appears.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Safe dead-code removal is a recurring 2026 codebase hygiene request in public developer discussion; this is a dated signal, not an adoption metric.

## Related
- static-analysis.md
- refactoring.md
- code-search.md

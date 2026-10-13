---
name: type-error-triage
description: Classify static type errors by root cause and fix order so large type-error backlogs shrink by cause rather than by file.
metadata:
  source: skills/05-code/type-error-triage.md
  category: 05-code
  version: "v1"
---

# Type Error Triage

## Description
Classify static type errors by root cause and fix order so large type-error backlogs shrink by cause rather than by file. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a codebase accumulates hundreds of static type errors and they must be grouped by cause before fixing.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for type error triage work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the type error triage steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def triage(errors):
    groups = {}
    for e in errors:
        cause = e.split(":")[0]
        groups.setdefault(cause, []).append(e)
    return sorted(groups.items(), key=lambda kv: -len(kv[1]))

errors = ["import:a", "import:b", "none:c"]
g = triage(errors)
assert g[0][0] == "import" and len(g[0][1]) == 2
```

## Failure Modes
- Fixing errors in file order instead of by cause.
- Disabling strictness to clear the backlog.
- Type-ignore lines without an explanatory reason.
- Fixing symptoms without reading the root cause.
- No measurement of the backlog after each pass.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Large type-error backlogs are a recurring 2026 migration pain point in public developer discussion; this is a dated signal, not an adoption metric.

## Related
- static-analysis.md
- debugging.md
- type-annotation-generation.md

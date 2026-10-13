---
name: system-prompt-refactoring
description: Refactor system prompts with behavior-preserving edits and regression checks so prompt changes do not silently alter outputs.
metadata:
  source: skills/05-code/system-prompt-refactoring.md
  category: 05-code
  version: "v1"
---

# System Prompt Refactoring

## Description
Refactor system prompts with behavior-preserving edits and regression checks so prompt changes do not silently alter outputs. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a long system prompt must be restructured without changing agent behavior.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for system prompt refactoring work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the system prompt refactoring steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def regression(old_outputs, new_outputs):
    if len(old_outputs) != len(new_outputs):
        return "length-mismatch"
    changed = [i for i, (a, b) in enumerate(zip(old_outputs, new_outputs)) if a != b]
    return changed

old = ["a", "b", "c"]
assert regression(old, old) == []
assert regression(old, ["a", "x", "c"]) == [1]
```

## Failure Modes
- Rewriting the prompt with no recorded before outputs.
- Reformatting sections that change precedence order.
- Deleting constraints while moving text around.
- Running regression on a different model than production.
- Merging prompt changes with no diff review.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Prompt regression testing is a documented 2026 practice as teams treat prompts as code in public coverage; this is a dated signal, not an adoption metric.

## Related
- code-review.md
- requirement-tracing.md
- documentation-generation.md

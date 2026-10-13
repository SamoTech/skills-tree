---
title: "Context Engineering"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Assemble and prune model context deliberately by selecting, ordering, and budgeting content instead of stuffing every available input."
added: "2026-10"
version: v1
related: [prompt-caching, memory-augmented, bounded-exploration]
tags: [context, token-budget, llm]
---

# Context Engineering

## Description
Assemble and prune model context deliberately by selecting, ordering, and budgeting content instead of stuffing every available input. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- the task outcome depends on what fits in a bounded context window and on the ordering of high-value content.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for context engineering work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the context engineering steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def pack_context(items, budget):
    packed, used = [], 0
    for name, size in sorted(items, key=lambda x: -x[1]):
        if used + size <= budget:
            packed.append(name)
            used += size
    return packed, used

items = [('system', 30), ('tools', 45), ('history', 60), ('docs', 80)]
packed, used = pack_context(items, 120)
assert used <= 120 and set(packed) <= set(i[0] for i in items)
print(packed, used)
```

## Failure Modes
- Stuffing context without measuring content cost.
- Pruning information that later turns out to be required.
- Assuming a model reports its own context limits accurately.
- Mixing private data into shared context without a policy check.
- Never recording which context variant produced a result.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Context-window budgeting and selective retrieval are treated as a first-class 2026 discipline in agent-framework discussions; this is a dated signal, not an adoption metric.

## Related
- prompt-caching.md
- memory-augmented.md
- bounded-exploration.md

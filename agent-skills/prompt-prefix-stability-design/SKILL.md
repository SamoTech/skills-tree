---
name: prompt-prefix-stability-design
description: Design prompts so a stable prefix is cached and versioned separately from variable content, with regression checks when the prefix changes.
metadata:
  source: skills/09-agentic-patterns/prompt-prefix-stability-design.md
  category: 09-agentic-patterns
  version: "v1"
---

# Prompt Prefix Stability Design

## Description
Design prompts so a stable prefix is cached and versioned separately from variable content, with regression checks when the prefix changes. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- prompt caching or regression control depends on a stable prefix across many requests.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for prompt prefix stability design work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the prompt prefix stability design steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def split_prompt(prefix, payload):
    if payload in prefix:
        raise ValueError('volatile payload leaked into cached prefix')
    return prefix + ' | ' + payload

prefix = 'You are a careful agent.'
p = split_prompt(prefix, 'Input: query-42')
assert p.startswith(prefix + ' | ')
print('prefix isolated')
```

## Failure Modes
- Embedding volatile data inside the cached prefix.
- Changing the prefix without versioning or regression checks.
- Assuming prompt caching without verifying cache hits.
- Merging unrelated edits into one prefix change.
- No rollback when a prefix change degrades output quality.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Prompt-prefix caching economics and prompt-as-code versioning recur across 2026 LLM cost-engineering requests; this is a dated signal, not an adoption metric.

## Related
- prompt-caching.md
- prompt-version-control.md
- agent-cost-accounting.md

---
title: "Style-Reference Image Generation"
category: 08-multimodal
level: basic
stability: experimental
description: "Generate images that follow a reference style while respecting subject, composition, and licensing constraints, and check outputs against the stated constraints."
added: "2026-10"
version: v1
related: [image-generation, image-editing, image-gen-prompt]
tags: [style, reference, image, generation, multimodal]
---

# Style-Reference Image Generation

## Description
Generate images that follow a reference style while respecting subject, composition, and licensing constraints, and check outputs against the stated constraints. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- The task has explicit constraints such as time, budget, or safety that must gate the outcome.
- A silent failure mode exists that must be surfaced rather than swallowed.
- Verification evidence is required before the result is trusted.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for style-reference image generation. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the style-reference image generation procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Style-Reference Image Generation: deterministic check
seen = {}
conflicts = []
for item in [{"k": "a", "v": 1}, {"k": "a", "v": 2}, {"k": "b", "v": 3}]:
    if item["k"] in seen and seen[item["k"]] != item["v"]:
        conflicts.append(item["k"])
    seen[item["k"]] = item["v"]
assert conflicts == ["a"]
print("conflicts:", conflicts)
```

## Failure Modes
- Proceeding with style-reference image generation without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Consistent-style image generation recurs in 2026 creative workflows; constraint checking is a named gap. These are dated public signals, not adoption metrics.

## Related
- image-generation.md
- image-editing.md
- image-gen-prompt.md

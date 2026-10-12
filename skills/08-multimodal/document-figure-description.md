---
title: "Document Figure Description"
category: 08-multimodal
level: intermediate
stability: experimental
description: "Produce accurate, accessible descriptions of figures, charts, and diagrams in documents, including axes, trends, and notable outliers."
added: "2026-10"
version: v1
related: [chart-reading, image-captioning, chart-generation]
tags: [document, figure, description, multimodal]
---

# Document Figure Description

## Description
Produce accurate, accessible descriptions of figures, charts, and diagrams in documents, including axes, trends, and notable outliers. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires document figure description before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for document figure description. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the document figure description steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# Document Figure Description: deterministic check
options = [{"name": "x", "gain": 5, "cost": 1}, {"name": "y", "gain": 4, "cost": 1}]
ranked = sorted(options, key=lambda o: (o["cost"], -o["gain"]))
assert ranked[0]["name"] == "x"
print("best:", ranked[0]["name"])
```

## Failure Modes
- Acting outside the declared task boundary.
- Assuming an estimate or preview equals the verified effect.
- Retrying without preserving state or evidence.
- Using stale inputs as if they were current.
- Reporting success without checking the resulting state.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Accessibility requirements in 2026 documentation include figure descriptions; WCAG guidance is a public standard. These are dated public signals, not adoption metrics.

## Related
- chart-reading.md
- image-captioning.md
- chart-generation.md

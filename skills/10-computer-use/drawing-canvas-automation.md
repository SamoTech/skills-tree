---
title: "Drawing Canvas Automation"
category: 10-computer-use
level: advanced
stability: experimental
description: "Automate interactions with drawing and design canvas applications using coordinate anchors and object-tree verification instead of pixel guessing."
added: "2026-10"
version: v1
related: [mouse-move, drag-drop, visual-element-detection]
tags: [canvas, design-tools, ui-automation]
---

# Drawing Canvas Automation

## Description
Automate interactions with drawing and design canvas applications using coordinate anchors and object-tree verification instead of pixel guessing. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a design or drawing canvas must be driven reliably across zoom and scroll states.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for drawing canvas automation work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the drawing canvas automation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def anchor(point, bounds):
    x, y = point
    (x0, y0), (x1, y1) = bounds
    return x0 <= x <= x1 and y0 <= y <= y1

assert anchor((50, 60), ((0, 0), (100, 100)))
assert not anchor((150, 60), ((0, 0), (100, 100)))
```

## Failure Modes
- Clicking raw screen pixels without anchoring to canvas objects.
- Ignoring zoom and scroll offsets in coordinates.
- Assuming canvas state after a drag without verification.
- Losing work because undo history was never captured.
- Treating a rendered artifact as saved without checking the file.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Canvas and design-tool automation requests recur in 2026 desktop-agent discussions; this is a dated signal, not an adoption metric.

## Related
- mouse-move.md
- drag-drop.md
- visual-element-detection.md

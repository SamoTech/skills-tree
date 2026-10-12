---
title: "Point Cloud Reading"
category: 01-perception
level: intermediate
stability: experimental
description: "Parse 3D point-cloud captures into structured scene descriptions with downsampling, coordinate frames, and provenance so reasoning skills can operate on spatial data."
added: "2026-10"
version: v1
related: [depth-estimation, geospatial-reading, 3d-scene-understanding]
tags: [point, cloud, reading, perception]
---
# Point Cloud Reading

## Description
Parse 3D point-cloud captures into structured scene descriptions with downsampling, coordinate frames, and provenance so reasoning skills can operate on spatial data. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires point cloud reading before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for point cloud reading. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the point cloud reading steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# Point Cloud Reading: deterministic check
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
- Acting outside the declared task boundary.
- Assuming an estimate or preview equals the verified effect.
- Retrying without preserving state or evidence.
- Using stale inputs as if they were current.
- Reporting success without checking the resulting state.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Embodied and spatial-agent research in 2026 publishes point-cloud front ends; robotics agent stacks request structured 3D perception outputs. These are dated public signals, not adoption metrics.

## Related
- depth-estimation.md
- geospatial-reading.md
- 3d-scene-understanding.md

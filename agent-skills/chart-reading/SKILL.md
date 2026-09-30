---
name: chart-reading
description: Extract chart structure, values, axes, units, series, and trends from visualizations. Use when important data is encoded in a chart image or dashboard graphic.
license: MIT
metadata:
  source: skills/01-perception/chart-reading.md
  version: "v2"
---

# Chart Reading

1. Identify chart type, title, axes, units, legend, and scale.
2. Extract only values that are visually supported; preserve approximate values as approximate.
3. Separate observed values from inferred trends.
4. Return structured series data when requested.
5. Flag unreadable labels, occlusion, low resolution, logarithmic axes, and truncated axes.
6. Never invent missing data points.

## Failure modes

- Low resolution: request a higher-resolution source or mark values uncertain.
- Truncated or logarithmic axes: report the scale before interpreting magnitude.
- Visual inference mistaken for measurement: distinguish exact labels from estimated positions.

## Evidence

- https://docs.anthropic.com/en/docs/build-with-claude/vision
- https://agentskills.io/specification

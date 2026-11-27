---
title: "Data Visualization"
category: 12-data
level: advanced
stability: stable
version: v2
description: "Create data visualizations from pre-aggregated values with declared axes, units, and plotted-to-source verification."
added: "2025-03"
related: [data-aggregation, data-summarization, funnel-analysis]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-data-visualization.json)

# Data Visualization

**Category:** `data`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Create data visualizations from pre-aggregated values with declared axes, units, and plotted-to-source verification. The data step is contract-first: validate the input contract before transforming, and verify the output against explicit expectations rather than trusting the pipeline.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | aggregates | list of object | Pre-aggregated values with their labels and units |
| Input | chart_spec | object | Chart type, axes, units, and sorting |
| Output | chart | object | A rendered specification mapping values to visual channels |
| Output | data_check | object | Confirmation that plotted values match the aggregates |

### Procedure
1. Aggregate before plotting; never render raw row-level data.
2. Choose the chart type from the comparison being made, not decoration.
3. Declare axes, units, and sorting before rendering.
4. Start quantitative axes at zero for bar charts or disclose truncation.
5. Verify plotted values match the aggregates one-to-one.

### Example

```python
agg = [{'label': 'east', 'sales': 15}, {'label': 'west', 'sales': 7}]
chart_spec = {'type': 'bar', 'x': 'label', 'y': 'sales', 'baseline_zero': True}
plotted = {a['label']: a['sales'] for a in agg}
assert all(v >= 0 for v in plotted.values()) and chart_spec['baseline_zero']
assert plotted == {'east': 15, 'west': 7}
print({'plotted': plotted, 'max': max(plotted.values())})
```

### Related Skills

- [Data Aggregation](data-aggregation.md) - prepare aggregates to plot
- [Data Summarization](data-summarization.md) - summarize before visualizing
- [Funnel Analysis](funnel-analysis.md) - visualize stage conversion

## Failure Modes

- Truncated axes exaggerating differences without disclosure.
- Plotting raw rows instead of aggregates, producing noise.
- Mismatched units across series on one axis.
- A chart type hiding the comparison the reader needs.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing pipeline's documentation; no benchmark claim is made without reproducible evidence.

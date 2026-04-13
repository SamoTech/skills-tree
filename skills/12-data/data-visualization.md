---
title: "Data Visualization"
category: 12-data
level: intermediate
stability: stable
description: "Apply data visualization in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-data-visualization.json)

# Data Visualization

**Category:** `data`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Generate charts, graphs, and dashboards from structured data to communicate insights visually.

### Example

```python
import plotly.express as px
fig = px.bar(df, x='month', y='revenue', color='region', title='Monthly Revenue')
fig.write_html('chart.html')
```

### Frameworks

- Python `plotly`, `matplotlib`, `seaborn`
- JavaScript Chart.js, D3.js, Recharts
- OpenAI Code Interpreter (auto-generates charts)

### Related Skills

- [Data Aggregation](data-aggregation.md)
- [Statistical Analysis](statistical-analysis.md)

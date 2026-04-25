---
title: "Data Visualization"
category: 12-data
level: basic
stability: stable
added: "2025-03"
description: "Apply data visualization in AI agent workflows."
dependencies:
  - package: plotly
    min_version: "5.0.0"
    tested_version: "6.7.0"
    confidence: verified
  - package: pandas
    min_version: "2.0.0"
    tested_version: "3.0.2"
    confidence: verified
code_blocks:
  - id: "example-viz"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-data-visualization.json)

# Data Visualization

**Category:** `data`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Generate interactive charts and static plots from structured data for agent-generated reports and dashboards.

### Example

```python
# pip install plotly pandas
import plotly.express as px
import pandas as pd

df = pd.read_csv("sales.csv")

# Bar chart
fig = px.bar(df, x="month", y="revenue", title="Monthly Revenue",
             color="region", barmode="group")
fig.write_html("revenue_chart.html")
fig.write_image("revenue_chart.png")  # requires kaleido

# Line chart with confidence band
fig2 = px.line(df, x="date", y="value", color="metric",
               title="Metrics Over Time")
fig2.show()
```

### Related Skills
- `csv-processing`, `pandas-operations`, `statistical-analysis`, `time-series`

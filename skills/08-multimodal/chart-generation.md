---
title: "Chart Generation"
category: 08-multimodal
level: intermediate
stability: stable
description: "Apply chart and diagram generation in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-08-multimodal-chart-generation.json)

# Chart / Diagram Generation

**Category:** `multimodal`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Generate charts, graphs, and diagrams from structured data or natural language descriptions. Produces publication-quality static images (PNG/SVG) or interactive HTML visualizations for reports, dashboards, and presentations.

### Example

```python
import matplotlib.pyplot as plt
import io, base64

def generate_bar_chart(labels, values, title):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(labels, values, color='steelblue')
    ax.set_title(title)
    ax.set_ylabel('Value')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()

chart_b64 = generate_bar_chart(
    ['Q1', 'Q2', 'Q3', 'Q4'],
    [120, 145, 132, 178],
    'Quarterly Revenue'
)
```

### LLM-Driven Code Generation

```python
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
    model='gpt-4o',
    messages=[{'role': 'user', 'content': """
        Generate Python matplotlib code for a line chart showing:
        Months: Jan, Feb, Mar, Apr, May
        Values: 30, 45, 28, 60, 52
        Title: Monthly Active Users
        Save as 'chart.png'
    """}]
)
code = response.choices[0].message.content
exec(code)  # run generated chart code
```

### Frameworks / Models

- Matplotlib / Seaborn (static PNG/SVG)
- Plotly (interactive HTML)
- Vega-Altair (declarative grammar)
- Mermaid.js (flowcharts, sequence diagrams)
- GPT-4o code generation → exec pipeline

### Related Skills

- [Data Visualization](../12-data/data-visualization.md)
- [Chart/Graph Reading](../01-perception/chart-reading.md)
- [Image Generation](image-generation.md)

# Data Visualization

**Category:** `data`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

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

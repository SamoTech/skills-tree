---
title: "Chart Reading"
category: 01-perception
level: intermediate
stability: stable
description: "Apply chart reading in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-chart-reading.json)

# Chart Reading

**Category:** `perception`  
**Skill Level:** `intermediate`  
**Stability:** `stable`  
**Added:** 2025-03  
**Last Updated:** 2026-04

---

## Description

Interpret charts, graphs, and data visualizations from images to extract numerical values, trends, comparisons, and patterns. Supports bar charts, line charts, pie charts, scatter plots, histograms, heatmaps, and dashboards. The model reads axis labels, legends, titles, and data points — returning structured JSON, markdown tables, or natural-language summaries.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `image` | `bytes` / `url` | ✅ | Chart image (PNG, JPEG, WebP) or public URL |
| `output_format` | `string` | ❌ | `json` (default), `markdown`, or `prose` |
| `context` | `string` | ❌ | Domain hint, e.g. `"financial quarterly report"` |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `chart_type` | `string` | Detected chart type |
| `series` | `list` | Data series with labels and values |
| `key_insight` | `string` | One-sentence summary of the main trend |

---

## Example

```python
import anthropic
import base64
from pathlib import Path

client = anthropic.Anthropic()

def read_chart(image_path: str) -> str:
    """Extract structured data from a chart image."""
    image_data = base64.standard_b64encode(
        Path(image_path).read_bytes()
    ).decode("utf-8")

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data,
                    },
                },
                {
                    "type": "text",
                    "text": (
                        "Analyze this chart and return a JSON object with:\n"
                        "- chart_type: type of chart\n"
                        "- title: chart title if present\n"
                        "- x_axis: {label, values}\n"
                        "- y_axis: {label, unit}\n"
                        "- series: [{name, values}]\n"
                        "- key_insight: one-sentence trend summary\n"
                        "Return ONLY valid JSON."
                    )
                }
            ],
        }]
    )
    return response.content[0].text

result = read_chart("quarterly_revenue.png")
print(result)
```

```python
# URL-hosted chart
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "url", "url": "https://example.com/chart.png"}},
            {"type": "text", "text": "Extract all data series as JSON."}
        ]
    }]
)
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| Claude claude-opus-4-5 | Native vision via `image` content block | 2024-06 |
| GPT-4o | Vision via `image_url` content block | 2024-05 |
| LangChain | `ChatAnthropic` + base64 image message | v0.2 |

---

## Notes

- For URL-hosted charts use `{"type": "url", "url": chart_url}` instead of base64
- Pass `"Return ONLY valid JSON"` to suppress prose wrapping
- Low-resolution or heavily compressed images reduce accuracy; request 1x–2x renders
- For dashboards with multiple charts, crop each chart individually before passing

---

## Related Skills

- [Image Understanding](image-understanding.md) — foundation vision skill
- [OCR](ocr.md) — when axis labels are the primary target
- [Document Parsing](document-parsing.md) — for charts embedded in reports
- [Structured Data Reading](structured-data-reading.md) — post-extraction processing

---

## Changelog

| Date | Change |
|---|---|
| `2026-04` | Expanded from stub: full description, inputs/outputs table, two code examples, notes |
| `2025-03` | Initial stub entry |

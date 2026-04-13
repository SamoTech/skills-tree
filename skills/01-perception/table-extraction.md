---
title: "Table Extraction"
category: 01-perception
level: intermediate
stability: stable
description: "Apply table extraction in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-table-extraction.json)

# Table Extraction
Category: perception | Level: intermediate | Stability: stable | Version: v1

## Description
Detect and extract tabular data from documents, images, and web pages into structured formats (CSV, JSON, DataFrame).

## Inputs
- `source`: file path, URL, or base64 image
- `output_format`: `json` | `csv` | `dataframe`

## Outputs
- List of tables, each as a 2D array with headers

## Example
```python
import anthropic, base64, json
client = anthropic.Anthropic()
with open("report.pdf", "rb") as f:
    data = base64.b64encode(f.read()).decode()
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=2048,
    messages=[{"role": "user", "content": [
        {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": data}},
        {"type": "text", "text": "Extract all tables as JSON arrays with headers as keys."}
    ]}]
)
tables = json.loads(response.content[0].text)
```

## Frameworks
| Framework | Method |
|---|---|
| LangChain | `UnstructuredTableTransformer` |
| LlamaIndex | `TableReader` |
| Raw API | Vision + structured output prompt |

## Failure Modes
- Merged cells break column alignment
- Rotated tables in scanned PDFs
- Borderless tables confused with plain text

## Related
- `pdf-parsing.md` · `structured-data-reading.md` · `ocr.md`

## Changelog
- v1 (2026-04): Initial entry

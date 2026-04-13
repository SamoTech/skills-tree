![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-csv-processing.json)

# CSV Processing

**Category:** `data`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Read, parse, and transform CSV files into structured data for downstream processing or analysis.

### Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `file_path` | `string` | ✅ | Path or URL to the CSV file |
| `delimiter` | `string` | ❌ | Column delimiter (default: `,`) |
| `encoding` | `string` | ❌ | File encoding (default: `utf-8`) |

### Outputs

| Output | Type | Description |
|---|---|---|
| `rows` | `list[dict]` | Parsed rows as list of dicts |
| `columns` | `list[str]` | Column names |

### Example

```python
import pandas as pd
df = pd.read_csv('data.csv')
print(df.head())
```

### Frameworks

- Python `pandas` — `read_csv()`
- LangChain CSVLoader
- OpenAI Code Interpreter

### Related Skills

- [Data Cleaning](data-cleaning.md)
- [Data Aggregation](data-aggregation.md)
- [JSON Transformation](json-transformation.md)

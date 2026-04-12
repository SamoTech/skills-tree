# Data Analyst Agent System

**Type:** `system`  
**Complexity:** High  
**Status:** Production-Ready  
**Version:** v1

---

## Overview

An agent that ingests structured data (CSV, Excel, SQL), performs exploratory analysis, generates insights, and produces reports with charts. It plans the analysis, writes and executes Python/SQL, interprets results, and iterates until a complete narrative is built.

---

## Architecture

```
User question + data
       │
       ▼
  ┌──────────┐     ┌────────────┐     ┌───────────┐
  │  INGEST  │────▶│   PLAN     │────▶│  EXECUTE  │
  │          │     │            │     │           │
  │ Detect   │     │ Formulate  │     │ Python /  │
  │ schema   │     │ analysis   │     │ SQL query │
  │ Profile  │     │ questions  │     │           │
  └──────────┘     └────────────┘     └─────┬─────┘
                                            │
                                    ┌───────▼───────┐
                                    │   INTERPRET   │
                                    │               │
                                    │ Extract key   │
                                    │ findings      │
                                    │ Generate viz  │
                                    └───────┬───────┘
                                            │
                                    ┌───────▼───────┐
                                    │    REPORT     │
                                    │               │
                                    │ Markdown +    │
                                    │ charts +      │
                                    │ caveats       │
                                    └───────────────┘
```

---

## Skills Used

| Skill | Role |
|---|---|
| [Structured Data Reading](../skills/01-perception/structured-data-reading.md) | Ingest and profile data |
| [Database Reading](../skills/01-perception/database-reading.md) | Query SQL sources |
| [Mathematical Reasoning](../skills/02-reasoning/mathematical-reasoning.md) | Statistical analysis |
| [Code Generation](../skills/05-code/code-generation.md) | Write pandas/SQL code |
| [Goal Setting](../skills/02-reasoning/goal-setting.md) | Clarify analysis questions |

---

## Implementation

```python
import pandas as pd
from anthropic import Anthropic

client = Anthropic()

def data_analyst_agent(csv_path: str, user_question: str) -> str:
    df = pd.read_csv(csv_path)
    schema_info = f"Columns: {list(df.columns)}\nShape: {df.shape}\n"
    schema_info += f"Sample:\n{df.head(3).to_markdown()}"
    schema_info += f"\nDtypes:\n{df.dtypes.to_string()}"

    messages = [{"role": "user", "content":
        f"Dataset info:\n{schema_info}\n\nQuestion: {user_question}\n"
        "Write Python pandas code to answer this. Use print() for results."}]

    for _ in range(5):  # max iterations
        resp = client.messages.create(
            model="claude-opus-4-5", max_tokens=2048, messages=messages
        )
        code = extract_code_block(resp.content[0].text)
        result = execute_python(code, df)  # sandboxed execution
        messages += [
            {"role": "assistant", "content": resp.content[0].text},
            {"role": "user", "content": f"Output:\n{result}\n"
             "Summarise the key finding in 2 sentences. If error, fix the code."}
        ]
        if "error" not in result.lower():
            break

    final = client.messages.create(
        model="claude-opus-4-5", max_tokens=1024, messages=messages
    )
    return final.content[0].text
```

---

## Analysis Checklist

- [ ] **Schema profiling** — nulls, dtypes, cardinality per column
- [ ] **Distribution analysis** — mean, median, std, skew for numerics
- [ ] **Outlier detection** — IQR method or Z-score
- [ ] **Correlation matrix** — `df.corr()` for numeric columns
- [ ] **Time series check** — detect datetime columns, plot trend
- [ ] **Group-by insights** — top segments by key metric
- [ ] **Anomaly flag** — values outside 3σ

---

## Cost Profile

| Data Size | Avg LLM calls | Avg Total Tokens | Est. Cost (Claude Opus) |
|---|---|---|---|
| Small (< 1K rows) | 3 | 6K | ~$0.09 |
| Medium (1K–100K rows) | 5 | 12K | ~$0.18 |
| Large (100K+ rows) | 7 | 20K | ~$0.30 |

---

## Related

- [System: Research Agent](research-agent.md)
- [System: Coding Agent](coding-agent.md)
- [Blueprint: RAG Stack](../blueprints/rag-stack.md)

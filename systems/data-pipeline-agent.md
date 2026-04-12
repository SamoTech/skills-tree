# Data Pipeline Agent System

**Category:** systems | **Level:** advanced | **Stability:** stable | **Version:** v1

## Overview

An autonomous data operations agent that reads from heterogeneous sources (databases, APIs, files), transforms and validates the data, detects anomalies, and writes clean output to a target store — with full observability and self-healing on common failures.

---

## Skills Used

| Skill | Role in System |
|---|---|
| `skills/01-perception/database-reading.md` | Read source tables and query results |
| `skills/01-perception/structured-data-reading.md` | Parse CSV, JSON, Parquet inputs |
| `skills/12-data/etl.md` | Extract, transform, load pipeline |
| `skills/12-data/anomaly-detection.md` | Flag statistical outliers in the stream |
| `skills/02-reasoning/causal.md` | Diagnose root cause of data quality failures |
| `skills/04-action/database-write.md` | Persist clean output to target store |
| `skills/04-action/alert.md` | Notify on pipeline failures or anomalies |

---

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                  Data Pipeline Agent                 │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Sources ──► Extractor ──► Schema Validator          │
│   DB / API /      │              │                   │
│   Files           │         Reject / Fix             │
│                   ▼              │                   │
│             Transformer ◄────────┘                   │
│                   │                                  │
│             Anomaly Detector                         │
│                   │                                  │
│          ┌────────┴────────┐                         │
│          │                 │                         │
│       Normal            Anomaly                      │
│          │                 │                         │
│       Target DB        Alert + Quarantine            │
└──────────────────────────────────────────────────────┘
```

---

## Implementation

```python
import anthropic
import pandas as pd
import json
from typing import Any

client = anthropic.Anthropic()

ETL_SYSTEM = """
You are a data quality agent. Given a batch of records as JSON, you must:
1. Identify and fix obvious data quality issues (nulls in required fields, type mismatches, duplicates)
2. Flag statistical anomalies (values > 3 std deviations from mean)
3. Return a JSON object with keys:
   - "clean": list of corrected records
   - "anomalies": list of {record, reason} for outliers
   - "dropped": list of {record, reason} for unfixable records
   - "summary": one-sentence description of what was done
"""

def extract_from_db(connection_string: str, query: str) -> pd.DataFrame:
    """Extract data from a SQL source."""
    import sqlalchemy
    engine = sqlalchemy.create_engine(connection_string)
    return pd.read_sql(query, engine)

def agent_transform(batch: list[dict]) -> dict:
    """Use LLM agent to clean and validate a batch."""
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        system=ETL_SYSTEM,
        messages=[{
            "role": "user",
            "content": f"Process this batch:\n{json.dumps(batch, indent=2)}"
        }]
    )
    return json.loads(response.content[0].text)

def load_to_target(records: list[dict], target_conn: str, table: str):
    """Write clean records to target database."""
    import sqlalchemy
    df = pd.DataFrame(records)
    engine = sqlalchemy.create_engine(target_conn)
    df.to_sql(table, engine, if_exists="append", index=False)

def run_pipeline(
    source_conn: str,
    source_query: str,
    target_conn: str,
    target_table: str,
    batch_size: int = 500
) -> dict:
    df = extract_from_db(source_conn, source_query)
    records = df.to_dict(orient="records")

    all_clean, all_anomalies, all_dropped = [], [], []

    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        result = agent_transform(batch)
        all_clean.extend(result["clean"])
        all_anomalies.extend(result["anomalies"])
        all_dropped.extend(result["dropped"])
        print(f"Batch {i//batch_size + 1}: {result['summary']}")

    if all_clean:
        load_to_target(all_clean, target_conn, target_table)

    return {
        "loaded": len(all_clean),
        "anomalies": len(all_anomalies),
        "dropped": len(all_dropped),
        "anomaly_details": all_anomalies,
    }

# Usage
if __name__ == "__main__":
    report = run_pipeline(
        source_conn="postgresql://user:pass@source-db/analytics",
        source_query="SELECT * FROM raw_events WHERE date = CURRENT_DATE",
        target_conn="postgresql://user:pass@target-db/warehouse",
        target_table="clean_events",
    )
    print(f"Pipeline complete: {report}")
```

---

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Schema drift | Source adds/removes columns | Validate schema before each run |
| LLM hallucination | Model invents values | Never let LLM generate data, only classify/flag |
| Batch too large | Token limit exceeded | Keep batches ≤ 500 rows, ~50KB JSON |
| Silent data loss | Drop without alert | Always log `dropped` list to quarantine table |

---

## Related

- `systems/data-analyst.md` — Analysis layer that runs on top of clean pipeline output
- `blueprints/rag-stack.md` — Embed clean records for retrieval
- `skills/12-data/etl.md` · `skills/12-data/anomaly-detection.md`

## Changelog

- **v1** (2026-04) — Initial system: extract, agent-transform, anomaly detection, load

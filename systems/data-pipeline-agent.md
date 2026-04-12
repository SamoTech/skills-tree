---
title: Data Pipeline Agent
category: systems
version: v1
stability: stable
skills: [database-reading, etl, anomaly-detection, structured-data-reading, action-execution]
---

# Data Pipeline Agent

> Autonomous agent that ingests raw data from multiple sources, transforms and validates it, detects anomalies, and loads clean records into a target store — with self-healing on failures.

## Skills Used

| Skill | Role |
|---|---|
| `skills/01-perception/database-reading.md` | Read source tables / API endpoints |
| `skills/01-perception/structured-data-reading.md` | Parse CSV, JSON, Parquet inputs |
| `skills/12-data/etl.md` | Transform, clean, normalise records |
| `skills/12-data/anomaly-detection.md` | Flag outliers before load |
| `skills/04-action-execution/database-write.md` | Write validated records to target |
| `skills/02-reasoning/self-correction.md` | Re-plan on schema drift or errors |

## Architecture

```
  Sources: Postgres · REST API · S3 CSV · Kafka topic
       │
       ▼
┌─────────────────┐
│   Extractor     │  parallel fetch, rate-limited
└────────┬────────┘
         │ raw records
         ▼
┌─────────────────┐
│   Transformer   │  type coercion, dedup, join
└────────┬────────┘
         │ candidate records
         ▼
┌─────────────────┐
│ Anomaly Scanner │  z-score + LLM semantic check
└────────┬────────┘
    ┌────┴────┐
  clean    flagged → quarantine table + alert
    │
    ▼
┌─────────────────┐
│    Loader       │  upsert with idempotency key
└─────────────────┘
         │
         ▼
  Target: Supabase / BigQuery / Redshift
```

## Implementation

```python
import anthropic
import pandas as pd
from sqlalchemy import create_engine, text

client = anthropic.Anthropic()

ETL_SYSTEM = """
You are a data pipeline controller. Given a sample of raw records and a target schema,
produce a Python pandas transformation script that:
1. Renames and casts columns to match target schema
2. Drops exact duplicates
3. Fills nulls with sensible defaults (document each)
4. Returns (clean_df, quarantine_df) where quarantine holds rows with
   irrecoverable issues
Output ONLY valid Python. No markdown fences.
"""

def generate_transform(sample: str, target_schema: dict) -> str:
    resp = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        system=ETL_SYSTEM,
        messages=[{"role": "user", "content": f"Sample:\n{sample}\n\nTarget schema:\n{target_schema}"}]
    )
    return resp.content[0].text

def run_pipeline(source_engine, target_engine, table: str):
    raw = pd.read_sql(f"SELECT * FROM {table} WHERE processed_at IS NULL LIMIT 5000", source_engine)
    sample = raw.head(5).to_json(orient="records", indent=2)
    target_schema = {"id": "int", "name": "str", "value": "float", "created_at": "datetime"}

    transform_code = generate_transform(sample, target_schema)
    local_vars = {"df": raw, "pd": pd}
    exec(transform_code, local_vars)  # sandboxed in practice
    clean_df, quarantine_df = local_vars["clean_df"], local_vars["quarantine_df"]

    clean_df.to_sql(f"{table}_clean", target_engine, if_exists="append", index=False, method="multi")
    if not quarantine_df.empty:
        quarantine_df.to_sql(f"{table}_quarantine", target_engine, if_exists="append", index=False)
    print(f"Loaded {len(clean_df)} rows. Quarantined {len(quarantine_df)}.")
```

## Failure Modes

| Failure | Cause | Fix |
|---|---|---|
| Schema drift | Source adds/removes columns | Re-generate transform script, alert |
| LLM produces invalid Python | Complex schema edge cases | Wrap exec in try/except, fall back to manual mapping |
| Anomaly false positives | Seasonal spikes in data | Tune z-score window per metric |
| Idempotency violation | Duplicate runs on retry | Add `idempotency_key` unique constraint on target |

## Related

- `systems/data-analyst.md`
- `skills/12-data/anomaly-detection.md`
- `blueprints/rag-stack.md`

## Changelog

- `v1` (2026-04) — Initial pipeline with LLM-generated transforms and anomaly quarantine

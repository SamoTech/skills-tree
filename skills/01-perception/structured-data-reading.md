# Structured Data Reading

**Category:** `perception`  
**Skill Level:** `basic`  
**Stability:** `stable`  
**Added:** 2025-03  
**Last Updated:** 2026-04

---

## Description

Parse and interpret structured text formats — JSON, YAML, TOML, XML, CSV, TSV, INI, and environment files. The agent normalizes irregular schemas, handles missing fields, detects type mismatches, and converts between formats. Useful for reading configuration files, API payloads, data exports, and deployment manifests.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `raw` | `string` | ✅ | Raw file content in any structured format |
| `target_schema` | `dict` | ❌ | JSON Schema or example dict to normalize against |
| `output_format` | `string` | ❌ | `json` (default), `yaml`, `csv` |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `parsed` | `dict` / `list` | Normalized structured data |
| `missing_fields` | `list` | Fields expected by schema but absent |
| `type_errors` | `list` | Fields with wrong data types |

---

## Example

```python
import anthropic
import json
from pathlib import Path

client = anthropic.Anthropic()

def normalize_config(file_path: str, target_schema: dict) -> dict:
    """Read a config file of any format and normalize it to a target schema."""
    raw = Path(file_path).read_text(encoding="utf-8")
    extension = Path(file_path).suffix

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": (
                f"Parse this {extension} file and return a JSON object matching this schema:\n"
                f"{json.dumps(target_schema, indent=2)}\n\n"
                "Use null for missing optional fields. Return ONLY valid JSON.\n\n"
                f"File content:\n{raw[:6000]}"
            )
        }]
    )
    return json.loads(response.content[0].text)

target = {
    "database": {"host": "string", "port": "int", "name": "string"},
    "debug": "bool",
    "allowed_hosts": ["string"]
}
result = normalize_config("config.yaml", target)
print(json.dumps(result, indent=2))
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| Claude claude-opus-4-5 | Direct text prompt | 2024-06 |
| LangChain | `StructuredOutputParser` | v0.1 |
| LangGraph | State node with schema validation | v0.1 |

---

## Notes

- For very large files (>50 KB), extract only relevant sections before sending
- Always validate the returned JSON with `json.loads()` inside a try/except
- Combine with [API Response Parsing](api-response-parsing.md) for webhook/API payloads

---

## Related Skills

- [API Response Parsing](api-response-parsing.md) — REST/GraphQL payload parsing
- [Document Parsing](document-parsing.md) — unstructured document extraction
- [Database Reading](database-reading.md) — live database access

---

## Changelog

| Date | Change |
|---|---|
| `2026-04` | Expanded from stub: full description, I/O table, normalize example, notes |
| `2025-03` | Initial stub entry |

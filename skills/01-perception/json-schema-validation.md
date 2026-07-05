---
title: "JSON Schema Validation"
category: 01-perception
level: basic
stability: stable
description: "Enable AI agents to validate JSON payloads against JSON Schema definitions, producing structured error reports and auto-corrected outputs for robust API and data pipeline contracts."
added: "2025-03"
version: "v2"
last_updated: "2026-07"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-json-schema-validation.json)

# JSON Schema Validation

**Category:** `01-perception`
**Skill Level:** `basic`
**Stability:** `stable`
**Version:** `v2`
**Added:** `2025-03`
**Last Updated:** `2026-07`

---

## Description

JSON Schema Validation enables an agent to verify that a JSON payload conforms to a schema definition (Draft-07, Draft-2019, or Draft-2020), producing structured error reports with exact paths and violation descriptions. It is the enforcement layer for tool-calling agents, API gateway validators, and data pipeline ingestion guards. The skill supports both strict validation and coercive auto-fixing of common type mismatches.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `data` | `dict` \| `list` | ✅ | JSON payload to validate |
| `schema` | `dict` | ✅ | JSON Schema definition (Draft-07 or later) |
| `strict` | `bool` | ❌ | Reject additional properties not in schema (default: false) |
| `coerce` | `bool` | ❌ | Auto-coerce type mismatches (e.g. string `"42"` → int `42`) before validation (default: false) |
| `draft` | `string` | ❌ | Schema draft version: `draft7` \| `draft201909` \| `draft202012` (default: `draft7`) |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `valid` | `bool` | `true` if data passes schema validation |
| `errors` | `list[dict]` | List of validation errors (empty if valid) |
| `errors[].path` | `string` | JSON Pointer to the failing field (e.g. `/user/email`) |
| `errors[].message` | `string` | Human-readable error description |
| `errors[].schema_path` | `string` | Path in the schema that triggered the error |
| `coerced_data` | `dict` | Auto-corrected payload (only when `coerce=true`) |

---

## Example

```python
import jsonschema
from jsonschema import validate, ValidationError, Draft7Validator

schema = {
    "type": "object",
    "required": ["name", "age", "email"],
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "age": {"type": "integer", "minimum": 0, "maximum": 150},
        "email": {"type": "string", "format": "email"},
    },
    "additionalProperties": False,
}

def validate_json(data: dict, schema: dict) -> dict:
    validator = Draft7Validator(schema)
    errors = list(validator.iter_errors(data))
    if not errors:
        return {"valid": True, "errors": []}
    return {
        "valid": False,
        "errors": [{
            "path": "/" + "/".join(str(p) for p in e.absolute_path),
            "message": e.message,
            "schema_path": "/" + "/".join(str(p) for p in e.absolute_schema_path),
        } for e in errors],
    }

result = validate_json({"name": "Ossama", "age": "thirty", "email": "test@example.com"}, schema)
print(result)
# → {"valid": False, "errors": [{"path": "/age", "message": "'thirty' is not of type 'integer'", ...}]}
```

```python
# Extended — LLM output validation with auto-repair loop
import json

def llm_output_validate_and_repair(llm_response: str, schema: dict, max_retries: int = 2) -> dict:
    for attempt in range(max_retries + 1):
        try:
            data = json.loads(llm_response)
        except json.JSONDecodeError as e:
            return {"valid": False, "errors": [{"path": "/", "message": f"Invalid JSON: {e}"}]}
        result = validate_json(data, schema)
        if result["valid"]:
            return {"valid": True, "data": data, "attempts": attempt + 1}
        if attempt < max_retries:
            # Feed errors back to LLM for self-correction (stub)
            llm_response = f"Fix these errors: {result['errors']}\nOriginal: {llm_response}"
    return result
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| Python `jsonschema` | `Draft7Validator`, `Draft202012Validator` — reference implementation | v1 |
| Python `pydantic` | `BaseModel` with automatic type coercion and validation | v1 |
| Python `cerberus` | Lightweight schema validation with custom rules | v1 |
| OpenAI Structured Outputs | `response_format={"type": "json_schema", ...}` — server-side enforcement | 2024-08 |
| LangChain `PydanticOutputParser` | Validates LLM output against a Pydantic model | v0.1 |
| LangGraph | Schema validation as a graph node for output gating | v0.1 |
| GPT-4o | Native JSON mode + structured outputs API | 2024-05 |
| Claude 3.7 Sonnet | Tool use enforces schema via `input_schema` parameter | 2025-01 |

---

## Model Comparison

| Capability | GPT-4o | Claude 3.7 Sonnet | Gemini 2.0 Flash | Notes |
|---|---|---|---|---|
| Schema compliance | 5 | 5 | 4 | GPT-4o structured outputs = near-perfect |
| Error self-correction | 5 | 4 | 3 | GPT-4o best at fixing its own JSON errors |
| Complex nested schemas | 4 | 5 | 3 | Claude handles deep nesting better |
| Instruction following | 5 | 5 | 4 | |
| Format consistency | 5 | 4 | 4 | GPT-4o most consistent across runs |

---

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Type coercion confusion | LLM outputs `"true"` (string) instead of `true` (bool) | Enable `coerce=true` or use Pydantic's `validator` |
| `additionalProperties` false positives | Schema too strict rejects valid vendor extensions | Set `additionalProperties: true` in development; tighten in production |
| Format keyword not enforced | `jsonschema` skips `format` checks by default | Use `format_checker=jsonschema.FormatChecker()` |
| Schema drift | LLM trained on old schema produces output matching old spec | Version schemas; pin schema version in system prompt |
| Circular `$ref` | Self-referential schemas cause infinite recursion | Use `jsonschema`'s `RefResolver` which handles circular refs |

---

## Prompt Patterns

### Pattern 1 — Strict Output Enforcement
```
Respond ONLY with a valid JSON object matching this schema:
{json_schema}

Do not include any explanation, markdown, or extra fields.

Task: {task_description}
Input: {input}
```

### Pattern 2 — Validation Error Fix
```
The following JSON failed schema validation:

JSON: {invalid_json}
Schema: {schema}
Errors: {validation_errors}

Return a corrected JSON object that passes all validation rules.
```

### Pattern 3 — Schema Generation
```
Given this example JSON object:
{example_json}

Generate a JSON Schema (Draft-07) that:
1. Validates this example as valid
2. Marks all present fields as required
3. Uses appropriate types and constraints
Return only the schema JSON.
```

---

## Notes

- Use `Draft7Validator.check_schema(schema)` to validate your schema itself before using it in production.
- OpenAI's Structured Outputs API enforces the schema server-side, eliminating the need for client-side validation entirely — prefer this when using GPT-4o.
- `pydantic` v2 is significantly faster than `jsonschema` for high-throughput validation (10x+ improvement).
- Never pass user-controlled strings as schema definitions — this is a potential code injection vector.

---

## Related Skills

- [API Response Parsing](./api-response-parsing.md) — validating API responses against expected schemas
- [Structured Data Reading](./structured-data-reading.md) — reading JSON/YAML/TOML before validation
- [Document Parsing](./document-parsing.md) — extracting JSON from mixed-format documents

---

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-04` | v1 | Initial entry |
| `2026-07` | v2 | Added typed I/O tables, extended examples, full frameworks table, model comparison, prompt patterns, detailed failure modes |

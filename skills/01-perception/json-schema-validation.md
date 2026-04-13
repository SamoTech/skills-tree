![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-json-schema-validation.json)

# JSON Schema Validation
Category: perception | Level: basic | Stability: stable | Version: v1

## Description
Validate incoming JSON payloads against a schema before processing, catching malformed or missing fields early.

## Inputs
- `payload`: raw JSON string or dict
- `schema`: JSON Schema object

## Outputs
- `valid`: bool
- `errors`: list of validation error messages

## Example
```python
import jsonschema
schema = {"type": "object", "required": ["id", "name"], "properties": {"id": {"type": "integer"}, "name": {"type": "string"}}}
try:
    jsonschema.validate({"id": 1, "name": "Alice"}, schema)
    print("Valid")
except jsonschema.ValidationError as e:
    print(f"Invalid: {e.message}")
```

## Frameworks
| Framework | Method |
|---|---|
| Python | `jsonschema` library |
| LangChain | `PydanticOutputParser` |
| OpenAI | Structured outputs with `response_format` |

## Failure Modes
- Nullable fields not declared with `anyOf: [type, null]`
- Extra properties silently ignored unless `additionalProperties: false`

## Related
- `api-response-parsing.md` · `structured-data-reading.md`

## Changelog
- v1 (2026-04): Initial entry

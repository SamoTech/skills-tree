---
name: structured-data-reading
description: Parse JSON, YAML, TOML, XML, CSV, and related structured formats into validated data while preserving type errors, missing fields, and parser failures.
license: MIT
metadata:
  source: skills/01-perception/structured-data-reading.md
  version: "v2"
---

# Structured Data Reading

1. Detect the declared or inferred format before parsing.
2. Use a format-aware parser instead of ad-hoc string manipulation.
3. Validate against a schema when one is available.
4. Preserve missing fields, nulls, duplicate-key behavior, and type errors according to the parser's semantics.
5. Bound input size and nesting depth where the parser permits.
6. Treat environment files and configuration values as potentially sensitive.

## Failure modes

- Malformed input: return a parse error with location where available.
- Duplicate or conflicting keys: preserve parser semantics and flag ambiguity.
- Resource exhaustion: impose size/depth limits and reject pathological inputs.

## Evidence

- https://docs.python.org/3/library/json.html
- https://yaml.org/spec/1.2.2/
- https://docs.python.org/3/library/xml.etree.elementtree.html

Evidence status: these references support implementation guidance; no performance benchmark is claimed without reproducible benchmark data.

---
name: api-response-parsing
description: Parse and validate API responses, including nested payloads, pagination, error envelopes, partial responses, and schema drift. Use when an agent must turn an API response into bounded structured data.
license: MIT
metadata:
  source: skills/01-perception/api-response-parsing.md
  version: "v2"
---

# API Response Parsing

1. Identify the response protocol and expected schema before extracting values.
2. Validate untrusted JSON against an explicit schema when one is available.
3. Handle pagination using the provider's documented cursor or page mechanism.
4. Preserve provider errors and validation failures instead of silently coercing them.
5. Bound response size, page count, retries, and downstream context.
6. Return structured data with provenance or source paths when extraction is ambiguous.

## Failure modes

- Schema drift: fail validation or route to an explicitly versioned fallback.
- Malformed or partial responses: return an error state rather than fabricated fields.
- Rate limits: honor provider retry guidance and stop at configured retry limits.

## Evidence

- https://json-schema.org/specification
- https://json-schema.org/draft/2020-12/json-schema-validation

Evidence status: these references support implementation guidance; no performance benchmark is claimed without reproducible benchmark data.

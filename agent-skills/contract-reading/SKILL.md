---
name: contract-reading
description: Extract parties, dates, definitions, obligations, payments, termination clauses, and other contract structure while preserving uncertainty and source locations. Use for document analysis, not legal advice.
license: MIT
metadata:
  source: skills/01-perception/contract-reading.md
  version: "v2"
---

# Contract Reading

1. Preserve the original document and page/section boundaries.
2. Identify parties, effective dates, defined terms, obligations, conditions, payments, renewals, termination, and governing-law clauses.
3. Return each extracted item with a source span when possible.
4. Distinguish explicit clauses from inferred relationships.
5. Flag missing schedules, exhibits, signatures, unreadable pages, and contradictory clauses.
6. Treat the result as document extraction, not legal advice.

## Failure modes

- Defined-term ambiguity: trace the definition before interpreting a clause.
- Missing exhibits/schedules: mark dependent obligations unresolved.
- OCR or parsing errors: retain page references and require human verification for material clauses.

## Evidence

- https://agentskills.io/specification
- https://docs.python.org/3/library/json.html

Evidence status: these references support implementation guidance; no performance benchmark is claimed without reproducible benchmark data.

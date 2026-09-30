---
name: sql-query-generation
description: Generate SQL from explicit data requirements, schema constraints, and supported database dialects while preserving correctness and safe parameter handling.
license: MIT
metadata:
  source: skills/05-code/sql-query-generation.md
  version: "v2"
---

# Sql Query Generation

1. Inspect the actual schema and database dialect.
2. Define required columns, filters, joins, ordering, and edge cases.
3. Generate parameterized SQL rather than unsafe interpolation.
4. Validate syntax and result shape against the target database.
5. Check query behavior for empty and boundary cases.
6. Record verification evidence.

## Failure modes
- Wrong schema assumptions.
- Unsafe interpolation.
- Dialect mismatch.
- Incorrect result shape or joins.

## Evidence
Canonical skill: skills/05-code/sql-query-generation.md
Repository governance: AI_CONSTITUTION.md

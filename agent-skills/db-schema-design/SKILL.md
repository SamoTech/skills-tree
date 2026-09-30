---
name: db-schema-design
description: Design database schemas from explicit data requirements, relationships, constraints, and access patterns.
license: MIT
metadata:
  source: skills/05-code/db-schema-design.md
  version: "v2"
---

# Db Schema Design

1. Inspect the current schema, migrations, queries, constraints, and explicit requirements.
2. Model entities, relationships, keys, nullability, indexes, and integrity constraints.
3. Choose the smallest compatible schema change and define migration and rollback behavior.
4. Implement the migration without bypassing repository controls.
5. Run schema, migration, and relevant application tests.
6. Record verification evidence.

## Failure modes
- Data loss or destructive migration without recovery.
- Missing constraints or incompatible interfaces.
- Designing from assumptions instead of repository evidence.
- Skipping migration validation.

## Evidence
Canonical skill: skills/05-code/db-schema-design.md
Repository governance: AI_CONSTITUTION.md

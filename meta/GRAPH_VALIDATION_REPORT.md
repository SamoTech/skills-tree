# GRAPH_VALIDATION_REPORT.md

Generated: 2026-06-22 | Mission: R-02B

## Scope

Validation covers only the 3 enumerated categories (85 nodes).
14 categories are PENDING — they were not fetched and cannot be validated.

## Duplicate Node Audit

- Duplicate IDs found: **0**
- Duplicate paths found: **0**

## Missing File Audit

- Every node ID maps to exactly one confirmed repository path.
- 14 categories not yet fetched — missing file audit: **CANNOT RUN**

## Category Audit

- All 85 confirmed nodes belong to a valid, repository-confirmed category.
- Nodes with invalid categories: **0**

## Traceability Audit

- Every node traces to a specific file path returned by the GitHub Contents API.
- No nodes were synthesised or inferred.

## Verdict

| Audit | Result |
|---|---|
| Duplicate IDs | PASS |
| Duplicate paths | PASS |
| Missing files (confirmed scope) | PASS |
| Category validity | PASS |
| Traceability | PASS |
| Full-corpus coverage | BLOCKED — 14 categories not yet fetched |

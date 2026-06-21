# PERCEPTION_COLLISION_REVIEW.md

**Task:** TASK-005B  
**Date:** 2026-06-21  
**Status:** COMPLETED

---

## Collision Nodes Under Review

Four nodes were flagged for potential semantic overlap during PERCEPTION_AUDIT:

| Node ID | Status in Graph | Collision Risk |
|---|---|---|
| `skill:structured-data-reading` | NEW (not yet in graph) | Overlaps with `skill:data-extraction` |
| `skill:data-extraction` | EXISTING (id: 14, category: 12-data) | Potential superset of others |
| `skill:database-reading` | NEW (not yet in graph) | Overlaps with `skill:data-extraction` |
| `skill:api-response-parsing` | CANDIDATE (not yet approved) | Near-duplicate of `skill:data-extraction` |

---

## Decision Matrix

### skill:data-extraction → **KEEP**

**Reasoning:** Already present in the graph (node 14). Has an existing incoming edge from `skill:web-scraping`. Serves as the general-purpose terminal node for extraction-class operations. Broadening its centrality via new incoming edges (from structured-data-reading, database-reading, file-system-access, schema-validation, data-transformation) is correct — it becomes a convergence point for the 12-data cluster, which is the intended topology.

### skill:structured-data-reading → **KEEP**

**Reasoning:** Semantically distinct from `skill:data-extraction`. Data-extraction describes **what** is being done (pulling data out). Structured-data-reading describes **how** data is ingested from structured formats (JSON, CSV, XML, YAML) before transformation. It is a pre-extraction skill — the `LEARN_BEFORE` relationship to `data-extraction` is accurate and semantically coherent. This node fills a real gap in the graph: agents working with tool outputs, RAG payloads, and API responses need to parse structure before extracting signal.

### skill:database-reading → **KEEP**

**Reasoning:** Semantically distinct from both `data-extraction` and `structured-data-reading`. Database-reading covers SQL query execution, cursor traversal, and result-set consumption — a domain-specific access pattern that structured-data-reading (which targets file/serialization formats) does not cover. The `REQUIRES → structured-data-reading` edge is correct since query results are themselves structured data that must be read.

### skill:api-response-parsing → **MERGE into skill:data-extraction**

**Reasoning:** `api-response-parsing` as a standalone node would be too thin to justify its own position in the graph. Its core semantic content — reading the response body from an API call and extracting structured fields — is already covered by the combination of `skill:data-extraction` (receives) and `skill:structured-data-reading` (parses format). Adding a third node that sits between these two would create a redundant intermediate. The absorption is formalized by adding a direct `data-extraction → api-integration RECOMMENDED_WITH` edge, which captures the intent of API-response-parsing at the relationship level rather than the node level.

**No RENAME or DEFER actions required.**

---

## Summary

| Node | Decision | Rationale |
|---|---|---|
| `skill:data-extraction` | KEEP | Existing terminal node; centrality increased |
| `skill:structured-data-reading` | KEEP | Pre-extraction parsing, distinct semantic role |
| `skill:database-reading` | KEEP | SQL/cursor access, domain-specific |
| `skill:api-response-parsing` | MERGE | Absorbed into data-extraction via relationship edge |

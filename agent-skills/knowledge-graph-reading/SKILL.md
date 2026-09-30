---
name: knowledge-graph-reading
description: Query and traverse RDF, SPARQL, property graphs, and knowledge-graph APIs to retrieve bounded entity relationships with explicit query limits and provenance.
license: MIT
metadata:
  source: skills/01-perception/knowledge-graph-reading.md
  version: "v2"
---

# Knowledge Graph Reading

1. Identify the graph model and query language.
2. Restrict traversal depth, result count, and query time.
3. Parameterize user-controlled values where the graph interface supports it.
4. Preserve identifiers, labels, relationships, and provenance.
5. Distinguish observed graph relationships from inferred relationships.
6. Do not execute arbitrary write queries in a read-only skill.

## Failure modes

- Query timeout: narrow predicates, traversal depth, or result limits.
- Incomplete graph: report missing relationships rather than inferring them.
- Injection or unintended writes: use read-only credentials and validated query templates.

## Evidence

- https://www.w3.org/TR/sparql11-query/
- https://neo4j.com/docs/cypher-manual/current/
- https://rdflib.readthedocs.io/

Evidence status: these references support implementation guidance; no performance benchmark is claimed without reproducible benchmark data.

---
name: knowledge-graph-reading
description: Query and traverse RDF, SPARQL, property graphs, and knowledge-graph APIs to retrieve bounded entity relationships with explicit query limits and provenance.
metadata:
  source: skills/01-perception/knowledge-graph-reading.md
  category: 01-perception
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-knowledge-graph-reading.json)

# Knowledge Graph Reading
Category: perception | Level: advanced | Stability: stable | Version: v1

## Description
Query and traverse knowledge graphs (RDF, Neo4j, Wikidata) to extract entity relationships for reasoning.

## Inputs
- `endpoint`: SPARQL URL or Neo4j connection
- `query`: SPARQL or Cypher query string

## Outputs
- List of triples or graph nodes/edges

## Example
```python
from SPARQLWrapper import SPARQLWrapper, JSON
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery("""
SELECT ?item ?label WHERE {
  ?item wdt:P31 wd:Q5 ; rdfs:label ?label . FILTER(LANG(?label)="en") } LIMIT 5
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
```

## Frameworks
| Framework | Method |
|---|---|
| Python | `SPARQLWrapper`, `py2neo`, `rdflib` |
| LlamaIndex | `KnowledgeGraphIndex` |
| LangChain | `Neo4jGraph` |

## Failure Modes
- SPARQL timeout on large graphs
- Blank nodes lack stable identifiers

## Related
- `structured-data-reading.md` · `database-reading.md`

## Changelog
- v1 (2026-04): Initial entry


## Evidence

- https://www.w3.org/TR/sparql11-query/
- https://neo4j.com/docs/cypher-manual/current/
- https://rdflib.readthedocs.io/

Evidence status: these references support implementation guidance; no performance benchmark is claimed without reproducible benchmark data.

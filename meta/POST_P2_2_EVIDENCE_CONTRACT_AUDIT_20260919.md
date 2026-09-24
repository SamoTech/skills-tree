# Post-P2.2 Evidence Contract Runtime Audit — 2026-09-19

## Finding

Evidence is already a first-class ontology entity and is consumed by Implementation, Adapter, Compatibility, and graph validation. Runtime integrity verifies evidence identifiers, reverse claim support, and universal provenance, but there was no dedicated machine-readable Evidence contract enforced during registry initialization.

That left the structural shape of Evidence dependent on the broad universal registry schema rather than a focused contract.

## Selected vertical slice

Implement only Evidence contract enforcement:

1. Add `meta/evidence-contract.schema.json` for the current Evidence record shape.
2. Validate every registered Evidence record during `UniversalRegistry` initialization.
3. Require explicit claim support through a non-empty `supports` list and traceable provenance source.
4. Add behavioral regressions for missing claim support and missing provenance source.
5. Preserve all current evidence records and existing implementation, adapter, compatibility, graph, and MCP behavior.
6. Do not create a numbered P2.3 roadmap item.

## Boundary

This slice strengthens structural and provenance enforcement only. It does not add evidence claims, ecosystem entities, freshness assertions, confidence scores, or new compatibility facts.
# Universal Graph Relationship Runtime Audit — 2026-10-03

## Scope

Fresh post-freshness audit of the typed Universal Graph contract and runtime semantic boundary on live `main`.

## Finding

`meta/universal-graph.schema.json` intentionally declares a broad relationship vocabulary, including future relationships such as `implemented_with`, `alternative_to`, `validated_by_benchmark`, `constrained_by`, `composes_with`, and `depends_on`.

Repository architecture documentation explicitly says these relationships must be introduced only after graph schema validation and deterministic generation rules are defined. The live graph currently uses six relationships with explicit runtime semantics:

- `requires_capability`
- `enables_skill`
- `realized_by`
- `exposed_through`
- `adapted_to`
- `supported_by_evidence`

Before this slice, any other schema-valid relationship reached the runtime validator's fallback branch and was silently accepted without semantic source/target/reference validation.

## Invariant

A schema-valid Universal Graph edge must not become trusted runtime data unless its relationship type has an explicit deterministic semantic validator.

Schema vocabulary may remain broader than the currently implemented runtime vocabulary, but unsupported relationships must fail closed rather than pass through silently.

## Selected smallest slice

1. Preserve the existing schema vocabulary; do not invent endpoint semantics for deferred relationships.
2. Define the runtime-supported relationship set explicitly.
3. Reject schema-valid but runtime-unsupported relationship types with a deterministic `ValueError`.
4. Add a negative behavioral regression test proving a valid-schema `alternative_to` edge cannot pass silently.
5. Record the boundary in decision memory and development knowledge.
6. Keep existing graph data unchanged.

## Non-goals

- No new Universal Graph relationship semantics.
- No new graph edges.
- No inferred dependencies or alternatives.
- No change to the existing six relationship contracts.
- No graph-generator rewrite.
- No ranking, trust score, or benchmark-result claims.

## Verification target

The existing eight graph edges must remain valid and deterministic. A synthetic graph using a schema-valid but runtime-unsupported relationship must fail at registry initialization with the explicit unsupported-relationship error.

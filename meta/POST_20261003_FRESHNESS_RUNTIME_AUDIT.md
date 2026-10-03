# Universal Registry Freshness Runtime Audit — 2026-10-03

## Scope

Fresh post-benchmark audit of the universal-registry consumer boundary against the repository evidence model and product mission.

## Finding

The universal registry has machine-readable identity, version, provenance, evidence, compatibility, benchmark, and graph boundaries. It does not yet expose the repository's existing freshness semantics as a normalized registry contract/runtime boundary.

Evidence:

- `meta/EVIDENCE_MODEL.md` defines freshness as last reviewed, review due, freshness basis, and known stale conditions.
- `meta/ROADMAP.md` includes freshness/review rules in the target metadata dimensions.
- Existing corpus and ontology records already use review timestamps, and stale-skill automation consumes review dates.
- `meta/universal-registry-data.schema.json` previously had no explicit freshness object on its generic entity contract.
- `UniversalRegistry` previously had no deterministic freshness accessor.

## Invariant

A registry consumer must be able to determine declared freshness metadata without inspecting arbitrary raw entity fields, while legacy entities remain valid and no freshness dates are invented.

## Selected smallest slice

1. Add an optional `freshness` object to the generic universal-registry entity schema.
2. Require `last_reviewed_at`, `review_due_at`, `basis`, and at least one `stale_conditions` entry when freshness is declared.
3. Add deterministic runtime `freshness_for_entity()` access returning an independent snapshot or `None` when no freshness declaration exists.
4. Reject timezone-naive timestamps and a review due date earlier than the last reviewed date.
5. Add focused behavioral regression tests.
6. Do not migrate existing registry records or invent dates in this slice.

## Non-goals

- No freshness score.
- No automatic claim that an entity is current or stale based on wall-clock time.
- No corpus-wide migration.
- No new entity type.
- No external freshness claims.

## Verification target

Schema validation must accept the existing registry unchanged. A synthetic registry fixture must prove valid freshness access, snapshot isolation, unknown-entity rejection, legacy absence behavior, and invalid chronological ordering rejection.

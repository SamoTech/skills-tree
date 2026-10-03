# Universal Registry Behavioral-Evaluation Audit — 2026-10-03

## Scope

Fresh audit of the universal-registry architecture and consumer boundaries against the current project direction:

Provenance → Evidence → Integrity → Behavioral Evaluation → Memory Safety → Action Governance

## Verified findings

| Layer | Current state | Finding |
|---|---|---|
| Provenance | First-class on registry entities and contracts; semantic integrity requires a traceable source | Covered |
| Evidence | Dedicated schema, validation, EvidenceRuntime, and UniversalRegistry facade | Covered |
| Integrity | Registry instance schema, semantic integrity checks, graph validation, deterministic read-only snapshots | Covered |
| Behavioral evaluation | Behavioral tests exist across runtime features, and benchmarks are a first-class registry collection, but benchmark records used only the generic entity schema and had no dedicated runtime facade | Gap |
| Memory safety | Memory skills cover provenance, validation, retention, uncertainty, correction, and injection | Skill coverage exists; no new memory ontology is justified by this audit |
| Action governance | Security skills cover human approval, permissions, audit logging, rollback, sandboxing, and destructive-action boundaries | Skill/governance coverage exists; no new action ontology is justified by this audit |

## Selected smallest architectural slice

Introduce a dedicated, backward-compatible Benchmark contract and read-only runtime facade:

1. `meta/benchmark-contract.schema.json` defines the minimum reproducible behavioral-evaluation contract.
2. `meta/universal-registry-data.schema.json` references that contract for `entities.benchmarks`.
3. `registry/benchmark.py` provides deterministic typed access.
4. `registry/runtime.py` exposes `resolve_benchmark()` and `benchmarks_for_entity()`.
5. Behavioral regression tests use a repository-local synthetic benchmark fixture only; no production benchmark claim or external result is added.

The contract requires task, inputs, expected behavior, evaluation criteria, test data, methodology, historical results, and provenance. Optional `subjects` provides explicit linkage to an evaluated entity without inventing graph semantics.

## Safety / non-goals

This slice does not add benchmark results, rankings, model claims, memory claims, trust scores, or autonomous action permissions. It does not alter canonical skills or generated projections.

## Verification target

The production registry must continue to load with an empty benchmark collection, while the synthetic test fixture proves schema enforcement, typed access, deterministic ordering, unknown-ID rejection, and snapshot isolation.

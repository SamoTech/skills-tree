# Implementation Ontology

## P2.1 — Contract unification

Phase 2 begins by making `Implementation` a first-class ontology entity rather than allowing it to inherit the generic entity shape.

The normative field contract is `meta/implementation-contract.schema.json`. The universal registry ontology now references that contract directly for `entity_types.implementation`.

An Implementation is a concrete realization of one canonical Skill. It is not a Skill alias, Tool, Model, Platform, Framework, Protocol, Runtime, or Adapter.

The minimum machine-readable contract is:

- stable `id`
- registry `version`
- `name`
- canonical `skill`
- implementation `type`
- optional `provider`
- executable/integration `interface`
- `inputs`
- `outputs`
- `requirements`
- `constraints`
- `limitations`
- `provenance`
- `evidence`
- lifecycle `status`

Lifecycle states are `candidate`, `verified`, `experimental`, and `deprecated`. A record must not be promoted to `verified` without the evidence and validation gates defined by the implementation contract.

P2.1 intentionally does not register new providers or implementations. The existing `implementation/code-reviewer-system` record is used as the real regression subject because its source and evidence already exist in the repository.

## P2.2 — Typed runtime access and validation

P2.2 is complete on `main`.

`registry/runtime.py` exposes the normative `ImplementationRecord` runtime shape, deterministic lookup by canonical Implementation ID, and deterministic lookup of Implementations linked to a canonical Skill. Registry initialization validates every registered Implementation against `meta/implementation-contract.schema.json` while preserving the existing read-only facade and graph/reference integrity checks.

Regression coverage in `tests/test_registry_implementation_runtime.py` verifies successful resolution, deterministic Skill lookup, unknown identifier rejection, and rejection of a contract-invalid Implementation registry. The P2.2 branch passed the required Python 3.11/3.12/3.13 test matrix, Test & Coverage, Security Scan, PR Checks, and Build & Verify Wheel before merge.

## Next vertical slice

No P2.3 item is currently defined.

The next Phase 2 slice must first be established by an architecture audit of the Implementation Ontology after P2.2. The audit should identify the highest-value missing invariant or runtime capability, confirm that it is not already covered by the existing contract, registry, or graph layers, and then define a minimal schema → runtime → behavioral-test slice. No new provider, platform, framework, model, adapter, or compatibility claim should be introduced without authoritative source and provenance.

MCP remains a Protocol and must not be promoted into the canonical Implementation ontology.

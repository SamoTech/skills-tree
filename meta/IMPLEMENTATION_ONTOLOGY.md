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

## Next vertical slice

P2.2 should introduce typed runtime access/validation for Implementation records while preserving the read-only registry behavior and existing graph/reference integrity rules.

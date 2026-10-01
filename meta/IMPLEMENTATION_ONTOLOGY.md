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


## Post-P2.2 Evidence Runtime Integration — 2026-10-01

The post-P2.2 audit identified a read-boundary gap: Evidence was already validated and had a dedicated `EvidenceRuntime`, but consumers of `UniversalRegistry` still had to depend on the internal registry JSON shape.

PR #223 integrated the existing validated `EvidenceRuntime` into `UniversalRegistry` and exposed:

- `resolve_evidence(evidence_id)`
- `evidence_for_entity(entity_id)`

The slice adds no new registry claims, provenance, compatibility facts, provider/platform/model claims, or MCP classifications. It preserves the existing read-only and validation boundaries.

**Verification:** PR #223 exact head `c26652b710064876e3ced5003a74f9d6ba3fce32` passed Test Suite, PR Checks, Security Scan, Build & Verify Wheel, and Auto Label before merge as `642e968879e9b6bfc8e7f9b2a44d12544585fc18`.

## Next Architecture Audit

No numbered P2.3 item is defined. The next slice must come from a fresh universal-registry runtime audit using live implementation, contract, graph, evidence, compatibility, and consumer behavior.

## Post-P2.2 Compatibility Runtime Audit — Selected Slice

The fresh post-P2.2 universal-registry runtime audit identified a second read-boundary gap: Compatibility already has a dedicated validated CompatibilityRuntime, but UniversalRegistry.compatibility_for() was still reading raw registry storage directly.

The selected slice integrates the existing CompatibilityRuntime into UniversalRegistry, exposes typed resolve_compatibility(), and routes compatibility_for() through the validated runtime. It adds no new compatibility facts, providers, platform/framework/model/protocol claims, evidence, or graph semantics.

**Verification:** PR #227 exact head `9e4c7608246092ce902384d10d87e2812330de8a` passed Test Suite, Security Scan, PR Checks, Build & Verify Wheel, and Auto Label before merge as `ba9682b26ea59b18f21eb017b6f239f735c4dec3`.

**Status:** VERIFIED — no compatibility facts or external claims were added.


## Post-P2.2 Skill Runtime Facade Integration — Verified 2026-10-02

A fresh universal-registry runtime audit found that the repository already had a validated `SkillRuntime` with focused deterministic tests, but `UniversalRegistry` still bypassed that boundary for Skill resolution and Skill-to-Implementation traversal.

The selected vertical slice integrates the existing `SkillRuntime` into `UniversalRegistry` and exposes `resolve_skill()`, `capabilities_for_skill()`, and delegated `implementations_for_skill()`. The `TYPE_CHECKING` import boundary keeps the runtime modules acyclic. No ontology records or external claims were introduced.

**Verification:** PR #234 exact head `2ec1690606b26b1727567b6c421ea538b9a07d3a` passed Security Scan, PR Checks, Test Suite, Build & Verify Wheel, and Auto Label before merge as `37b2a529555db2e5db34713ffcb8e3b72083cfb5`.

**Status:** VERIFIED — Skill access through the UniversalRegistry facade is now routed through the dedicated validated runtime.

# Repository Development Knowledge

**Status:** Governing development knowledge for the Universal Agent Knowledge Layer
**Version:** 1.0
**Updated:** 2026-09-18
**Authority:** This document records the development model, architecture direction, execution rules, and verified implementation state. It complements `meta/PROJECT_CONSTITUTION.md`, `meta/AGENT_OPERATING_MODEL.md`, and the machine-readable registry contract in `meta/universal-registry.schema.json`.

## 1. Mission

Skills Tree is evolving from a skill-centric catalogue into a universal, platform-agnostic knowledge layer for AI agents.

The target system allows an agent to start with a goal and deterministically discover:

`Goal → Capability → Skill → Implementation → Adapter → Platform / Framework / Model`

and then reason over prerequisites, dependencies, evidence, benchmarks, constraints, failure modes, composition, architecture, and execution paths.

P1.8 compatibility is a merged registry capability: compatibility facts are typed, evidence-backed, and consumed as applicability data rather than ranking scores. P1.9 eligibility is implemented as a standalone pre-ranking filter and must remain separate from ranking and calibration. P1.10 adds typed universal graph edges, and P1.11 integrates eligibility with recommendations without converting eligibility or compatibility into ranking scores. Phase 2 has since promoted Implementation into the ontology and added typed runtime access and normative contract validation.

The repository is not intended to become a prompt library, a framework-specific skill collection, or a static Markdown directory. Markdown remains valuable as human-readable source material, while machine-readable contracts, provenance, graph integrity, and deterministic runtime behavior become first-class.

## 2. Canonical Ontology

The universal model separates these entities:

- **Goal** — desired outcome or user objective.
- **Capability** — abstract ability required to achieve a goal.
- **Skill** — reusable knowledge/procedure describing how a capability is performed; canonical skills are platform-agnostic.
- **Tool** — executable or externally provided mechanism used by an implementation.
- **Implementation** — concrete realization of a canonical skill using one or more tools/providers/technologies.
- **Platform** — execution/provider environment.
- **Framework** — agent/application framework or SDK.
- **Model** — foundation or task model participating in execution.
- **Adapter** — compatibility bridge mapping an implementation into a platform/framework/model/runtime.
- **Evidence** — provenance-backed support for an entity or claim.
- **Benchmark** — measurable evaluation of quality/performance.
- **Architecture** — validated composition of capabilities, skills, implementations, adapters, runtime components, and deployment constraints.

Never create ecosystem-specific copies of a canonical skill merely because implementations differ. For example, use one canonical Web Search skill and attach multiple implementations/adapters.

## 3. Decision Pipeline

The intended intelligence pipeline is:

`Goal → Goal Resolution → Capability Identification → Skill Discovery → Eligibility → Constraints → Prerequisites → Dependency Graph → Evidence → Benchmark Analysis → Deterministic Scoring → Calibration → Platform Compatibility → Skill Composition → Learning / Execution Path → Architecture Inference → Blueprint → Validation`

Each stage should remain independently testable and explainable. Eligibility, ranking, scoring, calibration, explanation, and presentation must not be collapsed into one opaque operation.

## 4. Engineering Principles

1. Audit before migration or redesign.
2. Preserve working behavior; no wholesale rewrite without evidence.
3. Treat schemas and contracts as first-class architecture.
4. Keep canonical skills platform-agnostic.
5. Keep implementations and adapters separate from canonical skills.
6. Make provenance and evidence first-class data.
7. Make graph relationships typed, validated, and deterministic.
8. Reject dangling references, duplicate identifiers, stale provenance, invalid cycles, and schema-incompatible data.
9. Prefer real behavioral tests over synthetic tests that merely exercise fixtures or mocks.
10. Every change must be minimal, justified, reviewable, and validated.
11. Do not migrate hundreds of skills in bulk before the first vertical slice is proven.
12. Security, supply-chain integrity, provenance, and data integrity are architecture concerns, not documentation afterthoughts.
13. Never claim an implementation is complete without repository/CI evidence.
14. Roadmap state changes only after verifiable commit and test evidence.

## 5. Autonomous Development Loop

Every engineering cycle follows:

`DISCOVER → AUDIT → CLASSIFY → PRIORITIZE → PLAN → IMPLEMENT → TEST → REVIEW → BUILD → CI → OBSERVE → LEARN → NEXT HIGHEST-VALUE TASK`

Agents must inspect existing work and dependencies before editing. Parallel agents may work independently only when their scopes do not overlap. Shared contracts and graph structures require explicit coordination.

Priority policy:

- **P0:** correctness, security, data loss, broken builds/contracts.
- **P1:** ontology, registry, graph, recommendation, architecture, platform abstraction.
- **P2:** API, performance, maintainability, developer experience.
- **P3:** documentation, UX, ecosystem growth.

## 6. Definition of Done

A vertical slice is complete only when applicable items are verified:

- implementation exists;
- real behavioral tests exist and pass;
- existing tests remain valid;
- lint/type checks pass where configured;
- build/package checks pass;
- graph validation passes;
- schema validation passes;
- security checks pass;
- deterministic behavior is tested;
- provenance/evidence is valid;
- documentation reflects the verified state;
- no unrelated changes are included;
- required CI checks are green.

## 7. Universal Agent OS Roadmap

### Phase 0 — Foundation & Governance

Establish the universal ontology, repository audit baseline, registry contract, runtime safety model, development governance, and evidence rules.

### Phase 1 — Universal Registry Core

Build the first runtime registry slice and then establish trustworthy source maps for implementations, adapters, platforms, frameworks, tools, and MCP assets.

Execution order:

`P1.1 Implementation Source Audit`
`P1.2 Adapter Source Audit`
`P1.3 Platform/Framework Source Audit`
`P1.4 Implementation Contract`
`P1.5 Adapter Contract`
`P1.6 First 1–3 audited implementations`
`P1.7 First real adapters`
`P1.8 Compatibility model`
`P1.9 Eligibility engine`
`P1.10 Typed graph edges`
`P1.11 Recommendation Engine integration`

**Verified state:** P1.1 through P1.11 are merged on `main`.

### Phase 2 — Implementation Ontology

Define Implementation independently from Skill. Minimum direction: stable ID, version, name, linked canonical skill, implementation type, provider, interface, inputs, outputs, requirements, constraints, limitations, provenance, evidence, and lifecycle/verification status.

**P2.1 — Complete.** Implementation is a first-class universal-registry entity governed by `meta/implementation-contract.schema.json`.

**P2.2 — Complete.** `registry/runtime.py` exposes typed Implementation access, deterministic Implementation-by-ID and Skill-to-Implementation lookup, and validates registered Implementation records against the normative contract during registry initialization. Behavioral regression tests cover successful lookup, unknown IDs, and contract rejection.

**Next:** no numbered P2.3 item is currently defined in the repository. The next Phase 2 slice must be derived from an audited architectural gap and documented before implementation; do not invent a roadmap item solely to advance the sequence.

### Phase 3 — Adapter Architecture

Define adapters as explicit compatibility bridges. Adapter metadata must identify the implementation, platform/framework/model constraints, input/output mappings, authentication/runtime requirements, compatibility state, limitations, and provenance.

### Phase 4 — Platform & Framework Registry

Promote existing curated framework/platform/model references into stable entities with versioning, aliases, lifecycle state, official provenance, and compatibility metadata.

### Phase 5 — Typed Universal Graph

Represent typed relationships across Goal, Capability, Skill, Prerequisite, Dependency, Tool, Implementation, Adapter, Platform, Framework, and Model. Enforce unique IDs, valid endpoints, valid relationship vocabulary, provenance integrity, deterministic generation, stale-reference detection, and forbidden-cycle rules.

### Phase 6 — Evidence Layer

Add evidence records with source, provenance, timestamp, version, confidence, methodology, freshness, and evidence type. Supported types include official documentation, implementation evidence, benchmark evidence, production evidence, community evidence, and experimental evidence.

### Phase 7 — Benchmark Registry

Create reusable benchmark entities and link measured results to skills, implementations, models, platforms, and relevant environments. Preserve methodology and reproducibility metadata.

### Phase 8 — Eligibility Engine

Determine which skills/implementations/adapters are actually eligible under a requested goal, constraints, runtime, platform, framework, model, security policy, and prerequisites before ranking them.

### Phase 9 — Deterministic Recommendation Engine

Implement discovery → eligibility → constraint filtering → ranking → calibration. Ranking must be deterministic and independently testable; the engine must not hide eligibility failures inside scores.

### Phase 10 — Recommendation Explanation

Produce machine-readable and human-readable explanations for why candidates were included/excluded/ranked, including evidence, constraints, compatibility, prerequisites, and uncertainty.

### Phase 11 — Skill Composition Engine

Compose multiple skills into valid capability plans while respecting dependencies, prerequisites, incompatibilities, and execution constraints.

### Phase 12 — Dependency Intelligence

Model prerequisites and dependencies deeply enough to support learning paths, execution ordering, impact analysis, and dependency risk detection.

### Phase 13 — Architecture Intelligence

Evolve architecture inference from `Goal → Static Architecture` into `Goal → Capabilities → Skills → Graph → Clusters → Patterns → Components → Tools → Runtime → Deployment → Risks → Blueprint`.

### Phase 14 — Architecture Pattern Registry

Create reusable architecture patterns with applicability conditions, required capabilities, components, trade-offs, constraints, evidence, and validation criteria.

### Phase 15 — Universal Blueprint Engine

Generate validated implementation blueprints containing selected capabilities, skills, implementations, adapters, components, runtime/deployment assumptions, risks, validation gates, and evidence references.

### Phase 16 — API

Expose universal registry, discovery, recommendation, compatibility, graph, evidence, and blueprint operations through stable machine-readable APIs.

### Phase 17 — CLI

Provide deterministic command-line access to registry discovery, validation, recommendation, graph inspection, compatibility checks, and blueprint generation.

### Phase 18 — Agent Interface

Expose the knowledge layer through an agent-oriented interface that supports goal-driven discovery and explainable execution planning.

### Phase 19 — MCP Interface

Expose the universal registry and reasoning operations through MCP without turning MCP into the canonical ontology. MCP is an adapter/protocol surface, not the definition of the knowledge model.

### Phase 20 — Learning Path Engine

Generate prerequisite-aware learning and execution paths from the dependency graph and evidence/maturity metadata.

### Phase 21 — Security & Supply Chain

Make trust, provenance, source integrity, dependency risk, malicious content, credential requirements, sandboxing, and policy constraints first-class compatibility signals.

### Phase 22 — Continuous Validation

Continuously validate schemas, references, provenance, graph integrity, deterministic generation, source freshness, security, and benchmark metadata.

### Phase 23 — Registry Compiler

Compile human-readable and machine-readable source assets into a deterministic registry artifact with traceable source provenance.

### Phase 24 — Search & Retrieval Layer

Provide lexical and semantic retrieval over the universal registry without bypassing eligibility or provenance rules.

### Phase 25 — Universal Query Engine

Support queries such as goal-to-capability, capability-to-skill, skill-to-implementation, implementation-to-adapter, compatibility, dependency, evidence, and architecture queries.

### Phase 26 — External Ecosystem Adapters

Add adapters for relevant agent ecosystems and registries while preserving one canonical ontology and avoiding duplicated skill definitions.

### Phase 27 — Developer Experience

Improve contribution tooling, validation feedback, templates, examples, documentation, local workflows, and integration ergonomics.

### Phase 28 — Public Knowledge Layer

Publish stable registry artifacts, documentation, graph views, APIs, and provenance-rich knowledge suitable for external agent builders.

### Phase 29 — Ecosystem Contribution Model

Define contribution rules, review gates, provenance requirements, benchmark standards, lifecycle management, and governance processes.

### Phase 30 — Autonomous Knowledge Maintenance

Automate source discovery, stale-data detection, compatibility drift detection, evidence refresh, and candidate updates while retaining human review for substantive changes.

### Phase 31 — Continuous Intelligence Loop

Use observed outcomes, benchmarks, failures, compatibility changes, and new ecosystem evidence to continuously improve the registry and recommendation quality.

### Phase 32 — Universal Agent Knowledge Layer

Final target: an open universal knowledge layer connecting goals, capabilities, skills, implementations, tools, models, frameworks, platforms, adapters, dependencies, evidence, benchmarks, and architectures.

## 8. Current Verified Development State

The repository contains a machine-readable universal registry contract and a read-only deterministic runtime slice. The registry now contains a small verified set of goals, capabilities, canonical skills, and the audited `implementation/code-reviewer-system` Implementation record. Implementation runtime access is contract-validated; broader implementation, adapter, platform, framework, model, benchmark, and architecture population remains intentionally limited to audited records.

The existing framework/model catalogue is `meta/frameworks.md`. It mixes agent frameworks, computer-use/browser systems, protocols/standards, and foundation models in a human-oriented curated reference. This is source material, not yet the canonical universal registry.

The repository also contains real MCP assets including `mcp/`, `examples/mcp-server/`, and MCP design/validation documents. These are existing implementation/protocol assets to be audited and linked through the universal ontology rather than copied into new canonical skill definitions.

## 9. Current Execution Position

**Verified completed sequence:**

- Phase 0 governance and registry foundation.
- P1.1 Implementation Source Audit.
- P1.2 Adapter Source Audit.
- P1.3 Platform/Framework Source Audit.
- P1.4 Implementation Contract.
- P1.5 Adapter Contract.
- P1.6 first audited Implementation slice.
- P1.7 first real Adapter slice.
- P1.8 Compatibility Model.
- P1.9 Eligibility Engine.
- P1.10 Typed Universal Graph.
- P1.11 Recommendation Engine integration.
- P2.1 Implementation Ontology contract unification.
- P2.2 typed Implementation runtime access and contract validation.

**Current mandatory action:**

Perform the Phase 2 post-P2.2 architectural audit and document the next vertical slice from an evidence-backed gap. Do not reopen completed P1 work and do not invent a P2.3 requirement without repository evidence.

## 10. Vertical-Slice Strategy

Do not migrate the entire skill corpus first. Prove the architecture with one capability and one to three canonical skills, backed by real implementations, at least one real adapter, evidence, compatibility metadata, tests, graph edges, and deterministic recommendation behavior. Only then scale the pattern to additional domains.

## 11. Source-of-Truth Hierarchy

When sources disagree, prefer:

1. machine-readable validated contract/data;
2. verified runtime behavior and tests;
3. canonical source files referenced by provenance;
4. current architecture/governance documents;
5. curated metadata/reference documents;
6. historical plans and stale roadmap documents.

Historical documents remain useful context but must not silently override the current runtime architecture.

## 12. Change Control

When a roadmap task is completed, update this document only with verifiable evidence: commit/PR, tests, CI, and resulting behavior. Never mark a phase complete because code was drafted or because a specification exists.

## Current roadmap state

P1.1 through P1.11 are verified on `main`. P2.1 and P2.2 are also verified on `main`. P1.9 provides the deterministic eligibility boundary in `registry/eligibility.py` with `meta/eligibility-contract.schema.json`; compatibility is evaluated before ranking and prerequisite evaluation is not fabricated where authoritative prerequisite records do not exist.

### P1.10 — Typed Universal Graph

P1.10 is implemented as an additive typed graph slice in `graph/universal_graph.json`, governed by `meta/universal-graph.schema.json` and exposed through deterministic `UniversalRegistry.graph_edges()`. Endpoint types are checked against registry entities, self-loops are rejected, and provenance is required. The existing `data/SKILLS_GRAPH.json` remains the generated skill-corpus graph; it is not silently replaced by the universal graph.

### P2.2 — Typed Implementation Runtime

P2.2 is implemented in `registry/runtime.py`. `ImplementationRecord` defines the runtime shape, `resolve_implementation()` resolves a canonical Implementation ID, `implementations_for_skill()` returns deterministic linked Implementations, and registry initialization validates every registered Implementation against `meta/implementation-contract.schema.json`. Regression coverage is in `tests/test_registry_implementation_runtime.py`.
# Repository Development Knowledge

**Status:** Governing development knowledge for the Universal Agent Knowledge Layer
**Version:** 1.0
**Updated:** 2026-10-06
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

The search projection contract is now verified: `meta/search-index.schema.json` validates `docs/search-index.json`, regression tests enforce canonical-path parity with `docs/api/skills.json`, and a real stale Kanban entry was detected and reconciled. The source/package runtime boundary is now explicit through `cli/search_runtime.py` and packaged `data/search-index.json`; the remaining gap is the deterministic query/ranking contract for Issue #86. Do not implement a second index or parser.

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

## Post-P2.2 Evidence Runtime Integration — Verified 2026-10-01

PR #223 integrated the existing validated EvidenceRuntime into UniversalRegistry. The runtime now exposes deterministic typed Evidence resolution and entity-support traversal. Exact-head CI passed before merge at 642e968879e9b6bfc8e7f9b2a44d12544585fc18.

Next: perform a fresh universal-registry runtime architecture audit. No numbered P2.3 item is defined.

## Post-P2.2 Compatibility Runtime Integration — Verified 2026-10-01

A fresh universal-registry runtime audit found that Compatibility had a validated dedicated runtime but the UniversalRegistry facade still exposed raw-storage access through compatibility_for(). The selected next vertical slice is to integrate the existing CompatibilityRuntime, expose typed resolve_compatibility(), and route filtering through the validated runtime.

No numbered P2.3 requirement is being invented. No compatibility records or external claims are being added.

**Verification:** PR #227 exact head `9e4c7608246092ce902384d10d87e2812330de8a` passed Test Suite, Security Scan, PR Checks, Build & Verify Wheel, and Auto Label before merge as `ba9682b26ea59b18f21eb017b6f239f735c4dec3`.

**Status:** VERIFIED — Compatibility runtime access is integrated into UniversalRegistry; no new compatibility facts or external claims were introduced.


## Phase 0 Workflow Permission Isolation — Verified 2026-10-02

The workflow-governance inventory identified `.github/workflows/validate-graph.yml` as a concrete least-privilege gap: PR/main graph validation and trusted-main generated writes previously shared a broader write permission boundary.

The implemented correction isolates responsibilities. `build-and-validate` now has `contents: read` only. `generate-main-graph` has `contents: write`, runs only for pushes to trusted `main`, and depends on successful validation. `quality-report` also runs only on trusted `main` and depends on both validation and graph generation, preventing the graph and quality writers from racing within the same workflow. The repository-wide `auto-commit-main` concurrency boundary is preserved.

**Verification:** PR #232 merged as `d89bb26bfd3e55f513b3c07e6ebb5ee2f84ba85b`. Security Scan, PR Checks, Test Suite, Build & Verify Wheel, and Auto Label passed; Dependabot Review Gate was skipped. The merged workflow was re-read from live `main` and confirms the intended job-level permissions and dependencies.

**Control-plane finding:** Live branch inspection reports `main` as unprotected with required-status-check enforcement off. This is recorded as a repository governance fact rather than inferred YAML behavior; no high-impact branch-protection change was made in this cycle.

**Next:** complete observable control-plane reconciliation, then perform the fresh universal-registry runtime architecture audit required before selecting the next vertical slice.


## Post-P2.2 Skill Runtime Facade Integration — Verified 2026-10-02

A fresh universal-registry runtime audit identified a remaining abstraction-boundary gap. `SkillRuntime` already provided deterministic canonical Skill resolution, capability traversal, implementation traversal, unknown-ID rejection, and defensive snapshots, but `UniversalRegistry` still bypassed it with raw registry access.

The selected vertical slice integrated the existing `SkillRuntime` into `UniversalRegistry`. The facade now exposes typed `resolve_skill()` and `capabilities_for_skill()` and delegates `implementations_for_skill()` to the dedicated runtime. The `TYPE_CHECKING` boundary prevents a runtime import cycle.

**Verification:** PR #234 exact head `2ec1690606b26b1727567b6c421ea538b9a07d3a` passed Security Scan, PR Checks, Test Suite, Build & Verify Wheel, and Auto Label before merge as `37b2a529555db2e5db34713ffcb8e3b72083cfb5`.

**Next:** perform another fresh universal-registry runtime architecture audit. Do not invent a numbered P2.3 requirement and do not add ontology facts without authoritative evidence.


## Post-P2.2 Capability Runtime Facade Integration — Verified 2026-10-02

A fresh universal-registry runtime audit identified the next remaining read-boundary gap. `CapabilityRuntime` already provided deterministic Capability resolution plus Implementation and Adapter traversal, but `UniversalRegistry` had no typed Capability facade.

The selected vertical slice integrated the existing `CapabilityRuntime` into `UniversalRegistry`. The facade now exposes `resolve_capability()`, `implementations_for_capability()`, and `adapters_for_capability()`. The `TYPE_CHECKING` boundary prevents a runtime import cycle.

**Verification:** PR #236 exact head `ccc0902bcb87714c8709d9a8f5d6d100554edb2f` passed Security Scan, PR Checks, Test Suite, Build & Verify Wheel, and Auto Label before merge as `8fc4dc8f6423b6b39ec2218f077a9d153b4560da`.

**Next:** perform another fresh universal-registry runtime architecture audit. Do not invent a numbered P2.3 requirement and do not add ontology facts without authoritative evidence.


## Post-P2.2 Goal Runtime Facade Integration — Verified 2026-10-02

A fresh universal-registry runtime audit identified the remaining public raw-storage access path in Goal resolution and Goal-to-Skill traversal. There was no dedicated Goal runtime boundary.

The selected vertical slice added `GoalRuntime`, integrated it into `UniversalRegistry`, exported it from the registry package, and delegated `resolve_goal()` and deterministic `skills_for_goal()` through the new runtime. Goal traversal reuses the validated Capability and Skill runtime boundaries rather than duplicating their storage access.

**Verification:** PR #238 exact head `0d45fd7b7a741c8984fbe5a90b1abe7e8570b744` passed Security Scan, PR Checks, Test Suite, Build & Verify Wheel, and Auto Label before merge as `3290ebc88060fca07e944cd31ad31d392982ca3d`.

**Next:** perform another fresh universal-registry runtime architecture audit. Do not invent a numbered P2.3 requirement and do not add ontology facts without authoritative evidence.


## Runtime Facade Boundary Audit — 2026-10-02

After the Goal runtime facade was verified, the public UniversalRegistry access surface was re-audited. Dedicated runtime boundaries now cover Goal, Capability, Skill, Evidence, and Compatibility. Implementation and Adapter remain intentionally implemented in the core runtime because their typed record contracts, initialization validation, defensive snapshots, and relationship checks already provide the required boundary. Graph edges are likewise schema- and relationship-validated before defensive return.

No additional runtime class was invented merely for symmetry. The next work item must come from a deeper invariant or consumer-behavior gap demonstrated by repository evidence.


## Universal Registry Runtime Data-Schema Validation — Verified 2026-10-02

A fresh post-facade audit identified a runtime integrity gap: `UniversalRegistry` loaded `registry/universal_registry.json` and ran semantic/entity/graph validators, but did not first validate the loaded document against a schema describing the actual registry data shape.

The first implementation attempt incorrectly targeted `meta/universal-registry.schema.json`. CI exposed that this file defines the registry ontology/contract vocabulary (`schema_version`, `entity_types`, `relationship_types`), while the live seed uses `registry_version` and `entities`. The implementation was corrected rather than weakening validation.

The final slice introduced `meta/universal-registry-data.schema.json` for the seed shape. It validates common entity metadata, Goal/Capability/Skill structure, Evidence, Compatibility, and delegates Implementation/Adapter structural shapes to their dedicated contracts. Cross-schema references are resolved locally through `referencing.Registry`; runtime validation therefore remains deterministic and does not depend on network retrieval.

The schema intentionally permits the repository's existing Skill version value `"3"`; version-format constraints remain owned by the specific contract that defines them. Provenance `source_type` is structural while the existing semantic validator retains responsibility for requiring a traceable `source`, preserving established error behavior.

**Verification:** PR #241 exact final head `8ad05dfc995db49da847ea479e06e13bec80d2e1` passed Security Scan, PR Checks, Test Suite, Build & Verify Wheel, and Auto Label before squash merge as `93c50c3616a7c558b483f341f44a91509ed032ca`.

**Engineering lesson:** when multiple schemas exist, first establish which artifact each schema governs. Runtime validation must target the schema of the loaded artifact, not a related ontology-definition schema.


## Security Stub Migration Batch 01 — 2026-10-02

Corpus audit identified nine remaining stubs in category 14-security. The batch upgraded all nine to the repository's evidence-backed content gate.

The migration deliberately removed placeholder descriptions and unsafe example patterns. Security skills now state explicit boundaries: audit logging must not become a secret sink; harm detection is a risk gate rather than an authorization oracle; human approval is action-bound and deny-by-default; authorization is distinct from authentication; privacy regexes are incomplete; rate limiting is not a substitute for provider quotas; rollback requires postcondition verification; subprocess timeouts are not sandboxes; and regex secret scanning is not complete protection.

Authoritative references were added for OWASP logging/authorization/secrets guidance, NIST AI risk-management guidance, RFC 6585, Python subprocess/hash/context-manager behavior, GitHub secret scanning/push protection, and the NIST Privacy Framework.

**Verification:** PR #243 final head `a76f44379b1fba4a6667e9efce04a5db6c912d97` passed the final validation matrix before squash merge `40fb35aa6c54438f08062c89c118815262b6fe98`.

**Automation verification:** the hardened `quality-report.yml` post-merge trigger regenerated `meta/QUALITY-REPORT.md` as GitHub Actions commit `ac8aacb5982018d2ee57a2953924dd74a9013e20`. The generated report verifies 374 skills: 202 battle-tested, 159 enriched, 13 stubs, 0 invalid; category 14-security is fully migrated at 13 battle-tested, 0 stubs.

**Next:** use the generated report as the authoritative baseline for the remaining 13-stub migration backlog.


## Post-P2.2 Goal Capability Traversal Slice — 2026-10-02

A fresh consumer-behavior audit identified a concrete runtime surface gap in the universal traversal contract. The repository documents the deterministic path `Goal → Capability → Skill → Implementation → Adapter`, but `GoalRuntime` exposed only `resolve_goal()` and `skills_for_goal()`. Consumers needing the immediate Goal→Capability relationship still had to inspect the Goal record directly.

The selected vertical slice adds typed deterministic `capabilities_for_goal()` access to `GoalRuntime` and `UniversalRegistry`. `skills_for_goal()` now obtains its Capability inputs through that runtime boundary, preserving deterministic ordering and defensive snapshots while avoiding duplicated raw-storage traversal.

Behavioral coverage adds deterministic Capability resolution from `goal/software-engineering` and snapshot-isolation coverage.

No registry records or external ecosystem claims were added. No numbered P2.3 requirement was invented.

**Verification:** PR #238 exact head `0d45fd7b7a741c8984fbe5a90b1abe7e8570b744` passed Security Scan, PR Checks, Test Suite, Build & Verify Wheel, and Auto Label before merge as `3290ebc88060fca07e944cd31ad31d392982ca3d`.

**Status:** VERIFIED — the typed Goal→Capability runtime boundary is merged to `main`, covered by deterministic traversal and defensive-snapshot tests, and routed through the validated Capability boundary.


## Kanban Task Management Skill — Verified 2026-10-03

PR #267 added the canonical `skills/15-orchestration/kanban-task-management.md` skill to `main`. The skill defines a portable file-backed Kanban contract for persistent agent task state, explicit lifecycle transitions, dependency-aware ready-set computation, controller/CAS concurrency control, transition receipts, and completion evidence gates. YYLO is documented only as an external reference implementation.

A review finding in PR #267 identified an inaccurate YYLO dependency-creation example. The example was corrected to create the task first and then add the dependency with the documented `yy ledger deps add` command, using the task ID actually returned by creation.

**Verification:** PR #267 final head `e8b866c75438e9456f6e11a6ee196cc979eb52da` passed Validate Skills, Schema Enforcement, Security Scan, PR Checks, Test Suite, Build & Verify Wheel, Validate Skills Graph, Check Links, AST Sweep, Skill Upgrade Detector, Skill Quality Report, and Agent Skills Distribution Audit. The pull request was squash-merged to `main` as `8a242e37e9bd5a9e694d4e2ede7fa1c9674be03c`.

**Integrity note:** PR #247 was closed without merge because its Capability↔Skill symmetry fix was already present on current `main`. No duplicate runtime patch was introduced.


## Universal Registry Behavioral-Evaluation Audit — 2026-10-03

A fresh architecture/consumer audit followed the verified Goal runtime facade and registry data-schema validation. Provenance, Evidence, integrity, memory-safety guidance, and action-governance skills are already covered by existing repository contracts or skills. The concrete remaining boundary gap was Benchmark: the registry contains a first-class benchmarks collection, but it used only the generic entity schema and had no typed runtime facade.

The selected smallest slice adds meta/benchmark-contract.schema.json, binds entities.benchmarks to that contract, adds BenchmarkRuntime, and exposes deterministic resolve_benchmark() plus benchmarks_for_entity() through UniversalRegistry. The test fixture is synthetic and repository-local; no benchmark result, ranking, model claim, or external ecosystem claim is introduced.

**Verification status:** implementation and focused regression tests are on branch runtime/benchmark-integrity-slice; exact-head CI is pending.


## Verified development update — 2026-10-03

- PR #272 established the dedicated Benchmark contract and typed BenchmarkRuntime boundary; PR #274 supplied the final contract-integrity and regression-test fixes. The final #272 head `4738303caeb6a9129af8a0f84cab4219aade5084` passed its required CI matrix before merge.
- PR #273 established deterministic anti-slop enforcement for changed canonical skills; PR #275 resolved rename detection and lowercase lifecycle-state false positives. The final #273 head `4477d33d846c68d71b666e6c283c8787312e023f` passed its required CI matrix before merge.
- The live main merge commits are `db474059fbe0efa56ca167a7108146323c9cf857` for benchmark runtime and `90f9422954936e054adc630ad723e6165074492c` for anti-slop.
- The merged main commits above currently have no associated workflow runs exposed by the available commit workflow-run endpoint. This is not treated as post-merge CI success; the exact PR-head CI evidence remains the verification evidence for those merges.
- The next engineering action remains the fresh universal-registry runtime/consumer audit. The audit must start from live main and confirm coverage before introducing another contract/runtime slice.


## Universal Graph Relationship Runtime Boundary — 2026-10-03

A fresh post-freshness audit found a semantic fail-open path in the typed Universal Graph runtime. The graph schema declares a forward-compatible relationship vocabulary, while the runtime has explicit semantics only for the six relationships currently used by the canonical graph.

The previous fallback silently accepted schema-valid deferred relationships. The selected correction preserves the schema vocabulary but makes the runtime-supported set explicit and rejects unsupported relationship types before endpoint/reference semantics are evaluated.

No new graph relationship was invented and the canonical eight graph edges were left unchanged.

**Verification target:** the existing graph remains valid; a synthetic schema-valid "alternative_to" edge fails deterministically with "Unsupported universal graph relationship: alternative_to".

**Engineering lesson:** a broad schema vocabulary is not evidence of runtime support. Forward-compatible enum values must remain outside the trusted runtime boundary until their semantic invariants are implemented and tested.


## 2026-10-03 — Documentation synchronization gate

The post-merge quality regeneration produced the authoritative current corpus state: 375 skills, 216 battle-tested, 158 enriched, 0 stubs, 0 invalid, and 1 intentional test fixture. A documentation audit found stale operational snapshot/roadmap entries that still described pre-migration counts and a pending Universal Graph runtime merge. These were synchronized without rewriting historical records.

The repository governance was strengthened with a mandatory Documentation Preflight in `AI_CONSTITUTION.md` and `AGENTS.md`. Agents must read authoritative state documents, verify them against live implementation/generated artifacts/CI evidence, synchronize drift before unrelated work, re-read the affected documents, and cannot report COMPLETE while the preflight remains unresolved.


## 2026-10-03 — Release documentation drift audit

Fresh documentation preflight found `meta/PYPI_RELEASE_PLAN.md` describing an obsolete 1.0.0/manual-token/publish.yml release process. The executable repository contract is now semantic-release plus `.github/workflows/zero-touch-release.yml`, with tag/version verification, build verification, and PyPI OIDC Trusted Publishing. The plan was synchronized without changing release runtime behavior.


## 2026-10-03 — CLI Search Consumer

Issue #86 now has a deterministic lexical search contract in `meta/SEARCH_CLI_CONTRACT.md`. `cli/search_engine.py` consumes only the loaded generated documents; it does not create a second index, parser, or semantic ranking layer. Verification must include focused tests, full CI, wheel installation, and actual installed `skills-tree search` execution.

Post-merge evidence: PR #299 merged as `7302d0780b2857bdd2f54363a2e6158eafc45292`. Exact-head Test Suite passed on Python 3.11/3.12/3.13; Security Scan, PR Checks, Build & Verify Wheel, and Auto Label passed. Build & Verify also installed the produced wheel and successfully executed `skills-tree search "memory" --limit 1 --format json`. An earlier wheel run exposed the missing runtime `jsonschema` dependency; that dependency was declared explicitly before the successful verification.


## 2026-10-03 — Discovery registry context

The generated machine-readable skill index now projects optional UniversalRegistry context only for exact registered canonical skills. The projection preserves canonical source ownership, exposes explicit capability/implementation/evidence/provenance/freshness references when declared, and does not infer context for uncovered skills. The search index remains a search-only corpus.


## 2026-10-03 — Discovery registry context verification

PR #300 merged as `4ff041511f2291e826b2a32c2cc72f36f8f023cb`. Final head `52ae305ad504416114d7efdd8313eff8f931f57d` passed Test Suite on Python 3.11/3.12/3.13, Security Scan, Build & Verify Wheel, PR Checks, Validate Skills Graph, and Auto Label. The wheel gate also executed the installed CLI search successfully.

The focused registry-context test exposed an unrelated pre-existing schema/artifact date-format mismatch (`docs/api/skills-schema.json` accepts `YYYY-MM` while some generated `added`/`last_updated` values contain day-level dates or fixture text). The mismatch was not broadened into this PR; it is now a separate audit finding. Future schema reconciliation must derive its contract from the canonical generator and corpus rather than weakening tests.


## 2026-10-03 — Generated discovery artifact reconciliation

PR #301 corrected the canonical Kanban body metadata and PR #302 synchronized the generated `docs/api/skills.json` and `docs/api/skills.yaml` projections. PR #301 exact-head CI passed Test Suite on Python 3.11/3.12/3.13, Security Scan, Build & Verify Wheel, PR Checks, Validate Skills Graph, Agent Skills Distribution Audit, Schema Enforcement, Check Links, Skill Quality Report, Validate Skills, AST Sweep, Skill Upgrade Detector, and Auto Label. PR #302 passed Test Suite on Python 3.11/3.12/3.13, Security Scan, Build & Verify Wheel, and PR Checks before merge.

The resulting machine-readable projection now matches the canonical source for the affected date fields. The next audit target is the `agent-skills/` projection and its provenance/canonical-source boundary.


## 2026-10-04 — Agent Skills reconciliation hard gate

A fresh corpus audit found that the existing reconciler already computed eligible_missing, but its default command returned success regardless of that result. This meant a newly eligible canonical skill could become absent from the Agent Skills projection without failing the distribution workflow.

The correction is intentionally small: reconciliation remains read-only by default, while --check turns the existing report into an enforcement boundary. The check fails for eligible missing projections, deterministic projection drift, required provenance renames, stale/ambiguous provenance, unexpected packages outside the explicit auxiliary boundary, and duplicate target names after collision resolution.

The Kanban skill was the concrete current example. It is eligible under the existing generator gates and is now represented by its deterministic projection; no Kanban-specific code path was added.

The important design distinction is that raw canonical collision groups are not themselves errors. The existing category-qualified resolver is the intended deterministic mechanism. Only a collision that survives resolution is invalid.

This keeps skills/ authoritative, avoids a second eligibility registry, and turns reconciliation from an informational report into a machine-enforced invariant without changing blocked legacy packages. PR #305 merged to main as `a9a649481c68bf0dd33447a2238174ebd8b79a4b` after exact-head verification; the merged baseline is 375 canonical skills, 258 eligible, 117 blocked, and 296 Agent Skills packages.


Legacy Agent Skills package names are a compatibility concern, not a reason to weaken the deterministic projection contract. When a valid canonical source has an older non-deterministic package name, reconciliation must require the deterministic package to exist while classifying the older package as legacy compatibility. This avoids mass renames while still proving that every eligible canonical skill has its deterministic projection.

## Verified Slice — Agent Skills Discovery Publication — 2026-10-04

The Agent Skills discovery publication boundary is now an executable, verified projection rather than a roadmap-only requirement.

Canonical and projection boundaries remain unchanged:
- `skills/` is canonical.
- `agent-skills/` is deterministic projection.
- `tools/reconcile_agent_skills.py --check` remains the hard reconciliation invariant.
- `docs/api/skills.json` remains the machine-readable registry projection.
- Search projections remain separate and are not reused as discovery catalogs.

Publication implementation:
- `tools/build_agent_skills_discovery.py` generates a deterministic, name-sorted discovery index from the existing reconciled projection.
- `meta/agent-skills-discovery-index.schema.json` defines the discovery contract.
- `tools/verify_agent_skills_discovery.py` verifies exact local or served bytes against SHA-256 digests.
- `.github/workflows/deploy-pages.yml` remains the only Pages deployment authority and now publishes the Agent Skills artifacts and discovery index in the same build artifact.

Important implementation findings:
1. Direct execution of a tooling script required an explicit repository-root import path before importing the existing reconciliation module.
2. MkDocs strict mode exposed a stale link from `docs/cli.md` to a file outside the documentation tree; the link was changed to an absolute GitHub source URL instead of weakening strict mode.
3. GitHub Pages artifact publication excludes hidden files by default; `.well-known` therefore required `include-hidden-files: true` on `actions/upload-pages-artifact`.
4. The served-byte verifier is the final publication gate; successful deployment alone is not sufficient evidence.

Final verification:
- Main HEAD: `e306a810c7cabac25b9f19fa4aeeab2e62ed0e3f`.
- Pages run: `37199284169`.
- Build job: success.
- Deploy job: success.
- Served discovery verification: success.
- 258 eligible Agent Skills entries are represented in the deterministic discovery index.
- Root-level `/.well-known/agent-skills/index.json` is intentionally not claimed because the current GitHub Pages topology is a project site under `/skills-tree`.

**Rule:** future discovery changes must reuse this publication boundary. Do not create another generator, reconciler, index, or deployment path.

## Verified Slice — Graph Projection Governance — 2026-10-04

Audit finding: the repository had two graph writer workflows. `build-graph.yml` generated `data/SKILLS_GRAPH.json` and a UI copy, while `validate-graph.yml` independently generated and validated the graph. This created competing workflow authority and allowed `docs/api/graph.json` to become stale.

Correction: PR #315 removed the duplicate `build-graph.yml` workflow and made `validate-graph.yml` the single graph generation/validation writer. The same generated bytes are copied to `docs/api/graph.json` for the existing UI consumer; no second graph generator or index was introduced.

The validation boundary now executes the real JSON Schema contract using the graph schema and its referenced skill/edge schemas, then checks node counts, edge counts, duplicate nodes, self-loops, dangling endpoints, invalid sources, and duplicate edges.

During implementation CI exposed four real schema drift cases: generated `requires_count` was undeclared; empty prerequisite arrays were rejected; generated REQUIRES edges carried `source_method`; and a valid skill slug beginning with a digit (`3d-scene-understanding`) was rejected. The schemas were corrected to match the established generator contract rather than weakening the generated data.

Final main verification: graph generation produced 375 nodes, 240 edges, 9 REQUIRES edges, and 0 warnings. `data/SKILLS_GRAPH.json` and `docs/api/graph.json` are byte-identical on main. PR #315 merged as `5c5720d61ed757e7d0f94cdfb3309ac8eb0d213f`; generated graph projections were subsequently refreshed on main as commit `9b06e6177dd7504d158626d926b402d47b3a1203`.

Rule: machine-readable graph consumers must consume the generated graph projection; do not add another graph writer, generator, or parallel graph catalog.

## Verified Slice — JSON-LD Export Governance — 2026-10-04

The audit disproved the documented existence of a dedicated `jsonld-export.yml` workflow on current main. JSON-LD generation is part of `tools/export_skills.py`, and `export-skills.yml` is the single generated-main writer for the API and JSON-LD projections.

The actual gap was trigger/validation coverage: `export-skills.yml` watched `skills/**/*.md` but not `tools/export_skills.py` or `registry/universal_registry.json`, and it committed generated JSON-LD without validating its structural relationship to the canonical `skills.json` registry.

The correction adds a deterministic read-only validator at `tools/verify_jsonld_export.py` plus focused tests. The validator checks JSON validity, TechArticle type, canonical skill ID/name agreement, ItemList ordering/counts, and duplicate URLs. The existing export workflow now invokes it and tracks exporter/registry changes.

Do not add a second JSON-LD generator or workflow. JSON-LD remains a projection of the existing skill export pipeline.


## Verified Slice — Release Authority Consolidation — 2026-10-04

The release audit found a real writer overlap: `release-package.yml` was independently triggered by `v*.*.*` tags and created/updated GitHub Release assets, while `zero-touch-release.yml` was already the authoritative production release pipeline and also wrote the same release.

The correction preserves the catalog packaging capability but moves it into the existing `zero-touch-release.yml` Job 4, using the exact release tag checkout. The catalog ZIP and MANIFEST are now attached in the same authoritative release job as the wheel and sdist. The duplicate tag-triggered workflow was removed.

This keeps one production release authority, one manual recovery path, and no competing GitHub Release writer.

Rule: release packaging is a projection of the authoritative release pipeline; do not recreate a separate tag-triggered publisher.


## Full Repository Re-Audit — 2026-10-04

A fresh audit against live `main` verified the canonical/projection architecture and found no justification for another graph, search, JSON-LD, Agent Skills, discovery, Pages, or release writer.

The current workflow inventory is 40 files. The previous 42 count is historical.

The concrete security finding was that the blocking security workflow enforced Gitleaks but did not enforce Python SAST or dependency vulnerability auditing. The security gate is being hardened with Bandit over `api/`, `cli/`, `mcp/`, `registry/`, and `tools/`, plus `pip-audit --strict` over the installed project environment.

The current generated quality report verifies 375 skills with 0 stubs and 0 invalid entries. The Universal Registry remains intentionally evidence-backed and small; no unsupported entities or ecosystem claims are being added to satisfy the audit.

Control-plane branch protection remains an external blocker because the connected GitHub integration returned HTTP 403 when reading branch protection. Issue #159 remains the tracking authority.

The complete audit evidence is recorded in `meta/audits/FULL_REPOSITORY_AUDIT_2026-10-04.md`.


## Full Repository Re-Audit — FINAL VERIFIED — 2026-10-04

PR #318 merged as `2ef8a3fe9c987032d614a0e2a026cc4152867204`. The repository-code remediation from the full re-audit is complete. Security Scan now blocks on Gitleaks, Bandit high-severity/high-confidence findings, and `pip-audit --strict`. Exact-head Security Scan, Test Suite, Build & Verify Wheel, Validate Skills Graph, and PR Checks all passed before merge.

The audit also reconciled current-state workflow count to 40, synchronized active memory/state, and preserved historical reports without treating them as current architecture. No competing generated source, index, graph, discovery, Pages, or release writer was introduced.

The remaining branch-protection requirement is a GitHub control-plane action tracked by issue #159 and is not marked complete from repository evidence alone.


## 2026-10-04 — Post-publication consumer/projection audit closure

A fresh audit was completed against live `main` at `168f88d64d8d397fa9d189ebeaa731a5a461d826`. The audit rechecked the Universal Registry typed runtime boundary, generated discovery/search/graph/JSON-LD projections, Agent Skills reconciliation/discovery, recommendation and blueprint registry context, and the release/security control boundaries. No new evidence-backed invariant gap was found and no competing implementation was justified.

Issue #276 was closed with this evidence-bound conclusion. No numbered P2.3 requirement was invented and no speculative implementation was introduced.

The remaining material blocker is Issue #159: GitHub `main` is currently unprotected with required status checks off, while the connected integration cannot modify the branch-protection control plane. Repository rulesets are currently empty.

## 2026-10-04 — Zero-Touch Release Idempotency Fix

The post-publication release audit found that `.github/workflows/zero-touch-release.yml` treated `pyproject.toml` matching the latest Git tag as evidence that a new release existed. After v1.72.6, ordinary `docs:` commits therefore rebuilt and attempted to upload the already-published v1.72.6 artifacts, producing the expected PyPI `400 File already exists` rejection.

The authoritative release workflow was corrected to use `semantic-release version --print` as the pre-mutation release decision. When the calculated next version equals the current project version, the workflow records `released=false` and skips build, PyPI publication, and GitHub Release attachment. When a real version bump exists, the workflow performs the release and fails closed if the expected tag or stamped project version is inconsistent.

PR #320 merged as `4a09394332a90aa5ec172d3dc2b31fa38b740402`. The resulting patch release v1.72.7 passed Semantic Release, Build & Verify, PyPI OIDC preflight/publication, and GitHub Release asset attachment. The existing single release authority and Trusted Publisher configuration were preserved; no `skip-existing` masking was introduced.

The next verification is an ordinary documentation-only main commit. It must produce a successful semantic-release gate with `released=false` and no build or PyPI publication jobs. This is the regression test for the v1.72.6 failure mode.

## Final Live Audit Reconciliation — 2026-10-06

The latest live audit supersedes only the active-state claims above where they conflict with current main; older dated paragraphs remain historical records.

Current verified control baseline:
- 45 GitHub Actions workflow files are present and classified in `meta/WORKFLOW_INVENTORY.md`.
- `skills/` remains the canonical source; generated Agent Skills, graph, search, and JSON-LD artifacts remain projections.
- The quality corpus contains 382 skill files including one intentional sandbox fixture; the production/public canonical corpus contains 381 skills across 17 categories.
- Agent Skills reconciliation currently verifies 264 eligible projections, 118 blocked canonical entries, and 302 existing packages.
- Graph projections are byte-identical at 382 nodes / 250 edges; search projections are byte-identical.
- DevLens is read-only and not an authoritative repository writer.
- Activation benchmark evidence is fail-closed for zero observations, partial versus complete corpus status is explicit, and unknown case IDs / duplicate run IDs are rejected.

Current evidence boundary:
- Issue #357 remains open for real agent-runtime activation traces. No empirical activation/reliability claim is valid without those traces.
- Issue #336 remains open for retrieval evidence freshness/reproducibility. The historical `benchmarks/memory/retrieval-accuracy.md` result table is not current evidence.
- No new skill, search engine, routing authority, or competing projection generator is justified by the current evidence.
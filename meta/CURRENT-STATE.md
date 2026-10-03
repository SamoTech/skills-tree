# Skills Tree — Live Repository State

> Maintained as a point-in-time operational snapshot. This file records verified state used for engineering and governance decisions.

## Verified snapshot

- Snapshot date: 2026-10-03
- Live `main`: authoritative and must be verified from the Git ref before execution; this document intentionally does not hard-code `main`'s own current commit because updating this document creates a new `main` commit.
- Latest verified implementation synchronization: Goal runtime facade integration merged to `main` as `3290ebc88060fca07e944cd31ad31d392982ca3d`; Capability runtime facade remains verified at `8fc4dc8f6423b6b39ec2218f077a9d153b4560da`; Skill runtime facade remains verified at `37b2a529555db2e5db34713ffcb8e3b72083cfb5`.
- PR #223 remains the implementation baseline for the post-P2.2 Evidence runtime slice, merged as `642e968879e9b6bfc8e7f9b2a44d12544585fc18`.
- PR #224 merged on 2026-10-01 and synchronized the affected P2 architecture, development knowledge, audit, decision memory, and current-state documentation.
- Quality report: current generated report `meta/QUALITY-REPORT.md` verifies 375 skill files: 207 battle-tested, 158 enriched, 10 stubs, 0 invalid.
- Quality-report figures are current only at the generated-report verification point; historical verification sections retain their original counts.
- `main` current HEAD was verified from the live Git ref as `a3609bebfdf54b0ccc6735e81588619a355e4aba` at the latest snapshot check.

## Current verified architecture state

- The canonical skill source is `skills/`.
- The universal registry is a read-only, deterministic machine-readable capability layer with typed runtime access.
- P2.1 Implementation ontology contract unification is verified.
- P2.2 typed Implementation runtime access and contract validation are verified.
- The post-P2.2 Evidence runtime slice is verified: `UniversalRegistry` exposes typed deterministic `resolve_evidence()` and `evidence_for_entity()` access through the existing validated `EvidenceRuntime`.
- The post-P2.2 Compatibility runtime slice is verified: `UniversalRegistry` exposes typed deterministic `resolve_compatibility()` and routes `compatibility_for()` through the existing validated `CompatibilityRuntime`.
- The post-P2.2 Skill runtime facade slice is verified: `UniversalRegistry` exposes typed deterministic `resolve_skill()` and `capabilities_for_skill()`, and delegates `implementations_for_skill()` through the existing validated `SkillRuntime`.
- The post-P2.2 Capability runtime facade slice is verified: `UniversalRegistry` exposes typed deterministic `resolve_capability()`, `implementations_for_capability()`, and `adapters_for_capability()` through the existing validated `CapabilityRuntime`.
- The post-P2.2 Goal runtime facade slice is verified: `UniversalRegistry` exposes typed deterministic `resolve_goal()` and `skills_for_goal()` through the dedicated validated `GoalRuntime`.
- The Evidence slice added no new Evidence records, provenance claims, compatibility facts, provider/platform/framework/model claims, or MCP classifications.
- `skills/15-orchestration/kanban-task-management.md` is present on `main` as a verified canonical skill addition. It remains `stability: experimental` and `version: v1`; no stronger maturity claim is implied.
- No numbered P2.3 requirement is currently defined. The next Phase 2 slice must come from a fresh architecture audit.

## Governance and documentation state

- `AI_CONSTITUTION.md` is the authoritative governance model.
- `AGENTS.md` is the AI-agent entrypoint.
- `meta/PRODUCT_MISSION.md` is the authoritative product mission.
- `meta/COO_MASTER_MISSION.md` is the authoritative COO execution mission under the product mission.
- `meta/memory/DECISIONS.md` is the durable decision record.
- `meta/ROADMAP.md` is the execution direction and must remain synchronized with verified state.
- `meta/DEVELOPMENT_KNOWLEDGE.md` records verified development progression.
- `meta/AGENT_HANDOFF_PROTOCOL.md` defines repository handoff requirements.
- Documentation is a completion gate: implementation without synchronized documentation is not COMPLETE.

## Automation state

- Release authority: `zero-touch-release.yml` is the production release pipeline; `release.yml` is retained as manual recovery.
- Pages authority: `deploy-pages.yml` is the single repository-controlled Pages deployment workflow.
- Confirmed direct-main generated writers use the shared `auto-commit-main` serialization group with `cancel-in-progress: false`.
- The live 42-workflow classification is now recorded in `meta/WORKFLOW_INVENTORY.md`.
- `validate-graph.yml` permission isolation is implemented and verified: `build-and-validate` is `contents: read`; `generate-main-graph` alone has `contents: write` and runs only on trusted `main` pushes after validation; `quality-report` waits for graph generation before writing its projection.
- PR #232 CI passed Security Scan, PR Checks, Test Suite, Build & Verify Wheel, and Auto Label; Dependabot Review Gate was skipped.
- GitHub branch inspection currently reports `main` as unprotected with required-status-check enforcement off. This is documented as a control-plane finding; no branch-protection change was made in this cycle.

## Source of truth

- Canonical source: GitHub repository `SamoTech/skills-tree`.
- Public source guide: `README.md`.
- Operational state: `meta/CURRENT-STATE.md` plus live GitHub CI/PR state.
- Strategic decisions: `meta/memory/DECISIONS.md`.
- Quality evidence: generated repository reports.
- External dashboards and Vercel deployments are not authoritative.

## Product mission alignment — VERIFIED — 2026-10-02

The governing product mission is now:

> **Skills Tree is a public, trusted, machine-discoverable source of AI skills. AI agents should be able to find the right skill here, and humans should be able to discover, understand, use, share, and contribute skills easily.**

`meta/PRODUCT_MISSION.md` is the canonical mission document. Active governance, roadmap, discovery, distribution, and public-source documentation are being synchronized to it. Historical strategy and decision records retain their original wording where they document prior decisions; they are not treated as the current product mission unless explicitly superseded.

PR #250 discovery alignment is merged and its mission/discovery documentation is now part of the verified product baseline.

## Next mandatory action

Perform a fresh universal-registry runtime architecture audit after the verified deterministic Agent Skills corpus. The next engineering slice must be evidence-backed and must not reopen completed runtime or distribution work. Identify the highest-value remaining missing invariant or consumer-behavior gap, confirm it is not already covered by the contract, registry, graph, evidence, compatibility, skill, or runtime layers, then implement the smallest evidence-backed schema → runtime → behavioral-test slice.

Do not invent a numbered P2.3 requirement, reopen completed P1 work, or expand scope merely to create activity.

## Kanban Skill Addition — VERIFIED — 2026-10-03

PR #267 was squash-merged after the final exact-head CI matrix passed. The merged skill is canonical under `skills/15-orchestration/` and did not create a competing generated catalog. The only review defect found was a third-party CLI example mismatch; it was corrected before merge and the review thread was resolved.

## Handoff

A future agent must re-read the authoritative documents and verify live GitHub state before continuing. The repository, not this snapshot alone, remains the final source of truth.


## Universal Registry Data Schema Validation — Verified 2026-10-02

PR #241 added runtime structural validation of the loaded universal registry against the dedicated `meta/universal-registry-data.schema.json` data-instance schema. The existing `meta/universal-registry.schema.json` remains the ontology/contract-definition schema and is not incorrectly used as a seed-data schema.

The runtime resolves the implementation and adapter contract schemas through an explicit local `referencing.Registry`, preserving offline/deterministic validation without fetching repository URLs at runtime. Structural validation runs immediately after JSON load; the existing semantic integrity and entity-specific contract validators remain responsible for semantic/provenance invariants.

A regression test rejects a schema-invalid Goal field with the expected `jsonschema.ValidationError`, while the existing provenance test continues to exercise the established semantic `ValueError` boundary.

**Verification:** PR #241 merged as `93c50c3616a7c558b483f341f44a91509ed032ca`. Exact-head Security Scan, PR Checks, Test Suite, and Build & Verify Wheel passed; Dependabot Review Gate was skipped.

**Status:** VERIFIED — runtime structural validation is now aligned with the actual registry data shape and existing semantic validation responsibilities.


## Security Skill Migration Batch 01 — Verified 2026-10-02

A corpus audit found 45 remaining stubs in the generated quality model. The highest-priority remaining cluster was the nine security-category stubs. PR #243 migrated Audit Logging, Harm Detection, Human In Loop, Permission Checking, Privacy Preservation, Rate Limiting, Rollback / Undo, Sandboxed Execution, and Secret Scanning.

Each migrated skill now has a concrete description, explicit I/O contract, runnable example, failure modes, security boundaries, related-skill metadata, and authoritative references. Unsupported benchmark and compliance claims were deliberately excluded.

**Verification:** PR #243 merged as `40fb35aa6c54438f08062c89c118815262b6fe98`. Validate Skills, Security Scan, PR Checks, Test Suite, Build & Verify Wheel, Schema Enforcement, Validate Skills Graph, AST Sweep, Check Links, and Skill Upgrade Detector passed on the final head. The intermediate quality-report run was superseded during the required frontmatter correction; the generated report had already passed for the same nine skill bodies before that metadata-only correction.

**Generated-artifact verification:** the hardened quality-report workflow regenerated `meta/QUALITY-REPORT.md` after the merged documentation PR. The live generated report now verifies 374 skills: 202 battle-tested, 159 enriched, 13 stubs, 0 invalid. Category 14-security is 13 battle-tested, 0 stubs.

**Status:** VERIFIED — implementation, generated corpus report, and public documentation are synchronized.


## Goal Capability Runtime Access — VERIFIED — 2026-10-02

A fresh runtime/consumer audit identified a missing typed Goal→Capability accessor. The implementation adds `GoalRuntime.capabilities_for_goal()` and `UniversalRegistry.capabilities_for_goal()`; `skills_for_goal()` reuses that boundary.

Focused regression coverage verifies deterministic Goal-to-Capability traversal and defensive snapshot behavior.

**Verification:** PR #238 exact head `0d45fd7b7a741c8984fbe5a90b1abe7e8570b744` passed Security Scan, PR Checks, Test Suite, Build & Verify Wheel, and Auto Label before merge as `3290ebc88060fca07e944cd31ad31d392982ca3d`.

**Status:** VERIFIED — the typed Goal→Capability runtime path is live on `main`.
\n\n## Deterministic Agent Skills Projection — VERIFIED — 2026-10-02

PR #251 established and verified the first executable canonical-to-Agent-Skills projection contract, then merged to `main` as `f1d169c3fd9388cf4244d9d4bfc4c64df382a1bb`.

The canonical source remains `skills/`. `tools/generate_agent_skills.py` deterministically derives package names, descriptions, provenance metadata, and package content, while refusing blocked entries. Generation has an explicit write mode; CI performs a read-only audit. The Agent Skills validator also enforces the current name constraint, including the prohibition on consecutive hyphens.

The verified corpus audit found 374 canonical skill entries after excluding category `README.md` files: 250 currently pass the projection gates and 124 are blocked. Eight deterministic-name collisions remain across canonical entries and must be resolved before full-corpus generation. The existing repository contains 280 validated Agent Skills packages; these are not assumed to be canonical projections until provenance reconciliation is completed.

Exact-head CI passed: Agent Skills Distribution Audit, Validate Agent Skills, Test Suite on Python 3.11/3.12/3.13, Security Scan, Build & Verify Wheel, PR Checks, Auto Label, and Validate Skills Graph. Dependabot Review Gate was skipped.

**Current boundary:** this is a verified projection/audit contract, not full-corpus Agent Skills compliance. The repository does not declare `/.well-known/agent-skills/index.json` live. SHA-256 publication and discovery-index generation remain gated on successful artifact reconciliation, provenance validation, reproducible publication, and served-byte integrity checks.

**Next:** reconcile the 280 existing packages against canonical provenance, resolve the eight canonical name collisions, then generate only eligible canonical projections in independently verifiable batches.


## Deterministic Agent Skills Corpus — VERIFIED — 2026-10-02

PR #264 merged the deterministic canonical-to-Agent-Skills corpus as commit `892a4d747e588cf2876e45ba3effcdd031fd9592`.

Verified generation run:
- 374 canonical skill entries scanned.
- 250 eligible canonical projections generated.
- 124 canonical entries remained blocked and were not generated.
- 288 Agent Skills packages exist on `main`: 250 eligible projections, 37 retained blocked existing packages, and the intentional auxiliary `skills-tree-registry` package.
- 10 canonical name-collision groups were reconciled with deterministic category-qualified projection names where eligible.
- Agent Skills validation passed after generation.
- Reconciliation passed with `git diff --check`.
- Final PR checks passed: Agent Skills validation/distribution audit, Test Suite on Python 3.11/3.12/3.13, Security Scan, Build & Verify Wheel, PR Checks, and repository graph validation.

The corpus is now a verified deterministic projection of the canonical source. `/.well-known/agent-skills/index.json` remains intentionally unpublished until served-byte integrity, provenance, reproducibility, and SHA-256 publication gates are implemented and verified.


## Universal Registry Behavioral-Evaluation Audit — 2026-10-03

A fresh universal-registry architecture and consumer-behavior audit completed the mandatory post-schema-validation review. Provenance, Evidence, integrity, memory safety, and action governance are already represented at their appropriate repository boundaries. The audit identified one concrete remaining machine-readable consumer gap: the first-class benchmarks registry collection had no dedicated contract or typed runtime facade.

The selected slice is implemented on runtime/benchmark-integrity-slice: meta/benchmark-contract.schema.json, BenchmarkRuntime, UniversalRegistry benchmark accessors, and focused behavioral tests. No production benchmark records or external claims were added.

**Status:** PENDING exact-head CI verification and merge.

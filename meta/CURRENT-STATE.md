# Skills Tree — Live Repository State

> Maintained as a point-in-time operational snapshot. This file records verified state used for engineering and governance decisions.

## Verified snapshot

- Snapshot date: 2026-10-04
- Live `main`: authoritative and must be verified from the Git ref before execution; this document intentionally does not hard-code `main`'s own current commit because updating this document creates a new `main` commit.
- Latest verified runtime sequence on `main` includes the benchmark runtime (`db474059fbe0efa56ca167a7108146323c9cf857`), anti-slop gate (`90f9422954936e054adc630ad723e6165074492c`), Universal Graph fail-closed boundary (`c8e1c536f8abfd860ddf41cefeff15b88518d095`), recommendation registry context (PR #292), and blueprint registry context (PR #293). Live `main` remains authoritative and must be resolved before each execution cycle.
- PR #223 remains the implementation baseline for the post-P2.2 Evidence runtime slice, merged as `642e968879e9b6bfc8e7f9b2a44d12544585fc18`.
- PR #224 merged on 2026-10-01 and synchronized the affected P2 architecture, development knowledge, audit, decision memory, and current-state documentation.
- Quality report: current generated report `meta/QUALITY-REPORT.md` verifies 375 skill files: 216 battle-tested, 158 enriched, 0 stubs, 0 invalid, 1 intentional test fixture.
- Quality-report figures are current only at the generated-report verification point; historical verification sections retain their original counts.
- `main` current HEAD is intentionally verified from the live Git ref during each execution cycle; this snapshot does not hard-code its own future commit.
- Latest documentation synchronization was verified on 2026-10-03 after quality-report regeneration at `af176a061abfa84401176043cd04ad2704736f47`.

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
- The Benchmark runtime slice is verified: `UniversalRegistry` exposes deterministic `resolve_benchmark()` and `benchmarks_for_entity()` under `meta/benchmark-contract.schema.json`; this defines evaluation contracts, not benchmark results.
- The Universal Graph runtime fail-closed boundary is verified on merged `main`: only semantically implemented relationship types are accepted; schema-valid deferred relationships are rejected.
- Recommendation and blueprint consumers expose additive `registry_context` derived from `UniversalRegistry`, preserving provenance/evidence/freshness/implementation context without changing ranking semantics.
- The generated search projection now has an explicit `meta/search-index.schema.json` contract and regression coverage for schema validity, duplicate IDs, canonical file resolution, and path parity with `docs/api/skills.json`. A real stale-projection defect for `kanban-task-management.md` was detected by that gate and reconciled before merge.
- Issue #86 CLI search is verified on `main`: `cli/search_engine.py` consumes the canonical generated projection via `cli/search_runtime.py`, with deterministic lexical ranking and CLI behavioral coverage. PR #299 merged as `7302d0780b2857bdd2f54363a2e6158eafc45292`.
- The installable search runtime boundary is verified: `docs/search-index.json` and `data/search-index.json` are identical generated projections, and `cli/search_runtime.py` resolves either the source checkout asset or installed wheel data.
- Issue #86 search behavior is implemented as a deterministic lexical consumer in `cli/search_engine.py`, with CLI coverage in `tests/test_search_cli.py` and ranking-unit coverage in `tests/test_search_engine.py`.
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
- The live workflow inventory is 40 files, as verified in `meta/WORKFLOW_INVENTORY.md`.
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

## Documentation synchronization status

**VERIFIED — synchronized in this documentation cycle.** The preflight found stale operational statements about merged graph/consumer work; those discrepancies are reconciled here without rewriting historical entries.

## Next mandatory action

The post-publication machine-readable consumer/projection audit was completed against live main at `168f88d64d8d397fa9d189ebeaa731a5a461d826`. Existing registry, graph, search, JSON-LD, Agent Skills, recommendation, blueprint, Pages, release, and security boundaries were rechecked and no new evidence-backed invariant gap was found.

Issue #276 was closed after recording that conclusion. Do not invent a numbered P2.3 requirement, reopen completed work, or expand scope merely to create activity. The next engineering slice requires a new concrete defect, contract gap, or governance requirement.

Issue #159 remains the only open high-impact governance blocker: GitHub `main` is currently unprotected with required status checks off, and repository rulesets are empty. The connected integration cannot modify branch protection.

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

The selected slice was implemented with `meta/benchmark-contract.schema.json`, `BenchmarkRuntime`, `UniversalRegistry` benchmark accessors, and focused behavioral tests. No production benchmark records or external claims were added.

PR #272 merged after the review-fix PR #274 was incorporated. The final exact head was `4738303caeb6a9129af8a0f84cab4219aade5084`; the final PR CI matrix passed Test Suite, Security Scan, PR Checks, Build & Verify Wheel, and Auto Label. The merged main commit is `db474059fbe0efa56ca167a7108146323c9cf857`.

**Status:** VERIFIED — implementation, contract validation, behavioral tests, provenance boundary, and exact-head CI were verified before merge.

## Anti-Slop Quality Gate — 2026-10-03

PR #273 established the deterministic anti-slop quality gate for changed skills. PR #275 supplied the targeted review fixes for rename detection and case-sensitive placeholder handling; #275 was incorporated into #273.

The final #273 head was `4477d33d846c68d71b666e6c283c8787312e023f`; its required CI matrix passed, including Security Scan, Test Suite, Build & Verify Wheel, PR Checks, Validate Skills Graph, Skill Quality Report, and Auto Label. The merged main commit is `90f9422954936e054adc630ad723e6165074492c`.

The gate is deterministic and changed-skill scoped. It blocks selected placeholder/marketing filler patterns, warns on unsupported absolute/generic claims, ignores fenced code/frontmatter, and does not attempt LLM-based style classification.

**Status:** VERIFIED — the quality gate and review fixes are merged. Historical corpus cleanup remains a separate evidence-driven migration and is not implied by this gate.


## Universal Graph Relationship Runtime Boundary — VERIFIED ON MAIN — 2026-10-03

PR #283 was merged to `main` as `c8e1c536f8abfd860ddf41cefeff15b88518d095` after exact-head verification. The runtime preserves the forward-compatible schema vocabulary but rejects schema-valid relationship types lacking explicit runtime semantics. No new graph relationship or evidence was invented.


## Registry Consumer Context — Verified 2026-10-03

The recommendation API now exposes additive registry_context for registered canonical skills. The context is derived from UniversalRegistry and includes canonical identity, provenance, explicitly linked evidence references, declared freshness when present, and registered implementation IDs. It does not create ranking or trust scores and does not infer evidence. Unregistered legacy recommendation entries may have null registry_context.

Verification: PR #292 merged the recommendation consumer context; focused API regression coverage is present. Next: audit remaining machine-readable discovery projections for equivalent registry context and provenance propagation.


## Blueprint Consumer Context — VERIFIED ON MAIN — 2026-10-03

PR #293 merged additive `registry_context` propagation onto required and optional blueprint skill entries. The field is descriptive and does not change blueprint generation, architecture selection, or ranking.


## PyPI Release Contract Synchronization — VERIFIED — 2026-10-03

`meta/PYPI_RELEASE_PLAN.md` was reconciled with the executable release path. The repository version is currently `1.68.0` in `pyproject.toml`. Production publication is performed by `.github/workflows/zero-touch-release.yml` using GitHub OIDC Trusted Publishing and the `pypi` environment. The historical `publish.yml` / `PYPI_API_TOKEN` / `1.0.0` instructions are no longer treated as current release instructions.


## Machine-Readable Discovery Registry Context — VERIFIED ON MAIN — 2026-10-03

The discovery audit found that docs/api/skills.json was not consuming the verified UniversalRegistry context. PR #300 merged as `4ff041511f2291e826b2a32c2cc72f36f8f023cb` and adds optional registry_context for the three exact registered skills only, with no synthetic membership or evidence. Final head `52ae305ad504416114d7efdd8313eff8f931f57d` passed the required CI matrix, including Test Suite on Python 3.11/3.12/3.13 and installed-wheel verification.

During validation, the new focused test exposed an existing schema/artifact date-format mismatch in unrelated `added`/`last_updated` fields. The test was narrowed to the registry_context sub-schema; the date-format drift remains a separate audit finding and was not changed in PR #300.


## Generated Discovery Projection Audit — VERIFIED — 2026-10-03

PR #301 corrected canonical Kanban date metadata and PR #302 reconciled `docs/api/skills.json` and `docs/api/skills.yaml`; the affected projection now reports `added: 2026-10` and `last_updated: 2026-10`.

The remaining machine-readable projection audit found:
- `agent-skills/` already has a read-only reconciliation/audit gate on canonical `skills/**` changes; no duplicate drift checker is warranted.
- `docs/api/jsonld/` is an SEO/presentation projection generated from the same skill index. It does not implement ranking, trust, evidence, or registry semantics, so `registry_context` was intentionally not duplicated into JSON-LD.
- `/.well-known/agent-skills/index.json` remains unpublished. Its existing gate correctly requires deterministic generation, provenance validation, reproducible publication, served-byte verification, and SHA-256 integrity before activation.

**Next:** audit remaining machine-readable consumers/projections after the verified discovery publication boundary; do not create a second generator, reconciler, search index, or deployment path.

## Agent Skills Reconciliation Gate — VERIFIED ON MAIN — 2026-10-04

A fresh Agent Skills distribution audit identified a governance gap: tools/reconcile_agent_skills.py classified eligible missing projections but exited successfully unless its result was manually interpreted. The merged implementation closes that gap with a read-only --check mode wired into the Agent Skills Distribution workflow.

Verified merged-main state:

- 375 canonical skill entries are scanned.
- 258 currently satisfy the deterministic Agent Skills projection gates.
- 117 are blocked by the existing eligibility rules.
- The Agent Skills projection contains 296 packages: 258 deterministic eligible projections, 37 retained blocked packages, 1 intentional auxiliary `skills-tree-registry` package, and 1 legacy compatibility package (`rag`).
- The newly added Kanban skill is eligible and has a deterministic projection at agent-skills/kanban-task-management/SKILL.md.
- Reconciliation classifies eligible missing, projection drift, rename-needed compatibility mappings, stale/ambiguous provenance, unexpected packages, and unresolved deterministic target-name collisions. `rename_needed` alone is not a failure.
- Known canonical collisions remain valid when the existing deterministic category-qualified resolution produces unique target names.
- No .well-known/agent-skills/index.json publication was introduced.

This state is VERIFIED ON MAIN after PR #305 merge; the next action is a fresh audit of remaining machine-readable discovery consumers.


## 2026-10-04 — Agent Skills discovery publication boundary — VERIFIED ON MAIN

The deterministic Agent Skills discovery publication slice is now merged and verified end-to-end.

Verified main:
- Main HEAD: `e306a810c7cabac25b9f19fa4aeeab2e62ed0e3f`.
- 375 canonical skill entries remain the source corpus.
- 258 eligible deterministic Agent Skills projections are published.
- 117 canonical entries remain blocked.
- 296 Agent Skills packages remain reconciled under the existing hard gate.
- The discovery index is generated from the same reconciled projection and validated against `meta/agent-skills-discovery-index.schema.json`.
- Every published `SKILL.md` digest is SHA-256 over the exact published bytes.
- Local Pages artifact byte verification passed.
- GitHub Pages deployment run `37199284169` passed both build and deployment jobs.
- Served discovery index and every advertised Agent Skills artifact passed served-byte SHA-256 verification.

Current project-site discovery URL:
`https://samotech.github.io/skills-tree/.well-known/agent-skills/index.json`

The repository does not claim the root-level `/.well-known/agent-skills/index.json` endpoint because the current hosting topology is a GitHub Pages project site. A root endpoint remains a separate hosting/custom-domain control-plane decision.

No second generator, reconciler, search index, or Pages deployment workflow was introduced.

**Status:** VERIFIED — deterministic discovery generation, provenance/reconciliation, schema validation, artifact integrity, Pages deployment, and served-byte verification are all aligned.

## 2026-10-04 — Graph projection boundary — VERIFIED ON MAIN

PR #315 unified the graph generation and projection governance boundary.

Verified:
- `tools/build_graph.py` remains the sole graph generator.
- `validate-graph.yml` is the single graph generation/validation writer; the duplicate `build-graph.yml` workflow was removed.
- The generated graph is validated against `schema/graph.schema.json` plus the referenced skill and edge schemas, including metadata counts and graph integrity checks.
- `docs/api/graph.json` is generated from the same graph output as `data/SKILLS_GRAPH.json` and is byte-identical on main (blob SHA `36aa24b193dc89cb1e0a789ef4ff78db2e14e286`).
- Main graph baseline after regeneration: 375 nodes, 240 edges, 9 REQUIRES edges, 0 warnings.
- Schema drift found during implementation was corrected for generated `requires_count`, prerequisite arrays, generated `source_method`, and numeric-leading skill slugs.

**Status:** VERIFIED — graph generation, schema validation, integrity checks, and synchronized runtime/UI projections are aligned.

## 2026-10-04 — JSON-LD export governance — VERIFIED

The machine-readable export audit confirmed that JSON-LD is generated by the existing `tools/export_skills.py` implementation and committed by `export-skills.yml`; no `jsonld-export.yml` workflow exists on current main.

A real governance gap was found: the export workflow only triggered on skill content changes, so exporter or UniversalRegistry changes could leave generated JSON/YAML/JSON-LD projections stale. It also had no deterministic JSON-LD projection validation.

PR branch `fix/jsonld-export-governance` adds `tools/verify_jsonld_export.py` and focused regression tests. The validator checks JSON validity, one TechArticle per registry skill, matching IDs/names, ItemList positions/counts, and duplicate URLs. `export-skills.yml` now runs the validator and triggers on exporter and registry changes.

PR #316 merged as `20ed032bdb83f22ef3bf37debb3004ed8153d9a8` after the required PR CI matrix passed. The validator and workflow trigger changes are now on main. Do not create a second JSON-LD generator or workflow.

## 2026-10-04 — Release authority consolidation — VERIFIED

Fresh release-path audit confirmed that `zero-touch-release.yml` is the production release authority and `release.yml` is manual recovery only. The former `release-package.yml` independently triggered on version tags and could create/update the same GitHub Release while the zero-touch pipeline was still completing.

PR consolidation moves catalog ZIP + MANIFEST generation into Job 4 of `zero-touch-release.yml`, alongside the existing wheel/sdist attachment, and removes `release-package.yml`. The production release path therefore has one release writer and one manual recovery workflow.

No semantic-release workflow file exists on current main; semantic-release is executed as Job 1 inside `zero-touch-release.yml`.

**Status:** VERIFIED implementation boundary; final PR CI and post-merge release-path checks are required before treating the change as complete.


## 2026-10-04 — Release authority consolidation — VERIFIED ON MAIN

PR #317 merged as `262dfea66fb81e5779e93b45884d857f3b10522d`.

The production release boundary is consolidated: `zero-touch-release.yml` is the sole production release writer; `release.yml` remains manual recovery only; catalog ZIP + MANIFEST packaging is now part of zero-touch Job 4; the duplicate tag-triggered `release-package.yml` workflow was removed.

The workflow inventory and release governance documentation are synchronized with the executable architecture.

**Rule:** do not reintroduce a second tag-triggered GitHub Release publisher.


## Full Repository Re-Audit — 2026-10-04

The current full-project audit is recorded in `meta/audits/FULL_REPOSITORY_AUDIT_2026-10-04.md`.

Verified current baseline:
- 375 canonical skills; quality report: 216 battle-tested, 158 enriched, 0 stubs, 0 invalid, 1 fixture.
- 258 eligible Agent Skills projections; 117 blocked; 296 packages.
- Graph: 375 nodes, 240 edges, 9 REQUIRES edges, 0 warnings; generated graph projections are byte-identical.
- 40 workflow files are present and classified in `meta/WORKFLOW_INVENTORY.md`.
- JSON-LD, search, Agent Skills reconciliation/discovery, graph, Pages, and release boundaries each have one authoritative writer/generation path.
- Release consolidation is merged as PR #317 at `262dfea66fb81e5779e93b45884d857f3b10522d`.
- The current audit found the security gate was under-scoped: Gitleaks was blocking, but Python SAST and dependency auditing were not part of the blocking security workflow. This is being hardened in the current audit PR.
- GitHub branch-protection state remains a control-plane finding; the connected integration returned HTTP 403 for the branch-protection endpoint, so no new control-plane claim is made.

The stale 42-workflow statement is historical only. Historical audit documents retain prior findings and are not current architecture authority.


**Post-audit verification:** PR #318 merged as `2ef8a3fe9c987032d614a0e2a026cc4152867204` after exact-head Security Scan `37201410948` passed Gitleaks, Bandit high-severity/high-confidence enforcement, and `pip-audit --strict`; Test Suite, Build & Verify Wheel, Validate Skills Graph, and PR Checks also passed.

The blocking repository security gate is now materially enforced. The remaining branch-protection finding is control-plane-only and remains tracked separately by issue #159.

## 2026-10-04 — Repository self-enforced governance

The repository governance model was audited after the owner explicitly rejected GitHub branch protection as a required control. Repository-local enforcement is now defined in `meta/GOVERNANCE_MODEL.md` and mechanically checked by `tools/verify_governance.py`, invoked by `.github/workflows/governance-gate.yml`.

The governance gate verifies the mandatory agent/documentation preflight, canonical `skills/` source boundary, unique release authority, unique machine-readable projection paths, anti-slop and new-stub enforcement, blocking security controls, and the repository's explicit independence from GitHub branch protection.

Issue #159 is therefore a control-plane decision outside the repository completion model, not an engineering blocker. Its historical references to branch protection remain historical and must not be interpreted as a current project requirement.

**Status:** VERIFIED — repository governance is self-enforced without requiring GitHub branch protection.


## Core Agentic Execution Loop — IMPLEMENTED — 2026-10-04 — HISTORICAL IMPLEMENTATION RECORD

The repository now defines a bounded autonomous execution contract for AI agents. The canonical cycle is `OBSERVE → ASSESS → PLAN → EXECUTE → VERIFY → RECORD → DECIDE`. Verification failures become evidence for the next cycle instead of requiring a new user prompt. The loop has explicit `CONTINUE`, `BLOCKED`, and `DONE` outcomes, a default 12-iteration ceiling, repeated-failure safeguards, authority escalation boundaries, and a completion contract requiring invariant verification, tests/CI, generated-artifact synchronization, and documentation synchronization.

The contract is defined in `meta/AGENT_OPERATING_MODEL.md`, reinforced by `AGENTS.md` and `AI_CONSTITUTION.md`, and checked by `tools/verify_governance.py`. This is an operating contract, not a claim that GitHub or an external hosted agent automatically executes arbitrary future work without an invoking agent runtime.

Status: VERIFIED — superseded by the exact-head verification recorded immediately below.


## Core Agentic Execution Loop — VERIFIED — 2026-10-04

PR #324 was merged after the exact final head `8f254754231bd8153efd50ab0e4b1bff4d067cad` passed Governance Gate, Validate Skills Graph, Test Suite on the applicable matrix, Security Scan, PR Checks, Build & Verify Wheel, and related validation. The repository now defines the bounded operational cycle `OBSERVE → ASSESS → PLAN → EXECUTE → VERIFY → RECORD → DECIDE`, with failure-driven continuation, a default 12-iteration ceiling, explicit CONTINUE/BLOCKED/DONE states, authority escalation boundaries, and documentation/generated-artifact completion requirements.

**Status:** VERIFIED on main at merge commit `6fa92dd42768395102215a26e22999d6de81c013`.

## Main-Writer Race — DETECTED AND RESOLVED — 2026-10-04

Post-merge verification exposed a real automation race: the graph writer advanced main while the quality projection and zero-touch release workflows were still operating from the triggering SHA. The graph projection itself completed, but the quality writer failed on stale upstream state and zero-touch release failed when its upstream SHA changed. This is a concurrency/state-reconciliation defect, not a graph-generation defect.

The remediation was implemented through PR #325 (stale-SHA synchronization) and PR #326 (lossless `queue: max` writer queue). Exact-head CI passed for both PRs. Post-merge evidence showed graph projection, quality projection, and zero-touch release completing sequentially; zero-touch release completed successfully at version 1.74.0, and the generated graph/quality writer sequence advanced main without the earlier stale-SHA failure.

**Status:** VERIFIED on live main. The repository-wide writer contract is now: shared `auto-commit-main`, `queue: max`, `cancel-in-progress: false`, plus live-main synchronization before mutation.


## Documentation Synchronization — VERIFIED — 2026-10-04

The agentic execution contract, governance model, main-writer serialization, and lossless writer queue are synchronized with the verified live implementation. Historical entries remain explicitly historical; current operational state is represented by the resolved sections above and the durable decisions in `meta/memory/DECISIONS.md`.

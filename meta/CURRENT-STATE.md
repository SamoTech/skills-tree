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
- `/.well-known/agent-skills/index.json` is published and verified live; deployment run `37227197992` passed the served-byte verification gate.

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
- 376 canonical skills; the new IDE Integration skill is the first demand-driven Phase 3 slice.
- 259 eligible Agent Skills projections; 117 blocked; 297 packages expected after deterministic projection maintenance.
- Graph baseline will advance from 375 to 376 nodes after generated projection maintenance; CI must verify the resulting edge and artifact counts.
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


## Consumer-Path Audit — 2026-10-04

The fresh consumer-path audit found that the previously tracked CLI search gap is already resolved on main. `skills-tree search` uses the canonical generated `data/search-index.json` projection through `cli/search_runtime.py`; deterministic ranking is defined in `meta/SEARCH_CLI_CONTRACT.md`; dedicated CLI, ranking, and projection-contract tests exist. No second search index or runtime Markdown parser is required.

The Agent Skills discovery publication boundary is also implemented in `.github/workflows/deploy-pages.yml`: Pages builds `/.well-known/agent-skills/index.json` from `tools/build_agent_skills_discovery.py`, validates the local publication bytes, and verifies the served URL with `tools/verify_agent_skills_discovery.py`. Repository code evidence therefore shows the publication path is implemented. External live serving is the remaining verification step; do not claim it is live until a successful Pages deployment provides that evidence.

**Decision:** Do not build another search/discovery generator. Complete live Pages verification first; then reassess demand intelligence from evidence.


## Demand Intelligence — IMPLEMENTED COLLECTION PATH — 2026-10-04

Phase 2 now has its first reproducible public-signal path: `tools/collect_demand_signals.py` reads the explicit `meta/demand-sources.json` query set and records public GitHub issue-search evidence with source ID, query, repository, issue number, URL, state, dates, and labels. `.github/workflows/demand-signals.yml` runs the collector manually or weekly and stores the raw snapshot as an artifact.

The collector deliberately does not infer popularity, adoption, or priority. The curated `meta/MOST-WANTED-SKILLS.md` remains unranked until a controlled collection run is reviewed and capability coverage/evidence gaps are mapped.


## Demand Signal Review — VERIFIED OBSERVATION — 2026-10-04

The first controlled public-signal review executed against the configured GitHub issue-search sources. The three configured queries returned raw result counts of 64, 63, and 54; overlap and operational/security issues make these counts unsuitable as popularity or adoption metrics.

The review identified an unranked capability signal cohort around search/discovery (#86), memory (#87), code/IDE integration (#88), reasoning (#90), and action execution (#91). Search/discovery is already implemented and verified; the remaining signals require canonical coverage, evidence-tier, freshness, and dependency-gap analysis before any migration priority is selected.

**Decision:** Do not create a popularity ranking. Use the observed cohort as input to a coverage/evidence reconciliation pass, then select Phase 3 work only where demand and repository gaps intersect.


## Phase 3 Candidate — IDE Integration — VERIFIED ON MAIN — 2026-10-04

Coverage/evidence reconciliation selected IDE integration as the first demand-driven Phase 3 slice. The canonical `05-code` directory already covers code generation, review, execution, Git, APIs, debugging, and related capabilities, but no dedicated IDE integration contract existed. The new `skills/05-code/ide-integration.md` defines a protocol-neutral contract around workspace identity, code intelligence, diagnostics, bounded edits, tests/builds, explicit authorization, least privilege, and independent postcondition verification.

The skill cites current public evidence for MCP/IDE integration and explicitly avoids universal compatibility or benchmark claims. CI must determine whether the skill is schema-valid, anti-slop compliant, projection-eligible, and safe to merge.


## Discovery Publication Boundary — VERIFIED

Live GitHub Pages verification completed on 2026-10-04. Deployment run `37227197992` for main commit `1b3a5f387a17ce6b57885b06d6f26db060a8784d` succeeded. The deployment job's `Verify served discovery bytes` step also succeeded, proving the published `/.well-known/agent-skills/index.json` endpoint passed the repository's served-byte verifier. The discovery publication boundary is therefore CLOSED as verified. Next strategic slice: Demand Intelligence / Most-Wanted evidence collection.

## Demand Intelligence — Initial Evidence Pass

The first repository-local demand collection path is present and a controlled public-signal cohort has been recorded. External public-source corroboration on 2026-10-04 shows Agent Skills are an ecosystem-scale concern, with strong activity around discovery, interoperability, retrieval/selection, evaluation, governance, and safety. A coverage reconciliation found that the repository already has broad canonical coverage for the local memory, IDE/code, reasoning, and action-execution demand signals. The next decision gate is therefore evidence/runtime quality rather than raw skill creation. Preferred investigation: skill evaluation/invocation evidence and retrieval quality.


## Agentic Loop — Retrieval/Evaluation Evidence — 2026-10-05

OBSERVE/ASSESS found a concrete evidence boundary defect: the retrieval benchmark is stale and not currently backed by a reproducible current run; its related canonical skill links are outdated; the evaluation ontology is past review due; and evaluation workflow path filters omitted the ontology itself. EXECUTE fixed the workflow trigger so evaluation-ontology changes now invoke validation. Issue #336 records the remaining evidence remediation: reproduce, retire, or re-qualify the stale benchmark without fabricating new scores. Current decision: **CONTINUE** — the next safe evidence-backed action is benchmark provenance/link repair and deterministic freshness validation.

## Agentic Loop — Evaluation Gate Reconciliation — 2026-10-05

**OBSERVE:** Live main has a deterministic lexical CLI search path and a typed Benchmark runtime, but no current reproducible retrieval-quality run. The legacy recommendation evaluator is historical and is not current runtime evidence. The current evaluation ontology contains seven mappings and remains overdue for review; CAP-007, CAP-011, and CAP-014 are still absent from the ontology mapping set.

**ASSESS:** The evaluation workflow was checking the wrong corpus location (`data/corpus/**`) and therefore could not reliably measure P0 evaluation coverage. Its warning-only behavior did not convert missing mappings into a false completion claim, so the safest correction is to point the check at the canonical `intelligence/corpus/entries/**` path and report missing P0 mappings explicitly without inventing evaluations. A declared-freshness check was added to detect malformed/inconsistent timestamps and surface overdue review dates without rewriting them automatically.

**EXECUTE:** The evaluation workflow was corrected on branch `fix/evaluation-evidence-gate-20261005`; the stale retrieval benchmark was qualified as historical, its current canonical skill links were repaired, and the benchmark index documentation no longer claims every result is currently reproducible.

**VERIFICATION:** No benchmark result was regenerated and no current retrieval score was claimed. The repository still requires benchmark provenance/reproduction or explicit retirement/re-qualification for the stale retrieval evidence, and authoritative P0 mappings for CAP-007/CAP-011/CAP-014 remain outstanding. These are tracked evidence gaps, not fabricated failures or success claims.

**DECISION:** CONTINUE / BLOCKED boundary remains evidence-driven. The next safe action after CI verification is to address Issue #336/Issue #335 only with reproducible benchmark evidence or an explicit evidence disposition; no new retrieval implementation is justified yet.

## Post-Merge Verification — Evaluation Gate Self-Trigger — 2026-10-05

**OBSERVED:** PR #337 merged to `main` as `4b1c1b9ffc28bcbecc3b899da8cbb58af7de65ec`. Exact-head PR checks passed, including Test Suite, Security Scan, Build & Verify Wheel, Governance Gate, PR Checks, and CodeQL. Post-merge Governance Gate also passed.

**NEW GAP:** The merged `validate-evaluations.yml` workflow did not include itself in its `push.paths` filter. Therefore the workflow was authoritative but did not self-trigger when the workflow definition itself changed. This is a CI trigger defect, not evidence of evaluation correctness.

**ACTION:** Follow-up branch `fix/evaluation-gate-self-trigger-20261005` adds `.github/workflows/validate-evaluations.yml` to its own push path filter and synchronizes the decision record with the merged state.

**DECISION:** CONTINUE until the follow-up exact-head CI proves the trigger correction. No benchmark or retrieval implementation is introduced.


## P0 Evaluation Contracts — VERIFIED ON MAIN — 2026-10-05

PR #339 merged to main as c88672e1d19e381aad8137796d4283678e3fc9e1. The canonical evaluation ontology now contains mappings for the remaining P0 capabilities CAP-014 tool_execution, CAP-007 semantic_retrieval, and CAP-011 self_evaluation. No new evaluation framework, ontology category, or retrieval implementation was introduced.

During exact-head CI, Validate Evaluations exposed two pre-existing validator defects: the gate expected min_required_score while canonical mappings use minimum_required_score, and two existing mappings had stale names for CAP-023 and CAP-025. Both were corrected. Final exact-head CI passed Validate Evaluations, Governance Gate, Test Suite, Security Scan, Build & Verify Wheel, PR Checks, and Auto Label; Dependabot Review Gate was skipped.

The P0 contracts are now structurally linked and CI-validated. This does not constitute current benchmark success: CAP-007 explicitly remains without a current reproducible result artifact, and CAP-011 calibration diagnostics remain evidence requirements rather than a fabricated new metric type. The next evidence boundary is reproducible evaluation execution/results, not another ontology or search implementation.


## Retrieval Evidence — VERIFIED ON MAIN — 2026-10-05

PR #340 merged to main as `8ae02bd08841a496d19f49cd1092ec5f011c6c6b`. The repository now has a versioned, machine-readable retrieval benchmark registered through the existing `BenchmarkRuntime` contract, a deterministic runner over the canonical `cli.search_engine.search_documents` implementation, and a PR/workflow-dispatch evidence workflow.

Exact-head PR verification passed the Retrieval Evidence Benchmark, Governance Gate, Security Scan, Build & Verify Wheel, Validate Skills Graph, PR Checks, Test Suite on Python 3.11/3.12/3.13, and CodeQL. The retrieval benchmark run `37301951280` produced artifact `retrieval-benchmark-95839c52567c32cad38c0a0038edc01dc0a298f4`.

Current evidence snapshot: 12 benchmark cases, Recall@5 = 1.0000, MRR = 0.9583, deterministic replay = true. Eleven of twelve expected skills ranked first; the RAG case ranked the expected `03-memory/rag` at position 2 behind `09-agentic-patterns/rag`. This is evidence of current deterministic retrieval behavior for the bounded dataset, not a semantic-search, popularity, adoption, or user-satisfaction claim.

Decision: do not change ranking yet. The measured RAG ambiguity is now a concrete candidate for a separate retrieval-quality investigation. Any ranking change requires a broader representative failure corpus and before/after measurement.


## Demand-Gap Skill Selection — VERIFIED MERGED — 2026-10-05

PR #341 merged to main as `af892ebf9aafd90dedb9d6039974d51c2bf02726` after exact-head CI passed.

The demand reconciliation identified a narrow missing capability: canonical skill-level selection and next-step routing. Existing coverage already included deterministic search, specialist-agent routing, role assignment, task decomposition, delegation, dependency traversal, registry eligibility, and orchestration primitives, but no dedicated contract for discriminating competing skills, resolving prerequisites, verifying invocation, and selecting the next skill from observed results.

Added `skills/15-orchestration/capability-based-skill-selection.md` as an experimental canonical skill and its deterministic `agent-skills/capability-based-skill-selection/SKILL.md` projection. The demand collector now includes selection/routing/orchestration/task-breakdown signals, and `meta/MOST-WANTED-SKILLS.md` records the evidence-backed demand gap.

The exact-head matrix passed Test Suite on Python 3.11/3.12/3.13, Security Scan, Build & Verify Wheel, Governance Gate, PR Checks, Validate Skills, Validate Agent Skills, Agent Skills Distribution Audit, Validate Skills Graph, Schema Enforcement, Check Links, AST Sweep, Skill Upgrade Detector, Dependency Auditor, and Retrieval Evidence Benchmark.

During verification, existing generated projection drift was exposed and reconciled: the canonical API/search projections and JSON-LD index were brought back into alignment with the live corpus, and the discovery-count test was updated to track the current verified projection count.

Status: MERGED. Post-merge push workflows are running; their results remain a separate verification boundary until observed.


## Behavioral Skill Selection — VERIFIED BOUNDED RUNTIME — 2026-10-05

PR #343 merged to main as `203d4b12e576cbeb5eaa83249cc97d96905b01fc` after exact-head CI passed Test Suite, Security Scan, Build & Verify Wheel, Governance Gate, PR Checks, Validate Skills Graph, Retrieval Evidence Benchmark, and the new Skill Selection Evidence Benchmark.

The repository now has `registry/skill_selection.py` as a deterministic registry-backed selection boundary. It resolves explicit required capabilities against registered canonical skills, applies existing eligibility, rejects unknown candidates fail-closed, returns explicit selection/rejection evidence, and emits CONTINUE/BLOCKED next actions. The versioned benchmark `benchmark/skill-selection-v1` currently covers the three skills represented in the Universal Registry plus unknown-candidate, insufficient-capability, and failed-invocation terminal cases.

Current benchmark evidence: 6/6 cases passed with deterministic replay. This verifies the bounded capability-selection behavior only.

LIMITATION: prerequisite routing is implemented in the selector against the existing `REQUIRES` graph API, but it is not yet behaviorally evidenced through the canonical registry because the Universal Registry currently contains only three skill records and no prerequisite-bearing registered skill pair. Do not claim full task → dependency → invocation sequencing as verified until registry coverage and a reproducible prerequisite benchmark exist.

Status: VERIFIED BOUNDED SLICE. Next justified action: reconcile canonical registry skill coverage for prerequisite-bearing skills, then extend the behavioral benchmark without creating a second registry or orchestration authority.


## Behavioral Skill Selection — PREREQUISITE ROUTING VERIFIED BOUNDED SLICE — 2026-10-05

PR #345 merged to main as `f15c729adf76794fc914f954f74a4964d7dbdd76` after exact-head `8200b0f359e35293121189cdf2dd263ce96252db` passed the applicable CI matrix, including Test Suite, Security Scan, Build & Verify Wheel, PR Checks, Retrieval Evidence Benchmark, and Skill Selection Evidence Benchmark.

The selection runtime now resolves transitive `REQUIRES` prerequisites deterministically, detects prerequisite cycles, fails closed when a graph prerequisite is not registered, and emits the next prerequisite before target invocation. The registry boundary now represents Agentic RAG, CoT, and ReAct with explicit capabilities; Agentic RAG is separated from general knowledge retrieval through `capability/agentic-knowledge-retrieval`, preventing the registry expansion from changing baseline RAG capability resolution.

Current bounded behavioral evidence covers:
- Agentic RAG selection over baseline RAG for the explicit agentic capability.
- Ordered prerequisite routing: RAG → CoT → ReAct before Agentic RAG invocation.
- Resume behavior after partial prerequisite completion.
- Target invocation only after all declared prerequisites are complete.
- Fail-closed behavior for invalid prerequisite graphs.

This verifies deterministic dependency-aware skill selection for the registered Agentic RAG scenario. It does not establish general autonomous task understanding, arbitrary graph correctness, or full task → capability → skill → invocation → verification → next-skill autonomy.

Post-merge workflow runs for `f15c729adf76794fc914f954f74a4964d7dbdd76` were not yet observable at the verification point. Exact-head PR CI is the authoritative pre-merge evidence.

Status: VERIFIED BOUNDED RUNTIME. Next action: use the verified prerequisite-routing boundary as the baseline for the next evidence-driven skill-selection/recovery slice; do not broaden the registry or add orchestration infrastructure without a concrete measured gap.


## Behavioral Skill Selection — FAILURE RECOVERY VERIFIED BOUNDED SLICE — 2026-10-05

PR #347 merged to main as `adbbb55c58a853e843883b2cbc14997f315226b7` after exact-head `40cff5782307469b9d9e62733d04841c667b9870` passed Test Suite, Security Scan, Build & Verify Wheel, Governance Gate, PR Checks, Validate Skills Graph, and Skill Selection Evidence Benchmark.

The recovery runtime now carries an explicit failed-skill history and excludes all previously failed candidates from subsequent recovery selection. The benchmark and unit tests verify remaining-candidate recovery, terminal escalation when no viable recovery remains, and deterministic replay. This closes the measured repeated-retry defect without adding a second orchestration authority.

LIMITATION: the current Universal Registry does not contain three independently registered, capability-compatible alternatives needed to produce a genuine multi-step A → failure → B → failure → C recovery-chain benchmark. A synthetic chain or registry expansion solely for benchmark convenience would fabricate evidence. Therefore this slice is bounded to history-aware candidate exclusion, single-step recovery, and terminal fail-closed behavior.

Post-merge workflows for `adbbb55c...` were not observable at the verification point. Exact-head PR CI is the authoritative pre-merge evidence.

Status: VERIFIED BOUNDED RECOVERY SLICE. Next justified action: obtain real canonical registry coverage with multiple independently eligible alternatives through existing project evolution, then add a multi-step recovery benchmark only when that evidence exists. No artificial skills or new orchestration framework should be introduced for the benchmark.


## Agent Skill Security Audit — VERIFIED ON MAIN — 2026-10-06

PR #350 merged to main as `436c15c745e1747e3ec1e931dccacea1ca013c7c` after exact-head CI passed Governance Gate, Skill Upgrade Detector, Agent Skills Distribution Audit, Schema Enforcement, Auto Label, Skill Quality Report, Validate Skills, Build & Verify Wheel, Check Links, PR Checks, AST Sweep, Validate Skills Graph, Security Scan, and Test Suite. Dependabot Review Gate was skipped.

Demand/evidence reconciliation identified a narrow security boundary missing from the canonical corpus: pre-installation/pre-execution auditing of a complete agent skill package. Existing security skills already cover sandboxed execution, secret scanning, permission checking, input sanitization, audit logging, and human approval; the new contract composes those controls and does not introduce a second scanner or authorization authority.

Added `skills/14-security/agent-skill-security-audit.md`. The contract covers package inventory, declared-vs-observed behavior, credential access, network egress, permission overreach, obfuscation, sandbox requirements, evidence locations, and fail-closed disposition. It explicitly states that static audit output is evidence rather than a safety guarantee and that audit success does not grant execution authorization.

Post-merge workflow runs for `436c15c745e1747e3ec1e931dccacea1ca013c7c` were not observable at documentation-sync time; exact-head PR CI is the authoritative pre-merge evidence. The skill remains experimental pending any future behavioral/security evaluation evidence.

Status: VERIFIED BOUNDED SECURITY CONTRACT. Next action: reconcile any generated projection/quality workflow results on live main, then return to Demand Intelligence only where a concrete evidence or implementation gap remains.


## Evaluation Ontology Freshness Review — VERIFIED — 2026-10-06

A live consistency audit reviewed `intelligence/ontology/evaluation_ontology.json` against the canonical capability ontology and both current corpus entries (`CORPUS-001`, `CORPUS-002`). The ontology contains 12 evaluation types and 12 capability mappings after the repair. All referenced `ET-*` identifiers resolve, capability mapping IDs are unique, mapping names resolve to canonical capabilities, and all ten P0 capabilities required by the current corpus are explicitly mapped. No new evaluation type, ontology category, registry, or benchmark framework was introduced.

The only verified issue was freshness metadata: `last_reviewed_at` was `2026-07-05` and `review_due_at` was `2026-10-03`. After the integrity audit passed, the review metadata was refreshed to `2026-10-06` with the existing 90-day review cadence, due `2027-01-04`.

Evidence: live ontology audit on main baseline `537c30944bdf2163f0ac3350ff4661a66ba85f8e`; 12/12 evaluation references resolve; 10/10 current corpus P0 mappings present after PR #354; no duplicate or unknown mapping IDs. This review does not claim empirical quality of evaluation metrics or benchmark results.

CI exposed two additional corpus P0 capabilities not covered by the initial live snapshot: CAP-018 `multi_turn_dialogue_management` and CAP-027 `compliance_logging`. The existing ontology boundary was extended with mappings for those capabilities using only existing ET-012, ET-001, ET-005, and ET-007 metrics. No new metric type or evaluation framework was introduced.

Status: VERIFIED ON MAIN — PR #354 merged as `15c455bbef43d5f88c17c0cbdbac1af09c8e2d04`. Exact-head applicable CI passed Governance Gate, Validate Evaluations, Test Suite, Security Scan, Build & Verify Wheel, PR Checks, and Auto Label; Dependabot Review Gate was skipped. The canonical corpus now has evaluation mappings for all 10 P0 capabilities. Next: return to Demand Intelligence and select only a new evidence-backed gap.


## Demand Intelligence — Skill Activation / Invocation Evidence — 2026-10-06

Live reconciliation of the current selection runtime and benchmark against fresh public ecosystem evidence identified a new bounded gap: real user-request skill activation/invocation is not behaviorally measured. The existing `benchmark/skill-selection-v1` verifies explicit capability-to-skill selection, prerequisite routing, and failure recovery, but it does not measure natural-language trigger reliability, false activation, collision behavior, repeated fresh-session variance, or actual invocation evidence.

External evidence includes addyosmani/agent-skills #620 (direct prompts with repeated 0/6 owning-skill activation and a measured description improvement), Hermes #82253 (2/3 activation on an identical message across fresh sessions), Hermes #96704 (activation/effectiveness evaluation gap), and Google skill-reach (routing/collision evaluation).

Issue #357 is the authoritative current investigation record. Decision: measure activation/invocation first using existing project boundaries; do not add a new skill, search engine, or routing authority without measured failure evidence.

Status: INVESTIGATING. Next executable action: design and run a bounded activation/invocation benchmark, then decide whether the result requires skill-description remediation, runtime/evaluation improvement, or no change.


## Skill Activation / Invocation Evidence Benchmark — VERIFIED ON MAIN — 2026-10-06

Issue #357 was advanced from investigation to an executable evidence instrument without introducing a new routing authority. PR #359 merged this measurement boundary to `main` as `51f22be5d3935437e19561e8aa1fdbf2eb19daab`. It adds:

- `benchmarks/activation/skill-activation-v1.json` — four bounded natural-language cases covering expected activation, must-not-activate behavior, collision groups, and repeated runs.
- `tools/run_skill_activation_benchmark.py` — trace-based evaluator for explicit `skill_selection` and `skill_execution` events.
- `tests/test_skill_activation_benchmark.py` — deterministic parser/metric regression coverage using synthetic fixtures only.
- `benchmark/skill-activation-v1` — registered in the existing Benchmark runtime boundary.

The evaluator deliberately does not simulate model routing or infer activation from prompt text. `NO_OBSERVATIONS` is an explicit non-PASS state. Therefore the repository now has an activation/invocation measurement boundary, but **no empirical activation-rate claim is made yet** because real agent-runtime traces have not been supplied.

Metrics: expected activation rate, false activation rate, invocation-evidence rate, and repeated-run activation variance.

Next executable action: obtain real structured traces from a compatible agent runtime, run the benchmark, record the evidence, then decide whether failures justify skill-description, runtime, or evaluation changes.


## Activation Observation Contract — IMPLEMENTED — 2026-10-06

The activation benchmark now has an explicit machine-readable observation contract at `meta/skill-activation-observation.schema.json`. `tools/run_skill_activation_benchmark.py` validates external trace payloads against this schema before calculating activation, false-activation, variance, and invocation-evidence metrics. This closes the interoperability/contract gap between an external agent runtime and the benchmark without introducing a routing runtime or new authority.

Empirical activation reliability remains UNVERIFIED: no real runtime trace corpus has been recorded in the repository. Synthetic fixtures remain evaluator tests only.

Next executable action: capture repeated fresh-session traces from a compatible external agent runtime that emits `skill_selection` and `skill_execution` events conforming to the schema, then run `benchmark/skill-activation-v1` and record the resulting evidence.


## Hermes Activation Observation Adapter — IMPLEMENTED — 2026-10-06

The activation evidence boundary now includes a deterministic interoperability adapter at tools/convert_hermes_activation_observations.py. It consumes explicit Hermes observer-hook JSONL evidence and emits the existing meta/skill-activation-observation.schema.json shape.

The adapter maps only observed events:
- Hermes post_tool_call with tool_name=skill_view → skill_selection.
- Hermes on_skill_lifecycle with action=loaded → skill_execution.
- Both must share an explicit session/task correlation and the run must be mapped explicitly to an ACT-* case. Selection-only evidence is preserved as selection evidence; execution evidence is independently preserved when observed. Mismatched selection/execution is intentionally retained so false activation and invocation gaps remain measurable.

The adapter does not infer activation from prompts, aggregate .usage.json counters, or missing events. It does not add routing authority or change runtime behavior.

Status: IMPLEMENTED — empirical evidence remains UNVERIFIED until real Hermes traces are collected and the resulting 12-run corpus passes schema validation and benchmark execution.

## Hermes Real-Trace Capture Instrumentation — VERIFIED ON MAIN — 2026-10-06

PR #364 merged the real-trace capture boundary as `ebb150dfb0f0ad6ddb3d2426cb81d7d7c31579ac`. It adds `benchmarks/activation/hermes_skill_activation_observer.py` and `benchmarks/activation/HERMES-TRACE-CAPTURE.md`.

The observer records only explicit Hermes `post_tool_call` / `skill_view` and `on_skill_lifecycle(action=loaded)` evidence with session/task correlation. It intentionally excludes prompts, model output, tool results, and aggregate usage counters. This is capture instrumentation, not a benchmark result.

Current blocker: no real Hermes trace corpus has been captured in this repository. The next executable action is operational capture of 12 fresh-session observations (4 cases × 3 repetitions), explicit ACT-case mapping, conversion, schema validation, and benchmark execution. Do not claim empirical reliability before that evidence exists.
## Evaluation Harness Integrity — FAIL-CLOSED GAP — 2026-10-06

Fresh public evidence identified silent zero-run benchmark failure as a reusable evaluation-harness integrity risk. Internal audit confirmed `tools/run_skill_activation_benchmark.py` reported `NO_OBSERVATIONS` while returning exit code 0.

PR #365 applies the minimum remediation: zero observed cases now return exit code 2 while still writing the explicit `NO_OBSERVATIONS` result. Existing observed-trace metrics and partial-corpus reporting are unchanged.

Status: IN PROGRESS — exact-head CI pending. This is not an activation-result claim.
Next executable action: verify PR #365 exact-head CI, merge only after all applicable gates pass, then continue demand/evidence reconciliation.
## Full-Project Live Reconciliation — 2026-10-06

Live main now contains the verified Model/Agent/Tool/Capability/Skill semantic boundary from PR #368, the Hermes activation adapter/capture instrumentation from PRs #363/#364, and the fail-closed zero-observation benchmark behavior from PR #365.

Current generated corpus evidence: `meta/QUALITY-REPORT.md` reports 382 skill files (223 battle-tested, 158 enriched, 0 stubs, 0 invalid, 1 intentional fixture). The Agent Skills Distribution Audit on the current PR #368 head verified 382 canonical entries and 302 existing Agent Skills packages with no eligible missing projections, projection drift, stale entries, unexpected packages, or unresolved collisions. `data/SKILLS_GRAPH.json` and `docs/api/graph.json` are byte-identical at 382 nodes / 250 edges; `data/search-index.json` and `docs/search-index.json` are byte-identical.

Governance: GitHub branch protection is not a project completion gate under the current repository-local governance decision; obsolete Issue #159 is closed as not planned. The remaining material activation investigation is Issue #357, which still lacks a real Hermes trace corpus.

Activation evidence contract: zero observations are a process failure; partial traces are explicitly classified as PARTIAL; empirical completion is COMPLETE only when all 4 benchmark cases meet their declared 3 repetitions (12 observations total). PR #369 implements this contract.

Earlier point-in-time audit sections in this file remain historical and must not be read as current counts or current activation status.
Next executable action after PR #369 verification: close/reconcile Issue #366, then continue the real-runtime activation evidence collection path; separately address the DevLens README writer finding tracked in Issue #370.
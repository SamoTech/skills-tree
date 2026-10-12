# Skills Tree â Executable Product Roadmap

> Strategic roadmap for the Skills Tree product mission.
> Effective: 2026-10-03
> Canonical source: `skills/`
> Product mission: `meta/PRODUCT_MISSION.md`
> Execution mission: `meta/COO_MASTER_MISSION.md`

## Current Execution Block â 2026-10-11

1. **Canonical corpus and distribution â verified.** 394 Markdown skill files including one intentional fixture; 393 public canonical skills across 17 categories. PR #467 (issue #466) adds the first demand-gap skills selected under the measured-gap rule: `skill-quality-evaluation` (09-agentic-patterns, tier A) and `progressive-skill-loading` (03-memory, tier B), both `stability: experimental` v1 with dated public demand signals recorded in `meta/MOST-WANTED-SKILLS.md` and byte-exact deterministic `project()` packages. The latest exact reconciliation [#38133298990](https://github.com/SamoTech/skills-tree/actions/runs/38133298990) passed on `f13420a27b1162faa08c74286779dbc6d71265b6`; no canonical skill content changed since that run. Result: 264 eligible, 118 blocked, 302 existing packages validated, zero missing eligible projections/drift/stale/unexpected/ambiguous/unresolved collisions. The ten former name-only fallback packages are grounded in PR #461: their legacy canonical files now carry the required `## Evidence` sections and their packages are deterministic projections with declared provenance (zero name-only matches; 274 eligible / 108 blocked after the exact-head audit passed on the PR head).
2. **Retrieval and selection â verified within bounded datasets.** Retrieval [#38133299000](https://github.com/SamoTech/skills-tree/actions/runs/38133299000): 12 cases, Recall@5 1.0, MRR 0.9583, deterministic replay. Selection [#38133298996](https://github.com/SamoTech/skills-tree/actions/runs/38133298996): 9 cases, accuracy 1.0, deterministic replay. These are not substitutes for the separate 100-case empirical contracts.
3. **Evaluation contracts â aligned.** PR #444 added CAP-006/CAP-010 mappings, corrected CAP-023 and CAP-025 generic methods, introduced `contract_scope`, and added validator/tests. PR #448 reviewed the corpus entries and refreshed freshness dates to 2026-10-11 / 2027-01-09. Issues #435 and #438 are closed.
4. **Next: empirical evaluation.** Prepare the 100 human-labeled support queries for CAP-007, 100 ground-truth pairs for CAP-011, and 100 mocked tool-execution scenarios for CAP-014. Capture dataset provenance and exact acceptance criteria before execution. Track in [#436](https://github.com/SamoTech/skills-tree/issues/436); do not fabricate labels or claim results from the 12/9-case benchmarks. Protocol/schema preparation is merged (CAP-014 mock fixture and scorer; CAP-011 protocol PR #455; CAP-007 protocol PR #456); the remaining work is the independently labeled datasets and the candidate runs. CAP-007 label-validation and empirical-evaluation harness tooling is added in PR #458 (fail-closed; NOT_RUN without human labels), leaving only the labeled dataset and the run itself. CAP-011 preparation is complete (PR #459): the versioned 100-case ground-truth dataset `cap011-dataset-v1.json` is a controlled experiment with machine-verifiable outcomes — every expected outcome is re-derived by committed deterministic predicates (`cap011-verifier-v1.json`, re-executed by tools/verify_cap011_ground_truth.py) under the protocol's reproducible-test ground-truth allowance — plus the fail-closed calibration runner tools/run_cap011_calibration_benchmark.py; the remaining work for CAP-011 is the candidate run itself, which requires records from the actual system under test and hallucination adjudication independent of the candidate. No empirical contract has been run; none may be claimed.
5. **Activation â infrastructure-blocked.** Run [#38131566320](https://github.com/SamoTech/skills-tree/actions/runs/38131566320) correctly classified the runner as infrastructure-ineligible; the activation benchmark was NOT RUN. Keep acceptance unchanged and resume only on an eligible accelerator runtime ([#357](https://github.com/SamoTech/skills-tree/issues/357)).
6. **Automation follow-up.** Timestamp-only graph refresh PR #449 was closed; PR #452 added normalized semantic comparison and post-merge run #38137153321 verified that publication is skipped when only timestamps/format differ. Issue #450 is closed. Quality-report PR creation now works, but bot-created commits can produce `action_required` CI results; issue #447 tracks an approved least-privilege solution. A second stranded-automation instance (the search-index rebuild after PR #461) was reconciled in PR #465 through the documented user-authored recommit; the bot-check root cause remains owner-action in #447. Post-#467 cycle: the graph rebuild published through bot PR #468 (owner-merged; 383 nodes / 263 edges); the quality-report rebuild's PR-creation step stranded and its trusted output is republished through the documented user-authored recommit; the search-index rebuild did not run for the API-driven squash merge and remains pending a trusted rebuild (owner-side workflow dispatch or the next skills-touching push to `main`). These are further #447-family instances. PR #470 closes the search-index stranding class by mirroring `quality-report.yml`'s proven redundant trigger set onto `generate-search-index.yml` (self-path push trigger, merged-PR `pull_request_target` with a merged-only guard, weekly self-heal schedule); the trusted-generator provenance, `auto-commit-main` serialization, and protected-main PR publication path are unchanged. Outcome (2026-10-12): the stranding class was root-caused (step-level evidence; run logs remain owner-side) to missing `pull-requests: write` and `[skip ci]` automation commits on the affected writers — `quality-report.yml` lost both fixes (`7a9cc9e92d`, `4057d03db7`) when `e6620488ec` landed minutes later, and `generate-search-index.yml`/`export-skills.yml` never carried them — while `validate-graph.yml`, which carries them, creates bot PRs successfully (PR #468). PR #472 restores both across the three writers and hardens `export-skills.yml` with the same redundant trigger set; the Skills API export rebuild and the atomic index+export republication (PR #471) follow in this cycle, and the weekly self-heal schedules bound any residual stranding. Resolution (2026-10-12): the export rebuild fired within seconds of PR #472's merge (`automation/generated-skill-api@00b73a86`, with bot PRs #473 and #474 created by the permission-restored writers) and the index+export republication landed atomically through PR #477; the staged PR #471 and bot PRs #473/#474 are superseded and closed. Follow-up (2026-10-12): the first post-#477 rebuild (bot PR #478) proved the export generator nondeterministic — wall-clock timestamps and hash-ordered keywords force a timestamp-only diff on every rebuild, which under the rebuild-after-every-merged-PR trigger would loop forever; PR #479 derives timestamps from git committer dates and sorts keywords, after which unchanged corpora produce "No generated changes." and publish nothing.
7. Preserve the canonical `skills/` source, deterministic lexical search, single generated index, and current capability-selection engine. No semantic-search replacement, competing registry, or raw-count skill additions without a reproducible measured gap.
8. **Owner-directed corpus expansion (2026-10-12):** the repository owner directed a one-time 100-skill expansion across all 17 categories. This is an explicit owner override of the raw-count rule in item 7, recorded in `meta/memory/DECISIONS.md`; no demand signal is claimed (see the expansion note in `meta/MOST-WANTED-SKILLS.md`). The expansion lands in three CI-gated batches (10-skill pilot first, PR #480); generated projections regenerate through trusted workflows after each merge.

Issue #336 retrieval freshness/reproducibility remains resolved.

## Product outcome

Skills Tree is a public, trusted, machine-discoverable source of AI skills. AI agents should be able to find the right skill here, and humans should be able to discover, understand, use, share, and contribute skills easily.

Roadmap work must strengthen AI discovery, human usability, reliable consumption, trust/evidence, distribution, sharing, contribution, and organic GitHub adoption.

Raw skill count and raw stub count are engineering measurements, not product objectives.

## Priority order

Security > Correctness > Canonical architecture > Discovery > Evidence > Freshness > Interoperability > Quality > Developer experience > Cosmetic improvements.

## Phase 0 â Governance stabilization â VERIFIED â 2026-10-06

1. Maintain the live 45-file workflow inventory and classify every workflow as authoritative, supporting, manual recovery, scheduled maintenance, evidence benchmark, or generated-main writer.
2. Maintain exactly one authoritative Pages deployment.
3. Maintain exactly one authoritative release architecture.
4. Consolidate generated-main writers where technically safe.
5. Require explicit reason, least privilege, deterministic output, serialization, bounded retry/rebase, and failure visibility for every generated-main writer.
6. Remove synthetic repository churn and duplicate automation only after dependency/reference verification.
7. Synchronize governance and current-state documentation with actual GitHub state.
8. Verify security gates and document any GitHub control-plane limitations that the connector cannot inspect.
9. Harden the identified `validate-graph.yml` PR permission boundary without weakening trusted-main graph generation. **VERIFIED 2026-10-02:** validation is read-only; trusted-main graph generation is isolated to a write-scoped job; quality generation depends on graph generation.

Exit evidence: workflow inventory, decision records, current-state update, passing relevant CI, verified permission boundaries, and no undocumented automation ownership.

## Previous Live Audit â 2026-10-06 (historical)

The final repository audit verified the current main control plane and canonical/projection boundaries.

- 45 GitHub Actions workflow files are present and classified in `meta/WORKFLOW_INVENTORY.md`.
- PRs #368, #371, #374, #375, #376, #377, and #379 were merged after exact-head applicable CI passed.
- DevLens is diagnostic-only and cannot write repository state; the stale README health snapshot was removed.
- Activation evidence integrity is fail-closed for unknown dataset case IDs and duplicate run IDs; incomplete corpora are classified PARTIAL rather than COMPLETE.
- The quality corpus contains 382 files including one intentional sandbox fixture; the production/public canonical corpus contains 381 skills across 17 categories.
- Agent Skills reconciliation verifies 264 eligible canonical projections, 118 blocked entries, and 302 existing packages.
- At that historical audit point, graph projections were recorded at 382 nodes / 250 edges; the current 2026-10-11 baseline is 381 nodes / 255 edges as recorded in the Current Execution Block above.
- Remaining material evidence gap is Issue #357 (real runtime activation traces). Issue #336 retrieval evidence freshness/reproducibility is resolved by the version-matched deterministic benchmark and explicit historical qualification.

The **Current Execution Block â 2026-10-11** above governs execution selection. This dated audit and older entries below are historical records.

## Phase 0 Exit Interpretation

The repository-local Phase 0 controls are verified. Ongoing maintenance consists of keeping workflow inventory, generated-writer classification, documentation state, and evidence boundaries synchronized with live main. GitHub branch protection is intentionally outside the project-local completion gate.

## Phase 1 â Registry foundation â VERIFIED â completed foundation

Build a backward-compatible machine-readable contract that can evolve without mass-rewriting the corpus.

Target metadata dimensions:
- identity: name, description, version, category
- lifecycle: status, maturity
- contract: inputs, outputs, failure modes
- dependencies and related capabilities
- compatibility
- provenance
- evidence
- validation
- freshness: last reviewed and review due
- security boundary
- license

Do not require every field on every legacy skill in the first migration. Add fields incrementally and validate them deterministically.

Deliverables:
- evidence taxonomy and evidence record format
- lifecycle state definitions
- provenance rules
- freshness/review rules
- compatibility representation
- schema/versioning plan
- deterministic validator and regression tests

Exit evidence: schema/tooling/fixtures demonstrate deterministic validation without weakening existing gates.

## Phase 2 â Capability intelligence â STRATEGIC FOLLOW-ON

Create and maintain `meta/MOST-WANTED-SKILLS.md` plus a generated machine-readable dataset when the signal collection is reproducible.

For each candidate capability record:
- capability
- demand signals
- signal dates and sources
- existing coverage
- quality gap
- evidence gap
- implementation gap
- ecosystem relevance
- proposed tier
- status
- verification date

Demand must be evidence-backed and privacy-respecting. Search volume must never be presented as adoption.

Priority is a transparent decision aid:

`Demand Ã capability importance Ã coverage gap Ã evidence gap Ã ecosystem relevance`

It is not an objective truth score.

Exit evidence: at least one reproducible signal collection path and a backlog that clearly separates observed evidence from COO judgment.

**2026-10-04 implementation:** the first public GitHub issue-search collector is implemented and scheduled/manual collection produces a raw evidence artifact. The controlled collection run, first evidence review, and coverage/evidence reconciliation are complete. IDE integration is selected as the first Phase 3 migration slice because the demand signal is traceable and canonical coverage lacks a dedicated IDE integration contract. No popularity ranking is used.

## Phase 3 â High-value skill migration

Replace directory-order migration with demand/evidence-driven selection.

Corpus tiers:
- A â high-demand capabilities
- B â foundational capabilities
- C â useful/lower-demand capabilities
- D â experimental/niche
- E â redundant/obsolete

For each selected skill:
Inspect â classify â identify evidence â identify demand â identify dependencies â define contract â enrich â validate â create projection â verify â document.

A migration is incomplete if it only adds frontmatter.

## Phase 4 â Agent Skills distribution â VERIFIED CORPUS BASELINE

The deterministic canonical-to-Agent-Skills projection is now generated and verified for the full currently eligible corpus.

Verified state:
- 382 files are present in the quality corpus, including one intentional `00-sandbox` fixture; the production/public canonical corpus contains 381 skills across 17 categories.
- 264 canonical entries are eligible for deterministic Agent Skills projection.
- 118 canonical entries are blocked by the existing eligibility/reconciliation contract.
- 302 Agent Skills packages are present on the verified main baseline.
- Collision-safe naming is deterministic and validator-compatible.
- Reconciliation, Agent Skills validation, security, graph, build, and test gates passed on the final corpus PR.

Remaining Phase 4 work is distribution hardening and publication, not regeneration of the already verified corpus.

Requirements:
- deterministic generation
- schema validation
- provenance
- security boundaries
- explicit inputs/outputs where applicable
- reproducible examples
- no private chain-of-thought
- no unsupported production claims

Do not claim full-corpus Agent Skills compliance until automated evidence proves it.

## Phase 5 â Deterministic discovery

Evolve the generated registry toward:
- `skills.json`
- `categories.json`
- `graph.json`
- `evidence.json`
- `demand.json`
- `compatibility.json`

Discovery must support capability, keyword, category, dependency, compatibility, evidence, and freshness filtering without requiring a hosted SaaS backend.

Evaluate semantic retrieval only after deterministic indexes and metadata contracts are stable.

## Phase 6 â Evidence and benchmark layer

Introduce reproducible benchmark infrastructure for important capability classes.

Every benchmark must define task, inputs, expected behavior, evaluation criteria, test data, methodology, and historical results.

Keep benchmark results separate from classifier labels, structural validation, and external adoption evidence.

## Phase 7 â Ecosystem intelligence

Use legitimate public signals to detect:
- emerging capabilities
- missing capabilities
- obsolete patterns
- framework requirements
- dependency changes
- recurring capability requests

Never fabricate popularity or adoption.

## Phase 8 â Universal distribution

Only when deterministic generation, validation, provenance, integrity verification, and reproducible publication exist, publish:

`/.well-known/agent-skills/index.json`

Published artifacts must carry version, provenance, validation status, and SHA-256 integrity.

## Continuous operating cadence

Every change: inspect â validate â document â verify.

Weekly:
- stale skills
- broken dependencies
- workflow failures
- demand signals
- migration progress
- security findings
- generated artifact drift

Monthly:
- taxonomy
- evidence model
- compatibility
- benchmark coverage
- workflow complexity
- architecture

Quarterly:
- strategic review: is Skills Tree becoming more useful as AI-agent capability infrastructure?

## Current verified execution position

The repository's live development record verifies the governance/registry foundation, P1.1âP1.11, P2.1, P2.2, the post-P2.2 runtime integrations, graph fail-closed validation, recommendation/blueprint context, and CLI search. No numbered P2.3 requirement is defined. The immediate execution queue is governed by the 2026-10-11 block above: documentation synchronization, current-head Agent Skills reconciliation, and resolution of the activation qualification discrepancy before unrelated feature work.

The strategic phases below remain the long-term product direction. They must not be treated as the immediate execution queue when the verified architecture audit identifies a higher-priority foundational gap.

## Previous execution queue â 2026-10-07 (historical)

1. Synchronize the project brain and public README counts.
2. Enforce the 381-skill public projection boundary while retaining the 382-file quality/test corpus.
3. Run retrieval and skill-selection evidence for canonical `skills/**` changes against branch-generated projections.
4. Verify generated public projections and exact-head CI after merge.
5. Collect Issue #357's 12 real independent runtime observations.
6. Decide on Skill-description, routing/runtime, or evaluation changes only if those observations produce measured failures.

Issue #336 is resolved and must not remain in the active execution queue.


## Definition of done

A roadmap item is complete only when implementation, tests/verification, documentation, and current-state evidence all agree.


## Verified Runtime Data-Schema Slice â 2026-10-02

The UniversalRegistry now validates the loaded registry against the dedicated `meta/universal-registry-data.schema.json` instance schema before semantic integrity, entity-specific contracts, and graph validation.

The existing `meta/universal-registry.schema.json` is preserved as the ontology/contract-definition schema; it is not treated as the shape of `registry/universal_registry.json`. Implementation and adapter structural contracts remain authoritative in their dedicated schemas and are resolved locally through the runtime's explicit JSON Schema resource registry.

**Verification:** PR #241 merged as `93c50c3616a7c558b483f341f44a91509ed032ca`; exact-head Test Suite, Security Scan, PR Checks, and Build & Verify Wheel passed.

**Next:** fresh runtime/consumer invariant audit. No numbered P2.3 requirement is created.


## Behavioral Evaluation Runtime â Verified Implementation 2026-10-03

PR #272 established the dedicated Benchmark contract and typed runtime boundary identified by the post-schema universal-registry audit. The contract validates reproducible evaluation definitions, benchmark subjects are checked against registered entity IDs, and `UniversalRegistry` exposes deterministic `resolve_benchmark()` and `benchmarks_for_entity()` access.

PR #274 supplied the final contract-integrity and regression-test fixes. The final exact head `4738303caeb6a9129af8a0f84cab4219aade5084` passed the required CI matrix before merge.

This establishes benchmark-definition infrastructure only. It does not represent benchmark results, rankings, production readiness, or external evaluation evidence.

## Anti-Slop Quality Gate â Verified Implementation 2026-10-03

PR #273 established deterministic anti-slop enforcement for changed skills, with PR #275 resolving rename detection and lowercase lifecycle-state false positives.

The final #273 head `4477d33d846c68d71b666e6c283c8787312e023f` passed its required CI matrix before merge. The gate is scoped to changed skills and is not a retroactive corpus-cleanup claim.

**Next:** continue the fresh universal-registry architecture audit; do not treat these slices as permission to invent a new phase requirement.

## Security Corpus Migration â Verified Implementation 2026-10-02

The first controlled security corpus migration batch upgraded the nine remaining security stubs in category 14. The batch preserves the canonical `skills/` source and strengthens the evidence-backed migration gate with explicit I/O, failure modes, security boundaries, related metadata, and authoritative references.

PR #243 merged as `40fb35aa6c54438f08062c89c118815262b6fe98` after the final validation matrix passed.

The quality-report workflow was hardened with a trusted post-merge `pull_request_target: closed` trigger. The live generated report now confirms 374 skills: 202 battle-tested, 159 enriched, 13 stubs, 0 invalid; category 14-security has 13 battle-tested and 0 stubs.

**Next:** continue with the remaining 13 verified stubs, selecting the next batch by evidence, safety, and agent utility rather than directory order.


## AI Source Discovery Slice â 2026-10-02

The product mission now has an explicit public discovery surface for AI agents and developers: root `llms.txt`, `docs/AI_DISCOVERY.md`, README AI-source guidance, the existing machine-readable `docs/api/skills.json`, and the existing `agent-skills/` compatibility layer.

This is a discovery/documentation layer only. It does not create a competing catalog or declare the future `/.well-known/agent-skills/index.json` live. The latter remains gated on deterministic generation, validation, provenance, publication reproducibility, and SHA-256 verification.

**Next:** discovery-surface validation is complete; the remaining work is the separately gated `/.well-known/agent-skills/index.json` publication boundary.
\n\n## Agent Skills Distribution Contract â VERIFIED IMPLEMENTATION â 2026-10-02

PR #251 established the executable distribution contract and merged to `main` as `f1d169c3fd9388cf4244d9d4bfc4c64df382a1bb`.

That historical baseline was superseded by the verified reconciliation state on 2026-10-04: 375 canonical entries, 258 eligible, 117 blocked, and 296 Agent Skills packages. PR #305 completed provenance/collision reconciliation and made it enforceable in CI.

The deterministic projector, read-only reconciliation workflow, validator, regression tests, and exact-head CI gates are verified. Phase 4 reconciliation hardening is complete; `/.well-known/agent-skills/index.json` is published and verified live; the discovery publication boundary is closed.

**Status:** Publication implementation is present in `deploy-pages.yml`: the Pages artifact builds `/.well-known/agent-skills/index.json` from `tools/build_agent_skills_discovery.py`, validates the local publication bytes, and verifies the served URL with `tools/verify_agent_skills_discovery.py`. No second generator or reconciler is introduced.

**Verified:** GitHub Pages deployment run `37227197992` for main commit `1b3a5f387a17ce6b57885b06d6f26db060a8784d` completed successfully on 2026-10-04. The `Deploy to GitHub Pages` job and its `Verify served discovery bytes` step both passed. This closes the live discovery publication boundary.

**Next:** Reconcile demand evidence against canonical coverage, evidence tiers, freshness, dependencies, and runtime proof. The first preferred investigation is skill evaluation / invocation evidence and retrieval quality; do not add raw skills until an implementation or evidence gap is demonstrated.


## Universal Graph Relationship Runtime Boundary â 2026-10-03

A fresh post-freshness audit identified a fail-open semantic boundary: the graph schema declares deferred relationship types, while runtime semantics currently cover only the six relationships used by the canonical graph. The runtime previously accepted unsupported schema-valid relationships silently.

The selected correction keeps the schema vocabulary unchanged but makes runtime-supported relationships explicit and rejects unsupported relationship types. No new graph semantics or graph records are introduced.

**Branch:** `runtime/graph-relationship-boundary-20261003`

**Verification status:** implementation and focused regression coverage are present; exact-head CI and merge are pending.

**Status:** The CLI `search` gap is resolved on main and has a deterministic contract plus regression coverage in `tests/test_search_cli.py`, `tests/test_search_engine.py`, and `tests/test_search_index_contract.py`.

**Next:** verify the externally published discovery boundary; do not create another search implementation.


## Phase 4 Distribution Hardening â VERIFIED ON MAIN â 2026-10-04

The deterministic Agent Skills corpus exposed a remaining control gap: reconciliation could report an eligible missing projection without making CI fail. The merged implementation adds the explicit read-only reconciliation gate and regression coverage.

Verified merged-main state:

- 376 canonical skills scanned after the IDE Integration Phase 3 slice.
- 259 eligible deterministic projections.
- 117 blocked canonical entries.
- Agent Skills package count will be reconciled by the deterministic projection workflow.
- Kanban is deterministically projected.
- CI now executes tools/reconcile_agent_skills.py --check.
- Unexpected projection drift and unresolved deterministic target-name collisions are now explicit failure categories.
- `/.well-known/agent-skills/index.json` is published and verified live.

Status is VERIFIED ON MAIN. PR #305 exact head `1c1d70a337f9952cd2c24d555ee9d67bab9cbe30` passed the applicable CI gates before merge as `a9a649481c68bf0dd33447a2238174ebd8b79a4b`.


## Full Repository Re-Audit â 2026-10-04

The current audit verified the existing canonical/projection boundaries and found no need for a new generator, catalog, reconciler, search index, graph writer, JSON-LD writer, Agent Skills generator, Pages deployment path, or release publisher.

Immediate execution state:
1. Security-gate hardening is the active implementation slice: blocking Bandit SAST plus `pip-audit --strict`.
2. Authoritative documentation is being synchronized to the verified 40-workflow inventory and current release baseline.
3. Issue #276 remains the current universal-registry architecture audit thread; do not invent P2.3 or force registry population beyond evidence-backed coverage.
4. Issue #159 remains an external GitHub control-plane requirement for branch protection and required status enforcement.
5. Historical audit documents remain historical evidence and must not be treated as current architecture.

The full evidence record is `meta/audits/FULL_REPOSITORY_AUDIT_2026-10-04.md`.


## Demand Intelligence â Activation Evidence Gate â 2026-10-06

The preferred demand/evidence investigation is now executable. The repository contains a bounded trace-based benchmark for real skill activation and invocation evidence, using existing discovery/selection and observability boundaries.

**Current state:** harness verified on main; empirical routing evidence pending.

**Required next step:** collect real structured traces from a compatible agent runtime for `benchmark/skill-activation-v1`, then record expected activation rate, false activation rate, invocation-evidence rate, and repeated-run variance.

**Decision rule:** measured failures may justify skill-description remediation or runtime/evaluation changes; absence of measured failures does not justify new capability creation. No new search engine or routing authority is permitted by this slice.


## Demand Intelligence â Real Activation Evidence Collection â 2026-10-06

The activation evidence instrument and its machine-readable observation contract are now implemented on main. The remaining gate is empirical: collect real runtime traces conforming to `meta/skill-activation-observation.schema.json` and evaluate `benchmark/skill-activation-v1`.

Decision rule remains unchanged: measured failures may justify skill-description or runtime/evaluation changes; no raw skill or routing authority should be added without evidence.


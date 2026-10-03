# Skills Tree — Executable Product Roadmap

> Strategic roadmap for the Skills Tree product mission.
> Effective: 2026-10-02
> Canonical source: `skills/`
> Product mission: `meta/PRODUCT_MISSION.md`
> Execution mission: `meta/COO_MASTER_MISSION.md`

## Product outcome

Skills Tree is a public, trusted, machine-discoverable source of AI skills. AI agents should be able to find the right skill here, and humans should be able to discover, understand, use, share, and contribute skills easily.

Roadmap work must strengthen AI discovery, human usability, reliable consumption, trust/evidence, distribution, sharing, contribution, and organic GitHub adoption.

Raw skill count and raw stub count are engineering measurements, not product objectives.

## Priority order

Security > Correctness > Canonical architecture > Discovery > Evidence > Freshness > Interoperability > Quality > Developer experience > Cosmetic improvements.

## Phase 0 — Governance stabilization — ACTIVE — final reconciliation

1. Maintain the live 42-file workflow inventory and classify every workflow as authoritative, supporting, manual recovery, scheduled maintenance, or generated-main writer.
2. Maintain exactly one authoritative Pages deployment.
3. Maintain exactly one authoritative release architecture.
4. Consolidate generated-main writers where technically safe.
5. Require explicit reason, least privilege, deterministic output, serialization, bounded retry/rebase, and failure visibility for every generated-main writer.
6. Remove synthetic repository churn and duplicate automation only after dependency/reference verification.
7. Synchronize governance and current-state documentation with actual GitHub state.
8. Verify security gates and document any GitHub control-plane limitations that the connector cannot inspect.
9. Harden the identified `validate-graph.yml` PR permission boundary without weakening trusted-main graph generation. **VERIFIED 2026-10-02:** validation is read-only; trusted-main graph generation is isolated to a write-scoped job; quality generation depends on graph generation.

Exit evidence: workflow inventory, decision records, current-state update, passing relevant CI, verified permission boundaries, and no undocumented automation ownership.

## Phase 1 — Registry foundation — VERIFIED — completed foundation

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

## Phase 2 — Capability intelligence — STRATEGIC FOLLOW-ON

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

`Demand × capability importance × coverage gap × evidence gap × ecosystem relevance`

It is not an objective truth score.

Exit evidence: at least one reproducible signal collection path and a backlog that clearly separates observed evidence from COO judgment.

## Phase 3 — High-value skill migration

Replace directory-order migration with demand/evidence-driven selection.

Corpus tiers:
- A — high-demand capabilities
- B — foundational capabilities
- C — useful/lower-demand capabilities
- D — experimental/niche
- E — redundant/obsolete

For each selected skill:
Inspect → classify → identify evidence → identify demand → identify dependencies → define contract → enrich → validate → create projection → verify → document.

A migration is incomplete if it only adds frontmatter.

## Phase 4 — Agent Skills distribution — VERIFIED CORPUS BASELINE

The deterministic canonical-to-Agent-Skills projection is now generated and verified for the full currently eligible corpus.

Verified state:
- 374 canonical entries scanned.
- 250 eligible projections generated.
- 124 canonical entries remain blocked.
- 288 total Agent Skills packages remain on `main`, including retained blocked legacy packages and the intentional registry helper.
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

## Phase 5 — Deterministic discovery

Evolve the generated registry toward:
- `skills.json`
- `categories.json`
- `graph.json`
- `evidence.json`
- `demand.json`
- `compatibility.json`

Discovery must support capability, keyword, category, dependency, compatibility, evidence, and freshness filtering without requiring a hosted SaaS backend.

Evaluate semantic retrieval only after deterministic indexes and metadata contracts are stable.

## Phase 6 — Evidence and benchmark layer

Introduce reproducible benchmark infrastructure for important capability classes.

Every benchmark must define task, inputs, expected behavior, evaluation criteria, test data, methodology, and historical results.

Keep benchmark results separate from classifier labels, structural validation, and external adoption evidence.

## Phase 7 — Ecosystem intelligence

Use legitimate public signals to detect:
- emerging capabilities
- missing capabilities
- obsolete patterns
- framework requirements
- dependency changes
- recurring capability requests

Never fabricate popularity or adoption.

## Phase 8 — Universal distribution

Only when deterministic generation, validation, provenance, integrity verification, and reproducible publication exist, publish:

`/.well-known/agent-skills/index.json`

Published artifacts must carry version, provenance, validation status, and SHA-256 integrity.

## Continuous operating cadence

Every change: inspect → validate → document → verify.

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

The repository's live development record verifies the governance/registry foundation and the deterministic Agent Skills corpus projection, P1.1–P1.11, P2.1, P2.2, the post-P2.2 Evidence runtime integration, the post-P2.2 Compatibility runtime integration, the verified Skill runtime facade integration, the verified Capability runtime facade integration, and the verified Goal runtime facade integration. The `validate-graph.yml` permission boundary is now hardened and CI-verified. Remaining Phase 0 work is limited to control-plane reconciliation/limitations and any material security findings discovered by inspection. The deterministic Agent Skills corpus is now a verified distribution baseline. The next distribution decision is whether the remaining evidence gates justify implementing `/.well-known/agent-skills/index.json`; otherwise continue the fresh universal-registry architecture audit. No numbered P2.3 requirement is defined.

The strategic phases below remain the long-term product direction. They must not be treated as the immediate execution queue when the verified architecture audit identifies a higher-priority foundational gap.

## Current execution queue

1. Complete any remaining Phase 0 control-plane reconciliation observable through available APIs and explicitly record unavailable settings; do not silently change high-impact repository governance.
2. Verify and merge the Universal Graph relationship runtime boundary only after exact-head CI and review/governance gates pass.
3. Re-audit the merged universal-registry runtime and consumer surface from the verified benchmark, anti-slop, freshness, and graph-integrity baseline.
4. Reconcile the remaining CLI search documentation/implementation gap (Issue #86) using existing search/runtime primitives; do not duplicate search logic.
5. Reconcile legacy open issues against the current roadmap without closing valid requirements merely because they are old.
6. Update decision memory, architecture documentation, development knowledge, roadmap, current state, and handoff state in the same cycle.
7. Re-verify live `main`, CI, generated artifacts, and documentation before selecting the next slice.
8. Resume strategic capability-intelligence and demand-driven work only when the foundational runtime path is sufficiently established by evidence.

## Definition of done

A roadmap item is complete only when implementation, tests/verification, documentation, and current-state evidence all agree.


## Verified Runtime Data-Schema Slice — 2026-10-02

The UniversalRegistry now validates the loaded registry against the dedicated `meta/universal-registry-data.schema.json` instance schema before semantic integrity, entity-specific contracts, and graph validation.

The existing `meta/universal-registry.schema.json` is preserved as the ontology/contract-definition schema; it is not treated as the shape of `registry/universal_registry.json`. Implementation and adapter structural contracts remain authoritative in their dedicated schemas and are resolved locally through the runtime's explicit JSON Schema resource registry.

**Verification:** PR #241 merged as `93c50c3616a7c558b483f341f44a91509ed032ca`; exact-head Test Suite, Security Scan, PR Checks, and Build & Verify Wheel passed.

**Next:** fresh runtime/consumer invariant audit. No numbered P2.3 requirement is created.


## Behavioral Evaluation Runtime — Verified Implementation 2026-10-03

PR #272 established the dedicated Benchmark contract and typed runtime boundary identified by the post-schema universal-registry audit. The contract validates reproducible evaluation definitions, benchmark subjects are checked against registered entity IDs, and `UniversalRegistry` exposes deterministic `resolve_benchmark()` and `benchmarks_for_entity()` access.

PR #274 supplied the final contract-integrity and regression-test fixes. The final exact head `4738303caeb6a9129af8a0f84cab4219aade5084` passed the required CI matrix before merge.

This establishes benchmark-definition infrastructure only. It does not represent benchmark results, rankings, production readiness, or external evaluation evidence.

## Anti-Slop Quality Gate — Verified Implementation 2026-10-03

PR #273 established deterministic anti-slop enforcement for changed skills, with PR #275 resolving rename detection and lowercase lifecycle-state false positives.

The final #273 head `4477d33d846c68d71b666e6c283c8787312e023f` passed its required CI matrix before merge. The gate is scoped to changed skills and is not a retroactive corpus-cleanup claim.

**Next:** continue the fresh universal-registry architecture audit; do not treat these slices as permission to invent a new phase requirement.

## Security Corpus Migration — Verified Implementation 2026-10-02

The first controlled security corpus migration batch upgraded the nine remaining security stubs in category 14. The batch preserves the canonical `skills/` source and strengthens the evidence-backed migration gate with explicit I/O, failure modes, security boundaries, related metadata, and authoritative references.

PR #243 merged as `40fb35aa6c54438f08062c89c118815262b6fe98` after the final validation matrix passed.

The quality-report workflow was hardened with a trusted post-merge `pull_request_target: closed` trigger. The live generated report now confirms 374 skills: 202 battle-tested, 159 enriched, 13 stubs, 0 invalid; category 14-security has 13 battle-tested and 0 stubs.

**Next:** continue with the remaining 13 verified stubs, selecting the next batch by evidence, safety, and agent utility rather than directory order.


## AI Source Discovery Slice — 2026-10-02

The product mission now has an explicit public discovery surface for AI agents and developers: root `llms.txt`, `docs/AI_DISCOVERY.md`, README AI-source guidance, the existing machine-readable `docs/api/skills.json`, and the existing `agent-skills/` compatibility layer.

This is a discovery/documentation layer only. It does not create a competing catalog or declare the future `/.well-known/agent-skills/index.json` live. The latter remains gated on deterministic generation, validation, provenance, publication reproducibility, and SHA-256 verification.

**Next:** validate this discovery surface in CI, then continue toward generated Agent Skills/discovery artifacts only when the repository's distribution completion gate is satisfied.
\n\n## Agent Skills Distribution Contract — VERIFIED IMPLEMENTATION — 2026-10-02

PR #251 established the executable distribution contract and merged to `main` as `f1d169c3fd9388cf4244d9d4bfc4c64df382a1bb`.

The verified audit baseline is 374 canonical skill entries, 250 currently eligible for projection, 124 blocked, and eight deterministic-name collisions. Existing `agent-skills/` contains 280 validator-passing packages, which require provenance reconciliation before they are treated as generated projections.

The deterministic projector, read-only audit workflow, validator, regression tests, and exact-head CI gates are verified. This does not complete Phase 4 and does not publish `/.well-known/agent-skills/index.json`.

**Next:** reconcile existing packages, resolve canonical collisions, then generate eligible projections in independently verifiable batches. Only after artifact/provenance reconciliation should discovery-index and SHA-256 publication work begin.


## Universal Graph Relationship Runtime Boundary — 2026-10-03

A fresh post-freshness audit identified a fail-open semantic boundary: the graph schema declares deferred relationship types, while runtime semantics currently cover only the six relationships used by the canonical graph. The runtime previously accepted unsupported schema-valid relationships silently.

The selected correction keeps the schema vocabulary unchanged but makes runtime-supported relationships explicit and rejects unsupported relationship types. No new graph semantics or graph records are introduced.

**Branch:** `runtime/graph-relationship-boundary-20261003`

**Verification status:** implementation and focused regression coverage are present; exact-head CI and merge are pending.

**Next after merge:** re-audit the merged runtime, then address the independently verified CLI `search` gap.

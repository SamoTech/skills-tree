# Skills Tree — Executable Product Roadmap

> Strategic roadmap for the AI-agent capability registry.
> Effective: 2026-10-02
> Canonical source: `skills/`
> Strategic mission: `meta/COO_MASTER_MISSION.md`

## Product outcome

Skills Tree is successful when an AI agent can reliably discover an appropriate capability, understand its contract, determine its evidence and freshness, identify dependencies and compatibility, consume a standard representation, and verify the evidence behind it.

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

## Phase 4 — Agent Skills distribution

Expand `agent-skills/` for high-value canonical skills.

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

The repository's live development record verifies Phase 0 governance/registry foundation work, P1.1–P1.11, P2.1, P2.2, the post-P2.2 Evidence runtime integration, the post-P2.2 Compatibility runtime integration, and the verified Skill runtime facade integration. The `validate-graph.yml` permission boundary is now hardened and CI-verified. Remaining Phase 0 work is limited to control-plane reconciliation/limitations and any material security findings discovered by inspection. The immediate Phase 2 engineering direction is a fresh universal-registry runtime architecture audit; no numbered P2.3 requirement is defined.

The strategic phases below remain the long-term product direction. They must not be treated as the immediate execution queue when the verified architecture audit identifies a higher-priority foundational gap.

## Current execution queue

1. Complete the remaining Phase 0 control-plane reconciliation observable through available APIs and explicitly record unavailable settings; do not silently change high-impact repository governance.
2. Perform another fresh universal-registry runtime architecture audit after the verified Skill runtime facade integration.
3. Implement the smallest evidence-backed schema → runtime → behavioral-test slice identified by that audit.
4. Update decision memory, architecture documentation, development knowledge, roadmap, and current state in the same cycle.
5. Re-verify live `main`, CI, generated artifacts, and documentation before selecting the next slice.
6. Resume strategic capability-intelligence and demand-driven work only when the foundational runtime path is sufficiently established by evidence.

## Definition of done

A roadmap item is complete only when implementation, tests/verification, documentation, and current-state evidence all agree.

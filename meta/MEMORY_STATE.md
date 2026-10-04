# MEMORY STATE

**Last reconciled:** 2026-10-04
**Current execution source of truth:** `meta/DEVELOPMENT_KNOWLEDGE.md`
**Governance authority:** `meta/PROJECT_CONSTITUTION.md`
**Execution model:** `meta/AGENT_OPERATING_MODEL.md`

---

## Verified Active State

| Key | Value |
|---|---|
| Main HEAD at task baseline | `20ed032bdb83f22ef3bf37debb3004ed8153d9a8` |
| Verified roadmap | P1.1–P1.11 + P2.1 + P2.2 |
| Current phase | Discovery and distribution hardening |
| Highest verified roadmap item | P2.2 — Typed runtime access and validation |
| Current audit-derived slice | JSON-LD export governance audit |
| Active branch | None — main verified; next work is the remaining machine-readable consumer/projection audit |
| Active governance blocker | None |
| Current implementation registry | `implementation/code-reviewer-system` |
| MCP classification | Protocol; not an Implementation |
| New claims policy | No provider/platform/framework/model/adapter/compatibility claims without authoritative provenance |

---

## State Reconciliation

P1.1–P1.11 and P2.1/P2.2 are verified on `main`. PR #131, Capability↔Adapter linkage symmetry, is merged in `264c467e3c0826503d0c63b19db81edf3153ce33` after green CI. No numbered P2.3 item is invented.

The post-P2.2 graph relationship integrity slice is merged in `77737a0fbf743c1cf28431b63790b9acc4d7c469` after green CI.

The fresh post-merge audit identified an Implementation evidence traceability gap: referenced evidence IDs were validated for all Implementations, but reverse claim support in `evidence.supports` was enforced only for `verified` Implementations. The current audited Implementation is `candidate` and already references repository-backed evidence.

The active branch enforces reverse evidence support for every Implementation lifecycle state and adds focused regression coverage. No registry entities, ecosystem claims, compatibility facts, or MCP classifications are added.

## Current Post-P2.2 State

PR #133 (Implementation evidence traceability) is merged into `main` at `3b4ddc44ba10dd3d97433b7095dfd624fd219a95`.

A fresh post-merge audit found that Adapter records have a normative contract and validation but lacked typed read-only runtime access analogous to Implementation access. The active branch adds `AdapterRecord`, deterministic Adapter-by-ID lookup, deterministic Implementation-to-Adapter lookup, and regression coverage without changing registry claims.

MCP remains a Protocol. No compatibility or ecosystem claims are added.

## Next Action

Run focused regression and required CI on `phase2/evidence-contract-runtime-20260919`. If green, open a PR, verify its exact head and all required checks, merge only the green head SHA, then verify the resulting `main` HEAD. If CI fails, inspect the actual failed job/log and make only the smallest architectural correction on the existing branch.


## State Reconciliation — 2026-10-04

PR #305 completed the Agent Skills reconciliation gate; PR #306 synchronized the operational documentation and removed the obsolete branch-specific apply workflow; PR #307 removed the remaining stale branch-state wording. The current main baseline is 375 canonical entries, 258 eligible, 117 blocked, and 296 Agent Skills packages.

The machine-readable discovery audit verified `docs/api/skills.json` as the canonical registry projection, `docs/search-index.json` and `data/search-index.json` as identical search-only projections, and the verified CLI search runtime consuming the generated projection without creating a second index. The remaining gated boundary is remaining machine-readable consumer/projection audit.

Historical state entries are retained below as history and are not treated as current state.

## State Reconciliation — 2026-10-02

A fresh post-schema runtime/consumer audit identified a narrow missing typed Goal→Capability access path. The development branch `feat/goal-capability-runtime-boundary` adds `GoalRuntime.capabilities_for_goal()`, exposes `UniversalRegistry.capabilities_for_goal()`, and routes `skills_for_goal()` through the validated Capability boundary.

No registry entities or ecosystem claims were changed. No numbered P2.3 item was invented.

Verification remains pending exact-head CI and required repository checks.

## State Reconciliation — 2026-10-04 Graph Projection

PR #315 is merged on main as `5c5720d61ed757e7d0f94cdfb3309ac8eb0d213f`.

The graph boundary is now single-writer and schema-enforced: `tools/build_graph.py` generates the graph, `validate-graph.yml` validates and publishes the generated projections, and the duplicate `build-graph.yml` writer is removed.

`data/SKILLS_GRAPH.json` and `docs/api/graph.json` are synchronized byte-for-byte on main. Current generated graph: 375 nodes, 240 edges, 9 REQUIRES edges, 0 warnings.

Next action is a fresh audit of remaining machine-readable consumers/projections. No additional graph generator, reconciler, search index, or deployment path should be introduced.
## State Reconciliation — 2026-10-04 JSON-LD Export Governance

PR #316 is merged on main as `20ed032bdb83f22ef3bf37debb3004ed8153d9a8`.

JSON-LD remains generated by `tools/export_skills.py` and written by `export-skills.yml`; no separate JSON-LD workflow exists on current main. The new `tools/verify_jsonld_export.py` validator and focused tests enforce structural consistency between `docs/api/skills.json` and `docs/api/jsonld/`.

`export-skills.yml` now triggers on skill source, exporter, and UniversalRegistry changes and runs the JSON-LD validator before committing generated artifacts.

Next action: continue the remaining machine-readable consumer/projection audit. Do not introduce another JSON-LD generator or workflow.
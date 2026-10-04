# Most-Wanted Skills — Demand Backlog

> Evidence-backed demand backlog for Skills Tree.
> This file intentionally contains no fabricated popularity ranking.

## Purpose

Identify important AI-agent capabilities that are missing, weakly represented, stale, duplicated, or insufficiently evidenced.

The backlog is a decision-support artifact. It separates observed demand signals from COO prioritization.

## Signal policy

Acceptable signals include:

- dated public GitHub references/search observations
- repository issues and discussions
- public package/ecosystem activity
- framework documentation showing recurring capability requirements
- public Agent Skills/MCP ecosystem activity
- repeated capability requests with traceable provenance
- internal repository dependency/coverage gaps

Do not use private user data. Do not represent search volume as adoption. Do not fabricate demand.

## Record format

For each candidate:

| Field | Requirement |
|---|---|
| Capability | normalized capability name |
| Demand signals | dated public signals and sources |
| Existing coverage | current Skills Tree coverage |
| Quality gap | documented quality deficiency |
| Evidence gap | missing evidence tier or proof |
| Implementation gap | missing/incomplete capability |
| Ecosystem relevance | documented compatibility/relevance |
| Proposed tier | A/B/C/D/E with rationale |
| Priority | transparent COO decision aid |
| Status | proposed/investigating/selected/in-progress/validated/deferred |
| Verified | date of latest verification |

## Initial backlog state

No capability is ranked here until a reproducible public-signal collection pass is performed.

The first implementation task is therefore to build the signal collection and verification path, then populate this backlog from evidence.

**2026-10-04 status:** `tools/collect_demand_signals.py`, `meta/demand-sources.json`, and the scheduled/manual `.github/workflows/demand-signals.yml` now provide the first reproducible public-signal path. The collector produces raw GitHub issue-search evidence only; it does not assign popularity, adoption, or priority. The first controlled public-signal review was performed on 2026-10-04 using the configured GitHub issue-search sources. The raw query result counts were 64, 63, and 54 respectively; these queries overlap heavily and include non-demand operational/security issues, so the counts are not a popularity measure.

Observed capability-related signal cohort (unranked):

| Capability signal | Public evidence | Current interpretation |
|---|---|---|
| Search / discovery | Issue #86: `skills-tree search <query>` | Demand signal; implementation is now verified, so this is not an open implementation gap. |
| Memory | Issue #87: hierarchical memory management, cache eviction, forgetting curves | Repeated capability signal; coverage/evidence audit required before prioritization. |
| Code / IDE integration | Issue #88: IDE integration, pair-programming, polyglot agents | Capability signal; current coverage and evidence gap must be measured. |
| Reasoning | Issue #90: expand reasoning skills | Capability signal; do not equate issue request with external adoption. |
| Action execution | Issue #91: expand action-execution skills | Capability signal; coverage/evidence gap must be measured. |

These records are **observed evidence, not ranked demand**. Closed issues remain valid historical signals but do not prove current demand. The next step is to reconcile this cohort against canonical coverage, evidence tiers, freshness, and dependency relationships before selecting any Phase 3 migration.

The first production snapshot remains intentionally collected as a workflow artifact before being promoted into a generated machine-readable backlog.

## External corroboration — 2026-10-04

A separate public-source review was performed after the repository-local signal pass. These are corroborating ecosystem signals, not popularity rankings:

| Signal | Public evidence | Relevance to Skills Tree |
|---|---|---|
| Agent Skills ecosystem scale | GitSkills reports 3,797,117 `SKILL.md` files across 282,200 public repositories collected in July 2026. | Strong evidence that skill discovery, provenance, quality, reuse, and maintenance are ecosystem-scale problems. |
| Agent Skills platform adoption | GitHub documents Agent Skills support across Copilot cloud agent, Copilot code review, Copilot CLI, Copilot app, VS Code, and JetBrains IDEs. | Confirms cross-agent/IDE interoperability as a live ecosystem concern. |
| MCP + Agent Skills composition | MCP documentation describes portable `SKILL.md` packages used to guide MCP server design and says the skills can work with any agent implementing the format. | Supports MCP/skill interoperability as a concrete ecosystem requirement. |
| Skill retrieval/evolution/governance | Current 2026 Agent Skills survey resources organize the field around skill representation, acquisition, retrieval/selection, evolution/governance, and evaluation. | Supports treating retrieval, evaluation, and governance as first-class capability areas rather than adding raw skill count. |
| Skill safety/evidence | Research on 40,285 public skills reports concentration, redundancy, supply-demand imbalance, and non-trivial safety risks. | Reinforces evidence, anti-slop, provenance, security boundaries, and quality gates as product differentiators. |

These external signals do **not** establish that any one capability is the next highest-demand skill. They justify the next reconciliation pass: map observed demand signals to existing canonical coverage, evidence tier, freshness, dependency relationships, and implementation gaps.

## First coverage reconciliation — 2026-10-04

The initial repository coverage check shows that the local signal cohort is already substantially represented:

- Memory: canonical coverage exists across short-term, working, episodic, semantic, procedural, long-term, cross-session, cross-thread, forgetting, RAG, vector retrieval, and verification-oriented skills.
- Code / IDE integration: `05-code/ide-integration.md` exists, alongside code generation, review, debugging, testing, Git, CI/CD, and dependency/security skills.
- Reasoning: `02-reasoning/` contains broad reasoning, planning, uncertainty, self-correction, reflection, decomposition, and decision-making coverage.
- Action execution: `04-action-execution/` contains concrete API, filesystem, process, browser/GUI input, notification, database, and form-action skills.
- Search / discovery: the CLI search and Agent Skills discovery/publication paths are now verified and are not open implementation gaps.

Therefore the observed demand cohort should **not** be converted directly into new skills. The next selection gate is to identify where existing coverage is weakly evidenced, stale, duplicated, or missing runtime/evaluation proof.

The preferred next investigation is **skill evaluation / invocation evidence and retrieval quality**, because external ecosystem evidence points to retrieval/selection, evolution/governance, and evaluation as material concerns while the current repository already has broad raw capability coverage.



## Priority model

Use:

`Demand × capability importance × coverage gap × evidence gap × ecosystem relevance`

The result is a prioritization aid, not a claim of objective popularity or universal importance.

## Required next steps

1. Define reproducible signal collectors.
2. Record sources and observation dates.
3. Normalize capability names.
4. Compare signals against current registry coverage.
5. Identify quality/evidence gaps.
6. Produce the first verified demand cohort.
7. Convert selected gaps into migration issues/PRs.
8. Recompute when ecosystem evidence changes.

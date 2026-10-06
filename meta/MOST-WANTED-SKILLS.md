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


## Agentic Loop — Retrieval/Evaluation Gate — 2026-10-04

**OBSERVE:** The live consumer search path is deterministic lexical retrieval over the canonical generated projection. The contract explicitly excludes semantic search, fuzzy matching, query expansion, and trust/quality scoring unless separately evidenced. Existing recommendation evaluation reports strong historical aggregate results (P@5 0.76, R@10 0.93) but also show recurring cross-goal ranking errors; the stored report is dated 2026-06-15 and therefore is not treated as current runtime evidence.

**ASSESS:** The repository already contains a universal registry runtime with typed evidence/benchmark access, deterministic goal/capability/skill traversal, provenance validation, compatibility checks, and defensive-copy behavior. Therefore there is no justification for adding another retrieval engine or registry. A stronger evidence gap exists in P0 capability evaluation coverage: the repository audit identifies CAP-007 semantic retrieval, CAP-011 self-evaluation, and CAP-014 tool execution as missing evaluation mappings. This finding requires live-state revalidation before implementation because the audit is historical.

**PLAN / DECIDE:** Opened GitHub Issue #335 as the bounded next implementation slice. It requires re-verifying the live evaluation ontology, defining the minimum canonical evaluation contracts using existing ontology/benchmark boundaries, adding executable behavioral tests and CI validation, and synchronizing documentation. Semantic search or new skills remain blocked until retrieval-quality evidence demonstrates a real implementation gap.

**Status:** `INVESTIGATING` — Issue #335. No new skill or competing search implementation is authorized by this loop.


## Retrieval / Evaluation Evidence Audit — 2026-10-05

The first evidence-driven investigation found a concrete gap in the existing evaluation boundary. `benchmarks/memory/retrieval-accuracy.md` is dated 2026-04-13 and its published model results have no current reproducible run artifact; its reproduction example uses a newer model identifier than the historical result table. Its related skill links also use the obsolete `skills/memory/...` path rather than the current category-prefixed canonical taxonomy. Separately, `intelligence/ontology/evaluation_ontology.json` is past its declared review due date (`2026-10-03`). The evaluation validation workflow did not previously trigger when that ontology itself changed; this trigger gap was fixed on 2026-10-05.

Issue #336 records the remediation boundary. This is classified as an **evidence/freshness/reproducibility gap**, not evidence that historical benchmark scores are false. No new retrieval skill is selected until the benchmark evidence is reproduced, retired, or explicitly re-qualified.

## Agentic Loop — Evaluation Gate Reconciliation — 2026-10-05

The evaluation workflow now reads the real canonical corpus under `intelligence/corpus/entries/` and explicitly reports the current missing P0 evaluation mappings instead of silently scanning the obsolete `data/corpus/` path. A declared-freshness audit also checks timestamp structure/order and surfaces overdue review dates without rewriting them.

The retrieval benchmark `benchmarks/memory/retrieval-accuracy.md` is now explicitly marked historical. Its canonical skill links were corrected to the current `03-memory` namespace, and the repository benchmark overview no longer treats every historical result as currently reproducible evidence.

No new retrieval skill, search engine, or popularity claim was created. Current bounded retrieval evidence is now verified by the 12-case deterministic benchmark (Recall@5 1.0000, MRR 0.9583, deterministic replay true). The remaining retrieval-quality boundary is broader representative failure coverage; the measured RAG ambiguity must not trigger ranking changes without that evidence. CAP-007, CAP-011, and CAP-014 evaluation mappings are now verified on main. Issue #335 and Issue #336 remain historical remediation records.

## New demand-gap candidate — Capability-Based Skill Selection — 2026-10-05

A new public-signal review identified a recurring capability request that is not represented by a dedicated canonical skill: **selecting the right skill/capability for a concrete task and routing execution based on task requirements, candidate fit, dependencies, and observed results**.

### Demand signals

| Signal | Evidence | Interpretation |
|---|---|---|
| Automated task breakdown + agent orchestration | Public GitHub issue BrianTruong23/kanban-coding-agents#8 requests automated decomposition plus agent assignment based on skills and performance, with dependency visualization. | Direct ecosystem demand for capability-aware routing and dependency-aware orchestration. |
| Skill selection / routing | Public GitHub issue searches for skill selection, agent routing, and orchestration return recurring active agent-routing and coordination work. | Corroborating signal; individual issue volume is not treated as adoption. |
| Runtime action decisioning | Public OWASP Agentic Top 10 discussion #802 describes pre-execution authorization, delegation controls, execution binding, and fail-closed runtime decisions. | Strong ecosystem relevance for selecting executable actions under authority and safety constraints. |
| Skills Tree behavioral gap | Current repository retrieval evidence proves search/retrieval quality, but task-specific competing-skill discrimination, dependency-aware selection, invocation, and next-skill decisions are not yet comprehensively benchmarked. | Internal implementation/evidence gap directly aligned with the demand signal. |

### Coverage reconciliation

Existing Skills Tree coverage already includes specialist-agent routing, role assignment, task decomposition, delegation, conditional branching, agent handoff, dependency graphs, registry eligibility, and deterministic search. Those skills are necessary building blocks but do not provide one canonical contract for **skill-level selection and next-step routing**.

This candidate therefore represents a **narrow missing capability**, not a request to duplicate the existing routing, search, registry, or orchestration frameworks.

### Selected migration

skills/15-orchestration/capability-based-skill-selection.md

Status: **proposed / implementation in progress** on the current branch.

Scope is intentionally limited to:

- required-capability identification;
- competing-skill discrimination;
- eligibility/evidence checks;
- prerequisite resolution;
- smallest-sufficient skill selection;
- invocation verification;
- failure-driven next-skill selection;
- explicit CONTINUE | BLOCKED | DONE outcome handling.

No popularity claim is made, and no new search or orchestration authority is introduced.

### Priority assessment

**Proposed tier: A — high strategic utility, evidence-backed gap.**

Rationale: the capability directly closes the gap between Skills Tree's now-verified retrieval layer and the product mission that agents should find **and use the right skill**. It also creates a concrete target for the next behavioral evaluation benchmark.

Verification date: 2026-10-05.


## New demand-gap candidate — Agent Skill Security Audit — 2026-10-06

A fresh ecosystem evidence pass identified a security capability that is not represented by a dedicated canonical skill: auditing an agent skill package itself before installation or execution. Existing Skills Tree security coverage includes sandboxing, secret scanning, permission checking, input sanitization, audit logging, and human approval, but those are controls around execution rather than a dedicated pre-installation audit contract.

### Demand signals

| Signal | Evidence | Interpretation |
|---|---|---|
| Agent-skill security auditing | OWASP Secure Agent Playbook issue #21 proposes an explicit Audit an agent skill play covering metadata/instruction consistency, shadow behavior, credential access, exfiltration, obfuscation, bundled scripts, hooks, and permission declarations. | Direct ecosystem demand for a pre-installation skill-audit procedure. |
| Malicious skill detection | 2026 research describes static and dynamic analysis of public agent skills and reports confirmed malicious examples. | Strong evidence that skill-package trust assessment is a distinct security problem. |
| Skills Tree internal coverage gap | Existing 14-security skills cover execution controls but no dedicated contract was found for auditing a complete third-party skill package before installation. | Concrete canonical capability gap; does not justify a second security framework. |

### Coverage reconciliation

Existing sandboxed execution, secret scanning, permission checking, input sanitization, and audit logging remain the implementation building blocks. The missing boundary is the pre-installation/pre-execution audit decision, including declared-vs-observed behavior, package inventory, evidence locations, sandbox requirements, and an explicit non-guarantee that passing static checks means safe.

### Selected migration

`skills/14-security/agent-skill-security-audit.md`

Status: VERIFIED ON MAIN — PR #350 merged as `436c15c745e1747e3ec1e931dccacea1ca013c7c` with exact-head CI passed.

### Priority assessment

**Proposed tier: A — high security utility, evidence-backed gap.**

Rationale: this closes a trust boundary directly related to Skills Tree product trust and composes with existing security controls instead of introducing a competing scanner or authorization system.

Verification date: 2026-10-06.


## Evaluation Ontology / P0 Coverage Repair — VERIFIED — 2026-10-06

The freshness audit initially exposed two real P0 evaluation gaps in CORPUS-001: CAP-018 `multi_turn_dialogue_management` and CAP-027 `compliance_logging`. Both were mapped using existing evaluation types; no new evaluation framework or metric type was introduced.

PR #354 merged to main as `15c455bbef43d5f88c17c0cbdbac1af09c8e2d04`. Exact-head CI passed Validate Evaluations, Governance Gate, Test Suite, Security Scan, Build & Verify Wheel, PR Checks, and Auto Label; Dependabot Review Gate was skipped. The canonical corpus now has evaluation mappings for all 10 P0 capabilities.

This closes the current P0 evaluation-mapping evidence gap. It does not claim empirical benchmark quality for those mappings; behavioral evidence remains a separate lifecycle step.


## New demand-gap candidate — Skill Activation / Invocation Evidence — 2026-10-06

A fresh public-source reconciliation identified a distinct capability/evidence boundary: whether the skill expected for a real user request actually activates and is invoked reliably, rather than merely being selectable after explicit capability requirements are supplied.

### External demand signals

| Signal | Evidence | Interpretation |
|---|---|---|
| Real routing misses | addyosmani/agent-skills issue #620 reports multiple direct task prompts where the owning skills fired 0/6 times, while one description change moved test-driven-development from 0/6 to 6/6 on target prompts with 0/24 adjacent false activations. | Direct evidence of activation reliability and false-activation evaluation demand. |
| Fresh-session variance | NousResearch/hermes-agent issue #82253 reports an identical message loading the expected skill in 2/3 fresh sessions and proposes a repeatable activation harness. | Direct evidence that invocation is probabilistic and needs repeated-run measurement. |
| Evaluation boundary | Hermes #96704 describes skill efficacy/activation as an unmeasured lifecycle boundary and treats activation measurement as a prerequisite to broader efficacy evaluation. | Supports measuring activation before changing skill content or runtime behavior. |
| Routing/collision evaluation | Google skill-reach describes evaluation of skill routing, collision detection, and multi-step trajectory. | Independent ecosystem corroboration that routing/selection needs behavioral evaluation, not only post-invocation tests. |

### Internal coverage reconciliation

Skills Tree already has deterministic capability-based selection, prerequisite routing, failure recovery, observability tracing, and a bounded 9-case selection benchmark. The benchmark begins with explicit `required_capabilities`; it does not measure natural-language trigger reliability, must-not-fire behavior, collision cases, fresh-session variance, or direct evidence that the expected skill was actually invoked.

### Decision

This is classified as an **evaluation/invocation evidence gap**, not a missing raw skill. Issue #357 records the bounded investigation. The next implementation should reuse existing discovery/selection and observability boundaries to build an activation/invocation benchmark. No new search engine, routing authority, or skill should be added unless measured failures prove one is necessary.

Status: **INVESTIGATING — Issue #357**.
Verification date: 2026-10-06.


## Skill Activation / Invocation Evidence — HARNESS IMPLEMENTED — 2026-10-06

Issue #357 has been converted into an executable measurement boundary without adding a raw skill or routing engine.

### Implemented evidence instrument

- Dataset: `benchmarks/activation/skill-activation-v1.json`
- Runner: `tools/run_skill_activation_benchmark.py`
- Tests: `tests/test_skill_activation_benchmark.py`
- Registry benchmark: `benchmark/skill-activation-v1`

The benchmark measures expected-skill activation, forbidden/false activation, collision cases, repeated-run activation variance, and explicit invocation evidence from runtime traces. It requires `skill_selection` and `skill_execution` events and refuses to infer activation from prompt text.

### Evidence status

**IMPLEMENTATION:** VERIFIED ON MAIN — PR #359 merged as `51f22be5d3935437e19561e8aa1fdbf2eb19daab`.

**EMPIRICAL ACTIVATION:** NOT YET VERIFIED. No real agent-runtime trace corpus has been recorded in the repository, so no activation-rate or reliability claim is made. Synthetic test fixtures validate only the evaluator's mechanics.

### Decision boundary

Do not modify skill descriptions, routing behavior, search, or add a new skill based only on external reports. First collect real traces, run the benchmark, and use measured failures as the next decision gate.

Next action: capture repeated fresh-session traces for the four versioned cases and record the resulting benchmark artifact as evidence.

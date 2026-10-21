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

No new retrieval skill, search engine, or popularity claim was created. Current bounded retrieval evidence is now verified by the 12-case deterministic benchmark (Recall@5 1.0000, MRR 0.9583, deterministic replay true). The remaining retrieval-quality boundary is broader representative failure coverage; the measured RAG ambiguity must not trigger ranking changes without that evidence. CAP-007, CAP-011, and CAP-014 evaluation mappings are now verified on main. Issue #335 is historical remediation; Issue #336 is resolved by the reproducible retrieval evidence slice and historical qualification recorded below; no stale model-comparison result is treated as current evidence.

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


## Activation Observation Contract — VERIFIED IMPLEMENTATION — 2026-10-06

The activation/invocation evidence gap now has both a benchmark and a machine-readable observation boundary. `meta/skill-activation-observation.schema.json` defines the accepted external trace shape; the benchmark runner validates against it before calculating metrics.

This is an evidence/interop improvement, not a new skill or routing authority. No empirical activation-rate claim is made until real agent-runtime traces are collected.

Next action: collect repeated fresh-session observations from a compatible runtime and record the benchmark result.
## New evaluation-quality gap — Fail-Closed Benchmark Outcomes — 2026-10-06

Fresh public evidence from anthropics/skills#1383 identifies silent evaluator failure modes where missing or invalid benchmark execution can be interpreted as a valid zero result. Skills Tree's activation runner already labels an empty trace corpus NO_OBSERVATIONS, but previously returned process exit code 0, allowing automation to treat the run as successful.

### Internal reconciliation

The activation benchmark is an evidence instrument, not a model simulator. An empty observation corpus therefore cannot be a successful execution state. Partial observed corpora remain reportable because they can contain useful evidence for selected cases; completeness is a separate contract decision.

### Decision

Classify this as an evaluation-harness integrity gap, not a new skill. The bounded remediation is to fail closed at the process boundary when zero cases have observations, while preserving the existing NO_OBSERVATIONS result record. Do not alter activation metrics or routing behavior.

Status: IN PROGRESS — PR #365.
Verification date: 2026-10-06.
## 2026-10-06 Live project reconciliation

Current implementation/evidence state now includes the semantic Model/Agent/Tool/Capability/Skill boundary, Hermes activation observation adapter and real-trace capture instrumentation, and fail-closed activation benchmarking.

Current corpus baseline verified by CI: 382 canonical skill files; 302 existing Agent Skills packages; no eligible missing projections, deterministic projection drift, stale entries, unexpected packages, or unresolved collisions on the verified PR #368 head.

Activation empirical evidence remains pending. Issue #357 has no real agent-runtime trace corpus. The bounded benchmark now distinguishes NO_OBSERVATIONS, PARTIAL, and COMPLETE; COMPLETE requires 12 observations (4 cases × 3 repetitions).

Evaluation-harness integrity is therefore separated from missing-skill demand: do not add or rewrite skills merely to improve activation before real runtime evidence exists.

Issue #370 is now completed by PR #377: DevLens is diagnostic-only and cannot mutate README.md.
## DevLens governance remediation — 2026-10-06

Issue #370 is resolved by PR #377. The remaining active evidence gaps are #357 (real runtime activation traces) and #336 (retrieval benchmark freshness/reproducibility). Issue #372 is resolved by PR #379.
## Activation observation integrity remediation — 2026-10-06

Issue #372 is resolved by PR #379: the observation universe is closed to the selected dataset and run identities must be unique before metric calculation.
## Final Live Audit State — 2026-10-06

Resolved governance/evidence implementation gaps: #370 (DevLens writer isolation) and #372 (activation observation integrity).

Remaining active evidence work: #357 real runtime activation traces and #336 retrieval benchmark freshness/reproducibility. No raw skill addition is justified by either gap without new measured implementation evidence.

## New demand-gap candidate — Skill Quality Evaluation — 2026-10-11

A fresh owner-directed demand-gap pass (2026-10-11) identified a recurring capability that is not represented by a dedicated canonical skill: **evaluating the quality of a skill or skill package against a reproducible rubric before it is trusted, installed, or published**.

### Demand signals

| Signal | Evidence | Interpretation |
|---|---|---|
| Ecosystem quality variance | The 2026 Agent Skills ecosystem report citing SkillsBench analyzed 47,150 public skills with an average quality score of 6.2/12, and reported that curated skills improved agent pass rates by +16.2 percentage points (https://agentman.ai/blog/agent-skills-ecosystem-report-2026). | Skill quality varies measurably at ecosystem scale; evaluation is a distinct, in-demand capability. |
| Structured skill review demand | fabiandistler/agents#325 (September 2026) reviews 26 skills against Anthropic skill-authoring guidance and the agentskills.io specification, producing 152 findings (https://github.com/fabiandistler/agents/issues/325; specification: https://agentskills.io/home). | Practitioners actively review skill artifacts against explicit quality criteria. |
| Internal coverage gap | Existing 14-security/agent-skill-security-audit covers pre-installation security; no canonical contract was found for a scored, reproducible quality evaluation. | Narrow missing capability; does not duplicate the security audit. |

### Coverage reconciliation

Existing Skills Tree coverage includes security auditing, evidence verification, critic agents, and capability-based selection. Those skills are necessary building blocks, but none provides one canonical contract for scoring a skill artifact against named quality dimensions - description fidelity, instruction actionability, runnable-example validity, failure-mode coverage, and evidence strength - with an explicit verdict.

### Selected migration

skills/09-agentic-patterns/skill-quality-evaluation.md

Status: **SELECTED / implementation in progress** on branch feat/demand-gap-skills-20261011 (issue #466).

### Priority assessment

**Proposed tier: A — high strategic utility, evidence-backed gap.**

Rationale: the capability extends Skills Tree's quality-gate differentiator from CI enforcement into a reusable agent-facing contract, and the demand signals are dated and public. No popularity or adoption claim is made.

Verification date: 2026-10-11.


## New demand-gap candidate — Progressive Skill Loading — 2026-10-11

The same pass identified a second capability gap: **loading skills into an agent context in escalating tiers so that a large skill library costs a bounded, measured number of tokens**.

### Demand signals

| Signal | Evidence | Interpretation |
|---|---|---|
| Skill-layer token cost | anthropics/claude-code#75376 reports that carrying roughly 30-40 skills can consume on the order of 800-1,200 tokens per turn and requests explicit visibility tiers (https://github.com/anthropics/claude-code/issues/75376). | Direct runtime evidence that unbounded skill loading is a measured cost concern. |
| Progressive disclosure guidance | Microsoft Agent Framework skill documentation directs skills to stay under 5,000 tokens and describes progressive disclosure of skill content (https://learn.microsoft.com/en-us/agent-framework/agents/skills). | Cross-runtime corroboration that tiered skill loading is an expected capability. |
| Lifecycle survey | A 2026 agent-skills lifecycle survey describes token-budget-aware skill loading as a recurring lifecycle concern (https://redreamality.com/blog/agent-skills-2026-survey-lifecycle-map/). | Corroborating signal; not adoption data. |
| Internal coverage gap | 03-memory/context-compaction compacts conversation history; no canonical contract was found for tiered loading of the skill layer itself under a token budget. | Narrow missing capability; does not duplicate compaction. |

### Coverage reconciliation

Existing Skills Tree coverage includes context compaction, working memory, budget management, and capability-based selection. None bounds the token cost of the skill layer specifically: metadata-tier loading, measured escalation, and budget-fail-closed behavior for skills are not covered by an existing contract.

### Selected migration

skills/03-memory/progressive-skill-loading.md

Status: **SELECTED / implementation in progress** on branch feat/demand-gap-skills-20261011 (issue #466).

### Priority assessment

**Proposed tier: B — clear utility, evidence-backed gap, narrower blast radius than tier A.**

Rationale: the demand signals are dated and public, but the capability is a runtime-performance contract whose empirical benefit for Skills Tree itself awaits measured use; the skill records that boundary honestly. No popularity or adoption claim is made.

Verification date: 2026-10-11.

## Owner-directed expansion note — 2026-10-12

The 2026-10-12 corpus expansion (100 new skills across all 17 categories, beginning with the 10-skill pilot in PR #480) is an owner-directed addition, not a demand-gap selection. No demand signal is claimed for these entries, and they do not appear in the tiered selection lists above. The override of the measured-gap rule and the execution constraints are recorded in `meta/memory/DECISIONS.md` under DECISION-2026-10-12-OWNER-DIRECTED-CORPUS-EXPANSION. Batch 2 (45 experimental skills across 08-multimodal, 10-computer-use, 11-web, 13-creative, 14-security, 15-orchestration, 16-domain-specific, and 17-infrastructure) lands in PR #487 under the same constraints; the discovery test count moves 286 to 331. Batch 3 (45 experimental skills across 01-perception, 02-reasoning, 03-memory, 04-action-execution, 05-code, 06-communication, 07-tool-use, 09-agentic-patterns, 12-data, and 17-infrastructure) lands in PR #491 under the same constraints and completes the 100-skill expansion; the discovery test count moves 331 to 376. No demand signal is claimed.


## Owner-directed expansion note - 2026-10-12 (wave 2)

A second owner-directed 100-skill expansion (wave 2) was directed on 2026-10-12, under the same constraints as the wave-1 override recorded above: an explicit owner override of the measured-gap rule, no fabricated demand signal, and experimental v1 entries with full section structure and byte-exact deterministic `project()` packages. Wave-2 batch 1 (10 experimental skills across 01-perception through 10-computer-use) lands in PR #506; the discovery test count moves 376 to 386. Wave-2 batch 2 (45 experimental skills across 11-web, 12-data, 13-creative, 14-security, 15-orchestration, 16-domain-specific, and 17-infrastructure) lands in PR #514 under the same constraints; the discovery test count moves 386 to 431. These entries do not appear in the tiered selection lists above, and no demand signal is claimed for them.


## Daily demand-driven expansion — 2026-10-12 (run batch 1)

Batch 1 of the owner-directed daily skill-expansion run (DECISION-2026-10-12-DAILY-DEMAND-DRIVEN-SKILL-EXPANSION) adds 50 experimental v1 skills across categories 01-perception through 05-code, published through the standard batch PR with full CI and an exact-head squash-merge. Selection basis for this batch: dated 2026-10 public signals — the MCP 2026-07-28 specification release candidate (stateless core, Extensions framework, Tasks, MCP Apps, authorization hardening), A2A agent-to-agent interop across trust boundaries, recurring developer pain points around agent evaluation, runaway agent spend, and agent security, plus the configured GitHub issue-search demand queries from meta/demand-sources.json (including open issue #357 and repository issue #87 on hierarchical memory). These are demand signals, not adoption metrics; no popularity or adoption claim is made. The public corpus moves from 538 to 588 skills.


## Daily demand-driven expansion — 2026-10-12 (run batch 2)

Batch 2 of the owner-directed daily skill-expansion run adds 50 experimental v1 skills across categories 05-code (completion), 06-communication, 07-tool-use, 08-multimodal, and 09-agentic-patterns (first 4), published through the standard batch PR with full CI and an exact-head squash-merge; the discovery test count moves 481 to 531 and the public corpus 588 to 638. Selection basis for this batch: dated 2026-10 public signals — the MCP 2026-07-28 specification release candidate (Extensions framework, Tasks, MCP Apps), A2A agent-card and trust-boundary interop work, agent evaluation as the top reported developer pain point, agent cost control (measured skill-layer token cost reports), agent supply-chain security (MCP tool poisoning, rug-pull attacks), content-provenance and deepfake concerns, plus the configured GitHub issue-search demand queries from meta/demand-sources.json. These are demand signals, not adoption metrics; no popularity or adoption claim is made.

## Daily demand-driven expansion — 2026-10-12 (run batch 3)

Batch 3 of the owner-directed daily skill-expansion run adds 50 experimental v1 skills across categories 09-agentic-patterns (completion), 10-computer-use, 11-web, 12-data, and 13-creative (first 6), published through the standard batch PR with full CI and an exact-head squash-merge; the discovery test count moves 531 to 581 and the public corpus 638 to 688. Selection basis for this batch: dated 2026-10 public signals — the MCP 2026-07-28 specification release candidate and its Tasks and Extensions surface, A2A protocol-compliance work across trust boundaries, agent evaluation and halt-condition design as recurring developer pain points, agent cost accounting and runaway-spend control, prompt version control, reward-hacking concerns in agentic evaluation, computer-use and browser-automation demand (session isolation, OAuth flows, accessibility auditing, link-rot and bulk URL health checking, session replay, CORS review), data-platform requests (data quality scoring, PII discovery, warehouse cost attribution, CDC, pipeline observability, vector index tuning, chunking strategy), and creative/content requests (interactive fiction, icon sets, newsletters, brand guidelines, alt text). Plus the configured GitHub issue-search demand queries from meta/demand-sources.json. These are demand signals, not adoption metrics; no popularity or adoption claim is made.

## Daily demand-driven expansion — 2026-10-12 (run batch 4)

Batch 4 of the owner-directed daily skill-expansion run adds 50 experimental v1 skills across categories 13-creative (completion), 14-security, 15-orchestration, 16-domain-specific, and 17-infrastructure, published through the standard batch PR with full CI and an exact-head squash-merge; the discovery test count moves 581 to 631 and the public corpus 688 to 738, completing the 200-skill daily target. Selection basis for this batch: dated 2026-10 public signals — agent supply-chain security (MCP tool poisoning and rug-pull attacks, SBOM review for agent deployments, model provenance), indirect prompt injection as the most reported agent attack vector, agent identity verification and exfiltration detection, red teaming and attack-surface mapping, multi-tenant isolation; orchestration demand (hard cost ceilings against runaway spend, chaos testing, SLO enforcement, staged fleet config rollout, canary agent deployment, durable execution guarantees, A2A/MCP protocol bridging, human escalation routing); domain requests (clinical trial protocol review, patent claim drafting, procurement comparison, HR policy drafting, support KB curation, ecommerce categorization, real-estate listing analysis, regulatory change monitoring, supply-chain visibility, loan underwriting, pharmacovigilance signal detection, ESG reporting); and infrastructure requests (GPU scheduling, inference autoscaling, observability configuration, IaC drift detection, DR drills, certificate expiry, serverless cold starts, connection pool tuning, runbook generation, multi-cloud failover, image slimming, queue provisioning). Plus the configured GitHub issue-search demand queries from meta/demand-sources.json. These are demand signals, not adoption metrics; no popularity or adoption claim is made.

## Daily demand-driven expansion — 2026-10-13 (run batch 1)

Batch 1 of the owner-directed daily skill-expansion run (DECISION-2026-10-12-DAILY-DEMAND-DRIVEN-SKILL-EXPANSION) adds 50 experimental v1 skills across categories 01-perception, 02-reasoning, 03-memory, and 04-action-execution, published through the standard batch PR with full CI and an exact-head squash-merge; the discovery test count moves 711 to 761 and the public corpus 738 to 788. Selection basis for this batch: dated 2026 public signals — the MCP 2026-07-28 specification (Streamable HTTP and server-sent events, the 2026-09-15 tool-list pinning client revision), A2A 1.0 signed Agent Cards and gRPC or JSON bindings (2026-03-12), streamed model and tool API responses, silent long-term-memory poisoning demonstrated against managed agent platforms, cryptographic continuity across agent restarts, memory governance including hierarchical memory management, forgetting and eviction from repository issue #87, deadline-aware and budget-aware reasoning, verifiability-first planning for long-horizon agents, agent payment mandates with cryptographic accountability, rate-limit and quota compliance, least-privilege action hygiene, and durable execution recovery guarantees, plus the configured GitHub issue-search demand queries from meta/demand-sources.json (including open issue #357 on skill activation reliability). These are demand signals, not adoption metrics; no popularity or adoption claim is made.

## Daily demand-driven expansion — 2026-10-13 (run batch 2)

Batch 2 of the owner-directed daily skill-expansion run (DECISION-2026-10-12-DAILY-DEMAND-DRIVEN-SKILL-EXPANSION) adds 50 experimental v1 skills across categories 05-code, 06-communication, 07-tool-use, and 08-multimodal, published through the standard batch PR with full CI; the discovery test count moves 761 to 811 and the public corpus 788 to 838. Selection basis for this batch: dated 2026 public signals — the MCP 2026-07-28 specification update and the 2026-09-15 tool-list pinning client revision, A2A 1.0 signed Agent Cards (2026-03-12) and ACP editor-protocol releases, coding-agent git configuration hijack disclosure in 2026 agent security coverage, CI cost and cache efficiency requests, prompt-as-code regression testing, small-model routing for inference cost reduction, MCP registry curation and WebMCP page tool exposure, and recurring multimodal requests (video tracking, audio event and highlight extraction, subject-consistent image generation, dubbing alignment), plus the configured GitHub issue-search demand queries from meta/demand-sources.json. These are demand signals, not adoption metrics; no popularity or adoption claim is made.

## Daily demand-driven expansion — 2026-10-13 (run batch 3)

Batch 3 of the owner-directed daily skill-expansion run (DECISION-2026-10-12-DAILY-DEMAND-DRIVEN-SKILL-EXPANSION) adds 50 experimental v1 skills across categories 09-agentic-patterns, 10-computer-use, 11-web, and 12-data, published through the standard batch PR with full CI; the discovery test count moves 811 to 861 and the public corpus 838 to 888. Selection basis for this batch: dated 2026 public signals — context engineering and context-window budgeting, LLM-as-judge calibration and simulated-user evaluation, eval regression gates and plan-adherence auditing for CI-for-agents, definition-of-done enforcement in spec-driven workflows, commitment tracking and turn-budget pacing for long-horizon runs, stuck-loop detection in agent observability, approach diversification and skill composition requests; computer-use requests (remote desktop, mobile and ADB device automation, drawing canvas, e-signature, system tray, permission dialogs, hotkey conflicts, app updates, VPN, scheduled tasks, session keepalive); web requests (llms.txt, agent-readable site markup alongside the MCP 2026-07-28 specification, bot authentication, browser fingerprint management, network interception, cookie consent, API mocking, signed URLs, verification links, localization verification, multi-tab flows, extensions, checkout, MFA); and data requests (AI-traffic classification, dialogue analytics, embedding cost tracking, Parquet processing, lakehouse maintenance, event-sourced projections, graph centrality, inter-annotator agreement, retention automation, metrics cardinality), plus the configured GitHub issue-search demand queries from meta/demand-sources.json. These are demand signals, not adoption metrics; no popularity or adoption claim is made.

## 2026-10-14 daily expansion — batch 1

Added 50 canonical skills selected from dated public signals gathered 2026-10-14: MCP 2026-07-28 specification (stateless, self-contained requests), A2A v1.0 task lifecycle states, Microsoft Agent Framework 1.0 GA (2026-04-03), agentic-commerce protocols (AP2 signed mandates, UCP, ACP, x402), context-engineering and harness-engineering practitioner surveys, production agent guardrail compliance guides, and agent evaluation practice (SWE-bench Pro, Terminal-Bench, eval dataset curation). Sources are public web search results recorded per skill in the PR body. No popularity ranking is claimed.

## 2026-10-15 daily expansion - batch 2

Added 50 experimental v1 canonical skills selected from dated public trend signals gathered 2026-10-15, published through the standard batch PR (skills/expansion-2026-10-15-b2) with full CI; the discovery test count moves 912 to 962 and the public corpus 939 to 989. Selection basis for this batch: agent-memory systems practice (memory store migration, memory deletion compliance, forgetting-curve scheduling, temporal memory anchoring, multi-agent memory merge coordination, PII memory minimization, memory key design, memory benchmark evaluation, long-term goal state tracking, cross-session identity resolution), typed agent frameworks and reasoning requests (Pydantic-AI-v2-style typed tool composition, assumption explicitness, claim-evidence alignment, dependency-cycle resolution, freshness-aware reasoning, model selection, refusal and rollback decision reasoning, multi-agent consensus, trust-boundary and unit-consistency reasoning, blast-radius estimation), the MCP 2026-07-28 stateless revision and gateway/deployment patterns (device authorization flows, hardware-token signing actions, webhook and calendar recurrence rule parsing, SARIF/PDF/image-metadata/audio-stream payload parsing, offline action queueing, human presence verification, micropayment batching, shell environment sanitization), and agent observability, evals, and developer-tooling security (agent trace span parsing, LLM confidence signal and usage metrics extraction, flaky-test quarantine, build reproducibility verification, CI cache poisoning prevention, unicode homoglyph detection, embedded prompt extraction, actionable error message implementation, agent commit hygiene, spec-driven implementation planning, polyglot type binding generation, documentation example testing, static analysis suppression auditing, recurring calendar event creation, database transaction isolation selection, action ledger hash chaining), plus the configured GitHub issue-search demand queries from meta/demand-sources.json. Sources are public web search results recorded per skill in the PR body. These are demand signals, not adoption metrics; no popularity or adoption claim is made.

## 2026-10-15 daily expansion - batch 3

Added 50 experimental v1 canonical skills selected from dated public trend signals gathered 2026-10-15, published through the standard batch PR (skills/expansion-2026-10-15-b3) with full CI; the discovery test count moves 962 to 1012 and the public corpus 989 to 1039. Selection basis for this batch: MCP ecosystem operational practice (tool-argument validation, server rate-limit backoff, OpenAPI-to-MCP tool bridging), A2A skill-declaration mapping across trust boundaries, agentic pattern requests (checkpoint/restore patterns, guardrail-wrapped agent loops, self-refine critique loops, agent memory compaction tiers, idle wakeup scheduling, multi-agent debate resolution and workstream merging), computer-use demand (accessibility-tree automation audits, sandboxed desktop VM execution, screenshot-diff verification, GUI element anchoring stability, install-wizard automation), web requests (SPA URL state snapshotting, crawl-budget allocation, JSON-LD structured-data extraction, shadow-DOM selector strategies, browser session state snapshots), data requests (vector-store schema migration, dataset contamination screening, RAG chunk boundary audits, observability span taxonomies, session replay sampling, trace cost attribution), and communication requests (agent handoff brief composition, cross-agent session continuity, conversational repair after tool failure, tool-description writing), plus the configured GitHub issue-search demand queries from meta/demand-sources.json. Sources are public web search results recorded per skill in the PR body. These are demand signals, not adoption metrics; no popularity or adoption claim is made.


## Expansion-batch content-quality contract (2026-10-18)

Codified from the Counsel slice-2 advisory findings B1–B5 (issue #617, triage comment of 2026-10-18). This contract governs all future daily-expansion batches (and is recommended for any new-skill PR). It applies to newly added skills only; no forced mass rewrite of the existing corpus (consistent with DECISION-2026-10-18-COUNSEL-SLICE2-CONVENTIONS, D-B4).

1. **Topic-relevant runnable examples (B1, B5).** A skill's `## Runnable Example` must exercise the subject matter of that skill. Shared template mechanics (generic budget guards, candidate/conflict loops) may appear only when the skill's topic is that mechanic. Examples must be deterministic and runnable without external API keys or network access; an example that genuinely requires an external dependency must say so explicitly and degrade to a no-key dry-run path.
2. **Topic-specific procedure and failure modes (B2).** `## Procedure` steps and `## Failure Modes` bullets must describe the skill's actual subject, not shared boilerplate. Evidence boilerplate ("These are dated public signals…") belongs only where the section genuinely reports demand signals; elsewhere Evidence must cite the concrete sources it relies on, or state the absence honestly.
3. **Changelog required (B3).** Every newly added skill must include a `## Changelog` section with at least the initial-entry line (version, date).
4. **Metadata completeness.** Frontmatter must carry the canonical key set (title/category/level/stability/description/added/version/related/tags) per the slice-2 conventions; `tags` are title-derived with stopwords dropped; `related` entries must resolve to real skills under the explicit-path convention.
5. **Batch gate.** Batch PR descriptions should record, per batch, that these five requirements were checked per file. A future freshness-contract test may codify parts of this mechanically; until then it is a review-time contract.

This contract does not weaken or replace any existing CI, quality, security, or governance gate.

## Expansion Note - 2026-10-18 (Expansion batch 1: 50 skills)

Selection basis for expansion batch 1 of 2026-10-18: dated October-2026 public ecosystem signals — Microsoft Agent Framework updates (developersdigest.tech), 2026 framework landscape covering Pydantic AI v1 and LangGraph 1.0 (alicelabs.ai), OpenAI Agents SDK and Google ADK integration patterns (vdf.ai), MCP 2026-10 revision elicitation, async tasks, multi round-trip requests, and deprecation policy (medium.com/@bitcot.insider and carmatec.com), agent memory benchmarks and the state-of-agent-memory review (mem0.ai), long-horizon context assembly research (arxiv.org 2606.06448), agentic identity and gateway enforcement (twilio.com), agent IAM grant-matches-task guidance (sweet.security), delegation chain and token patterns for agent skills security (github.com/LLMSecurity), machine identity scale for agents (iternal.ai), model card safety and autonomy thresholds (aitechmodel.com), agentic browser sessions, engine limits, and cloud provisioning (browser-use.com, github.com/vercel-labs/agent-browser, nohacks.co, techiehub.blog), desktop GUI agents and UI-TARS and OSWorld test grids (dev.to/agdex_ai), and collaboration-space agent frameworks (aiagentstore.ai). No popularity ranking is claimed; these are dated signals recorded under the signal policy above.

### Expansion note (2026-10-18, batch 2)
Delivered 50 further skills selected from fresh ecosystem signals gathered this session: agent-observability and telemetry-convention tooling (Arize, Braintrust, Confident AI), the 2026-07-28 MCP specification and registry roadmap (modelcontextprotocol.io), agent memory and context-engineering practice (mem0 State of AI Agent Memory, context-engineering guides), agentic security reporting on prompt injection, policy testing, and egress control (OWASP/Help Net Security, Stellar Cyber, Gravitee), coding-agent workflow requests (Morphllm, CodePick, Checkmarx developer-tool roundups, GitHub community discussion), and framework evolution coverage (LangChain, vdf.ai, developersdigest). Duplicates of all 1089 existing skills were excluded before selection; category spread covers all 17 directories.


## Expansion note — 2026-10-18, batch 3

50 new skills selected from dated October-2026 demand signals: OWASP Top 10 for Agentic Applications 2026 (genai.owasp.org), the CSA research notes on the NIST AI agent standards initiative (labs.cloudsecurityalliance.org), the OWASP Agentic Security Initiative, protocol ecosystem maps covering MCP, A2A, ACP, UCP, and ANP convergence (zylos.ai, atlan.com, digitalapplied.com, arxiv.org survey 2505.02279), the ARD Agent Requirements Document specification (metirai.com), context-engineering practice including context rot and episodic reuse (anthropic.com/engineering, sourcegraph.com, cruxdigits.nl), the Datadog State of AI Engineering report, October-2026 agentic-security state reporting (rockcybermusings.com), 2026 agent security checklists (iternal.ai, forcepoint.com, buildmvpfast.com), October-2026 AI news coverage of AI-authorship disputes, AI-assisted pricing litigation, AI robocall rulemaking, minors-protection litigation, export-control announcements, and provider-termination events (aiagentstore.ai weekly news), October-2026 framework analyses (developersdigest.tech, shakudo.io, zyneto.com, vdf.ai). Corpus 1139 to 1189 public skills. Sources are dated public signals, not adoption metrics; per-skill selection bases are recorded in the expansion batch 3 PR body.

## Expansion note — 2026-10-19, batch 4

50 new skills selected from dated October-2026 demand signals, completing the 2026-10-18 daily expansion run (merged 2026-10-19 UTC): persistent-agent and 24/7 agent operations coverage (aiagentstore.ai weekly news; Google Gemini at Work 2026, cloud.google.com), agentic AI security best practices including egress control and session lockdown (forcepoint.com), agent evaluation practice (anthropic.com/engineering demystifying evals for AI agents; DeepEval, docs.confident-ai.com), the MCP specification including JSON-RPC batch usage (modelcontextprotocol.io 2025-06-18), the A2A protocol and its multi-agent governance survey (a2a-protocol.org; arxiv.org 2505.02279), Microsoft Agent Framework / Semantic Kernel scheduling surfaces (learn.microsoft.com), agent memory research (mem0.ai/research), x402 agentic-commerce payment practice, voice-agent safety and compliance reporting, and multiday-session continuity patterns. Corpus 1189 to 1239 public skills. Sources are dated public signals, not adoption metrics; per-skill selection bases are recorded in the expansion batch 4 PR body.

## Expansion note - 2026-10-19, batch 1

50 new skills selected from dated October-2026 demand signals: the 2026 agent protocol stack listing AG-UI and AP2 among active agent protocols (peterindia.net, ruh.ai), agent protocol convergence guides (atlan.com), the State of AI Agent Memory 2026 (mem0.ai), agent observability tracing and evaluation practice (futransolutions.com), the state-of-agents reliability analysis for October 2026 (brandon-ta.com), the industrial AI stack formation report (iot-analytics.com), the AI CLI tools digest of 2026-10-16 (github.com/duanyytop/agents-radar), and the agentic-commerce and compliance weekly coverage (aiagentstore.ai). Corpus 1239 to 1289 public skills. Sources are dated public signals, not adoption metrics; per-skill selection bases are recorded in the expansion batch 1 PR body.

## Expansion note - 2026-10-19, batch 2

50 new skills selected from dated October-2026 demand signals, continuing the 2026-10-19 daily expansion run: the industrial AI stack formation report naming OPC UA a core telemetry layer (iot-analytics.com), the State of AI Agent Memory 2026 and memory-operations practice (mem0.ai), agent protocol and MCP/A2A protocol practice guides (ruh.ai, peterindia.net, modelcontextprotocol.io, a2a-protocol.org), agent observability and evaluation practice (futransolutions.com), the state-of-agents reliability analysis for October 2026 (brandon-ta.com), the AI CLI tools digest of 2026-10-16 and its configuration-authoring requests (github.com/duanyytop/agents-radar), and the agentic-commerce, office-automation, and recruiting-agent weekly coverage (aiagentstore.ai). Corpus 1289 to 1339 public skills. Sources are dated public signals, not adoption metrics; per-skill selection bases are recorded in the expansion batch 2 PR body.

## Expansion note — 2026-10-20, batch 1

50 new skills selected from dated October-2026 demand signals, opening the 2026-10-20 daily expansion run: Sierra's Personal Agent Protocol for personal-agent handshake and permissions (sierra.ai), Meta Connect 2026 smart-glasses agent interfaces (theverge.com), the NVIDIA Vera CPU launch for agentic single-thread performance (nvidianews.nvidia.com, developer.nvidia.com), NSA/CISA/NIST rogue-agent guidance, India CERT-In's first agent attack-surface advisory, and NIST/NSA/CISA agent-evidence guidance (cybersecuritynews.com, forkast.news, complexdiscovery.com), context-engineering practice covering compaction, cache preservation, and record-graph memory (louisbouchard.ai, platform.claude.com, redis.io), per-task credential injection and egress policy practice (agentgateway.dev, opsinsecurity.com), exposed-MCP-server security reporting (darkreading.com), fleet AI dash-cam operations and incident evidence practice (gomotive.com), legal-practice agent adoption (harvey.ai, unite.ai), governed-AI management for SMBs (theaiinsider.tech), A2A protocol practice (omidsaffari.com, thenextweb.com), long-running agent harnesses (notion.com), and Anthropic Claude Opus 5.5 release coverage (anthropic.com). Corpus 1339 to 1389 public skills. Sources are dated public signals, not adoption metrics; per-skill selection bases are recorded in the expansion batch 1 PR body.

## Expansion batch 2 of the 2026-10-20 run — 2026-10-20

Batch 2 of the 2026-10-20 daily demand-driven expansion (50 skills, PR #647) was selected from fresh October-2026 public signals gathered via web search: MCP OAuth token-redirect theft advisories (dev.to, safeguard.sh, Ars Technica — CVE-2026-104850/RMCP), American Express Intent Intelligence (Digital Commerce 360, Oct 16), NSA/CISA/NIST rogue-agent guidance (cryptika, Oct 16), the Deadbugz delayed-payload supply-chain campaign (adversa.ai), OpenAI ChatGPT Chrome tab controls (unite.ai, Oct 15), Google persistent Gemini agents with dedicated Gmail/Calendar/Drive storage (VentureBeat, Google Cloud blog), the Webex agentic meeting framework, Rocket-Geniez mainframe agents, Meta Muse active-memory recall, and an agentic-maturity survey (aiagentstore.ai weekly roundup), the DeepSeek Harness plugin runtime (dreaming.press), and browser-agent infrastructure with CDP session-log export (mastra.ai). Duplicates and near-duplicates of existing corpus capabilities were excluded; each skill records its dated signal in its Evidence section. These are demand signals, not adoption metrics.


## Expansion batch 1 of the 2026-10-21 run — 2026-10-21

Batch 1 of the 2026-10-21 daily demand-driven expansion (50 skills, PR #649) was selected from fresh October-2026 public signals gathered via web search: the MCP 2026-07-28 stateless spec update and gateway support (AWS AgentCore Gateway blog, Google Developers Blog), Azure MCP Server 3.0 cloud-operations tools (Visual Studio Magazine, Oct 20), OpenAI DevDay 2026 (openai.com, InfoQ, Oct 1–2), the Google Cloud Gemini at Work universal enterprise agent (cloud.google.com / MarkTechPost, Oct 8), NSA/CISA/NIST rogue-agent and AI agent incident-response guidance (cybersecuritynews.com Oct 19, windowsforum.com Oct 16), Five Eyes careful-adoption guidance (aigovernance.com), the OWASP Top 10 for Agentic Applications, Agent Control Standard, and GenAI Red Teaming Manual v1.0 (genai.owasp.org, Sep 1 / Oct 20), October 2026 model launches including GPT-6 Intelligent UI and Mistral Large 4 (gadgetsfocus.com, thepromptbuddy.com), the agentic payment protocol landscape x402/AP2/ACP/MPP/UCP (protofire.io, fireblocks.com, agenticcommerceatlas.com, reactify-solutions.com), SWE-Bench Pro V2 (arxiv.org 2610.24206, Oct 16) and October coding leaderboards (benchlm.ai), and Grafana ObservabilityCON 2026 agent observability with watchers and pages (grafana.com, Oct 20; newrelic.com, Oct 5). Duplicates and near-duplicates of the existing 1439-skill corpus were excluded; each skill records its dated signal in its Evidence section. These are demand signals, not adoption metrics.

## Expansion batch 2 of the 2026-10-21 run — 2026-10-21

Batch 2 of the 2026-10-21 daily demand-driven expansion (50 skills, PR #651) was selected from fresh September-October 2026 public signals gathered via web search: Microsoft Agent Framework 1.0 GA, its agent harness, and the interactive-experiences/memory/resilient-execution post (devblogs.microsoft.com, Apr 8 / Jul 23 / Sep 22, 2026), A2A joining the Agentic AI Foundation (aaif.io, Aug 17; a2a-protocol.org, Aug 27), the Azure MCP Server 3.0 stable release (devblogs.microsoft.com, Oct 8), Splunk AI agent monitoring in Splunk Observability Cloud (splunk.com, Jun 3), the x402/AP2/ACP/MPP agent payment landscape (patechlabs.com, Oct 9; pondero.ai, Oct 7; roundhouseai.io, Oct 2026), Microsoft Security's agents-as-newest-insiders guidance (microsoft.com, Oct 19), Databricks agent memory (databricks.com, 2026), Cohere North 2 with redesigned agent harness and memory (unite.ai, Oct 5), OpenAI computer use in Chrome with ChatGPT tab controls (unite.ai, Oct 15), and the October 2026 LangChain newsletter (langchain.com, Oct 15). Duplicates and near-duplicates of the 1489-skill corpus, including every batch-1 (PR #649) slug and theme, were excluded; each skill records its dated signal in its Evidence section. These are demand signals, not adoption metrics.

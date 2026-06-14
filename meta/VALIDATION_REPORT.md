# Skills Tree — Validation Report

## Executive Summary

Wave 0 created a real strategic pivot, but the project is now operating with **two competing truths**. The repository’s foundational documents still describe Skills Tree as a content-heavy catalog and roadmap-driven upgrade machine, while the new strategic documents reframe it as an **AI Engineering Operating System** centered on **Agent Skill Architect** as the flagship product surface.[page:35][page:2][page:6][page:7]

That means the pivot is directionally strong but **not yet validated through planning alignment**. `README.md` already presents the project as “an AI Engineering Operating System,” while `PROJECT_MEMORY.md` still gives content scale, contributor growth, and catalog completion much more weight than product orchestration.[page:2][page:3] `ROADMAP_V2.md` still prioritizes stub upgrades as the highest-value move, while `CHATGPT_DECISION.md` explicitly demotes content-first execution and promotes Agent Skill Architect, CLI, MCP, semantic search, and framework guidance ahead of bulk content work.[page:4][page:7]

The validation result is therefore clear: **the strategic pivot is not fully absorbed into the execution system**. The project now needs a roadmap and dependency rewrite around a new critical path: structured data hardening → architect-ready recommendation layer → flagship MVP → distribution surfaces → content acceleration in support of architect outputs.[page:4][page:6][page:7]

---

## Conflicts

### 1. Product identity conflict

`README.md` says Skills Tree “maps, validates, composes, and operationalizes” AI capabilities, which is a product-platform framing rather than a repository framing.[page:2] By contrast, `PROJECT_MEMORY.md` still defines the mission mainly as a comprehensive, versioned, community-powered index of AI agent capabilities, with growth targets emphasizing 1,000+ skills, 50+ contributors, and broad content coverage.[page:3]

**Conflict:** the public homepage already promises an operating system, but the internal memory system still optimizes for catalog expansion as the dominant value engine.[page:2][page:3]

### 2. Roadmap objective conflict

`ROADMAP_V2.md` says the next immediate action is **T-04 Stub Upgrade Wave 1**, and calls it the highest priority in the entire project because “the catalog is the product.”[page:4] `CHATGPT_DECISION.md` directly contradicts this and says the catalog should no longer be treated as the primary priority surface; instead, Agent Skill Architect becomes Wave 1 and content expansion falls to Wave 5.[page:7]

**Conflict:** one document says “fix the top 50 stubs first,” while the newer strategy says “build the architect first and let tools unlock more leverage than content.”[page:4][page:7]

### 3. Architecture direction conflict

`AGENT_SKILL_ARCHITECT_MVP.md` proposes a Next.js/React product in `tools/architect/` with a visual selector, architecture canvas, validation engine, and export system.[page:6] `ROADMAP_V2.md`, however, continues to assume the main product arc is static-site evolution on top of GitHub Pages plus CLI, paths, benchmarks, and content upgrade waves.[page:4]

**Conflict:** the architect MVP introduces a new application surface and likely a new frontend architecture, but `ROADMAP_V2.md` does not contain the prerequisite planning tasks needed to safely support that architectural branch.[page:4][page:6]

### 4. Scope conflict: validator vs builder

`REALITY_AUDIT.md` is correct that API, graph, search, paths UI, and release foundations already exist, which made content quality look like the logical next local optimization.[page:5] But the new vision documents argue that those same completed foundations are exactly what make a product leap possible now, meaning they should feed a recommendation system rather than justify more content-first backlog sequencing.[page:6][page:7]

**Conflict:** the same evidence supports two different strategies, and the current roadmap chose the conservative one.[page:4][page:5][page:7]

### 5. MVP definition conflict

`AGENT_SKILL_ARCHITECT_MVP.md` defines an MVP around browsing, selecting, composing, validating, and exporting architectures.[page:6] `CHATGPT_DECISION.md` then elevates that MVP to the next sprint, but `ROADMAP_V2.md` has no architect-specific milestone, scoring model, or prerequisite data tasks for recommendation quality.[page:4][page:7]

**Conflict:** the product MVP exists as a specification, but not as an execution-ready roadmap item.[page:4][page:6][page:7]

---

## Roadmap Drift

These tasks still make sense in the abstract but no longer make sense at their current priority, framing, or dependency position.

| Task | Current status in ROADMAP_V2 | Drift assessment | Why it drifted |
|---|---|---|---|
| T-04 Stub Upgrade Wave 1 | Wave 1, highest priority | **Drifted** | Still valuable, but no longer the first move if the flagship strategy is Agent Skill Architect.[page:4][page:7] |
| T-05 Stub Upgrade Wave 2 | Wave 2 | **Drifted** | Should support recommendation quality later, not dominate early execution.[page:4][page:7] |
| T-06 Stub Upgrade Wave 3 | Wave 5 | **Drifted** | Full catalog completion is no longer the best global optimization path.[page:4][page:7] |
| T-14 Benchmark Expansion | Wave 2 | **Partially drifted** | Still strategically strong, but should be reframed as evidence infrastructure for architect trust scoring.[page:4][page:6] |
| T-08 Populate `paths/` | Wave 4 | **Drifted upward** | Learning paths become much more important because Agent Skill Architect outputs need a guided execution sequence.[page:4][page:6] |
| T-19 CLI Scaffold + PyPI | Wave 3 | **Drifted upward** | The tool-first vision makes programmatic access core, not secondary.[page:4][page:7] |
| T-24 MCP Registry Listing | Wave 3 | **Drifted upward** | Distribution becomes part of product activation for the OS vision.[page:4][page:7] |
| T-23 LangChain Hub Submission | Wave 3 | **Drifted upward** | Framework embedding is more important under the OS strategy.[page:4][page:7] |
| T-25 Semantic Search Embeddings | Wave 6 | **Drifted sharply upward** | Natural-language discovery is architect-critical, not late-stage polish.[page:4][page:7] |
| T-10 Mobile Responsive UI | Wave 7 | **Partially drifted** | Important for reach, but not on the architect critical path.[page:4] |
| T-22 Skill Champion Field | Wave 7 | **Drifted downward** | Governance metadata does not unlock architect-mode value soon enough.[page:4] |

### Tasks that no longer make sense in their current form

- **T-07 Model Comparison AST Sweep** is not obsolete, but its current framing is too narrow. Model tables should become a **ranking input** and **trust signal** for architecture recommendations, not just a bulk content enrichment pass.[page:4][page:6]
- **T-06 Full stub completion** is too locally optimal. It assumes full-catalog completeness is the best path to differentiation, but the new strategy says differentiation comes from orchestration and planning intelligence first.[page:4][page:7]

---

## Missing Tasks

`ROADMAP_V2.md` does not currently contain the tasks required to deliver Agent Skill Architect as an execution-grade product, even though the MVP and strategic decision docs clearly establish it as the new flagship direction.[page:4][page:6][page:7]

### Missing critical tasks

| New ID | Task | Why it is required |
|---|---|---|
| N-01 | **Architect Data Contract Audit** | The architect needs trustworthy structured inputs across schema, frameworks, graph, paths, and benchmarks before recommendation quality can be credible.[page:3][page:6] |
| N-02 | **Goal / Use-Case Taxonomy** | User input must normalize goals such as research agent, code agent, browser agent, RAG assistant, eval harness, and workflow automation.[page:6] |
| N-03 | **Recommendation Engine Spec** | There is no current roadmap item defining how skills are selected, weighted, grouped, or substituted for architecture generation.[page:6] |
| N-04 | **Graph Query + Dependency Logic Spec** | The graph exists, but the roadmap does not define architect-mode graph operations such as prerequisite expansion, substitutes, bundle extraction, or conflict detection.[page:5][page:6] |
| N-05 | **Architecture Output Schema** | JSON blueprint, dependency maps, risk blocks, and learning-path output need a stable contract.[page:6] |
| N-06 | **Architect MVP Surface** | There is no explicit product task to build the actual architect user experience described in `AGENT_SKILL_ARCHITECT_MVP.md`.[page:6][page:7] |
| N-07 | **Framework Matrix Explorer** | The new strategy prioritizes framework guidance, but no dedicated roadmap task exists for turning framework mappings into a decision layer.[page:3][page:7] |
| N-08 | **Trust / Validation Score Engine** | The architect needs recommendation confidence, maturity, or trust scoring to avoid black-box outputs.[page:6] |
| N-09 | **Blueprint / Export Contract** | Export is mentioned in the MVP, but no roadmap task defines formats, schemas, or portability guarantees.[page:6] |
| N-10 | **Metrics + Instrumentation Plan** | The pivot needs product metrics such as architecture runs, share rate, output-to-star conversion, and contributor conversion from architect flows.[page:6] |

### Missing supporting tasks

- **Search-to-architect integration task**: `ROADMAP_V2.md` includes semantic search, but not architect-aware retrieval logic.[page:4][page:6]
- **Benchmark-to-ranking integration task**: benchmarks exist as content goals, but not as recommendation inputs.[page:4][page:6]
- **Paths schema + path scoring task**: paths are treated as learning content, but not as a recommendation output primitive.[page:4][page:6]

---

## Task Re-ranking

Below is the re-ranking of the remaining roadmap tasks using the new “AI Engineering OS / Agent Skill Architect” lens.

### Product Alignment Score legend

- **Strongly Aligned** — directly enables Agent Skill Architect or its distribution.
- **Partially Aligned** — useful supporting work, but not core to the new flagship.
- **Misaligned** — still useful, but no longer a near-term priority.
- **Obsolete** — should be removed or replaced.

| New Rank | Task | Previous Wave | Alignment | Rationale |
|---:|---|---|---|---|
| 1 | **N-01 Architect Data Contract Audit** | New | **Strongly Aligned** | Architect cannot work credibly without structured data validation across schema, graph, search, benchmarks, and paths.[page:3][page:6] |
| 2 | **N-02 Goal / Use-Case Taxonomy** | New | **Strongly Aligned** | User input normalization is foundational for recommendation quality.[page:6] |
| 3 | **N-03 Recommendation Engine Spec** | New | **Strongly Aligned** | Defines how the product thinks; missing today.[page:6] |
| 4 | **N-04 Graph Query + Dependency Logic Spec** | New | **Strongly Aligned** | The graph becomes core product logic under the pivot.[page:5][page:6] |
| 5 | **N-05 Architecture Output Schema** | New | **Strongly Aligned** | Required for blueprint export, UI consistency, and future API/CLI reuse.[page:6] |
| 6 | **N-06 Architect MVP Surface** | New | **Strongly Aligned** | This is the flagship feature itself.[page:6][page:7] |
| 7 | **T-25 Semantic Search Embeddings** | Wave 6 | **Strongly Aligned** | Natural-language discovery becomes core retrieval infrastructure for architect mode.[page:4][page:7] |
| 8 | **T-19 CLI Scaffold + PyPI Publication** | Wave 3 | **Strongly Aligned** | Programmatic access reinforces OS positioning and future architect CLI surface.[page:4][page:7] |
| 9 | **T-20 CLI `new` Wizard** | Wave 3 | **Partially Aligned** | Useful for contributor growth, but less critical than architect decision support.[page:4] |
| 10 | **T-24 MCP Registry Listing** | Wave 3 | **Strongly Aligned** | Major distribution channel for the OS identity.[page:4][page:7] |
| 11 | **T-23 LangChain Hub Submission** | Wave 3 | **Strongly Aligned** | Strengthens integration narrative and framework presence.[page:4][page:7] |
| 12 | **N-07 Framework Matrix Explorer** | New | **Strongly Aligned** | Explicitly prioritized by the strategic pivot but missing from the roadmap.[page:7] |
| 13 | **T-08 Populate `paths/`** | Wave 4 | **Strongly Aligned** | Architect output needs guided learning and build sequence.[page:4][page:6] |
| 14 | **T-14 Benchmark Expansion** | Wave 2 | **Partially Aligned** | Important as evidence infrastructure, but should be targeted by architect demand, not category coverage first.[page:4][page:6] |
| 15 | **T-04 Stub Upgrade Wave 1** | Wave 1 | **Partially Aligned** | Still valuable, but should be narrowed to architect-critical skills only.[page:4][page:7] |
| 16 | **T-07 Model Comparison AST Sweep** | Wave 1 | **Partially Aligned** | Better reframed as trust/ranking enrichment for architect outputs.[page:4][page:6] |
| 17 | **T-05 Stub Upgrade Wave 2** | Wave 2 | **Misaligned** | Bulk expansion no longer belongs this early.[page:4][page:7] |
| 18 | **T-21 AI Stub Upgrade Draft PRs** | Wave 6 | **Partially Aligned** | Useful later for scaling content once architect demand reveals gaps.[page:4][page:6] |
| 19 | **T-10 Mobile-Responsive UI Refactor** | Wave 7 | **Partially Aligned** | Important for reach, but not a prerequisite for product differentiation.[page:4] |
| 20 | **T-06 Stub Upgrade Wave 3** | Wave 5 | **Misaligned** | Full-catalog completion is no longer the critical path.[page:4][page:7] |
| 21 | **T-22 Skill Champion Frontmatter** | Wave 7 | **Misaligned** | Governance value exists, but it does not move the flagship product forward soon enough.[page:4] |

### Obsolete or replaceable framing

No remaining roadmap task is fully obsolete in substance, but **T-05** and **T-06** are obsolete in their current framing as major near-term value engines.[page:4][page:7]

---

## Dependency Changes

The old roadmap assumes that content quality is the first prerequisite and that distribution follows once enough skills are upgraded.[page:4] The new strategy changes this: the architect requires **structured intelligence layers** first, while broad content quality becomes a support multiplier rather than the initial gate.[page:6][page:7]

### New prerequisite shifts

| Task | Old prerequisite logic | New prerequisite logic |
|---|---|---|
| T-04 Stub Upgrade Wave 1 | First task in roadmap | Depends on architect-critical skill selection criteria so upgrades support recommendation quality, not generic coverage. |
| T-14 Benchmark Expansion | After enough v2 content | Depends on architect ranking needs; benchmark categories should follow likely architecture demand. |
| T-19 CLI Scaffold | After content and exports | Can begin earlier once output schema and architect contracts are stable. |
| T-24 MCP Registry | After 50 quality skills | Depends more on a coherent product story and usable API than on broad content volume alone. |
| T-25 Semantic Search | Late-stage enhancement | Becomes an early enabling task for architect retrieval. |
| T-08 Paths | After content | Depends on normalized goal taxonomy because paths should map to architect outputs. |

### New prerequisite tasks

The following become prerequisites before meaningful architect implementation:

1. **N-01 Architect Data Contract Audit**
2. **N-02 Goal / Use-Case Taxonomy**
3. **N-03 Recommendation Engine Spec**
4. **N-04 Graph Query + Dependency Logic Spec**
5. **N-05 Architecture Output Schema**

Without those, implementation risks producing a flashy surface with weak recommendation quality.[page:6]

---

## New Critical Path

The critical path should no longer be “upgrade stubs, then distribute.” The new execution sequence should be:

### Phase A — Architect Foundations

1. **N-01 Architect Data Contract Audit**
2. **N-02 Goal / Use-Case Taxonomy**
3. **N-03 Recommendation Engine Spec**
4. **N-04 Graph Query + Dependency Logic Spec**
5. **N-05 Architecture Output Schema**

### Phase B — Flagship Product

6. **N-06 Architect MVP Surface**
7. **T-25 Semantic Search Embeddings**
8. **N-07 Framework Matrix Explorer**
9. **T-08 Populate `paths/` for architect learning outputs**

### Phase C — Distribution Layer

10. **T-19 CLI Scaffold + PyPI**
11. **T-24 MCP Registry Listing**
12. **T-23 LangChain Hub Submission**

### Phase D — Evidence + Content Support

13. **T-14 Benchmark Expansion**
14. **T-04 Stub Upgrade Wave 1 (architect-critical skills only)**
15. **T-07 Model Comparison Enrichment**
16. **T-21 AI Stub Upgrade Draft PRs**

### Phase E — Scale + Polish

17. **T-05 Stub Upgrade Wave 2**
18. **T-10 Mobile UI Refactor**
19. **T-06 Stub Upgrade Wave 3**
20. **T-22 Skill Champion Field**

This sequence aligns execution with the new thesis: **build the decision engine first, then use content and distribution to compound it**.[page:6][page:7]

---

## Recommended Next Sprint

The next sprint should not start with bulk stub work. It should start with the minimum design-and-data package needed to make Agent Skill Architect implementation real.

### Sprint goal

Create the architect execution substrate.

### Recommended sprint contents

1. **N-01 Architect Data Contract Audit**
   - Validate which existing assets are trustworthy enough for recommendation use: `docs/api/skills.json`, `docs/api/graph.json`, `docs/search-index.json`, `meta/skill-schema.json`, `meta/frameworks.md`, benchmark metadata, and `paths/` assets.[page:3][page:5][page:6]
2. **N-02 Goal / Use-Case Taxonomy**
   - Define the input language for architect mode: goals, deployment classes, budget bands, model families, and framework aliases.[page:6]
3. **N-03 Recommendation Engine Spec**
   - Specify ranking signals, weighting, substitution logic, and explanation format.[page:6]
4. **N-05 Architecture Output Schema**
   - Lock the structure of `agent-blueprint.json`, dependency maps, learning path output, and risk blocks.[page:6]

### Sprint deliverables

- one architect data audit document,
- one intent taxonomy document,
- one recommendation specification,
- one architecture output contract,
- one updated roadmap reflecting the new critical path.

### Why this sprint

This is the smallest sprint that converts the pivot from aspiration into an executable product program. It also reduces the chance of building a beautiful but shallow Architect UI disconnected from the repository’s strongest real assets.[page:6][page:7]

---

## Final Validation Judgment

The Wave 0 pivot is **strategically correct but operationally incomplete**. The repository now has a public identity consistent with an AI Engineering OS and a documented flagship concept in Agent Skill Architect, but the roadmap still optimizes for catalog-local gains instead of global product leverage.[page:2][page:4][page:6][page:7]

Validation outcome:

- **Strategic direction:** Validated.[page:2][page:6][page:7]
- **Current roadmap alignment:** Not validated.[page:4][page:7]
- **Need for roadmap rewrite:** Critical.[page:4][page:6][page:7]
- **Recommended next sprint:** Architect foundations, not stub expansion.[page:6][page:7]

# Agent Skill Architect v1

## Product Vision

Agent Skill Architect turns Skills Tree from a static catalog into a decision engine for building AI agents. The current project already has the foundations for this shift: a structured skill schema, framework mapping, benchmark templates, quality reporting, release packaging, and a roadmap that confirms API, search, graph, paths UI, and release foundations are already delivered.[page:35][page:2]

The problem it solves is decision overload. A developer who wants to build an agent does not usually need “more skills to browse.” They need a reliable answer to a much sharper question: *given my goal, framework, model, budget, and deployment constraints, what architecture should I build and why?* Skills Tree currently helps with discovery, but Agent Skill Architect would help with design.[page:2][page:35]

### What problem does it solve?

It solves five product failures at once:

1. **Choice paralysis** — users do not know which skills fit together.
2. **Architecture uncertainty** — users can find components, but not system designs.
3. **Framework ambiguity** — users cannot quickly see how choices differ across LangChain, MCP, OpenAI Agents SDK, Mastra, or LlamaIndex.[page:35]
4. **Trust gaps** — users need evidence, dependencies, and risks, not just descriptions.[page:2][page:35]
5. **Poor return loops** — a catalog is useful once; an architecture planner becomes useful every time a new agent idea appears.

### Who uses it?

Primary users:

- **AI application developers** choosing patterns and components for a new agent.
- **Framework evaluators** comparing stacks across ecosystems.
- **Technical founders** who need an implementation path without hiring a dedicated agent architect.
- **Open-source contributors** who want to see where content gaps exist and what additions improve recommendations most.
- **Sponsors and platform teams** looking for a neutral skill intelligence layer with evidence and compatibility signals.

### Why would they return?

Users return because the system becomes a planning surface, not a reading surface. They come back when:

- They start a new agent project.
- They change framework, model, or deployment environment.
- They need a lower-cost or lower-latency variant of an existing stack.
- They want to compare alternatives for a current build.
- They want to monitor when benchmarks, graph relations, or recommended stacks improve.

The return loop is stronger than a search page because user intent evolves over time. Architectures are revisited, refined, shared, and benchmarked.

---

## User Journey

### Input

The v1 user flow starts with a structured intake form that captures the minimum planning context.

#### Required inputs

- **Goal** — what the user is building, such as research agent, browser agent, RAG assistant, coding copilot, eval harness, voice assistant, or workflow automator.
- **Framework** — LangChain, LlamaIndex, OpenAI Agents SDK, MCP-native, Mastra, custom Python, or undecided.[page:35]
- **Model** — Claude, GPT, Gemini, local model, or model-agnostic.
- **Budget** — low-cost, balanced, premium, or explicit monthly/runtime budget.
- **Deployment Type** — local, serverless, containerized, edge, enterprise/private VPC, or hybrid.

#### Optional inputs for v1.1 or v2

- Latency tolerance.
- Need for browsing or computer use.
- Memory depth required.
- Compliance or security sensitivity.
- Team skill level.

### Output

The output should feel like a design review, not a list of links.

#### Output sections

- **Architecture** — a recommended end-to-end agent pattern, for example planner → retriever → tool router → response synthesizer → evaluator.
- **Skills** — ranked recommended skills for each architecture layer, with substitutes.
- **Dependencies** — prerequisite skills, supporting systems, framework requirements, and skill-to-skill links from the graph.[page:35]
- **Learning Path** — a guided sequence of skills or `paths/` modules to learn or implement the stack in order.[page:2]
- **Risks** — likely failure points, weak assumptions, model limitations, cost blowups, latency trade-offs, and operational concerns.

### Example journey

A user selects:

- Goal: Research agent
- Framework: LangChain
- Model: Claude
- Budget: Balanced
- Deployment: Containerized

The system returns:

1. A recommended architecture for retrieval, summarization, memory, citation, and monitoring.
2. The exact skills most relevant to each stage.
3. Dependencies such as RAG, memory injection, summarization, web search, and evaluation patterns.
4. A learning path built from existing path assets plus missing-skill recommendations.[page:2]
5. A risk report explaining citation drift, retrieval quality, and cost trade-offs.

---

## System Design

### Inputs

The system consumes structured user intent plus repository-derived product data.

#### User inputs

- Goal
- Framework
- Model
- Budget
- Deployment type

#### Repository inputs

- Skill metadata from schema-validated frontmatter.[page:35]
- Graph relationships between skills and systems.[page:2][page:35]
- Searchable descriptions and examples.[page:2]
- Benchmarks and comparisons for evidence weighting.[page:2][page:35]
- Paths for learning sequence output.[page:2]
- Framework mappings for compatibility.[page:35]

### Processing

Processing should happen in five phases.

#### Phase 1 — Intent normalization

Convert the user’s raw inputs into a normalized query profile:

- Goal class.
- Capability requirements.
- Constraints.
- Preferred framework.
- Preferred model family.
- Deployment profile.

Example: “research agent + LangChain + Claude + balanced budget + containerized” becomes a requirements vector emphasizing web search, RAG, summarization, citation, memory, and monitoring.

#### Phase 2 — Candidate generation

Fetch candidate skills, systems, and blueprints using:

- taxonomy match,
- framework compatibility,
- benchmark relevance,
- graph adjacency,
- search relevance,
- path inclusion.

This phase should over-generate candidates rather than prematurely narrow them.

#### Phase 3 — Dependency expansion

Expand the shortlist through graph edges:

- prerequisites,
- complements,
- substitutes,
- common bundles,
- anti-pattern or conflict relationships.

This is where the graph becomes strategic instead of decorative.

#### Phase 4 — Architecture synthesis

Group candidates into architecture layers such as:

- input/perception,
- planning/reasoning,
- memory,
- tool execution,
- orchestration,
- monitoring,
- safety.

Then produce a coherent stack, not just top-ranked isolated skills.

#### Phase 5 — Explanation generation

Produce human-readable reasoning for each recommendation:

- why it was selected,
- what it depends on,
- what risks it introduces,
- what lower-cost or lower-complexity alternative exists.

### Recommendation Engine

The recommendation engine selects the best skill candidates for each architecture slot.

#### Responsibilities

- Match user goals to needed capability classes.
- Prefer schema-complete and benchmark-backed skills where possible.[page:35][page:2]
- Respect framework fit and deployment fit.
- Avoid recommending isolated skills that create hidden integration debt.
- Recommend substitute skills where multiple valid paths exist.

#### Core recommendation logic

The engine should combine:

- rule-based matching for core taxonomy,
- graph-based neighborhood expansion,
- evidence weighting from benchmarks and quality reports,
- heuristic stack templates for common goals.

### Ranking Engine

The ranking engine scores candidate skills and architectures.

#### Proposed v1 score dimensions

- Goal relevance.
- Framework compatibility.
- Model suitability.
- Budget fit.
- Deployment fit.
- Benchmark evidence.
- Graph centrality or trust.
- Skill quality level (v2/v3 status, example depth, failure modes).
- Path usefulness.

#### Output of the ranking engine

- Top architecture recommendation.
- 2–3 alternate architectures.
- Ranked skill list per architecture layer.
- Confidence score with explanation.

### Graph Engine

The graph engine is the differentiator.

#### Responsibilities

- Store and query skill nodes and relationship edges.
- Expand dependency chains.
- Detect complementary bundles.
- Surface substitutes when a preferred skill does not fit budget, framework, or deployment.
- Highlight risk clusters, such as architectures overly dependent on a single fragile skill.

#### Required graph operations

- Neighbor lookup.
- Shortest useful path between goal and implementation skills.
- Bundle extraction.
- Conflict detection.
- Learning path projection.

### Outputs

The final product output should contain five artifacts per session:

1. **Architecture Card** — the recommended system design.
2. **Skill Stack Table** — selected skills by layer with rationale.
3. **Dependency Map** — direct and indirect dependencies.
4. **Learning Path** — ordered implementation or study sequence.
5. **Risk Report** — primary trade-offs, weak links, and mitigations.

---

## Data Sources

Agent Skill Architect should reuse current repository assets rather than invent a separate data universe.

### `graph.json`

Use as the primary relationship layer for:

- dependency edges,
- related skills,
- bundle discovery,
- graph expansion,
- alternate pathing.

The roadmap and reality audit state that graph foundations already exist, which makes this file central to architect-mode recommendations rather than just visualization.[page:2]

### `search-index.json`

Use for:

- initial candidate retrieval,
- keyword and intent lookups,
- fallback matching when graph coverage is incomplete,
- fast browser-side suggestions.

The roadmap states that search infrastructure is already in place, and later work adds semantic layers on top of it.[page:2]

### `skill-schema.json`

Use as the canonical contract for:

- metadata validation,
- category and level filters,
- frameworks field,
- related skill references,
- future champion or trust metadata.[page:35]

### Framework mappings

Use `meta/frameworks.md` and any derived mappings for:

- framework-specific compatibility,
- architecture rendering per framework,
- alternate implementation suggestions across ecosystems.[page:35]

### Benchmarks

Use benchmark files and benchmark templates for:

- evidence weighting,
- model and method comparison,
- trust scoring,
- ranking tie-breakers.

The roadmap explicitly treats benchmarks as evidence-backed guidance and a strategic artifact for every taxonomy category.[page:2]

### Paths

Use the `paths/` system for:

- learning-path output,
- onboarding routes,
- milestone generation,
- implementation order.

The roadmap already defines `paths/` as the mechanism for guided entry and learning sequence design.[page:2]

---

## MVP Scope

### What can be built in 2 weeks?

A 2-week MVP should be a **guided architecture recommender**, not a full autonomous planner.

#### MVP capabilities

- Simple form with five inputs: goal, framework, model, budget, deployment.
- Candidate retrieval from search index plus schema metadata.
- Basic graph expansion from `graph.json`.
- Rule-based ranking engine with weighted scoring.
- Single architecture output with:
  - recommended skill stack,
  - dependencies,
  - learning path,
  - risks,
  - deep links back to skill pages.
- Static export of one shareable result page.

#### Explicitly out of MVP

- Real-time semantic embeddings.
- Automated benchmark execution.
- Multi-user persistence.
- Personalized recommendation history.
- LLM-generated architecture prose beyond lightweight templating.
- External API access.

The point of the MVP is to prove that Skills Tree can answer “what should I build?” rather than only “what exists?”

---

## V2 Scope

### What can be built in 30 days?

V2 should make the system feel much smarter and more reusable.

#### V2 additions

- Multiple architecture variants: cheapest, safest, fastest, simplest.
- Better graph traversal and substitute recommendation.
- Benchmark-aware ranking.
- Framework Matrix view inside the output.
- Path-aware implementation plan with milestones.
- Session permalink or static sharable architecture page.
- Better explanation engine with confidence and evidence callouts.
- Architecture comparison mode between two frameworks or two model choices.

V2 should move the product from “interesting prototype” to “shareable workflow tool.”

---

## V3 Scope

### What can be built in 90 days?

V3 should turn Agent Skill Architect into the signature surface of the project.

#### V3 additions

- Semantic search layer using embeddings or nearest-neighbor lookups, aligned with the roadmap’s semantic search direction.[page:2]
- Trust scoring using benchmark coverage, freshness, skill quality, and graph confidence.
- API endpoint for architecture generation.
- CLI command such as `skills-tree architect`.
- Export to JSON, markdown, and blueprint formats.
- Saved architecture history.
- Contributor feedback loop: “missing skill” and “improve this recommendation.”
- Sponsor or enterprise mode for policy, deployment, and compliance constraints.
- Public “popular architectures” gallery for backlinks and sharing.

At V3, the product stops being a docs enhancement and becomes a platform layer.

---

## Success Metrics

Success should be measured at both repository and product-surface levels.

### GitHub stars

Track:

- total stars,
- weekly star velocity,
- stars per architecture-share visit,
- stars following major architecture-launch content.

### Visitors

Track:

- unique visitors to the architect page,
- architecture runs per visitor,
- bounce rate versus static catalog pages.

### Returning users

Track:

- 7-day return rate,
- 30-day return rate,
- repeat architecture sessions per user cohort.

### Contributor growth

Track:

- new contributors after launch,
- PRs tied to recommendation improvements,
- new or upgraded skills referenced by architecture reports.

### Sponsor interest

Track:

- inbound partnership requests,
- sponsor page visits,
- demos requested,
- conversion from architecture feature mentions to sponsorship conversations.

### Product metrics specific to Agent Skill Architect

- completion rate of architecture flow,
- click-through rate from output to underlying skills,
- share rate of generated architectures,
- confidence score acceptance rate,
- architecture export count.

---

## Implementation Plan

This section defines the exact milestones, files, and dependencies needed to build Agent Skill Architect without writing code in this document.

### Milestone 1 — Data Contract Audit

#### Goal

Confirm all required fields exist and identify gaps.

#### Files touched

- `meta/skill-schema.json`[page:35]
- `meta/frameworks.md`[page:35]
- `meta/QUALITY-REPORT.md`[page:35]
- `docs/api/skills.json`.[page:2]

#### Deliverables

- Required-field checklist.
- Missing metadata list.
- Recommendation-weight field definitions.

### Milestone 2 — Architecture Input Taxonomy

#### Goal

Define normalized intent classes for user input.

#### Files to create or update

- `meta/agent-architect-inputs.md`
- `meta/glossary.md` if new goal terms are needed.[page:35]

#### Deliverables

- Goal taxonomy.
- Budget classes.
- Deployment classes.
- Framework aliases.

### Milestone 3 — Recommendation Specification

#### Goal

Define scoring rules and architecture templates.

#### Files to create

- `meta/agent-architect-ranking.md`
- `meta/agent-architect-templates.md`

#### Dependencies

- `graph.json`
- `search-index.json`
- `docs/api/skills.json`
- benchmark metadata.

### Milestone 4 — Graph Query Specification

#### Goal

Define the graph operations needed for architect mode.

#### Files to create

- `meta/agent-architect-graph.md`

#### Deliverables

- edge types,
- path rules,
- substitute logic,
- risk heuristics.

### Milestone 5 — Output Specification

#### Goal

Design the architecture report format.

#### Files to create

- `meta/agent-architect-output-spec.md`

#### Deliverables

- Architecture card schema.
- Skill stack schema.
- Risk block schema.
- Learning path schema.
- Share/export schema.

### Milestone 6 — MVP Product Surface

#### Goal

Define where the feature lives in the website and how users discover it.

#### Files likely involved

- `docs/index.html`.[page:2]
- `docs/paths.html` if cross-linked from learning paths.[page:2]
- `meta/ROADMAP_V2.md` for future planning reference.[page:2]

#### Deliverables

- navigation placement,
- entry CTA,
- results layout,
- mobile behavior.

### Milestone 7 — Metrics + Instrumentation Plan

#### Goal

Define how success is measured before build begins.

#### Files to create

- `meta/agent-architect-metrics.md`

#### Deliverables

- event taxonomy,
- funnel definition,
- KPI dashboard requirements.

### Exact dependencies

Core dependencies already visible in the repo:

- `meta/skill-schema.json` for structure and validation.[page:35]
- `meta/frameworks.md` for ecosystem mapping.[page:35]
- `meta/benchmark-template.md` and benchmark files for evidence logic.[page:35][page:2]
- `docs/api/skills.json` for structured export surface.[page:2]
- graph export foundations already marked complete in roadmap v2.[page:2]
- search infrastructure already marked complete in roadmap v2.[page:2]
- `paths/` and `docs/paths.html` foundations already marked complete in roadmap v2.[page:2]

---

## Risk Analysis

### Risk 1 — Weak or inconsistent metadata

If skill metadata is incomplete or inconsistent, recommendations will look arbitrary.

#### Mitigation

- Run a schema audit first.
- Weight only trusted fields in v1.
- Expose confidence and “data incomplete” states instead of pretending certainty.

### Risk 2 — Graph quality is too shallow

If graph relationships are sparse or noisy, dependency expansion becomes misleading.

#### Mitigation

- Start with a high-confidence subset of graph edges.
- Prefer explicit frontmatter links and curated mappings.
- Mark inferred edges separately from declared ones.

### Risk 3 — Output feels generic

If the architect returns obvious advice, users will not share or revisit it.

#### Mitigation

- Emphasize architecture structure, alternatives, risks, and reasoning.
- Include framework-specific and deployment-specific deltas.
- Add benchmark-backed evidence wherever available.

### Risk 4 — Search and graph disagree

Keyword retrieval and graph relationships may return conflicting candidates.

#### Mitigation

- Use multi-stage ranking.
- Show primary recommendation and alternates.
- Log divergence cases for future tuning.

### Risk 5 — Not enough benchmark coverage

Some categories may lack enough evidence for confident ranking.

#### Mitigation

- Use benchmark evidence as a boost, not a hard requirement.
- Fall back to quality score plus graph fit.
- Label evidence strength visibly.

### Risk 6 — Too much scope for a first release

The idea is large and can sprawl into a platform rewrite.

#### Mitigation

- Lock the 2-week MVP to a single architecture result format.
- Defer persistence, API, semantic embeddings, and advanced personalization.
- Use existing repository assets aggressively before creating new systems.

### Risk 7 — Hard-to-explain recommendations reduce trust

If users cannot tell why a skill was chosen, the feature may feel like a black box.

#### Mitigation

- Every recommendation must include rationale.
- Every architecture must include evidence, risks, and alternatives.
- Link deeply back into the source skills and benchmarks.

### Risk 8 — Competitors copy the interface quickly

A visible UI can be copied faster than an underlying intelligence layer.

#### Mitigation

- Build the moat in graph quality, benchmark grounding, structured mappings, and explainable ranking.
- Treat the interface as presentation and the recommendation system as the asset.

---

## Final Recommendation

Agent Skill Architect v1 should be treated as the product layer that unifies Skills Tree’s existing structured assets. The current project already has schema, roadmap-confirmed graph/search/API foundations, framework mapping, quality systems, and benchmark direction.[page:35][page:2] The winning move is not adding more isolated content surfaces, but turning those assets into a planning engine that tells users what to build, why to build it that way, and what to learn next.

In short: **Skills Tree should evolve from a catalog of skills into an architect for agent systems.**

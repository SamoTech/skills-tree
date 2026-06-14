# Skills Tree — OS Master Plan

## Purpose

This document supersedes `meta/ROADMAP_V2.md` as the primary execution plan for Skills Tree. The goal is to transform Skills Tree from a catalog of AI skills into an **AI Engineering Operating System**: a product that helps developers discover, compare, validate, compose, and operationalize the capabilities required to build production AI agents.[page:49]

The current public positioning already points in this direction. The repository README describes Skills Tree as an “AI Engineering Operating System,” highlights 361 skills across 17 categories, and frames the platform as something that maps, validates, composes, and operationalizes agent capabilities rather than merely listing them.[page:49] The master plan therefore treats the catalog as an important asset, but not the end product. The product is the intelligence layer built on top of the catalog.

---

## Product Vision

Skills Tree should become the default planning and decision layer for AI engineering. Instead of forcing users to manually browse dozens of markdown files and infer an architecture, the platform should let them describe what they want to build and receive a recommended system design, supporting skills, dependencies, framework options, evidence, risks, and next steps.[page:49]

The long-term vision is simple:

- A developer says what kind of agent they want.
- Skills Tree recommends how to build it.
- The recommendation is grounded in structured skill data, graph relationships, framework mappings, benchmarks, and learning paths.
- The result can be explored in the UI, queried through an API, consumed via CLI, and distributed through MCP and framework ecosystems.

This turns the repository from a content destination into infrastructure for AI builders.

---

## Product Pillars

### 1. Decision Intelligence

The system must answer “what should I build?” rather than only “what exists?” This pillar is embodied by Agent Skill Architect and the recommendation engine.

### 2. Structured Trust

Every recommendation should be backed by structured inputs, explicit dependencies, benchmark signals, and transparent rationale. Users should understand *why* a recommendation was made and how confident the system is.

### 3. Composable Knowledge

The graph, schema, framework mappings, and paths must work together as a single knowledge system. Skills Tree’s moat comes from relationship quality, not just page count.

### 4. Multi-Surface Access

The same core intelligence should be accessible through the website, CLI, API, and MCP-friendly surfaces. The UI is not the product; the intelligence layer is.

### 5. Community-Compounding Quality

Contributors should not just add pages. They should improve the recommendation quality of the system by filling data gaps, strengthening links, adding benchmarks, and upgrading architect-critical skills.

---

## Core User Journeys

### Journey 1 — Plan an agent system

A developer enters a goal, framework, model, budget, and deployment type, then receives a recommended architecture, supporting skills, dependencies, learning path, and risks.

### Journey 2 — Compare implementation options

A builder compares frameworks, model trade-offs, and skill alternatives to choose the best implementation path for a specific agent use case.

### Journey 3 — Validate a current stack

A user enters an existing stack and checks whether it is missing crucial capabilities, relying on weak components, or ignoring better substitutes.

### Journey 4 — Learn the stack in order

A user receives a path-like progression from prerequisite concepts to implementation-ready systems, instead of browsing random isolated pages.

### Journey 5 — Integrate Skills Tree into tooling

A power user, team, or product consumes recommendations and skill intelligence through CLI, API, or MCP-compatible interfaces.

---

## Agent Skill Architect Vision

Agent Skill Architect is the flagship product surface. It should let users describe the agent they want to build and receive a structured architecture recommendation.

### Inputs

- Goal
- Framework
- Model
- Budget
- Deployment type

### Outputs

- Architecture pattern
- Recommended skill stack
- Dependencies and prerequisites
- Learning path
- Risks and trade-offs
- Optional alternatives

### Why it matters

This shifts Skills Tree from passive discovery to active engineering guidance. It creates a shareable artifact, a repeat-use workflow, and a much stronger product identity than a large markdown catalog alone.

---

## Recommendation Engine Vision

The recommendation engine is the logic core of the operating system. It should combine rule-based scoring, graph expansion, framework compatibility, benchmark signals, and quality metadata to assemble coherent skill stacks rather than isolated top results.

### Responsibilities

- Normalize user intent.
- Retrieve candidate skills, systems, and blueprints.
- Expand candidates through graph relationships.
- Rank candidates by fit, evidence, compatibility, and trust.
- Group results into a practical architecture.
- Explain each recommendation clearly.

### Design principle

Recommendations must be **explainable**. A black-box ranker would reduce trust. Every major recommendation should say why it fits, what it depends on, and what alternatives exist.

---

## Knowledge Graph Vision

The knowledge graph should be more than a visualization. It should become the structural engine behind recommendation, dependency resolution, substitute discovery, bundle detection, and path generation.

### Core graph capabilities

- Skill-to-skill dependency mapping.
- Complementary bundle detection.
- Substitute recommendation.
- Conflict or anti-pattern detection.
- Architecture-layer clustering.
- Learning path projection.

### Strategic value

This is one of the hardest parts for competitors to copy quickly. A scraped catalog can imitate content; it cannot quickly reproduce a curated and trustworthy relationship graph.

---

## Framework Matrix Vision

The framework matrix should become a first-class product surface for comparing how the same capability is implemented across ecosystems such as LangChain, LlamaIndex, OpenAI Agents SDK, MCP-native approaches, Mastra, and custom stacks.

### The matrix should answer

- Which frameworks support a capability natively?
- Where are the trade-offs in abstraction, control, observability, and cost?
- Which framework best fits a given deployment or team profile?
- How do recommended architectures differ by framework?

### Strategic value

Framework decisions drive adoption and backlinks because developers actively search for neutral comparisons before committing to a stack.

---

## Semantic Search Vision

Search should evolve from keyword retrieval into intent-aware discovery. The user should be able to ask for outcomes or constraints, not just known skill names.

### Search should support queries like

- “best skills for browser agents with memory”
- “low-cost RAG stack for local deployment”
- “OpenAI Agents SDK alternatives for tool orchestration”

### Strategic value

Semantic search strengthens both direct discovery and Architect candidate generation. It also raises the value of every future structured data improvement.

---

## CLI Vision

The CLI should expose Skills Tree as an engineering tool, not just a website companion.

### CLI goals

- Query recommendations from terminal workflows.
- Generate blueprints or architecture summaries.
- Scaffold skills or systems.
- Validate metadata and recommendation inputs.
- Support CI or automation use cases.

### Strategic value

A real CLI makes the project feel like infrastructure. It improves developer adoption, sponsor credibility, and long-term integration potential.

---

## API Vision

The API should expose the intelligence layer in programmable form. External tools, IDE extensions, dashboards, and agents should be able to query skill recommendations, graph relations, frameworks, and blueprint outputs.

### API goals

- Return ranked skills by use case.
- Return architecture recommendations.
- Return graph neighbors, dependencies, and substitutes.
- Return framework comparisons.
- Return blueprint-ready output formats.

### Strategic value

The API turns Skills Tree from a destination into a dependency. That creates real defensibility and downstream distribution.

---

## MCP Vision

MCP should be treated as a distribution and integration channel for the operating system. A compatible interface allows agent runtimes and tool ecosystems to consume Skills Tree intelligence directly.

### MCP goals

- Expose recommendation functions.
- Expose skill and graph lookups.
- Support blueprint retrieval.
- Position Skills Tree inside agent-native ecosystems.

### Strategic value

This aligns the product with where AI tooling is going: systems that are discoverable and callable by other agent platforms, not just browsable by humans.

---

## Distribution Strategy

Distribution should follow the product surface, not precede it.

### Primary distribution channels

- GitHub repository and README as authority layer.[page:49]
- GitHub Pages site as public product surface.[page:49]
- CLI for developer workflows.
- API for integrations.
- MCP registry for agent-native distribution.
- LangChain Hub and similar ecosystems for framework-native discovery.

### Distribution principle

Every major distribution move should point back to a concrete product experience, ideally Agent Skill Architect, framework comparisons, or exportable blueprints.

---

## Success Metrics

### Product usage

- Unique visitors to Architect and framework surfaces.
- Architecture runs per visitor.
- Search-to-recommendation conversion.
- Blueprint export count.
- API request volume.
- CLI installs and active usage.

### Repository growth

- GitHub stars.[page:49]
- Star velocity per week.
- Fork growth.[page:49]
- Contributor count and active contributor rate.[page:49]

### Retention

- 7-day returning users.
- 30-day returning users.
- Repeat Architect sessions.
- Repeat framework comparison sessions.

### Quality and trust

- Recommendation acceptance rate.
- Click-through to source skills.
- Benchmark-backed recommendation coverage.
- Architect confidence score coverage.

### Sponsorship and ecosystem pull

- Sponsor inquiries.
- Sponsor conversion rate.[page:49]
- Backlinks from technical blogs.
- Integrations built on the API or MCP surface.

---

## Execution Phases

Only four execution phases exist in the OS master plan. Every roadmap item must map to one of them.

### Phase 1 — Architect Foundations

Purpose: build the structured substrate required to power recommendations.

#### Existing tasks mapped here

- T-25 Semantic Search Embeddings.
- T-08 Populate `paths/`.
- T-14 Benchmark Expansion.
- T-07 Model Comparison enrichment.
- T-04 Stub Upgrade Wave 1, but only for architect-critical skills.

#### New tasks required in this phase

- **A1. Architect Data Contract Audit**
- **A2. Goal / Use-Case Taxonomy**
- **A3. Recommendation Engine Specification**
- **A4. Graph Query + Dependency Logic Specification**
- **A5. Architecture Output Schema**
- **A6. Trust / Confidence Scoring Model**
- **A7. Framework Matrix Data Model**
- **A8. Search-to-Architect Retrieval Spec**

### Phase 2 — Agent Skill Architect MVP

Purpose: deliver the first flagship product surface.

#### Existing tasks mapped here

- No current roadmap task fully covers this phase.

#### New tasks required in this phase

- **B1. Architect MVP UI Surface**
- **B2. Architecture Result Renderer**
- **B3. Blueprint Export Format**
- **B4. Learning Path Output Engine**
- **B5. Risk Explanation Engine**
- **B6. Framework Matrix Explorer**
- **B7. Architect Session Metrics Instrumentation**

### Phase 3 — Distribution Layer

Purpose: expose the operating system through multiple access surfaces.

#### Existing tasks mapped here

- T-19 CLI Scaffold + PyPI publication.
- T-20 CLI `new` wizard.
- T-24 MCP registry listing.
- T-23 LangChain Hub submission.

#### New tasks required in this phase

- **C1. Architect API Endpoints**
- **C2. CLI `architect` Command**
- **C3. MCP Recommendation Surface**
- **C4. Public Blueprint Gallery**
- **C5. Integration Docs for API / CLI / MCP**

### Phase 4 — Scale & Intelligence

Purpose: strengthen quality, reach, and automation after the flagship exists.

#### Existing tasks mapped here

- T-05 Stub Upgrade Wave 2.
- T-06 Stub Upgrade Wave 3.
- T-21 AI Stub Upgrade Draft PRs.
- T-10 Mobile-responsive UI refactor.
- T-22 Skill Champion frontmatter.

#### New tasks required in this phase

- **D1. Recommendation Feedback Loop**
- **D2. Architecture Popularity / Community Signals**
- **D3. Sponsor / Enterprise Mode Constraints**
- **D4. Automated Gap Detection for Missing Skills**
- **D5. Historical Architecture Diffing**

---

## Task Mapping Summary

| Task | New Phase | Notes |
|---|---|---|
| T-04 Stub Upgrade Wave 1 | Phase 1 | Narrow to architect-critical skills only. |
| T-05 Stub Upgrade Wave 2 | Phase 4 | Supports scale, not initial differentiation. |
| T-06 Stub Upgrade Wave 3 | Phase 4 | Long-tail catalog completion. |
| T-07 Model Comparison AST Sweep | Phase 1 | Reframe as ranking/trust enrichment. |
| T-08 Populate `paths/` | Phase 1 | Needed for learning-path output. |
| T-10 Mobile-responsive UI | Phase 4 | Important polish, not critical path. |
| T-14 Benchmark Expansion | Phase 1 | Evidence infrastructure for Architect. |
| T-19 CLI Scaffold + PyPI | Phase 3 | Distribution layer. |
| T-20 CLI `new` Wizard | Phase 3 | Contributor workflow and tool access. |
| T-21 AI Stub Upgrade Draft PRs | Phase 4 | Scale accelerator after product exists. |
| T-22 Skill Champion Field | Phase 4 | Governance and attribution layer. |
| T-23 LangChain Hub Submission | Phase 3 | Ecosystem distribution. |
| T-24 MCP Registry Listing | Phase 3 | Agent-native distribution. |
| T-25 Semantic Search Embeddings | Phase 1 | Core retrieval layer. |

---

## Tasks to Remove

These tasks should be removed from the roadmap **in their current framing**, because they optimize local catalog growth rather than the new OS thesis.

- **T-05 Stub Upgrade Wave 2** as a near-term expansion priority.
- **T-06 Stub Upgrade Wave 3** as a roadmap-defining objective.

They are not removed from the project entirely, but they should be removed as primary strategic milestones and reintroduced only as scale tasks in Phase 4.

---

## Tasks to Merge

### Merge group 1

- **T-07 Model Comparison AST Sweep**
- **T-14 Benchmark Expansion**
- **T-04 Stub Upgrade Wave 1**

These should merge into a broader Phase 1 program:

- **Architect-Critical Knowledge Hardening**

This merged program focuses on upgrading only the skills, comparisons, and benchmarks that directly improve recommendation quality.

### Merge group 2

- **T-19 CLI Scaffold + PyPI**
- **T-20 CLI `new` Wizard**

These should merge into:

- **Developer CLI Surface**

### Merge group 3

- **T-23 LangChain Hub Submission**
- **T-24 MCP Registry Listing**

These should merge into:

- **Ecosystem Distribution Integrations**

---

## Tasks to Rename

| Old task | New name |
|---|---|
| T-04 Stub Upgrade Wave 1 | **Architect-Critical Skill Hardening** |
| T-07 Model Comparison AST Sweep | **Model Compatibility Signal Enrichment** |
| T-08 Populate `paths/` | **Learning Path Engine Foundations** |
| T-14 Benchmark Expansion | **Benchmark Evidence Layer** |
| T-19 CLI Scaffold + PyPI | **Developer CLI Surface** |
| T-20 CLI `new` Wizard | **CLI Contribution Scaffolding** |
| T-23 LangChain Hub Submission | **Framework Ecosystem Distribution** |
| T-24 MCP Registry Listing | **Agent-Native Distribution** |
| T-25 Semantic Search Embeddings | **Intent-Aware Semantic Retrieval** |
| T-21 AI Stub Upgrade Draft PRs | **AI-Assisted Knowledge Expansion** |

---

## New Tasks Required

These tasks do not currently exist in `ROADMAP_V2.md` but are required by the operating system vision.

### Phase 1 — Architect Foundations

- A1. Architect Data Contract Audit.
- A2. Goal / Use-Case Taxonomy.
- A3. Recommendation Engine Specification.
- A4. Graph Query + Dependency Logic Specification.
- A5. Architecture Output Schema.
- A6. Trust / Confidence Scoring Model.
- A7. Framework Matrix Data Model.
- A8. Search-to-Architect Retrieval Spec.

### Phase 2 — Agent Skill Architect MVP

- B1. Architect MVP UI Surface.
- B2. Architecture Result Renderer.
- B3. Blueprint Export Format.
- B4. Learning Path Output Engine.
- B5. Risk Explanation Engine.
- B6. Framework Matrix Explorer.
- B7. Architect Session Metrics Instrumentation.

### Phase 3 — Distribution Layer

- C1. Architect API Endpoints.
- C2. CLI `architect` Command.
- C3. MCP Recommendation Surface.
- C4. Public Blueprint Gallery.
- C5. Integration Docs for API / CLI / MCP.

### Phase 4 — Scale & Intelligence

- D1. Recommendation Feedback Loop.
- D2. Architecture Popularity / Community Signals.
- D3. Sponsor / Enterprise Mode Constraints.
- D4. Automated Gap Detection for Missing Skills.
- D5. Historical Architecture Diffing.

---

## Final Direction

The operating system strategy changes the meaning of the roadmap. The repository is no longer optimized primarily to become a more complete catalog. It is optimized to become the **default intelligence layer for AI engineering decisions**. Content remains important, but only insofar as it strengthens recommendation quality, trust, framework understanding, and architecture generation.

The execution rule is therefore simple:

1. Build the structured intelligence substrate.
2. Ship Agent Skill Architect MVP.
3. Expose the system through CLI, API, MCP, and ecosystem surfaces.
4. Scale content, automation, and intelligence after the flagship exists.

That is the OS Master Plan.

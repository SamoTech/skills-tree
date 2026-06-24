# USER INTENT GRAPH
## INITIATIVE-020 — Phase 1
**Project:** Skills Tree · **Date:** 2026-06-24

---

## Overview

The User Intent Graph maps the causal chain from a user's initial goal through to the platform actions they take, the capabilities they need, and the gaps they encounter. In the absence of live telemetry, these personas are derived from: repository structure (what was built implies what was expected), meta-document history (20+ planning documents reveal intended use cases), and the AI engineering community's known behavioral patterns.

**Caveat:** Until analytics are deployed, these are demand hypotheses — not confirmed user segments. Each persona requires validation through the first 30-day instrumented period.

---

## Persona 1 — The Agent Builder

```
GOAL:          Build a production AI agent (e.g., customer support bot, research agent)
TRIGGER:       Starting from scratch; overwhelmed by tool/framework choice
DISCOVERY:     Google search → "AI agent skills" or via HN/Reddit thread
LANDING:       Explorer or README
DESIRED OUTCOME: A clear map of what skills my agent needs, in what order to implement them
PLATFORM ACTIONS:
  → Opens Explorer
  → Searches for "tool use", "memory", "planning"
  → Explores node dependencies
  → Opens Blueprint Generator
  → Generates "Customer Support Agent" blueprint
  → Downloads blueprint JSON
  → Begins implementation
SKILLS USED:   Tool Use, Memory Management, Context Window, Retrieval, Guardrails
BLUEPRINT GENERATED: agent-customer-support-v1.json
MISSING CAPABILITIES (currently):
  - No "start here" onboarding flow in Explorer
  - No suggested skill ordering / learning path output
  - Blueprint JSON has no code scaffold or starter template
  - No failure modes documented per blueprint
  - No benchmark recommendations attached
```

---

## Persona 2 — The AI Engineering Team Lead

```
GOAL:          Audit team's AI capability gaps; plan hiring and training
TRIGGER:       Team ships agents with inconsistent quality; wants a common vocabulary
DISCOVERY:     LinkedIn or word-of-mouth from developer community
LANDING:       README → meta/AGENT_ARCHITECT_VISION.md
DESIRED OUTCOME: A skills matrix that maps to team roles; a gap analysis tool
PLATFORM ACTIONS:
  → Reads README and vision docs
  → Opens Explorer to survey domain coverage
  → Generates blueprints for each agent type team builds
  → Compares skill stacks across blueprints
SKILLS USED:   Orchestration, Evaluation, Observability, Security, Multi-Agent Coordination
BLUEPRINT GENERATED: agent-internal-ops-v1.json, agent-research-v1.json
MISSING CAPABILITIES (currently):
  - No team workspace or shareable blueprint URLs
  - No role → skill mapping view
  - No CSV/PDF export of skill coverage
  - No benchmark comparison across blueprints
```

---

## Persona 3 — The LLM/MCP Integrator

```
GOAL:          Integrate skills-tree knowledge into Cursor, Claude, or a custom AI assistant
TRIGGER:       Building a coding assistant that needs to reason about AI engineering tasks
DISCOVERY:     MCP marketplace, GitHub search for "MCP skills"
LANDING:       MCP server directory or README MCP section
DESIRED OUTCOME: Install MCP server, query skills graph from inside IDE
PLATFORM ACTIONS:
  → Finds MCP server in marketplace
  → Installs via Claude/Cursor settings
  → Queries: "what skills does an agent need for web scraping?"
  → Receives structured skill list with dependencies
SKILLS USED:   (consumed programmatically — all nodes)
MISSING CAPABILITIES (currently):
  - MCP server not yet listed in Claude/Cursor/Windsurf marketplaces
  - No natural language query interface on top of graph
  - No versioned graph API endpoint (only static JSON)
  - No changelog feed for MCP consumers to track graph updates
```

---

## Persona 4 — The Self-Taught AI Engineer

```
GOAL:          Learn AI engineering systematically; build a portfolio of skills
TRIGGER:       Career transition into AI; overwhelmed by scattered tutorials
DISCOVERY:     Google, Reddit r/LearnMachineLearning, or YouTube
LANDING:       Explorer
DESIRED OUTCOME: A learning roadmap; know what to learn in what order
PLATFORM ACTIONS:
  → Browses Explorer by category
  → Clicks individual skill nodes
  → Looks for "beginner → intermediate → advanced" path
  → Generates a learning blueprint for their target role
SKILLS USED:   Varies by target role
MISSING CAPABILITIES (currently):
  - No learning path / roadmap mode in Explorer
  - No difficulty/prerequisite levels on nodes
  - No external resource links per skill
  - No progress tracking
  - Skill descriptions are brief; no expanded explanations
```

---

## Persona 5 — The Researcher / Taxonomy Contributor

```
GOAL:          Reference or extend the skills taxonomy for research or publication
TRIGGER:       Writing a paper on AI agent capabilities; needs a canonical taxonomy
DISCOVERY:     Google Scholar adjacent search, GitHub search "AI skills taxonomy"
LANDING:       GitHub repo README or SKILLS_GRAPH.json directly
DESIRED OUTCOME: Citable, versioned, machine-readable taxonomy; ability to propose additions
PLATFORM ACTIONS:
  → Clones or downloads SKILLS_GRAPH.json
  → Reviews schema and category structure
  → Opens a GitHub Issue or PR to propose a new skill
  → Cites the taxonomy in a paper or blog post
MISSING CAPABILITIES (currently):
  - No DOI or citable release (Zenodo not configured)
  - No contributor guide for skill proposals
  - No review process documented for new skill acceptance
  - No taxonomy versioning communicated externally (semver exists but not publicized)
```

---

## Aggregate Missing Capabilities — Ranked by Frequency

| Gap | Personas Affected | Priority |
|-----|------------------|----------|
| No onboarding / "start here" flow | 1, 4 | P0 |
| No learning path output from Blueprint | 1, 4 | P0 |
| MCP not in public marketplaces | 3 | P0 |
| No failure modes per blueprint | 1, 2 | P1 |
| No shareable blueprint URLs | 2 | P1 |
| No role → skill matrix view | 2 | P1 |
| No external resource links on nodes | 4 | P1 |
| No citable release / DOI | 5 | P2 |
| No contributor workflow for skill proposals | 5 | P2 |
| No benchmark recommendations | 1, 2 | P2 |

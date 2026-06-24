# PRODUCT SURFACE RANKING
## INITIATIVE-020 — Phase 2
**Project:** Skills Tree · **Date:** 2026-06-24

---

## Overview

All six product surfaces are scored across five dimensions. Scores are 1–5 (5 = highest). Weights reflect the current stage of the project: a pre-traction platform where virality and contributor interest unlock all downstream value.

**Scoring weights:**
- Usage (current): 20%
- Retention potential: 20%
- Virality (shareability, discovery potential): 25%
- Contributor interest (likelihood of community ownership): 20%
- Monetization potential (without changing open-source license): 15%

---

## Surface Scoring Matrix

| Surface | Usage (×0.20) | Retention (×0.20) | Virality (×0.25) | Contributor Interest (×0.20) | Monetization (×0.15) | **Weighted Score** |
|---------|--------------|-------------------|-----------------|------------------------------|---------------------|-------------------|
| Explorer | 2 | 3 | 5 | 3 | 2 | **3.30** |
| Blueprint Generator | 2 | 4 | 4 | 4 | 4 | **3.60** |
| MCP Server | 1 | 5 | 5 | 5 | 5 | **4.10** |
| CLI | 2 | 3 | 2 | 3 | 2 | **2.50** |
| Graph API | 1 | 4 | 3 | 4 | 4 | **3.05** |
| Learning Paths | 0 | 5 | 5 | 3 | 4 | **3.50** |
| Benchmarks | 0 | 3 | 4 | 2 | 3 | **2.55** |

---

## Surface Analysis

### 1. MCP Server — Score: 4.10 (HIGHEST)

The MCP ecosystem is the fastest-growing integration surface in AI tooling as of 2026. Claude, Cursor, Windsurf, and VS Code Copilot all support MCP. A skills-tree MCP server that answers "what skills does my agent need?" from inside an IDE is a **zero-friction distribution mechanism**: users discover it through marketplace listings, install in one click, and the graph becomes part of their daily workflow. Virality is structural — every developer who installs it becomes a potential advocate. Monetization path is clear: hosted enterprise graph with private skill namespaces.

**Current state:** MCP server exists in repo but is not listed in any public marketplace. This is the highest-ROI action gap in the entire platform.

### 2. Blueprint Generator — Score: 3.60

Blueprint generation is the core value proposition made tangible. A user arrives with a vague goal ("I want to build an agent") and leaves with a structured artifact (skill stack, dependencies, learning path). This is inherently shareable — blueprints can become the "shareable output" that drives word-of-mouth. Retention is high because blueprints represent decisions that users revisit as their projects evolve.

**Current state:** Functional but missing failure modes, learning paths, and shareable URLs — all three of which are required for virality to activate.

### 3. Explorer — Score: 3.30

The Explorer is the first visual impression. A graph of 368 nodes with search and filters is genuinely impressive as a discovery surface. It went viral-adjacent in similar projects (e.g., roadmap.sh attracted millions of users with a simpler concept). The Explorer's virality is gated by: (a) it was broken on GitHub Pages until 2026-06-23, and (b) there is no "shareable node" link — you cannot send someone a URL to a specific skill.

**Current state:** Now functional. Next required feature is deep-linkable node URLs to unlock shareability.

### 4. Learning Paths — Score: 3.50 (DOES NOT EXIST YET)

This surface scores high despite not existing because the demand signal is enormous: "how do I learn AI engineering systematically" is one of the most searched queries in the developer community. A curated, graph-derived learning path that outputs a personalized roadmap from current skill level to target role would be the most shareable artifact the platform could produce. It is also the most direct path to certification monetization.

**Current state:** Not built. Highest-value greenfield surface.

### 5. Graph API — Score: 3.05

A stable, versioned REST/GraphQL API over the skills graph enables third-party integrations: company skill matrices, LMS platforms, HR tools, AI capability audits. Currently the graph is a static JSON file — functional for single consumers but unscalable for integrations. The API surface is a prerequisite for monetization (hosted API tier) but is not itself a discovery mechanism.

### 6. CLI — Score: 2.50

The CLI serves power users and automation pipelines. It scores lower because it requires installation friction and appeals to a narrow persona (developer already using the project). It is valuable as a contributor tool but is not a growth mechanism.

### 7. Benchmarks — Score: 2.55

Benchmarks are a knowledge moat asset (see MOAT_INDEX) but are not yet built. They would score higher with content. An agent benchmark comparison page (e.g., "which agent framework performs best on tool-use tasks?") would attract researchers and be highly citable. Currently this surface is aspirational.

---

## Investment Priority (Next 90 Days)

| Priority | Surface | Action |
|----------|---------|--------|
| 1 | MCP Server | Submit to Claude, Cursor, Windsurf marketplaces |
| 2 | Blueprint Generator | Add failure modes + shareable URLs |
| 3 | Explorer | Add deep-linkable node URLs |
| 4 | Learning Paths | Spec and build V1 |
| 5 | Graph API | Design versioned endpoint schema |

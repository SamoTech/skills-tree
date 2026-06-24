# Explorer V2 Specification

**Initiative:** INITIATIVE-014A.2 — Phase 2  
**Date:** 2026-06-24  
**Lead Agent:** Repository Architect  
**Status:** SPEC — Pending implementation in INITIATIVE-014A.3  

---

## Current Explorer State

The Explorer is a D3-powered force graph with:
- Node search (functional)
- Category filters (functional)
- Node detail pane (functional)
- Graph path normalization fix (INITIATIVE-012B1)

---

## V2 Feature Specifications

### Feature 1 — Featured Skills Panel
**Priority:** P1 — Wow Factor  
**Description:** A curated row of 6–8 "battle-tested" skills displayed at the top of the sidebar as quick-access entry points. First-time visitors have no natural entry point into the graph — the Featured panel removes the blank-slate problem.

**Implementation:**
- Static array of `featuredSkillIds` in `app.js` (e.g., `rag`, `react-pattern`, `chain-of-thought`, `function-calling`, `memory-injection`, `multi-agent-orchestration`)
- Rendered as pill chips above the search bar
- Click focuses + highlights the node in the graph and opens the detail pane
- Label: "⭐ Popular Skills"

---

### Feature 2 — Popular Learning Paths
**Priority:** P1 — Engagement  
**Description:** 4 pre-defined learning path shortcuts visible in the sidebar. Each path is a named sequence of skill IDs that the user can step through linearly.

**Paths to implement:**
1. "RAG Mastery" — 6 skills: embedding-generation → vector-store-retrieval → rag → memory-injection → hybrid-search → graphrag
2. "Build Your First Agent" — 5 skills: function-calling → react-pattern → chain-of-thought → tool-use → multi-agent-orchestration
3. "Computer Use" — 4 skills: screen-reading → ocr → click-type-scroll → browser-automation
4. "Security Hardening" — 4 skills: input-sanitization → prompt-injection-defense → secret-scanning → audit-logging

**Implementation:**
- Sidebar "Learning Paths" section below search
- Click highlights all path nodes on the graph
- "Next skill" arrow button steps through the path

---

### Feature 3 — Random Discovery Button
**Priority:** P2 — Delight  
**Description:** A "Discover a random skill" button that selects a random node and opens its detail pane. Encourages exploration and repeat visits.

**Implementation:**
- Button in sidebar footer: "🎲 Surprise me"
- Picks random node from `graphData.nodes` (excluding sandbox)
- Zooms to node, opens detail pane
- Keyboard shortcut: `R`

---

### Feature 4 — Skill Share Card
**Priority:** P1 — Virality  
**Description:** Each skill detail pane gets a "Share this skill" button that copies a deep-link URL (`?skill=<id>`) to clipboard. Enables viral sharing of individual skill pages.

**URL format:** `https://samotech.github.io/skills-tree/explorer/?skill=rag`

**Implementation:**
- Add `?skill=<id>` deep-link parsing to `app.js` on load
- "🔗 Share" button in detail pane header
- Toast confirmation on copy

---

### Feature 5 — Dependency Visualization Highlight
**Priority:** P2 — Educational Value  
**Description:** When a skill is selected, highlight its direct prerequisites in one color and its direct dependents in another color on the graph.

**Implementation:**
- On node select: traverse `prerequisites` array from node data
- Apply CSS class `node-prereq` (blue tint) to prerequisite nodes
- Apply CSS class `node-dependent` (green tint) to nodes that list current node in their prerequisites
- Reset on deselect

---

## Implementation Order

1. Skill Share Card (highest virality, lowest effort)
2. Featured Skills Panel (first-time experience fix)
3. Random Discovery Button (delight)
4. Popular Learning Paths (engagement)
5. Dependency Visualization (educational, higher effort)

---

## Success Metrics

- Average session length: current baseline unknown → target 3+ minutes
- Share button click rate: target 5% of sessions
- Return visitor rate: target 20% within 7 days

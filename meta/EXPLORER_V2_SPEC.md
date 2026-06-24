# Explorer V2 Specification

**Initiative:** INITIATIVE-014A.2 — Phase 2  
**Date:** 2026-06-24  
**Status:** APPROVED FOR IMPLEMENTATION  
**Target:** [https://samotech.github.io/skills-tree/explorer/](https://samotech.github.io/skills-tree/explorer/)

---

## Objective

Deliver a "wow" moment to a Show HN visitor within 30 seconds of first load. The graph must be immediately engaging, explorable without any instruction, and shareable.

---

## Feature 1 — Featured Skills Section

### Display
A horizontal carousel strip at the top of the sidebar, above the search input, labeled **"✨ Start Here"**.

### Content
8 curated skills representing the most battle-tested, high-signal nodes:
- `react` (ReAct) — Agentic Patterns
- `rag` — Memory
- `cot` (Chain of Thought) — Agentic Patterns
- `function-calling` — Tool Use
- `memory-injection` — Memory
- `code-generation` — Code
- `web-search` — Web
- `input-sanitization` — Security

### Behavior
Clicking a featured skill badge fires `selectNode(id)` — centers the graph on that node, highlights its 1-hop neighborhood, and opens the detail panel. Gives first-time visitors an instant on-ramp without needing to type anything.

---

## Feature 2 — Popular Paths Section

### Display
A collapsible section in the sidebar below filters, labeled **"🗺️ Popular Paths"**.

### Content
5 curated learning paths as ordered node sequences:

| Path Name | Skills (ordered) |
|---|---|
| Build a RAG Agent | embedding-generation → vector-store-retrieval → rag → function-calling → openai-api |
| Reasoning Loop | cot → self-consistency → react → tot → reflection |
| Multi-Agent System | task-decomposition → planning → react → consensus → multi-agent-orchestration |
| Security-First Agent | input-sanitization → sandboxing → secret-scanning → audit-logging → rollback |
| Production LLM | openai-api → anthropic-api → function-calling → retry-logic → streaming |

### Behavior
Clicking a path highlights all nodes in the sequence with a sequential color overlay (step 1 = green, step 2 = teal, …) and draws a bold path edge between them. Clears on clicking elsewhere.

---

## Feature 3 — Random Discovery Button

### Display
A **"🎲 Surprise Me"** button in the sidebar toolbar, between the search input and filters.

### Behavior
1. Picks a random node from `graph.nodes` (weighted toward battle-tested: `stability === 'stable'`)
2. Animates the camera to center on that node (500ms ease-in-out)
3. Highlights the node's 2-hop neighborhood
4. Opens the node detail panel
5. Displays a small toast: `"Discovered: [Skill Name] in [Category]"`

### Rationale
Pure serendipitous exploration — the primary way developers discover adjacent skills they didn't know existed. Creates organic "rabbit hole" sessions that drive session length and return visits.

---

## Feature 4 — Skill Dependency Visualization

### Display
In the node detail panel (right sidebar), below the skill description, add a **"Dependencies"** mini-section.

### Content
Two lists derived from the graph edges:
- **Requires:** All nodes with an edge pointing *to* this node (prerequisites)
- **Enables:** All nodes this node points *to* (what you can learn next)

Each entry is a clickable chip that fires `selectNode(id)`.

### Visual
A compact inline mini-graph (D3 force simulation, radius 120px) showing only the selected node and its 1-hop neighbors, rendered inside the panel. Falls back to the chip list if the mini-graph has >8 neighbors.

---

## Feature 5 — Shareable Skill Cards

### Display
A **"Share"** button (icon: link) in the node detail panel header.

### Behavior
1. Generates a URL with hash: `https://samotech.github.io/skills-tree/explorer/#skill=rag`
2. On page load, if `#skill=<id>` is present: auto-select that node and center graph
3. Copies URL to clipboard and shows toast: `"Link copied!"`

### Social Card (Optional — Phase 3)
A generated 1200×630 OG meta tag per skill node using a dynamic template so that pasting a skill URL into Twitter/LinkedIn shows a rich card with: skill name, category, stability badge, short description.

---

## Implementation Notes

- All features are additive to the existing `docs/explorer/app.js` — no rewrites
- Featured skills and popular paths are defined as JS constants at the top of `app.js`
- Dependency viz uses existing edge data — no new data generation needed
- Shareable URLs use `window.location.hash` — no server-side routing required
- The `getGraphUrl()` path normalization from INITIATIVE-012B.1 remains intact

---

## Acceptance Criteria

- [ ] Featured Skills strip renders above search input
- [ ] Clicking a featured skill centers graph on that node
- [ ] Popular Paths renders 5 paths, click highlights path
- [ ] Surprise Me fires on click, centers on random node, opens panel
- [ ] Dependency chips render in node detail panel
- [ ] `#skill=<id>` URL deep-links to node on load
- [ ] Share button copies URL to clipboard
- [ ] All features work on localhost AND GitHub Pages
- [ ] No new console errors introduced

# PLATFORM ASCENSION — FINAL DECISION & ROADMAP
## INITIATIVE-020 — Phases 0–8 Summary
**Project:** Skills Tree · **Date:** 2026-06-24 · **Classification:** STRATEGIC

---

## Final Classification

> **Skills Tree is classified as: E. AI Engineering Infrastructure Layer**

### Evidence

| Criterion | Evidence |
|-----------|----------|
| Structured, machine-readable knowledge graph | 515+ skills, 774+ edges, semantic versioning |
| Consumed programmatically by other systems | MCP server, REST API, CLI, JSON endpoint |
| Dependency graph encoding expert judgment | 774 edges represent curatorial knowledge unavailable elsewhere |
| Blueprint generation (goal → architecture) | Converts knowledge into actionable engineering specs |
| Designed for integration, not end-user consumption | MCP, API, CLI are all developer-facing primitives |
| Infrastructure implies version stability contract | Semver, CI validation, schema guards |

**Why not D (AI Engineering Operating System)?** An OS implies a runtime, a process model, and an execution environment. Skills Tree does not execute agents — it informs their design. It is the layer that sits beneath the operating environment, not the environment itself.

**Why not C (Knowledge Platform)?** A knowledge platform is primarily consumed by humans browsing content. Skills Tree's highest-value delivery mechanism is machine-to-machine (MCP server queries, API calls, CLI pipelines).

---

## 12-Month Strategic Recommendation

### Phase I — Signal (Months 1–3): Get Real Data

No new features until there is measurement. Deploy Plausible Analytics on Explorer. Submit MCP server to Claude + Cursor marketplaces. Submit Show HN. Seed GitHub Discussions. Collect 90 days of real usage data.

**Key deliverable:** First 500 MAU. First 50 MCP installations. First 5 external contributors.

### Phase II — Moat (Months 4–8): Build What No One Else Will

Use signal data to prioritize highest-demand moat assets: Failure Mode Library, Role-Based Learning Paths, Architecture Builder V1, Framework Compatibility Matrix.

**Key deliverable:** 2,000 MAU. Architecture Builder live. 20 external integrations.

### Phase III — Infrastructure (Months 9–12): Lock In the Layer

Launch Hosted API (paid tiers). Establish Skills Tree as the citation reference for AI engineering capability discussions. Begin 3 enterprise Graph pilots.

**Key deliverable:** 5,000 MAU. First $1K MRR. 5 enterprise pilots in conversation.

---

## Next Initiatives — Ranked by ROI

### INITIATIVE-021: MCP MARKETPLACE LAUNCH
**Classification:** P0 Distribution
**ROI:** Highest.

Submit MCP server to Anthropic MCP registry, Cursor marketplace, Windsurf plugin directory, and awesome-mcp-servers list. Write MCP demo blog post + demo video. Update README with one-click MCP install badge. Add telemetry to count installations.

**Timeline:** 2 weeks
**Estimated impact:** 10× increase in daily active usage vs. current baseline. 500+ installations in 30 days.

---

### INITIATIVE-022: EXPLORER ANALYTICS & SHAREABILITY
**Classification:** P0 Measurement + P1 Virality
**ROI:** Second highest.

Deploy Plausible Analytics (privacy-first, GDPR-compliant). Wire custom events: node_click, search_performed, blueprint_generated, share_clicked. Implement deep-linkable node URLs (`/explorer#skill-tool-use`). Add "Share this skill" and "Share this blueprint" buttons with permanent URLs.

**Timeline:** 2–3 weeks
**Estimated impact:** First real MAU baseline; 10% of blueprint generations become share events within 60 days.

---

### INITIATIVE-023: FAILURE MODE LIBRARY
**Classification:** P0 Moat
**ROI:** Third highest.

Document 5 failure modes for each of 10 common agent architecture types (50 total). Structure as graph-linked data referencing skill nodes. Add Failure Modes tab to Explorer node detail panel. Publish "50 Ways Your AI Agent Will Fail" as launch blog post. Submit to HN, r/MachineLearning, r/LocalLLaMA.

**Timeline:** 4–6 weeks
**Estimated impact:** High-traffic inbound content; potential HN front-page moment; 500+ new users from organic search within 90 days.

---

## Initiative ROI Summary

| Initiative | Work | Impact | ROI Rank |
|-----------|------|--------|----------|
| INIT-021: MCP Launch | 2 weeks | Daily-active installs in 3 marketplaces | **#1** |
| INIT-022: Analytics + Shareability | 2–3 weeks | First real data + viral loop activation | **#2** |
| INIT-023: Failure Mode Library | 4–6 weeks | Moat asset + inbound content + HN moment | **#3** |

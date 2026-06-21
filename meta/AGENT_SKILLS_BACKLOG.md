# AGENT_SKILLS_BACKLOG.md

**Last Updated:** 2026-06-21 (Post TASK-005B)  
**Graph State:** 53 nodes / 108 edges

---

## PRIORITY 1 — Immediate Next

### TASK-006: Skill File Stubs for 6 New Nodes

Create skill file stubs in `09-agentic-patterns/` or appropriate directories for:
- `skill:structured-data-reading`
- `skill:database-reading`
- `skill:file-system-access`
- `skill:output-formatting`
- `skill:schema-validation`
- `skill:data-transformation`

Each file: id, name, category, level, description, prerequisites, use cases, related skills.

**Effort:** Low  **Risk:** Low  **Value:** High (closes Phase 2 gap)

---

## PRIORITY 2 — Near Term

### TASK-007: 01-perception Category Bootstrap

Add perception cluster nodes:
- `skill:visual-understanding`
- `skill:audio-processing`
- `skill:multimodal-fusion`
- `skill:ocr-reading`
- `skill:screenshot-analysis`

Requires: NODE_SELECTION audit first.

**Effort:** Medium  **Risk:** Medium (new category)

### TASK-008: 08-safety Category Bootstrap

Add safety/guardrail nodes:
- `skill:output-filtering`
- `skill:prompt-injection-defense`
- `skill:constitutional-constraints`
- `skill:toxicity-detection`

**Effort:** Medium  **Risk:** Low

---

## PRIORITY 3 — Deferred

### TASK-009: Graph Export to RDF/OWL

Export SKILLS_GRAPH.json to RDF/Turtle for semantic web interoperability.

### TASK-010: Evidence Deriver Integration

Link graph nodes to real skill file metadata for live evidence counts.

### TASK-011: Centrality API Endpoint

Expose graph centrality scores via MCP server tool.

---

## DEFERRED NODES (from TASK-004 audit)

| Node | Reason deferred | Target task |
|---|---|---|
| `skill:api-response-parsing` | Merged into data-extraction | N/A — resolved |
| `skill:visual-understanding` | New category needed | TASK-007 |
| `skill:audio-processing` | New category needed | TASK-007 |
| `skill:multimodal-fusion` | Depends on visual + audio | TASK-007 |

# RECOVERY PLAN

**Audit ID:** TASK-000A  
**Date:** 2026-06-21  
**Status:** Repository is UNHEALTHY in governance layer; HEALTHY in content layer  
**Approach:** Prioritize by ROI — fix foundational blockers before adding features

---

## Repository Health Assessment

| Layer | Health | Action Needed |
|---|---|---|
| Skills corpus (377 files) | ✅ HEALTHY | Continue stub upgrades (roadmap T-04 through T-06) |
| CI/CD (30 workflows) | ✅ HEALTHY | Monitor; no immediate action |
| Schema/validation | ✅ HEALTHY | No action needed |
| GitHub Pages UI | ✅ HEALTHY | Mobile refactor planned (T-10) |
| Governance files | ❌ CRITICAL | All placeholders — rebuild required |
| Graph data layer | ❌ CRITICAL | `SKILLS_GRAPH.json` is placeholder — build required |
| Learning paths | ❌ MISSING | `paths/` empty — content needed |
| CLI/PyPI | ❌ MISSING | Not started |

---

## Recovery Actions (Ordered by ROI)

### R-01 — Rebuild Governance Layer [IMMEDIATE]

**What:** Replace all 11 placeholder governance files with real content

**Files to rebuild:**
1. `meta/MEMORY_STATE.md` — current project state, verified node/skill counts, active decisions
2. `meta/DECISION_LOG.md` — log of architectural decisions made to date (derive from PROJECT_MEMORY)
3. `meta/AGENT_SKILLS_MASTER_PLAN.md` — derive from PROJECT_MEMORY Sections 5, 14, 15
4. `meta/AGENT_SKILLS_BACKLOG.md` — derive from PROJECT_MEMORY Section 5 backlog
5. All missing planning documents: `PROJECT_CONSTITUTION.md`, `GRAPH_DIFF_PLAN.md`

**Source of truth:** `PROJECT_MEMORY.md` Sections 5, 14, 15 contain the real backlog and roadmap.

**Effort:** Low (content derivation, not creation)
**Risk:** Low
**ROI:** HIGH — unlocks all future governed task execution

---

### R-02 — Build Real Graph Data [HIGH PRIORITY]

**What:** Replace `data/SKILLS_GRAPH.json` placeholder with real graph built from skill `related_skills` fields

**Method:**
1. Option A: Trigger / inspect `build-graph.yml` workflow — it already exists
2. Option B: Extend `tools/export_skills.py` to output graph.json
3. Option C: New Python script that reads all skill frontmatter and emits nodes + edges

**Do NOT:** Manually author node/edge lists — would recreate the fabrication problem

**Expected output format:**
```json
{
  "schema_version": "1.0",
  "generated_at": "YYYY-MM-DD",
  "nodes": [{"id": "skills/03-memory/rag.md", "title": "...", "category": "03-memory", "level": "...", "version": "..."}],
  "edges": [{"source": "skills/03-memory/rag.md", "target": "skills/09-agentic-patterns/react.md", "type": "related"}]
}
```

**Effort:** Medium
**Risk:** Low
**ROI:** HIGH — unlocks D3 graph visualization (T-12) and graph-based navigation

---

### R-03 — Stub Upgrade Blitz [HIGH PRIORITY, ONGOING]

**What:** Upgrade 302 v1 stubs to v2 minimum (per PROJECT_MEMORY P0-1)

**This is the #1 content priority per the project's own assessment.**

**Target:** 50 skills per wave (T-04 → T-05 → T-06 per PROJECT_MEMORY Section 15)

**Effort:** High (content creation)
**Risk:** Low
**ROI:** HIGHEST — eliminates 80% stub ratio, the #1 trust killer

---

### R-04 — Enable GitHub Discussions [LOW EFFORT, HIGH IMPACT]

**What:** Toggle GitHub Discussions, create 5 categories, pin Start Here post

**This is T-01 in PROJECT_MEMORY Section 15 and P0-2 in the backlog.**

**Effort:** 2 hours
**Risk:** Zero
**ROI:** HIGH — opens community loop

---

### R-05 — Populate `paths/` [MEDIUM PRIORITY]

**What:** Create 4 learning track YAML files (Research Agent, Memory-First, Computer Use, Zero-to-Production)

**This is T-08 in PROJECT_MEMORY Section 15.**

**Effort:** Medium
**Risk:** Low (depends on enough v2 skills existing in target categories)
**ROI:** HIGH — dramatically improves discoverability and SEO

---

### R-06 — Fix `ARCHITECTURE_OUTPUT_SCHEMA.md` [LOW EFFORT]

**What:** Replace the 1-byte empty file with real content or delete it

**Effort:** Minimal
**Risk:** Zero

---

## What NOT to Do

1. **Do NOT launch another "graph implementation task"** until R-01 (governance) and R-02 (real graph build) are complete. Prior graph tasks failed because they operated without verified baselines.

2. **Do NOT trust MEMORY_STATE.md, DECISION_LOG.md, or any TASK report** until R-01 is complete and files have verified, substantive content (>1KB per governance doc).

3. **Do NOT add new graph nodes manually** — use the workflow or script method (R-02). Manual node lists are how the fabrication problem started.

4. **Do NOT assume prior agent session numbers are real** — 47, 53, 58 nodes; 93, 108, 122 edges — all fabricated. The real starting point is 0 graph nodes.

---

## Recovery Sequence

```
R-01 Governance rebuild
  └── R-02 Graph build (from skill files)
        └── TASK-002 (graph validation + UI integration, when ready)

R-03 Stub upgrades (parallel, ongoing)
R-04 GitHub Discussions (immediate, parallel)
R-05 Paths population (after R-03 wave 1)
```

---

## Success Criteria for Recovery Complete

- [ ] `meta/MEMORY_STATE.md` > 2,000 bytes with real content
- [ ] `meta/DECISION_LOG.md` > 2,000 bytes with real decisions
- [ ] `meta/AGENT_SKILLS_MASTER_PLAN.md` > 3,000 bytes with real plan
- [ ] `meta/AGENT_SKILLS_BACKLOG.md` > 2,000 bytes with real backlog
- [ ] `data/SKILLS_GRAPH.json` is valid JSON with > 100 nodes
- [ ] All missing planning docs created (`PROJECT_CONSTITUTION.md`, etc.)
- [ ] No placeholder files remain in `meta/` or `data/`

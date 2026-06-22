# INITIATIVE-001 — Next Execution Prompt

**Use this prompt to begin the next session.**

---

```
MISSION: INITIATIVE-001 — Priority 1
Repository: SamoTech/skills-tree
Objective: Diagnose and fix graph generation.

FACTS (verified at commit 245b47f21962dff89fd49da612bf55992e93178a):
- tools/build_graph.py EXISTS (12,659 bytes)
- .github/workflows/build-graph.yml EXISTS (2,048 bytes)
- data/SKILLS_GRAPH.json is a placeholder (21 bytes, contains only "SKILLS_GRAPH_PLACEHOLDER")
- schema/ contains all 4 schemas
- tools/extract_edges.py EXISTS

TASK:
1. Read tools/build_graph.py
2. Read .github/workflows/build-graph.yml
3. Read data/SKILLS_GRAPH.json (confirm placeholder)
4. Identify the exact reason graph generation has not produced a real output
5. Fix the root cause (workflow permissions, missing inputs, or disabled trigger)
6. Do NOT create any new tools
7. Do NOT run any manual audits
8. Do NOT invent node counts or edge counts

SUCCESS CRITERION:
data/SKILLS_GRAPH.json must be a real JSON graph after a push to main.

DO NOT PROCEED beyond diagnosis + fix in this session.
```

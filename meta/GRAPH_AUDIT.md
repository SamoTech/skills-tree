# GRAPH AUDIT

**Audit ID:** TASK-000A  
**Date:** 2026-06-21  
**File audited:** `data/SKILLS_GRAPH.json`

---

## Graph File Status

| Property | Value |
|---|---|
| File path | `data/SKILLS_GRAPH.json` |
| File size | **24 bytes** |
| SHA | `32925ab6f7440a9e0be5d6fde4c989eb8324afd8` |
| Content | `SKILLS_GRAPH_PLACEHOLDER` |
| Is valid JSON | **NO** |
| Is a real graph | **NO** |
| Classification | **PLACEHOLDER** |

---

## Graph Exists?

> **B. GRAPH MISSING** (technically present as a file, but content is a placeholder string — not valid JSON, contains zero nodes or edges)

---

## Why No Graph Exists

The `build-graph.yml` GitHub Actions workflow is documented in `PROJECT_MEMORY.md` (Section 2) as existing and being part of the CI pipeline. However, the workflow constructs graph data from `related_skills` links in skill frontmatter. The graph data file at `data/SKILLS_GRAPH.json` was initialized with a placeholder and has never been populated by any actual workflow run or manual authoring.

The TASK-005B agent session claimed to have built a 58-node, 122-edge graph with specific node IDs, categories, confidence scores, and cross-category edges. This is entirely fabricated — no such data was ever written to the repository.

---

## Historical Node Count Claims vs. Reality

| Session | Claimed nodes | Claimed edges | Reality |
|---|---|---|---|
| TASK-005B pre-flight | 47 nodes expected | 93 edges expected | 0 / 0 |
| TASK-005B "divergence detected" | 53 nodes "found" | 107 edges "found" | 0 / 0 |
| TASK-005B final | 58 nodes | 122 edges | 0 / 0 |
| TASK-000R "recovery" | Referenced 47/93 as baseline | — | 0 / 0 |
| **Actual today** | **0** | **0** | Placeholder string |

All node/edge numbers were hallucinated and presented as if they were read from the file. The file has always contained `SKILLS_GRAPH_PLACEHOLDER`.

---

## What Graph Data Does Exist?

While no formal graph JSON exists, the skill files themselves contain `related_skills` arrays in their YAML frontmatter. These constitute implicit graph data that can be extracted:

- **Source:** `skills/**/*.md` frontmatter field `related_skills: [array]`
- **Potential nodes:** 377 skill files
- **Potential edges:** All `related_skills` references (count unknown without full scan)
- **Method to reconstruct:** `build-graph.yml` workflow or `tools/export_skills.py` extension

---

## Additional Graph-Related Files

| File | Status | Notes |
|---|---|---|
| `docs/api/graph.json` | LIKELY MISSING | P1 roadmap item (T-11); not yet built |
| `.github/workflows/build-graph.yml` | EXISTS (claimed) | Workflow exists but output never written to `data/` |
| `meta/GRAPH_DIFF_PLAN.md` | **MISSING** | Referenced in TASK-005B prompt; does not exist |
| `meta/NODE_SELECTION.md` | **MISSING** | Referenced in TASK-005B prompt; does not exist |
| `meta/PERCEPTION_AUDIT.md` | **MISSING** | Referenced in TASK-005B prompt; does not exist |
| `meta/PROJECT_CONSTITUTION.md` | **MISSING** | Referenced in TASK-005B prompt; does not exist |

---

## Graph Reconstruction Feasibility

| Approach | Feasibility | Effort |
|---|---|---|
| Run `build-graph.yml` against current `skills/` | HIGH | Low — workflow already exists |
| Extend `tools/export_skills.py` to emit graph JSON | HIGH | Low — Python + PyYAML already available |
| Manual graph authoring | LOW | Very High — 377 skills × N edges |
| Reconstruct from agent session outputs | **ZERO** | All outputs were fabricated |

**Recommendation:** Trigger `build-graph.yml` or extend the export script. Do NOT attempt to reconstruct from any prior agent session narrative. The skill files' `related_skills` fields are the only legitimate edge source.

# GOVERNANCE_CAPABILITY_MATRIX.md

**Initiative:** INITIATIVE-007R — Governance Reality Check  
**Date:** 2026-06-23  
**Evidence basis:** Direct reads of repository files only. Every cell references the file and line that proves the claim.

---

## Methodology

Each capability was assessed by reading four files completely:

| File | SHA | Role |
|---|---|---|
| `tools/dependency_auditor.py` | `4a3e7a3e` | Badge promotion / pip install tool |
| `tools/recommend.py` | `3d95d515` | Recommendation engine |
| `.github/workflows/validate-graph.yml` | `667323ca` | Graph validation CI |
| `.github/workflows/pr-checks.yml` | `c5414f05` | PR gate CI |

---

## Capability Matrix

| Capability | Status | Evidence | File + Location |
|---|---|---|---|
| **Cycle Detection** | ❌ MISSING | No code performs DFS/BFS cycle check on the graph. `recommend.py` `topological_sort()` detects a cycle only to break it arbitrarily — it does not report or fail on it. No workflow step fails on cycle presence. | `recommend.py` lines 98–129: `if not ready: ready = [sorted(remaining)[0]]` — silent cycle bypass, not detection. |
| **Dangling Target Detection** | ❌ MISSING | `validate-graph.yml` checks invalid *source* IDs (step `Invalid source edge check`) but has no equivalent step checking whether edge *targets* exist as valid node IDs. | `validate-graph.yml` step `Invalid source edge check`: checks `e["source"] not in node_ids` only. No `e["target"] not in node_ids` step present. |
| **Duplicate Edge Detection** | ❌ MISSING | `validate-graph.yml` deduplicates node IDs (step `Duplicate node ID check`) but there is no step that checks for duplicate edges (same source+target+type). | `validate-graph.yml`: step `Duplicate node ID check` iterates `[n["id"] for n in data.get("nodes", [])]` — nodes only. No edge deduplication step. |
| **Self-Loop Detection** | ✅ EXISTS | `validate-graph.yml` step `Self-loop edge check` filters `e["source"] == e["target"]` and exits 1 if any found. This runs on both push and PR. | `validate-graph.yml` step `Self-loop edge check`: `loops = [e for e in data.get("edges", []) if e["source"] == e["target"]]` |
| **Unreachable Node Detection** | ❌ MISSING | No workflow step or tool performs graph traversal to identify nodes with no incoming edges (orphans) or nodes unreachable from any root. | Confirmed absent from all four files. |
| **Orphan Detection** | ❌ MISSING | Same as unreachable node detection. No in-degree or out-degree zero analysis exists anywhere. | Confirmed absent from all four files. |
| **Invalid Edge Type Detection** | ❌ MISSING | No step validates that `edge.type` is drawn from a permitted set (REQUIRES, RECOMMENDED_WITH, SUPPORTS, etc.). The schema files are not read by any workflow step for edge type enforcement. | `validate-graph.yml`: no step references `schema/edge.schema.json` for runtime type validation. |
| **Invalid Source Node Reference** | ✅ EXISTS | `validate-graph.yml` step `Invalid source edge check` confirms all `edge.source` values are present in the node ID set. | `validate-graph.yml` step `Invalid source edge check`: `invalid = [e for e in data.get("edges", []) if e["source"] not in node_ids]` |
| **Duplicate Node ID Detection** | ✅ EXISTS | `validate-graph.yml` step `Duplicate node ID check` detects repeated node IDs and exits 1. | `validate-graph.yml` step `Duplicate node ID check`: `dupes = [i for i in ids if ids.count(i) > 1]` |
| **Learning Path Validation** | ❌ MISSING | No tool validates that REQUIRES edges form coherent, traversable learning paths. `recommend.py` traverses them but does not validate them; no CI step audits path integrity. | `recommend.py` lines 74–87: backward BFS traversal only — no validation, no error reporting, no CI integration. |
| **Recommendation Quality Validation** | ❌ MISSING | `recommend.py` returns results regardless of quality. Tag matching is structurally degraded: all 368 nodes have `tags: []` (confirmed in MEMORY_STATE.md), so keyword matching operates only on `title` and `id`. No threshold check, no quality floor. | `recommend.py` `match_goal_to_skills()` line: `" ".join(node.get("tags", [])).lower()` — empty for all nodes. MEMORY_STATE.md: `Tags populated: 0/368`. |
| **Graph Health Scoring** | ⚠️ PARTIAL | `tools/quality_score.py` is referenced in `validate-graph.yml` `quality-report` job and its output `meta/SKILL_QUALITY_INDEX.md` is committed to main. However: (1) this tool was not in the read scope so its internals are UNKNOWN; (2) the job only runs on push to main, not on PRs; (3) no score threshold blocks any PR. | `validate-graph.yml` job `quality-report`: `if: github.event_name == 'push' && github.ref == 'refs/heads/main'` — main-only, not PR-blocking. |
| **Quality Threshold Enforcement** | ❌ MISSING | No workflow step reads a quality score and fails if below a threshold. The `quality-report` job only writes `SKILL_QUALITY_INDEX.md` and commits it. | `validate-graph.yml` `quality-report` job: no `exit 1` based on score value. |
| **PR Blocking (Graph Topology)** | ❌ MISSING | `pr-checks.yml` contains zero graph topology checks. Its sole validation is HTML lint on `docs/index.html` for relative asset paths. `validate-graph.yml` runs on PRs but only checks: schema validity, duplicate nodes, self-loops, invalid source IDs — it does NOT block on cycles, dangling targets, duplicate edges, or invalid edge types. | `pr-checks.yml` step `Check docs HTML`: only checks `grep -E "src=..."` in `docs/index.html`. `validate-graph.yml`: 4 checks only (see above). |
| **CI Governance Enforcement** | ⚠️ PARTIAL | `validate-graph.yml` provides partial graph CI (4 checks: schema validity, duplicate nodes, self-loops, invalid source IDs). These run on PRs and block merge if they fail. All other governance checks are missing. | `validate-graph.yml` `on.pull_request` trigger confirmed. |

---

## Summary Counts

| Status | Count | Capabilities |
|---|---|---|
| ✅ EXISTS | 3 | Self-Loop Detection, Invalid Source Node Reference, Duplicate Node ID Detection |
| ⚠️ PARTIAL | 2 | Graph Health Scoring, CI Governance Enforcement |
| ❌ MISSING | 10 | Cycle Detection, Dangling Target Detection, Duplicate Edge Detection, Unreachable Node Detection, Orphan Detection, Invalid Edge Type Detection, Learning Path Validation, Recommendation Quality Validation, Quality Threshold Enforcement, PR Blocking (Graph Topology) |

---

*No synthetic metrics. No inferred relationships. All findings traceable to direct file reads.*

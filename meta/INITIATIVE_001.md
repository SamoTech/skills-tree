# INITIATIVE-001 — SKILLS TREE V3 REFOUNDATION

**Status:** Proposed  
**Priority:** Critical  
**Owner:** Repository Architecture  
**Created:** 2026-06-22  
**Source of Truth:** Repository state at commit `245b47f21962dff89fd49da612bf55992e93178a`

---

## Reality Check — What Already Exists

Before planning any phase, this section records what the repository *already contains*, verified by direct file listing. This prevents re-implementing what was already shipped.

### Phase A — Schema: COMPLETE

All four canonical schemas already exist under `schema/`:

| File | Size | Status |
|---|---|---|
| `schema/skill.schema.json` | 2,376 bytes | ✅ EXISTS |
| `schema/graph.schema.json` | 1,393 bytes | ✅ EXISTS |
| `schema/edge.schema.json` | 1,317 bytes | ✅ EXISTS |
| `schema/category.schema.json` | 1,123 bytes | ✅ EXISTS |

**Decision:** Phase A requires no new files. Work required: verify schema completeness against the canonical objects defined in this initiative.

### Phase C — Graph Builder: COMPLETE (tool exists, activation unknown)

`tools/build_graph.py` exists at 12,659 bytes. Whether it is wired to generate `data/SKILLS_GRAPH.json` deterministically from source files is UNKNOWN until the file is read and the CI workflow `build-graph.yml` is inspected.

### Phase D — Edge Extraction Engine: COMPLETE (tool exists)

`tools/extract_edges.py` exists at 8,705 bytes.

### Phase E — Quality Index: COMPLETE (tool exists)

`tools/quality_score.py` exists at 7,103 bytes. A separate `tools/check_skill_quality.py` also exists at 18,259 bytes.

### Phase G — Recommendation Engine: COMPLETE (tool exists)

`tools/recommend.py` exists at 8,253 bytes.

### Phase H — CI Enforcement: SUBSTANTIALLY COMPLETE

The following enforcement workflows already exist:

| Workflow | Purpose | Status |
|---|---|---|
| `.github/workflows/build-graph.yml` | Runs graph builder | ✅ EXISTS |
| `.github/workflows/validate-graph.yml` | Validates graph output | ✅ EXISTS |
| `.github/workflows/validate-skills.yml` | Validates skill files | ✅ EXISTS |
| `.github/workflows/schema-enforce.yml` | Schema enforcement | ✅ EXISTS |
| `.github/workflows/pr-checks.yml` | PR gate checks | ✅ EXISTS |
| `.github/workflows/build-and-verify.yml` | Full build + verify | ✅ EXISTS |

---

## Actual Gaps (What Does Not Exist)

Verified by direct directory listing at `245b47f21962dff89fd49da612bf55992e93178a`:

### Phase B — Structured Skill Metadata (`skill.json` sidecar files)

**Status: UNKNOWN / LIKELY MISSING**  
The initiative requires every `skills/category/skill.md` to have a companion `skills/category/skill.json`. Whether any `.json` sidecar files exist in the `skills/` directory is UNKNOWN — the skills directory was not fully traversed in this session. This is the **highest-priority gap to verify**.

**Evidence needed:** Run `find skills/ -name '*.json' | wc -l` in the repository to confirm.

### Phase F — Category Normalization (Architecture Layers)

**Status: UNKNOWN**  
The initiative proposes a 4-layer architecture:
- Layer 1: Perception
- Layer 2: Reasoning  
- Layer 3: Execution
- Layer 4: Systems

Whether the current category structure in `skills/` maps to these layers is UNKNOWN. A category audit is required before this phase can be planned.

### `data/SKILLS_GRAPH.json` — Verified Placeholder Problem

**Status: CONFIRMED BROKEN**  
Previous governance recovery (R-01, 2026-06-21) confirmed `data/SKILLS_GRAPH.json` contains only the placeholder string `SKILLS_GRAPH_PLACEHOLDER` (21 bytes). Despite `tools/build_graph.py` existing, the graph has never been successfully generated and committed by CI. This is the **single most critical blocking issue** for the entire initiative.

**Root cause candidates (unverified, require investigation):**
1. `build-graph.yml` workflow may not have write permissions to commit `data/SKILLS_GRAPH.json`
2. `build_graph.py` may depend on skill `.json` sidecar files that do not yet exist
3. The workflow may be disabled or not triggered on the correct branch
4. Schema validation may be failing silently and blocking the commit step

---

## Revised Phase Plan

Given the above analysis, the phases are re-ordered by actual gap priority:

### Priority 1 — Unblock Graph Generation

**Objective:** Get `tools/build_graph.py` to produce a valid, committed `data/SKILLS_GRAPH.json`.

Steps:
1. Read `tools/build_graph.py` — understand its input requirements
2. Read `.github/workflows/build-graph.yml` — identify why it has not committed output
3. Fix the root cause (permissions, missing inputs, or disabled trigger)
4. Verify `data/SKILLS_GRAPH.json` is a real graph JSON after a CI run

**Success criterion:** `data/SKILLS_GRAPH.json` is non-placeholder after any push to main.

### Priority 2 — Phase B: Skill Metadata Sidecar Audit

**Objective:** Determine whether `.json` sidecar files exist alongside skill `.md` files.

Steps:
1. Count `.json` files under `skills/` — if zero, Phase B is unstarted
2. If zero: design the sidecar format using `schema/skill.schema.json` as the contract
3. Generate sidecar files programmatically from existing frontmatter in `.md` files
4. Wire `build_graph.py` to consume sidecar files as its primary input

### Priority 3 — Phase F: Category Layer Mapping

**Objective:** Map existing categories to the 4-layer architecture.

Steps:
1. List all category directories under `skills/`
2. Assign each to Layer 1–4
3. Create `schema/layer.schema.json` defining the layer contract
4. Update `schema/category.schema.json` to include a `layer` field

### Phases A, C, D, E, G, H — Monitor and Harden

These phases are substantially complete at the tooling level. After graph generation is unblocked, the focus shifts to:
- Ensuring all tools are wired into CI (not just present as standalone scripts)
- Ensuring CI **fails hard** (non-zero exit) on validation errors, not just warns
- Verifying `recommend.py` can consume the generated graph and produce valid output

---

## Governance Termination Decisions

Per the initiative proposal:

| Terminated | Replacement | Reason |
|---|---|---|
| R-02 (manual graph reconstruction) | INITIATIVE-001 Priority 1 | Graph must be generated, not reconstructed manually |
| R-03 (manual edge extraction) | `tools/extract_edges.py` + CI | Tool already exists; focus is activation, not creation |
| R-05 (manual node registration) | `tools/build_graph.py` + sidecar files | Nodes must be derived from skill files, not registered manually |

**All future governance documents must reference generated artifacts only. Manual node counts and edge counts are permanently retired.**

---

## Success Criteria (Unchanged from Proposal)

- [ ] `data/SKILLS_GRAPH.json` is generated automatically on every push to main
- [ ] Manual node registration is removed (no `meta/NODE_SELECTION.md` or equivalent)
- [ ] Manual edge extraction is removed (no `meta/GRAPH_DIFF_PLAN.md` or equivalent)
- [ ] `tools/recommend.py` produces valid learning paths from the generated graph
- [ ] Governance files (`meta/MEMORY_STATE.md` etc.) are generated from repository state
- [ ] CI fails on: duplicate IDs, invalid edges, orphan references, schema failure, graph generation failure

---

## Open Questions

| Question | Blocking | Resolution |
|---|---|---|
| Does `build_graph.py` require `.json` sidecar files to run? | YES — Priority 1 | Read the script |
| Why has `build-graph.yml` never committed a real graph? | YES — Priority 1 | Read the workflow |
| How many `.json` sidecar files exist under `skills/`? | YES — Priority 2 | `find skills/ -name '*.json'` |
| What categories currently exist under `skills/`? | YES — Priority 3 | `ls skills/` |
| Does `recommend.py` depend on a valid graph to run? | NO — after Priority 1 | Read the script |

---

## Next Action

**Read `tools/build_graph.py` and `.github/workflows/build-graph.yml` to diagnose why graph generation has never produced a real output. This is the single action that unblocks all downstream phases.**

Do not create any new tools. Do not run any audits. Do not generate governance documents with invented metrics.

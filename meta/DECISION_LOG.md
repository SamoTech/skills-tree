# Decision Log

**Rule:** Only decisions provable from commits, files, or repository structure are recorded here.

---

## D-INIT-001-001 — Terminate Manual Graph Missions

**Date:** 2026-06-22  
**Decision:** Terminate R-02, R-03, R-05. Replace with INITIATIVE-001 automated pipeline.  
**Evidence:** `meta/INITIATIVE_001.md` committed at `38082503fb42c16445ce468ec7d67159cecd6dec`  
**Status:** ACTIVE

---

## D-INIT-001A-001 — Root Cause Confirmed: Workflow/Script Interface Mismatch

**Date:** 2026-06-22  
**Decision:** The graph generation failure is caused by a three-way interface mismatch between the workflow invocation, the script's CLI interface, and the output path. Fix-1 (align workflow to script) is the recommended remediation.  
**Evidence:**
- `tools/build_graph.py` SHA `f84c8e008ad17ba2f357107f7df98fab2f80fa44` — argparse defines only `--dry-run` and `--output`
- `.github/workflows/build-graph.yml` SHA `82a1afd03df5d10c3312b997b71c1fc42c300789` — workflow passes `--skills-root` and `--sbom-root` (unrecognized by script)
- `data/SKILLS_GRAPH.json` — 21-byte placeholder, never overwritten by automation
**Status:** ACTIVE — implementation pending INITIATIVE-001B

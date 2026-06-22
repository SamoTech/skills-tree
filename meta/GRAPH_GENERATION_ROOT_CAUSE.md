# Graph Generation Root Cause

**Mission:** INITIATIVE-001A  
**Date:** 2026-06-22  
**Evidence source:** Direct file reads from repository only.

---

## ROOT_CAUSE

**Three-way interface mismatch between the workflow, the script, and the output path.**

### Mismatch 1 — Unrecognized CLI arguments (PRIMARY BLOCKER)

The workflow (`build-graph.yml`) invokes the script with arguments `--skills-root` and `--sbom-root`. The script (`build_graph.py`) does not define these arguments in its argparse configuration. Python argparse exits with code 2 (`unrecognized arguments`) before any graph logic executes.

```
Workflow passes: --skills-root skills/ --sbom-root docs/sbom/ --output docs/api/graph.json
Script accepts:  --dry-run, --output
Result:          sys.exit(2) — script never runs
```

### Mismatch 2 — Output path divergence (SECONDARY)

Even if the argument error were absent, the workflow writes to `docs/api/graph.json` while the placeholder file that governance references lives at `data/SKILLS_GRAPH.json`. The workflow would generate a graph but it would land in the wrong location.

### Consequence

Every push to `skills/**/*.md` triggers the workflow. The workflow fails silently (from a graph perspective — the job appears to run). `data/SKILLS_GRAPH.json` is never written by automation. It remains the manually-committed placeholder string `SKILLS_GRAPH_PLACEHOLDER`.

---

## RECOMMENDED_FIX

**Fix-1: Align the workflow invocation to the script's actual interface.**

Change `.github/workflows/build-graph.yml` lines 35-43 from:
```yaml
- name: Build graph
  run: |
    python tools/build_graph.py \
      --skills-root skills/ \
      --sbom-root docs/sbom/ \
      --output docs/api/graph.json

- name: Commit graph
  run: |
    git add docs/api/graph.json
```

To:
```yaml
- name: Build graph
  run: |
    python tools/build_graph.py \
      --output data/SKILLS_GRAPH.json

- name: Commit graph
  run: |
    git add data/SKILLS_GRAPH.json
```

This change:
- Removes both unrecognized arguments
- Aligns the output path with the governance placeholder location
- Requires zero changes to `build_graph.py`
- Risk level: LOW

---

## READY_FOR_INITIATIVE_001B

**YES** — root cause is precisely identified with direct file evidence. Fix-1 is fully specified. No further diagnosis required.

Next session should:
1. Apply Fix-1 to `.github/workflows/build-graph.yml`
2. Trigger `workflow_dispatch` to generate the first real graph
3. Verify `data/SKILLS_GRAPH.json` is written with real node and edge counts
4. Delete the placeholder

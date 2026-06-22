# Graph Generation Forensics Report

**Mission:** INITIATIVE-001A  
**Date:** 2026-06-22  
**Status:** COMPLETE  
**Method:** Direct repository evidence only. No estimates. No synthetic findings.

---

## Pre-Flight: File Inventory

| File | SHA | Size | Exists |
|---|---|---|---|
| `tools/build_graph.py` | `f84c8e008ad17ba2f357107f7df98fab2f80fa44` | 12,659 bytes (API) | ✅ YES |
| `.github/workflows/build-graph.yml` | `82a1afd03df5d10c3312b997b71c1fc42c300789` | 1,512 bytes (API) | ✅ YES |
| `data/SKILLS_GRAPH.json` | (21 bytes) | `SKILLS_GRAPH_PLACEHOLDER` string | ✅ EXISTS — but is a placeholder |
| `skills/01-perception/*.md` | Multiple files confirmed | 30 skill .md files in 01-perception alone | ✅ YES |
| `skills/01-perception/ocr.md` | `8432f883a55125099bd23102af4833be31aea136` | 7,179 bytes | ✅ YES — has valid YAML frontmatter |

**Category directories confirmed:** 17 categories (`01-perception` through `17-infrastructure`).

---

## Phase 1: Graph Builder Audit

### What `build_graph.py` expects

Source: `tools/build_graph.py` SHA `f84c8e008ad17ba2f357107f7df98fab2f80fa44`.

**Hardcoded paths (inside script):**
```
REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
DATA_DIR   = REPO_ROOT / "data"
META_DIR   = REPO_ROOT / "meta"
```

**Expected CLI interface (argparse, lines 168-173):**
```
python tools/build_graph.py
python tools/build_graph.py --dry-run
python tools/build_graph.py --output path
```
Only `--dry-run` and `--output` are defined. The script does NOT accept `--skills-root` or `--sbom-root`.

**Expected output path:**  
`data/SKILLS_GRAPH.json` (default) or custom path via `--output`.

**Input format required:**  
Markdown files with YAML frontmatter starting with `---`. The parser (`parse_frontmatter`) reads the first `---...---` block.

**Confirmed working input example:**  
`skills/01-perception/ocr.md` has valid frontmatter with `title`, `category`, `level`, `stability`, `version`, `added`. The parser would successfully produce a node from this file.

**When does the script produce placeholder output?**  
It does NOT produce placeholder output. It either:
- Writes a real graph (0+ nodes, 0+ edges) to `data/SKILLS_GRAPH.json`
- Exits with code 1 on validation errors (does not write)
- Crashes on an unhandled exception (does not write)

The placeholder `SKILLS_GRAPH_PLACEHOLDER` was written **manually** or by an initialization commit, not by the script.

---

## Phase 2: Input Discovery Audit

| Expected Input | Actual Input | Compatible? |
|---|---|---|
| `skills/NN-category/*.md` files | ✅ Confirmed present (30 files in `01-perception` alone, 17 categories) | ✅ YES |
| YAML frontmatter `---...---` block | ✅ Confirmed in `ocr.md` — valid `title`, `category`, `level`, `stability`, `version`, `added` | ✅ YES |
| Category dirs matching regex `^[0-9]{2}-` | ✅ All 17 dirs match (`01-perception` … `17-infrastructure`) | ✅ YES |
| `docs/sbom/` directory (workflow only) | UNKNOWN — not checked | N/A — script does not require it |
| `--skills-root` argument | ❌ NOT SUPPORTED by script | ❌ NO — argument not defined |
| `--sbom-root` argument | ❌ NOT SUPPORTED by script | ❌ NO — argument not defined |

**Finding:** The skill source files are valid and compatible with the script's actual parser. The script would successfully generate nodes if invoked correctly.

---

## Phase 3: Workflow Audit

Source: `.github/workflows/build-graph.yml` SHA `82a1afd03df5d10c3312b997b71c1fc42c300789`.

**Trigger:** `push` to `main` on paths `skills/**/*.md` or `docs/sbom/**`, plus `workflow_dispatch`.

**Execution command (lines 35-39):**
```yaml
run: |
  python tools/build_graph.py \
    --skills-root skills/ \
    --sbom-root docs/sbom/ \
    --output docs/api/graph.json
```

**Does CI actually execute `build_graph.py`?**  
**YES** — but with three fatal mismatches:

| Argument | In Workflow | In Script | Result |
|---|---|---|---|
| `--skills-root skills/` | ✅ passed | ❌ not defined in argparse | `argparse` error → **script exits with error before doing anything** |
| `--sbom-root docs/sbom/` | ✅ passed | ❌ not defined in argparse | same — unrecognized argument |
| `--output docs/api/graph.json` | ✅ passed | ✅ defined | would work if script reaches it |

**Output path mismatch:**

| | Value |
|---|---|
| Workflow writes to | `docs/api/graph.json` |
| Script default writes to | `data/SKILLS_GRAPH.json` |
| Commit step adds | `docs/api/graph.json` |
| Placeholder file location | `data/SKILLS_GRAPH.json` |

Even if the argument mismatch were fixed, the workflow writes to `docs/api/graph.json` while the placeholder lives at `data/SKILLS_GRAPH.json`. These are different files. The workflow would never overwrite the placeholder.

---

## Phase 4: Failure Reproduction

**Execution path trace:**

1. A commit touching `skills/**/*.md` is pushed to `main`.
2. Workflow `build-graph.yml` is triggered.
3. Python 3.11 installed. PyYAML and networkx installed.
4. `python tools/build_graph.py --skills-root skills/ --sbom-root docs/sbom/ --output docs/api/graph.json` is executed.
5. **FIRST POINT OF FAILURE:** Python argparse encounters `--skills-root` — an unrecognized argument. argparse calls `sys.exit(2)` with error message `error: unrecognized arguments: --skills-root skills/`.
6. Script exits with code 2. No graph is generated. No files are written.
7. GitHub Actions step reports failure.
8. Commit step is skipped (preceding step failed).
9. `data/SKILLS_GRAPH.json` remains `SKILLS_GRAPH_PLACEHOLDER`.

**Failure Classification:** `D — Workflow bug` (primary) + `E — Output path mismatch` (secondary)

**Exact evidence:**
- Script argparse block (lines 168-173 of `build_graph.py`): defines only `--dry-run` and `--output`.
- Workflow command (lines 35-39 of `build-graph.yml`): passes `--skills-root` and `--sbom-root`.
- These are mutually exclusive: the workflow invocation has never successfully executed the script.

---

## Phase 5: Remediation Plan

### Fix-1 — Align workflow to script (minimal risk)

**Files affected:** `.github/workflows/build-graph.yml` only  
**Change:** Replace the broken invocation:
```yaml
# CURRENT (broken)
python tools/build_graph.py \
  --skills-root skills/ \
  --sbom-root docs/sbom/ \
  --output docs/api/graph.json

# FIXED
python tools/build_graph.py \
  --output data/SKILLS_GRAPH.json
```
Also update the commit step to `git add data/SKILLS_GRAPH.json`.

**Risk level:** LOW — no script changes, only workflow alignment  
**Estimated scope:** 4 line changes in one YAML file  
**Rollback:** Revert the workflow commit

---

### Fix-2 — Add `--skills-root` and `--sbom-root` to script (script extension)

**Files affected:** `tools/build_graph.py`  
**Change:** Add the two arguments to argparse:
```python
parser.add_argument('--skills-root', default=str(SKILLS_DIR))
parser.add_argument('--sbom-root', default=None)  # optional, ignored if absent
```
Update `SKILLS_DIR` to use the argument value.

**Risk level:** LOW-MEDIUM — script change; requires test before merge  
**Estimated scope:** ~10 line changes in one Python file  
**Rollback:** Revert the script commit

---

### Fix-3 — Unified output path (aligns both to `data/`)

**Files affected:** `.github/workflows/build-graph.yml` AND `tools/build_graph.py`  
**Change:** Standardize on `data/SKILLS_GRAPH.json` everywhere. Remove the `docs/api/graph.json` reference from the workflow entirely.  

**Risk level:** MEDIUM — if other workflows or tooling depend on `docs/api/graph.json`, this breaks them  
**Estimated scope:** Changes to 2 files; requires audit of all workflow references first  
**Rollback:** Revert both file commits

---

## Phase 6: Decision

**RECOMMENDED_FIX: Fix-1**

Reason: The script is correct. The frontmatter is correct. The skill files are valid. Only the workflow invocation is wrong. Fix-1 is a 4-line change to one YAML file with no risk of introducing regressions in the script itself. It unblocks graph generation immediately.

Fix-2 is acceptable as an additive follow-on if `--skills-root` flexibility is needed for tooling. Fix-3 requires a separate audit first.

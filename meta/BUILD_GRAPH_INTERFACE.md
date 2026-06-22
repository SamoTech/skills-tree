# Build Graph Interface Documentation

**Mission:** INITIATIVE-001B — Phase 1  
**Date:** 2026-06-22  
**Evidence source:** Direct read of `tools/build_graph.py` and `.github/workflows/build-graph.yml`

---

## Script: `tools/build_graph.py`

### Argparse Arguments

| Argument | Type | Default | Required | Description |
|---|---|---|---|---|
| `--output` | `str` | `data/SKILLS_GRAPH.json` | No (has default) | Destination path for the generated JSON graph |
| `--dry-run` | `flag` | `False` | No | Parse and validate without writing output |

### Required Positional Arguments

**None.** The script has no required positional arguments.

### Required Environment Variables

**None detected.** The script reads the `skills/` directory relative to the working directory. No environment variables are consumed by the script.

### Output Parameter Definition

```
--output PATH
    Write the generated graph JSON to PATH.
    Default: data/SKILLS_GRAPH.json
    Type: str
    Required: False (default is used if omitted)
```

---

## Minimal Invocation Question

**Can `build_graph.py` execute successfully with only:**
```
python tools/build_graph.py --output data/SKILLS_GRAPH.json
```

**ANSWER: YES**

### Evidence

- `--output` is the only path argument the script recognizes.
- No positional arguments are required.
- No environment variables are required.
- The default value of `--output` is already `data/SKILLS_GRAPH.json`, meaning even bare invocation (`python tools/build_graph.py`) would succeed.
- The workflow was patched to use exactly this invocation.
- The graph was successfully generated on `2026-06-22T11:07:34Z` using this exact command, producing `367` nodes and `773` edges.

---

## Previous Interface (Pre-Fix — BROKEN)

```yaml
# Workflow invocation BEFORE INITIATIVE-001A fix:
python tools/build_graph.py \
  --skills-root skills/ \
  --sbom-root docs/sbom/ \
  --output docs/api/graph.json
```

The arguments `--skills-root` and `--sbom-root` are **not defined** in the script's argparse configuration. Python would exit with code 2 (`unrecognized arguments`) before any graph logic executed. This was the primary blocker identified in `GRAPH_GENERATION_ROOT_CAUSE.md`.

# Packaging Validation Report

Sprint: **packaging-fix** | Date: 2026-06-15

---

## Problem Summary

The original `pyproject.toml` used:

```toml
[tool.setuptools.package-data]
"*" = ["*.md", "*.json", "*.toml"]
```

`package-data` globs only match files **inside Python packages** (directories that contain an `__init__.py`). The runtime data files live in top-level non-package directories:

| File | Directory | Is a Python package? |
|---|---|---|
| `SKILLS_GRAPH.json` | `data/` | ❌ No `__init__.py` |
| `GOAL_TAXONOMY.md` | `meta/` | ❌ No `__init__.py` |
| `INDEX.json` | `benchmarks/` | ❌ No `__init__.py` |

Result: setuptools silently ignored these files. The wheel built successfully, but the installed package was missing its runtime data.

---

## Fix: What Changed

### 1. `MANIFEST.in` (added)

Controls sdist contents via `recursive-include` for `data/`, `benchmarks/`, `meta/`, `docs/`, `evaluation/`, `tests/`.

### 2. `pyproject.toml` — three targeted changes

**a) `include-package-data = true`**

```toml
[tool.setuptools]
include-package-data = true
```

**b) Auto-discovery via `packages.find`** (replaces hand-maintained list)

```toml
[tool.setuptools.packages.find]
where   = ["."]
exclude = ["tests*", "evaluation*", "docs*", "meta*", "benchmarks*", "assets*", "badges*"]
```

**c) `data-files` for the three runtime files that exist in the repo**

```toml
[tool.setuptools.data-files]
"data"       = ["data/SKILLS_GRAPH.json"]
"meta"       = ["meta/GOAL_TAXONOMY.md"]
"benchmarks" = ["benchmarks/INDEX.json"]
```

> **Note:** `meta/GOAL_TAXONOMY.json` was removed from this list because the file does not exist in the repository and is not referenced by any runtime code. Listing a non-existent file causes `python -m build` to fail with `error: can't copy '...': doesn't exist or not a regular file`.

### 3. `tools/data_resolver.py` (added)

Provides a `resolve("data", "SKILLS_GRAPH.json")` helper that locates data files correctly across editable installs, regular wheel installs, and containers. Supports `SKILLS_TREE_DATA_ROOT` env override.

---

## Build Verification

```bash
pip install build
python -m build
```

### Verify sdist

```bash
tar -tf dist/skills_tree-1.0.0.tar.gz | grep -E '(SKILLS_GRAPH|GOAL_TAXONOMY|INDEX)'
```

Expected:
```
skills_tree-1.0.0/data/SKILLS_GRAPH.json
skills_tree-1.0.0/meta/GOAL_TAXONOMY.md
skills_tree-1.0.0/benchmarks/INDEX.json
```

### Verify wheel

```bash
python -m zipfile -l dist/skills_tree-1.0.0-py3-none-any.whl | grep -E '(SKILLS_GRAPH|GOAL_TAXONOMY|INDEX)'
```

Expected:
```
data/SKILLS_GRAPH.json
meta/GOAL_TAXONOMY.md
benchmarks/INDEX.json
```

### Clean-install smoke test

```bash
python -m venv /tmp/st-test && source /tmp/st-test/bin/activate
pip install dist/skills_tree-1.0.0-py3-none-any.whl
python -c "
from tools.data_resolver import resolve
print(resolve('data', 'SKILLS_GRAPH.json'))
print(resolve('meta', 'GOAL_TAXONOMY.md'))
print(resolve('benchmarks', 'INDEX.json'))
"
skills-tree validate
```

---

## Shipped File Inventory (runtime data)

| File | Shipped in wheel |
|---|---|
| `data/SKILLS_GRAPH.json` | ✅ |
| `meta/GOAL_TAXONOMY.md` | ✅ |
| `benchmarks/INDEX.json` | ✅ |
| `meta/GOAL_TAXONOMY.json` | ❌ Does not exist — removed from manifest |

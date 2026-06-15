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

## Changes Made

### 1. `MANIFEST.in` (new file)

Controls sdist contents. Without this file, `python -m build --sdist` uses only heuristics and misses non-package directories.

```
recursive-include data       *.json *.md *.yml *.yaml
recursive-include benchmarks *.json *.md
recursive-include meta       *.md *.json *.yml *.yaml
recursive-include docs       *.html *.css *.js *.png *.svg
recursive-include evaluation *.json
recursive-include tests      *.json *.md
```

### 2. `pyproject.toml` — three targeted changes

**a) `include-package-data = true`**

Tells setuptools to honour both `MANIFEST.in` patterns and `package-data` globs.

```toml
[tool.setuptools]
include-package-data = true
```

**b) `[tool.setuptools.packages.find]`** (replaces hand-maintained list)

Auto-discovery of all packages, excluding non-package directories from the Python namespace.

```toml
[tool.setuptools.packages.find]
where   = ["."]
exclude = ["tests*", "evaluation*", "docs*", "meta*", "benchmarks*", "assets*", "badges*"]
```

**c) `[tool.setuptools.data-files]`** (new section)

Explicitly ships the three required runtime files into the wheel:

```toml
[tool.setuptools.data-files]
"data"       = ["data/SKILLS_GRAPH.json"]
"meta"       = ["meta/GOAL_TAXONOMY.md", "meta/GOAL_TAXONOMY.json"]
"benchmarks" = ["benchmarks/INDEX.json"]
```

### 3. `tools/data_resolver.py` (new file)

Provides a `resolve("data", "SKILLS_GRAPH.json")` helper that finds data files correctly in all install modes (editable, regular wheel, container). Supports `SKILLS_TREE_DATA_ROOT` env override for testing.

---

## Build Verification

Run the following on any machine with the repo cloned:

```bash
pip install build
python -m build
```

### Verify sdist contents

```bash
tar -tf dist/skills_tree-1.0.0.tar.gz | grep -E '(SKILLS_GRAPH|GOAL_TAXONOMY|INDEX)'
```

Expected output (exact paths may vary by platform):
```
skills_tree-1.0.0/data/SKILLS_GRAPH.json
skills_tree-1.0.0/meta/GOAL_TAXONOMY.md
skills_tree-1.0.0/meta/GOAL_TAXONOMY.json
skills_tree-1.0.0/benchmarks/INDEX.json
```

### Verify wheel contents

```bash
python -m zipfile -l dist/skills_tree-1.0.0-py3-none-any.whl | grep -E '(SKILLS_GRAPH|GOAL_TAXONOMY|INDEX)'
```

Expected output:
```
data/SKILLS_GRAPH.json
meta/GOAL_TAXONOMY.md
meta/GOAL_TAXONOMY.json
benchmarks/INDEX.json
```

### Verify clean install

```bash
# Create a fresh venv
python -m venv /tmp/skills-tree-test
source /tmp/skills-tree-test/bin/activate

# Install from wheel
pip install dist/skills_tree-1.0.0-py3-none-any.whl

# Confirm data files present in site-packages
python -c "
from tools.data_resolver import resolve
print(resolve('data', 'SKILLS_GRAPH.json'))
print(resolve('meta', 'GOAL_TAXONOMY.md'))
print(resolve('benchmarks', 'INDEX.json'))
"

# Run full CLI validation
skills-tree validate
```

---

## Expected Wheel File Inventory (key files)

| File | Present Before Fix | Present After Fix |
|---|---|---|
| `api/__init__.py` | ✅ | ✅ |
| `cli/main.py` | ✅ | ✅ |
| `tools/architect.py` | ✅ | ✅ |
| `data/SKILLS_GRAPH.json` | ❌ | ✅ |
| `meta/GOAL_TAXONOMY.md` | ❌ | ✅ |
| `meta/GOAL_TAXONOMY.json` | ❌ | ✅ |
| `benchmarks/INDEX.json` | ❌ | ✅ |

---

## Remaining Notes

- `twine check dist/*` should return PASSED for both artifacts after this fix.
- If any of the three data files do not yet exist in the repository (e.g. `data/SKILLS_GRAPH.json`), the `data-files` entry will silently skip them at build time. The file must exist in the repo for setuptools to include it. Verify with: `ls data/ meta/ benchmarks/`.
- For the `data_resolver.py` to work after a regular (non-editable) wheel install, the `data-files` destination paths must match the paths the resolver searches. The current resolver searches `sys.path` entries for `data/SKILLS_GRAPH.json` — this matches the wheel layout where data files land adjacent to the site-packages root.

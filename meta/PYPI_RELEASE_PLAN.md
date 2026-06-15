# Architect PyPI Release Plan

Sprint: **C-11**

---

## Package Structure

```
skills-tree/
├── api/                     # FastAPI service layer (C-09)
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── dependencies.py
│   └── routes/
│       ├── health.py
│       ├── goals.py
│       ├── skills.py
│       ├── recommend.py
│       └── blueprint.py
├── cli/                     # CLI layer (C-11)  ← new
│   ├── __init__.py
│   └── main.py
├── mcp/                     # MCP server layer (C-10)
│   ├── __init__.py
│   ├── server.py
│   └── tools.py
├── tools/                   # Engine layer (C-01 – C-08)
│   ├── architect.py
│   └── ranking_calibrator.py
├── pyproject.toml           # Package manifest (C-11)  ← new
├── README.md
└── LICENSE
```

The installable distributions ships four namespaces: `api`, `cli`, `mcp`, `tools`.
Data files (`*.md`, `*.json`) bundled via `package-data` in `pyproject.toml`.

---

## Versioning

Architect follows **Semantic Versioning 2.0** (`MAJOR.MINOR.PATCH`).

| Component | Meaning |
|---|---|
| `MAJOR` | Breaking API or CLI contract changes |
| `MINOR` | New commands, endpoints, or MCP tools (backwards-compatible) |
| `PATCH` | Bug fixes, calibration tweaks, doc updates |

Current version: **`1.0.0`** (set in `pyproject.toml`).

Version is the single source of truth — mirrored into the API `/health` response via `version` field in `api/routes/health.py`.

---

## Release Workflow

### 1. Pre-release checklist

```bash
# Run full test suite
pytest tests/ -v

# Validate CLI end-to-end
pip install -e .
skills-tree validate
skills-tree recommend --goal "Coding Agent"

# Confirm version bump
grep version pyproject.toml
```

### 2. Build distributions

```bash
pip install build
python -m build
# produces:
#   dist/skills_tree-1.0.0.tar.gz        (sdist)
#   dist/skills_tree-1.0.0-py3-none-any.whl (wheel)
```

### 3. Publish to TestPyPI (staging)

```bash
pip install twine
twine upload --repository testpypi dist/*
# Verify:
pip install -i https://test.pypi.org/simple/ skills-tree==1.0.0
skills-tree --help
```

### 4. Publish to PyPI (production)

```bash
twine upload dist/*
```

CI publishing via GitHub Actions (`.github/workflows/publish.yml`) using the `PYPI_API_TOKEN` repository secret.

---

## PyPI Publishing

### GitHub Actions workflow

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI
on:
  push:
    tags: ['v*.*.*']
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install build twine
      - run: python -m build
      - run: twine upload dist/*
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

### Trusted Publisher (recommended)

Configure PyPI Trusted Publisher (OIDC) at `pypi.org/manage/account/publishing/`
to remove the need for a long-lived `PYPI_API_TOKEN`:

- **Owner:** SamoTech
- **Repository:** skills-tree
- **Workflow:** `publish.yml`
- **Environment:** `pypi`

---

## Install Command

```bash
# From PyPI (once published)
pip install skills-tree

# Development install from source
git clone https://github.com/SamoTech/skills-tree
cd skills-tree
pip install -e .[dev]

# Verify
skills-tree --help
skills-tree validate
```

---

## Upgrade Strategy

```bash
# Check current version
pip show skills-tree

# Upgrade
pip install --upgrade skills-tree

# Pin to major version (for stability)
pip install "skills-tree>=1.0,<2.0"
```

### Deprecation policy

- CLI flags: deprecated in a `MINOR` release, removed in the next `MAJOR`.
- API endpoints: versioned under `/v1/` path prefix starting from `v2.0.0`.
- MCP tool contracts: tool `name` field is stable; `input_schema` changes follow minor versioning.

---

## Package Size Estimate

| Component | Size (approx) |
|---|---|
| Source code (`.py`) | ~85 KB |
| Meta / data files (`.md`, `.json`) | ~450 KB |
| **sdist total** | ~535 KB |
| **wheel total** | ~95 KB |

---

## Post-release Validation

```bash
pip install skills-tree==1.0.0
skills-tree validate
skills-tree recommend --goal "Coding Agent"
```

Expected output for `recommend`:
```json
{
  "goal": "Coding Agent",
  "goal_id": "G01",
  "confidence_score": 0.86,
  "required_skills": [...],
  "optional_skills": [...],
  "learning_path": [...],
  "calibration_applied": true
}
```

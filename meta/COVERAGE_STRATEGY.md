# Coverage Strategy

> Current state, uncovered modules, and roadmap to 90%+ test coverage.

## Current State

| Module | Current Coverage | Target | Status |
|---|---|---|---|
| `cli/` | ~40% | 80% | 🟡 In progress |
| `api/` | ~50% | 85% | 🟡 In progress |
| `tools/` | ~30% | 70% | 🔴 Needs work |
| `mcp/` | ~20% | 75% | 🔴 Needs work |
| Overall | **~35%** | **70%** (CI gate) | 🔴 Below gate |

> Note: The 70% CI gate is enforced via `pytest --cov-fail-under=70`. PRs that drop coverage below 70% will fail.

## Uncovered Modules

### Priority 1 — Core API (`api/`)
The Python API is the primary programmatic interface and must be well-covered:
- `SkillsTree.search()` — missing edge case tests (empty query, special characters, no results)
- `SkillsTree.get()` — missing `SkillNotFound` exception test
- `SkillsTree.recommend()` — no tests at all
- `SkillsTree.get_category()` — missing invalid category test

### Priority 2 — CLI (`cli/`)
CLI coverage requires testing Typer commands with `typer.testing.CliRunner`:
- `skills-tree search` — partial coverage
- `skills-tree show` — missing `--format json` and `--format yaml` tests
- `skills-tree mcp serve` — no tests
- `skills-tree categories` — no tests

### Priority 3 — Validation Tools (`tools/`)
- `check_skill_quality.py` — needs schema validation tests
- `update_readme_counts.py` — no tests
- `build_search_index.py` — no tests

### Priority 4 — MCP Server (`mcp/`)
- All endpoints untested
- Integration tests needed

## Roadmap to 90%+

### Phase A — Reach 70% (Current Sprint)
Focus on `api/` and `cli/` core paths. This is the minimum bar for production confidence.

**Estimated effort:** 2-3 days  
**Target date:** Next minor release

### Phase B — Reach 80%
Add edge case tests for all public API methods. Add CLI option coverage.

**Estimated effort:** 1 week

### Phase C — Reach 90%+
Add integration tests for MCP server. Add property-based tests for schema validation.

**Estimated effort:** 2 weeks

## How to Run Coverage Locally

```bash
pip install pytest pytest-cov
pytest tests/ --cov=. --cov-report=html --cov-report=term-missing
# Open htmlcov/index.html to see per-file coverage
```

## Contributing Tests

Tests that increase coverage are always welcome! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.
Test files go in `tests/` and follow the naming convention `test_{module}.py`.

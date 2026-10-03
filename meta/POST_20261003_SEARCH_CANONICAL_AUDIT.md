# Search Canonical Implementation Audit — 2026-10-03

## Objective

Determine whether the documented `SkillsTree.search()` / `skills-tree search` capability has an existing canonical implementation that can be reused without creating a parallel search system.

## Findings

### 1. Historical Python API is not present

Repository search on `main` found documentation and examples referencing `skills_tree.SkillsTree`, including `SkillsTree.search()`, but did not identify an implementation module or package directory defining that class.

The current `pyproject.toml` exposes the console entry point `skills-tree = "cli.main:app"`. The current CLI implementation is in `cli/main.py` and contains five commands: `recommend`, `blueprint`, `goals`, `skills`, and `validate`.

Conclusion: the documented `SkillsTree` Python API is stale/legacy documentation, not a verified current runtime capability.

### 2. Search does have a concrete canonical implementation

The verified search pipeline is:

```
skills/**/*.md
      |
      v
tools/build_search_index.py
      |
      v
docs/search-index.json
      |
      v
static web client search
```

`tools/build_search_index.py` parses skill frontmatter and body content and produces the generated JSON search corpus.

`.github/workflows/generate-search-index.yml` invokes that builder when canonical skill content changes.

The repository architecture and README describe this generated search index as the search layer.

### 3. CLI search is not implemented

`docs/cli.md` previously documented `skills-tree search`, but `cli/main.py` has no corresponding command.

Issue #86 is therefore still valid as an implementation gap.

### 4. No parallel implementation should be introduced

The audit does not justify creating a second index, a second parser, or an independent ranking system for the CLI.

A future CLI search implementation should first establish a reusable runtime boundary around the existing generated/canonical search data, with explicit schema, deterministic behavior, tests, and packaging/runtime evidence.

## Documentation action

The stale Python API and CLI documentation were corrected in the accompanying documentation change. The repository now explicitly distinguishes:

- verified current runtime interfaces;
- the canonical web search-index pipeline;
- historical/unimplemented Python API claims;
- the open CLI search implementation gap.

## Evidence boundary

This audit establishes repository evidence only. It does not claim that the public PyPI artifact, historical releases, or external deployments lack the `SkillsTree` API. Those external states require separate artifact/runtime verification and are not used as evidence for the current repository implementation.

## Next engineering action

Before implementing issue #86, define the canonical runtime contract for consuming `docs/search-index.json` or another repository-native search source. Then add behavior and regression tests before exposing it through the CLI.

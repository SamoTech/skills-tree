# CLI Reference

Skills Tree currently ships a Typer CLI implemented in `cli/main.py`.

## Installation from the repository

The repository currently supports local installation through the project packaging configuration:

```bash
pip install -e .
```

The current CLI surface is the following.

## `skills-tree recommend`

Get skill recommendations for a goal.

```bash
skills-tree recommend --goal "Coding Agent"
skills-tree recommend --goal "RAG Assistant" --experience intermediate --time-budget 80
```

## `skills-tree blueprint`

Generate an architecture blueprint for a goal.

```bash
skills-tree blueprint --goal "Coding Agent"
```

## `skills-tree goals`

List taxonomy goals.

```bash
skills-tree goals
```

## `skills-tree skills`

List graph skills.

```bash
skills-tree skills
```

## `skills-tree validate`

Run CLI/API health checks, with optional goal-specific recommendation and blueprint validation.

```bash
skills-tree validate
skills-tree validate --goal "Coding Agent"
```

## Search status

`skills-tree search` is not currently implemented in `cli/main.py`.

The repository does have a canonical search-index generation pipeline in `tools/build_search_index.py` and `.github/workflows/generate-search-index.yml`. The generated `docs/search-index.json` is used by the static web experience.

Issue #86 tracks the CLI search implementation gap. A future CLI command must reuse the existing canonical search/data layer rather than introducing a parallel index or ranking implementation. The remaining design work is the deterministic query/ranking contract, not another data source.

## Output formats

The implemented commands support the formats documented by their source options: `json`, `pretty`, and `table` where applicable.

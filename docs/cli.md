# CLI Reference

Skills Tree currently ships a Typer CLI implemented in `cli/main.py`.

## Installation from the repository

The repository currently supports local installation through the project packaging configuration:

~~~bash
pip install -e .
~~~

The current CLI surface is the following.

## `skills-tree search`

Searches the canonical generated skill corpus with deterministic lexical ranking.

~~~bash
skills-tree search "memory injection"
skills-tree search "vision" --limit 10 --format table
~~~

The command consumes `data/search-index.json` through `cli/search_runtime.py`; it does not build a second index or parse Markdown at runtime. Ranking and tie-breaking are defined in [`meta/SEARCH_CLI_CONTRACT.md`](https://github.com/SamoTech/skills-tree/blob/main/meta/SEARCH_CLI_CONTRACT.md).

## `skills-tree recommend`

Get skill recommendations for a goal.

~~~bash
skills-tree recommend --goal "Coding Agent"
skills-tree recommend --goal "RAG Assistant" --experience intermediate --time-budget 80
~~~

## `skills-tree blueprint`

Generate an architecture blueprint for a goal.

~~~bash
skills-tree blueprint --goal "Coding Agent"
~~~

## `skills-tree goals`

List taxonomy goals.

~~~bash
skills-tree goals
~~~

## `skills-tree skills`

List graph skills.

~~~bash
skills-tree skills
~~~

## `skills-tree validate`

Run CLI/API health checks, with optional goal-specific recommendation and blueprint validation.

~~~bash
skills-tree validate
skills-tree validate --goal "Coding Agent"
~~~

## Search implementation status

`skills-tree search` is implemented in `cli/main.py` and consumes the existing generated search projection through `cli/search_runtime.py`.

The canonical generation pipeline remains `skills/**/*.md` → `tools/build_search_index.py` → identical `docs/search-index.json` and `data/search-index.json` projections. Runtime search does not create another index or parse Markdown.

Issue #86 is therefore an implemented CLI consumer. Its deterministic tokenization, field weights, ranking, tie-breaking, and output contract are defined in [`meta/SEARCH_CLI_CONTRACT.md`](https://github.com/SamoTech/skills-tree/blob/main/meta/SEARCH_CLI_CONTRACT.md).

## Output formats

The implemented commands support the formats documented by their source options: `json`, `pretty`, and `table` where applicable.

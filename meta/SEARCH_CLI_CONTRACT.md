# CLI Search Query and Ranking Contract

Status: VERIFIED ON MAIN — PR #299 merged as `7302d0780b2857bdd2f54363a2e6158eafc45292`; installable search-runtime verification is complete.

Issue #86 is implemented against the existing generated search projection. The CLI does not build a second index and does not parse canonical Markdown.

## Source boundary

`cli.search_runtime.load_search_index()` loads the generated `data/search-index.json` projection. That file is byte-identical to `docs/search-index.json`, which is generated from canonical `skills/**/*.md` by `tools/build_search_index.py`.

## Query tokenization

- Unicode word tokens are extracted with Python's Unicode-aware `\\w+` regular expression.
- Tokens are case-folded.
- Punctuation and whitespace are separators.
- Repeated query tokens do not increase a document's score.
- A query with no word tokens is a user error.

## Matching fields and weights

Each distinct query token contributes at most once to each field when that token is present:

| Field | Weight |
| --- | ---: |
| title | 8 |
| tags | 6 |
| category | 4 |
| description | 3 |
| body | 1 |

The score is the sum of matched-token weights across fields. This is a deterministic lexical ranking contract, not a quality or trust score.

The search uses OR semantics: a document is returned when at least one query token matches at least one indexed field.

## Tie-breaking

Results are sorted by:

1. descending numeric score;
2. case-folded title ascending;
3. canonical skill ID ascending.

No source-order, hash-order, timestamp, or runtime-dependent ordering is used.

## CLI output

`skills-tree search "<query>"` returns a JSON array by default. Each result contains:

- `id`
- `title`
- `category`
- `level`
- `stability`
- `description`
- `score`

`--limit/-n` defaults to 20 and accepts 1 through 100.

`--format/-f` supports the existing CLI output modes: `json`, `pretty`, and `table`.

No-results is a successful invocation returning an empty result array.

## Non-goals

This contract does not introduce:

- a second index format;
- Markdown parsing at runtime;
- embeddings or semantic search;
- a trust/quality score;
- fuzzy matching;
- query expansion;
- undocumented filters.

Those require separate evidence and contracts.

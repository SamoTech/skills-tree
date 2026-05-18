# badges/ — Deprecated

> **This directory is no longer active.**

Badge JSON files are generated and served from **`docs/badges/`**, not here.

All CI workflows (`sync-badges.yml`, `ast-sweep.yml`, `revoke-phantom-badges.yml`, `osv-watch.yml`) write exclusively to `docs/badges/`.

This directory exists only because it was created before the `docs/` restructure. It will be removed in a future cleanup PR. Do not add files here.

## Live badge location

```
docs/badges/<category>-<skill-name>.json
```

See [meta/badge-states.md](../meta/badge-states.md) for the full badge lifecycle documentation.

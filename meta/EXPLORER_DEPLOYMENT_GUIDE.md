# Explorer Deployment Guide

**Initiative:** INITIATIVE-012B  

## Live URL

```
https://samotech.github.io/skills-tree/explorer/
```

## Deep Link Format

```
https://samotech.github.io/skills-tree/explorer/?skill=09-agentic-patterns/react
https://samotech.github.io/skills-tree/explorer/?skill=02-reasoning/chain-of-thought
```

## Deployment Trigger

The GitHub Actions workflow `.github/workflows/deploy-explorer.yml` deploys automatically on:
- Any push to `main` that touches `docs/explorer/**` or `data/SKILLS_GRAPH.json`
- Manual trigger via `workflow_dispatch`

## Local Development

```bash
# From repository root:
python3 -m http.server 8000
# Open: http://localhost:8000/docs/explorer/
```

The Explorer reads `../../data/SKILLS_GRAPH.json` (relative to `docs/explorer/`), which resolves to `data/SKILLS_GRAPH.json` from the repo root.

## GitHub Pages Setup (one-time)

1. Go to **Settings → Pages**
2. Set **Source** to `GitHub Actions`
3. Push any change to trigger the workflow

## Graph Data Contract

The Explorer reads `data/SKILLS_GRAPH.json` and expects:

```json
{
  "meta": { "schema_version": "3.1", "node_count": N, "edge_count": N, "requires_count": N },
  "nodes": [ { "id", "title", "category", "level", "stability", "version", "layer", "added", "tags", "prerequisites", "related_skills", "source_file" } ],
  "edges": [ { "source", "target", "type" } ]
}
```

If `schema_version` changes, update the pre-flight check in `app.js`.

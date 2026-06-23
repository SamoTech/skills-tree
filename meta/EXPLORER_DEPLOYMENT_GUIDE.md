# EXPLORER DEPLOYMENT GUIDE

**Initiative:** INITIATIVE-012B  
**Target:** GitHub Pages  
**URL pattern:** `https://samotech.github.io/skills-tree/explorer/`

---

## Prerequisites

1. GitHub Pages must be enabled on the repository
2. Source: **GitHub Actions** (not branch deploy)
3. Workflow file: `.github/workflows/deploy-explorer.yml`

## Enable GitHub Pages

```
Repository → Settings → Pages
  Source: GitHub Actions
```

## Trigger Deployment

Deployment triggers automatically on:
- Any push to `main` that changes `docs/explorer/**` or `data/SKILLS_GRAPH.json`
- Manual trigger via Actions → Deploy Explorer → Run workflow

## Explorer URL

```
https://samotech.github.io/skills-tree/explorer/
```

## Deep Link Format

```
https://samotech.github.io/skills-tree/explorer/?skill=09-agentic-patterns/react
https://samotech.github.io/skills-tree/explorer/?skill=02-reasoning/chain-of-thought
https://samotech.github.io/skills-tree/explorer/?skill=05-code/code-generation
```

## Data Source

The Explorer reads `data/SKILLS_GRAPH.json` via:
```
../../data/SKILLS_GRAPH.json  (relative from docs/explorer/)
```

This resolves correctly under GitHub Pages when the site root is `/skills-tree/`.

## Local Development

```bash
# From repo root:
python3 -m http.server 8000
# Then open: http://localhost:8000/docs/explorer/
```

## Updating the Graph

When `data/SKILLS_GRAPH.json` is updated, the Explorer automatically reflects the new data on next page load — no rebuild required.

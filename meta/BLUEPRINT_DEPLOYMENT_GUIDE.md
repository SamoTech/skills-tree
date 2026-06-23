# BLUEPRINT GENERATOR DEPLOYMENT GUIDE
> Initiative: INITIATIVE-012C

## Live URL

```
https://samotech.github.io/skills-tree/blueprints/
```

## Activation

1. Go to **Settings → Pages → Source → GitHub Actions**
2. Push any change to `docs/blueprints/**` or `data/SKILLS_GRAPH.json`
3. GitHub Actions runs `deploy-blueprints.yml` automatically
4. Live within ~60 seconds of push

## Deep Link Format

```
/blueprints/?goal=<goal-id>
```

Examples:
```
/blueprints/?goal=rag-assistant
/blueprints/?goal=customer-support-agent
/blueprints/?goal=coding-agent
/blueprints/?goal=multi-agent-team
```

## Data Source

```
../../data/SKILLS_GRAPH.json
```

Blueprint Generator reads directly from the repository graph.
No backend. No API calls. No authentication.

## Local Development

```bash
# From repo root:
python3 -m http.server 8000
# Open: http://localhost:8000/docs/blueprints/
```

## Adding New Goals

1. Edit `meta/BLUEPRINT_GOAL_CATALOG.md`
2. Add goal entry to `GOALS` array in `docs/blueprints/app.js`
3. Commit and push → auto-deploys

## Export Formats

- **JSON**: Full Blueprint object, downloadable as `.json`
- **Markdown**: Human-readable learning plan, downloadable as `.md`

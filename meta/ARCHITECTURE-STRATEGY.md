# Architecture Strategy — Skills Tree v3.0

> Technical architecture for the global AI knowledge platform.

---

## Architecture Principles

1. **Git as the database** — The repository IS the source of truth. All structured data is generated FROM the Markdown + YAML frontmatter, not stored separately.
2. **Static-first** — Everything runs as a static site. No servers required for the core product. Zero hosting cost for the community.
3. **API as a side effect** — The structured data exports (JSON/YAML) are the API. Serve them from CDN. No backend needed.
4. **Progressive enhancement** — Base experience works without JavaScript. Graph and search are enhancements.
5. **Zero vendor lock-in** — Every format is open. Every tool is replaceable. The data outlives the tooling.

---

## System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    GITHUB REPOSITORY                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Markdown    │  │ YAML Front- │  │ Schema Files        │  │
│  │ Skill Files │  │ matter      │  │ (validation)        │  │
│  └──────┬──────┘  └──────┬──────┘  └─────────────────────┘  │
│         └────────────────┘                                    │
│                  ↓ (CI/CD Pipeline)                           │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │               BUILD PIPELINE (GitHub Actions)           │  │
│  │  validate → extract → transform → generate → deploy    │  │
│  └─────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────────┐
│                    STATIC ARTIFACTS                           │
│  ┌────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │ data/*.json│  │ search-index │  │  graph.json        │   │
│  │ data/*.yaml│  │ .json        │  │  (D3 / Cytoscape)  │   │
│  └────────────┘  └──────────────┘  └────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────────┐
│                  DELIVERY LAYER                               │
│  ┌─────────────────────┐  ┌────────────────────────────────┐ │
│  │  GitHub Pages       │  │  jsDelivr CDN (raw JSON/YAML)  │ │
│  │  (static site)      │  │  (API endpoint)                │ │
│  └─────────────────────┘  └────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

---

## The "API Without a Server" Pattern

Skills Tree provides a free public API by serving structured JSON files from GitHub/jsDelivr CDN:

```
https://cdn.jsdelivr.net/gh/SamoTech/skills-tree@main/data/skills.json
https://cdn.jsdelivr.net/gh/SamoTech/skills-tree@main/data/knowledge-graph.json
https://cdn.jsdelivr.net/gh/SamoTech/skills-tree@main/data/mcp-tools.json
```

This is:
- **Free** — jsDelivr is free for open source
- **Fast** — Global CDN with 99.9% uptime
- **Versioned** — Pin to `@v2.0.0` tag for stability
- **Zero infrastructure** — No servers, no databases, no bills

For full REST/GraphQL API (Phase 2), deploy to Vercel/Cloudflare Workers with read-only DB:

```
GET /api/v1/skills                    ← List all skills
GET /api/v1/skills/:id                ← Get skill by ID
GET /api/v1/skills/search?q=:query    ← Search skills
GET /api/v1/mcp-tools                 ← List MCP tools
GET /api/v1/graph                     ← Full knowledge graph
GET /api/v1/paths                     ← Learning paths
GET /api/v1/benchmarks                ← Benchmark results
GET /api/v1/agent-builder?goal=:text  ← Agent builder (AI-powered)
```

---

## Search Architecture

### Phase 1: Client-side Fuse.js (immediate)
```javascript
// Load JSON index, instantiate Fuse, search in-browser
import Fuse from 'fuse.js';
const skills = await fetch('/data/index.json').then(r => r.json());
const fuse = new Fuse(skills, {
  keys: ['name', 'description', 'tags', 'category.name', 'use_cases'],
  threshold: 0.3,
  includeScore: true
});
```

### Phase 2: Pagefind (static, no server)
```bash
npx pagefind --source docs --bundle-output docs/pagefind
```
Pagefind runs at build time, creates a static search index deployed with the site. Zero server cost.

### Phase 3: Semantic search (future)
Embed skill descriptions using `text-embedding-3-small`. Store in static JSON. Browser-side cosine similarity for semantic matching.

---

## Knowledge Graph Rendering

### Technology Choice: D3.js Force-Directed Graph

Reasoning:
- Runs entirely client-side
- No server required
- Highly customizable
- Powers the most impressive open-source graph visualizations
- Community understands it

```javascript
// Force simulation config
const simulation = d3.forceSimulation(nodes)
  .force('link', d3.forceLink(edges).id(d => d.id).strength(d => d.strength))
  .force('charge', d3.forceManyBody().strength(-300))
  .force('center', d3.forceCenter(width / 2, height / 2))
  .force('collision', d3.forceCollide().radius(30));

// Node color by category
const colorScale = d3.scaleOrdinal()
  .domain(categories)
  .range(categoryColors);
```

### Alternative: Cytoscape.js for richer interaction
Cytoscape.js is better for:
- Complex layouts (hierarchical, concentric)
- Rich event handling
- Export to image
- Plugin ecosystem

---

## Build Pipeline

### `tools/build-data.py`
Runs on every PR merge and nightly:
1. Parse all Markdown files with YAML frontmatter
2. Validate against JSON Schema
3. Generate `data/skills.json`
4. Generate `data/index.json` (lightweight for search)
5. Generate `data/knowledge-graph.json` (from `related_skills` + `required_skills`)
6. Generate `data/mcp-tools.json`
7. Update `meta/QUALITY-REPORT.md`
8. Update README skill counts

### GitHub Actions Triggers
```yaml
# .github/workflows/build-data.yml
on:
  push:
    branches: [main]
    paths: ['skills/**', 'schema/**']
  schedule:
    - cron: '0 0 * * *'  # Nightly
  workflow_dispatch:
```

---

## MCP Explorer Architecture

### Data Source Strategy
MCP tools are catalogued in `mcp/` directory:
```
mcp/
├── servers/
│   ├── brave-search.yaml
│   ├── github-mcp.yaml
│   ├── filesystem.yaml
│   └── ...
├── clients/
│   ├── claude-desktop.yaml
│   ├── cursor.yaml
│   └── ...
├── patterns/
│   ├── tool-composition.md
│   ├── multi-server.md
│   └── ...
└── index.yaml              ← Master MCP catalogue
```

### Auto-sync from modelcontextprotocol/servers
Weekly GitHub Action pulls from the official MCP registry and updates our catalogue:
```yaml
- name: Sync MCP registry
  run: python3 tools/sync-mcp-registry.py
```

---

## Agent Engineering Platform Architecture

Dedicated section structure:
```
agent-engineering/
├── architectures/
│   ├── single-agent.md
│   ├── multi-agent-sequential.md
│   ├── multi-agent-parallel.md
│   ├── multi-agent-hierarchical.md
│   ├── supervisor-worker.md
│   └── swarm.md
├── memory-systems/
│   ├── overview.md
│   ├── working-memory.md
│   ├── episodic-memory.md
│   ├── semantic-memory.md
│   └── vector-memory.md
├── tool-calling/
│   ├── overview.md
│   ├── function-calling.md
│   ├── mcp-integration.md
│   └── tool-selection.md
├── evaluation/
│   ├── overview.md
│   ├── trajectory-evaluation.md
│   ├── tool-use-accuracy.md
│   └── end-to-end-benchmarks.md
└── planning/
    ├── overview.md
    ├── react-loop.md
    ├── plan-execute.md
    └── lats.md
```

---

*Version: 1.0 — June 2026*

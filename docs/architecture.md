# Architecture

Skills Tree is a layered, evidence-backed registry. Canonical Markdown under skills/ is the source of truth; build and validation tools produce deterministic machine-readable projections; the CLI, static documentation UI, external agents, and Agent Skills consumers read those projections. See Python API Status (api.md) for the verified boundary: the historical skills_tree.SkillsTree API is not a current verified capability.

## System Layers

```
Canonical sources
  skills/  |  systems/  |  blueprints/  |  benchmarks/
                       |
                       v
Build, validation, and evidence gates
  tools/  |  tests/  |  .github/workflows/
                       |
                       v
Generated projections (not independent sources)
  docs/api/skills.json  |  graph.json  |  search indexes
  agent-skills/         |  Agent Skills discovery index
                       |
                       v
Consumers
  skills-tree CLI  |  static docs/explorer  |  external agents
```

The graph and search projections are generated artifacts. skills/ remains canonical; consumers must not create competing catalogs or indexers. The CLI search runtime consumes the generated search projection.

## Repository Structure

```
skills-tree/
├── skills/               # 381 public canonical skills (382 quality files including one sandbox fixture)
│   ├── 01-perception/
│   ├── 02-reasoning/
│   ├── 03-memory/
│   ├── 04-action-execution/
│   ├── 05-code/
│   ├── 06-communication/
│   ├── 07-tool-use/
│   ├── 08-multimodal/
│   ├── 09-agentic-patterns/
│   ├── 10-computer-use/
│   ├── 11-web/
│   ├── 12-data/
│   ├── 13-creative/
│   ├── 14-security/
│   ├── 15-orchestration/
│   ├── 16-domain-specific/
│   └── 17-infrastructure/
├── systems/              # Multi-skill workflow definitions
├── blueprints/           # Production architecture templates
├── benchmarks/           # Reproducible skill comparisons
├── labs/                 # Experimental capabilities
├── mcp/                  # MCP server implementation
├── cli/                  # CLI entry points (Typer)
├── api/                  # API-related modules; see docs/api.md for verified status
├── tools/                # Validation & build scripts
├── tests/                # pytest test suite
├── docs/                 # Documentation site (MkDocs + custom UI)
├── meta/                 # Schema, glossary, roadmap, changelog
├── i18n/                 # Localized READMEs (10 languages)
└── .github/              # CI/CD workflows, templates, Dependabot
```

## The Skill Schema

Every skill file follows a validated frontmatter schema:

```yaml
---
title: Retrieval-Augmented Generation
category: memory
level: intermediate         # beginner | intermediate | advanced
stability: stable           # experimental | beta | stable
version: v3
badge: verified             # verified | reviewed | stub
tags: [retrieval, generation, grounding]
related: [vector-store-retrieval, memory-injection, embedding-generation]
---
```

## Versioning Model

Skills evolve through three maturity stages:

| Version | Criteria | Status |
|---|---|---|
| **v1** | Description + minimal example | Stub |
| **v2** | Enriched: failure modes + typed I/O + frameworks | Reviewed |
| **v3** | Battle-tested: benchmarks + model comparison + production notes | Verified |

## CI/CD Pipeline

```
Push to main branch
       ↓
validate-skills.yml    → Schema validation + quality scoring
test.yml               → pytest + coverage report
docs-deploy.yml        → MkDocs build + GitHub Pages deploy
update-skill-count.yml → README badge sync
semantic-release.yml   → Version bump + PyPI publish (OIDC)
```

## Data Flow

1. A contributor adds or modifies a skill Markdown file.
2. CI validates the schema, checks links, and scores quality.
3. On merge to `main`, semantic-release determines the version bump.
4. The package is published to PyPI via OIDC trusted publishing (no stored secrets).
5. MkDocs rebuilds the documentation site and deploys to GitHub Pages.
6. The search index is regenerated and embedded in the static site.

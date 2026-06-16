# Architecture

Skills Tree is designed as a layered system: a human-readable data layer (Markdown files), a validation and tooling layer (Python scripts), and a programmatic access layer (CLI + Python API + MCP server).

## System Layers

```
┌─────────────────────────────────────────────────────────┐
│                  Consumers                              │
│  CLI (Typer)  │  Python API  │  MCP Server  │  Docs UI  │
├──────────────┴─────────────┴─────────────┴────────┤
│              SkillsTree Python Package                  │
│  search()  │  get()  │  categories()  │  recommend()  │
├─────────────────────────────────────────────────────────┤
│              Skills Data Layer                          │
│  skills/  │  systems/  │  blueprints/  │  benchmarks/ │
├─────────────────────────────────────────────────────────┤
│  Validation & Tooling (tools/, .github/workflows/)      │
│  Quality scoring │ Schema validation │ Search indexing │
└─────────────────────────────────────────────────────────┘
```

## Repository Structure

```
skills-tree/
├── skills/               # 360 atomic skill files
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
├── api/                  # Python API module
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

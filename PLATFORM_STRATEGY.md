# Skills Tree — Platform Strategy

> The full product, architecture, and community strategy for transforming Skills Tree into the world's definitive AI knowledge platform.

---

## SWOT Analysis

### Strengths
- **361 skills already indexed** — the largest structured AI capability taxonomy in the open-source ecosystem
- **Battle-tested quality signal** — 51 production-ready skills with real code, benchmarks, and failure modes
- **Strong information architecture** — 17 categories, versioning system, quality tiers
- **Internationalization** — 10 languages already shipped
- **CI/CD automation** — GitHub Actions workflows for validation, counts, and changelog
- **Clear contribution model** — templates, PR format rules, quality gates
- **Existing community hooks** — CONTRIBUTING.md, issue templates, weekly highlights

### Weaknesses
- **308 stubs (85%)** — vast majority of content is placeholder-quality
- **No interactive discovery** — browsing is entirely README/file-tree based
- **No search** — zero search capability beyond `grep`
- **No machine-readable export** — no JSON/YAML API, no structured data layer
- **No MCP coverage** — the fastest-growing AI tool category is absent
- **No visual knowledge graph** — relationships exist in links but aren't navigable visually
- **No contributor reputation system** — no incentive beyond goodwill
- **GitHub Pages UI is not documented** as a distinct product surface
- **No sponsorship infrastructure** that scales beyond a single SPONSORS.md file

### Opportunities
- **MCP explosion** — 2,000+ MCP servers exist with zero canonical index. First-mover advantage is enormous.
- **Agent engineering as discipline** — the field is maturing; it needs MDN-equivalent reference material
- **Public API** — no open API exists for AI capability data. Skills Tree can own this space.
- **Framework integrations** — LangChain, CrewAI, AutoGen could embed Skills Tree data
- **Conference circuit** — NeurIPS, ICLR, AI Engineer World's Fair are underserved by open-source tooling content
- **Corporate adoption** — enterprises building internal AI platforms need structured capability taxonomies
- **Academic citation** — structured taxonomy with stable URLs becomes citable infrastructure

### Threats
- **OpenAI / Anthropic documentation** — could build a competing canonical reference
- **LangChain Hub** — already has a head start on prompt/chain sharing
- **Hugging Face** — expanding beyond models into workflows and agents
- **Content quality decay** — stub proliferation damages credibility faster than it adds breadth
- **Maintainer burnout** — single-org ownership limits scaling

---

## Product Strategy

### Platform Surfaces

#### 1. Skills Explorer (GitHub Pages)
The primary interactive experience. Users browse, search, and discover capabilities without ever opening a file.

**Key features:**
- Instant search across all 361+ skills by name, keyword, category, difficulty, framework
- Filter by: category, difficulty (beginner/intermediate/advanced), status (battle-tested/stub), framework
- Card-based skill display with live preview
- Related skills panel
- Copy-to-clipboard code examples

#### 2. Capability Search Engine
Semantics-first search that understands intent, not just keywords.

```
User: "how do I give my agent memory across sessions?"
Results:
  → skills/03-memory/episodic-memory.md (96% match)
  → skills/03-memory/vector-store-retrieval.md (87% match)
  → blueprints/memory-first-agent.md (82% match)
  → systems/research-agent.md (uses episodic memory)
```

#### 3. Agent Builder
Conversational tool: user describes a goal → platform generates a recommended architecture.

```
Input: "I need an agent that researches competitors and sends weekly Slack reports"
Output:
  Required skills: Web Search, Summarization, Memory, Slack API, Scheduling
  Recommended architecture: Research Agent blueprint + Memory-First pattern
  Suggested frameworks: LangChain + mem0 + Tavily
  Estimated complexity: Intermediate (5-7 days)
  Starting point: blueprints/research-agent.md
```

#### 4. MCP Explorer
The canonical index of the MCP ecosystem.

```
mcp-explorer/
├── servers/           # All known MCP servers with metadata
├── clients/           # MCP client implementations
├── tools/             # Individual tool definitions
├── patterns/          # Common MCP integration patterns
└── compatibility/     # Server × Client compatibility matrix
```

#### 5. Knowledge Graph Navigator
Visual, traversable graph of all AI capabilities and their relationships.

#### 6. Public API Platform
Machine-readable access to all Skills Tree data via REST/JSON.

#### 7. Contributor Dashboard
Real-time stats, contribution leaderboard, reputation system, monthly challenges.

#### 8. Sponsor Portal
Transparent, tiered sponsorship with clear value exchange and no content gating.

---

## Architecture Strategy

### Data-First Redesign

Every Markdown file gets a structured YAML frontmatter that enables all platform features:

```yaml
# skills/03-memory/episodic-memory.md
---
id: episodic-memory
version: v2
category: memory
tags: [memory, episodic, long-term, storage]
difficulty: intermediate
status: battle-tested
frameworks: [langchain, mem0, crewai]
related: [vector-store-retrieval, memory-injection, rag]
use_cases: [personalization, context-persistence, user-profiling]
complexity: O(n) storage
benchmark: benchmarks/memory/injection-strategies.md
authors: [community]
last_updated: 2026-06-01
---
```

This frontmatter is parsed by CI to:
1. Generate `data/registry/skills.json` — the canonical machine-readable index
2. Power the GitHub Pages search/filter UI
3. Feed the public API
4. Build the knowledge graph edge list

### Repository Structure (v3)

```
skills-tree/
│
├── skills/              # 361+ atomic skill files (Markdown + structured frontmatter)
├── systems/             # Multi-skill workflow documentation
├── blueprints/          # Copy-paste production architectures
├── benchmarks/          # Reproducible benchmarks with methodology
├── labs/                # Experimental capabilities
│
├── mcp/                 # NEW: MCP ecosystem
│   ├── servers/         # MCP server registry
│   ├── clients/         # MCP client implementations
│   ├── tools/           # Tool definitions
│   └── patterns/        # Integration patterns
│
├── agents/              # NEW: Agent engineering platform
│   ├── architectures/   # Architecture patterns
│   ├── multi-agent/     # Multi-agent system patterns
│   ├── evaluation/      # Agent evaluation frameworks
│   └── autonomous/      # Autonomous agent patterns
│
├── data/                # NEW: Machine-readable platform data
│   ├── schemas/         # JSON schemas for all entities
│   ├── registry/        # Auto-generated registries (JSON/YAML)
│   └── graph/           # Knowledge graph edge definitions
│
├── platform/            # NEW: Platform feature documentation
│   ├── api/             # Public API documentation
│   ├── search/          # Search design and implementation
│   └── community/       # Community system design
│
├── docs/                # GitHub Pages interactive UI
├── i18n/                # Localized READMEs
├── meta/                # Schema, glossary, roadmap, changelog
├── .github/             # Workflows, templates, actions
└── tools/               # Python build/validation tooling
```

---

## The MCP Gap — First-Mover Strategy

The Model Context Protocol has created an ecosystem with:
- 2,000+ servers on GitHub
- No canonical discovery mechanism
- No quality ratings
- No integration pattern library
- No compatibility matrix

Skills Tree can own this space by shipping:
1. `mcp/servers/` — JSON registry of all known MCP servers
2. `mcp/tools/` — individual tool definitions in standard schema
3. `mcp/patterns/` — 20+ integration patterns with working code
4. `mcp/compatibility/` — tested client × server compatibility matrix
5. `data/registry/mcp-servers.json` — machine-readable feed for tools to consume

This alone would drive 10,000+ stars from the MCP community.

---

## Community Engine

### Contribution Tiers

| Tier | Threshold | Badge | Perks |
|---|---|---|---|
| **Contributor** | 1 merged PR | 🌱 Contributor | Name in CONTRIBUTORS.md |
| **Skill Author** | 3 skills improved | ✍️ Skill Author | Contributor profile page |
| **Reviewer** | 10 PR reviews | 🔍 Reviewer | Trusted reviewer status |
| **Maintainer** | Invited | 🛠️ Maintainer | Write access, roadmap vote |
| **Core Team** | Invited | ⭐ Core | Direction-setting |

### Monthly Challenges

Monthly community challenges to drive engagement:

- **Stub Buster Month**: Upgrade 5 stubs to battle-tested, win a featured contributor spot
- **MCP Month**: Index 50 new MCP servers with quality reviews
- **Benchmark Month**: Add reproducible benchmarks to 10 skills
- **Translation Month**: Complete a language translation for a bonus i18n badge

### Reputation System

Contribution points tracked in `meta/LEADERBOARD.md` (auto-updated by CI):
- +10: New battle-tested skill
- +5: Stub → v2 upgrade
- +3: Benchmark added
- +2: PR review completed
- +1: Issue filed with reproduction

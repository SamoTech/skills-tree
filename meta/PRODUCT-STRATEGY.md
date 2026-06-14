# Product Strategy — Skills Tree v3.0

> Platform thinking. Global adoption. Ecosystem dominance.

---

## Product Philosophy

We are not building documentation. We are building **infrastructure for the AI-native era**.

The distinction matters:
- Documentation is consumed passively.
- Infrastructure is integrated actively.
- Documentation ages.
- Infrastructure evolves with its ecosystem.
- Documentation has readers.
- Infrastructure has builders who depend on it.

Every product decision must pass the test: **"Does this make Skills Tree more like infrastructure and less like documentation?"**

---

## Target Personas

### Primary

**1. The Agent Builder** (largest segment)
- Building LLM-powered products professionally
- Needs: proven patterns, working code, production benchmarks
- Pain: rediscovers the same solutions repeatedly
- Value: Skills Tree as their "skills OS" — install once, use forever

**2. The AI Researcher**
- Academic or industry researcher studying agent capabilities
- Needs: taxonomy, benchmarks, reproducible experiments
- Pain: no canonical reference for agent skill classification
- Value: Skills Tree as the cited reference in papers

**3. The Platform Builder**
- Building tools, frameworks, or platforms for AI agents
- Needs: a skills API to embed in their product
- Pain: maintaining their own skill library is expensive
- Value: Skills Tree API as a dependency

### Secondary

**4. The Learner**
- Entering the AI agent space
- Needs: structured learning path, clear examples
- Pain: overwhelming fragmentation
- Value: Skills Tree as their guided curriculum

**5. The Technical Writer / DevRel**
- Documents AI systems at companies
- Needs: reference taxonomy and examples
- Pain: inconsistent terminology across teams
- Value: Skills Tree as the shared vocabulary

---

## The Platform Stack

```
┌─────────────────────────────────────────────────────┐
│                  COMMUNITY LAYER                      │
│  Contributors · Reviewers · Sponsors · Champions      │
├─────────────────────────────────────────────────────┤
│                  PRODUCT LAYER                        │
│  Skills Explorer · Agent Builder · MCP Explorer       │
│  Knowledge Graph · Learning Paths · Benchmarks        │
├─────────────────────────────────────────────────────┤
│                  API LAYER                            │
│  REST API · GraphQL · WebSocket (live updates)        │
├─────────────────────────────────────────────────────┤
│                  DATA LAYER                           │
│  Skill JSON · MCP YAML · Relationship Graph           │
│  Benchmark DB · Learning Path JSON                    │
├─────────────────────────────────────────────────────┤
│                  CONTENT LAYER                        │
│  361+ Markdown Skill Files · Systems · Blueprints     │
│  Benchmarks · Labs · i18n                             │
└─────────────────────────────────────────────────────┘
```

---

## Feature Roadmap by Priority

### P0 — Critical (Must ship to unlock everything else)

| Feature | Why P0 | Effort |
|---|---|---|
| **Structured skill schema + JSON export** | Enables API, search, graph — the foundation of everything | Medium |
| **Search index** | Discovery is the #1 onboarding blocker | Medium |
| **MCP Explorer section** | MCP is the fastest-growing segment; missing it is leaving the table | Medium |
| **Code of Conduct** | Required for OSS health; blocks corporate contributions | Low |
| **Stub-to-battle-tested conversion sprint** | 85% stubs destroys credibility at scale | High |

### P1 — High Impact

| Feature | Why P1 | Effort |
|---|---|---|
| **Knowledge Graph data model** | Visual navigation is the killer feature for discovery | High |
| **Agent Builder (v1: form-based)** | Transforms passive readers into active users | High |
| **REST API (read-only)** | Unlocks integrations and embeds | Medium |
| **Contributor leaderboard** | Community engagement driver | Low |
| **Governance document** | Required for corporate contributors + sponsors | Low |
| **GitHub Discussions** | Community hub beyond Issues | Low |
| **Sponsor tiers + wall** | Sustainability mechanism | Low |

### P2 — Medium Impact

| Feature | Why P2 | Effort |
|---|---|---|
| **Visual knowledge graph UI** | Showcases the graph data | High |
| **Learning paths** | Learner persona activation | Medium |
| **CLI tool** | `skills-tree search "memory injection"` | Medium |
| **VS Code extension** | Meets builders in their IDE | High |
| **Monthly challenges** | Community cadence | Low |
| **Newsletter** | Retention mechanism | Low |

### P3 — Future

| Feature | Why P3 | Effort |
|---|---|---|
| **AI search assistant** | Semantic + generative search | High |
| **Agent Builder (v2: AI-powered)** | Requires P0 data layer | High |
| **Evaluation framework** | How to know a skill works in prod | High |
| **Certification program** | Community credentialing | High |
| **IDE integrations beyond VS Code** | JetBrains, Cursor, Zed | High |

---

## The "Platform Flywheel"

```
 More content → Better search → More users → More contributors
     ↑                                              ↓
 Better reputation ←── More sponsors ←── More visibility
```

The flywheel starts with **content quality** (converting stubs) and **search** (making that content findable). Everything else accelerates once these two are solved.

---

*Version: 1.0 — June 2026*

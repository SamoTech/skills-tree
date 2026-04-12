# Roadmap

This document is the strategic plan for transforming Skills Tree into a **category-defining AI skill ecosystem** — the go-to reference for every AI agent builder on the planet.

> **Status key:** 🟢 Done · 🔵 In Progress · ⚪ Planned · 🟡 Under Discussion · 🔴 Blocked

---

## 🎯 North Star

> Skills Tree becomes **the canonical index of AI agent capabilities** — versioned, benchmarked, community-powered, and integrated into every major agent framework.

Milestones:
- **1,000 GitHub stars** — credibility signal, triggers organic sharing
- **50 contributors** — self-sustaining growth loop begins
- **1,000+ skills** — true encyclopedia coverage
- **Framework integration** — LangChain Hub, MCP registry, LangGraph docs link here

---

## ✅ v1.0 — Foundation (Done)

| Status | Item |
|--------|------|
| 🟢 | 16 skill categories defined with clear taxonomy |
| 🟢 | 515+ individual skill stub files |
| 🟢 | Skill template + contribution guide (`CONTRIBUTING.md`) |
| 🟢 | Glossary, frameworks reference, and schema |
| 🟢 | GitHub Pages documentation site (`docs/index.html`) |
| 🟢 | CI: skill format validation on every PR |
| 🟢 | Issue templates (bug report, new skill request, skill update) |
| 🟢 | `CODEOWNERS`, `SECURITY.md`, `SPONSORS.md` |

---

## ✅ v1.1 — UI & Interactivity (Done)

| Status | Item |
|--------|------|
| 🟢 | Redesigned `docs/index.html` with dark/light mode toggle |
| 🟢 | Level-based filtering (Basic / Intermediate / Advanced / Experimental) |
| 🟢 | Real-time search synced across navbar and hero bar |
| 🟢 | Count-up animation for hero statistics |
| 🟢 | CSS scroll-driven reveal animations |
| 🟢 | Accessible empty state when search yields no results |
| 🟢 | Card redesign: gradient top-edge, skill level badges, browse CTA |
| 🟢 | Stats bar highlighting key category counts |

---

## ✅ v1.2 — Skill Expansion (Done)

| Status | Item |
|--------|------|
| 🟢 | 11 fully expanded perception skill files (chart-reading, pdf-parsing, handwriting-recognition, ...) |
| 🟢 | 4 expanded reasoning skill files (abductive, analogical, causal, commonsense) |
| 🟢 | 7 expanded memory skill files (fact-verification, forgetting, memory-injection, user-profile, ...) |
| 🟢 | Every expanded skill: typed I/O, runnable Python example, frameworks table, related skills, changelog |

---

## 🔵 v2.0 — Depth, Systems & Viral Mechanics (In Progress)

### Repository Structure

| Status | Item |
|--------|------|
| 🔵 | `/systems` — multi-skill workflow files (research agent, code reviewer, data pipeline, ...) |
| 🔵 | `/blueprints` — copy-paste production architectures (RAG stack, multi-agent mesh, ...) |
| 🔵 | `/benchmarks` — reproducible head-to-head skill comparisons |
| 🔵 | `/labs` — experimental and bleeding-edge skill ideas |

### Skill Quality Uplift

| Status | Item |
|--------|------|
| ⚪ | Expand ALL 515+ stubs: add description, I/O table, working code example |
| ⚪ | Add "Failure Modes" section to every skill |
| ⚪ | Add "Prompt Patterns" section to every skill |
| ⚪ | Model comparison table per skill (Claude vs GPT-4o vs Gemini 2.0) |
| ⚪ | JSON/YAML export of all skill metadata for programmatic consumption |
| ⚪ | OpenAPI-style schema for skills |

### Skill Versioning System

| Status | Item |
|--------|------|
| ⚪ | Define v1/v2/v3 versioning spec and enforce in template |
| ⚪ | Track version per skill in frontmatter (`version: v1`) |
| ⚪ | PR title convention: `improve: [skill] — v1→v2` |
| ⚪ | Auto-badge: skills that reach v3 get "Battle-Tested" label |

### Viral Growth Mechanics

| Status | Item |
|--------|------|
| ⚪ | `meta/LEADERBOARD.md` — weekly auto-updated Top Skills, Most Improved, Battle-Tested |
| ⚪ | "This Week's Highlights" section in README (manual until automated) |
| ⚪ | "Most Active Skills" badge driven by PR activity |
| ⚪ | "Trending Systems" section updated with each new system added |
| ⚪ | "Used In" tracker — link public projects that reference Skills Tree skills |

---

## ⚪ v2.x — Community & Ecosystem

### Community Growth

| Status | Item |
|--------|------|
| ⚪ | Contribution leaderboard: top contributors by skill count + quality |
| ⚪ | "Skill Champion" role — assigned to contributor who owns a skill's evolution |
| ⚪ | Monthly "State of the Skills Tree" post (Reddit, Twitter/X, LinkedIn) |
| ⚪ | GitHub Discussions enabled with categories: Ideas, Benchmarks, Q&A, Showcase |
| ⚪ | Discord or community server (once 200+ stars) |

### Auto-Growth Engine

| Status | Item |
|--------|------|
| ⚪ | GitHub Action: auto-label PRs by contribution type (feat/improve/benchmark/system) |
| ⚪ | GitHub Action: auto-generate LEADERBOARD.md from PR merge history |
| ⚪ | GitHub Action: auto-update skill count badges in README on merge |
| ⚪ | GitHub Action: detect and comment when a PR upgrades a skill to v2/v3 |
| ⚪ | Remixing guide: how to fork and specialize Skills Tree for a domain |

### Skill Paths (Learning Tracks)

| Status | Item |
|--------|------|
| ⚪ | "Build a Research Agent" path (5 skills, ordered) |
| ⚪ | "Memory-First Agent" path |
| ⚪ | "Computer Use Agent" path |
| ⚪ | "From Zero to Production" beginner track |
| ⚪ | Visual skill dependency graph (interactive, web UI) |

### Localization

| Status | Item |
|--------|------|
| 🟡 | Arabic README translation (`README.ar.md`) |
| 🟡 | Chinese README translation (`README.zh.md`) |
| 🟡 | Spanish README translation (`README.es.md`) |
| 🟡 | Category READMEs in Arabic, Chinese, Spanish |

---

## ⚪ v3.0 — Platform & Integration

### CLI Tool

| Status | Item |
|--------|------|
| ⚪ | `skills-tree search "memory injection"` — ranked results from the index |
| ⚪ | `skills-tree show memory/memory-injection` — render a skill in terminal |
| ⚪ | `skills-tree new` — interactive skill creation wizard |
| ⚪ | `skills-tree benchmark run <skill>` — run a benchmark script locally |
| ⚪ | Publish to PyPI (`pip install skills-tree`) |

### Framework Integration

| Status | Item |
|--------|------|
| 🟡 | LangChain Hub: publish skills as Hub templates |
| 🟡 | MCP (Model Context Protocol) registry: list skills as MCP tools |
| 🟡 | LangGraph docs: "See Skills Tree" reference in relevant pages |
| 🟡 | OpenAI cookbook cross-reference |
| ⚪ | Anthropic cookbook cross-reference |

### API & Programmatic Access

| Status | Item |
|--------|------|
| ⚪ | Static JSON API: `https://samotech.github.io/skills-tree/api/skills.json` |
| ⚪ | Skills metadata in JSON-LD format for SEO |
| ⚪ | GitHub Release: packaged skill index (JSON + Markdown zip) |

---

## 📈 Content Strategy

### What to Prioritize

1. **High-frequency, real-agent skills** — things builders actually use in production today
2. **Benchmarkable skills** — anything with a measurable quality output (accuracy, latency, cost)
3. **Framework-specific patterns** — LangGraph nodes, CrewAI tools, AutoGen agents
4. **Domain verticals** — healthcare, legal, finance, DevOps are the highest-demand sectors
5. **Bleeding-edge** — add labs/ entries for skills that will be mainstream in 6-12 months

### What to Avoid

- ❌ Generic prompts with no structure ("Ask the model to summarize")
- ❌ Skills without working code examples
- ❌ Duplicate skills with only cosmetic differences
- ❌ Speculative capabilities not yet reproducible
- ❌ Framework-locked skills without model-agnostic alternatives

### Staying Aligned with AI Trends

- Follow [Anthropic](https://www.anthropic.com/news), [OpenAI](https://openai.com/blog), [DeepMind](https://deepmind.google) release notes monthly
- Monitor [Papers With Code](https://paperswithcode.com) for emerging agent techniques
- Track GitHub trending repos in `ai-agents`, `llm`, `langchain` topics weekly
- Every new major model release triggers a "model comparison" update pass on top-20 skills

---

## 🌍 Distribution Strategy

### Launch Playbook (Each Major Version)

| Channel | Action | Timing |
|---|---|---|
| **GitHub** | Create Release with full changelog + highlights | Day 0 |
| **Twitter/X** | Thread: "What's new in Skills Tree vX.X" with skill examples | Day 0 |
| **Reddit r/MachineLearning** | "Show HN"-style post with benchmark results | Day 1 |
| **Reddit r/LangChain** | Post linking specific skills relevant to the community | Day 1 |
| **Hacker News** | "Show HN: Skills Tree — open-source AI agent skill OS" | Day 2 |
| **Dev.to** | Tutorial post using 3 skills to build a mini-agent | Day 3 |
| **LinkedIn** | Founder-voice post on the vision + milestone reached | Day 3 |

### Ongoing Growth

- Pin the repo to your GitHub profile
- Add "Powered by Skills Tree" badge option for projects using these skills
- Cross-link from skill files to relevant blog posts, papers, and tutorials
- Engage every star — reply to issues, review PRs within 48h
- Feature contributor work in monthly updates

### Attraction Mechanics

| Hook | Description |
|---|---|
| **"Top Skills This Week"** | Updated every Monday — drives return visits |
| **"Most Improved"** | Celebrates contributors — drives contributions |
| **"Battle-Tested"** | Social proof signal — drives trust and stars |
| **"Trending Systems"** | Shows what builders are assembling — drives interest |
| **Skill Remix** | Fork + specialize pattern — drives forks and citations |

---

## 🔧 Skill Coverage Gaps (Open for Contribution)

> Pick one and open a PR. See [CONTRIBUTING.md](../CONTRIBUTING.md) for the template.

- [ ] **Reasoning**: Probabilistic reasoning, Bayesian inference, constraint satisfaction
- [ ] **Memory**: Hierarchical memory management, cache eviction strategies, forgetting curves
- [ ] **Code**: IDE integration patterns, pair-programming protocols, polyglot agents
- [ ] **Security**: Red-teaming, jailbreak resistance, adversarial robustness, prompt injection defense
- [ ] **Domain-Specific**: Healthcare NLP, legal document analysis, scientific literature review, financial modeling
- [ ] **Orchestration**: Multi-modal pipelines, cross-agent authentication, consensus mechanisms
- [ ] **Agentic Patterns**: Monte Carlo Tree Search, Reflexion, self-consistency sampling
- [ ] **Computer Use**: Accessibility tree parsing, game automation, industrial HMI control

---

## 💡 How to Propose a Roadmap Item

1. Open a [Discussion](https://github.com/SamoTech/skills-tree/discussions) tagged `roadmap`
2. Describe the item, its value, and its scope
3. If accepted, it gets added here with ⚪ status
4. Assign yourself and submit a PR when ready

---

## 📊 Progress Summary

| Phase | Status | ETA |
|---|---|---|
| v1.0 Foundation | 🟢 Complete | 2025-03 |
| v1.1 UI | 🟢 Complete | 2025-04 |
| v1.2 Skill Expansion | 🟢 Complete | 2026-04 |
| v2.0 Systems + Benchmarks | 🔵 In Progress | 2026 Q2 |
| v2.x Community Engine | ⚪ Planned | 2026 Q3 |
| v3.0 Platform + CLI | ⚪ Planned | 2026 Q4 |

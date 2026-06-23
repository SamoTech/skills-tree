# VIRAL BASELINE AUDIT

**Initiative:** INITIATIVE-011A  
**Date:** 2026-06-23  
**Assessor:** Program Director  
**Source of truth:** Repository files only

---

## Authoritative State (from meta/MEMORY_STATE.md + README.md)

| Metric | Value | Source |
|--------|-------|--------|
| Schema version | 3.1 | MEMORY_STATE.md |
| Node count | 368 | MEMORY_STATE.md |
| Edge count | 780 | MEMORY_STATE.md |
| REQUIRES edges | 15 | MEMORY_STATE.md |
| OS Readiness Score | 6.97 / 10 | meta/AI_ENGINEERING_OS_READINESS.md |
| Last initiative | INITIATIVE-010A | MEMORY_STATE.md |
| Skill categories | 17 | README.md |
| Battle-tested skills | ~50 | README.md |
| Stub skills | ~308 | README.md |
| Supported languages (i18n) | 10 | README.md |
| Blueprints | 6+ | README.md |
| Systems | 6 | README.md |
| Benchmarks | 4 | README.md |

---

## Community Metrics (from README badges — live at audit time)

> Note: Live star/fork/contributor counts are dynamic. The following reflects what is observable from README badge configuration and repository structure. Exact counts require GitHub API at runtime.

| Metric | Observable signal | Notes |
|--------|------------------|-------|
| Stars | Badge present (green) | Count not readable from static file |
| Forks | Badge present (blue) | Count not readable from static file |
| Contributors | Badge present (amber) | Count not readable from static file |
| Open issues | Not prominently surfaced | Opportunity gap |
| PRs welcome | Badge present | CONTRIBUTING.md exists |
| PyPI package | Published, versioned | `skills-tree` on PyPI |
| Live docs | GitHub Pages active | samotech.github.io/skills-tree |
| CI status | Green badge present | validate-skills.yml |

---

## Documentation Depth Audit

| Asset | Status | Quality signal |
|-------|--------|---------------|
| README.md | ✅ Comprehensive | Long-form, structured, comparison table, quick install |
| docs/installation.md | ✅ Linked | Dedicated install guide |
| docs/quickstart.md | ✅ Linked | Quick start guide |
| docs/architecture.md | ✅ Linked | Architecture deep-dive |
| docs/WHY_SKILLS_TREE.md | ✅ Linked | Problem statement + competitive positioning |
| docs/USE_CASES.md | ✅ Linked | Real-world use cases |
| CONTRIBUTING.md | ✅ Present | PR formats defined |
| i18n/ (10 languages) | ✅ Present | Arabic, Chinese, Spanish, German, French, Hindi, Japanese, Korean, Portuguese, Russian |
| meta/ROADMAP.md | ✅ Present | Near/medium/long-term roadmap |
| meta/skill-template.md | ✅ Present | Contributor template |

---

## Onboarding Friction Analysis

| Step | Current state | Friction level |
|------|-------------|---------------|
| Discover repo | README has strong hook | LOW |
| Install package | `pip install skills-tree` — 1 command | VERY LOW |
| First API call | 3-line Python example in README | LOW |
| First contribution | `cp meta/skill-template.md` — clear instructions | LOW |
| Find a skill to contribute | 308 stubs = obvious open slots | LOW |
| Understanding the graph | SKILLS_GRAPH.json not surfaced in README | MEDIUM |
| Understanding REQUIRES model | Not explained in README | MEDIUM-HIGH |
| Interactive exploration | No live interactive demo linked | HIGH |
| Finding learning paths | Not surfaced — paths not yet user-facing | HIGH |
| Contributor recognition | No scoreboard, no Hall of Fame visible | HIGH |

---

## Viral Surface Gaps

| Gap | Impact | Priority |
|-----|--------|----------|
| No interactive skill explorer (web app) | Users can't explore without cloning | CRITICAL |
| Learning paths not user-facing | Core value prop invisible | CRITICAL |
| No contributor scoreboard | No social proof loop | HIGH |
| Benchmarks section has only 4 entries | Opportunity for viral "head-to-head" content | HIGH |
| Open issues not surfaced as contributor hooks | Community momentum gap | HIGH |
| Goal-to-Blueprint generator doesn't exist | High-demand feature missing | HIGH |
| No "weekly highlights" with real content yet | "No skill changes this week" visible to all | MEDIUM |
| No community Discord/GitHub Discussions | No async community hub | MEDIUM |

---

## Positioning Strength Assessment

| Element | Current | Verdict |
|---------|---------|--------|
| Primary tagline | "The AI Agent Skill OS" | ✅ Strong — clear and unique |
| Secondary tagline | "Build Smarter Agents, Faster" | ✅ Benefit-focused |
| Problem framing | "Every AI agent builder rediscovers the same skills from scratch" | ✅ Emotionally resonant |
| Comparison table | vs LangChain Hub, HF Hub, Custom YAML | ✅ Well-executed |
| Social share button | X/Twitter intent pre-filled | ✅ Present |
| Sponsor link | Present | ✅ Present |
| Viral hook density | Moderate | ⚠️ Can be amplified |

---

*This document is the authoritative baseline for INITIATIVE-011A growth tracking.*

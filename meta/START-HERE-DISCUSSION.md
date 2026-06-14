# 👋 Start Here — Welcome to Skills Tree!

> This post is pinned. If you're new, read this first.

**Skills Tree** is the AI Agent Skill OS — the world's most comprehensive, versioned, community-powered index of AI agent capabilities. Every skill is documented with working code, real benchmarks, failure modes, and evolution history so that every AI agent builder never has to rediscover the same skills from scratch.

📚 **Docs site:** https://samotech.github.io/skills-tree  
⭐ **GitHub:** https://github.com/SamoTech/skills-tree  
📖 **API:** https://samotech.github.io/skills-tree/api/skills.json

---

## 🗺️ What's in the Repository

| Directory | What It Contains |
|-----------|------------------|
| `skills/` | 377+ atomic skill files across 17 categories |
| `systems/` | 8 multi-skill workflow docs (research agent, code reviewer, etc.) |
| `blueprints/` | 7 copy-paste production architectures |
| `benchmarks/` | 4 reproducible head-to-head comparisons |
| `labs/` | 4 experimental bleeding-edge skill ideas |
| `paths/` | Curated learning tracks (coming soon) |

---

## ⚡ Your First Contribution in 5 Minutes

The fastest way to contribute is upgrading a stub skill to v2. Here's the exact process:

1. **Pick a stub** from [`meta/QUALITY-REPORT.md`](../meta/QUALITY-REPORT.md) — any skill marked `v1 stub`
2. **Fork the repo** and open the skill's `.md` file
3. **Add these three things** using [`meta/skill-template.md`](../meta/skill-template.md) as your guide:
   - A real, runnable Python code example (≥3 lines, no pseudocode)
   - A "Failure Modes" section (2-3 bullet points of what goes wrong)
   - `related_skills` links to ≥2 other skill files
4. **Bump the version** in frontmatter: `version: v2`
5. **Open a PR** with title: `improve: [skill-name] — v1→v2`

That's it. CI will validate your frontmatter automatically. A maintainer will review within 48 hours.

---

## 🎯 Current Top Priorities

Here's what makes the biggest difference right now:

| # | Task | Why It Matters |
|---|------|----------------|
| 1 | **Upgrade a stub to v2** | ~80% of skills are thin stubs — every upgrade makes the catalog more trustworthy |
| 2 | **Submit a used-in** | Open a [used-in issue](../../../issues/new?template=used-in.yml) if you've used any of these skills in a project |
| 3 | **Benchmark a skill** | Pick any category that lacks a benchmark and write a head-to-head comparison |
| 4 | **Translate a category README** | Arabic, Chinese, Spanish are highest-priority |

---

## 🏷️ Labels to Watch

| Label | What to Look For |
|-------|------------------|
| `good first issue` | Safe first PRs — upgrade a named stub to v2 |
| `feat` | New skill additions |
| `improve` | Skill upgrades (v1→v2, v2→v3) |
| `benchmark` | Head-to-head comparisons |
| `Battle-Tested` | Skills that have reached v3 — congratulations PRs! |

---

## 💬 Discussion Categories

Use the right category for your post:

- **Ideas** — feature requests, new categories, schema proposals
- **Benchmarks** — share your benchmark results or request comparisons
- **Q&A** — questions about skills, the project, or AI agents in general
- **Showcase** — show off a project you built using skills from this index
- **Roadmap** — discuss upcoming priorities and what to build next

---

## 📬 Stay in the Loop

- ⭐ **Star the repo** — triggers the weekly leaderboard and helps other builders find us
- 👁️ **Watch** → *All Activity* to see every new skill and discussion
- 🔔 Subscribe to this thread for announcements

---

*Built with ❤️ by [Ossama Hashim](https://github.com/SamoTech) and contributors. Every skill you add saves someone else a week of research.*

# COMMUNITY ENGINE

**Initiative:** INITIATIVE-011A  
**Date:** 2026-06-23  
**Purpose:** Design the contributor onboarding, retention, and community momentum system.

---

## Contributor Onboarding

### The First 5 Minutes

```
Discover skills-tree
  → Star the repo (CTA in README)
  → Read README (< 3 min to "What This Is")
  → Run: pip install skills-tree
  → Run: skills-tree search "memory"
  → See: 308 stubs → "I could contribute this"
```

The onboarding goal is to get a contributor from zero to their first meaningful action in under 10 minutes.

---

## First PR Path

The lowest-friction contribution path in the AI open-source space:

### Step 1 — Choose a stub (2 min)
```bash
skills-tree list --maturity stub
# Returns: 308 skills with stub status
# Pick one you know
```

### Step 2 — Copy the template (30 sec)
```bash
cp meta/skill-template.md skills/<category>/<your-skill>.md
```

### Step 3 — Fill in the template (20–60 min)
The template guides you through every section. You don't need to invent structure — just fill in what you know.

### Step 4 — Open PR (5 min)
```bash
git checkout -b feat/add-<skill-name>
git add skills/<category>/<skill>.md
git commit -m "feat: add <skill> to <category>"
git push origin feat/add-<skill-name>
# Open PR → title auto-formats from commit message
```

### Step 5 — CI validates (automatic)
- `validate-skills.yml` runs automatically
- If green → PR is mergeable
- If red → CI tells you exactly what to fix

**Time to first merged PR: under 2 hours for a known skill.**

---

## Good First Issue Framework

### Issue Labels

| Label | Definition | Difficulty |
|-------|-----------|----------|
| `good first issue` | Stub skill that needs content — template provided | Beginner |
| `skill upgrade` | v1 skill needing v2 treatment (add code, failure modes) | Intermediate |
| `benchmark needed` | Skill needing head-to-head benchmark | Intermediate |
| `translation` | i18n README update | Beginner |
| `system design` | New system (multi-skill workflow) needed | Advanced |
| `blueprint` | New production blueprint needed | Advanced |

### Good First Issue Template
```markdown
## Add skill: <skill-name>

**Category:** <category>
**Template:** [meta/skill-template.md](meta/skill-template.md)
**Difficulty:** Beginner
**Estimated time:** 30–60 minutes

### What to do
1. Copy `meta/skill-template.md` to `skills/<category>/<skill-name>.md`
2. Fill in all sections
3. Open a PR with title: `feat: add <skill-name> to <category>`

### Definition of Done
- [ ] All required fields filled in
- [ ] At least one runnable code example
- [ ] Failure modes section completed
- [ ] CI passes
```

**Target: 50 open "good first issues" at all times.** When one closes, open a new one.

---

## Community Missions

Missions are time-boxed, community-wide efforts with a shared goal.

### Mission Format
```markdown
## Mission: <name>
Duration: <X weeks>
Goal: <metric target>
Reward: <recognition + badge>
Progress: <current> / <target>
```

### Launch Missions

**Mission 1 — Battle-Test 100**
- Goal: Upgrade 50 more skills from stub → battle-tested (reach 100 total)
- Duration: 60 days
- Reward: "Battle-Tester" badge for all contributors
- Progress tracker: live in README

**Mission 2 — Benchmark Blitz**
- Goal: Add 20 new head-to-head benchmarks
- Duration: 45 days
- Reward: "Benchmarker" badge
- Each benchmark: run two approaches on the same task, report real numbers

**Mission 3 — Path Builder**
- Goal: Create 10 community learning paths
- Duration: 30 days
- Reward: "Path Builder" badge
- Path format: skill sequence + rationale + estimated time

**Mission 4 — Global Reach**
- Goal: Validate and update all 10 i18n READMEs
- Duration: 14 days
- Reward: "Ambassador" badge per language

---

## Monthly Challenges

| Month | Challenge | Prize |
|-------|-----------|-------|
| Month 1 | First 10 learning paths | Feature in README |
| Month 2 | Best new benchmark (most upvotes) | "Benchmark of the Month" + LinkedIn shoutout |
| Month 3 | Most skills added in a single PR (quality gate applies) | Top Contributor badge |
| Month 4 | Best blueprint (voted by community) | "Blueprint Award" |
| Month 5 | Most creative system design | "Systems Architect" title |
| Month 6 | "Steward" challenge: close 10 issues | "Steward" badge |

---

## Community Infrastructure

| Channel | Purpose | Priority |
|---------|---------|----------|
| GitHub Discussions | Primary async community hub | CRITICAL — launch now |
| GitHub Issues | Bug reports + good first issues | ACTIVE |
| GitHub Projects | Roadmap visibility | ACTIVE |
| Discord (future) | Real-time community chat | Milestone: 500 stars |
| Newsletter (future) | Monthly highlights + contributor recognition | Milestone: 200 contributors |

---

## Contributor Recognition System

| Tier | Threshold | Recognition |
|------|-----------|------------|
| Contributor | 1 merged PR | Listed in CONTRIBUTORS.md |
| Skill Author | 3+ skills merged | "Skill Author" label |
| Benchmarker | 2+ benchmarks merged | "Benchmarker" label |
| Path Builder | 1+ learning path merged | "Path Builder" label |
| Core Contributor | 10+ merged PRs | README acknowledgment |
| Top Contributor | Top 10 all-time score | Scoreboard + LinkedIn shoutout |
| Maintainer | Invited by owner | Write access + governance rights |

---

*The goal: every contributor feels seen, celebrated, and motivated to return.*

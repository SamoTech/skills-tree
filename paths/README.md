# Skill Paths

Curated learning tracks that guide you through building a specific type of AI agent — step by step, skill by skill.

Each path is a **ordered sequence** of Skills Tree entries. You follow them in order, using each skill's code examples, prompt patterns, and failure modes to build up a working system.

> **How to use a path**
> 1. Open the path file below
> 2. Follow skills in order — each step builds on the last
> 3. Run the code examples from each skill file
> 4. Check off the completion checklist at the bottom of each path
> 5. You now have a working, production-ready agent pattern

---

## Available Paths

| Path | Difficulty | Skills | Est. Time | What You Build |
|------|-----------|--------|-----------|----------------|
| [Build a Research Agent](./research-agent.md) | ⭐⭐ Intermediate | 5 | ~3 hours | Agent that searches, retrieves, and synthesises information autonomously |
| [Memory-First Agent](./memory-first-agent.md) | ⭐⭐ Intermediate | 5 | ~3 hours | Agent with persistent, queryable, multi-layer memory |
| [Computer Use Agent](./computer-use-agent.md) | ⭐⭐⭐ Advanced | 5 | ~4 hours | Agent that controls a desktop UI end-to-end |
| [From Zero to Production](./zero-to-production.md) | ⭐ Beginner | 7 | ~5 hours | Full agent dev lifecycle from first prompt to deployed system |

---

## Path Format

Every path file follows this structure:

```
## Overview      — what you'll build and why
## Prerequisites — what to know before starting
## The Path      — ordered skill steps with rationale
## Code Scaffold — minimal working skeleton
## Checklist     — verify you've covered everything
## Next Steps    — where to go after completion
```

---

## Contributing a Path

1. Copy `meta/path-template.md` (see below)
2. Name your file `paths/your-path-name.md`
3. Reference only skills that exist in `skills/**/*.md`
4. Include a working code scaffold (even minimal)
5. Open a PR with title `feat(path): your path name`

### Path template

```markdown
# Path: [Name]

**Difficulty:** ⭐ Beginner / ⭐⭐ Intermediate / ⭐⭐⭐ Advanced  
**Skills:** N  
**Est. Time:** X hours  
**Goal:** One sentence — what the learner builds.

## Overview
## Prerequisites
## The Path
### Step 1 — [Skill Name]
### Step 2 — ...
## Code Scaffold
## Checklist
## Next Steps
```

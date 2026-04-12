# Contributing to Skills Tree

> The AI Agent Skill OS — built by the community, for the community.

Thank you for helping grow the most comprehensive AI agent skills resource on the internet. Every contribution — a new skill, a benchmark, a system, or a fix — makes every AI builder who comes after you faster.

---

## Table of Contents

- [4 Ways to Contribute](#4-ways-to-contribute)
- [How to Add a New Skill](#how-to-add-a-new-skill)
- [How to Upgrade a Skill (v1→v2)](#how-to-upgrade-a-skill-v1v2)
- [How to Add a Benchmark](#how-to-add-a-benchmark)
- [How to Add a System or Blueprint](#how-to-add-a-system-or-blueprint)
- [Skill Quality Bar](#skill-quality-bar)
- [Skill Versioning Rules](#skill-versioning-rules)
- [PR Templates](#pr-templates)
- [Commit Convention](#commit-convention)
- [PR Checklist](#pr-checklist)
- [Code of Conduct](#code-of-conduct)

---

## 4 Ways to Contribute

| Type | What It Is | Where | PR Title Format |
|---|---|---|---|
| **New Skill** | A capability not yet in the index | `skills/XX-category/` | `feat: add [skill] to [category]` |
| **Skill Upgrade** | Bump v1→v2 or v2→v3 with better content | Same file | `improve: [skill] — v1→v2` |
| **Benchmark** | Head-to-head with real numbers | `benchmarks/category/` | `benchmark: [skill-a] vs [skill-b]` |
| **System / Blueprint** | Multi-skill workflow or architecture | `systems/` or `blueprints/` | `system: add [name]` / `blueprint: add [name]` |

---

## How to Add a New Skill

```bash
# 1. Fork and clone
git clone https://github.com/SamoTech/skills-tree.git
cd skills-tree

# 2. Check for duplicates
grep -r "your-skill-name" skills/ --include="*.md" -l

# 3. Copy the template
cp meta/skill-template.md skills/05-code/my-new-skill.md

# 4. Fill in every field (no placeholders!)

# 5. Commit and push
git checkout -b feat/add-my-new-skill
git add skills/05-code/my-new-skill.md
git commit -m "feat: add my-new-skill to 05-code"
git push origin feat/add-my-new-skill
```

---

## How to Upgrade a Skill (v1→v2)

Skills are versioned. Upgrading an existing skill is highly valued — often more than adding a new stub.

**v1 → v2 means adding:**
- A complete, real code example (not pseudocode)
- A "Failure Modes" section
- Benchmark link (if one exists)
- Related Skills links to ≥ 2 other files

**v2 → v3 means adding:**
- Model comparison table (Claude vs GPT-4o vs Gemini)
- Production notes (cost, rate limits, edge cases)
- Link to a System or Blueprint that uses this skill

PR title: `improve: [skill-name] — v1→v2`

---

## How to Add a Benchmark

```bash
cp meta/benchmark-template.md benchmarks/reasoning/skill-a-vs-skill-b.md
# Fill in all sections with real numbers
# PR title: benchmark: [skill-a] vs [skill-b] on [dataset]
```

**Minimum benchmark requirements:**
- Named public dataset OR precisely described custom test set
- At least 2 metrics (not just one number)
- Reproducible methodology (code or clear description)
- Honest scope limits ("what was NOT tested")

---

## How to Add a System or Blueprint

```bash
# System (multi-skill workflow)
cp meta/system-template.md systems/my-system.md
# PR title: system: add [name]

# Blueprint (production architecture)
cp meta/blueprint-template.md blueprints/my-blueprint.md
# PR title: blueprint: add [name]
```

**System quality bar:** Must be runnable end-to-end, not just a diagram.  
**Blueprint quality bar:** Must include technology choices with rationale, cost estimate, and scaling notes.

---

## Skill Quality Bar

### Must Have

- ✅ A real capability that works **today** in an existing agent, model, or framework
- ✅ Clear description (2–4 sentences: what it does + when to use it)
- ✅ At least one **complete, runnable** code example
- ✅ `Skill Level`: `basic` | `intermediate` | `advanced`
- ✅ `Stability`: `stable` | `experimental` | `deprecated`
- ✅ `Version`: `v1` (new), `v2`, `v3`
- ✅ At least one **Related Skills** link

### Must Not Have

- ❌ Speculative future capabilities
- ❌ Duplicate of an existing skill
- ❌ Vague descriptions ("helps agents do things better")
- ❌ Placeholder examples that don't run
- ❌ Broken internal links

### Skill Level Definitions

| Level | Meaning |
|---|---|
| `basic` | Works out-of-the-box with a simple prompt |
| `intermediate` | Requires tool-calling, APIs, or multi-step logic |
| `advanced` | Requires specialized architecture or fine-tuning |

---

## Skill Versioning Rules

```
v1 — Initial entry: description + basic example (stubs are OK at v1)
v2 — Enriched: complete example + failure modes + related skills
v3 — Battle-tested: benchmarks + model comparison + production notes
```

**Bump the version** in the frontmatter AND add a changelog row at the bottom of the file whenever you upgrade.

---

## PR Templates

### New Skill PR

```markdown
## New Skill: [skill-name]

**Category:** XX-category
**Skill Level:** basic | intermediate | advanced
**Problem solved:** What gap in the index does this fill?
**Example input:** ...
**Example output:** ...
**Why it's better than existing alternatives:** ...
```

### Skill Upgrade PR

```markdown
## Skill Upgrade: [skill-name] v1→v2

**What changed:**
- Added complete runnable example
- Added failure modes section
- Added benchmark link

**Why this upgrade matters:** ...
```

### Benchmark PR

```markdown
## Benchmark: [skill-a] vs [skill-b]

**Dataset:** [name + size]
**Key finding:** [winner + margin]
**Reproducibility:** [link to code or methodology description]
```

---

## Commit Convention

```
feat: add [skill-name] to [category]
improve: [skill-name] — v1→v2
benchmark: [skill-a] vs [skill-b] on [dataset]
system: add [system-name]
blueprint: add [blueprint-name]
fix: [what was wrong and what you fixed]
docs: [what you updated]
```

---

## PR Checklist

- [ ] Correct folder and `kebab-case.md` filename
- [ ] No placeholder fields left in template
- [ ] Code example is real and runnable (not pseudocode)
- [ ] No duplicate skill exists (`grep -r "skill-name" skills/`)
- [ ] Internal links point to real files
- [ ] PR title follows convention
- [ ] Version field set in frontmatter
- [ ] Changelog row added at bottom of file

---

## Code of Conduct

Be kind, constructive, and welcoming. We follow the [Contributor Covenant v2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). Harassment will not be tolerated.

---

*Made with ❤️ by [Ossama Hashim](https://github.com/SamoTech) and contributors.*

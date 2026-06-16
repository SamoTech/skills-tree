# Contributing

Thank you for contributing to Skills Tree! This guide covers everything you need to submit a high-quality contribution.

Full details are also in the root [`CONTRIBUTING.md`](https://github.com/SamoTech/skills-tree/blob/main/CONTRIBUTING.md).

## Types of Contributions

| Type | What It Is | PR Title Format |
|---|---|---|
| **New Skill** | A capability not yet indexed | `feat: add [skill] to [category]` |
| **Skill Upgrade** | Bump v1→v2 with better content | `improve: [skill] — v1→v2` |
| **Benchmark** | Head-to-head with real numbers | `benchmark: [skill-a] vs [skill-b]` |
| **System / Blueprint** | Multi-skill workflow or architecture | `system: add [name]` |
| **Bug Fix** | Fix a broken example or link | `fix: ...` |
| **Docs** | Documentation improvements | `docs: ...` |

## Quick Contribution Flow

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/skills-tree.git

# 2. Create a branch
git checkout -b feat/add-my-skill

# 3. Copy the skill template
cp meta/skill-template.md skills/05-code/my-new-skill.md

# 4. Fill in the template (all required sections)

# 5. Validate locally
python tools/check_skill_quality.py skills/05-code/my-new-skill.md

# 6. Commit and push
git add .
git commit -m "feat: add my-new-skill to code"
git push origin feat/add-my-skill

# 7. Open a PR on GitHub
```

## Quality Rules

- ❌ No generic prompts or vague descriptions
- ❌ No skills without a working code example
- ✅ Must solve a real, specific problem
- ✅ Must be structured and reusable
- ✅ Must include typed inputs, outputs, and at least one runnable example

## Skill Template

All skills must follow the schema in [`meta/skill-template.md`](https://github.com/SamoTech/skills-tree/blob/main/meta/skill-template.md).

## Getting Help

- Open a [GitHub Discussion](https://github.com/SamoTech/skills-tree/discussions)
- Check existing [issues](https://github.com/SamoTech/skills-tree/issues)
- Review the [CONTRIBUTING.md](https://github.com/SamoTech/skills-tree/blob/main/CONTRIBUTING.md)

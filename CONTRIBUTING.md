# 🤝 Contributing to Skills Tree

Thank you for helping grow the most comprehensive AI agent skills catalog on the internet! 🌱

Every contribution — whether a new skill, a fix, a framework update, or a glossary entry — makes this resource more valuable for everyone building AI agents and autonomous systems.

---

## 📋 Table of Contents

- [Types of Contributions](#types-of-contributions)
- [How to Add a Skill](#how-to-add-a-skill)
- [Skill Quality Guidelines](#skill-quality-guidelines)
- [How to Update a Skill](#how-to-update-a-skill)
- [How to Add a Framework or Model](#how-to-add-a-framework-or-model)
- [How to Propose a New Category](#how-to-propose-a-new-category)
- [Commit Message Convention](#commit-message-convention)
- [Pull Request Checklist](#pull-request-checklist)
- [Code of Conduct](#code-of-conduct)

---

## 🧩 Types of Contributions

| Type | Label | Description |
|---|---|---|
| New skill | `feat` | A brand-new skill file added to an existing category |
| Skill improvement | `improve` | Better description, richer example, more related skills |
| Bug / typo fix | `fix` | Fixing incorrect info, broken links, or typos |
| New category | `category` | Proposing an entirely new skill family |
| Framework update | `framework` | Adding/updating an entry in `meta/frameworks.md` |
| Glossary term | `glossary` | New term or improved definition in `meta/glossary.md` |
| Documentation | `docs` | README, CONTRIBUTING, or meta file improvements |

---

## ➕ How to Add a Skill

1. **Fork & clone** the repository
   ```bash
   git clone https://github.com/SamoTech/skills-tree.git
   cd skills-tree
   ```

2. **Find the right category** in `skills/` — browse the 16 folders to locate where your skill fits best.

3. **Check for duplicates** — search existing files before creating a new one:
   ```bash
   grep -r "your-skill-name" skills/
   ```

4. **Copy the template** from `meta/skill-template.md`:
   ```bash
   cp meta/skill-template.md skills/05-code/my-new-skill.md
   ```

5. **Fill in all fields** — name, description, inputs, outputs, example, frameworks, related skills.

6. **Name your file** using `kebab-case.md` (e.g., `sql-query-generation.md`).

7. **Commit and open a pull request**:
   ```bash
   git checkout -b feat/add-sql-query-generation
   git add skills/05-code/sql-query-generation.md
   git commit -m "feat: add sql-query-generation to 05-code"
   git push origin feat/add-sql-query-generation
   ```

8. **PR title format**: `feat: add [skill-name] to [category-number]-[category-name]`

---

## ✅ Skill Quality Guidelines

### Must Have

- ✅ A real capability that an existing agent, model, or framework can perform **today**
- ✅ Clear, concise description (1–3 sentences max)
- ✅ At least one concrete, runnable code example
- ✅ `skill-level` set to `basic`, `intermediate`, or `advanced`
- ✅ `stability` set to `stable`, `experimental`, or `deprecated`
- ✅ At least one entry in **Related Skills**
- ✅ Referenced to a real framework or model that implements it

### Must Not Have

- ❌ Speculative or hypothetical future capabilities
- ❌ Duplicates — always search before submitting
- ❌ Vague descriptions like "helps agents do things"
- ❌ Placeholder examples that don't demonstrate real usage
- ❌ Broken links

### Skill Level Definitions

| Level | Meaning |
|---|---|
| `basic` | Any agent/LLM can do this out-of-the-box with a simple prompt |
| `intermediate` | Requires tool-calling, specific APIs, or multi-step logic |
| `advanced` | Requires specialized architecture, fine-tuning, or complex orchestration |

### Stability Definitions

| Stability | Meaning |
|---|---|
| `stable` | Widely supported across multiple frameworks and models |
| `experimental` | Available in some systems but not yet standardized |
| `deprecated` | Was once common but superseded by a better approach |

---

## ✏️ How to Update a Skill

- Open the skill's `.md` file directly and make your changes.
- PR title format: `improve: [skill-name] — [what changed]`
- Examples of good improvements:
  - Adding a missing framework reference
  - Providing a better or more realistic code example
  - Linking to a newly discovered related skill
  - Updating stability from `experimental` to `stable`

---

## 🧰 How to Add a Framework or Model

Edit `meta/frameworks.md` and add a row to the appropriate table:

- **Agent Frameworks** — orchestration libraries (LangChain, CrewAI, etc.)
- **Computer Use Agents** — GUI/OS automation tools
- **Foundation Models** — LLMs and multimodal models

PR title: `framework: add [FrameworkName]`

---

## 🗂️ How to Propose a New Category

If your skill doesn't fit any of the 16 existing categories:

1. Open an issue with the label **`new-category`**
2. Include:
   - Proposed folder name (e.g., `17-robotics`)
   - Description of the skill family
   - At least 5 example skills that belong in it
3. A maintainer will review and approve before you create the folder

---

## 📝 Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <short description>

[optional body]
```

| Type | When to use |
|---|---|
| `feat` | New skill or category |
| `improve` | Richer content for existing skill |
| `fix` | Typo, broken link, or factual correction |
| `docs` | README, CONTRIBUTING, or meta files |
| `framework` | `meta/frameworks.md` update |
| `glossary` | `meta/glossary.md` update |
| `chore` | Maintenance (renaming, reorganizing) |

**Examples:**
```
feat: add svg-generation to 13-creative
improve: enrich chain-of-thought with LATS example
fix: correct broken link in 09-agentic-patterns/react.md
framework: add Agno to agent frameworks table
```

---

## ☑️ Pull Request Checklist

Before opening your PR, confirm:

- [ ] File is placed in the correct `skills/XX-category/` folder
- [ ] Filename uses `kebab-case.md`
- [ ] All template fields are filled in (no placeholders left)
- [ ] Code example is real and runnable
- [ ] No duplicate skill exists in the repo
- [ ] Related skills links point to real files
- [ ] PR title follows the convention above

---

## 💛 Sponsoring

If Skills Tree has saved you time or helped you design better agent systems, consider [sponsoring the project](https://github.com/sponsors/SamoTech). Sponsorships directly fund maintenance, new skill research, and tooling improvements.

---

## 🌐 Code of Conduct

Be kind, constructive, and welcoming. We follow the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) Code of Conduct. Harassment or exclusionary behavior will not be tolerated.

---

*Made with ❤️ by [Ossama Hashim](https://github.com/SamoTech) and contributors.*

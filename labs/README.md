# Labs

> **Experimental & bleeding-edge skills** — things that work but aren't yet standardized. Contribute early, shape the future.

Labs is where ideas prove themselves before graduating to `/skills`. Skills here may be incomplete, model-specific, or require cutting-edge APIs — but they're real and worth sharing.

---

## Lab Skill Lifecycle

```
labs/ → (community validation + benchmarks) → skills/
  ↑                                                ↓
  └──────── (deprecated or superseded) ───────────┘
```

A lab skill graduates to `/skills` when:
- It works on 2+ major models or frameworks
- It has a stable API / implementation
- At least one community member has used it in production

---

## Current Lab Skills

| Skill | Area | Status | Description |
|---|---|---|---|
| [Tree of Agents](reasoning/tree-of-agents.md) | reasoning | 🔬 Active | Multi-agent tree search for complex planning |
| [Episodic Compression](memory/episodic-compression.md) | memory | 🔬 Active | Lossy-but-useful memory compression — 10-15x ratio, 80%+ recall |
| [Adaptive Tool Selection](tool-use/adaptive-tool-selection.md) | tool-use | 🔬 Active | Two-stage router filters 50+ tools down to 5-8 per task, -76% token cost |

---

## Contribute to Labs

Lower bar than `/skills` — you don't need benchmarks, just a working implementation and honest notes on limitations.

```bash
cp meta/skill-template.md labs/category/my-experiment.md
# Add: **Status:** 🔬 Experimental  to the frontmatter
# PR title: lab: add [skill-name]
```

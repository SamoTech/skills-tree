# Blueprints

> **Production-ready architectures** — complete, deployable patterns for common agent system designs.

Blueprints are the "floor plans" of the Skills Tree. They go beyond individual skills and systems to describe full production stacks — with deployment guidance, scaling notes, and cost estimates.

---

## What Makes a Blueprint

A Blueprint must:

- Define a **complete deployable architecture** (not just a concept)
- Include a **component diagram** (text-based)
- Provide **technology choices** with rationale
- Cover **scaling, failure handling, and cost**
- Reference the Skills and Systems it builds on

---

## Available Blueprints

| Blueprint | Use Case | Complexity |
|---|---|---|
| [RAG Stack](rag-stack.md) | Retrieval-augmented generation in production | Intermediate |
| [Multi-Agent Workflow](multi-agent-workflow.md) | Sequential orchestration with agent handoffs | Intermediate |
| [Multi-Agent Mesh](multi-agent-mesh.md) | N specialized agents + orchestrator, parallel execution | Advanced |
| [Computer Use Browser](computer-use-browser.md) | Browser automation via Playwright + vision | Advanced |
| [Human-in-the-Loop](human-in-the-loop.md) | Approval gates + escalation + audit trail | Intermediate |
| [Self-Healing Agent](self-healing-agent.md) | Error detection + exponential retry + rollback | Advanced |
| [Memory-First Agent](memory-first-agent.md) | Profile + episodic + vector memory combined | Advanced |

---

## Contribute a Blueprint

```bash
cp meta/skill-template.md blueprints/my-blueprint.md
# PR title: blueprint: add [name]
```

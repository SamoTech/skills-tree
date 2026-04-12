# Systems

> **Multi-skill workflows** — complete, end-to-end agent implementations that combine 2+ skills to solve real problems.

Systems are the "recipes" of the Skills Tree. Where individual skill files teach you *what* a capability is, Systems show you *how to combine them* into something that ships.

---

## What Makes a System

A System file must:

- Combine **2+ skills** from the `/skills` directory
- Solve a **real, named use case** (not a toy example)
- Include a **complete, runnable implementation**
- Show the **skill flow diagram** (text-based)
- List **inputs, outputs, and failure modes**

---

## Available Systems

| System | Skills Used | Complexity |
|---|---|---|
| [Research Agent](research-agent.md) | Web search · RAG · Summarization · Citation | Intermediate |
| [Code Reviewer](code-reviewer.md) | Code reading · Reasoning · Comment generation | Intermediate |
| [Data Pipeline Agent](data-pipeline-agent.md) | DB reading · ETL · Anomaly detection · Alerting | Advanced |
| [Customer Support Bot](customer-support-bot.md) | Memory injection · Intent classification · Response gen | Intermediate |
| [Computer Use Agent](computer-use-agent.md) | Screen reading · OCR · Click · Type · Verification | Advanced |

---

## Contribute a System

```bash
cp meta/system-template.md systems/my-system.md
# Fill in all sections → open PR titled: system: add [name]
```

Quality bar: the system must be runnable end-to-end, not a diagram of boxes.

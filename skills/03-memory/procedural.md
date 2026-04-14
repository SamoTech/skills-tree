---
title: "Procedural Memory"
category: 03-memory
level: intermediate
stability: stable
description: "Apply procedural memory in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-03-memory-procedural.json)

# Procedural Memory

**Category:** `memory`  
**Skill Level:** `intermediate`  
**Stability:** `stable`  
**Added:** 2025-03  
**Last Updated:** 2026-04

---

## Description

Store, retrieve, and execute step-by-step procedures — how-to knowledge for recurring tasks. Unlike semantic memory (facts) or episodic memory (events), procedural memory captures actionable workflows: deployment runbooks, coding patterns, troubleshooting checklists, and user-specific workflows. Retrieved procedures are injected into the agent's prompt as system-level instructions.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `task` | `string` | ✅ | Task or goal to retrieve a procedure for |
| `user_id` | `string` | ❌ | User scope for personalized procedures |
| `procedure` | `dict` | ❌ | When writing: `{title, steps, tags}` |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `procedure_id` | `string` | ID of stored or retrieved procedure |
| `title` | `string` | Procedure name |
| `steps` | `list` | Ordered list of steps |
| `applicable` | `bool` | Whether a procedure was found for the task |

---

## Example

```python type:illustrative
# pip install mem0ai anthropic
# Note: `mem0` is the import name for PyPI package `mem0ai`
import anthropic
from mem0 import MemoryClient
import json

llm_client = anthropic.Anthropic()
mem_client = MemoryClient()

def store_procedure(title: str, steps: list[str], tags: list[str], user_id: str) -> str:
    """Store a how-to procedure in memory."""
    content = f"PROCEDURE: {title}\nSteps:\n" + "\n".join(f"{i+1}. {s}" for i, s in enumerate(steps))
    result = mem_client.add(
        messages=[{"role": "user", "content": content}],
        user_id=user_id,
        metadata={"type": "procedural", "tags": tags}
    )
    return result[0]["id"]

def retrieve_procedure(task: str, user_id: str) -> dict:
    """Retrieve the best matching procedure for a given task."""
    memories = mem_client.search(task, user_id=user_id, limit=3)
    procs = [m for m in memories if m.get("metadata", {}).get("type") == "procedural"]

    if not procs:
        return {"applicable": False, "steps": []}

    response = llm_client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": (
                f"Task: {task}\n"
                f"Available procedures:\n{json.dumps(procs, indent=2)}\n\n"
                "Which procedure best matches this task? Return JSON: "
                "{applicable: bool, best_match_id: str, title: str, steps: [str]}"
            )
        }]
    )
    return json.loads(response.content[0].text)

# Store a procedure
store_procedure(
    title="Deploy Next.js App to Vercel",
    steps=[
        "Run `npm run build` and confirm no errors",
        "Push latest changes to main branch",
        "Open Vercel dashboard and verify deployment triggered",
        "Check deployment logs for errors",
        "Test production URL with smoke test script"
    ],
    tags=["deployment", "vercel", "nextjs"],
    user_id="ossama"
)
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| mem0ai | `add()` + `search()` with type metadata | v1.0 |
| LangChain | `VectorStore` with procedure schema | v0.1 |
| LangGraph | Procedure retrieval node | v0.1 |

---

## Notes

- Tag procedures with domain + tool names for accurate retrieval
- Version procedures — store `version` in metadata so outdated steps can be identified
- Inject retrieved procedures into the agent system prompt, not the user turn

---

## Related Skills

- [Memory Injection](memory-injection.md) — storing memories
- [Memory Summarization](memory-summarization.md) — condensing procedure histories
- [Fact Verification](fact-verification.md) — verifying procedure steps are still accurate

---

## Changelog

| Date | Change |
|---|---|
| `2026-04` | Annotated code block as type:illustrative to clarify mem0 import name |
| `2026-04` | Fixed PyPI package name: mem0 → mem0ai |
| `2026-04` | Expanded from stub: store+retrieve pattern, versioning note, mem0 example |
| `2025-03` | Initial stub entry |

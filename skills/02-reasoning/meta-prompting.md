---
title: "Meta-Prompting"
category: 02-reasoning
level: advanced
stability: stable
description: "Use a meta-model (or meta-prompt) to dynamically generate, select, or refine prompts for a task-specific model. Enables automated prompt engineering and zero-shot task specialisation at runtime."
added: "2025-06"
version: v2
tags: [reasoning, meta-learning, prompt-generation, orchestration]
updated: "2026-06"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-meta-prompting.json)

# Meta-Prompting

## Description

Meta-Prompting (Zhang et al., 2024) operates at the prompt-construction level rather than the answer level. A **meta-model** receives a task description and generates the optimal prompt (or a set of candidate prompts) for a **task model** to execute. This creates a two-level hierarchy:

1. **Meta-level:** "Given this task, what is the best prompt to give a model to solve it?"
2. **Task-level:** The generated prompt is executed by the task model.

In production, meta-prompting is used in AutoGen's `AssistantAgent` system message generation, Semantic Kernel's planner, and DSPy's `BootstrapFewShot` optimizer.

## When to Use

- You have a diverse set of task types and can't hand-craft prompts for each.
- You want automatic prompt adaptation to user intent at runtime.
- Building multi-agent systems where agent prompts should specialise per task.
- **Don't use** when task distribution is narrow and fixed prompts are optimal.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `task_description` | `str` | Description of the task to solve |
| `constraints` | `list[str]` | Optional constraints (format, length, tone) |
| → `generated_prompt` | `str` | The meta-generated prompt |
| → `task_output` | `str` | Result of running generated prompt on task |

## Runnable Example

```python
import anthropic

client = anthropic.Anthropic()
META_MODEL = "claude-opus-4-5"
TASK_MODEL = "claude-haiku-4-5"

META_PROMPT = """You are a prompt engineering expert. Given the task description below,
write an optimal system prompt for a language model to complete this task.
Output ONLY the system prompt text, nothing else.

Task: {task_description}
Constraints: {constraints}"""

def meta_prompt_solve(task_description: str, user_input: str, constraints: list[str] | None = None) -> dict:
    constraints_str = "; ".join(constraints) if constraints else "none"

    # Step 1: Meta-model generates the prompt
    meta_resp = client.messages.create(
        model=META_MODEL, max_tokens=512,
        messages=[{"role": "user", "content": META_PROMPT.format(
            task_description=task_description, constraints=constraints_str
        )}]
    )
    generated_prompt = meta_resp.content[0].text.strip()

    # Step 2: Task model executes with generated prompt
    task_resp = client.messages.create(
        model=TASK_MODEL, max_tokens=1024,
        system=generated_prompt,
        messages=[{"role": "user", "content": user_input}]
    )
    return {"generated_prompt": generated_prompt, "task_output": task_resp.content[0].text.strip()}

if __name__ == "__main__":
    result = meta_prompt_solve(
        task_description="Extract all action items from a meeting transcript",
        user_input="Meeting notes: Alice to fix the login bug by Friday. Bob will draft the API spec.",
        constraints=["Output as JSON list", "Include owner and deadline for each item"]
    )
    print("Generated Prompt:", result["generated_prompt"][:200])
    print("Output:", result["task_output"])
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Generated prompt is too generic | Meta-model under-specified | Provide richer task description with examples |
| Task model ignores generated prompt | Weak system prompt influence | Use stronger instruction verbs; test with multiple models |
| Meta-prompt latency doubles cost | Two LLM calls | Cache generated prompts per task type |

## Production Applications

- **G08 Multi-Agent Systems:** Dynamically assign system prompts to specialised sub-agents
- **G01 Coding Agent:** Generate task-specific coding guidelines per request type
- **G02 Research Agent:** Adapt search and synthesis prompts per research domain

## Related Skills

- [Prompt Engineering](prompt-engineering.md) — prerequisite; meta-prompting automates this skill
- [ReAct Pattern](../09-agentic-patterns/react-pattern.md) — meta-prompting can generate ReAct system prompts
- [Planning Decomposition](planning-decomposition.md) — meta-prompting supports plan generation
- [Reflection](../09-agentic-patterns/reflection-pattern.md) — meta-prompting + reflection creates self-improving prompt loops

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-06 | v1 | Initial skill file |
| 2026-06 | v2 | Full runnable example, production applications, failure modes |

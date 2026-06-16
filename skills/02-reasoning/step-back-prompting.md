---
title: "Step-Back Prompting"
category: 02-reasoning
level: intermediate
stability: stable
description: "Prompt the LLM to first answer a high-level abstraction (the 'step-back' question) before solving the original task. Improves performance on multi-step reasoning by grounding the answer in principles before details."
added: "2025-06"
version: v2
tags: [reasoning, prompting, abstraction, principles]
updated: "2026-06"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-step-back-prompting.json)

# Step-Back Prompting

## Description

Step-Back Prompting (Zheng et al., 2023) instructs the model to first retrieve a high-level principle or concept relevant to the question before attempting a solution. The two-step structure is:

1. **Step-back question:** "What is the general principle or concept behind this problem?"
2. **Grounded answer:** Use the retrieved principle as context for the original answer.

On MMLU (physics, chemistry) and TimeQA benchmarks, Step-Back Prompting improved accuracy by 7-27% over direct prompting and 1-11% over Chain-of-Thought.

## When to Use

- Multi-hop questions requiring domain knowledge before specific calculation.
- Research agents that need to ground answers in principles before synthesis.
- RAG pipelines where the retrieval query benefits from abstraction before specifics.
- **Don't use** for simple factual lookups or purely procedural tasks with no principles.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `question` | `str` | The original user question |
| `domain` | `str` | Optional domain hint for better step-back generation |
| → `step_back_q` | `str` | The generated high-level question |
| → `principle` | `str` | The retrieved principle or concept |
| → `answer` | `str` | Final grounded answer |

## Runnable Example

```python
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-opus-4-5"

STEP_BACK_PROMPT = """
Given the following question, generate the step-back question that asks
about the general principle or concept needed to answer it.

Original question: {question}

Step-back question:"""

ANSWER_PROMPT = """
Principle: {principle}

Using the above principle, answer: {question}"""

def step_back_prompting(question: str) -> dict:
    # Step 1: Generate step-back question
    sb_resp = client.messages.create(
        model=MODEL, max_tokens=256,
        messages=[{"role": "user", "content": STEP_BACK_PROMPT.format(question=question)}]
    )
    step_back_q = sb_resp.content[0].text.strip()

    # Step 2: Answer the step-back question to get the principle
    principle_resp = client.messages.create(
        model=MODEL, max_tokens=512,
        messages=[{"role": "user", "content": step_back_q}]
    )
    principle = principle_resp.content[0].text.strip()

    # Step 3: Answer original with grounded principle
    final_resp = client.messages.create(
        model=MODEL, max_tokens=1024,
        messages=[{"role": "user", "content": ANSWER_PROMPT.format(
            principle=principle, question=question
        )}]
    )
    return {"step_back_q": step_back_q, "principle": principle, "answer": final_resp.content[0].text.strip()}

if __name__ == "__main__":
    q = "Why does estrogen affect bone density in post-menopausal women?"
    result = step_back_prompting(q)
    print("Step-back:", result["step_back_q"])
    print("Principle:", result["principle"][:200])
    print("Answer:", result["answer"][:200])
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Generic step-back question | Model doesn't understand domain | Provide domain hint in prompt |
| Principle contradicts answer | Model ignores grounding context | Explicitly reference principle in answer prompt |
| Extra latency not justified | Simple questions don't need abstraction | Gate on question complexity score |

## Production Applications

- **G02 Research Agent:** Abstract research questions before RAG retrieval
- **G04 RAG Assistant:** Improve retrieval query quality via abstraction layer
- **G01 Coding Agent:** Retrieve architectural principles before generating code

## Related Skills

- [Chain of Thought](../09-agentic-patterns/cot.md) — linear reasoning; Step-Back adds principled grounding
- [Prompt Engineering](prompt-engineering.md) — prerequisite skill
- [Least-to-Most Prompting](least-to-most.md) — complementary decomposition approach
- [RAG Pattern](../09-agentic-patterns/rag-pattern.md) — Step-Back improves RAG query formulation

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-06 | v1 | Initial skill file |
| 2026-06 | v2 | Added runnable example, failure modes, production applications |

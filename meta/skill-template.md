# Skill Name

> 📋 **Instructions:** Copy this file to the appropriate `skills/XX-category/` folder, rename it to `kebab-case.md`, fill in every field, and delete this instruction block before submitting.

---

**Category:** `category-slug`  
**Skill Level:** `basic` | `intermediate` | `advanced`  
**Stability:** `stable` | `experimental` | `deprecated`  
**Added:** `YYYY-MM`  
**Last Updated:** `YYYY-MM`

---

## Description

One to three sentences describing **what this skill enables an agent to do**, why it matters, and in what context it is typically used.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | ✅ | Primary instruction, query, or task payload |
| `context` | `string` | ❌ | Optional background information to guide execution |
| `options` | `dict` | ❌ | Optional configuration flags and constraints |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `result` | `string` / `object` | The primary output produced by this skill |
| `confidence` | `float` | Optional confidence score (0.0–1.0) |
| `metadata` | `dict` | Optional execution details, timing, or provenance |

---

## Example

```python
# Minimal example — replace with a real, runnable snippet
agent.skill("skill-name", input="example task")
# → "expected output"
```

```python
# Extended example with options
agent.skill(
    "skill-name",
    input="example task",
    options={"format": "json", "max_tokens": 500}
)
```

---

## Frameworks & Models

List every framework, library, or model that implements or supports this skill:

| Framework / Model | Implementation | Since |
|---|---|---|
| [LangChain](https://langchain.com) | `Tool` abstraction + `AgentExecutor` | v0.1 |
| [LangGraph](https://langchain.com/langgraph) | Node in a state graph | v0.1 |
| [AutoGen](https://microsoft.github.io/autogen) | `AssistantAgent` + `function_map` | v0.2 |
| [CrewAI](https://crewai.com) | `@tool` decorator | v0.1 |
| [OpenAI Assistants](https://platform.openai.com/docs/assistants) | Function calling / Code Interpreter | 2023-11 |
| GPT-4o | Native tool-call support | 2024-05 |
| Claude 3.7 Sonnet | Tool use via `tools` parameter | 2025-01 |

> Remove rows that do not apply. Add new rows for any framework not listed.

---

## Notes

- List any caveats, rate limits, token costs, or known edge cases.
- Note if this skill behaves differently across models (e.g., better with Claude vs. GPT).
- Mention any security or privacy considerations if applicable.

---

## Related Skills

- [Related Skill A](../XX-category/related-skill-a.md) — brief reason it's related
- [Related Skill B](../YY-category/related-skill-b.md) — brief reason it's related

---

## Changelog

| Date | Change |
|---|---|
| `YYYY-MM` | Initial entry |

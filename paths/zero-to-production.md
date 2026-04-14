# Path: From Zero to Production

**Difficulty:** ⭐ Beginner  
**Skills:** 7  
**Est. Time:** ~5 hours  
**Goal:** Build and deploy your first production-ready AI agent from scratch — covering the full lifecycle from first prompt to running system.

---

## Overview

This path is for developers who are new to agent development. You start with a single LLM call, progressively add tool use, memory, error handling, and observability, and end with a deployable agent with a simple API interface. No prior agent experience needed.

---

## Prerequisites

- Python 3.11+ and basic Python proficiency
- `pip install openai langchain langgraph fastapi uvicorn`
- An OpenAI API key
- Familiarity with REST APIs

---

## The Path

### Step 1 — Instruction Following
`skills/06-communication/instruction-following.md`

**Why first:** Before tools, memory, or orchestration — you must understand how models interpret instructions. This skill teaches prompt structure, system messages, and why models ignore or misfollow instructions.

**Key takeaways:**
- System prompt = persistent rules; user message = single-turn request
- Be explicit: "Respond only in JSON" beats "respond in a structured format"
- Test instructions with adversarial inputs before shipping

---

### Step 2 — Tool Use (Function Calling)
`skills/07-tool-use/function-calling.md`

**Why second:** Tool use is the most important agent primitive. You learn how to define tools as JSON schemas, handle the model's tool call requests, execute functions, and return results in the expected format.

**Key takeaways:**
- Tool names must be unambiguous — the model picks tools by name
- Always validate tool inputs before execution
- Return structured results, not prose — the model parses your tool output

---

### Step 3 — Working Memory
`skills/03-memory/working-memory.md`

**Why third:** Your agent now has tools. It needs a state object to carry information between tool calls within a session. This step introduces the agent state dict pattern.

**Key takeaways:**
- State is just a typed dict — keep it flat and serialisable
- Pass state through every node in your graph
- Log state transitions for debugging

---

### Step 4 — ReAct Loop
`skills/09-agentic-patterns/react-loop.md`

**Why fourth:** ReAct (Reason + Act) is the core agentic loop: think about what to do, do it, observe the result, repeat. This skill teaches you to implement a basic ReAct agent with a step budget and termination condition.

**Key takeaways:**
- Always set a max_steps limit (10-15 for most tasks)
- The "Observation" step is not optional — it closes the feedback loop
- Log every Thought/Action/Observation triple for debugging

---

### Step 5 — Error Handling
`skills/09-agentic-patterns/error-recovery.md`

**Why fifth:** Production agents fail. APIs time out, tools return errors, models hallucinate tool names. This step teaches retry logic, graceful degradation, and how to surface errors to the user without crashing.

**Key takeaways:**
- Wrap every tool call in try/except and return a structured error to the model
- Distinguish retryable errors (timeout) from terminal errors (auth failure)
- Set a global agent timeout — never let a runaway agent loop forever

---

### Step 6 — Structured Output
`skills/06-communication/structured-output.md`

**Why sixth:** Before deployment, standardise your agent's output format. Callers need predictable, parseable responses. This skill covers JSON mode, Pydantic output parsers, and output validation.

**Key takeaways:**
- Use `response_format={"type": "json_object"}` or tool-based output for reliability
- Validate output against a Pydantic schema before returning to the caller
- Always include an `error` field so callers can detect failures without parsing

---

### Step 7 — Agent Deployment
`skills/15-orchestration/agent-deployment.md`

**Why last:** Wrap your agent in a FastAPI endpoint, add basic auth, set up structured logging, and deploy to a cloud service. This skill turns your script into a production service.

**Key takeaways:**
- Use background tasks for long-running agent runs — don't block the HTTP thread
- Return a `run_id` immediately; let the caller poll for status
- Log agent runs as structured JSON for observability

---

## Code Scaffold

```python
# agent_api.py — production agent with FastAPI wrapper
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import openai, uuid, asyncio

app = FastAPI(title="My First Agent")
client = openai.AsyncOpenAI()

# ---- Tools (Step 2) ----
TOOLS = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"]
        }
    }
}]

async def get_weather(city: str) -> dict:
    """Fake tool — replace with real API call."""
    return {"city": city, "temp_c": 22, "condition": "sunny"}

# ---- ReAct loop (Step 4) ----
async def run_agent(question: str, max_steps: int = 10) -> str:
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use tools when needed. Respond in JSON: {\"answer\": \"...\"}."},
        {"role": "user",   "content": question}
    ]
    for step in range(max_steps):
        resp = await client.chat.completions.create(
            model="gpt-4o-mini", messages=messages,
            tools=TOOLS, response_format={"type": "json_object"}
        )
        msg = resp.choices[0].message
        messages.append(msg)
        if not msg.tool_calls:
            return msg.content  # Final answer
        # Execute tools (Step 2 + 5: error handling)
        for tc in msg.tool_calls:
            try:
                if tc.function.name == "get_weather":
                    import json
                    args = json.loads(tc.function.arguments)
                    result = await get_weather(**args)
                else:
                    result = {"error": f"Unknown tool: {tc.function.name}"}
            except Exception as e:
                result = {"error": str(e)}
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": str(result)})
    return '{"answer": "Max steps reached", "error": "step_limit"}'

# ---- API (Step 7) ----
class RunRequest(BaseModel):
    question: str

class RunResponse(BaseModel):
    run_id: str
    answer: Optional[str] = None
    error: Optional[str] = None

@app.post("/run", response_model=RunResponse)
async def run(req: RunRequest):
    run_id = str(uuid.uuid4())
    try:
        answer = await run_agent(req.question)
        return RunResponse(run_id=run_id, answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}

# Run: uvicorn agent_api:app --reload
```

---

## Completion Checklist

- [ ] Agent answers a question using at least one tool call
- [ ] Agent handles a tool error without crashing
- [ ] Output is valid JSON matching the Pydantic schema
- [ ] `/run` endpoint returns a response in under 10 seconds
- [ ] `/health` endpoint returns `{"status": "ok"}`
- [ ] Agent stops gracefully when max_steps is reached
- [ ] All agent steps are logged as structured JSON

---

## Next Steps

- Add persistent memory: follow the **Memory-First Agent** path
- Add web search: follow the **Research Agent** path
- Add observability with LangSmith or Langfuse
- See `blueprints/` for production architecture patterns

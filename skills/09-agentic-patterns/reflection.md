---
title: "Reflection / Reflexion"
category: 09-agentic-patterns
level: advanced
stability: stable
description: "After producing an answer or executing a step, the agent critiques its own output and revises. Closes the loop on first-try mistakes that no amount of better prompting can fix."
added: "2025-03"
version: v3
tags: [reasoning, self-critique, revision, agent-loop]
updated: "2026-04"
dependencies:
  - package: anthropic
    min_version: "0.39.0"
    tested_version: "0.39.0"
    confidence: verified
code_blocks:
  - id: "example-reflection"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-reflection.json)

# Reflection / Reflexion

## Description

Reflection adds a **critique → revise** pass on top of any agent output. The model produces a draft, then a second prompt asks it (or a stronger model) to find flaws — wrong reasoning, hallucinated facts, missed constraints — and rewrite. Reflexion ([Shinn et al., 2023](https://arxiv.org/abs/2303.11366)) generalises this into a loop: store self-critiques in memory, retry the task, do better next time.

This skill is the foundation of every agent that *recovers from its own first-try mistakes* — code agents that fix lint errors before submitting, planners that re-plan when a step fails, writers that revise drafts.

## When to Use

- Tasks where the **first answer is often wrong but a fix is cheap** (code, math proofs, structured output validation).
- You have a verifier signal — failing tests, schema errors, retrieval mismatch — that the critique can ground itself in.
- Latency budget allows ≥2 model calls per task.
- **Don't use** when the underlying error is information you don't have (no amount of reflection invents missing facts).

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `task` | `str` | The original instruction |
| `draft` | `str` | First-pass output |
| `verifier` | `Callable[[str], str \| None]` | Returns `None` on pass, error string on fail |
| `max_rounds` | `int` | Hard cap on revise iterations (default 3) |
| → `final` | `str` | Last accepted output |
| → `history` | `list[Round]` | Per-round draft + critique + verifier result |

## Runnable Example

```python
# pip install anthropic
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-opus-4-5"

@dataclass
class Round:
    draft: str
    critique: str
    verifier_error: str | None

def _ask(system: str, user: str) -> str:
    r = client.messages.create(
        model=MODEL, max_tokens=1024,
        system=system, messages=[{"role": "user", "content": user}],
    )
    return r.content[0].text

def reflect(
    task: str,
    initial_draft: str,
    verifier: Callable[[str], str | None],
    max_rounds: int = 3,
) -> dict:
    rounds: list[Round] = []
    draft = initial_draft
    for _ in range(max_rounds):
        err = verifier(draft)
        if err is None:
            rounds.append(Round(draft, "(passed verifier — no revision)", None))
            return {"final": draft, "history": rounds}

        critique = _ask(
            "You are a strict code reviewer. Identify exactly what is wrong "
            "with the candidate output relative to the task and the verifier "
            "error. Be concrete; quote the offending fragment.",
            f"TASK:\n{task}\n\nCANDIDATE:\n{draft}\n\nVERIFIER ERROR:\n{err}",
        )
        revised = _ask(
            "Rewrite the candidate to fix the issues raised in the critique. "
            "Output ONLY the revised answer, no preamble.",
            f"TASK:\n{task}\n\nCANDIDATE:\n{draft}\n\nCRITIQUE:\n{critique}",
        )
        rounds.append(Round(draft, critique, err))
        draft = revised
    return {"final": draft, "history": rounds}

# Demo: a tiny verifier that requires the JSON to contain a "skills" key.
import json
def verifier(s: str) -> str | None:
    try:
        obj = json.loads(s)
    except Exception as e:
        return f"not valid JSON: {e}"
    if "skills" not in obj:
        return "missing required key 'skills'"
    return None

if __name__ == "__main__":
    bad = '{"items": ["a","b"]}'
    out = reflect("Return JSON with a 'skills' key listing items.", bad, verifier)
    print(out["final"])
    print(f"{len(out['history'])} round(s)")
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Reflection makes the answer worse | Critique is overconfident; introduces a regression | Run the verifier on the revision; **never** accept a worse output |
| Infinite revise loop | Verifier never converges | Hard `max_rounds` + accept best-by-verifier-score draft on exhaustion |
| Critique hallucinates problems | Model invents bugs that aren't there | Ground the critique in concrete verifier output, not "look for issues" |
| Self-judge bias | Same model can't see its own blind spots | Use a stronger or differently-trained model as the critic |
| Budget blow-up | Each round = 2 calls | Skip critique when verifier already passes; cache stable inputs |

## Frameworks & Models

| Framework | Notes |
|---|---|
| **Reflexion** (paper) | Stores critiques as long-term memory, retries similar tasks |
| **DSPy `Refine`** | Programmatic revise pipeline |
| **LangGraph** | `branch_on_verifier_failure` pattern |
| **Self-Discover** ([Zhou et al.](https://arxiv.org/abs/2402.03620)) | Generates the *reasoning structure* to reflect on |

## Model Comparison

| Capability | claude-opus-4-5 | gpt-4o | claude-sonnet-4-5 |
|---|---|---|---|
| Faithful self-critique | 5 | 4 | 4 |
| Revision quality | 5 | 5 | 4 |
| Cost per round | 2 | 3 | 4 |
| Latency per round | 3 | 4 | 4 |

## Related Skills

- [Chain of Thought](cot.md) — useful as the *draft* step
- [Tree of Thought](tot.md) — branch instead of revise
- [Planning](../02-reasoning/planning.md) — re-plan on verifier failure
- [Self-Consistency](../02-reasoning/self-consistency.md) — sample many drafts instead

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Initial stub |
| 2026-04 | v3 | Battle-tested: critique→revise loop, verifier integration, failure modes, model comparison |

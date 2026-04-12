---
Category: Reasoning
Skill Level: Advanced
Stability: Stable
Tags: [cot, prompting, step-by-step, reasoning, scratchpad]
---

# Chain-of-Thought Reasoning

### Description
Elicits intermediate reasoning steps from a language model before producing a final answer. CoT dramatically improves accuracy on multi-step arithmetic, logical deduction, and complex planning tasks by forcing the model to externalize its reasoning trace. Variants include zero-shot CoT ("think step by step"), few-shot CoT (exemplars), self-consistency CoT (majority vote), and program-of-thought (code as reasoning).

### When to Use
- Multi-step math or algorithmic problems where intermediate steps matter
- Logical deduction chains (syllogisms, constraint propagation, causal chains)
- Any task where accuracy is more important than latency
- As the first reasoning layer in agentic pipelines before tool calls

### Example
```python
from openai import OpenAI

client = OpenAI()

SYSTEM = """You are a precise reasoning assistant. For every problem:
1. Restate what is being asked.
2. List all given facts and constraints.
3. Work through the solution step by step, showing every calculation.
4. State your final answer clearly on a line starting with 'Answer:'."""

def cot_solve(problem: str, n_samples: int = 5) -> str:
    """Self-consistency CoT: sample n times, return majority answer."""
    from collections import Counter
    answers = []
    for _ in range(n_samples):
        r = client.chat.completions.create(
            model="o3",
            messages=[{"role": "system", "content": SYSTEM},
                      {"role": "user", "content": problem}],
            temperature=0.7
        )
        text = r.choices[0].message.content
        ans_line = next((l for l in text.splitlines() if l.startswith("Answer:")), text)
        answers.append(ans_line.replace("Answer:", "").strip())
    most_common = Counter(answers).most_common(1)[0][0]
    return most_common
```

### Advanced Techniques
- **Program-of-Thought**: generate Python code as the reasoning trace, execute it, return result
- **Process Reward Models (PRM)**: score each reasoning step independently to detect errors early
- **Auto-CoT**: cluster training problems and auto-generate diverse exemplars for few-shot CoT
- **Least-to-Most prompting**: decompose into easier sub-problems, solve sequentially, compose answer

### Related Skills
- `tree-of-thought`, `self-reflection`, `task-decomposition`, `mathematical-reasoning`, `react`

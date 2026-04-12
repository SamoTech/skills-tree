**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Surveys and synthesises a body of academic literature into a coherent narrative covering themes, methodological trends, conflicting findings, and open research gaps. Produces structured section outlines suitable for grant proposals or survey papers.

### Example
```python
import anthropic

client = anthropic.Anthropic()

def literature_review(topic: str, papers: list[dict]) -> str:
    refs = "\n".join(f"- {p['title']} ({p['year']}): {p['tldr']}" for p in papers)
    prompt = (
        f"Write a structured literature review on '{topic}' using these sources.\n"
        "Sections: 1) Overview, 2) Key Themes, 3) Methodological Approaches, "
        "4) Conflicting Findings, 5) Research Gaps.\n\nSources:\n" + refs
    )
    resp = client.messages.create(
        model="claude-opus-4-5", max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.content[0].text

papers = [
    {"title": "Chain-of-Thought Prompting", "year": 2022, "tldr": "CoT improves multi-step reasoning"},
    {"title": "Tree of Thoughts", "year": 2023, "tldr": "ToT enables lookahead search in LLMs"},
]
print(literature_review("LLM reasoning strategies", papers))
```

### Related Skills
- [Paper Summarization](paper-summarization.md)
- [Hypothesis Generation](hypothesis-generation.md)
- [RAG](../03-memory/rag.md)

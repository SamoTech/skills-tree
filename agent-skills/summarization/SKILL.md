---
name: summarization
description: Summarize long documents or conversation threads in AI agent workflows.
metadata:
  source: skills/06-communication/summarization.md
  category: 06-communication
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-06-communication-summarization.json)

# Summarization
Category: communication | Level: intermediate | Stability: stable | Version: v1

## Description
Condense long-form content (documents, threads, transcripts) into concise, structured summaries. Supports map-reduce and refine strategies for documents that exceed context window limits.

## Inputs
- `content`: string or list of strings to summarize
- `style`: `"bullet"` | `"paragraph"` | `"tldr"`
- `max_words`: optional length constraint

## Outputs
- Summary string in the requested style

## Example
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template(
    "Summarize the following in {style} format:\n\n{content}"
)
chain = prompt | llm

def summarize(content, style="bullet"):
    return chain.invoke({"content": content, "style": style}).content
```

## Frameworks
| Framework | Method |
|---|---|
| LangChain | `load_summarize_chain`, map-reduce / refine |
| LlamaIndex | `TreeSummarize`, `CompactAndRefine` |
| OpenAI | direct `gpt-4o` / `gpt-4o-mini` with system prompt |

## Dependencies
- package: langchain-openai
  tested_version: "0.3.16"
  confidence: verified
  notes: "Patched GHSA-r7w7-9xr2-qq2r. Use langchain-openai>=0.3.16."
- package: langchain-core
  tested_version: "0.3.55"
  confidence: verified
  notes: "Patched GHSA-pjwx-r37v-7724 (arbitrary code execution via unsafe deserialization). Use langchain-core>=0.3.55."

## Failure Modes
- Context window overflow on very long documents — use chunked map-reduce
- Hallucinated facts in summaries — add grounding/citation prompts

## Related
- `text-reading.md` · `rag.md` · `plan-and-execute.md`

## Changelog
- v1 (2026-02): Initial entry
- v1.1 (2026-05): Bump langchain-openai to 0.3.16 + langchain-core to 0.3.55 (CVE patches)

## Evidence
The canonical skill file is the authoritative repository implementation. Repository schema, validation workflows, and the Agent Skills projection contract define structural conformance. Implementation guidance must remain traceable to supplied or independently verified authoritative sources; no benchmark claim is made without reproducible evidence.

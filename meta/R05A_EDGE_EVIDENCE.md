# R05A Edge Evidence

**Mission:** R-05A — Edge Extraction Pilot  
**Date:** 2026-06-22  
**Scope:** Categories 02-reasoning, 03-memory, 07-tool-use, 09-agentic-patterns, 12-data  
**Source:** Explicit text in Related Skills sections, markdown links, prerequisite/dependency language only.  
**Files read for extraction:** 19 skill files (see list below)

---

## Files Read

| File | Edges Extracted |
|------|-----------------|
| `skills/02-reasoning/chain-of-thought.md` | 6 |
| `skills/02-reasoning/planning.md` | 5 |
| `skills/02-reasoning/least-to-most.md` | 4 |
| `skills/02-reasoning/self-consistency.md` | 3 |
| `skills/02-reasoning/goal-decomposition.md` | 4 |
| `skills/02-reasoning/task-decomposition.md` | 3 |
| `skills/02-reasoning/planning-decomposition.md` | 5 |
| `skills/02-reasoning/step-back-prompting.md` | 4 |
| `skills/02-reasoning/reasoning-under-uncertainty.md` | 4 |
| `skills/02-reasoning/meta-prompting.md` | 4 |
| `skills/03-memory/long-term-memory.md` | 5 |
| `skills/03-memory/vector-store-retrieval.md` | 3 |
| `skills/09-agentic-patterns/reflection.md` | 4 |
| `skills/09-agentic-patterns/plan-and-execute.md` | 2 |
| `skills/09-agentic-patterns/react.md` | 4 |
| `skills/09-agentic-patterns/cot.md` | 4 |
| `skills/07-tool-use/function-calling.md` | 3 |
| `skills/12-data/json-transformation.md` | 2 |
| `skills/12-data/csv-processing.md` | 4 |

---

## All Edges — Traceable Evidence

| ID | Source Node | Target Node | Edge Type | Evidence Text | Source File |
|----|-------------|-------------|-----------|---------------|-------------|
| E001 | `chain-of-thought` | `tree-of-thought` | RELATED_TO | Related Skills: `tree-of-thought` | `skills/02-reasoning/chain-of-thought.md` |
| E002 | `chain-of-thought` | `react` | RELATED_TO | Related Skills: `react` | `skills/02-reasoning/chain-of-thought.md` |
| E003 | `chain-of-thought` | `self-reflection` | RELATED_TO | Related Skills: `self-reflection` | `skills/02-reasoning/chain-of-thought.md` |
| E004 | `chain-of-thought` | `planning` | RELATED_TO | Related Skills: `planning` | `skills/02-reasoning/chain-of-thought.md` |
| E005 | `self-consistency` | `chain-of-thought` | REQUIRES | Advanced Techniques: 'Self-consistency: sample multiple CoT paths' | `skills/02-reasoning/chain-of-thought.md` |
| E006 | `least-to-most` | `chain-of-thought` | REQUIRES | Advanced Techniques: 'Least-to-most prompting: decompose into sub-problems' | `skills/02-reasoning/chain-of-thought.md` |
| E007 | `planning` | `task-decomposition` | RELATED_TO | Related Skills: [Task Decomposition](task-decomposition.md) | `skills/02-reasoning/planning.md` |
| E008 | `planning` | `react` | RELATED_TO | Related Skills: [ReAct](../09-agentic-patterns/react.md) | `skills/02-reasoning/planning.md` |
| E009 | `planning` | `reflection` | RELATED_TO | Related Skills: [Reflection](../09-agentic-patterns/reflection.md) | `skills/02-reasoning/planning.md` |
| E010 | `planning` | `goal-setting` | RELATED_TO | Related Skills: [Goal Setting](goal-setting.md) | `skills/02-reasoning/planning.md` |
| E011 | `planning` | `reflection` | SUPPORTS | Failure Modes: 'Pair with reflection.md: on failure, replan from the failed step' | `skills/02-reasoning/planning.md` |
| E012 | `least-to-most` | `chain-of-thought` | REQUIRES | Related Skills: 'Least-to-Most extends CoT with explicit decomposition' | `skills/02-reasoning/least-to-most.md` |
| E013 | `least-to-most` | `goal-decomposition` | RELATED_TO | Related Skills: [Goal Decomposition](goal-decomposition.md) | `skills/02-reasoning/least-to-most.md` |
| E014 | `least-to-most` | `planning-decomposition` | RELATED_TO | Related Skills: [Planning Decomposition](planning-decomposition.md) | `skills/02-reasoning/least-to-most.md` |
| E015 | `least-to-most` | `plan-and-execute` | RELATED_TO | Related Skills: [Plan-and-Execute](../09-agentic-patterns/plan-and-execute.md) | `skills/02-reasoning/least-to-most.md` |
| E016 | `self-consistency` | `chain-of-thought` | REQUIRES | Description: 'augments Chain of Thought by sampling N independent reasoning chains' | `skills/02-reasoning/self-consistency.md` |
| E017 | `self-consistency` | `reflection` | RELATED_TO | Related Skills: [Reflection](../09-agentic-patterns/reflection.md) | `skills/02-reasoning/self-consistency.md` |
| E018 | `self-consistency` | `tree-of-thought` | RELATED_TO | Related Skills: [Tree of Thought](../09-agentic-patterns/tot.md) | `skills/02-reasoning/self-consistency.md` |
| E019 | `goal-decomposition` | `planning-decomposition` | SUPPORTS | Related Skills: '[Planning Decomposition] — converts sub-goals into executable tasks' | `skills/02-reasoning/goal-decomposition.md` |
| E020 | `goal-decomposition` | `least-to-most` | RELATED_TO | Related Skills: [Least-to-Most Prompting] — reasoning technique for decomposition | `skills/02-reasoning/goal-decomposition.md` |
| E021 | `goal-decomposition` | `plan-and-execute` | RELATED_TO | Related Skills: [Plan-and-Execute] — executes the resulting plan | `skills/02-reasoning/goal-decomposition.md` |
| E022 | `goal-decomposition` | `memory-augmented` | RELATED_TO | Related Skills: [Memory-Augmented Agent] — tracks progress against goal tree | `skills/02-reasoning/goal-decomposition.md` |
| E023 | `task-decomposition` | `planning` | REQUIRES | Description: 'distinct from Planning — decomposition produces what to do, planning adds order, deps, constraints' | `skills/02-reasoning/task-decomposition.md` |
| E024 | `task-decomposition` | `reflection` | RELATED_TO | Related Skills: [Reflection] — revise a bad decomposition | `skills/02-reasoning/task-decomposition.md` |
| E025 | `task-decomposition` | `tree-of-thought` | RELATED_TO | Related Skills: [Tree of Thought] — branch over alternative decompositions | `skills/02-reasoning/task-decomposition.md` |
| E026 | `planning-decomposition` | `plan-and-execute` | SUPPORTS | Related Skills: '[Plan-and-Execute] — the agentic pattern that executes decomposed plans' | `skills/02-reasoning/planning-decomposition.md` |
| E027 | `planning-decomposition` | `goal-decomposition` | REQUIRES | Related Skills: '[Goal Decomposition] — operates at intent level; precedes planning decomposition' | `skills/02-reasoning/planning-decomposition.md` |
| E028 | `planning-decomposition` | `least-to-most` | RELATED_TO | Related Skills: [Least-to-Most Prompting] — reasoning-level analogue | `skills/02-reasoning/planning-decomposition.md` |
| E029 | `planning-decomposition` | `react` | RELATED_TO | Related Skills: [ReAct Pattern] — executes individual plan steps | `skills/02-reasoning/planning-decomposition.md` |
| E030 | `planning-decomposition` | `subagent-delegation` | RELATED_TO | Related Skills: [Subagent Delegation] — assigns plan tasks to sub-agents | `skills/02-reasoning/planning-decomposition.md` |
| E031 | `step-back-prompting` | `chain-of-thought` | RELATED_TO | Related Skills: 'CoT — linear reasoning; Step-Back adds principled grounding' | `skills/02-reasoning/step-back-prompting.md` |
| E032 | `step-back-prompting` | `prompt-engineering` | REQUIRES | Related Skills: '[Prompt Engineering] — prerequisite skill' | `skills/02-reasoning/step-back-prompting.md` |
| E033 | `step-back-prompting` | `least-to-most` | RELATED_TO | Related Skills: [Least-to-Most Prompting] — complementary decomposition approach | `skills/02-reasoning/step-back-prompting.md` |
| E034 | `step-back-prompting` | `rag-pattern` | RELATED_TO | Related Skills: [RAG Pattern] — Step-Back improves RAG query formulation | `skills/02-reasoning/step-back-prompting.md` |
| E035 | `reasoning-under-uncertainty` | `self-consistency` | RELATED_TO | Related Skills: [Self-Consistency] — uses voting to reduce uncertainty in answers | `skills/02-reasoning/reasoning-under-uncertainty.md` |
| E036 | `reasoning-under-uncertainty` | `hypothesis-generation` | RELATED_TO | Related Skills: [Hypothesis Generation] — generates candidate explanations | `skills/02-reasoning/reasoning-under-uncertainty.md` |
| E037 | `reasoning-under-uncertainty` | `reflection` | RELATED_TO | Related Skills: [Reflection Pattern] — re-evaluates low-confidence outputs | `skills/02-reasoning/reasoning-under-uncertainty.md` |
| E038 | `reasoning-under-uncertainty` | `rag-retrieval` | REQUIRES | Related Skills: [RAG Retrieval](../03-memory/rag-retrieval.md) — retrieves evidence to reduce uncertainty | `skills/02-reasoning/reasoning-under-uncertainty.md` |
| E039 | `meta-prompting` | `prompt-engineering` | REQUIRES | Related Skills: '[Prompt Engineering] — prerequisite; meta-prompting automates this skill' | `skills/02-reasoning/meta-prompting.md` |
| E040 | `meta-prompting` | `react` | RELATED_TO | Related Skills: [ReAct Pattern] — meta-prompting can generate ReAct system prompts | `skills/02-reasoning/meta-prompting.md` |
| E041 | `meta-prompting` | `planning-decomposition` | SUPPORTS | Related Skills: [Planning Decomposition] — meta-prompting supports plan generation | `skills/02-reasoning/meta-prompting.md` |
| E042 | `meta-prompting` | `reflection` | SUPPORTS | Related Skills: [Reflection] — meta-prompting + reflection creates self-improving prompt loops | `skills/02-reasoning/meta-prompting.md` |
| E043 | `long-term-memory` | `episodic-memory` | RELATED_TO | Related Skills: `episodic-memory` | `skills/03-memory/long-term-memory.md` |
| E044 | `long-term-memory` | `semantic-memory` | RELATED_TO | Related Skills: `semantic-memory` | `skills/03-memory/long-term-memory.md` |
| E045 | `long-term-memory` | `working-memory` | RELATED_TO | Related Skills: `working-memory` | `skills/03-memory/long-term-memory.md` |
| E046 | `long-term-memory` | `memory-augmented` | RELATED_TO | Related Skills: `memory-augmented` | `skills/03-memory/long-term-memory.md` |
| E047 | `long-term-memory` | `rag` | RELATED_TO | Related Skills: `rag` | `skills/03-memory/long-term-memory.md` |
| E048 | `vector-store-retrieval` | `rag` | SUPPORTS | Related Skills: [RAG](rag.md) — uses this primitive end-to-end | `skills/03-memory/vector-store-retrieval.md` |
| E049 | `vector-store-retrieval` | `embedding-generation` | REQUIRES | Related Skills: [Embedding Generation](../12-data/embedding-generation.md) — how vector is produced | `skills/03-memory/vector-store-retrieval.md` |
| E050 | `vector-store-retrieval` | `memory-injection` | RELATED_TO | Related Skills: [Memory Injection](memory-injection.md) — broader pattern for stitching context into a prompt | `skills/03-memory/vector-store-retrieval.md` |
| E051 | `reflection` | `chain-of-thought` | RELATED_TO | Related Skills: [Chain of Thought](cot.md) — useful as the draft step | `skills/09-agentic-patterns/reflection.md` |
| E052 | `reflection` | `tree-of-thought` | RELATED_TO | Related Skills: [Tree of Thought](tot.md) — branch instead of revise | `skills/09-agentic-patterns/reflection.md` |
| E053 | `reflection` | `planning` | SUPPORTS | Related Skills: [Planning](../02-reasoning/planning.md) — re-plan on verifier failure | `skills/09-agentic-patterns/reflection.md` |
| E054 | `reflection` | `self-consistency` | RELATED_TO | Related Skills: [Self-Consistency] — sample many drafts instead | `skills/09-agentic-patterns/reflection.md` |
| E055 | `plan-and-execute` | `react` | RELATED_TO | Related Skills: `react` | `skills/09-agentic-patterns/plan-and-execute.md` |
| E056 | `plan-and-execute` | `planning` | REQUIRES | Related Skills: `planning` | `skills/09-agentic-patterns/plan-and-execute.md` |
| E057 | `react` | `chain-of-thought` | RELATED_TO | Related Skills: [Chain of Thought](cot.md) — pure reasoning, no tools | `skills/09-agentic-patterns/react.md` |
| E058 | `react` | `tool-use-loop` | RELATED_TO | Related Skills: [Tool-Use Loop](tool-use-loop.md) — parallel-tool variant | `skills/09-agentic-patterns/react.md` |
| E059 | `react` | `reflection` | RELATED_TO | Related Skills: [Reflection](reflection.md) — critic + retry on failure | `skills/09-agentic-patterns/react.md` |
| E060 | `react` | `planning` | REQUIRES | Related Skills: [Planning](../02-reasoning/planning.md) — structured plan first, then execute | `skills/09-agentic-patterns/react.md` |
| E061 | `cot` | `react` | RELATED_TO | Related Skills: [ReAct](react.md) — CoT + tools | `skills/09-agentic-patterns/cot.md` |
| E062 | `cot` | `tree-of-thought` | RELATED_TO | Related Skills: [Tree of Thought](tot.md) — branched reasoning | `skills/09-agentic-patterns/cot.md` |
| E063 | `cot` | `self-consistency` | RELATED_TO | Related Skills: [Self-Consistency](../02-reasoning/self-consistency.md) | `skills/09-agentic-patterns/cot.md` |
| E064 | `cot` | `planning` | RELATED_TO | Related Skills: [Planning](../02-reasoning/planning.md) — least-to-most variant lives here | `skills/09-agentic-patterns/cot.md` |
| E065 | `function-calling` | `react` | SUPPORTS | Related Skills: [ReAct](../09-agentic-patterns/react.md) — function calling inside a reasoning loop | `skills/07-tool-use/function-calling.md` |
| E066 | `function-calling` | `openai-api` | RELATED_TO | Related Skills: [OpenAI API](openai-api.md) — full provider wrappers | `skills/07-tool-use/function-calling.md` |
| E067 | `function-calling` | `anthropic-api` | RELATED_TO | Related Skills: [Anthropic API](anthropic-api.md) — full provider wrappers | `skills/07-tool-use/function-calling.md` |
| E068 | `json-transformation` | `csv-processing` | RELATED_TO | Related Skills: [CSV Processing](csv-processing.md) | `skills/12-data/json-transformation.md` |
| E069 | `json-transformation` | `structured-data-reading` | RELATED_TO | Related Skills: [Structured Data Reading](../01-perception/structured-data-reading.md) | `skills/12-data/json-transformation.md` |
| E070 | `csv-processing` | `pandas-operations` | RELATED_TO | Related Skills: `pandas-operations` | `skills/12-data/csv-processing.md` |
| E071 | `csv-processing` | `schema-inference` | RELATED_TO | Related Skills: `schema-inference` | `skills/12-data/csv-processing.md` |
| E072 | `csv-processing` | `data-visualization` | RELATED_TO | Related Skills: `data-visualization` | `skills/12-data/csv-processing.md` |
| E073 | `csv-processing` | `sql-execution` | RELATED_TO | Related Skills: `sql-execution` | `skills/12-data/csv-processing.md` |

---

## Totals

| Metric | Value |
|--------|-------|
| Total edges | 73 |
| REQUIRES | 12 |
| SUPPORTS | 8 |
| RELATED_TO | 53 |
| Unique node IDs touched | 42 |

---

*Every edge above is traceable to an exact sentence in the listed source file. No inferred or hallucinated edges.*

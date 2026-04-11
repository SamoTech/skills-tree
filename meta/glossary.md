# 📖 Glossary

Key terms, acronyms, and concepts used throughout the Skills Tree. Terms are listed alphabetically within sections.

> 💡 Missing a term? Open a PR editing this file — see [CONTRIBUTING.md](../CONTRIBUTING.md).

---

## 🤖 Core Agent Concepts

| Term | Definition |
|---|---|
| **Action** | A concrete operation performed by an agent in the world (e.g., click, API call, file write) |
| **Agent** | An AI system that perceives its environment, reasons about it, and takes actions to achieve a goal |
| **Agentic Loop** | The core cycle agents run: perceive → reason → act → observe → repeat |
| **Autonomy Level** | How independently an agent operates: from copilot (human-in-loop) to fully autonomous |
| **Computer Use** | The ability of an agent to interact with GUIs, desktop apps, and OS-level interfaces |
| **Environment** | The external context the agent can observe and interact with (file system, web, APIs, OS) |
| **Grounding** | Connecting abstract language understanding to real-world references (files, URLs, database rows) |
| **Orchestration** | Coordinating multiple agents or tools to complete a complex, multi-step task |
| **Perception** | The ability to read and interpret inputs: text, images, audio, files, screen state |
| **Reasoning** | The ability to think, plan, and decide — typically via CoT, ReAct, or MCTS |
| **Skill** | A discrete, reusable capability an agent can invoke to complete a subtask |
| **Task Decomposition** | Breaking a high-level goal into smaller, manageable sub-tasks |
| **Tool** | An external function, API, or service the agent can call to extend its capabilities |

---

## 🧠 Memory & Retrieval

| Term | Definition |
|---|---|
| **Context Window** | The maximum number of tokens an LLM can process in a single inference call |
| **Embedding** | A fixed-size vector representation of text or data, used for semantic similarity search |
| **Episodic Memory** | Memory of specific past events or interactions, indexed by time |
| **Forgetting** | Deliberate pruning or decay of stale memories to keep context focused and efficient |
| **Long-term Memory** | Persistent storage that survives across sessions — typically a vector store or database |
| **Memory Injection** | Inserting retrieved memories into the prompt context before inference |
| **Procedural Memory** | Stored step-by-step procedures and workflows the agent has learned |
| **RAG** | Retrieval-Augmented Generation — fetching relevant documents before generating an answer |
| **Semantic Memory** | General factual knowledge stored independently of specific events |
| **Short-term Memory** | In-context information limited to the current conversation or task window |
| **Vector Store** | A database optimized for approximate nearest-neighbor search over embeddings |
| **Working Memory** | The active subset of information held in context during a task |

---

## 💬 Language & Inference

| Term | Definition |
|---|---|
| **Chain-of-Thought (CoT)** | A prompting technique that instructs the model to reason step-by-step before answering |
| **Context Stuffing** | Inserting large amounts of retrieved text into the context window to ground responses |
| **Few-shot** | Prompting with a small number of examples to guide the model's output format or style |
| **Fine-tuning** | Further training a pre-trained model on task-specific data to improve performance |
| **Function Calling** | A model feature for emitting structured JSON to invoke external tools or APIs |
| **Hallucination** | When a model generates plausible-sounding but factually incorrect or fabricated content |
| **LLM** | Large Language Model — the core neural reasoning engine powering most modern agents |
| **Prompt** | The input instruction or context given to an LLM to elicit a response |
| **Prompt Engineering** | The practice of crafting effective prompts to elicit desired model behavior |
| **Structured Output** | Model responses constrained to a specific schema (JSON, XML, etc.) via grammar or logit bias |
| **System Prompt** | A special prompt segment that sets persistent instructions, persona, or constraints for an LLM |
| **Temperature** | A sampling parameter controlling output randomness: 0 = deterministic, 1+ = creative |
| **Token** | The atomic unit of text an LLM processes — roughly 0.75 words in English |
| **Tool Call** | A structured invocation of an external function emitted by the model during generation |
| **Zero-shot** | Prompting a model to perform a task with no in-context examples |

---

## 🔁 Agentic Patterns

| Term | Definition |
|---|---|
| **A2A** | Agent-to-Agent protocol — a standard for agents to discover and communicate with each other |
| **Constitutional AI** | A technique for training agents to follow a set of principles via self-critique and revision |
| **LATS** | Language Agent Tree Search — combining MCTS with LLM reasoning for planning |
| **MCP** | Model Context Protocol — Anthropic's standard for connecting agents to external tools and data |
| **MCTS** | Monte Carlo Tree Search — a tree-based planning algorithm used in advanced agent reasoning |
| **Mixture of Agents** | Using multiple specialized agents whose outputs are aggregated by a router or aggregator |
| **Multi-agent System** | A setup where multiple AI agents collaborate, compete, or specialize to solve tasks |
| **Plan-and-Execute** | An agentic pattern where a planner creates a full plan upfront, then an executor runs each step |
| **ReAct** | Reasoning + Acting — agents interleave internal thought steps with tool-call actions |
| **Reflection** | An agent pausing to critique and revise its own output before finalizing it |
| **ReWOO** | Reasoning WithOut Observation — pre-planning all tool calls before executing any |
| **Sandbox** | An isolated execution environment for running untrusted or risky code safely |
| **Self-Correction** | An agent detecting an error in its output and automatically repairing it |
| **Subagent** | A specialized agent spawned by an orchestrator to handle a specific subtask |
| **Tree of Thought (ToT)** | Exploring multiple reasoning branches simultaneously and selecting the best path |

---

## 🔒 Safety & Security

| Term | Definition |
|---|---|
| **Alignment** | Ensuring an agent's goals and behavior match the intentions and values of its designers |
| **Guardrails** | Hard constraints placed on an agent's actions or outputs to prevent harm |
| **Human-in-the-Loop** | A design pattern where a human must approve or review before the agent proceeds |
| **Input Sanitization** | Validating and cleaning agent inputs to prevent injection attacks or prompt manipulation |
| **Jailbreak** | An adversarial prompt designed to bypass an agent's safety guardrails |
| **Permission Scoping** | Limiting which tools or resources an agent can access based on task context |
| **Prompt Injection** | Malicious content in external data designed to hijack agent instructions |
| **Rate Limiting** | Capping how many tool calls or API requests an agent can make per unit time |
| **Rollback** | Reversing actions taken by an agent when an error or unintended consequence is detected |

---

*Last updated: April 2026. Suggest additions via PR or [open an issue](https://github.com/SamoTech/skills-tree/issues).*

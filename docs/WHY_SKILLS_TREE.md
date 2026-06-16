# Why Skills Tree?

> The problem with AI agent development isn’t model intelligence — it’s skill chaos.

## The Problem

Every team building AI agents reinvents the same wheel: they enumerate capabilities informally in a wiki, a spreadsheet, a Notion doc, or a Confluence page. Then three months later, two agents implement the same “memory” capability in completely different ways. One uses vector search. One uses Redis. Neither team knows about the other until a system integration meeting.

The deeper problem: **there is no shared vocabulary for what AI agents can do**.

Without a shared vocabulary:
- Agent teams can’t communicate about capabilities
- Orchestration layers can’t route tasks to the right specialist agent
- Developers can’t discover which existing skill to reuse
- Learners have no map of what to learn next
- LLMs hallucinate skill names that don’t correspond to real implementations

## Target Audience

| Audience | How Skills Tree Helps |
|---|---|
| **AI agent builders** | Canonical skill IDs, versioned implementations, and benchmarks to copy-paste |
| **Orchestration engineers** | A taxonomy-driven routing layer — skills expose typed I/O, agents declare their skills |
| **Developer educators** | A curriculum map: 515+ skills organized from foundational to expert, with progression paths |
| **Researchers** | A structured dataset for agent capability studies and benchmark design |
| **Enterprise architects** | A governance layer — standardize what “memory”, “reasoning”, and “planning” mean in your org |
| **MCP server authors** | A registry of tools your server should expose, with schemas and examples |

## Competitive Positioning

| | Skills Tree | LangChain Hub | Hugging Face Hub | Custom wiki |
|---|---|---|---|---|
| Skills taxonomy | ✅ Structured, versioned | ❌ Prompts only | ❌ Models only | ⚠️ Ad hoc |
| Versioned quality tiers | ✅ v1/v2/v3 | ❌ | ❌ | ❌ |
| CLI + Python API | ✅ | ⚠️ Limited | ⚠️ Limited | ❌ |
| MCP server built-in | ✅ | ❌ | ❌ | ❌ |
| Dependency graph | ✅ Prerequisite chains | ❌ | ❌ | ❌ |
| Runnable code examples | ✅ | ⚠️ Prompts | ❌ | ⚠️ Varies |
| Open source, self-hostable | ✅ MIT | ⚠️ Partial | ⚠️ Partial | ✅ |
| Benchmark data | ✅ | ❌ | ⚠️ Model cards | ❌ |

## Unique Advantages

### 1. Versioned Quality Tiers
Skills have three quality levels — v1 (stub), v2 (production-ready), v3 (battle-tested with benchmarks). You can filter by tier so you only use skills that meet your quality bar.

### 2. Prerequisite Dependency Graph
Every skill declares its prerequisites. Skills Tree builds a directed graph you can query: *“what do I need to master before I can implement skill X?”*

### 3. MCP-Native
Skills Tree ships a Model Context Protocol server. Any MCP-compatible host (Claude Desktop, Cursor, Cline, Continue) can query Skills Tree directly. Your IDE becomes a skill oracle.

### 4. Typed I/O Contracts
v2+ skills declare strongly typed inputs and outputs using Pydantic. This means skills can be composed into pipelines without manual schema negotiation.

### 5. Framework Portability
Each skill includes implementation notes for LangChain, LangGraph, CrewAI, AutoGen, and plain Python. You’re never locked into one framework.

## Network Effect

Skills Tree gets more valuable as more teams contribute upgraded skills. A skill upgraded from v1 to v3 by one team benefits every team using that skill. This is the compounding return on investment that individual wikis can never achieve.

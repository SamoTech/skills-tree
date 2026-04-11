# 🧰 Supported Frameworks, Platforms & Models

A curated reference of every framework, platform, and model referenced throughout the Skills Tree. Entries are kept current as of **April 2026**.

> 💡 To add a new entry, see [CONTRIBUTING.md](../CONTRIBUTING.md#how-to-add-a-framework-or-model).

---

## 🤖 Agent Frameworks

| Framework | Language | Specialty | Skills Coverage | Link |
|---|---|---|---|---|
| **LangChain** | Python / JS | Tool-use, RAG, chains | [Tool Use](../skills/07-tool-use/), [Memory](../skills/03-memory/) | [langchain.com](https://langchain.com) |
| **LangGraph** | Python | Graph-based multi-agent orchestration | [Orchestration](../skills/15-orchestration/), [Agentic Patterns](../skills/09-agentic-patterns/) | [langchain.com/langgraph](https://langchain.com/langgraph) |
| **AutoGen** | Python | Multi-agent conversation & debate | [Orchestration](../skills/15-orchestration/), [Communication](../skills/06-communication/) | [microsoft.github.io/autogen](https://microsoft.github.io/autogen) |
| **CrewAI** | Python | Role-based agent crews | [Orchestration](../skills/15-orchestration/), [Domain-Specific](../skills/16-domain-specific/) | [crewai.com](https://crewai.com) |
| **Semantic Kernel** | Python / C# / Java | Enterprise LLM SDK, plugins | [Tool Use](../skills/07-tool-use/), [Memory](../skills/03-memory/) | [learn.microsoft.com](https://learn.microsoft.com/semantic-kernel) |
| **Haystack** | Python | NLP pipelines, document RAG | [Memory](../skills/03-memory/), [Data](../skills/12-data/) | [haystack.deepset.ai](https://haystack.deepset.ai) |
| **CAMEL** | Python | Role-playing autonomous agents | [Communication](../skills/06-communication/), [Agentic Patterns](../skills/09-agentic-patterns/) | [camel-ai.org](https://camel-ai.org) |
| **MetaGPT** | Python | Software company simulation | [Code](../skills/05-code/), [Orchestration](../skills/15-orchestration/) | [deepwisdom.ai](https://deepwisdom.ai) |
| **Agno** | Python | High-performance agentic framework | [Action Execution](../skills/04-action-execution/), [Tool Use](../skills/07-tool-use/) | [agno.com](https://agno.com) |
| **Pydantic AI** | Python | Type-safe agents with validation | [Code](../skills/05-code/), [Reasoning](../skills/02-reasoning/) | [ai.pydantic.dev](https://ai.pydantic.dev) |
| **DSPy** | Python | Declarative LLM pipelines, auto-optimization | [Reasoning](../skills/02-reasoning/), [Agentic Patterns](../skills/09-agentic-patterns/) | [dspy.ai](https://dspy.ai) |
| **Smolagents** | Python | HuggingFace lightweight agents | [Tool Use](../skills/07-tool-use/), [Code](../skills/05-code/) | [huggingface.co/smolagents](https://huggingface.co/docs/smolagents) |
| **OpenAI Assistants API** | Python / JS | Native OpenAI agent platform | [Tool Use](../skills/07-tool-use/), [Memory](../skills/03-memory/) | [platform.openai.com](https://platform.openai.com/docs/assistants) |
| **Vertex AI Agents** | Python | Google Cloud agent platform | [Tool Use](../skills/07-tool-use/), [Domain-Specific](../skills/16-domain-specific/) | [cloud.google.com](https://cloud.google.com/vertex-ai/generative-ai/docs/agents) |
| **Amazon Bedrock Agents** | Python | AWS managed agent platform | [Tool Use](../skills/07-tool-use/), [Memory](../skills/03-memory/) | [aws.amazon.com/bedrock](https://aws.amazon.com/bedrock/agents) |
| **Bee Agent Framework** | TypeScript | IBM open-source agents | [Tool Use](../skills/07-tool-use/), [Reasoning](../skills/02-reasoning/) | [github.com/i-am-bee](https://github.com/i-am-bee/bee-agent-framework) |
| **Mirascope** | Python | Ergonomic LLM calls & structured output | [Communication](../skills/06-communication/), [Code](../skills/05-code/) | [mirascope.com](https://mirascope.com) |

---

## 🖥️ Computer Use & Browser Agents

| Framework | Description | Skills Coverage | Link |
|---|---|---|---|
| **Anthropic Computer Use** | Claude-powered GUI + OS automation | [Computer Use](../skills/10-computer-use/) | [anthropic.com](https://anthropic.com) |
| **OpenAI CUA** | GPT-4o computer-use agent | [Computer Use](../skills/10-computer-use/) | [openai.com](https://openai.com) |
| **Open Interpreter** | LLM-powered local code + shell execution | [Code](../skills/05-code/), [Action Execution](../skills/04-action-execution/) | [openinterpreter.com](https://openinterpreter.com) |
| **SWE-Agent** | Autonomous software engineering on GitHub | [Code](../skills/05-code/), [Web](../skills/11-web/) | [swe-agent.com](https://swe-agent.com) |
| **Devin** | Fully autonomous coding agent (Cognition) | [Code](../skills/05-code/), [Computer Use](../skills/10-computer-use/) | [cognition.ai](https://cognition.ai) |
| **Browser Use** | LLM-driven web browser automation | [Web](../skills/11-web/), [Computer Use](../skills/10-computer-use/) | [browser-use.com](https://browser-use.com) |
| **Playwright MCP** | Playwright browser control via MCP protocol | [Web](../skills/11-web/), [Computer Use](../skills/10-computer-use/) | [github.com/microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) |
| **Stagehand** | AI browser automation (BrowserBase) | [Web](../skills/11-web/) | [stagehand.dev](https://stagehand.dev) |
| **Skyvern** | Visual browser agent for workflow automation | [Web](../skills/11-web/), [Computer Use](../skills/10-computer-use/) | [skyvern.com](https://skyvern.com) |

---

## 🔌 Protocol & Interoperability Standards

| Standard | Description | Skills Coverage | Link |
|---|---|---|---|
| **MCP** (Model Context Protocol) | Anthropic standard for agent ↔ tool connections | [Tool Use](../skills/07-tool-use/) | [modelcontextprotocol.io](https://modelcontextprotocol.io) |
| **A2A** (Agent-to-Agent) | Google protocol for inter-agent communication | [Orchestration](../skills/15-orchestration/) | [google.github.io/A2A](https://google.github.io/A2A) |
| **OpenAI Function Calling** | Structured JSON tool invocation standard | [Tool Use](../skills/07-tool-use/) | [platform.openai.com](https://platform.openai.com/docs/guides/function-calling) |
| **ACP** (Agent Communication Protocol) | IBM/BeeAI open agent messaging standard | [Orchestration](../skills/15-orchestration/) | [agentcommunicationprotocol.dev](https://agentcommunicationprotocol.dev) |

---

## 🧠 Foundation Models

| Model | Provider | Modalities | Key Strengths | Skill Highlights |
|---|---|---|---|---|
| **GPT-4o** | OpenAI | Text, Image, Audio | Flagship multimodal, fast | [Multimodal](../skills/08-multimodal/), [Tool Use](../skills/07-tool-use/) |
| **o3 / o4-mini** | OpenAI | Text, Code, Image | Deep reasoning, math | [Reasoning](../skills/02-reasoning/), [Code](../skills/05-code/) |
| **Claude 3.7 Sonnet** | Anthropic | Text, Image, Computer Use | Extended thinking, computer use | [Computer Use](../skills/10-computer-use/), [Reasoning](../skills/02-reasoning/) |
| **Claude 3.5 Haiku** | Anthropic | Text, Image | Fast, cost-efficient | [Communication](../skills/06-communication/) |
| **Gemini 2.5 Pro** | Google DeepMind | Text, Image, Audio, Video | Longest context (1M tokens) | [Multimodal](../skills/08-multimodal/), [Data](../skills/12-data/) |
| **Gemini 2.0 Flash** | Google DeepMind | Text, Image, Audio | Low latency, real-time | [Action Execution](../skills/04-action-execution/) |
| **Llama 3.3 70B** | Meta | Text | Open weights, self-hostable | [Reasoning](../skills/02-reasoning/) |
| **Llama 3.2 Vision** | Meta | Text, Image | Open multimodal | [Multimodal](../skills/08-multimodal/) |
| **Mistral Large 2** | Mistral AI | Text, Code | European open model, multilingual | [Code](../skills/05-code/) |
| **Codestral** | Mistral AI | Code | Code-specialized | [Code](../skills/05-code/) |
| **Grok 3** | xAI | Text, Image | Real-time web data | [Web](../skills/11-web/) |
| **DeepSeek R1** | DeepSeek | Text, Code | Open-weights reasoning | [Reasoning](../skills/02-reasoning/), [Code](../skills/05-code/) |
| **DeepSeek V3** | DeepSeek | Text, Code | Strong coding, cost-efficient | [Code](../skills/05-code/) |
| **Qwen 2.5 72B** | Alibaba | Text, Code, Vision | Multilingual, long context | [Communication](../skills/06-communication/) |
| **Command R+** | Cohere | Text | RAG-optimized, enterprise | [Memory](../skills/03-memory/) |
| **Phi-4** | Microsoft | Text, Code | Small but capable, on-device | [Reasoning](../skills/02-reasoning/) |
| **Falcon 3** | TII UAE | Text | Arabic + multilingual | [Communication](../skills/06-communication/) |

---

## 🗃️ Vector Stores & Memory Backends

| Store | Type | Skills Coverage | Link |
|---|---|---|---|
| **Pinecone** | Managed vector DB | [Memory](../skills/03-memory/) | [pinecone.io](https://pinecone.io) |
| **Weaviate** | Open-source vector DB | [Memory](../skills/03-memory/) | [weaviate.io](https://weaviate.io) |
| **Qdrant** | High-performance vector DB | [Memory](../skills/03-memory/) | [qdrant.tech](https://qdrant.tech) |
| **Chroma** | Local-first embedding store | [Memory](../skills/03-memory/) | [trychroma.com](https://trychroma.com) |
| **pgvector** | PostgreSQL vector extension | [Memory](../skills/03-memory/), [Data](../skills/12-data/) | [github.com/pgvector](https://github.com/pgvector/pgvector) |
| **Redis Vector** | Redis-native vector search | [Memory](../skills/03-memory/) | [redis.io](https://redis.io/docs/interact/search-and-query/advanced-concepts/vectors/) |

---

*Last updated: April 2026. PRs welcome — see [CONTRIBUTING.md](../CONTRIBUTING.md).*

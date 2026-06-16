# Examples

> Runnable, production-quality examples demonstrating Skills Tree in real-world scenarios.
> All examples live in the [`examples/`](https://github.com/SamoTech/skills-tree/tree/main/examples) directory.

## Quick Navigation

| Example | Description | Complexity |
|---|---|---|
| [openai-agent](#openai-agent) | Skill-aware OpenAI agent with dynamic tool selection | Beginner |
| [mcp-server](#mcp-server) | MCP server exposing Skills Tree as Claude Desktop tools | Intermediate |
| [recommendation-engine](#recommendation-engine) | Learning path recommender with prerequisite graph | Intermediate |
| [rag-system](#rag-system) | RAG pipeline enhanced with structured skill context | Advanced |
| [enterprise-agent](#enterprise-agent) | Multi-agent system with governance and audit layer | Advanced |

---

## openai-agent

**File:** [`examples/openai-agent/`](https://github.com/SamoTech/skills-tree/tree/main/examples/openai-agent)

Demonstrates how to build an OpenAI-powered agent that uses Skills Tree to:
- Dynamically select which skills to apply based on user intent
- Enrich system prompts with skill descriptions and examples
- Log which skills were invoked for observability

```bash
cd examples/openai-agent
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python agent.py "how do I build a RAG system?"
```

---

## mcp-server

**File:** [`examples/mcp-server/`](https://github.com/SamoTech/skills-tree/tree/main/examples/mcp-server)

A complete MCP (Model Context Protocol) server that exposes Skills Tree as tools available to Claude Desktop, Cursor, and any MCP-compatible host.

Tools exposed:
- `search_skills` — semantic search across 515+ skills
- `get_skill` — retrieve full skill details by ID
- `get_prerequisites` — get the prerequisite chain for a skill
- `get_learning_path` — get an ordered path between two skills

```bash
cd examples/mcp-server
pip install -r requirements.txt
python server.py
# Configure in Claude Desktop: point to this server
```

---

## recommendation-engine

**File:** [`examples/recommendation-engine/`](https://github.com/SamoTech/skills-tree/tree/main/examples/recommendation-engine)

A learning path recommendation engine for EdTech platforms. Given a user’s current skills and a target goal, it generates the shortest learning path using the prerequisite dependency graph.

```bash
cd examples/recommendation-engine
pip install -r requirements.txt
python recommend.py --current "python-basics,api-calls" --target "production-rag"
```

---

## rag-system

**File:** [`examples/rag-system/`](https://github.com/SamoTech/skills-tree/tree/main/examples/rag-system)

Shows how to use Skills Tree as a structured knowledge layer above a RAG pipeline. The system:
1. Identifies which skills are relevant to a user query
2. Enriches RAG context with structured skill prerequisites
3. Provides more accurate, structured answers

```bash
cd examples/rag-system
pip install -r requirements.txt
python rag.py "how do I add memory to my agent?"
```

---

## enterprise-agent

**File:** [`examples/enterprise-agent/`](https://github.com/SamoTech/skills-tree/tree/main/examples/enterprise-agent)

A production-grade multi-agent system with:
- Skill-based routing (tasks matched to agents by declared skill IDs)
- Agent manifest validation against the taxonomy
- Audit logging of skill invocations
- Compliance checks for deprecated or unknown skills

```bash
cd examples/enterprise-agent
pip install -r requirements.txt
python orchestrator.py --task "research and summarize AI safety papers"
```

---

## Running All Examples

```bash
# Install skills-tree first
pip install skills-tree

# Clone the repo for examples
git clone https://github.com/SamoTech/skills-tree.git
cd skills-tree

# Each example has its own requirements
for dir in examples/*/; do
  echo "=== $dir ==="
  (cd "$dir" && pip install -r requirements.txt -q && echo "Ready")
done
```

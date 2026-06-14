# Data Model — Skills Tree v3.0

> The foundation of the API, search index, and knowledge graph.

---

## Design Philosophy

Every entity in Skills Tree is a **structured record first** and a Markdown document second. The Markdown is the human-readable view of the data. The JSON/YAML is the machine-readable canonical form.

---

## Core Schemas

### 1. Skill

```yaml
# schema/skill.schema.yaml
skill:
  id: string                    # Unique slug: "rag", "memory-injection"
  name: string                  # Display name: "RAG Pipeline"
  category:
    id: string                  # "03-memory"
    name: string                # "Memory"
  description: string           # 1-3 sentence summary
  version: string               # "v3"
  stability:
    enum: [stable, beta, experimental, deprecated]
  quality:
    enum: [battle-tested, verified, stub]
  difficulty:
    enum: [beginner, intermediate, advanced, expert]
  domains: string[]             # ["nlp", "code", "web", "data", "multimodal"]
  tags: string[]                # Free-form tags for search
  input_types: string[]         # Types this skill accepts as input
  output_types: string[]        # Types this skill produces as output
  frameworks: FrameworkSupport[]
  related_skills: string[]      # Skill IDs
  required_skills: string[]     # Prerequisite skill IDs
  mcp_tools: string[]           # MCP tool IDs that implement this skill
  benchmarks: BenchmarkRef[]
  changelog: ChangelogEntry[]
  author: ContributorRef
  contributors: ContributorRef[]
  created_at: date
  updated_at: date
  github_path: string           # Path in repo: "skills/03-memory/rag.md"
  example_code:
    language: string
    runtime: string
    snippet: string
  io_spec:
    inputs: IOField[]
    outputs: IOField[]
  failure_modes: FailureMode[]
  use_cases: string[]
  agent_types: string[]         # ["research", "coding", "customer-support"]
```

### 2. MCP Tool

```yaml
# schema/mcp-tool.schema.yaml
mcp_tool:
  id: string                    # Unique slug: "brave-search-mcp"
  name: string                  # "Brave Search"
  description: string
  type:
    enum: [server, client, tool, middleware]
  transport:
    enum: [stdio, http, sse, websocket]
  category: string              # "search", "code", "database", "browser"...
  skills: string[]              # Skill IDs this tool enables
  install:
    npm: string
    pip: string
    docker: string
    manual_url: string
  config_schema: object         # JSON Schema for tool configuration
  capabilities: string[]        # Capability names
  authentication:
    required: boolean
    methods: string[]
  rate_limits:
    requests_per_minute: integer
    tokens_per_day: integer
  pricing:
    model: enum [free, freemium, paid]
    free_tier: string
  status: enum [stable, beta, deprecated]
  version: string
  repo_url: string
  docs_url: string
  community_rating: float       # 0-5
  community_reviews: integer
  last_updated: date
  maintainer: string
```

### 3. Agent Architecture Pattern

```yaml
# schema/agent-pattern.schema.yaml
agent_pattern:
  id: string                    # "react", "plan-and-execute", "multi-agent-mesh"
  name: string
  description: string
  category:
    enum: [single-agent, multi-agent, hybrid]
  planning_type:
    enum: [reactive, deliberative, hybrid]
  memory_types: string[]        # ["working", "episodic", "semantic"]
  tool_calling: boolean
  reflection: boolean
  skills: string[]              # Core skill IDs for this pattern
  frameworks: string[]          # Framework IDs that implement this
  complexity: enum [low, medium, high, expert]
  latency_profile: enum [low, medium, high]
  token_efficiency: enum [low, medium, high]
  use_cases: string[]
  trade_offs:
    pros: string[]
    cons: string[]
  visual_diagram: string        # Path to Mermaid or SVG diagram
  reference_implementations: CodeRef[]
  benchmarks: BenchmarkRef[]
  related_patterns: string[]
```

### 4. Learning Path

```yaml
# schema/learning-path.schema.yaml
learning_path:
  id: string
  title: string
  description: string
  goal: string                  # "Build a production RAG pipeline"
  audience:
    enum: [beginner, intermediate, advanced]
  estimated_hours: integer
  skills: LearningPathStep[]    # Ordered skill sequence
  milestones: Milestone[]
  outcome: string               # What the learner can build at the end
  prerequisites: string[]       # Skill IDs needed before starting
  frameworks_used: string[]
  projects: ProjectRef[]        # Hands-on projects
  created_by: ContributorRef
  community_completions: integer
  rating: float
```

### 5. Benchmark

```yaml
# schema/benchmark.schema.yaml
benchmark:
  id: string
  title: string
  description: string
  type:
    enum: [accuracy, latency, cost, quality, comparison]
  skills: string[]              # Skills being benchmarked
  dataset: DatasetRef
  methodology: string
  results: BenchmarkResult[]
  winner: string                # Skill/approach ID
  margin: string                # "+8.3% accuracy"
  reproducible: boolean
  scripts: string[]             # Paths to test scripts
  models_tested: string[]
  frameworks_tested: string[]
  hardware: string
  run_date: date
  author: ContributorRef
```

### 6. Relationship Graph Node

```yaml
# schema/relationship.schema.yaml
relationship:
  source_id: string             # Skill/Pattern/Tool ID
  source_type: enum [skill, pattern, tool, framework]
  target_id: string
  target_type: enum [skill, pattern, tool, framework]
  relationship_type:
    enum:
      - requires           # Source requires target to function
      - extends            # Source is a specialization of target
      - implements         # Source is an implementation of target
      - enables            # Source enables target capability
      - competes_with      # Source is an alternative to target
      - complements        # Source works better with target
      - part_of            # Source is a component of target
  strength: float              # 0.0-1.0 relationship strength
  description: string
  bidirectional: boolean
```

### 7. Framework

```yaml
# schema/framework.schema.yaml
framework:
  id: string                    # "langchain", "llamaindex", "crewai"
  name: string
  description: string
  category:
    enum: [orchestration, memory, tools, evaluation, fine-tuning, deployment]
  language: string[]            # ["python", "javascript", "typescript"]
  skills_supported: string[]    # Skill IDs with native support
  install: object               # Package manager commands
  github_url: string
  docs_url: string
  stars: integer                # Updated periodically
  last_release: date
  license: string
  status: enum [active, maintenance, deprecated]
```

---

## Knowledge Graph Structure

The knowledge graph is a directed property graph stored as a JSON file at `data/knowledge-graph.json`.

### Hierarchy Example

```
Memory (category)
└── Working Memory (skill)
    └── Short-Term Memory (skill) [part_of]
        ├── Token Budget Management (skill) [requires]
        └── Context Window (concept)
Memory (category)
└── Long-Term Memory (skill)
    ├── Episodic Memory (skill) [part_of]
    │   └── Memory Compression (skill) [enables]
    ├── Semantic Memory (skill) [part_of]
    │   └── Knowledge Graph Memory (skill) [extends]
    └── Vector Memory (skill) [part_of]
        ├── Vector Store Retrieval (skill) [requires]
        └── Embedding Generation (skill) [requires]

Tool Use (category)
└── MCP (skill)
    ├── MCP Server (mcp_tool) [implements]
    ├── MCP Client (mcp_tool) [implements]
    └── Tool Calling (skill) [requires]
```

### Graph JSON Format

```json
{
  "version": "1.0",
  "generated_at": "2026-06-14",
  "nodes": [
    {
      "id": "rag",
      "type": "skill",
      "label": "RAG Pipeline",
      "category": "03-memory",
      "quality": "battle-tested",
      "difficulty": "intermediate",
      "x": 0.4,
      "y": 0.3
    }
  ],
  "edges": [
    {
      "source": "rag",
      "target": "embedding-generation",
      "type": "requires",
      "strength": 1.0
    },
    {
      "source": "rag",
      "target": "vector-store-retrieval",
      "type": "requires",
      "strength": 1.0
    }
  ]
}
```

---

## File Layout for Data

```
skills-tree/
├── data/
│   ├── skills.json             ← All skills as structured JSON array
│   ├── skills.yaml             ← Same data as YAML
│   ├── mcp-tools.json          ← All MCP tools
│   ├── frameworks.json         ← All frameworks
│   ├── learning-paths.json     ← All learning paths
│   ├── benchmarks.json         ← All benchmark results
│   ├── knowledge-graph.json    ← Full relationship graph
│   └── index.json              ← Lightweight index for search
├── schema/
│   ├── skill.schema.json       ← JSON Schema for validation
│   ├── mcp-tool.schema.json
│   ├── framework.schema.json
│   ├── benchmark.schema.json
│   ├── learning-path.schema.json
│   └── relationship.schema.json
```

---

*Version: 1.0 — June 2026*

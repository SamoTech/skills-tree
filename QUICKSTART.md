# Skills Tree OS - Quickstart

## 🎯 What Skills Tree Does Today

Skills Tree OS is now a **working intelligence platform**. You can:

1. Run a command
2. Enter a goal ("Coding Agent", "RAG Assistant", etc.)
3. Get a complete architecture blueprint with:
   - Required Skills
   - Optional Skills
   - Dependencies
   - Learning Path
   - Risks
   - Confidence Score

**This is no longer a spec. This is executable software.**

---

## 🚀 Usage

### Run the Architect

```bash
python tools/architect.py
```

### Interactive Session

```
🌳 Skills Tree OS - Agent Skill Architect
Transform goals into executable architectures

Available Goals:
  • Coding Agent
  • Browser Agent
  • RAG Assistant
  • Research Agent
  • Multi-Agent System

What do you want to build?
> Coding Agent
```

### Example Output

```
======================================================================
ARCHITECTURE BLUEPRINT: Coding Agent
======================================================================

ID: blueprint-20260614150000
Confidence Score: 0.95
Architecture Type: Single-Agent
Deployment: local
Complexity: Medium
Maturity: Alpha

──────────────────────────────────────────────────────────────────────
REQUIRED SKILLS:
  • Code Generation (Priority: Critical, Learn Time: 10 hours)
    Rationale: Core capability for Coding Agent
  • Prompt Engineering (Priority: Critical, Learn Time: 15 hours)
    Rationale: Core capability for Coding Agent

──────────────────────────────────────────────────────────────────────
OPTIONAL SKILLS:
  • Function Calling

──────────────────────────────────────────────────────────────────────
DEPENDENCIES:
  • Prompt Engineering (Confidence: 0.95)

──────────────────────────────────────────────────────────────────────
LEARNING PATH:
  1. Prompt Engineering
  2. Code Generation
  3. Function Calling

──────────────────────────────────────────────────────────────────────
RISKS:
  ⚠️  [Major] Probability: Medium
      Mitigation: Implement code review and testing

======================================================================

✅ Blueprint saved to: blueprint_20260614150000.json
```

---

## 📊 What Got Built

### Phase 1: Knowledge Graph ✅
- **File**: `data/SKILLS_GRAPH.json`
- **Contents**: 15 production-ready skills with 13 relationships
- **Edge Types**: REQUIRES, SUPPORTS, RECOMMENDED_WITH, LEARN_BEFORE
- **Confidence Scores**: Per-relationship confidence values

### Phase 2: Recommendation Engine ✅
- **File**: `tools/architect.py`
- **Capabilities**:
  - Goal-to-skill mapping
  - Graph traversal for dependencies
  - Learning path generation
  - Confidence calculation

### Phase 3: Blueprint Generator ✅
- **File**: `tools/architect.py`
- **Output**: Complete blueprints matching `ARCHITECTURE_OUTPUT_SCHEMA.md`
- **Includes**: Skills, dependencies, risks, learning paths, JSON export

---

## 🎓 Supported Goals

| Goal | Required Skills | Complexity |
|---|---|---|
| **Coding Agent** | Code Generation, Prompt Engineering | Medium |
| **Browser Agent** | Browser Automation, Error Recovery | High |
| **RAG Assistant** | RAG Retrieval, Vector Search, Embedding Generation | Medium |
| **Research Agent** | Web Scraping, Data Extraction | Medium |
| **Multi-Agent System** | Multi-Agent Coordination, LLM Orchestration, Context Management | Expert |

---

## 📐 Architecture

```
Skills Tree OS
│
├── data/
│   └── SKILLS_GRAPH.json       # Knowledge graph (15 nodes, 13 edges)
│
├── tools/
│   └── architect.py             # Recommendation + Blueprint + Demo (324 lines)
│
└── meta/
    ├── GRAPH_QUERY_LOGIC_SPEC.md
    ├── ARCHITECTURE_OUTPUT_SCHEMA.md
    └── RECOMMENDATION_ENGINE_SPEC.md
```

---

## 🔍 How It Works

1. **User enters a goal** (e.g., "Coding Agent")
2. **Recommendation Engine** maps goal → required skills
3. **Graph Query** expands dependencies via REQUIRES, RECOMMENDED_WITH edges
4. **Learning Path Generator** traverses LEARN_BEFORE edges to create ordered path
5. **Blueprint Generator** packages everything into a schema-compliant JSON object
6. **Output** displays to console + saves to file

---

## ✅ Success Criteria: ACHIEVED

**Original Goal**:
> A user can run `python demo.py`, enter "Coding Agent", and receive:
> - Architecture Blueprint
> - Required Skills
> - Optional Skills
> - Dependencies
> - Learning Path
> - Risks
> - Confidence Score

**Status**: ✅ **COMPLETE**

The system now generates complete, schema-compliant blueprints for 5 different agent archetypes, with graph-powered intelligence, confidence scoring, and risk analysis.

---

## 🎯 What Changed

**Before Today**: Skills Tree was a documentation repository with 361 skill stubs and strategic specifications.

**After Today**: Skills Tree is a **working intelligence platform** that generates actionable architecture blueprints from user goals.

The graph is the engine. The recommendations are real. The blueprints are executable.

---

## 🔮 Next Steps

To expand the system:
1. Add more skills to `data/SKILLS_GRAPH.json`
2. Add more goal mappings in `RecommendationEngine.GOAL_MAPPINGS`
3. Add more risks in `BlueprintGenerator.RISK_LIBRARY`
4. Expand edge types (ALTERNATIVE_TO, VALIDATED_BY, etc.)

---

**Skills Tree OS is live. The specs became software.**

# Use Cases

> Real-world applications of Skills Tree across AI agent systems.

## 1. AI Agent Skill Registration

**Problem:** Your agent declares it can “reason” and “use memory” but these mean different things to every developer on the team.

**Solution:** Use Skills Tree skill IDs as canonical capability identifiers.

```python
from skills_tree import SkillsTree

st = SkillsTree()

# Register an agent’s declared skills using canonical IDs
agent_skills = [
    st.get("chain-of-thought"),       # reasoning
    st.get("rag"),                     # memory/retrieval
    st.get("tool-use"),                # tool calling
    st.get("structured-output"),       # output formatting
]

print(f"Agent has {len(agent_skills)} registered skills")
for skill in agent_skills:
    print(f"  - {skill.id} (v{skill.version}, tier={skill.tier})")
```

**Who uses this:** Multi-agent orchestration teams, agent marketplaces, capability registries.

---

## 2. MCP Server Tool Exposure

**Problem:** Your MCP server needs to expose tools, but you don’t know which tools are most useful for AI assistants.

**Solution:** Query Skills Tree for MCP-relevant skills and expose them as tools.

```python
from skills_tree import SkillsTree

st = SkillsTree()

# Find all MCP-relevant skills
mcp_skills = st.search("mcp tool-use api")

# Generate tool definitions
for skill in mcp_skills[:5]:
    print(f"Tool: {skill.id}")
    print(f"  Description: {skill.description}")
    print(f"  Inputs: {skill.input_schema}")
    print()
```

See the [MCP server example](../examples/mcp-server/) for a full working implementation.

**Who uses this:** MCP server authors, Claude Desktop plugin developers, IDE extension builders.

---

## 3. Recommendation Engine

**Problem:** A learner says “I know Python and I want to build RAG systems.” You need to recommend a learning path.

**Solution:** Use the prerequisite graph to find the shortest path to their goal.

```python
from skills_tree import SkillsTree

st = SkillsTree()

# Get personalized learning path
path = st.get_path(
    current_skills=["python-basics", "api-calls"],
    target_skill="production-rag"
)

print("Your learning path:")
for i, step in enumerate(path, 1):
    print(f"  {i}. {step.id} — {step.title} (~{step.estimated_hours}h)")
```

See the [recommendation engine example](../examples/recommendation-engine/) for a full implementation.

**Who uses this:** EdTech platforms, developer onboarding tools, skills assessment systems.

---

## 4. RAG System Enhancement

**Problem:** Your RAG pipeline keeps retrieving irrelevant context because the chunks have no semantic structure.

**Solution:** Use Skills Tree’s search index as a structured knowledge layer above your unstructured documents.

```python
from skills_tree import SkillsTree

st = SkillsTree()

def skills_aware_rag(user_query: str) -> dict:
    # Step 1: Identify which skills are relevant to the query
    relevant_skills = st.search(user_query, limit=3)
    
    # Step 2: Use skill prerequisites as context enrichment
    context_skills = []
    for skill in relevant_skills:
        context_skills.extend(st.get_prerequisites(skill.id))
    
    # Step 3: Build structured context for the LLM
    skill_context = "\n".join([
        f"Skill: {s.id}\nDescription: {s.description}\nPrerequisites: {', '.join(s.prerequisites)}"
        for s in context_skills[:5]
    ])
    
    return {
        "query": user_query,
        "relevant_skills": [s.id for s in relevant_skills],
        "structured_context": skill_context
    }

result = skills_aware_rag("how do I implement memory for my agent?")
print(result)
```

See the [RAG system example](../examples/rag-system/) for production patterns.

**Who uses this:** RAG pipeline architects, AI product teams, knowledge management systems.

---

## 5. Agent Orchestration Routing

**Problem:** Your orchestrator needs to route a task to the right specialist agent, but routing is hardcoded and breaks every time you add a new agent.

**Solution:** Use Skills Tree IDs as a routing contract. Agents declare skills. Orchestrator matches task requirements to declared skills.

```python
from skills_tree import SkillsTree

st = SkillsTree()

# Skill-based agent registry
agent_registry = {
    "researcher": ["web-search", "rag", "summarization"],
    "coder": ["code-generation", "code-review", "debugging"],
    "planner": ["task-decomposition", "goal-setting", "reflection"],
}

def route_task(task_description: str) -> str:
    """Route a task to the best-matching agent using Skills Tree."""
    required_skills = st.search(task_description, limit=3)
    required_ids = {s.id for s in required_skills}
    
    best_agent = None
    best_score = 0
    
    for agent, skills in agent_registry.items():
        score = len(required_ids.intersection(set(skills)))
        if score > best_score:
            best_score = score
            best_agent = agent
    
    return best_agent or "default"

print(route_task("search the web and summarize recent AI papers"))
# → researcher
```

**Who uses this:** Multi-agent orchestration frameworks, AutoGen teams, agent mesh architects.

---

## 6. Learning Systems & EdTech

**Problem:** Your platform teaches AI development but has no structured curriculum map.

**Solution:** Use Skills Tree as your curriculum backbone. Skills have difficulty levels, prerequisites, and estimated hours.

```python
from skills_tree import SkillsTree

st = SkillsTree()

# Build a beginner curriculum
beginner_path = st.get_category("01-foundations")
for skill in beginner_path[:5]:
    print(f"✔ {skill.title}")
    print(f"   Difficulty: {skill.difficulty} | Est: {skill.estimated_hours}h")
    print(f"   Prerequisites: {', '.join(skill.prerequisites) or 'None'}")
    print()
```

**Who uses this:** Online learning platforms, bootcamps, corporate training programs, developer advocates.

---

## 7. Enterprise Governance

**Problem:** Your enterprise AI team has 15 teams building agents. Every team defines “memory”, “reasoning”, and “safety” differently. Audits are impossible.

**Solution:** Adopt Skills Tree as the organizational standard. All agents must declare skills using canonical IDs. Architecture reviews check against the taxonomy.

```python
from skills_tree import SkillsTree
import json

st = SkillsTree()

def audit_agent_manifest(manifest_path: str) -> dict:
    """Validate an agent’s skill declarations against the taxonomy."""
    with open(manifest_path) as f:
        manifest = json.load(f)
    
    declared_skills = manifest.get("skills", [])
    results = {"valid": [], "unknown": [], "deprecated": []}
    
    for skill_id in declared_skills:
        skill = st.get(skill_id)
        if skill is None:
            results["unknown"].append(skill_id)
        elif skill.version < 2:
            results["deprecated"].append(skill_id)
        else:
            results["valid"].append(skill_id)
    
    return results

# audit_agent_manifest("agents/researcher/manifest.json")
```

**Who uses this:** Enterprise AI CoEs, platform engineering teams, AI governance officers, compliance teams.

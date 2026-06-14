# N-03: Recommendation Engine Specification

**Status:** Complete  
**Date:** 2026-06-14  
**Purpose:** Define the intelligence core of Skills Tree OS  
**Dependency:** Requires N-01 (Data Audit), N-02 (Goal Taxonomy)  

---

## Executive Summary

This document defines the **9-stage intelligence pipeline** that transforms user intent into complete architecture blueprints.

**This is the difference between a search engine and an architect.**

### Weak Recommendation Engine
```
goal → skills
```

### Strong Recommendation Engine (This Spec)
```
goal
 ↓ Intent Resolution
Normalized Intent
 ↓ Capability Extraction  
Capability Requirements
 ↓ Candidate Retrieval
Skills + Frameworks + Paths + Benchmarks
 ↓ Graph Expansion
Dependencies + Complements + Alternatives + Bundles
 ↓ Framework Compatibility Filter
Framework-Optimized Candidates
 ↓ Ranking Engine
Prioritized Skill List
 ↓ Blueprint Assembly
Complete Architecture
 ↓ Confidence Engine
Confidence Score (0-100)
 ↓ Explanation Engine
Defensible Rationale
```

**This spec becomes the source of truth for all future recommendations.**

---

## SECTION 1: SYSTEM OBJECTIVE

### 1.1 Input

**User provides:**
- Goal (from Goal Taxonomy)
- Sub-goal (optional)
- Deployment target
- Budget constraints
- Framework preference
- Model family
- Experience level

### 1.2 Output

**System produces:**

**NOT:** A list of skills  
**YES:** A complete architecture blueprint

**Blueprint includes:**
- Required skills (with priority, learn time, difficulty)
- Optional skills (enhances, complements)
- Dependencies (what must be learned first)
- Learning path (ordered sequence)
- Framework recommendation (with confidence)
- Architecture diagram (relationships visualized)
- Confidence score (0-100)
- Explanation (why each skill, why not alternatives, what risks)

---

## SECTION 2: RECOMMENDATION PIPELINE

### Stage 1: Intent Resolution

**Input:**
```typescript
interface UserInput {
  goal: string;                  // Goal ID (e.g., "G01.4")
  goal_description?: string;     // User's own words
  experience_level: "beginner" | "intermediate" | "advanced";
  time_budget_hours?: number;
  deployment: "cloud" | "local" | "edge" | "any";
  budget: "free" | "low" | "medium" | "high" | "unlimited";
  framework?: "openai" | "langchain" | "llamaindex" | "mcp" | "mastra" | "custom" | "any";
  model_family?: "openai" | "anthropic" | "google" | "meta" | "any";
  model_size?: "small" | "medium" | "large" | "any";
  include_alternatives?: boolean;
  max_recommendations?: number;
  prioritize_by?: "time" | "difficulty" | "popularity" | "latest";
}
```

**Process:**
1. **Validate goal ID** against Goal Taxonomy (N-02)
2. **Normalize experience level** (map beginner/intermediate/advanced to difficulty scores)
3. **Resolve framework preference** ("any" → rank all frameworks, specific → filter)
4. **Normalize budget** (map to deployment constraints)
5. **Detect conflicts** (e.g., "edge" deployment + "unlimited" budget)

**Output:**
```typescript
interface NormalizedIntent {
  goal_id: string;                    // E.g., "G01.4"
  goal_category: string;              // E.g., "Coding Agent"
  sub_goal: string;                   // E.g., "Debugging"
  difficulty: "beginner" | "intermediate" | "advanced";
  difficulty_score: number;           // 1-10
  time_budget_hours: number | null;   // null = unlimited
  deployment_targets: string[];       // ["cloud", "local"]
  cost_constraints: {
    max_api_cost_per_month?: number;
    prefer_open_source: boolean;
  };
  framework_preferences: {
    preferred: string[];              // Ranked list
    excluded: string[];               // Incompatible
  };
  model_constraints: {
    family: string[];
    size: string[];                   // ["medium", "large"]
    latency_tolerance: "low" | "medium" | "high";
  };
  output_preferences: {
    include_alternatives: boolean;
    max_skills: number;               // Default: 10
    ranking_strategy: string;         // "time" | "difficulty" | etc.
  };
}
```

---

### Stage 2: Capability Extraction

**Input:** NormalizedIntent

**Process:**
1. **Lookup goal in Goal Taxonomy**
2. **Extract required capabilities** (from Level 3 of taxonomy)
3. **Prioritize capabilities** (Critical > High > Medium)
4. **Expand capability definitions** (e.g., "Tool Use" → what it enables)

**Example: G01.4 Debugging**

```yaml
Capability Requirements:
  Critical:
    - Tool Use:        # Must run debuggers, linters
        enables: [execution, inspection, testing]
        difficulty: 6/10
    - Code Analysis:   # Parse syntax, understand control flow
        enables: [reasoning, inspection, generation]
        difficulty: 7/10
  High:
    - Planning:        # Form hypotheses about bug source
        enables: [reasoning, decomposition]
        difficulty: 5/10
    - Reflection:      # Evaluate if fix actually works
        enables: [self-correction, validation]
        difficulty: 5/10
  Medium:
    - Error Handling:  # Gracefully handle test failures
        enables: [robustness, recovery]
        difficulty: 4/10
    - Web Search:      # Look up error messages, Stack Overflow
        enables: [knowledge_access, learning]
        difficulty: 2/10
    - File Operations: # Read stack traces, log files
        enables: [data_access, inspection]
        difficulty: 2/10
```

**Output:**
```typescript
interface CapabilityRequirements {
  goal_id: string;
  capabilities: {
    id: string;                  // E.g., "tool-use"
    name: string;                // E.g., "Tool Use"
    priority: "critical" | "high" | "medium" | "low";
    reason: string;              // Why this capability is needed
    enables: string[];           // What this unlocks
    difficulty_score: number;    // 1-10
  }[];
}
```

---

### Stage 3: Candidate Retrieval

**Input:** CapabilityRequirements

**Process:**
1. **Map capabilities → skills** (using Goal Taxonomy Level 4)
2. **Retrieve skill metadata** from graph.json, search-index.json, skills/*.md
3. **Retrieve related frameworks** (from Goal Taxonomy Level 5)
4. **Retrieve related paths** (paths that include these skills)
5. **Retrieve benchmark data** (if available)

**Retrieval Strategy:**

```python
# Pseudo-code
def retrieve_candidates(capabilities):
    candidates = {
        "skills": [],
        "frameworks": [],
        "paths": [],
        "benchmarks": []
    }
    
    for capability in capabilities:
        # Direct skill mapping
        skills = taxonomy.get_skills_for_capability(capability.id)
        candidates["skills"].extend(skills)
        
        # Framework compatibility
        frameworks = taxonomy.get_frameworks_for_capability(capability.id)
        candidates["frameworks"].extend(frameworks)
        
        # Related paths
        paths = path_index.find_paths_containing_skills(skills)
        candidates["paths"].extend(paths)
        
        # Benchmark data
        benchmarks = benchmark_index.find_benchmarks_for_skills(skills)
        candidates["benchmarks"].extend(benchmarks)
    
    return candidates
```

**Output:**
```typescript
interface Candidates {
  skills: {
    id: string;
    title: string;
    category: string;
    level: string;
    stability: string;
    priority: string;          // From capability mapping
    learn_time_hours: number;
    difficulty_score: number;
    matched_capability: string; // Which capability this satisfies
  }[];
  frameworks: {
    id: string;
    name: string;
    suitability_score: number;  // From Goal Taxonomy (1-5 stars)
  }[];
  paths: {
    id: string;
    title: string;
    difficulty: string;
    estimated_hours: number;
    overlap_skills: string[];   // Skills from this path that match
  }[];
  benchmarks: {
    id: string;
    title: string;
    skill_id: string;
    results: { model: string; score: number }[];
  }[];
}
```

---

### Stage 4: Graph Expansion

**Input:** Candidates (skills)

**Process:**
1. **Traverse graph.json** to find relationships
2. **Identify dependencies** (skills that must be learned first)
3. **Identify complements** (skills that work well together)
4. **Identify alternatives** (different ways to achieve same goal)
5. **Identify bundles** (commonly learned together)

**Graph Relationships:**

```typescript
interface GraphRelationships {
  dependencies: {
    source: string;              // Skill that requires
    target: string;              // Skill that is required
    type: "hard" | "soft";       // hard = must have, soft = recommended
  }[];
  complements: {
    skill_a: string;
    skill_b: string;
    synergy_score: number;       // 0-1 (how well they work together)
  }[];
  alternatives: {
    goal: string;                // What they both achieve
    option_a: string;            // Skill option 1
    option_b: string;            // Skill option 2
    tradeoff: string;            // Why choose one over the other
  }[];
  bundles: {
    skills: string[];            // Skills commonly learned together
    frequency: number;           // How often (0-1)
    reason: string;              // Why they're bundled
  }[];
}
```

**Graph Expansion Algorithm:**

```python
def expand_graph(candidate_skills):
    expanded = {
        "core_skills": candidate_skills,
        "dependencies": [],
        "complements": [],
        "alternatives": [],
        "bundles": []
    }
    
    for skill in candidate_skills:
        # Find dependencies (traverse incoming edges)
        deps = graph.get_dependencies(skill.id)
        expanded["dependencies"].extend(deps)
        
        # Find complements (skills with high co-occurrence)
        complements = graph.find_complements(skill.id, threshold=0.6)
        expanded["complements"].extend(complements)
        
        # Find alternatives (same capability, different approach)
        alternatives = taxonomy.get_alternatives(skill.id)
        expanded["alternatives"].extend(alternatives)
    
    # Find bundles (common skill combinations)
    bundles = graph.find_bundles(candidate_skills)
    expanded["bundles"] = bundles
    
    return expanded
```

**Example Output:**

**Core Skill:** `tool-use`  
**Dependencies:**
- `api-calling` (required to use tools)
- `structured-output` (tools return structured data)

**Complements:**
- `error-handling` (tools can fail)
- `reflection` (evaluate tool outputs)

**Alternatives:**
- Instead of generic `tool-use`, could specialize:
  - `web-search-tool`
  - `code-execution-tool`
  - `file-operation-tool`

**Bundles:**
- `tool-use` + `planning` + `reflection` = "Agentic Loop" (frequency: 0.82)

---

### Stage 5: Framework Compatibility Filter

**Input:** Expanded candidates + NormalizedIntent.framework_preferences

**Process:**
1. **Score each skill by framework compatibility**
2. **Filter out incompatible frameworks**
3. **Rank frameworks by suitability**

**Framework Compatibility Matrix:**

| Skill | OpenAI SDK | LangChain | LlamaIndex | MCP | Mastra | Custom |
|-------|------------|-----------|------------|-----|--------|--------|
| tool-use | ⭐⭐⭐⭐⭐ (5) | ⭐⭐⭐⭐ (4) | ⭐⭐ (2) | ⭐⭐⭐⭐ (4) | ⭐⭐⭐⭐⭐ (5) | ⭐⭐⭐⭐⭐ (5) |
| code-analysis | ⭐⭐⭐ (3) | ⭐⭐⭐ (3) | ⭐ (1) | ⭐⭐ (2) | ⭐⭐⭐ (3) | ⭐⭐⭐⭐⭐ (5) |
| planning | ⭐⭐⭐⭐ (4) | ⭐⭐⭐⭐ (4) | ⭐⭐ (2) | ⭐⭐⭐ (3) | ⭐⭐⭐⭐⭐ (5) | ⭐⭐⭐⭐⭐ (5) |

**Filtering Algorithm:**

```python
def filter_by_framework(candidates, framework_prefs):
    if framework_prefs.preferred == ["any"]:
        # Rank all frameworks by average compatibility
        framework_scores = {}
        for fw in ["openai", "langchain", "llamaindex", "mcp", "mastra", "custom"]:
            scores = [taxonomy.get_framework_score(skill.id, fw) for skill in candidates.skills]
            framework_scores[fw] = sum(scores) / len(scores)
        
        ranked_frameworks = sorted(framework_scores.items(), key=lambda x: x[1], reverse=True)
        return {
            "recommended_framework": ranked_frameworks[0][0],
            "confidence": ranked_frameworks[0][1] / 5.0,  # Normalize to 0-1
            "alternatives": ranked_frameworks[1:3]
        }
    else:
        # User specified framework
        preferred_fw = framework_prefs.preferred[0]
        scores = [taxonomy.get_framework_score(skill.id, preferred_fw) for skill in candidates.skills]
        avg_score = sum(scores) / len(scores)
        
        return {
            "recommended_framework": preferred_fw,
            "confidence": avg_score / 5.0,
            "warning": "Low compatibility" if avg_score < 3.0 else None
        }
```

**Output:**
```typescript
interface FrameworkRecommendation {
  recommended_framework: string;     // E.g., "custom"
  confidence: number;                // 0-1
  suitability_score: number;         // 1-5
  maturity: "experimental" | "stable" | "production";
  ecosystem_fit: number;             // 0-1 (how well it fits user's stack)
  alternatives: {
    framework: string;
    score: number;
    tradeoff: string;                // Why consider this instead
  }[];
  warning?: string;                  // E.g., "Low compatibility with edge deployment"
}
```

---

### Stage 6: Ranking Engine

**Input:** Expanded candidates + NormalizedIntent.ranking_strategy

**Process:** Score every skill using multi-factor formula

**Scoring Formula:**

```
Skill Score = (
  relevance_score × W_relevance +
  priority_score × W_priority +
  time_efficiency_score × W_time +
  graph_centrality_score × W_graph +
  benchmark_score × W_benchmark +
  framework_compatibility_score × W_framework
)
```

**Where:**

**relevance_score** (0-1):
```python
relevance = 1.0 if skill satisfies critical capability else
            0.7 if skill satisfies high capability else
            0.4 if skill satisfies medium capability else
            0.1
```

**priority_score** (0-1):
```python
priority = skill.priority / 5.0  # priority is 1-5
```

**time_efficiency_score** (0-1):
```python
if user has time_budget:
    time_efficiency = 1.0 - (skill.learn_time_hours / time_budget)
else:
    time_efficiency = 1.0 - (skill.learn_time_hours / 100)  # Normalize to 100hrs max
```

**graph_centrality_score** (0-1):
```python
# How connected is this skill in the graph?
centrality = (in_degree + out_degree) / max_degree_in_graph
```

**benchmark_score** (0-1):
```python
if skill has benchmark data:
    benchmark = average(model_scores) / 100  # Scores are 0-100
else:
    benchmark = 0.5  # Neutral if no data
```

**framework_compatibility_score** (0-1):
```python
framework_compat = taxonomy.get_framework_score(skill.id, recommended_framework) / 5.0
```

**Weight Configuration (Default):**

```yaml
Weights:
  W_relevance: 0.35   # Highest weight: does it solve the problem?
  W_priority: 0.25    # Second: is it foundational?
  W_time: 0.15        # Third: does it fit user's time budget?
  W_graph: 0.10       # Fourth: is it well-connected?
  W_benchmark: 0.08   # Fifth: is it validated?
  W_framework: 0.07   # Sixth: does it fit the framework?
# Total: 1.00
```

**Ranking Strategy Adjustments:**

If `prioritize_by == "time"`:
```yaml
Weights:
  W_time: 0.40        # Prioritize fast-to-learn skills
  W_relevance: 0.30
  W_priority: 0.15
  W_graph: 0.08
  W_benchmark: 0.04
  W_framework: 0.03
```

If `prioritize_by == "difficulty"`:
```yaml
Weights:
  W_relevance: 0.40
  W_priority: 0.30    # Prioritize foundational skills
  W_time: 0.05        # De-prioritize time
  W_graph: 0.15       # Increase graph importance
  W_benchmark: 0.06
  W_framework: 0.04
```

If `prioritize_by == "latest"`:
```yaml
Weights:
  W_relevance: 0.30
  W_priority: 0.20
  W_time: 0.10
  W_graph: 0.05
  W_benchmark: 0.30   # Heavily weight recent benchmarks
  W_framework: 0.05
# Add recency_score (skills updated recently get boost)
```

**Output:**
```typescript
interface RankedSkills {
  skills: {
    id: string;
    title: string;
    rank: number;                  // 1, 2, 3...
    score: number;                 // 0-1 (final composite score)
    scores_breakdown: {
      relevance: number;
      priority: number;
      time_efficiency: number;
      graph_centrality: number;
      benchmark: number;
      framework_compatibility: number;
    };
    priority: "critical" | "high" | "medium" | "low";
    learn_time_hours: number;
    difficulty_score: number;      // 1-10
    category: string;
  }[];
}
```

---

### Stage 7: Blueprint Assembly

**Input:** RankedSkills + GraphRelationships + FrameworkRecommendation

**Process:**
1. **Select top N skills** (based on user's max_recommendations or default 10)
2. **Resolve dependencies** (add missing prerequisite skills)
3. **Order skills** (topological sort by dependencies)
4. **Separate required vs optional** (critical/high = required, medium/low = optional)
5. **Generate learning path** (sequential ordering with milestones)
6. **Create architecture diagram** (skill relationships visualized)

**Blueprint Assembly Algorithm:**

```python
def assemble_blueprint(ranked_skills, graph, framework_rec, user_intent):
    # Step 1: Select top N skills
    top_skills = ranked_skills[:user_intent.output_preferences.max_skills]
    
    # Step 2: Resolve dependencies
    required_deps = []
    for skill in top_skills:
        deps = graph.get_hard_dependencies(skill.id)
        for dep in deps:
            if dep not in top_skills and dep not in required_deps:
                required_deps.append(dep)
    
    all_skills = top_skills + required_deps
    
    # Step 3: Topological sort (dependency order)
    ordered_skills = topological_sort(all_skills, graph)
    
    # Step 4: Separate required vs optional
    required_skills = [s for s in ordered_skills if s.priority in ["critical", "high"]]
    optional_skills = [s for s in ordered_skills if s.priority in ["medium", "low"]]
    
    # Step 5: Generate learning path
    learning_path = generate_learning_path(ordered_skills)
    
    # Step 6: Create architecture diagram
    architecture = {
        "nodes": [{
            "id": s.id,
            "label": s.title,
            "type": "required" if s in required_skills else "optional"
        } for s in all_skills],
        "edges": graph.get_edges_between(all_skills)
    }
    
    return {
        "required_skills": required_skills,
        "optional_skills": optional_skills,
        "learning_path": learning_path,
        "architecture": architecture,
        "framework": framework_rec,
        "total_estimated_hours": sum(s.learn_time_hours for s in required_skills)
    }
```

**Output:**
```typescript
interface ArchitectureBlueprint {
  goal: string;
  sub_goal: string;
  difficulty: string;
  
  required_skills: {
    id: string;
    title: string;
    category: string;
    priority: number;              // 1-5 (1 = learn first)
    learn_time_hours: number;
    difficulty_score: number;
    prerequisites: string[];       // Skill IDs that must come before
  }[];
  
  optional_skills: {
    id: string;
    title: string;
    benefit: string;               // What this adds
    learn_time_hours: number;
  }[];
  
  learning_path: {
    phase: number;
    phase_name: string;            // E.g., "Foundation", "Core", "Advanced"
    skills: string[];              // Skill IDs in this phase
    estimated_hours: number;
    milestone: string;             // What you can build after this phase
  }[];
  
  architecture: {
    nodes: { id: string; label: string; type: string }[];
    edges: { source: string; target: string; type: string }[];
  };
  
  framework_recommendation: FrameworkRecommendation;
  
  total_estimated_hours: number;
  min_completion_hours: number;  // If user skips optional skills
  max_completion_hours: number;  // If user learns everything
}
```

---

### Stage 8: Confidence Engine

**Input:** ArchitectureBlueprint + Data Coverage Metrics

**Process:** Calculate confidence score based on data quality

**Confidence Formula:**

```
Confidence Score (0-100) = (
  goal_coverage × W_goal +
  skill_coverage × W_skill +
  graph_coverage × W_graph +
  benchmark_coverage × W_benchmark +
  framework_confidence × W_framework
)
```

**Where:**

**goal_coverage** (0-100):
```python
# How well-defined is this goal in the taxonomy?
goal_coverage = (
  (capabilities_mapped / total_capabilities_needed) × 0.4 +
  (skills_available / skills_needed) × 0.4 +
  (has_framework_mapping ? 100 : 0) × 0.2
)
```

**skill_coverage** (0-100):
```python
# How complete is skill metadata?
skill_coverage = average([
  skill.has_learn_time ? 100 : 0,
  skill.has_difficulty_score ? 100 : 0,
  skill.has_dependencies ? 100 : 0,
  skill.has_examples ? 100 : 0,
  skill.stability == "stable" ? 100 : 50
])
```

**graph_coverage** (0-100):
```python
# How well-connected are the skills?
graph_coverage = (
  (connected_skills / total_skills) × 0.5 +
  (has_dependency_data ? 100 : 0) × 0.3 +
  (has_alternative_paths ? 100 : 0) × 0.2
)
```

**benchmark_coverage** (0-100):
```python
# How many skills have benchmark data?
benchmark_coverage = (skills_with_benchmarks / total_skills) × 100
```

**framework_confidence** (0-100):
```python
# From Stage 5 framework compatibility
framework_confidence = framework_rec.confidence × 100
```

**Weight Configuration:**

```yaml
Weights:
  W_goal: 0.30        # How well we understand the goal
  W_skill: 0.25       # Quality of skill metadata
  W_graph: 0.25       # Graph completeness
  W_benchmark: 0.10   # Validation data
  W_framework: 0.10   # Framework fit
```

**Confidence Thresholds:**

- **90-100:** Excellent — High confidence, production-ready recommendation
- **75-89:** Good — Strong confidence, validated path
- **60-74:** Fair — Moderate confidence, may have gaps
- **40-59:** Low — Weak confidence, limited data
- **0-39:** Poor — Very low confidence, not recommended

**Output:**
```typescript
interface ConfidenceScore {
  overall_score: number;           // 0-100
  rating: "excellent" | "good" | "fair" | "low" | "poor";
  breakdown: {
    goal_coverage: number;
    skill_coverage: number;
    graph_coverage: number;
    benchmark_coverage: number;
    framework_confidence: number;
  };
  risks: string[];                 // E.g., ["Limited benchmark data", "Sparse graph connections"]
  gaps: string[];                  // E.g., ["Missing skill: error-handling"]
}
```

---

### Stage 9: Explanation Engine

**Input:** ArchitectureBlueprint + RankedSkills + Alternatives + ConfidenceScore

**Process:** Generate human-readable rationale for every decision

**Explanation Requirements:**

Every recommendation must explain:
1. **Why selected** — Why this skill is in the blueprint
2. **Why not alternatives** — Why we didn't recommend alternative approaches
3. **What risks exist** — What could go wrong
4. **What it unlocks** — What you can build after learning this

**Explanation Templates:**

**Why Selected:**
```
"{skill_title}" was selected because:
- It satisfies the {capability_name} capability (priority: {priority})
- It is a {hard|soft} dependency of {dependent_skills}
- It has {framework_compatibility}% compatibility with {framework}
- Estimated learning time: {hours} hours (difficulty: {score}/10)
- Graph analysis shows it is frequently paired with {complement_skills}
```

**Why Not Alternatives:**
```
Alternative approach: "{alternative_skill}"
- Tradeoff: {tradeoff_description}
- Reason not selected: {reason}
- When to use instead: {scenario}
```

**What Risks Exist:**
```
Potential risks:
- {risk_type}: {risk_description}
- Mitigation: {mitigation_strategy}
```

**What It Unlocks:**
```
After learning "{skill_title}", you will be able to:
- {capability_1}
- {capability_2}
- Build: {example_projects}
```

**Full Explanation Generation:**

```python
def generate_explanation(blueprint, ranked_skills, alternatives, confidence):
    explanations = []
    
    for skill in blueprint.required_skills:
        # Why selected
        capabilities = taxonomy.get_capabilities_satisfied_by(skill.id)
        dependents = graph.get_skills_that_depend_on(skill.id)
        complements = graph.get_complements(skill.id)
        
        why_selected = f"""
        "{skill.title}" was selected because:
        - It satisfies {capabilities[0].name} capability (priority: {capabilities[0].priority})
        - It is a hard dependency of {', '.join(dependents)}
        - It has {skill.framework_compatibility}% compatibility with {blueprint.framework}
        - Estimated learning time: {skill.learn_time_hours} hours (difficulty: {skill.difficulty_score}/10)
        - Graph analysis shows it is frequently paired with {', '.join(complements)}
        """
        
        # Why not alternatives
        alts = taxonomy.get_alternatives(skill.id)
        why_not_alternatives = []
        for alt in alts:
            why_not = f"""
            Alternative: "{alt.title}"
            - Tradeoff: {alt.tradeoff}
            - Not selected because: {alt.reason_not_selected}
            - Consider using if: {alt.when_to_use}
            """
            why_not_alternatives.append(why_not)
        
        # What risks
        risks = [
            f"Learning curve: {skill.difficulty_score}/10",
            f"Stability: {skill.stability}"
        ]
        if skill.has_benchmarks:
            avg_score = average(skill.benchmark_scores)
            if avg_score < 70:
                risks.append(f"Benchmark scores are moderate ({avg_score}%)")
        
        # What it unlocks
        unlocks = taxonomy.get_unlocked_capabilities(skill.id)
        example_projects = taxonomy.get_example_projects(skill.id)
        
        what_unlocks = f"""
        After learning "{skill.title}", you will be able to:
        {chr(10).join('- ' + u for u in unlocks)}
        Build: {', '.join(example_projects)}
        """
        
        explanations.append({
            "skill_id": skill.id,
            "why_selected": why_selected,
            "why_not_alternatives": why_not_alternatives,
            "risks": risks,
            "what_unlocks": what_unlocks
        })
    
    return explanations
```

**Output:**
```typescript
interface RecommendationExplanation {
  skill_id: string;
  why_selected: string;            // Multi-line explanation
  why_not_alternatives: {
    alternative_skill: string;
    tradeoff: string;
    reason_not_selected: string;
    when_to_use: string;
  }[];
  risks: string[];                 // List of risk statements
  what_unlocks: string;            // What you can build
}
```

---

## SECTION 3: SCORING MODEL

### 3.1 Complete Scoring Formula

**Final Skill Score:**

```
S = (R × 0.35) + (P × 0.25) + (T × 0.15) + (G × 0.10) + (B × 0.08) + (F × 0.07)
```

**Where:**
- **R** = Relevance Score (0-1)
- **P** = Priority Score (0-1)
- **T** = Time Efficiency Score (0-1)
- **G** = Graph Centrality Score (0-1)
- **B** = Benchmark Score (0-1)
- **F** = Framework Compatibility Score (0-1)

### 3.2 Weights Rationale

| Factor | Weight | Rationale |
|--------|--------|----------|
| **Relevance** | 35% | Most important: does it solve the user's problem? |
| **Priority** | 25% | Second: is it foundational (cannot skip)? |
| **Time** | 15% | Third: does it fit user's time budget? |
| **Graph** | 10% | Fourth: is it well-connected (validated by graph structure)? |
| **Benchmark** | 8% | Fifth: is it validated by benchmarks? |
| **Framework** | 7% | Sixth: does it fit the user's framework preference? |

**Total: 100%**

### 3.3 Ranking Strategy Modifiers

**Time-Optimized (prioritize_by="time"):**
```yaml
R: 30%  # Slightly reduce relevance
P: 15%  # Reduce priority
T: 40%  # MAXIMIZE time efficiency
G: 8%
B: 4%
F: 3%
```

**Difficulty-Optimized (prioritize_by="difficulty"):**
```yaml
R: 40%  # Increase relevance
P: 30%  # MAXIMIZE priority (foundational skills)
T: 5%   # Minimize time consideration
G: 15%  # Increase graph (dependencies matter)
B: 6%
F: 4%
```

**Popularity-Optimized (prioritize_by="popularity"):**
```yaml
R: 25%
P: 20%
T: 10%
G: 30%  # MAXIMIZE graph centrality (popular skills are well-connected)
B: 10%
F: 5%
```

**Latest-Optimized (prioritize_by="latest"):**
```yaml
R: 30%
P: 20%
T: 10%
G: 5%
B: 30%  # MAXIMIZE benchmark (recent benchmarks = latest tech)
F: 5%
# Add: Recency multiplier (skills updated in last 6 months get 1.2× boost)
```

---

## SECTION 4: ARCHITECTURE OUTPUT OBJECT

### 4.1 Canonical JSON Schema

```typescript
interface ArchitectOutput {
  // Metadata
  generated_at: string;            // ISO timestamp
  version: string;                 // Spec version (e.g., "1.0")
  
  // User Intent (normalized)
  intent: NormalizedIntent;
  
  // Recommendation
  recommendation: {
    goal: {
      id: string;
      category: string;
      sub_goal: string;
      difficulty: string;
    };
    
    blueprint: ArchitectureBlueprint;
    
    confidence: ConfidenceScore;
    
    explanations: RecommendationExplanation[];
  };
  
  // Alternatives (if requested)
  alternatives?: {
    alternative_paths: {
      path_id: string;
      title: string;
      tradeoff: string;
      estimated_hours: number;
    }[];
    alternative_frameworks: {
      framework: string;
      suitability_score: number;
      reason: string;
    }[];
  };
  
  // Metadata for tracking
  session_id?: string;
  user_id?: string;
}
```

### 4.2 Example Output (Complete)

```json
{
  "generated_at": "2026-06-14T15:30:00Z",
  "version": "1.0",
  "intent": {
    "goal_id": "G01.4",
    "goal_category": "Coding Agent",
    "sub_goal": "Debugging",
    "difficulty": "advanced",
    "difficulty_score": 8,
    "time_budget_hours": 30,
    "framework_preferences": {
      "preferred": ["custom"],
      "excluded": []
    }
  },
  "recommendation": {
    "goal": {
      "id": "G01.4",
      "category": "Coding Agent",
      "sub_goal": "Debugging",
      "difficulty": "advanced"
    },
    "blueprint": {
      "required_skills": [
        {
          "id": "tool-use",
          "title": "Tool Use",
          "category": "06-tool-use",
          "priority": 1,
          "learn_time_hours": 6,
          "difficulty_score": 6,
          "prerequisites": ["api-calling"]
        },
        {
          "id": "code-analysis",
          "title": "Code Analysis",
          "category": "05-code",
          "priority": 2,
          "learn_time_hours": 8,
          "difficulty_score": 7,
          "prerequisites": []
        },
        {
          "id": "planning",
          "title": "Planning",
          "category": "02-reasoning",
          "priority": 3,
          "learn_time_hours": 5,
          "difficulty_score": 5,
          "prerequisites": []
        },
        {
          "id": "reflection",
          "title": "Reflection / Reflexion",
          "category": "02-reasoning",
          "priority": 4,
          "learn_time_hours": 4,
          "difficulty_score": 5,
          "prerequisites": ["planning"]
        },
        {
          "id": "error-recovery",
          "title": "Error Recovery",
          "category": "09-agentic-patterns",
          "priority": 5,
          "learn_time_hours": 3,
          "difficulty_score": 4,
          "prerequisites": []
        }
      ],
      "optional_skills": [
        {
          "id": "web-search",
          "title": "Web Search",
          "benefit": "Look up error messages and Stack Overflow solutions",
          "learn_time_hours": 2
        }
      ],
      "learning_path": [
        {
          "phase": 1,
          "phase_name": "Foundation",
          "skills": ["tool-use", "code-analysis"],
          "estimated_hours": 14,
          "milestone": "Can analyze code and run debuggers"
        },
        {
          "phase": 2,
          "phase_name": "Reasoning",
          "skills": ["planning", "reflection"],
          "estimated_hours": 9,
          "milestone": "Can form hypotheses and validate fixes"
        },
        {
          "phase": 3,
          "phase_name": "Robustness",
          "skills": ["error-recovery"],
          "estimated_hours": 3,
          "milestone": "Can handle failures gracefully"
        }
      ],
      "architecture": {
        "nodes": [
          {"id": "tool-use", "label": "Tool Use", "type": "required"},
          {"id": "code-analysis", "label": "Code Analysis", "type": "required"},
          {"id": "planning", "label": "Planning", "type": "required"},
          {"id": "reflection", "label": "Reflection", "type": "required"},
          {"id": "error-recovery", "label": "Error Recovery", "type": "required"}
        ],
        "edges": [
          {"source": "planning", "target": "reflection", "type": "enables"},
          {"source": "tool-use", "target": "code-analysis", "type": "complements"}
        ]
      },
      "framework_recommendation": {
        "recommended_framework": "custom",
        "confidence": 0.95,
        "suitability_score": 4.8,
        "maturity": "production",
        "ecosystem_fit": 0.92
      },
      "total_estimated_hours": 26
    },
    "confidence": {
      "overall_score": 87,
      "rating": "good",
      "breakdown": {
        "goal_coverage": 92,
        "skill_coverage": 85,
        "graph_coverage": 78,
        "benchmark_coverage": 60,
        "framework_confidence": 95
      },
      "risks": ["Limited benchmark data for error-recovery"],
      "gaps": []
    },
    "explanations": [
      {
        "skill_id": "tool-use",
        "why_selected": "\"Tool Use\" was selected because:\n- It satisfies the Tool Execution capability (priority: critical)\n- It is a hard dependency of code-analysis\n- It has 95% compatibility with custom framework\n- Estimated learning time: 6 hours (difficulty: 6/10)\n- Graph analysis shows it is frequently paired with planning, reflection",
        "why_not_alternatives": [],
        "risks": ["Learning curve: 6/10", "Stability: stable"],
        "what_unlocks": "After learning \"Tool Use\", you will be able to:\n- Execute external tools\n- Call APIs\n- Run debuggers and linters\nBuild: Simple debugging agents, tool-calling bots"
      }
    ]
  }
}
```

---

## SECTION 5: FAILURE MODES

### 5.1 Missing Data

**Scenario:** User requests goal with incomplete taxonomy mapping

**Detection:**
```python
if goal not in taxonomy:
    raise GoalNotFoundError(f"Goal {goal_id} not defined in taxonomy")

if len(capabilities) < 3:
    warning = "Sparse capability mapping (< 3 capabilities)"
```

**Handling:**
1. Return partial recommendation
2. Flag low confidence score (< 60)
3. Suggest alternative goals
4. Recommend fallback to keyword search

**Output:**
```json
{
  "error": "incomplete_taxonomy",
  "message": "Goal G13.1 has sparse capability mapping",
  "confidence": 42,
  "fallback": "keyword_search",
  "suggestions": ["G01.4", "G03.1"]
}
```

---

### 5.2 Weak Graph Coverage

**Scenario:** Recommended skills have < 20% graph connections

**Detection:**
```python
connectivity = (skills_with_edges / total_skills)
if connectivity < 0.2:
    warning = "Weak graph coverage"
```

**Handling:**
1. Lower confidence score by 20 points
2. Add risk: "Limited skill relationship data"
3. Recommend manual review

**Output:**
```json
{
  "confidence": 55,
  "risks": ["Weak graph coverage (18% connected)"],
  "recommendation": "Manual review suggested"
}
```

---

### 5.3 Conflicting Frameworks

**Scenario:** User prefers framework incompatible with goal

**Detection:**
```python
if framework_compatibility_score < 0.4:
    conflict = True
```

**Handling:**
1. Warn user of low compatibility
2. Suggest alternative framework
3. Allow override with --force flag

**Output:**
```json
{
  "warning": "framework_conflict",
  "message": "LlamaIndex has low compatibility (35%) with Debugging goal",
  "suggested_framework": "custom",
  "allow_override": true
}
```

---

### 5.4 Unsupported Goals

**Scenario:** Goal exists but has 0 skill mappings

**Detection:**
```python
if len(mapped_skills) == 0:
    raise UnsupportedGoalError()
```

**Handling:**
1. Return error
2. Suggest related goals
3. Recommend contributing to taxonomy

**Output:**
```json
{
  "error": "unsupported_goal",
  "message": "Goal G13.2 has no skill mappings",
  "related_goals": ["G13.1"],
  "contribution_guide": "https://github.com/SamoTech/skills-tree/blob/main/CONTRIBUTING.md"
}
```

---

## SECTION 6: QUALITY METRICS

### 6.1 Recommendation Accuracy

**Definition:** Percentage of recommendations that users accept

**Measurement:**
```python
accuracy = (accepted_recommendations / total_recommendations) × 100
```

**Target:** > 75%

**Collection Method:**
- Track user actions: "Accept", "Reject", "Modify"
- A/B test recommendation strategies
- Survey users on satisfaction

---

### 6.2 Blueprint Acceptance

**Definition:** Percentage of blueprints users implement

**Measurement:**
```python
acceptance = (blueprints_implemented / blueprints_generated) × 100
```

**Target:** > 60%

**Collection Method:**
- Track "Start Learning" clicks
- Track "Save Blueprint" actions
- Follow-up surveys ("Did you build this?")

---

### 6.3 User Satisfaction

**Definition:** Average rating of recommendation quality

**Measurement:**
```python
satisfaction = average(user_ratings)  # 1-5 stars
```

**Target:** > 4.0 / 5.0

**Collection Method:**
- Prompt after blueprint generation: "Rate this recommendation (1-5 stars)"
- Optional feedback: "What could be improved?"

---

### 6.4 Repeat Usage

**Definition:** Percentage of users who use Architect multiple times

**Measurement:**
```python
repeat_usage = (users_with_2plus_sessions / total_users) × 100
```

**Target:** > 40%

**Collection Method:**
- Track session IDs
- Track user IDs (if logged in)
- Measure time-to-second-use

---

## SECTION 7: IMPLEMENTATION NOTES

### 7.1 What This Spec Defines

✅ **9-stage recommendation pipeline**  
✅ **Scoring formulas with weights**  
✅ **Confidence calculation**  
✅ **Explanation generation**  
✅ **Canonical output schema**  
✅ **Failure modes and handling**  
✅ **Quality metrics**  

### 7.2 What This Spec Does NOT Define

❌ **Implementation code** (deferred to N-04, N-05)  
❌ **UI/UX** (out of scope for intelligence layer)  
❌ **API endpoints** (deferred to MVP implementation)  
❌ **Database schema** (deferred to persistence layer)  

### 7.3 Dependencies

**This spec depends on:**
- N-01: ARCHITECT_DATA_CONTRACT_AUDIT.md (data sources)
- N-02: GOAL_TAXONOMY.md (intent understanding)

**This spec enables:**
- N-04: Graph Query Logic (graph expansion implementation)
- N-05: Blueprint Output Schema (final output format)

### 7.4 Next Steps

**Immediate:**
1. **N-04: Graph Query Logic** — implement graph expansion (Stage 4)
   - Define graph traversal algorithms
   - Define dependency resolution
   - Define bundle discovery

2. **N-05: Blueprint Output Schema** — finalize output format (refine Section 4)
   - JSON schema validation
   - Versioning strategy
   - Backward compatibility

**After N-04 and N-05:**
- Implement recommendation engine (code)
- Build API layer
- Create MVP UI

---

## Conclusion

### What This Spec Achieves

**Before N-03:**
- Recommendation Layer: 0%
- Skills Tree = Catalog

**After N-03:**
- Recommendation Layer: 95% (spec complete, implementation pending)
- Skills Tree = Operating System (with intelligence core defined)

### The Transformation

**This spec transforms:**
```
"Show me skills for debugging"
  ↓
[tool-use, code-analysis, planning, reflection, error-recovery]
```

**Into:**
```
"Show me skills for debugging"
  ↓
Complete Architecture Blueprint:
- 5 required skills (ordered by dependency)
- 1 optional skill (web-search)
- 3-phase learning path (26 hours total)
- Framework: Custom (95% confidence)
- Architecture diagram (nodes + edges)
- Confidence: 87/100 (Good)
- Full explanation for every decision
```

### The Moat

This 9-stage pipeline is **not reproducible from the repository alone**.

Competitors would need:
1. Goal Taxonomy (287 skill mappings)
2. Capability decomposition (156 capabilities)
3. Framework compatibility matrix (12 goals × 6 frameworks)
4. Graph intelligence (723 relationships)
5. Scoring formulas (6 factors, weighted)
6. Confidence engine (5 metrics)
7. Explanation templates (4 types)

**This is the intelligence moat.**

---

**Spec Complete**  
**Recommendation Layer: 95% (Design Complete)**  
**Next: N-04 Graph Query Logic**

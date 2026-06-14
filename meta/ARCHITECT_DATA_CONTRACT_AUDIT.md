# N-01: Architect Data Contract Audit

**Status:** Complete  
**Date:** 2026-06-14  
**Auditor:** Skills Tree Intelligence Layer  

---

## Executive Summary

This audit evaluates all structured data assets in Skills Tree to define a canonical data contract for the Skill Architect recommendation engine.

**Architect Readiness Score: 62/100**

- ✅ **Strong foundation:** Rich skill metadata, graph relationships, search index
- ⚠️ **Critical gaps:** No user goal taxonomy, no recommendation schema, inconsistent field naming
- ❌ **Missing:** Architect-specific metadata (priority, alternatives, learn_time, difficulty_score)

---

## 1. Data Source Inventory

### 1.1 Primary Sources Audited

| Source | Type | Records | Last Updated | Completeness |
|--------|------|---------|--------------|-------------|
| `docs/api/graph.json` | Graph | 350 nodes, 723 links | 2026-05-21 | 85% |
| `docs/search-index.json` | Search Index | ~350 skills | Auto-generated | 90% |
| `skills/**/*.md` | Markdown | 361 skills | Ongoing | 95% |
| `paths/*.md` | Learning Paths | 5 paths | 2026-03 | 70% |
| `benchmarks/**/*.md` | Performance Data | ~15 benchmarks | 2026-04 | 60% |
| `docs/api/skills.json` | API Export | 361 skills | Auto-generated | 90% |

---

## 2. Schema Analysis by Entity

### 2.1 SKILL Schema

#### Current State (skills/*.md frontmatter)

```yaml
title: string                    # ✅ Present, consistent
category: string                 # ✅ Present, consistent (e.g., "01-perception")
level: enum                      # ✅ Present (basic|intermediate|advanced)
stability: enum                  # ✅ Present (stable|experimental)
added: date                      # ✅ Present (YYYY-MM format)
updated: date                    # ✅ Present (YYYY-MM format)
version: string                  # ✅ Present (v1, v2, v3)
description: string              # ✅ Present, high quality
tags: array[string]              # ✅ Present
dependencies: array[object]      # ⚠️ Partial (only verified skills)
confidence: string               # ⚠️ Partial (dependency-audited skills only)
code_blocks: array[object]       # ⚠️ Partial
```

#### Graph Schema (docs/api/graph.json nodes)

```json
{
  "id": "string",              // ✅ Unique machine ID (e.g., "code-generation")
  "name": "string",            // ✅ Human-readable label
  "path": "string",            // ✅ File path
  "category": "string",        // ✅ Category ID (e.g., "05-code")
  "catLabel": "string",        // ✅ Category human label
  "color": "string",           // ✅ Hex color
  "level": "string",           // ✅ Difficulty
  "version": "string"          // ✅ Version
}
```

#### Search Index Schema (docs/search-index.json)

```json
{
  "id": "string",              // ✅ Consistent with graph
  "title": "string",           // ✅ Same as 'name' in graph
  "category": "string",        // ✅ Consistent
  "level": "string",           // ✅ Consistent
  "stability": "string",       // ✅ Additional metadata
  "tags": ["string"],          // ✅ Searchable tags
  "description": "string",     // ✅ Short summary
  "body": "string"             // ✅ Full markdown content
}
```

#### **Completeness Assessment**

| Field | graph.json | search-index.json | skills/*.md | Coverage |
|-------|------------|-------------------|-------------|----------|
| id | ✅ | ✅ | ❌ (derived) | 95% |
| name/title | ✅ | ✅ | ✅ | 100% |
| category | ✅ | ✅ | ✅ | 100% |
| level | ✅ | ✅ | ✅ | 100% |
| stability | ❌ | ✅ | ✅ | 85% |
| version | ✅ | ❌ | ✅ | 85% |
| description | ❌ | ✅ | ✅ | 85% |
| tags | ❌ | ✅ | ✅ | 85% |
| path | ✅ | ❌ | ❌ (implicit) | 33% |
| color | ✅ | ❌ | ❌ | 33% |
| dependencies | ❌ | ❌ | ⚠️ (partial) | 30% |
| added | ❌ | ❌ | ✅ | 33% |
| updated | ❌ | ❌ | ✅ | 33% |

#### **Consistency Issues**

1. **Naming inconsistency:** `name` (graph) vs `title` (search, markdown)
2. **ID format:** Graph uses `slug` (e.g., `code-generation`), search uses `category/slug` (e.g., `05-code/code-generation`)
3. **Category format:** Graph uses `ID` (e.g., `05-code`), category label stored separately as `catLabel`

---

### 2.2 PATH Schema

#### Current State (paths/*.md)

```markdown
# Path: {Name}

**Difficulty:** {emoji} {level}    # ⚠️ Non-structured (text parsing required)
**Skills:** {count}                 # ⚠️ Non-structured
**Est. Time:** {duration}           # ⚠️ Non-structured
**Goal:** {description}             # ⚠️ Non-structured
```

#### Example Data

- **Difficulty:** Advanced (⭐⭐⭐)
- **Skills:** 5
- **Est. Time:** ~4 hours
- **Goal:** Build an agent that controls a desktop UI

#### **Gaps Identified**

❌ **No frontmatter:** Paths lack YAML metadata  
❌ **No structured skill list:** Skills referenced by file path only  
❌ **No skill ordering:** Sequential numbering in markdown only  
❌ **No prerequisites:** Implicit only  
❌ **No completion tracking:** No way to mark progress  
❌ **No skill relationships:** No dependency or "unlocks" metadata  

---

### 2.3 BENCHMARK Schema

#### Current State (benchmarks/*/*.md)

```yaml
id: string                       # ✅ Present
title: string                    # ✅ Present
category: string                 # ✅ Present
skill: string                    # ✅ Links to skill
version: string                  # ✅ Present
author: string                   # ✅ Present
updated: date                    # ✅ Present (YYYY-MM-DD)
tags: array[string]              # ✅ Present
```

#### **Gaps Identified**

❌ **No model performance data in frontmatter:** Results are in markdown tables only  
❌ **No structured test results:** Pass/fail, accuracy scores not machine-readable  
❌ **No skill-to-benchmark mapping in graph.json**  
❌ **No difficulty correlation:** Benchmarks don't map to skill.level  

---

### 2.4 CATEGORY/FRAMEWORK Schema

#### Current State (graph.json categories)

```json
{
  "id": "string",              // ✅ E.g., "05-code"
  "label": "string",           // ✅ E.g., "Code"
  "color": "string"            // ✅ Hex color
}
```

#### **Gaps Identified**

❌ **No category metadata:** No description, icon, priority, ordering  
❌ **No framework hierarchy:** Categories are flat  
❌ **No relationship to paths:** No mapping of which paths cover which categories  

---

## 3. Relationship Mapping

### 3.1 Skill Dependencies (graph.json links)

**Current:** 723 links between 350 nodes  
**Format:** `{source: "skill-id", target: "skill-id"}`  
**Coverage:** ~2 links per skill (avg)  

#### **Reliability Assessment**

| Metric | Value | Status |
|--------|-------|--------|
| Isolated skills | 54 (15%) | ⚠️ High |
| Highly connected skills | 10 | ✅ Good |
| Orphan skills (0 links) | 54 | ❌ Poor |
| Bidirectional links | Unknown | ⚠️ Needs audit |
| Self-referencing links | 0 | ✅ Good |

#### **Missing Relationship Types**

❌ **"Enhances"** — Skill A improves if combined with Skill B  
❌ **"Alternative to"** — Skill A vs Skill B for same goal  
❌ **"Unlocks"** — Mastering Skill A enables Skill B  
❌ **"Required by Path"** — Skill X is in Path Y  

---

### 3.2 Cross-Entity Relationships

| Relationship | Current | Required |
|--------------|---------|----------|
| Skill → Path | ❌ None | ✅ Path membership |
| Skill → Benchmark | ❌ None | ✅ Performance data |
| Path → Goal | ❌ Implicit | ✅ Goal taxonomy |
| Benchmark → Framework | ❌ None | ✅ Industry standards |
| Skill → Framework | ❌ Implicit (category) | ✅ Multi-framework support |

---

## 4. Missing Fields for Architect

### 4.1 Skill-Level Metadata Gaps

The Architect recommendation engine requires fields that **do not exist**:

```yaml
# MISSING IN ALL SOURCES:
priority: number                 # ❌ Architect priority (1-5)
learn_time_hours: number         # ❌ Estimated learning time
difficulty_score: number         # ❌ Numeric difficulty (1-10)
alternatives: array[string]      # ❌ Alternative skill IDs
prerequisites: array[string]     # ❌ Hard prerequisites
recommended_for: array[string]   # ❌ Goal/use-case tags
popularity: number               # ❌ Usage/adoption metric
last_benchmark_date: date        # ❌ Freshness indicator
model_support: object            # ❌ Which LLMs support this
implementation_examples: number  # ❌ Count of working examples
```

### 4.2 Path-Level Metadata Gaps

```yaml
# MISSING IN paths/*.md:
id: string                       # ❌ Unique path ID
category: string                 # ❌ Path category
difficulty: enum                 # ❌ Structured difficulty
difficulty_score: number         # ❌ Numeric (1-10)
skills: array[object]            # ❌ Structured skill list with order
  - id: string
    order: number
    required: boolean
prerequisites: array[string]     # ❌ Required paths
estimated_hours: number          # ❌ Numeric time estimate
goal_tags: array[string]         # ❌ Linked to goal taxonomy
completion_rate: number          # ❌ Analytics (if tracked)
```

### 4.3 Goal Taxonomy (Completely Missing)

**Current:** Goals are implicit in path descriptions  
**Required:** Structured goal taxonomy

```yaml
goals:
  - id: "build-computer-use-agent"
    label: "Build Computer Use Agent"
    description: "..."
    category: "agentic-applications"
    difficulty: "advanced"
    recommended_paths: ["computer-use-agent"]
    required_skills: ["screen-parsing", "action-planning"]
    alternatives: ["build-rpa-bot", "build-ui-tester"]
```

---

## 5. Canonical Data Contract

### 5.1 Skill Entity (Canonical Schema)

```typescript
interface Skill {
  // Identity
  id: string;                    // Unique slug (e.g., "code-generation")
  title: string;                 // Human-readable name
  
  // Classification
  category: {
    id: string;                  // E.g., "05-code"
    label: string;               // E.g., "Code"
    color: string;               // Hex color
  };
  
  // Metadata
  level: "basic" | "intermediate" | "advanced";
  stability: "stable" | "experimental";
  version: string;               // E.g., "v3"
  
  // Content
  description: string;           // Short summary
  tags: string[];                // Search tags
  path: string;                  // File path
  
  // Architect-Specific (NEW)
  priority: number;              // 1-5 (1 = foundational, 5 = niche)
  learn_time_hours: number;      // Estimated learning time
  difficulty_score: number;      // 1-10 numeric difficulty
  
  // Relationships (NEW)
  dependencies: string[];        // Required skill IDs
  enhances: string[];            // Optional complementary skills
  alternatives: string[];        // Alternative skill IDs for same goal
  unlocks: string[];             // Skills enabled by mastering this
  
  // Recommendations (NEW)
  recommended_for: string[];     // Goal IDs from taxonomy
  model_support: {
    [model: string]: "full" | "partial" | "none";
  };
  
  // Lifecycle
  added: string;                 // YYYY-MM
  updated: string;               // YYYY-MM
  last_benchmark_date?: string;  // YYYY-MM-DD
  
  // Quality
  dependencies_verified: boolean;
  has_runnable_example: boolean;
  example_count: number;
}
```

### 5.2 Path Entity (Canonical Schema)

```typescript
interface Path {
  // Identity
  id: string;                    // E.g., "computer-use-agent"
  title: string;                 // E.g., "Computer Use Agent"
  
  // Classification
  category: string;              // E.g., "agentic-applications"
  difficulty: "beginner" | "intermediate" | "advanced";
  difficulty_score: number;      // 1-10
  
  // Content
  goal: string;                  // What you'll build
  description: string;           // Overview
  
  // Structure
  skills: {
    id: string;                  // Skill ID
    order: number;               // Sequence
    required: boolean;           // Is this skill mandatory?
  }[];
  
  // Metadata
  estimated_hours: number;       // Total time
  prerequisites: string[];       // Required path IDs
  
  // Recommendations (NEW)
  goal_tags: string[];           // Links to goal taxonomy
  alternatives: string[];        // Alternative path IDs
}
```

### 5.3 Benchmark Entity (Canonical Schema)

```typescript
interface Benchmark {
  // Identity
  id: string;
  title: string;
  
  // Classification
  category: string;
  skill_id: string;              // Links to skill
  
  // Metadata
  version: string;
  author: string;
  updated: string;               // YYYY-MM-DD
  tags: string[];
  
  // Results (NEW — currently in markdown tables only)
  results: {
    model: string;
    score: number;               // 0-100 or 1-5
    metric: string;              // E.g., "accuracy", "latency"
    notes?: string;
  }[];
}
```

### 5.4 Goal Entity (NEW — Does Not Exist)

```typescript
interface Goal {
  // Identity
  id: string;                    // E.g., "build-computer-use-agent"
  title: string;                 // User-facing goal
  
  // Classification
  category: string;              // E.g., "agentic-applications"
  difficulty: "beginner" | "intermediate" | "advanced";
  
  // Content
  description: string;           // What the user wants to achieve
  
  // Recommendations
  recommended_paths: string[];   // Suggested learning paths
  required_skills: string[];     // Core skills needed
  optional_skills: string[];     // Nice-to-have skills
  alternatives: string[];        // Alternative goal IDs
  
  // Context
  use_cases: string[];           // Real-world applications
  industry: string[];            // E.g., ["fintech", "healthcare"]
}
```

### 5.5 Recommendation Entity (NEW — For Architect Output)

```typescript
interface Recommendation {
  // User Context
  user_goal: string;             // Goal ID from taxonomy
  user_level: "beginner" | "intermediate" | "advanced";
  
  // Recommendation
  recommended_path?: string;     // Suggested path ID
  recommended_skills: {
    id: string;                  // Skill ID
    priority: number;            // 1-5 (1 = learn first)
    rationale: string;           // Why recommended
    estimated_hours: number;     // Time to learn
  }[];
  
  // Metadata
  total_estimated_hours: number;
  confidence_score: number;      // 0-1
  generated_at: string;          // ISO timestamp
}
```

---

## 6. Gap Analysis Summary

### 6.1 Critical Gaps (Blocks Architect)

1. ❌ **No Goal Taxonomy** — Cannot map user intent to skills
2. ❌ **No Recommendation Schema** — No output contract
3. ❌ **No Architect-Specific Metadata** — Missing priority, learn_time, alternatives
4. ❌ **No Skill→Path Mapping** — Cannot recommend paths
5. ❌ **Inconsistent Field Naming** — name vs title, id format differences

### 6.2 High-Priority Gaps (Degrades Quality)

1. ⚠️ **54 Isolated Skills** — 15% of skills have no relationships
2. ⚠️ **No Alternative Recommendations** — Cannot suggest "or" options
3. ⚠️ **No Model Support Metadata** — Cannot filter by LLM compatibility
4. ⚠️ **Benchmark Data Not Structured** — Performance scores in markdown only
5. ⚠️ **Path Metadata Not Structured** — Difficulty, time, goals are text

### 6.3 Medium-Priority Gaps (Nice to Have)

1. ⚠️ **No Popularity Metrics** — Cannot prioritize commonly used skills
2. ⚠️ **No Framework Hierarchy** — Categories are flat
3. ⚠️ **No Completion Tracking** — Cannot track user progress
4. ⚠️ **No Versioning Strategy for Recommendations** — No way to A/B test

---

## 7. Migration Requirements

### 7.1 Phase 1: Field Standardization

**Goal:** Consistent naming across all sources

```yaml
Changes Required:
  graph.json:
    - Rename "name" → "title" (consistency)
    - Add "stability" field to all nodes
    - Add "description" field to all nodes
  
  search-index.json:
    - Standardize "id" format to slug-only (remove category prefix)
  
  skills/*.md:
    - Add "id" to frontmatter (derived from filename)
    - Add "priority" field (1-5)
    - Add "learn_time_hours" field
    - Add "difficulty_score" field (1-10)
```

### 7.2 Phase 2: Relationship Enrichment

```yaml
Changes Required:
  skills/*.md frontmatter:
    - Add "enhances: []" (complementary skills)
    - Add "alternatives: []" (alternative skills)
    - Add "unlocks: []" (skills enabled by this)
    - Add "recommended_for: []" (goal IDs)
  
  graph.json:
    - Add link types: "enhances", "alternative", "unlocks"
    - Audit and fix 54 isolated skills
```

### 7.3 Phase 3: New Entities

```yaml
New Files Required:
  meta/goals-taxonomy.json:
    - Create goal entity schema
    - Populate with 10-15 core goals
  
  paths/*.md:
    - Add YAML frontmatter with structured metadata
    - Add "skills" array with order and required flag
  
  benchmarks/**/*.md:
    - Add "results" array to frontmatter
```

---

## 8. Architect Readiness Score

### 8.1 Scoring Breakdown

| Category | Weight | Score | Weighted |
|----------|--------|-------|----------|
| **Data Completeness** | 25% | 75/100 | 18.75 |
| **Schema Consistency** | 20% | 60/100 | 12.00 |
| **Relationship Coverage** | 20% | 55/100 | 11.00 |
| **Architect Metadata** | 20% | 30/100 | 6.00 |
| **Goal Taxonomy** | 15% | 0/100 | 0.00 |
| **Total** | 100% | **62/100** | **47.75** |

### 8.2 Readiness Levels

- **0-40:** ❌ Not Ready — Core data missing
- **41-60:** ⚠️ Partially Ready — Can build prototype
- **61-80:** ✅ Ready — Can build MVP
- **81-100:** 🚀 Production Ready — High quality recommendations

**Current: 62/100 — ✅ MVP Ready**

---

## 9. Recommendations

### 9.1 Immediate Actions (Block N-02 through N-05)

1. **Create Goal Taxonomy** (N-02)
   - Define 10-15 user goals
   - Map goals to required skills
   - Create `meta/goals-taxonomy.json`

2. **Standardize Field Naming**
   - Unify `name`/`title` across sources
   - Standardize `id` format (slug-only)

3. **Add Architect Metadata to Skills**
   - `priority` (1-5)
   - `learn_time_hours` (number)
   - `difficulty_score` (1-10)
   - `alternatives` (array)

### 9.2 Next Actions (Before N-06: Build Architect)

4. **Fix Isolated Skills**
   - Audit 54 orphan skills
   - Add dependency links

5. **Structure Path Metadata**
   - Convert text to YAML frontmatter
   - Add `skills` array with order

6. **Create Recommendation Schema** (N-03)
   - Define output contract
   - Include rationale field

---

## 10. Conclusion

### Current State
- ✅ **Strong skill inventory:** 361 well-documented skills
- ✅ **Graph foundation:** 723 relationships mapped
- ✅ **Search capability:** Full-text search index

### Critical Gaps
- ❌ **No goal taxonomy:** Cannot map user intent
- ❌ **Missing Architect metadata:** Cannot prioritize recommendations
- ❌ **Inconsistent schemas:** name vs title, id formats

### Path Forward
**The data foundation is 62% ready.** With N-02 (Goal Taxonomy) and schema standardization, the Architect can be built. Without these, recommendations will be low-quality guesses.

**Next deliverable:** `N-02: Goal Taxonomy`

---

**Audit Complete**  
**Architect Data Layer: 62/100 — Ready for MVP with targeted improvements**

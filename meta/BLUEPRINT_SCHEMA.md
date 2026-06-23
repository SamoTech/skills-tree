# BLUEPRINT_SCHEMA.md

**Initiative:** INITIATIVE-012C  
**Phase:** 3  
**Status:** COMPLETE — schema_version 1.0

---

## Blueprint Object Schema

```typescript
interface Blueprint {
  id: string;                  // goal slug, URL-safe
  goal: string;                // human display title
  summary: string;             // goal description
  skills: Skill[];             // all required skills, sorted
  learningPath: Skill[][];     // phases: array of skill arrays
  categories: string[];        // skill categories present
  difficulty: "beginner" | "intermediate" | "advanced";
  estimatedTime: string;       // e.g. "6–9 weeks"
  version: "1.0";
  generatedAt: string;         // ISO 8601 timestamp
}

interface Skill {
  id: string;        // e.g. "09-agentic-patterns/react-agent"
  title: string;
  category: string;  // e.g. "09-agentic-patterns"
  level: "basic" | "intermediate" | "advanced";
  stability: "stable" | "evolving" | "experimental";
  reason: string;    // why this skill is included
}
```

---

## Example JSON Export

```json
{
  "id": "rag-assistant",
  "goal": "RAG Assistant",
  "summary": "Retrieval-augmented assistant that answers questions grounded in a private document corpus.",
  "skills": [
    {
      "id": "03-memory/vector-database",
      "title": "Vector Database",
      "category": "03-memory",
      "level": "intermediate",
      "stability": "stable",
      "reason": "Core skill for this goal"
    },
    {
      "id": "03-memory/embedding-retrieval",
      "title": "Embedding Retrieval",
      "category": "03-memory",
      "level": "intermediate",
      "stability": "stable",
      "reason": "Core skill for this goal"
    },
    {
      "id": "09-agentic-patterns/rag-pattern",
      "title": "RAG Pattern",
      "category": "09-agentic-patterns",
      "level": "intermediate",
      "stability": "stable",
      "reason": "Core skill for this goal"
    }
  ],
  "learningPath": [
    [
      {"id": "03-memory/vector-database", "title": "Vector Database", "level": "intermediate"}
    ],
    [
      {"id": "09-agentic-patterns/rag-pattern", "title": "RAG Pattern", "level": "intermediate"}
    ]
  ],
  "categories": ["03-memory", "07-tool-use", "09-agentic-patterns"],
  "difficulty": "intermediate",
  "estimatedTime": "5–7 weeks",
  "version": "1.0",
  "generatedAt": "2026-06-23T12:00:00.000Z"
}
```

---

_Generated: INITIATIVE-012C Phase 3_

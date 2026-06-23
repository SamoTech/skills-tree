# BLUEPRINT SCHEMA
> Initiative: INITIATIVE-012C | Phase 3
> schema_version: 1.0

## Blueprint Object

```typescript
interface Blueprint {
  id: string;                    // e.g. "customer-support-agent"
  goal: string;                  // Human-readable goal title
  summary: string;               // 1-2 sentence description
  skills: SkillRef[];            // All required skills (ranked)
  dependencies: Edge[];          // prerequisite edges between skills
  learning_path: SkillRef[][];   // Topological order — array of phases
  recommended_categories: string[];
  difficulty: "beginner" | "intermediate" | "advanced";
  estimated_learning_time: string; // e.g. "4–6 weeks"
  exports: {
    json_url: string;            // Deep link to this blueprint as JSON
    share_url: string;           // /blueprints/?goal=<id>
  };
  version: string;               // "1.0"
  generated_at: string;          // ISO timestamp
}

interface SkillRef {
  id: string;
  title: string;
  category: string;
  level: "basic" | "intermediate" | "advanced";
  stability: "stable" | "evolving" | "experimental";
  reason: string;               // Why this skill is required
}

interface Edge {
  from: string;                  // skill id
  to: string;                    // skill id
  type: "prerequisite";
}
```

## Example JSON

```json
{
  "id": "rag-assistant",
  "goal": "RAG Assistant",
  "summary": "Build a retrieval-augmented assistant grounded in a private document corpus.",
  "skills": [
    {
      "id": "03-memory/rag",
      "title": "RAG (Retrieval-Augmented Generation)",
      "category": "03-memory",
      "level": "intermediate",
      "stability": "stable",
      "reason": "Core pattern for this blueprint"
    },
    {
      "id": "03-memory/vector-store-retrieval",
      "title": "Vector Store Retrieval",
      "category": "03-memory",
      "level": "intermediate",
      "stability": "stable",
      "reason": "Required for semantic search over documents"
    },
    {
      "id": "01-perception/document-parsing",
      "title": "Document Parsing",
      "category": "01-perception",
      "level": "intermediate",
      "stability": "stable",
      "reason": "Ingestion of source documents"
    }
  ],
  "dependencies": [
    { "from": "01-perception/document-parsing", "to": "03-memory/rag", "type": "prerequisite" },
    { "from": "03-memory/vector-store-retrieval", "to": "03-memory/rag", "type": "prerequisite" }
  ],
  "learning_path": [
    ["01-perception/document-parsing", "03-memory/vector-store-retrieval"],
    ["03-memory/rag"],
    ["09-agentic-patterns/agentic-rag"]
  ],
  "recommended_categories": ["03-memory", "09-agentic-patterns", "01-perception", "07-tool-use"],
  "difficulty": "intermediate",
  "estimated_learning_time": "3–5 weeks",
  "exports": {
    "json_url": "/blueprints/?goal=rag-assistant&format=json",
    "share_url": "/blueprints/?goal=rag-assistant"
  },
  "version": "1.0",
  "generated_at": "2026-06-23T14:00:00Z"
}
```

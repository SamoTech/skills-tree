# Blueprint Schema
**Initiative:** INITIATIVE-012C  
**Version:** 1.0.0

## Blueprint Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | URL-safe goal identifier |
| `goal` | string | Human-readable goal title |
| `summary` | string | One-sentence description |
| `skills` | string[] | All required skill IDs |
| `dependencies` | object | Skills grouped by category |
| `learning_path` | string[] | Topologically ordered skill list |
| `recommended_categories` | string[] | Primary skill categories |
| `difficulty` | enum | `basic\|intermediate\|advanced\|expert` |
| `estimated_learning_time` | string | Human-readable estimate |
| `skill_count` | integer | Total required skills |
| `category_count` | integer | Distinct skill categories |
| `exports` | object | Available export formats |
| `version` | string | Blueprint schema version |
| `generated_at` | string | ISO 8601 timestamp |

## Deep Link Pattern
```
/blueprints/?goal={goal-id}
```
Example: `/blueprints/?goal=rag-assistant`

## Export Formats
- **JSON**: Full blueprint object. Filename: `blueprint-{goal-id}.json`
- **Markdown**: Human-readable with skills, path, ASCII arch diagram. Filename: `blueprint-{goal-id}.md`

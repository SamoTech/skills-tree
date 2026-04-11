# Database Schema Design

**Category:** `code`  
**Skill Level:** `advanced`  
**Stability:** `stable`

### Description

Design normalized relational or document database schemas for a given domain, including tables, relationships, and indexes.

### Example

```sql
-- Skills Tree schema
CREATE TABLE skills (
    id      SERIAL PRIMARY KEY,
    slug    TEXT NOT NULL UNIQUE,
    title   TEXT NOT NULL,
    category TEXT NOT NULL,
    level   TEXT CHECK (level IN ('basic','intermediate','advanced'))
);

CREATE INDEX idx_skills_category ON skills(category);
```

### Related Skills

- [SQL Query Generation](sql-query-generation.md)
- [Database Write](../04-action-execution/database-write.md)

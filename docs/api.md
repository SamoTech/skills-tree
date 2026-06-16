# Python API Reference

The `skills_tree` Python package provides a clean API for programmatic access to the skill taxonomy.

## Installation

```bash
pip install skills-tree
```

## `SkillsTree`

The main entry point.

```python
from skills_tree import SkillsTree

st = SkillsTree()
```

### `SkillsTree.get(skill_id: str) -> Skill`

Fetch a skill by its ID.

```python
skill = st.get("rag")
print(skill.title)      # "Retrieval-Augmented Generation"
print(skill.category)   # "memory"
print(skill.version)    # "v3"
print(skill.badge)      # "verified"
```

**Raises:** `SkillNotFound` if the skill ID does not exist.

---

### `SkillsTree.search(query: str, limit: int = 20) -> list[Skill]`

Full-text search across all skill titles, descriptions, and tags.

```python
results = st.search("memory injection", limit=5)
for skill in results:
    print(skill.id, skill.title, skill.badge)
```

---

### `SkillsTree.categories() -> list[Category]`

List all 17 skill categories.

```python
categories = st.categories()
for cat in categories:
    print(cat.id, cat.name, cat.skill_count)
```

---

### `SkillsTree.get_category(category_id: str) -> list[Skill]`

Get all skills in a specific category.

```python
memory_skills = st.get_category("memory")
```

---

### `SkillsTree.recommend(task: str, top_k: int = 5) -> list[Skill]`

Recommend skills for a given task description using semantic similarity.

```python
recommendations = st.recommend(
    "I need to build an agent that remembers user preferences",
    top_k=5
)
```

---

## Data Models

### `Skill`

| Field | Type | Description |
|---|---|---|
| `id` | `str` | Unique skill identifier (slug) |
| `title` | `str` | Human-readable skill name |
| `category` | `str` | Parent category ID |
| `level` | `str` | `beginner`, `intermediate`, or `advanced` |
| `stability` | `str` | `experimental`, `beta`, or `stable` |
| `version` | `str` | Current version (e.g. `v3`) |
| `badge` | `str` | `verified`, `reviewed`, or `stub` |
| `tags` | `list[str]` | Associated tags |
| `related` | `list[str]` | Related skill IDs |
| `content` | `str` | Full Markdown content |

### `Category`

| Field | Type | Description |
|---|---|---|
| `id` | `str` | Category identifier (e.g. `memory`) |
| `name` | `str` | Display name |
| `skill_count` | `int` | Number of skills in this category |

# LEARNING_PATH_ENGINE.md

**Initiative:** INITIATIVE-012C  
**Phase:** 4  
**Status:** COMPLETE

---

## Overview

The Learning Path Engine converts an unordered skill set into a sequenced, phase-grouped learning plan using only the graph topology and category ordering.

---

## Algorithm

### Step 1: Category-based phase assignment

```
For each skill:
  phase_key = CAT_ORDER.indexOf(skill.category)
  if not found → phase_key = 99 ("other")
```

`CAT_ORDER` is a static constant that defines a pedagogically-ordered sequence:

```
01-perception → 02-reasoning → 03-memory → 04-action-execution
→ 05-code → 06-communication → 07-tool-use → 08-multimodal
→ 09-agentic-patterns → 10-computer-use → 11-web
```

This ordering ensures foundational skills (perception, reasoning, memory) appear before applied skills (orchestration, tool use, agentic patterns).

### Step 2: Level sub-ordering

Within each category phase:
```
basic skills first → intermediate → advanced
```

### Step 3: Phase merging

Small phases (< 2 skills) are merged with the next phase to avoid trivial one-item steps.

### Step 4: Output

```
learningPath = [
  Phase 1: [skill, skill, skill],  // foundational
  Phase 2: [skill, skill],         // intermediate
  ...
  Phase N: [skill],                // applied/advanced
]
```

---

## Topological Ordering Notes

The current engine uses **category order** as a proxy for topological order. Full prerequisite-graph topological sort (Kahn's algorithm) is documented as a gap:

### Gap: Deep Prerequisite Traversal

- **Current:** One level of prerequisite expansion (node.prerequisites → add to skill set)
- **Missing:** Recursive transitive closure (prerequisites of prerequisites)
- **Impact:** Low for current goals. Could matter for highly nested skill trees.
- **Planned:** Phase 2 upgrade after graph edge coverage reaches >90%

### Gap: Cycle Detection

- **Current:** No cycle detection in prerequisite expansion
- **Status:** SKILLS_GRAPH.json governance rules prohibit cycles; governance system enforces this
- **Risk:** Minimal

---

## Graceful Degradation

If `SKILLS_GRAPH.json` fails to load (network error, offline), the engine returns an empty skill list. The goal catalog and goal selection UI remain fully functional. A message is surfaced to the user.

---

_Generated: INITIATIVE-012C Phase 4_

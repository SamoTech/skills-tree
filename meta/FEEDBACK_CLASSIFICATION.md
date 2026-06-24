# FEEDBACK CLASSIFICATION FRAMEWORK

**Initiative:** INITIATIVE-014B — Phase 7  
**Purpose:** Standardize triage of post-launch feedback into INITIATIVE-014C scope items.

---

## Classification Taxonomy

### Class A — Bugs (P0 blockers)

Any feedback that prevents core functionality from working.

| Signal | Example |
|---|---|
| Explorer fails to load | "Graph doesn't render on Firefox" |
| CLI install fails | "pip install fails on Python 3.11" |
| Broken link in README | "Explorer link 404s" |
| API returns wrong data | "st.get('rag') returns None" |

**Response SLA:** Fix within 24h of report. Close loop in the original issue/comment with the fix commit.

---

### Class B — UX Friction

Functionality works but is confusing or hard to use.

| Signal | Example |
|---|---|
| "I couldn't find X" | Explorer search not surfacing expected results |
| "I didn't know Y existed" | Featured Skills strip missing a key skill |
| "How do I Z" | Unclear how to contribute a skill |
| "The difference between X and Y is unclear" | RAG vs Retrieval-Augmented-Generation ambiguity |

**Response SLA:** Acknowledge within 24h. Fix within 7 days.

---

### Class C — Missing Features

Requests for capabilities that don't exist yet.

| Signal | Example |
|---|---|
| "It would be great if..." | Export to JSON/YAML |
| "I wish it had..." | Framework filter (show only LangChain-compatible skills) |
| "Does it support X" | LlamaIndex integration |
| "Can I use it with..." | AutoGen, CrewAI, LangGraph |

**Response SLA:** Label with `skill-request` or `feature-request`. Add to INITIATIVE-014C backlog.

---

### Class D — Positioning / Taxonomy Confusion

Feedback that signals a conceptual misalignment.

| Signal | Example |
|---|---|
| "This is just a list of prompts" | Taxonomy scope unclear |
| "How is this different from LangChain Hub?" | Differentiation not landing |
| "Why 17 categories?" | Taxonomy structure questioned |
| "Some skills seem like the same thing" | Granularity inconsistency |

**Response SLA:** Answer publicly with a clear, specific response. If recurring, update README or docs.

---

### Class E — Confusion Points (Onboarding)

Feedback that signals friction in the first 5 minutes.

| Signal | Example |
|---|---|
| "I don't know where to start" | Entry point unclear |
| "What does 'battle-tested' mean?" | Badge definitions unclear |
| "Is this production-ready?" | Stability signals unclear |
| "I tried pip install and nothing happened" | CLI first-run experience gap |

**Response SLA:** Acknowledge in thread. Feed into README and QUICKSTART updates in 014C.

---

## Feedback Log Template

Add a row per feedback item to INITIATIVE-014C input:

```
| Source | Date | Class | Summary | Action |
|---|---|---|---|---|
| HN comment | 2026-06-30 | B | "Couldn't find LangGraph skills" | Add LangGraph filter tag |
| GitHub issue | 2026-07-01 | A | "Explorer 404 on Safari" | P0 — hotfix |
```

---

## Feedback Aggregation Rules

- If the **same Class D signal** appears 3+ times from different sources: it is a positioning problem, not a user error. Update README within 48h.
- If the **same Class C request** appears 3+ times: it becomes a P1 backlog item for 014C.
- If a **Class A bug** appears from 2+ different users: it is a systemic issue, not a one-off. Treat as P0 hotfix.

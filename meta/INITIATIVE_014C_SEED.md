# INITIATIVE-014C — POST-LAUNCH ITERATION

**Status:** SEED — scope finalized after T+7d feedback synthesis  
**Predecessor:** INITIATIVE-014B (Show HN Launch)  
**Activation condition:** T+7d war room check complete (2026-07-07)  
**Owner:** Graph Architect

---

## Purpose

INITIATIVE-014C converts real user feedback from the Show HN launch into the highest-ROI product improvements. It is driven entirely by signal from external users, not internal assumptions.

---

## Pre-Seeded Backlog (internal)

These items are already known from INITIATIVE-014A.2 scoring gaps. They enter 014C only if post-launch feedback confirms their importance.

| Item | Score Gap | Confirmation needed |
|---|---|---|
| OG image / social preview card | Growth +2 | Any social share CTR complaint |
| `good first issue` pre-population | Community +1 | Any "how do I contribute" confusion |
| Star ask in README hero | Growth +1 | Low star conversion vs page views |
| Analytics deployment (Plausible) | Growth +1 | After 500 stars milestone |
| Skill dependency mini-graph in panel | Product +1 | Any "I want to visualize" feedback |

---

## Input Channels

1. **HN comments** — classified per FEEDBACK_CLASSIFICATION.md
2. **GitHub issues** opened by external users
3. **GitHub Discussions** — Feedback thread + Feature Requests thread
4. **Reddit comments** on r/MachineLearning, r/LocalLLaMA
5. **LinkedIn comments**
6. **PyPI download anomalies** (sudden drop = install bug)

---

## Scope Finalization Process (T+7d)

1. Aggregate all Class A-E feedback items from all channels
2. Count frequency per item
3. Apply ROI formula: `impact × frequency / effort`
4. Select top 5 items as P0-P2 for 014C Phase 1
5. Remaining items become 014C backlog for Phase 2+

---

## Success Condition

014C is complete when:
- All Class A (bugs) from launch week are closed
- Top 3 Class B (UX) items are shipped
- Top 2 Class C (features) items are shipped or roadmapped
- LAUNCH_DASHBOARD.md 7d actuals are filled in

---

## Activation

This initiative activates automatically on 2026-07-07 after T+7d war room check.
INITIATIVE-014C will be formally scoped using the feedback log from LAUNCH_DASHBOARD.md.

# DECISION LOG

**Maintained by:** Governance Recovery R-01 / Verification R-01V  
**Version:** R-01V  
**Source of truth:** Repository commits, file content, and PROJECT_CONSTITUTION.md only  
**Rule:** Only decisions that can be proven from commits, files, or repository structure are recorded here.  
**Supreme Governing Document:** `meta/PROJECT_CONSTITUTION.md` (v1.0.0, ratified 2026-06-16)  
**Governing Rule:** Constitution Article V, G-03 — this log is append-only.

> **⚠️ INTEGRITY NOTICE**
> The previous DECISION_LOG.md was a placeholder (24 bytes). All entries in this
> file are derived exclusively from the commit history and verified file content.
> No decisions from prior agent sessions have been carried forward without commit
> evidence.

---

## FORMAT

Each entry requires:
- **Decision ID** (D-RRXX where RR = recovery round, XX = sequence)
- **Date** (from commit timestamp or file timestamp)
- **Evidence** (commit SHA or file reference — no evidence = not recorded)
- **Decision** and **Rationale**

---

## DECISIONS DERIVED FROM COMMIT HISTORY

---

### D-ARCH-01 — Static Markdown as CMS (PERMANENT)

**Date:** Pre-2026 (foundational)  
**Evidence:** PROJECT_MEMORY.md Section 16 (DO NOT IMPLEMENT)  
**Decision:** Use GitHub-hosted Markdown files as the content layer. No database backend.  
**Rationale:** "The entire value of the project is that content is in Markdown — diffable, clonable, offline-readable. GitHub as CMS is a core design principle."  
**Status:** PERMANENT — do not revisit

---

### D-ARCH-02 — Vanilla HTML/CSS/JS for UI (PERMANENT)

**Date:** Pre-2026 (foundational)  
**Evidence:** PROJECT_MEMORY.md Section 16  
**Decision:** Keep `docs/index.html` as vanilla HTML/CSS/JS. No Next.js, React, or bundler.  
**Rationale:** "Keeps the UI hackable by everyone" — avoids build complexity and contributor friction.  
**Status:** PERMANENT — no framework migration

---

### D-ARCH-03 — No Auto-Merge of AI-Generated Content (PERMANENT)

**Date:** Pre-2026 (foundational)  
**Evidence:** PROJECT_MEMORY.md Section 16  
**Decision:** All AI-generated skill upgrades require human review before merge.  
**Rationale:** "LLMs produce plausible but incorrect code. Auto-merge would destroy content quality."  
**Status:** PERMANENT — non-negotiable quality gate

---

### D-ARCH-04 — Free API Access Forever (PERMANENT)

**Date:** Pre-2026 (foundational)  
**Evidence:** PROJECT_MEMORY.md Section 16  
**Decision:** All API access remains free. Revenue from sponsorship and certification only, never API gates.  
**Rationale:** Paywalled API creates friction for the developer audience the project depends on for growth.  
**Status:** PERMANENT

---

### D-SEC-01 — Least-Privilege Permissions on All Workflows

**Date:** 2026-06-21T08:00:34Z  
**Evidence:** Commit `33af1551709a15922aee9db6b4fa575b8e402f63`  
**Decision:** Added least-privilege `permissions:` blocks to all GitHub Actions workflows. Files affected: `test-coverage.yml`, `build-and-verify.yml`, `clean-install-test.yml`, `verify-taxonomy.yml`.  
**Rationale:** Resolves CodeQL alert: "Workflow does not contain permissions". No functional changes to job logic.  
**Status:** APPLIED

---

### D-GRAPH-01 — Graph JSON Layer Does Not Exist (VERIFIED)

**Date:** 2026-06-21T12:15:13Z  
**Evidence:** Commit `71e93ebabe7aa359a3fff98a2013814eede969b5` (TASK-000A audit)  
**Decision:** `data/SKILLS_GRAPH.json` confirmed as 24-byte placeholder string. No graph has been built. The graph layer starts at zero.  
**Rationale:** Independent audit found SKILLS_GRAPH.json = 24 bytes = literal placeholder string. All prior claims of 47, 53, or 58 nodes are fabricated.  
**Status:** VERIFIED FACT — informs all future graph tasks

---

### D-GOV-01 — PROJECT_CONSTITUTION.md Status ~~MISSING~~ → CORRECTED: EXISTS

**Date (original):** 2026-06-21T12:32:21Z (R-01 recovery)  
**Date (correction):** 2026-06-21T15:39 EEST (R-01V.1 closure)  
**Evidence (original):** TASK-000A audit, `meta/VERIFIED_BASELINE_V2.md` Section 8  
**Evidence (correction):** Direct file read during R-01V — SHA `a8f73852ea977637cc01ff8fdcc0a2abb1214f2d`, size 12,312 bytes  

**Original assumption (R-01):** `meta/PROJECT_CONSTITUTION.md` is MISSING from the repository.  

**Corrected verified state (R-01V):** `meta/PROJECT_CONSTITUTION.md` EXISTS.  
- Size: 12,312 bytes  
- Blob SHA: `a8f73852ea977637cc01ff8fdcc0a2abb1214f2d`  
- Version: 1.0.0  
- Ratified: 2026-06-16  
- Authority: SamoTech Architect  
- Content: 10 binding principles (P-01–P-10), 8 priority categories, 6 governance rules (G-01–G-06), 5 success metrics (M-01–M-05), amendment process, conflict resolution priority order  
- Graph state at ratification: 38 nodes / 72 edges (Appendix A)  

**Classification:** Governance audit correction — R-01 mistakenly recorded the file as absent; R-01V direct read confirmed existence.  
**Impact:** The Constitution is the supreme governance authority (supersedes PROJECT_MEMORY.md per Article I). All future agent sessions must read it as the first governance document.  
**Status:** CORRECTED — contradiction count now 0

---

### D-GOV-02 — Governance Recovery R-01

**Date:** 2026-06-21T12:32:21Z  
**Evidence:** Commit `f27c7354ae46eba9e632aa7643681795e9f15605`  
**Decision:** Rebuild all four governance files (MEMORY_STATE, DECISION_LOG, AGENT_SKILLS_MASTER_PLAN, AGENT_SKILLS_BACKLOG) from repository evidence only. Void all prior agent claims.  
**Rationale:** All four files were placeholders (18-24 bytes). Repository cannot function as a governance artifact without real content in these files.  
**Status:** APPLIED — commit `f27c7354`

---

### D-GOV-03 — Governance Verification Passed (R-01V)

**Date:** 2026-06-21T15:39 EEST  
**Evidence:** Mission R-01V direct file reads; this commit  
**Decision:** Close R-01V verification. Governance layer confirmed operational.  

**Verification results:**
- `meta/MEMORY_STATE.md` — REAL_CONTENT (4,747B, commit `f27c7354`) ✅  
- `meta/DECISION_LOG.md` — REAL_CONTENT (5,908B, commit `f27c7354`) ✅  
- `meta/AGENT_SKILLS_MASTER_PLAN.md` — REAL_CONTENT (7,313B, commit `f27c7354`) ✅  
- `meta/AGENT_SKILLS_BACKLOG.md` — REAL_CONTENT (11,019B, commit `f27c7354`) ✅  
- `meta/PROJECT_CONSTITUTION.md` — EXISTS (12,312B, SHA `a8f73852`) ✅  
- `data/SKILLS_GRAPH.json` — PLACEHOLDER (24B, string literal) ⚠️  

**Contradiction count after R-01V.1:** 0  
**Governance readiness grade:** B (operational, graph layer still missing)  
**Fabricated claims voided:** All TASK-001 through TASK-005B completion claims remain voided  
**Graph status:** PLACEHOLDER — zero real nodes; next mission R-02 required  

**Status:** APPLIED — this commit

---

### D-DISC-01 — No Discord Until 10+ Monthly Contributors

**Date:** Pre-2026 (foundational)  
**Evidence:** PROJECT_MEMORY.md Section 16  
**Decision:** Do not create a Discord server until monthly contributor count exceeds 10.  
**Rationale:** "An empty Discord is worse than no Discord — it signals abandonment."  
**Status:** PERMANENT DEFERRAL — condition not yet met

---

## DECISIONS PENDING (observed gaps requiring a decision)

These are NOT decisions yet — they are observed gaps that require a decision:

| Gap | Required Decision |
|---|---|
| `data/SKILLS_GRAPH.json` is placeholder | Decide: execute R-02 to construct real graph from scratch |
| `paths/` directory exists but is empty | Decide: execute T-08 (4 learning tracks) as next task |
| Per-category READMEs missing | Decide: execute T-03 (17 README files) |
| 302 v1 stubs remain | Decide: begin T-04 (Stub Upgrade Wave 1) |
| Constitution at ratification shows 38 nodes / 72 edges; current graph unknown | Verify: read SKILLS_GRAPH.json and reconcile with Constitution Appendix A |

---

*This log was rebuilt during Mission R-01 on 2026-06-21.*  
*Version bumped R-01 → R-01V; D-GOV-01 corrected; D-GOV-03 added during Mission R-01V.1 on 2026-06-21.*  
*This log is append-only per Constitution Article V, G-03. Only add entries that can be proven from commit history, file content, or repository structure.*

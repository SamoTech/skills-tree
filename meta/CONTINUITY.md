# Skills Tree — Sustainability and Continuity Mandate

> Status: ACTIVE — 2026-10-14, owner-directed.
> This file is the sustainability contract for SamoTech/skills-tree. It exists so
> the project cannot die through the loss of a person, a session, or a tool:
> any AI agent or human must be able to resume development from this repository
> alone, with the authoritative documentation acting as the project brain.

## Why this file exists

The repository owner directed (2026-10-14) that continuity and perpetual
development capability is the primary sustainability objective: the repository
must remain permanently developable, with documentation kept continuously
synchronized, so that any agent can pick up the work without prior
conversation context.

## Non-negotiable invariants

1. Never weaken CI, quality, security, or governance gates to make a change pass.
2. Documentation synchronization is a blocking completion gate (AGENTS.md).
3. Never fabricate demand, adoption, benchmark, quality, or production claims.
4. `skills/` is the canonical registry source; generated artifacts are projections.
5. Merge only after full CI green at the exact head (squash-merge protocol).

## Self-sustaining systems already in place

- Fail-closed benchmark runners (CAP-011, CAP-014) are re-executed by CI on every
  push; committed reports are machine-verified, not agent-asserted.
- The zero-touch semantic-release pipeline (with hourly self-heal) releases merged
  work even when an individual release run is cancelled by the writer-queue race.
- Generated projections (graph, search index, Skills API, badges, quality report,
  changelog) rebuild through trusted workflows after every merge.
- The evaluation harness and its evidence protocol are the durable, hard-to-
  replicate asset; the skill corpus alone is commodity content in a world where
  models can generate comparable instructions on demand.

## Standing queue (never-empty next actions)

This queue is never allowed to be empty. Whenever an item completes or blocks,
replace it in the same delivery cycle by promoting or adding a next action.

1. **Productize the evaluation harness** — make the fail-closed benchmark protocol
   usable by external agent maintainers (generalized runners, protocol
   documentation, published methodology). This is the primary growth surface.
   Status: public protocol documentation published on main
   (`benchmarks/EVALUATION-PROTOCOL.md`, linked from the benchmarks index);
   the next increment is a generalized external-candidate runner and
   adoption guide. No new registry authority is created.
2. **Strengthen public distribution** — keep the Pages discovery surface,
   `docs/api/skills.json`, and the multi-platform Agent Skills compatibility
   (agentskills.io open format) as the primary distribution story.
   Status: live; hardening is continuous.
3. **Second, non-overlapping candidate** — run an external candidate system
   (different model family) against the executed CAP-011 and CAP-014 contracts
   to remove the disclosed same-family limitation.
   Status: NOT RUN; requires an external candidate runtime.
4. **CAP-007 labeled dataset** — the remaining unexecuted evaluation contract.
   Status: blocked on an independently human-labeled 100-query dataset;
   do not fabricate labels.
5. **Quality-first corpus expansion** — add skills only from recorded,
   reproducible demand evidence (`meta/MOST-WANTED-SKILLS.md`), never raw-count
   growth without a measured gap.

## Succession procedure for a new agent

1. Read `AGENTS.md` and its preflight list (including this file).
2. Verify live `main` state; never trust conversation memory or cached reports.
3. Select the highest-priority unblocked item from the standing queue.
4. Follow the change protocol: feature branch, PR, full CI green at the exact
   head, exact-head squash-merge, post-merge verification.
5. Update this file, `meta/CURRENT-STATE.md`, and (for significant decisions)
   `meta/memory/DECISIONS.md` in the same delivery cycle.

## Update rules for this file

- Keep the standing queue current whenever an item completes or blocks.
- Treat this mandate as subordinate to the Human Owner's authority; the owner
  may override any item here, recorded as a decision.
- Never delete the non-negotiable invariants; propose changes through a PR that
  does not weaken any gate.

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
   the adoption guide for external candidates is published
   (`benchmarks/ADOPTION-GUIDE.md`, linked from the protocol). The generalized external-candidate runner is published
   (`tools/run_external_candidate.py`: NDJSON serve/record adapter protocol with
   ground truth stripped from served cases, raw-trace sha256 digests, a copy
   guard against the dataset expected records, mandatory overlap disclosure,
   and contract scorer invocation for CAP-011 and CAP-014); external results
   themselves remain gated on a real external runtime (queue item 3).
   No new registry authority is created.
2. **Strengthen public distribution** — keep the Pages discovery surface,
   `docs/api/skills.json`, and the multi-platform Agent Skills compatibility
   (agentskills.io open format) as the primary distribution story.
   Status: live; hardening is continuous. 2026-10-14: the committed Skills
   API projection (`docs/api/skills.json`, `skills.yaml`, `skills-schema.json`,
   JSON-LD) is machine-verified fresh against the canonical corpus by
   `tests/test_skills_api_freshness.py` on every push (git-derived timestamp
   fields excluded), so export-PR staleness now fails CI instead of publishing
   drift. The committed skills-graph projections
   (`data/SKILLS_GRAPH.json`, `docs/api/graph.json`) are machine-verified
   fresh the same way by `tests/test_graph_projection_freshness.py`. The Pages
   landing page (`docs/index.md`) and the committed README skill counts are
   patched by the same count tool and machine-verified fresh by
   `tests/test_update_readme_counts.py`. The Pages deploy itself is now self-healing: `deploy-pages.yml` gained a `staleness-gate` job plus a six-hourly schedule that re-deploys when the live `github-pages` deployment does not serve the main tip (same pattern as the release self-heal), so a transient `actions/deploy-pages` failure can no longer leave the public site silently stale. The deploy action itself was root-caused and fixed: `actions/deploy-pages@v4` (node20 build) is systematically broken by the runner-side forced Node 24 and is now pinned to the upstream Node-24 release `v5.0.1`. The orphaned synthetic-heartbeat artifacts (the frozen `docs/heartbeat.json` on the public Pages surface and the stale `meta/heartbeat.yml` claiming automation) are removed; live uptime monitoring remains `uptime-monitor.yml` plus the hourly release self-heal. The post-deploy served-bytes verification is now propagation-tolerant: observed on the `c01d1dff` deploy, `actions/deploy-pages@v5.0.1` published successfully but the single immediate verification pass hit stale CDN bytes and falsely failed the job, so `tools/verify_agent_skills_discovery.py` gained `--max-attempts`/`--retry-delay` whole-pass retries (fail-closed; machine-verified by `tests/test_verify_agent_skills_discovery.py`) and `deploy-pages.yml` verifies with `--max-attempts 5 --retry-delay 30`. Honest open status: the post-deploy verification still fails deterministically on live deploys (`c01d1dff`, `34317b30`) even though the deployments publish correctly and the served bytes re-verify against the committed digests; the verifier now emits workflow-command annotations so the next deploy run reveals the exact failing URL or status through the check-runs annotations API — diagnose from that evidence before changing any retry or verification behavior. Resolution (same day): the diagnosis annotations exposed exit 127 — the retry flags had been appended on a separate shell line and never reached the verifier; the single-pass verification itself succeeded on `60b7308c` (earlier failures were genuine CDN-propagation races), and the step is now a properly continued single command that actually exercises the `--max-attempts 5 --retry-delay 30` retrying verification on every deploy. 2026-10-15: the post-expansion generated-projection republication wave (quality report #591, graph #592, README counts #593, Skills API #594, badges #595, search index #597; duplicate #596 closed as already applied) is merged at exact heads with full CI via the documented App-authored identical-content recommit workaround, and the deterministic discovery-count contract is repaired by #598 (the pre-expansion 861 constant in `tests/test_agent_skills_discovery.py` had kept `main` red through the wave; the live projection carries 912 eligible packages for the 939-skill corpus), restoring fully green push CI on `main`. 2026-10-16: the next assigned
   distribution-hardening slice is the search-index skills-freshness
   contract, assigned to the newly hired Counsel agent
   (`meta/COUNSEL_CHARTER.md`): re-derive the search corpus in-memory from
   canonical `skills/` and require equality with the committed
   `data/search-index.json` and `docs/search-index.json` in the pattern of
   the Skills-API (#581) and graph (#582) freshness contracts — the
   2026-10-15 batch-2 automation encoding defect that corrupted the pushed
   search-index copy stayed CI-green because no such contract exists. 2026-10-16 (Counsel cycle 1): delivered as PR #616 — `tests/test_search_index_freshness.py` re-derives the search projection in-memory from canonical `skills/` via `tools.build_search_index.build_index` (shared `tools/skill_corpus.py` boundary, deterministic sorted iteration, no file writes, no second index or parser) and requires parsed equality with the committed `data/search-index.json` and `docs/search-index.json` plus byte-identity with the generator's canonical serialization (`json.dumps(..., ensure_ascii=False, indent=2)` + trailing newline); the projection has no git-derived timestamp fields, so there are no exclusions (unlike #581/#582). The batch-2 defect class — double-encoded non-ASCII or any serialization drift that still parses equal — now fails CI. No gate weakened, no workflow changes.
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

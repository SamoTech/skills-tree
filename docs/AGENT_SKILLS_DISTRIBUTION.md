# Agent Skills Distribution Contract

## Purpose

Skills Tree is a public, trusted, machine-discoverable source of AI skills. The repository supports GitHub-native consumption and a standards-compatible Agent Skills distribution without creating competing sources of truth.

## Canonical source

`skills/` is authoritative.

`agent-skills/` is a deterministic compatibility projection generated from eligible canonical entries. It is never an independently authored source of truth.

`docs/api/skills.json` is the machine-readable registry projection. Search projections remain separate search-only artifacts.

## Verified Agent Skills baseline — 2026-10-06

- 382 canonical skill entries scanned.
- 264 eligible deterministic projections.
- 118 blocked canonical entries.
- 302 Agent Skills packages.
- 264 deterministic eligible projections.
- 37 retained blocked packages.
- 1 intentional auxiliary package: `skills-tree-registry`.
- 1 legacy compatibility package: `rag`.

Reconciliation is a read-only CI invariant:

~~~bash
python tools/reconcile_agent_skills.py --check
~~~

The gate fails for eligible missing projections, deterministic projection drift, stale or ambiguous provenance, unexpected packages, and unresolved target-name collisions. `rename_needed` is compatibility metadata and is not itself a failure.

## Discovery publication contract

The discovery index is generated from the same reconciled Agent Skills projection. It is not hand-authored and does not introduce a second eligibility or package generator.

~~~bash
python tools/build_agent_skills_discovery.py \
  --output site/.well-known/agent-skills/index.json
~~~

The builder:

1. executes the existing reconciliation contract;
2. reuses canonical projection naming and eligibility logic;
3. refuses reconciliation failures;
4. verifies every eligible published `SKILL.md` against the deterministic projection;
5. computes SHA-256 over the exact published bytes;
6. emits a stable name-sorted discovery index;
7. validates the result against `meta/agent-skills-discovery-index.schema.json`.

The index uses the documented v0.2.0-compatible fields: `$schema`, `skills[]`, `name`, `type`, `description`, `url`, and `digest`.

Blocked and legacy-only packages are not published merely because they exist in the repository.

## Publication artifact

`.github/workflows/deploy-pages.yml` remains the single Pages deployment authority.

The Pages build stages:

~~~text
site/
├── agent-skills/<name>/SKILL.md
└── .well-known/agent-skills/index.json
~~~

The index and artifacts are produced in the same Pages build output. Local publication verification checks every staged `SKILL.md` digest before upload.

After deployment, the workflow fetches the served index and every advertised skill artifact and verifies the served bytes against the published SHA-256 digests.

## Hosting boundary

The current site is a GitHub Pages project site at:

`https://samotech.github.io/skills-tree`

Therefore the currently verifiable discovery URL is:

`https://samotech.github.io/skills-tree/.well-known/agent-skills/index.json`

This is intentionally not declared to be the standards root endpoint:

`https://<domain>/.well-known/agent-skills/index.json`

GitHub documents that project Pages sites are served under the repository-name path, while custom domains can change the site root.

A future root endpoint may be activated only after a verified root-capable user/organization Pages site or custom domain exists and the published URLs are updated accordingly. The repository must not claim root-level discovery while it is hosted as a project site.

## Integrity and provenance

Every published skill is traceable to:

- its canonical `skills/` source;
- its deterministic `agent-skills/<name>/SKILL.md` projection;
- its stable package name;
- its exact published bytes;
- its SHA-256 digest.

The publication boundary does not infer trust, evidence, maturity, popularity, or benchmark results from package presence.

## CI completion gates

A distribution publication is incomplete unless applicable gates pass:

1. canonical source validation;
2. Agent Skills validation;
3. deterministic reconciliation;
4. deterministic discovery-index generation;
5. discovery-index schema validation;
6. local artifact byte/digest verification;
7. Pages artifact verification;
8. deployment;
9. served index and served-artifact digest verification;
10. synchronized documentation/current-state records.

## Anti-duplication rule

Do not add:

- another Agent Skills generator;
- another reconciliation engine;
- another search index;
- a hand-maintained discovery catalog;
- a second Pages deployment workflow;
- inferred trust/evidence/ranking fields in the discovery index.

Future changes must reuse the canonical source and existing deterministic projection/reconciliation boundaries.

## Live reconciliation verification — 2026-10-06

The latest exact-head Agent Skills Distribution Audit verified 382 canonical entries, 264 eligible projections, 118 blocked canonical entries, and 302 existing Agent Skills packages.

Reconciliation reported no eligible missing projections, deterministic projection drift, stale entries, unexpected packages, ambiguous provenance, or unresolved target-name collisions.

The older 2026-10-04 baseline is superseded by this live verified baseline; historical records elsewhere remain historical.
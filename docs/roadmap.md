# Roadmap

See the full tracking document: [`meta/ROADMAP.md`](https://github.com/SamoTech/skills-tree/blob/main/meta/ROADMAP.md)

Status reconciled against live main on 2026-11-27 (registry: 2488 public skills; quality corpus 2489 files including one intentional sandbox fixture).

## Shipped

- [x] Skill dependency graph — generated projections (`data/SKILLS_GRAPH.json`, `docs/api/graph.json`) plus the interactive viewer (`docs/graph.html`)
- [x] JSON/YAML export of all skill metadata — `docs/api/skills.json`, `docs/api/skills.yaml`, per-skill JSON-LD
- [x] CLI recommendation — `skills-tree recommend --goal "..."` (taxonomy/graph-based)
- [x] PyPI package with OIDC publishing
- [x] Semantic release automation
- [x] GitHub Pages documentation site
- [x] 10-language localized READMEs
- [x] MCP server integration
- [x] Automated quality scoring
- [x] MkDocs Material documentation platform

## Near-Term (v2.x)

- [ ] Skill Paths — curated learning tracks (e.g., "Build a Research Agent in 5 skills")
- [ ] Community skill ratings and upvotes
- [ ] Recommendation-quality benchmarking — Top-K relevance evaluation for `skills-tree recommend` / `skills-tree search`
- [ ] Coverage to 80%+ on the test suite

## Medium-Term (v3.0)

- [ ] LangChain Hub / MCP registry integration
- [ ] Semantic-similarity recommendation upgrade (recommend is taxonomy/graph-based today)
- [ ] Agent-runtime adapters beyond the Agent Skills open format

## Long-Term Vision

- Skills Tree becomes the canonical reference for AI agent capabilities
- Battle-tested coverage for every public skill, with benchmark-backed evidence for performance claims
- Multi-language skill index (not just localized READMEs)

*(Historical numeric scale targets — "500+ skills", "1000+ skills" — were retired on 2026-11-27: the registry has passed both; the priority is now quality, evidence, and adoption. Tracking: issue #730.)*

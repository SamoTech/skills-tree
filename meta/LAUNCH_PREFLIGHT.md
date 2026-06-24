# LAUNCH PREFLIGHT CHECKLIST

**Initiative:** INITIATIVE-014B  
**Date:** 2026-06-24 (pre-flight) | Launch: 2026-06-30 09:00 ET  
**Owner:** Release Manager

---

## Phase 1 — Asset Verification

| Asset | Status | URL / Path | Notes |
|---|---|---|---|
| README hero | ✅ GREEN | `README.md` | AI OS tagline, stat trio, 3 CTAs above fold |
| Response SLA | ✅ GREEN | `README.md` line 32 | Issues <72h, PRs <7d, Governance <5d |
| Explorer live | ✅ GREEN | https://samotech.github.io/skills-tree/explorer/ | V2: Featured, Paths, Surprise Me, `#skill=` |
| Explorer hotfix | ✅ GREEN | `docs/explorer/app.js` | 012B1 path normalization deployed |
| Blueprints live | ✅ GREEN | https://samotech.github.io/skills-tree/blueprints/ | Blueprint Generator accessible |
| Python package | ✅ GREEN | https://pypi.org/project/skills-tree/ | `pip install skills-tree` |
| MCP server | ✅ GREEN | `mcp/` | Documented in README architecture |
| CONTRIBUTING.md | ✅ GREEN | `CONTRIBUTING.md` | PR templates, skill template, SLA |
| QUICKSTART | ✅ GREEN | `docs/quickstart.md` | pip install + 3 CLI examples |
| Launch copy | ✅ GREEN | `meta/LAUNCH_ASSET_PACK.md` | 6 surfaces written and reviewed |
| Shareable URLs | ✅ GREEN | `#skill=<id>` scheme | pushState + popstate + clipboard |
| GitHub Discussions | ⏳ PENDING | Enable in repo settings before T-1 | 4 threads ready to post |
| OG image | ⚠️ OPTIONAL | Not blocking | Social preview image improves X/LinkedIn CTR |
| `good first issue` labels | ⚠️ OPTIONAL | Not blocking | Pre-populate on 3 stub skills |

---

## Launch Sequence (June 30)

```
T-1 day  (June 29, 16:00 EEST)
  └─ Post GitHub Discussion — Welcome + Roadmap threads

T-0 (June 30, 16:00 EEST = 09:00 ET)
  ├─ LinkedIn post (founder story)
  ├─ X/Twitter thread (simultaneous)
  └─ Show HN post

T+1h (17:00 EEST)
  └─ Reddit posts — r/MachineLearning, r/LocalLLaMA, r/ArtificialIntelligence

T+4h (20:00 EEST)
  └─ First war room check — stars, comments, issues, traffic

T+24h (June 31, 16:00 EEST)
  └─ 24h audit — update LAUNCH_DASHBOARD.md
  └─ Reply to every HN comment
  └─ Triage all GitHub issues
  └─ Post Day 1 recap
```

---

## Blocking Checks

Do NOT launch if any of these are RED:

- [ ] Explorer loads on GitHub Pages (test at https://samotech.github.io/skills-tree/explorer/)
- [ ] `pip install skills-tree` completes successfully
- [ ] README renders correctly on github.com (check hero above fold)
- [ ] `#skill=09-agentic-patterns/react` deep-link opens correct detail panel
- [ ] Show HN title and body final-reviewed

---

## Go/No-Go

```
LAUNCH_READINESS_SCORE = 86 / 100
THRESHOLD              = 85
GO_LIVE_DECISION       = YES
SHOW_HN_READY          = YES
```

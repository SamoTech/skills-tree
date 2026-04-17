# Issue Cleanup Log

## 2026-04-17 — Bulk close duplicate dependency advisory issues

Root cause: `osv-watch.yml` lacked a deduplication guard before `github.rest.issues.create`.
Every 15-minute cron run created a new issue when OSV hits were detected, regardless of
whether an identical open issue already existed.

Fix: commit `6aed2a0` — added a deduplication guard that lists open `dependency-advisory`
issues and skips creation if an issue with the same title already exists.

Closed as duplicates: #29, #30, #31, #32, #33, #34, #35, #36, #37, #38, #39, #40,
#41, #42, #43, #44, #45, #46, #47, #48, #49, #50, #51, #52.

Kept open (canonical): #53

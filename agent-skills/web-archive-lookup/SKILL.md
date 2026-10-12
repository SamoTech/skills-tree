---
name: web-archive-lookup
description: Query archived web snapshots through timestamped request construction and nearest-snapshot selection so historical page state is retrieved explicitly and reproducibly.
metadata:
  source: skills/11-web/web-archive-lookup.md
  category: 11-web
  version: "v1"
---

# Web Archive Lookup

Category: Web | Level: basic | Stability: experimental | Version: v1

## Description

Pages change and disappear, and an agent that cited one yesterday may need the bytes it saw, not today’s revision. Web archives answer with timestamped snapshots, but only if requests are built correctly: a canonical URL form, a timestamp in the archive’s format, and an explicit rule for choosing among nearby snapshots. This skill defines that lookup as a deterministic computation.

## When to Use

Use when verifying a citation against a prior page state, recovering deleted content for evidence, or comparing a page across time.

Do not use archived copies as a substitute for fetching the live page when current information is the requirement; archives lag and the present is authoritative.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `url` | `string` | Yes | The page URL whose history is needed |
| `timestamp` | `string` | Yes | Requested capture time in the archive’s compact format |
| `snapshots` | `list[timestamp]` | Yes | Available capture timestamps for the URL |

## Procedure

1. Normalize the URL before requesting archives; equivalent spellings fragment the snapshot history.
2. Construct the archive request with the normalized URL and the requested timestamp in the documented format.
3. When the exact timestamp is absent, select the nearest earlier snapshot under a declared rule and record both requested and selected times.
4. Report when no snapshot precedes the request; an empty history is an answer, not an error to retry.
5. Record the archive’s identifier for the chosen snapshot so the same evidence can be retrieved again.
6. Treat archived content as historical evidence with its capture date attached; undated citation of an archive is a defect.

## Outputs

| Output | Type | Description |
|---|---|---|
| `request_url` | `string` | The archive lookup URL built from the inputs |
| `snapshot` | `string | null` | The selected capture timestamp, or null when none precedes the request |

## Runnable Example

```python
ARCHIVE_BASE = "https://web.archive.org"

def wayback_url(url, timestamp):
    """Build a Wayback Machine request URL for a 14-digit timestamp."""
    clean = url.replace("http://", "").replace("https://", "")
    return f"{ARCHIVE_BASE}/web/{timestamp}/{clean}"

def closest_snapshot(snapshots, requested):
    """Select the nearest snapshot at or before the requested timestamp."""
    earlier = [s for s in snapshots if s <= requested]
    return max(earlier) if earlier else None

snapshots = ["20200101120000", "20210601120000", "20240101120000"]
requested = "20220101120000"
selected = closest_snapshot(snapshots, requested)
print(wayback_url("https://example.com/docs", selected))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Fragmented history | URL variants each archive separately | Normalize the URL before any archive request |
| Nearest-after bias | Later snapshot silently substituted | Select nearest-earlier by rule and record both times |
| Undated citations | Archive content cited without capture date | Attach the snapshot timestamp to every retrieval |
| Empty history retried | Missing snapshots treated as fetch errors | Report an empty history explicitly |
| Live/archived confusion | Historical copy cited as current fact | Label archived content with its capture date |

## Security and Authority Boundary

Archived pages are third-party records, not the original source’s word; they can be incomplete or manipulated upstream. Archive lookups grant no authority over the original site and inherit the archive’s own terms of use.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia’s overview of the Wayback Machine (https://en.wikipedia.org/wiki/Wayback_Machine).
2. The Internet Archive’s developer documentation (https://archive.org/developers/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [URL Fetching](url-fetching.md) — the transport reused for archive requests once they are built.
- [Web Search](web-search.md) — a complementary route for locating live sources when archives lack coverage.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |

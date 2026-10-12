---
name: file-download-verification
description: Trigger downloads through an authenticated browser session, wait for completion, and verify the artifact against expected name, size, media type, and checksum before downstream use.
metadata:
  source: skills/11-web/file-download-verification.md
  category: 11-web
  version: "v1"
---

# File Download Verification

Category: Web | Level: basic | Stability: experimental | Version: v1

## Description

A download is not finished when the file appears; it is finished when it is verified. The skill arms download handling before triggering the event, waits for completion with a bounded timeout, then checks size, media type, and checksum against expectations before the artifact is allowed downstream. Failures quarantine the file rather than silently passing it along.

## When to Use

Use when automation must fetch files through an authenticated or interactive browser session and must prove the result is the expected artifact rather than a truncated or substituted payload.

Do not trust the downloaded filename or extension. Verify content by checksum and media type before any downstream use, because names and extensions are attacker-controllable.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `trigger` | `object` | Yes | Action or URL that initiates the download |
| `expectations` | `object` | No | Expected size, media type, and checksum where known |
| `store_as` | `string` | No | Normalized artifact name; defaults to the observed name |

## Procedure

1. Arm download handling before triggering the event so the stream is captured from the start.
2. Trigger the download and capture the suggested filename and the serving URL as provenance.
3. Wait for completion with a bounded timeout; a partial file must fail, not pass.
4. Verify size, media type, and when provided checksum against the expectations.
5. Store the artifact under a collision-free normalized name with its provenance metadata.
6. Report verification results and quarantine any file that fails a check.

## Outputs

| Output | Type | Description |
|---|---|---|
| `artifact` | `object` | Stored file path and normalized name |
| `verification` | `object` | Per-check results and overall pass or quarantine verdict |
| `provenance` | `object` | Serving URL, observed filename, and capture timestamp |

## Runnable Example

```python
def verify_download(observed, expected):
    """observed/expected: maps with size, media_type, sha256"""
    checks = []
    for field in ("size", "media_type", "sha256"):
        if expected.get(field) is None:
            continue
        checks.append({"check": field, "ok": observed.get(field) == expected.get(field)})
    verdict = all(c["ok"] for c in checks) if checks else False
    return {"verdict": "pass" if verdict else "quarantine", "checks": checks}

print(verify_download(
    {"size": 1048576, "media_type": "application/pdf", "sha256": "9f86d081884c7d659a9f"},
    {"size": 1048576, "media_type": "application/pdf", "sha256": "9f86d081884c7d659a9f"},
))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Partial file accepted | Connection dropped mid-transfer | Verify size and checksum; never act on partial writes |
| Name spoofing | Extension suggests a benign type the content does not match | Verify media type by content, not extension |
| Wrong artifact served | Redirect or session error returned an error page instead | Compare checksum against the expectation |
| No expectation available | Checksum unknown before the run | Record verification limits explicitly instead of claiming pass |
| Download never completes | Server trickles bytes to hold the session open | Bound the wait with a timeout and fail fast |

## Security and Authority Boundary

Downloads cross a trust boundary into local storage. Verify the serving origin, quarantine unexpected artifacts, and never execute or open a downloaded file before verification, because the browser session may have been steered to serve attacker-controlled content.

## Evidence

This skill is grounded in dated public implementation references:

1. The Playwright downloads documentation (https://playwright.dev/python/docs/downloads).
2. The MDN reference for the Content-Disposition header that carries download filenames (https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [URL Fetching](url-fetching.md) — the non-browser path for artifacts that need no session or interaction.
- [Web Scraping](web-scraping.md) — extraction flows that frequently end in triggered downloads.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |

---
name: url-dom-inspection
description: Inspect authorized public URLs and DOM structures with bounded fetching and explicit provenance.
license: MIT
metadata:
  source: skills/01-perception/url-dom-inspection.md
  version: "v2"
---

# url-dom-inspection

Provide a public URL and requested extraction fields; return page metadata, text, links, structured data, and relevant DOM observations.

## Failure modes

- SSRF/private endpoints: allow only authorized public targets.
- Oversized pages: bound response bytes and extracted nodes.
- Dynamic content: distinguish fetched HTML from rendered DOM.

## Evidence

- https://agentskills.io/specification
- https://playwright.dev/python/docs/api/class-page

Evidence status: references support implementation guidance; no performance benchmark is claimed without reproducible benchmark data.

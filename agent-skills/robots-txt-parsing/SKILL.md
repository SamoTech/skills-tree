---
name: robots-txt-parsing
description: Parse robots.txt directives into per-agent allow, disallow, and crawl-delay rules with sitemap extraction so fetching decisions are made by an explicit, testable policy instead of ad-hoc checks.
metadata:
  source: skills/11-web/robots-txt-parsing.md
  category: 11-web
  version: "v1"
---

# Robots.txt Parsing

Category: Web | Level: basic | Stability: experimental | Version: v1

## Description

Politeness on the web starts with a parsed contract, not string matching. robots.txt groups directives by user-agent, allows and disallows paths, requests a crawl delay, and points to sitemaps. This skill defines a minimal deterministic parser — grouping, per-agent rule lists, sitemap collection — and a query interface so “may this agent fetch this path” is a testable function of recorded rules.

## When to Use

Use before any crawl or scrape touches a new host, and as the standing policy engine that answers per-path fetch questions during crawling.

Do not use robots.txt parsing as a legal position; it encodes machine etiquette, and separate permission, terms, and law still apply.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | Yes | Raw robots.txt body fetched from the host |
| `agent` | `string` | Yes | The requesting agent’s product token |
| `path` | `string` | No | Target path evaluated against the parsed rules |

## Procedure

1. Strip comments and blank lines before directive parsing; directives survive, decoration does not.
2. Group rules by user-agent block: directives following a User-agent line belong to that agent until the next one.
3. Collect Sitemap lines globally; they are host-level, not per-agent.
4. Store Allow, Disallow, and Crawl-delay as ordered per-agent rule lists.
5. Answer path queries by longest-prefix match, with Allow and Disallow resolved by rule specificity.
6. Treat parse failure or absence of robots.txt under the declared fallback policy — ask-permissive or ask-conservative — chosen once and recorded.
7. Re-fetch robots.txt at a bounded interval during long crawls; a cached policy outlives its welcome.

## Outputs

| Output | Type | Description |
|---|---|---|
| `rules` | `map[agent -> list[(kind, value)]]` | Parsed per-agent directive lists |
| `sitemaps` | `list[url]` | Host-declared sitemap URLs |
| `allowed` | `boolean | null` | Path decision, or null when no rule applies |

## Runnable Example

```python
def parse_robots(text):
    """Parse a minimal robots.txt into per-agent rules and sitemaps."""
    rules, sitemaps, agent = {}, [], None
    for raw in text.splitlines():
        line = raw.split("#")[0].strip()
        if not line or ":" not in line:
            continue
        key, _, value = line.partition(":")
        key, value = key.strip().lower(), value.strip()
        if key == "user-agent":
            agent = value.lower()
            rules.setdefault(agent, [])
        elif key == "sitemap":
            sitemaps.append(value)
        elif agent and key in ("allow", "disallow", "crawl-delay"):
            rules[agent].append((key, value))
    return rules, sitemaps

robots = "User-agent: *\nDisallow: /admin\nCrawl-delay: 2\n\nUser-agent: mybot\nAllow: /\nDisallow: /private\nSitemap: https://example.com/sitemap.xml"
rules, sitemaps = parse_robots(robots)
print("mybot rules:", rules["mybot"])
print("sitemaps:", sitemaps)
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Misgrouped rules | Directives attached to the wrong agent | Reset the current agent on every User-agent line |
| Prefix mismatch | Rule scope guessed instead of matched | Resolve queries by longest-prefix specificity |
| Stale policy | robots.txt cached for the crawl’s life | Re-fetch at a bounded interval and after fetcher errors |
| Comment noise | Directive values read with trailing comments | Strip comments before parsing values |
| Untracked fallback | Missing robots.txt handled by mood | Choose one fallback policy up front and record it |

## Security and Authority Boundary

Respecting robots.txt is a floor, not a license. Parsing grants no authority to fetch; authentication, terms of service, and rate limits still bind, and crawl behavior must stay within the host’s declared delay.

## Evidence

This skill is grounded in dated public implementation references:

1. RFC 9309 defining the Robots Exclusion Protocol (https://www.rfc-editor.org/rfc/rfc9309).
2. The original robots.txt specification at robotstxt.org (https://www.robotstxt.org/robotstxt.html).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Web Crawling](web-crawling.md) — the traversal that consumes this skill’s parsed per-path policy.
- [Web Scraping](web-scraping.md) — extraction flows gated by the same allow/deny decisions.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |

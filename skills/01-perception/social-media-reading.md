---
title: "Social Media Reading"
category: 01-perception
level: intermediate
stability: stable
version: v2
description: "Parse authorized social-media API responses or exported datasets into normalized posts, threads, authors, timestamps, and engagement metadata while respecting platform limits and privacy boundaries."
related: []
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-social-media-reading.json)

# Social Media Reading
Category: perception | Level: basic | Stability: stable | Version: v1

## Description
Fetch and parse posts, threads, and metadata from social media APIs and exported data dumps.

## Inputs
- `source`: API endpoint, archive ZIP, or JSON export
- `platform`: `twitter` | `reddit` | `linkedin` | `mastodon`

## Outputs
- Normalized post objects: `{id, author, text, timestamp, engagement, media}`

## Example
```python
import os
import praw
reddit = praw.Reddit(client_id=os.environ["REDDIT_CLIENT_ID"], client_secret=os.environ["REDDIT_CLIENT_SECRET"], user_agent=os.environ.get("REDDIT_USER_AGENT", "skills-tree-agent"))
for post in reddit.subreddit("python").hot(limit=10):
    print(post.title, post.score, post.url)
```

## Frameworks
| Framework | Method |
|---|---|
| Python | `praw` (Reddit), `tweepy` (X/Twitter) |
| LangChain | `RedditPostsLoader` |
| Mastodon | `mastodon.py` |

## Failure Modes
- Rate limits require exponential backoff
- Deleted posts return 404 mid-batch

## Related
- `rss-parsing.md` (11-web) · `text-reading.md`

## Changelog
- v1 (2026-04): Initial entry


## Evidence

- https://www.reddit.com/dev/api/
- https://docs.joinmastodon.org/api/
- https://docs.x.com/x-api

Evidence status: these references support implementation guidance; no performance benchmark is claimed without reproducible benchmark data.

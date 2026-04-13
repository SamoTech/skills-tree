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
import praw
reddit = praw.Reddit(client_id="...", client_secret="...", user_agent="bot/1.0")
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

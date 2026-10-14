#!/usr/bin/env python3
"""Verify discovery-index digests against local or served Agent Skills bytes."""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlparse


def digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def load_index(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_local(index: dict, site_root: Path) -> None:
    for item in index["skills"]:
        path = urlparse(item["url"]).path.lstrip("/")
        # Discovery URLs intentionally include the project-site prefix.
        marker = "/agent-skills/"
        if marker not in "/" + path:
            raise ValueError(f"skill URL has no agent-skills path: {item['url']}")
        relative = "agent-skills/" + path.split("/agent-skills/", 1)[1]
        artifact = site_root / relative
        if not artifact.is_file():
            raise ValueError(f"missing published artifact: {artifact}")
        actual = digest(artifact.read_bytes())
        if actual != item["digest"]:
            raise ValueError(f"digest mismatch for {item['name']}: {actual} != {item['digest']}")


def fetch(url: str) -> bytes:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError(f"refusing non-HTTPS URL: {url}")
    request = Request(url, headers={"User-Agent": "skills-tree-discovery-verifier/1.0"})
    with urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise ValueError(f"{url}: HTTP {response.status}")
        return response.read()


def verify_served(index_url: str, max_attempts: int = 1, retry_delay: float = 30.0) -> None:
    """Verify served bytes, retrying whole passes to tolerate CDN propagation.

    A freshly published Pages deployment is not guaranteed to be visible on
    every CDN edge the moment actions/deploy-pages reports success, so a
    single immediate pass can observe stale bytes and false-fail a green
    deployment. Retrying the whole pass (index plus every artifact) keeps the
    guarantee fail-closed: the final attempt's error propagates unchanged.
    """
    attempts = 0
    while True:
        attempts += 1
        try:
            index_bytes = fetch(index_url)
            index = json.loads(index_bytes)
            for item in index["skills"]:
                actual = digest(fetch(item["url"]))
                if actual != item["digest"]:
                    raise ValueError(
                        f"served digest mismatch for {item['name']}: {actual} != {item['digest']}"
                    )
            return
        except Exception as exc:
            if attempts >= max_attempts:
                raise
            print(f"served verification attempt {attempts}/{max_attempts} failed: {exc}")
            print(f"retrying the whole pass in {retry_delay}s (Pages CDN propagation tolerance)")
            time.sleep(retry_delay)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index-file", type=Path)
    parser.add_argument("--site-root", type=Path)
    parser.add_argument("--index-url")
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=1,
        help="whole-pass attempts for --index-url verification (>= 1)",
    )
    parser.add_argument(
        "--retry-delay",
        type=float,
        default=30.0,
        help="seconds to wait between served verification attempts (>= 0)",
    )
    args = parser.parse_args()

    if not args.index_url and (args.max_attempts != 1 or args.retry_delay != 30.0):
        parser.error("--max-attempts and --retry-delay require --index-url")
    if args.max_attempts < 1:
        parser.error("--max-attempts must be >= 1")
    if args.retry_delay < 0:
        parser.error("--retry-delay must be >= 0")

    if args.index_file and args.site_root:
        verify_local(load_index(args.index_file), args.site_root)
        print("OK: all local published Agent Skills bytes match discovery digests")
        return 0
    if args.index_url:
        verify_served(
            args.index_url, max_attempts=args.max_attempts, retry_delay=args.retry_delay
        )
        print("OK: discovery index and all served Agent Skills bytes match SHA-256 digests")
        return 0
    parser.error("provide --index-file and --site-root, or --index-url")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
